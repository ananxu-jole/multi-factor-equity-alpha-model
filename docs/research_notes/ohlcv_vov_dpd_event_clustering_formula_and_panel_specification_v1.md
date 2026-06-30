# Project Underdog - OHLCV Volatility-of-Volatility, Dispersion Path-Dependence, and Event-Clustering Formula and Panel Specification v1

## SECTION 1 - Specification Objective

This note freezes candidate ids, formulas, required OHLCV inputs, derived features, horizons, panel schema, artifact paths, contamination checks, and stop conditions for the next OHLCV-only discovery program.

Source design classification: `DESIGN_READY_WITH_RESEARCH_RISKS`.

Formula specification classification: `FORMULA_SPEC_READY_WITH_RESEARCH_RISKS`.

This is a specification-only document. It does not implement formulas, generate panels, compute IC, run redundancy screening, run refinement, run validation, modify governance, modify production registry, change thresholds, or introduce ML.

Program families:

- Family A: Volatility-of-Volatility, 5 candidates.
- Family B: Dispersion Path-Dependence, 6 candidates.
- Family C: Event Clustering, 6 candidates.

Total specified candidates: 17.

## SECTION 2 - Formula Notation

All formulas are OHLCV-only and use information available through signal date `t`.

Raw fields:

- `open[t,i]`
- `high[t,i]`
- `low[t,i]`
- `close[t,i]`
- `volume[t,i]`

Operators:

- `lag(x, n)`: value of `x` n trading days before `t`.
- `ts_mean(x, n)`: trailing n-day mean through `t`.
- `ts_std(x, n)`: trailing n-day standard deviation through `t`.
- `ts_sum(x, n)`: trailing n-day sum through `t`.
- `ts_z(x, n)`: `(x - ts_mean(x,n)) / ts_std(x,n)`, clipped only for divide-by-zero safety.
- `delta(x, n)`: `x - lag(x,n)`.
- `rank_cs(x)`: cross-sectional percentile rank by date, scaled 0 to 1.
- `z_cs(x)`: cross-sectional z-score by date.
- `clip(x, lo, hi)`: truncate to `[lo, hi]`.
- `where(condition, x, y)`: x if condition is true, otherwise y.
- `safe_div(a,b)`: `a / b` when `b` is finite and nonzero, otherwise missing.
- `neutral_if_inactive(score, active)`: `score` if active, otherwise 0.

Ranking convention:

- Higher candidate score should predict higher forward return.
- All final candidate scores are cross-sectional ranked with `rank_cs(raw_score)` unless explicitly specified as z-scored.
- Inactive observations are set to 0 before final ranking only when the formula explicitly uses `neutral_if_inactive`.

## SECTION 3 - Required Input Schema

Required raw input panel:

| column | type | required | rule |
| --- | --- | --- | --- |
| `date` | date | yes | Trading date. |
| `ticker` | string | yes | Current research ticker identifier from the existing OHLCV universe. |
| `open` | float | yes | Split-adjusted or existing project-standard open. |
| `high` | float | yes | Existing project-standard high. |
| `low` | float | yes | Existing project-standard low. |
| `close` | float | yes | Existing project-standard close. |
| `volume` | float | yes | Existing project-standard volume. |

Universe rule:

- Use the same currently available OHLCV research universe and date calendar used by recent OHLCV family discovery.
- Do not add external licensed metadata, PIT metadata, sector/industry fields, peer labels, fundamentals, options, macro, or alternative data.
- Do not change the universe definition inside this specification.

## SECTION 4 - Derived Feature Definitions

Shared ticker-level features:

| feature | definition |
| --- | --- |
| `ret_1` | `close / lag(close,1) - 1` |
| `ret_5` | `close / lag(close,5) - 1` |
| `ret_10` | `close / lag(close,10) - 1` |
| `ret_20` | `close / lag(close,20) - 1` |
| `abs_ret_1` | `abs(ret_1)` |
| `range_1` | `safe_div(high - low, close)` |
| `gap_1` | `safe_div(open, lag(close,1)) - 1` |
| `dollar_volume` | `close * volume` |
| `vol_5` | `ts_std(ret_1,5)` |
| `vol_10` | `ts_std(ret_1,10)` |
| `vol_20` | `ts_std(ret_1,20)` |
| `vol_40` | `ts_std(ret_1,40)` |
| `vov_5_20` | `ts_std(vol_5,20)` |
| `vov_10_40` | `ts_std(vol_10,40)` |
| `vov_slope_5` | `delta(vov_5_20,5)` |
| `vov_slope_10` | `delta(vov_10_40,10)` |
| `range_chop_20` | `ts_std(range_1,20)` |
| `range_chop_slope_5` | `delta(range_chop_20,5)` |
| `low_extension_20` | `1 - rank_cs(abs(ret_20))` |
| `trend_rank_20` | `rank_cs(ret_20)` |
| `rank_churn_5` | `abs(rank_cs(ret_20) - lag(rank_cs(ret_20),5))` |
| `low_churn_5` | `1 - rank_cs(rank_churn_5)` |
| `abn_volume_20` | `ts_z(log(1 + volume),20)` |
| `volume_event` | `abn_volume_20 > 1.5` |
| `range_event` | `ts_z(range_1,20) > 1.5` |
| `gap_event` | `abs(ts_z(gap_1,40)) > 1.5` |
| `return_event` | `abs(ts_z(ret_1,40)) > 1.5` |
| `vol_event` | `ts_z(abs_ret_1,40) > 1.5` |
| `event_count_1` | `volume_event + range_event + gap_event + return_event + vol_event` |
| `event_cluster_5` | `ts_sum(event_count_1 > 0,5)` |
| `event_cluster_10` | `ts_sum(event_count_1 > 0,10)` |
| `event_intensity_10` | `ts_sum(event_count_1,10)` |
| `event_decay` | `ts_sum(event_count_1,5) - ts_sum(event_count_1,10) / 2` |
| `cluster_active_10` | `event_cluster_10 >= 3` |

Shared date-level cross-sectional features, broadcast to every ticker for the same date:

| feature | definition |
| --- | --- |
| `xsec_disp_ret_1` | cross-sectional standard deviation of `ret_1` by date |
| `xsec_disp_ret_5` | cross-sectional standard deviation of `ret_5` by date |
| `xsec_disp_range_1` | cross-sectional standard deviation of `range_1` by date |
| `disp_20` | `ts_mean(xsec_disp_ret_1,20)` |
| `disp_slope_5` | `delta(disp_20,5)` |
| `disp_slope_10` | `delta(disp_20,10)` |
| `disp_accel_5` | `disp_slope_5 - lag(disp_slope_5,5)` |
| `disp_stability_10` | `-ts_std(xsec_disp_ret_1,10)` |
| `disp_relapse_10` | `where(lag(disp_slope_10,10) < 0 and disp_slope_5 > 0, 1, 0)` |
| `disp_normalizing_10` | `where(disp_slope_10 < 0, 1, 0)` |
| `disp_elevated_40` | `rank_cs(ts_mean(xsec_disp_ret_1,40))` by date history, evaluated as a time-series rank approximation if implemented |

Implementation note for `disp_elevated_40`:

- The later implementation should use a trailing time-series percentile of `disp_20` over 252 trading days if available.
- If the project lacks a time-series percentile helper, use `ts_z(disp_20,252)` and document the fallback.

## SECTION 5 - Warmup, Missing Data, Date Alignment, And Ranking Rules

Warmup:

- Minimum warmup: 252 trading days for date-level dispersion percentile features.
- If 252-day history is unavailable in early dates, candidates using `disp_elevated_40` are missing until sufficient history exists.
- Other rolling features require at least the maximum window in their formula plus 5 additional days.
- No backfilling is allowed.

Missing data:

- If any required raw OHLCV field is missing for a ticker-date, the candidate score is missing.
- If a formula-specific rolling feature is missing, the candidate score is missing.
- Infinite values must be treated as missing.
- Missing scores should not be converted to zero except explicit inactive states via `neutral_if_inactive`.

Date alignment:

- Signal at date `t` may use only OHLCV data through `t`.
- Forward returns for h1/h5/h10/h20 must start after `t` according to the existing research framework.
- Same-bar timing must be flagged in the future manifest because formulas use close/high/low/volume through `t`.

Cross-sectional ranking:

- Rank or z-score only within the active same-date research universe.
- Require at least 50 finite candidate values on a date for a cross-sectional rank.
- Dates below finite-count minimum should be marked invalid for that candidate.

## SECTION 6 - Candidate ID Table

| candidate_id | candidate_name | family | primary horizon | secondary horizons | expected sign |
| --- | --- | --- | --- | --- | --- |
| `vov_01_instability_calm_after_chop` | Volatility instability calming after choppy risk | A - Volatility-of-Volatility | h10 | h5, h20 | positive |
| `vov_02_low_extension_vov_rise` | Low-extension volatility-of-volatility rise | A - Volatility-of-Volatility | h10 | h5, h20 | positive |
| `vov_03_range_chop_exhaustion` | Range-chop exhaustion | A - Volatility-of-Volatility | h10 | h5, h20 | positive |
| `vov_04_vov_slope_divergence` | Volatility level versus volatility-instability divergence | A - Volatility-of-Volatility | h10 | h5, h20 | positive |
| `vov_05_churn_controlled_vov_stabilization` | Low-churn volatility-instability stabilization | A - Volatility-of-Volatility | h10 | h5, h20 | positive |
| `dpath_01_elevated_dispersion_stabilizing` | Elevated dispersion stabilizing | B - Dispersion Path-Dependence | h10 | h5, h20 | positive |
| `dpath_02_dispersion_relapse_resilience` | Dispersion relapse resilience | B - Dispersion Path-Dependence | h10 | h5, h20 | positive |
| `dpath_03_normalization_without_leadership_crowding` | Dispersion normalization without crowding | B - Dispersion Path-Dependence | h10 | h5, h20 | positive |
| `dpath_04_vol_dispersion_path_divergence` | Volatility-dispersion path divergence | B - Dispersion Path-Dependence | h10 | h5, h20 | positive |
| `dpath_05_low_churn_dispersion_transition` | Low-churn dispersion transition | B - Dispersion Path-Dependence | h10 | h5, h20 | positive |
| `dpath_06_dispersion_after_event_absorption` | Dispersion after event absorption | B - Dispersion Path-Dependence | h10 | h5, h20 | positive |
| `ecluster_01_multi_shock_absorption` | Multi-shock absorption | C - Event Clustering | h5 | h1, h10, h20 | positive |
| `ecluster_02_cluster_decay_stabilization` | Event-cluster decay stabilization | C - Event Clustering | h10 | h5, h20 | positive |
| `ecluster_03_isolated_vs_clustered_volume_shock` | Isolated versus clustered volume shock | C - Event Clustering | h5 | h1, h10 | positive |
| `ecluster_04_gap_range_cluster_containment` | Gap-range cluster containment | C - Event Clustering | h10 | h5, h20 | positive |
| `ecluster_05_event_cluster_low_churn_rebalance` | Low-churn event cluster rebalance | C - Event Clustering | h10 | h5, h20 | positive |
| `ecluster_06_cross_event_divergence` | Cross-event divergence | C - Event Clustering | h5 | h1, h10 | positive |

## SECTION 7 - Formula Table

All final scores below are panel output signal values. Component columns are defined in Section 9.

| candidate_id | research hypothesis | exact OHLCV-only formula | activation condition | exclusion / stop conditions | contamination checks |
| --- | --- | --- | --- | --- | --- |
| `vov_01_instability_calm_after_chop` | Names whose volatility instability calms after elevated chop should outperform as risk uncertainty resolves. | `rank_cs(rank_cs(lag(vov_5_20,5)) * rank_cs(-vov_slope_5) * rank_cs(lag(range_chop_20,5)) * rank_cs(low_extension_20))` | `lag(vov_5_20,5)` above date median and `vov_slope_5 < 0`. | Stop if active dates below 10% or max corr to volatility compression reference exceeds 0.70. | Volatility compression, stress repair, rank-coherence. |
| `vov_02_low_extension_vov_rise` | Rising VOV with low price extension may mark early repricing before mature momentum. | `rank_cs(rank_cs(vov_slope_5) * rank_cs(low_extension_20) * (1 - rank_cs(abs(ret_5))) * rank_cs(dollar_volume))` | `vov_slope_5 > 0` and `abs(ret_20)` below date median. | Stop if max momentum corr exceeds 0.60 or h1 dominates all medium horizons. | Momentum, plain reversal, volatility level. |
| `vov_03_range_chop_exhaustion` | Repeated range chop that starts compressing may identify exhaustion of disorder. | `rank_cs(rank_cs(lag(range_chop_20,5)) * rank_cs(-range_chop_slope_5) * rank_cs(-abs(ret_10)) * rank_cs(low_extension_20))` | `lag(range_chop_20,5)` above date median and `range_chop_slope_5 < 0`. | Stop if signal is positive only in panic/liquidity stress diagnostics. | Stress repair, volatility compression, reversal. |
| `vov_04_vov_slope_divergence` | Divergence between volatility level and VOV path may add information beyond volatility level. | `rank_cs(abs(rank_cs(delta(vol_20,10)) - rank_cs(vov_slope_10)) * rank_cs(low_extension_20) * rank_cs(-abs(ret_20)))` | none; continuous divergence score. | Stop if simple volatility level explains more than 70% correlation. | Simple volatility level, volatility compression, rank-coherence. |
| `vov_05_churn_controlled_vov_stabilization` | VOV stabilization with low rank churn should be cleaner than noisy instability. | `rank_cs(rank_cs(-vov_slope_10) * rank_cs(lag(vov_10_40,10)) * rank_cs(low_churn_5) * rank_cs(low_extension_20))` | `lag(vov_10_40,10)` above date median and `vov_slope_10 < 0`. | Stop if max corr to rank-coherence exceeds 0.65 or active dates below 12%. | Rank-coherence, persistence, volatility compression. |
| `dpath_01_elevated_dispersion_stabilizing` | Names stable during elevated but calming dispersion may benefit from orderly cross-sectional normalization. | `rank_cs(rank_cs(disp_elevated_40) * rank_cs(-disp_slope_10) * rank_cs(low_churn_5) * rank_cs(-abs(ret_10)))` | `disp_elevated_40 > 0.60` and `disp_slope_10 < 0`. | Stop if h20 is negative and h5/h10 are flat, matching prior dispersion decay. | Dispersion anchor, rank-coherence, stress repair. |
| `dpath_02_dispersion_relapse_resilience` | Names resilient during dispersion relapse after calm may capture path-specific strength. | `neutral_if_inactive(rank_cs(rank_cs(ret_5) * rank_cs(low_churn_5) * rank_cs(low_extension_20)), disp_relapse_10 == 1)` | `disp_relapse_10 == 1`. | Stop if active dates below 8% or one-window dominance above 0.75. | Persistence, rank-coherence, stress repair. |
| `dpath_03_normalization_without_leadership_crowding` | Dispersion normalization should help low-extension improvers, not crowded leaders. | `neutral_if_inactive(rank_cs(rank_cs(ret_5) * rank_cs(low_extension_20) * (1 - trend_rank_20) * rank_cs(-rank_churn_5)), disp_normalizing_10 == 1)` | `disp_normalizing_10 == 1`. | Stop if max corr to parked non-hostile leadership references or momentum exceeds 0.60. | Momentum, parked OHLCV leadership, rank-coherence. |
| `dpath_04_vol_dispersion_path_divergence` | Divergence between volatility path and dispersion path may indicate uneven repricing. | `rank_cs(abs(rank_cs(disp_slope_10) - rank_cs(delta(vol_20,10))) * rank_cs(low_extension_20) * rank_cs(low_churn_5))` | none; continuous divergence score. | Stop if max corr to VOV candidates exceeds 0.80 and no independent family behavior appears. | VOV family, simple dispersion, simple volatility. |
| `dpath_05_low_churn_dispersion_transition` | Dispersion transitions with low rank churn may preserve useful structure without pure rank-coherence. | `rank_cs(rank_cs(abs(disp_slope_10)) * rank_cs(low_churn_5) * rank_cs(low_extension_20) * (1 - rank_cs(abs(ret_20))))` | `abs(disp_slope_10)` above its trailing median approximation. | Stop if rank-coherence corr exceeds 0.65 or dispersion-anchor corr exceeds 0.75. | Rank-coherence, dispersion anchor, persistence. |
| `dpath_06_dispersion_after_event_absorption` | Names stabilizing after clustered events while dispersion remains elevated may show delayed absorption. | `neutral_if_inactive(rank_cs(rank_cs(low_churn_5) * rank_cs(-abs(ret_5)) * rank_cs(low_extension_20) * rank_cs(disp_elevated_40)), event_cluster_10 >= 3 and disp_elevated_40 > 0.60)` | `event_cluster_10 >= 3` and `disp_elevated_40 > 0.60`. | Stop if event-cluster overlap makes it indistinguishable from Family C. | Event clustering, volume shock reversal, dispersion anchor. |
| `ecluster_01_multi_shock_absorption` | Absorbing several shock types without extreme extension may indicate resilient demand. | `neutral_if_inactive(rank_cs(rank_cs(event_intensity_10) * rank_cs(-abs(ret_5)) * rank_cs(low_extension_20) * rank_cs(low_churn_5)), cluster_active_10)` | `cluster_active_10`. | Stop if active dates below 8% or max volume shock reversal corr exceeds 0.65. | Volume shock reversal, plain reversal, stress repair. |
| `ecluster_02_cluster_decay_stabilization` | Stabilization as event clusters decay may capture exhaustion of forced adjustment. | `rank_cs(rank_cs(-event_decay) * rank_cs(lag(event_intensity_10,5)) * rank_cs(low_churn_5) * rank_cs(low_extension_20))` | `lag(event_intensity_10,5) >= 3` and `event_decay < 0`. | Stop if h1 only or if recent-window positive rate collapses. | Volume shock reversal, volatility compression, reversal. |
| `ecluster_03_isolated_vs_clustered_volume_shock` | Isolated abnormal volume may differ from clustered volume/range shocks. | `rank_cs(rank_cs(abn_volume_20) * (1 - rank_cs(event_cluster_10)) * rank_cs(-abs(ret_1)) * rank_cs(low_extension_20))` | `volume_event` and `event_cluster_10 <= 2`. | Stop if corr to `volume_shock_reversal_stable_20` exceeds 0.70. | Volume shock reversal, plain reversal, liquidity-flow proxy. |
| `ecluster_04_gap_range_cluster_containment` | Repeated gap/range events without deterioration may identify containment. | `neutral_if_inactive(rank_cs(rank_cs(ts_sum(gap_event + range_event,10)) * rank_cs(-abs(ret_10)) * rank_cs(low_churn_5)), ts_sum(gap_event + range_event,10) >= 3)` | at least three gap/range events in 10 days. | Stop if one-window dominance above 0.75 or active dates below 6%. | Event-quality rejected candidates, reversal, stress repair. |
| `ecluster_05_event_cluster_low_churn_rebalance` | Event clusters may be useful only when rank churn is controlled. | `neutral_if_inactive(rank_cs(rank_cs(event_intensity_10) * rank_cs(low_churn_5) * rank_cs(low_extension_20) * rank_cs(-rank_churn_5)), cluster_active_10)` | `cluster_active_10`. | Stop if max rank-coherence corr exceeds 0.65 or volume shock corr exceeds 0.65. | Rank-coherence, volume shock reversal, persistence. |
| `ecluster_06_cross_event_divergence` | Disagreement among volume, range, return, and volatility events may signal non-obvious repricing. | `rank_cs(abs(rank_cs(ts_sum(volume_event,10)) - rank_cs(ts_sum(range_event + return_event + vol_event,10))) * rank_cs(low_extension_20) * rank_cs(-abs(ret_5)))` | at least one event type has 10-day count >= 2. | Stop if finite active sample is too broad to represent clustering or too sparse below 8%. | Volume shock reversal, plain reversal, volatility level. |

## SECTION 8 - Family And Horizon Mapping

| family | candidates | primary horizon policy | secondary horizon policy | success interpretation |
| --- | --- | --- | --- | --- |
| Family A - Volatility-of-Volatility | 5 | h10 primary for all candidates. | h5 for early repricing; h20 for durability only. | h10 positive evidence with low volatility-compression and stress-repair contamination. |
| Family B - Dispersion Path-Dependence | 6 | h10 primary. | h5 acceptable; h20 durability only. | h5/h10 positive evidence is enough for research interest if distinct from rank-coherence and stress repair. |
| Family C - Event Clustering | 6 | h5 primary for `ecluster_01`, `ecluster_03`, `ecluster_06`; h10 primary for others. | h1 diagnostic; h20 slow-repricing durability only. | h1-only behavior is diagnostic, not refinement-ready; h5/h10 must carry the case. |

## SECTION 9 - Panel Output Schema

Future panel output should be wide by candidate or long by candidate-date-ticker, but must preserve these fields.

Required index fields:

| column | type | required |
| --- | --- | --- |
| `date` | date | yes |
| `ticker` | string | yes |

Required per-candidate output columns:

| column pattern | type | description |
| --- | --- | --- |
| `{candidate_id}_signal` | float | Final candidate score. |
| `{candidate_id}_raw_score` | float | Formula score before final cross-sectional rank. |
| `{candidate_id}_active` | bool | Activation flag, true for continuous candidates. |
| `{candidate_id}_family` | string | `vov`, `dpath`, or `ecluster`. |
| `{candidate_id}_primary_horizon` | string | Frozen primary horizon. |
| `{candidate_id}_missing_reason` | string | Null or reason code. |

Required shared diagnostic columns:

- `ret_1`
- `ret_5`
- `ret_10`
- `ret_20`
- `vol_5`
- `vol_20`
- `vov_5_20`
- `vov_10_40`
- `range_chop_20`
- `low_extension_20`
- `rank_churn_5`
- `low_churn_5`
- `event_cluster_10`
- `event_intensity_10`
- `disp_20`
- `disp_slope_10`
- `disp_relapse_10`
- `disp_normalizing_10`
- `disp_elevated_40`

Missing reason vocabulary:

- `raw_ohlcv_missing`
- `rolling_warmup`
- `insufficient_cross_section`
- `nonfinite_feature`
- `inactive_zeroed`
- `date_level_feature_missing`

## SECTION 10 - Artifact Path Plan

Future artifact root:

`artifacts/research/ohlcv_vov_dispersion_path_dependence_event_clustering_discovery_v1/`

Planned future artifacts:

- `candidate_registry.csv`
- `candidate_formula_manifest.csv`
- `required_input_schema.csv`
- `derived_feature_manifest.csv`
- `panel_manifest.csv`
- `panel_integrity_summary.csv`
- `candidate_horizon_ic_scores.csv`
- `daily_ic_by_candidate_horizon.csv`
- `family_horizon_summary.csv`
- `candidate_rankings.csv`
- `state_attribution_summary.csv`
- `redundancy_contamination_summary.csv`
- `coactivation_summary.csv`
- `turnover_churn_summary.csv`
- `window_diagnostics.csv`
- `stop_condition_report.csv`
- `manifest.json`

This specification does not create those artifacts.

## SECTION 11 - Contamination And Redundancy Controls

Required future reference comparisons:

- hostile/stress repair: `participation_liquidity_state_shift_20_60`, `participation_breadth_repair_under_hostile_trend`;
- volatility compression: `volatility_compression_after_stress_stabilization`;
- volume shock reversal: `volume_shock_reversal_stable_20`;
- persistence: `post_drawdown_persistence_churn_adjusted_20`;
- rank-coherence: `rank_coherence_churn_avoidance_02_overlap_adjusted`;
- dispersion anchors: `dispersion_transition_acceleration_20`, `dispersion_transition_acceleration_neutralized_20`;
- simple references: plain reversal, momentum/trend, simple volatility level, simple dispersion level.

Required future diagnostics:

- pairwise signal correlation;
- active co-activation;
- active-date overlap by family;
- top/bottom overlap if existing tooling supports it;
- horizon concentration;
- WFV-style window concentration;
- one-window dominance;
- turnover proxy;
- rank-churn proxy;
- state attribution;
- max absolute correlation by contamination family.

This specification does not run those checks.

## SECTION 12 - Stop Conditions

Candidate-level stop conditions:

- Active date ratio below 6% for event-cluster candidates or below 8% for all other activated candidates.
- Valid finite cross-sectional score count below 50 on most dates.
- h1-only positive evidence with flat or negative h5/h10/h20.
- Max absolute correlation above 0.70 to an existing single reference unless explicitly expected and reviewed.
- One-window dominance above 0.75.
- Same mechanism cannot be interpreted after negative evidence.

Family-level fail-fast criteria:

- Fewer than two candidates in a family produce positive primary-horizon mean IC in first-pass discovery.
- Family mean primary-horizon IC is negative and no candidate has a distinct diagnostic role.
- Family's strongest candidate is also highly contaminated with stress repair, volume shock reversal, persistence, or rank-coherence.
- Family evidence depends only on panic/drawdown/weak-breadth states.
- Candidate outcomes are internally contradictory with no interpretable state-path explanation.

Program-level stop conditions:

- More than half of positive candidates are redundant with existing hostile/stress repair or volume shock reversal references.
- All apparent effects are h1-only.
- No family produces a candidate with interpretable h5 or h10 evidence.
- Missingness or warmup rules invalidate too much of the research period.

## SECTION 13 - Explicit Non-Goals

This specification does not:

- implement formulas;
- create or edit pipeline code;
- generate candidate panels;
- compute IC;
- run redundancy screening;
- run refinement;
- run validation;
- modify governance;
- modify production registry;
- change thresholds;
- introduce ML;
- use external data;
- use PIT metadata;
- use static sector, industry, peer, company, fundamental, options, macro, or alternative data.

## SECTION 14 - Readiness Classification

Classification: `FORMULA_SPEC_READY_WITH_RESEARCH_RISKS`.

Rationale:

- All 17 candidates are specified with frozen ids, formulas, required inputs, horizons, panel columns, stop conditions, and contamination checks.
- The specification is implementable using current OHLCV-derived research infrastructure.
- Research risks remain material: stress-repair contamination, rank-coherence overlap, volume-shock reversal overlap, event-cluster sparsity, and prior dispersion h20 decay.
- Implementation should proceed only as a separate task using this frozen specification.

## SECTION 15 - Verification

Verification for this note:

- Required sections exist: specification objective, candidate ID table, formula table, family/horizon mapping, required input schema, derived feature definitions, panel output schema, artifact path plan, contamination and redundancy controls, warmup/missing-data/date-alignment rules, stop conditions, explicit non-goals, and readiness classification.
- All 17 candidates are specified: 5 Family A, 6 Family B, and 6 Family C.
- Classification appears as `FORMULA_SPEC_READY_WITH_RESEARCH_RISKS`.
- Documentation only: no implementation, panel, IC, validation, governance, production, threshold, or ML files were changed.
