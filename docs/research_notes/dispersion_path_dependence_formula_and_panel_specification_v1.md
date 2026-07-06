# Project Underdog - Dispersion Path-Dependence Formula and Panel Specification v1

## SECTION 1 - Executive Summary

Classification: `FORMULA_SPEC_READY_WITH_SCIENTIFIC_NOTES`

This note specifies the Platform v2 formula and panel plan for the first Dispersion Path-Dependence research module batch.

This is a specification-only task. It does not implement formulas, generate panels, compute IC, run validation, modify governance decisions, modify the production registry, change thresholds, or introduce ML.

The specification is constrained by the approved scientific lineage:

- Platform v2 Scientific Standard: `PLATFORM_V2_SCIENTIFIC_STANDARD_APPROVED`
- Scientific Review: `SCIENTIFIC_GATE_APPROVED_WITH_NOTES`
- Research Module Design: `DESIGN_READY_WITH_SCIENTIFIC_NOTES`
- Scientific Mechanism Review: `MECHANISM_REVIEW_READY_WITH_NOTES`
- Candidate Allocation: `CANDIDATE_ALLOCATION_READY_WITH_NOTES`

First-batch candidates:

| candidate_id | candidate_name | mechanism family | primary horizon | expected sign |
| --- | --- | --- | --- | --- |
| `dpath_01_relapse_resilience_after_calm` | Relapse Resilience After Temporary Calm | Disagreement Relapse Resilience | h10 | positive |
| `dpath_02_disagreement_vol_stress_divergence` | Disagreement Path Divergence From Volatility/Stress | Disagreement Path Divergence | h10 | positive |
| `dpath_03_elevated_disagreement_stabilization` | Elevated Disagreement Stabilization | Elevated Disagreement Stabilization | h10 | positive |
| `dpath_04_consensus_without_crowding` | Consensus Formation Without Crowding | Consensus Formation Without Crowding | h10 | positive |

Candidate budget:

- Total specified candidates: 4.
- Platform v2 default range: 4 to 6.
- Deferred mechanism excluded: Smooth Versus Burst Resolution.
- No parameter grid, broad search, target hacking, or horizon shopping is authorized.

Artifact root for future panel generation:

`artifacts/research/dispersion_path_dependence_research_module_v1/panel_v1/`

This note does not create that directory or any artifact files.

## SECTION 2 - Materials Reviewed

Reviewed:

- `docs/research_notes/project_underdog_platform_v2_scientific_research_standard_v1.md`
- `docs/research_notes/dispersion_path_dependence_scientific_review_v1.md`
- `docs/research_notes/dispersion_path_dependence_research_module_design_v1.md`
- `docs/research_notes/dispersion_path_dependence_scientific_mechanism_review_v1.md`
- `docs/research_notes/dispersion_path_dependence_candidate_allocation_and_formula_planning_v1.md`
- `docs/research_notes/project_underdog_research_state_audit_v1.md`
- `docs/research_notes/project_underdog_master_status_recap_2026-06-17.md`
- `docs/research_notes/candidate_consolidation_workplan_v1.md`
- `docs/research_notes/alpha_research_frontier_reassessment_and_next_discovery_program_v1.md`

## SECTION 3 - Lifecycle Placement

Current phase:

- Formula and Panel Specification under Platform v2.

Prior completed phases:

1. Scientific review.
2. Research module design.
3. Scientific mechanism review.
4. Candidate allocation and formula planning.

Future phases only:

1. Implementation.
2. Implementation review.
3. Panel generation.
4. Panel audit.
5. IC discovery.
6. Research review.
7. Governance decision.
8. Master state update.

No validation, refinement, production registration, threshold change, or ML work is authorized by this specification.

## SECTION 4 - Formula Notation and Shared Feature Definitions

All formulas are OHLCV-only and after-close. Signal date `t` may use only open, high, low, close, adjusted close if available, and volume through the close of `t`.

Notation:

| symbol | meaning |
| --- | --- |
| `close_t` | Adjusted close if the existing research dataset provides adjusted close; otherwise close. |
| `open_t`, `high_t`, `low_t`, `volume_t` | Same-date OHLCV fields. |
| `ret_k` | `close_t / close_{t-k} - 1`. |
| `range_1` | `(high_t - low_t) / close_t`. |
| `range_k` | `mean_ts(range_1, k)`. |
| `vol_k` | `std_ts(ret_1, k)`. |
| `drawdown_20` | `close_t / max_ts(close, 20) - 1`. |
| `dollar_volume_20` | `mean_ts(close * volume, 20)`. |
| `rank_cs(x)` | Same-date cross-sectional percentile rank over finite active-universe values, scaled 0 to 1. |
| `z_ts(x, k)` | Trailing time-series z-score using only history through `t`. |
| `delta(x, k)` | `x_t - x_{t-k}`. |
| `lag(x, k)` | Value of `x` at `t-k`. |
| `median_ts(x, k)` | Trailing median using only history through `t`. |
| `mean_ts(x, k)` | Trailing mean using only history through `t`. |
| `std_ts(x, k)` | Trailing standard deviation using only history through `t`. |
| `median_cs(x)` | Same-date cross-sectional median. |
| `mean_cs(x)` | Same-date cross-sectional mean over finite active-universe values. |
| `mad_cs(x)` | Same-date median absolute deviation over finite active-universe values. |
| `active_rank(raw, active)` | If `active` is true and raw is finite, output `rank_cs(raw)`; if inactive, output neutral value `0.5` and `is_active = false`; if required data are missing, output null with a missing reason. |

Shared cross-sectional disagreement features:

| feature | exact definition | purpose |
| --- | --- | --- |
| `disp_1` | `mad_cs(ret_1)` | Daily cross-sectional disagreement footprint. |
| `disp_5` | `mean_ts(disp_1, 5)` | Short disagreement state. |
| `disp_10` | `mean_ts(disp_1, 10)` | Medium disagreement state. |
| `disp_20` | `mean_ts(disp_1, 20)` | Current static dispersion anchor state. |
| `disp_z_20` | `z_ts(disp_20, 252)` | Normalized static dispersion level. |
| `disp_slope_5` | `disp_5 - lag(disp_5, 5)` | Short disagreement path change. |
| `disp_slope_10` | `disp_10 - lag(disp_10, 10)` | Medium disagreement path change. |
| `disp_accel_5_10` | `disp_slope_5 - lag(disp_slope_5, 5)` | Diagnostic acceleration control; not a primary mechanism. |

Shared volatility and stress features:

| feature | exact definition | purpose |
| --- | --- | --- |
| `mkt_vol_20` | `median_cs(vol_20)` | Market-wide realized volatility level. |
| `mkt_vol_slope_10` | `mkt_vol_20 - lag(mkt_vol_20, 10)` | Volatility path reference. |
| `mkt_range_20` | `median_cs(range_20)` | Range/chop reference. |
| `stress_score_i` | `(rank_cs(-ret_5) + rank_cs(range_20) + rank_cs(-drawdown_20)) / 3` | Security-level OHLCV stress proxy. |
| `mkt_stress_20` | `mean_cs(stress_score_i)` | Market-wide stress proxy. |
| `mkt_stress_slope_10` | `mkt_stress_20 - lag(mkt_stress_20, 10)` | Stress path reference. |
| `vov_5_20` | `std_ts(vol_5, 20)` | VoV contamination control. |
| `vov_path_10` | `median_cs(vov_5_20) - lag(median_cs(vov_5_20), 10)` | VoV path control. |

Shared security-level controls:

| feature | exact definition | purpose |
| --- | --- | --- |
| `rank_ret_5` | `rank_cs(ret_5)` | Recent relative behavior. |
| `low_extension_20` | `1 - rank_cs(abs(ret_20))` | Penalizes mature extension and plain momentum/reversal exposure. |
| `rank_churn_5` | `abs(rank_cs(ret_5) - lag(rank_cs(ret_5), 5))` | Rank movement instability. |
| `low_churn_5` | `1 - rank_cs(rank_churn_5)` | Rank-stability control; never a primary mechanism. |
| `liquidity_rank_20` | `rank_cs(dollar_volume_20)` | Liquidity/coverage diagnostic. |
| `leadership_crowding_60` | `(rank_cs(ret_60) + rank_cs(abs(ret_60)) + rank_cs(low_churn_5)) / 3` | Mature leadership/crowding control for consensus candidate. |
| `emerging_improvement_5_20` | `rank_cs(ret_5 - ret_20 / 4)` | Short improvement relative to recent path. |

Minimum feature maturity:

- `ret_60` requires 60 prior sessions.
- `disp_z_20`, `mkt_vol_slope_10`, `mkt_stress_slope_10`, and z-scored path comparisons require 252 sessions of date-level feature history.
- Candidate rows before all required features are mature must be marked `feature_warmup_complete = false` and `missing_reason = rolling_warmup`.

## SECTION 5 - Candidate Registry

| candidate_id | candidate_name | mechanism family | primary horizon | secondary horizons | expected sign | status |
| --- | --- | --- | --- | --- | --- | --- |
| `dpath_01_relapse_resilience_after_calm` | Relapse Resilience After Temporary Calm | Disagreement Relapse Resilience | h10 | h5, h20 | positive | RESEARCH_ONLY |
| `dpath_02_disagreement_vol_stress_divergence` | Disagreement Path Divergence From Volatility/Stress | Disagreement Path Divergence | h10 | h5, h20 | positive | RESEARCH_ONLY |
| `dpath_03_elevated_disagreement_stabilization` | Elevated Disagreement Stabilization | Elevated Disagreement Stabilization | h10 | h5, h20 | positive | RESEARCH_ONLY |
| `dpath_04_consensus_without_crowding` | Consensus Formation Without Crowding | Consensus Formation Without Crowding | h10 | h5, h20 | positive | RESEARCH_ONLY |

Explicit exclusion:

- No Smooth Versus Burst Resolution candidate is included.
- No `dpath_05` or higher candidate ID is authorized by this specification.
- No event-clustering candidate is authorized by this specification.

## SECTION 6 - Candidate Specifications

### 6.1 `dpath_01_relapse_resilience_after_calm`

Scientific lineage:

| field | specification |
| --- | --- |
| hypothesis | Securities resilient during renewed disagreement after temporary calm should carry positive medium-horizon information if disagreement memory matters. |
| mechanism | Disagreement Relapse Resilience. |
| scientific question | Do securities resilient during renewed disagreement after temporary calm behave differently from securities that only appeared strong during calm? |
| expected evidence | Positive h10 primary evidence, h5 support, h20 durability only; stable active coverage across multiple relapse episodes. |
| primary falsification criterion | Park or revise if prior winners, rank persistence, or simple rising dispersion explains the signal. |
| observable implication | A calm or partially normalized disagreement state must precede renewed disagreement, and security-level resilience must be observed during the relapse. |
| expected orthogonality | Should differ from static dispersion, rank coherence, persistence, and hostile/stress repair because the activation is relapse-after-calm. |
| contamination risks | Persistence, rank coherence, hostile/stress repair, static dispersion acceleration. |

Formula specification:

| field | value |
| --- | --- |
| candidate_id | `dpath_01_relapse_resilience_after_calm` |
| candidate_name | Relapse Resilience After Temporary Calm |
| mechanism family | Disagreement Relapse Resilience |
| primary horizon | h10 |
| secondary horizons | h5, h20 |
| expected sign | positive |
| exact OHLCV-only formula | `active_rank(rank_ret_5 * low_extension_20 * low_churn_5 * liquidity_rank_20, relapse_active)` |
| activation conditions | `relapse_active = (lag(disp_z_20, 5) < 0) and (disp_z_20 > 0) and (disp_slope_5 > 0) and (disp_5 > lag(disp_5, 5))` |
| required raw inputs | `date`, `ticker`, `open`, `high`, `low`, `close` or adjusted close, `volume`. |
| derived rolling features | `ret_1`, `ret_5`, `ret_20`, `ret_60`, `dollar_volume_20`, `rank_churn_5`, `disp_1`, `disp_5`, `disp_20`, `disp_z_20`, `disp_slope_5`. |
| cross-sectional features | `rank_ret_5`, `low_extension_20`, `low_churn_5`, `liquidity_rank_20`, `disp_1`. |
| missing-data handling | Missing raw OHLCV or nonfinite required features produce null `signal_value` and controlled `missing_reason`; inactive states use neutral `0.5` and `is_active = false`. |
| warmup rules | Requires 252 sessions of date-level dispersion history and 60 security sessions for `ret_60` availability checks. |
| date alignment | Signal date `t` uses data through close `t`; h5/h10/h20 forward returns begin after `t`. |
| after-close timing policy | `after_close_t_forward_returns_after_t`. |
| output schema | Canonical long-form row with `signal_value`, `raw_score`, `pre_activation_raw_score`, `is_active`, lineage fields, timing fields, and contamination metadata. |
| artifact naming | Candidate rows written to future `dpath_signal_panel_long.parquet`; metadata entry in future `candidate_formula_manifest.csv`. |
| anchor/static-dispersion comparator requirement | Compare against `static_dispersion_anchor_20` and `dispersion_relapse_anchor_without_security_resilience`. |
| contamination checks | Persistence, rank coherence, hostile/stress repair, static dispersion acceleration, volatility compression, VoV, volume shock reversal. |

Candidate-specific stop conditions:

- Active date ratio below 8%.
- One-window dominance above 0.75.
- Maximum absolute correlation above 0.70 to rank persistence or rank coherence references.
- No h5/h10 incremental evidence beyond static dispersion relapse anchor.

### 6.2 `dpath_02_disagreement_vol_stress_divergence`

Scientific lineage:

| field | specification |
| --- | --- |
| hypothesis | Cross-sectional disagreement path may add information when it diverges from volatility, VoV, or stress-state paths. |
| mechanism | Disagreement Path Divergence. |
| scientific question | Does disagreement path contribute forward information when volatility and stress paths tell a different story? |
| expected evidence | Positive h10 primary evidence with h5 support and lower contamination versus VoV and volatility compression than stabilization concepts. |
| primary falsification criterion | Park or revise if VoV, volatility compression, or stress repair explains most behavior. |
| observable implication | Date-level disagreement path must separate from volatility or stress path, and the security score must not be a static dispersion level proxy. |
| expected orthogonality | Highest expected module orthogonality because the candidate directly tests disagreement path versus other state paths. |
| contamination risks | VoV, volatility compression, hostile/stress repair, indicator engineering without economic meaning. |

Formula specification:

| field | value |
| --- | --- |
| candidate_id | `dpath_02_disagreement_vol_stress_divergence` |
| candidate_name | Disagreement Path Divergence From Volatility/Stress |
| mechanism family | Disagreement Path Divergence |
| primary horizon | h10 |
| secondary horizons | h5, h20 |
| expected sign | positive |
| exact OHLCV-only formula | `active_rank(divergence_intensity * low_extension_20 * low_churn_5 * (1 - rank_cs(abs(ret_10))) * liquidity_rank_20, divergence_active)` |
| activation conditions | `divergence_intensity = abs(z_ts(disp_slope_10, 252) - z_ts(mkt_vol_slope_10, 252)) + abs(z_ts(disp_slope_10, 252) - z_ts(mkt_stress_slope_10, 252)); divergence_active = divergence_intensity > median_ts(divergence_intensity, 252)` |
| required raw inputs | `date`, `ticker`, `open`, `high`, `low`, `close` or adjusted close, `volume`. |
| derived rolling features | `ret_1`, `ret_5`, `ret_10`, `ret_20`, `range_20`, `vol_20`, `drawdown_20`, `dollar_volume_20`, `disp_1`, `disp_10`, `disp_slope_10`, `mkt_vol_20`, `mkt_vol_slope_10`, `mkt_stress_20`, `mkt_stress_slope_10`. |
| cross-sectional features | `low_extension_20`, `low_churn_5`, `rank_cs(abs(ret_10))`, `liquidity_rank_20`, `stress_score_i`. |
| missing-data handling | Missing raw OHLCV, missing market-state history, or nonfinite candidate features produce null `signal_value`; inactive states use neutral `0.5`. |
| warmup rules | Requires 252 sessions for all path z-scores and divergence median. |
| date alignment | Signal date `t` uses data through close `t`; h5/h10/h20 forward returns begin after `t`. |
| after-close timing policy | `after_close_t_forward_returns_after_t`. |
| output schema | Canonical long-form row with `divergence_intensity` as optional diagnostic metadata. |
| artifact naming | Candidate rows written to future `dpath_signal_panel_long.parquet`; formula lineage in future `candidate_formula_manifest.csv`. |
| anchor/static-dispersion comparator requirement | Compare against `static_dispersion_anchor_20`, `dispersion_slope_anchor_10`, `volatility_path_anchor_20`, and `stress_path_anchor_20`. |
| contamination checks | VoV, volatility compression, hostile/stress repair, static dispersion, static volatility, rank coherence, persistence. |

Candidate-specific stop conditions:

- Divergence activation below 8% of dates or so broad that it exceeds 70% of dates.
- Maximum absolute correlation above 0.70 to VoV or volatility compression references without clear incremental h5/h10 evidence.
- Evidence is positive only when volatility is calming or stress is repairing.
- Formula behavior cannot be economically interpreted beyond indicator difference.

### 6.3 `dpath_03_elevated_disagreement_stabilization`

Scientific lineage:

| field | specification |
| --- | --- |
| hypothesis | Securities that remain orderly while disagreement is elevated but stabilizing should benefit from orderly repricing. |
| mechanism | Elevated Disagreement Stabilization. |
| scientific question | Do securities that remain orderly while market disagreement is elevated but stabilizing carry positive forward information? |
| expected evidence | Positive h10 primary evidence, h5 support, and no h20-only rescue. |
| primary falsification criterion | Park or revise if volatility compression or stress repair explains the behavior. |
| observable implication | Disagreement must have been elevated and must now be stabilizing; current low dispersion alone is not sufficient. |
| expected orthogonality | Should differ from static dispersion level by requiring elevated prior disagreement plus current stabilization path. |
| contamination risks | Volatility compression, hostile/stress repair, VoV calming, rank coherence. |

Formula specification:

| field | value |
| --- | --- |
| candidate_id | `dpath_03_elevated_disagreement_stabilization` |
| candidate_name | Elevated Disagreement Stabilization |
| mechanism family | Elevated Disagreement Stabilization |
| primary horizon | h10 |
| secondary horizons | h5, h20 |
| expected sign | positive |
| exact OHLCV-only formula | `active_rank(low_churn_5 * low_extension_20 * (1 - rank_cs(abs(ret_10))) * liquidity_rank_20, stabilization_active)` |
| activation conditions | `stabilization_active = (lag(disp_z_20, 10) > 0.5) and (disp_z_20 > 0) and (disp_slope_10 < 0) and (abs(disp_slope_5) < abs(lag(disp_slope_5, 5)))` |
| required raw inputs | `date`, `ticker`, `open`, `high`, `low`, `close` or adjusted close, `volume`. |
| derived rolling features | `ret_1`, `ret_5`, `ret_10`, `ret_20`, `dollar_volume_20`, `rank_churn_5`, `disp_1`, `disp_5`, `disp_10`, `disp_20`, `disp_z_20`, `disp_slope_5`, `disp_slope_10`. |
| cross-sectional features | `low_churn_5`, `low_extension_20`, `rank_cs(abs(ret_10))`, `liquidity_rank_20`. |
| missing-data handling | Missing inputs or nonfinite stabilization features produce null `signal_value`; inactive states use neutral `0.5`. |
| warmup rules | Requires 252 sessions of dispersion history plus 60 security sessions for shared controls. |
| date alignment | Signal date `t` uses data through close `t`; h5/h10/h20 forward returns begin after `t`. |
| after-close timing policy | `after_close_t_forward_returns_after_t`. |
| output schema | Canonical long-form row with stabilization activation diagnostics. |
| artifact naming | Candidate rows written to future `dpath_signal_panel_long.parquet`; formula lineage in future `candidate_formula_manifest.csv`. |
| anchor/static-dispersion comparator requirement | Compare against `static_dispersion_anchor_20` and `elevated_dispersion_level_anchor`. |
| contamination checks | Volatility compression, hostile/stress repair, VoV calming, rank coherence, persistence, static dispersion. |

Candidate-specific stop conditions:

- Evidence disappears after volatility-compression controls.
- Evidence exists only in drawdown or stress-repair windows.
- Maximum absolute correlation above 0.70 to volatility compression or hostile/stress repair references.
- h5/h10 flat or unstable while h20 alone is positive.

### 6.4 `dpath_04_consensus_without_crowding`

Scientific lineage:

| field | specification |
| --- | --- |
| hypothesis | Orderly disagreement normalization may identify emerging consensus if it avoids mature leadership crowding. |
| mechanism | Consensus Formation Without Crowding. |
| scientific question | Does disagreement normalization identify securities benefiting from delayed consensus formation without rewarding crowded leadership? |
| expected evidence | Positive h10 primary evidence, h5 support, and separation from parked non-hostile transition and rank persistence. |
| primary falsification criterion | Park or revise if mature leadership, momentum, or prior winners explain the signal. |
| observable implication | Prior disagreement must normalize gradually, and the security score must favor emerging improvement without mature crowding. |
| expected orthogonality | Should differ from parked non-hostile transition by making disagreement normalization primary and leadership crowding a penalty. |
| contamination risks | Parked non-hostile transition, momentum, rank coherence, persistence, leadership crowding. |

Formula specification:

| field | value |
| --- | --- |
| candidate_id | `dpath_04_consensus_without_crowding` |
| candidate_name | Consensus Formation Without Crowding |
| mechanism family | Consensus Formation Without Crowding |
| primary horizon | h10 |
| secondary horizons | h5, h20 |
| expected sign | positive |
| exact OHLCV-only formula | `active_rank(emerging_improvement_5_20 * low_extension_20 * (1 - leadership_crowding_60) * low_churn_5 * liquidity_rank_20, consensus_active)` |
| activation conditions | `consensus_active = (lag(disp_z_20, 10) > 0) and (disp_slope_10 < 0) and (disp_z_20 < lag(disp_z_20, 10)) and (disp_z_20 > -0.5)` |
| required raw inputs | `date`, `ticker`, `open`, `high`, `low`, `close` or adjusted close, `volume`. |
| derived rolling features | `ret_1`, `ret_5`, `ret_20`, `ret_60`, `dollar_volume_20`, `rank_churn_5`, `disp_1`, `disp_10`, `disp_20`, `disp_z_20`, `disp_slope_10`. |
| cross-sectional features | `emerging_improvement_5_20`, `low_extension_20`, `leadership_crowding_60`, `low_churn_5`, `liquidity_rank_20`. |
| missing-data handling | Missing OHLCV or nonfinite crowding controls produce null `signal_value`; inactive states use neutral `0.5`. |
| warmup rules | Requires 252 sessions of dispersion history and 60 security sessions for leadership crowding. |
| date alignment | Signal date `t` uses data through close `t`; h5/h10/h20 forward returns begin after `t`. |
| after-close timing policy | `after_close_t_forward_returns_after_t`. |
| output schema | Canonical long-form row with consensus activation and crowding diagnostic fields. |
| artifact naming | Candidate rows written to future `dpath_signal_panel_long.parquet`; formula lineage in future `candidate_formula_manifest.csv`. |
| anchor/static-dispersion comparator requirement | Compare against `static_dispersion_anchor_20`, `dispersion_normalization_anchor`, and parked non-hostile transition references where available. |
| contamination checks | Parked non-hostile transition, momentum, rank coherence, persistence, volume shock reversal, volatility compression, hostile/stress repair. |

Candidate-specific stop conditions:

- Maximum absolute correlation above 0.60 to parked non-hostile transition or momentum references.
- Evidence is strongest only in mature leaders or prior winners.
- No incremental h5/h10 evidence beyond rank coherence or persistence.
- Active coverage collapses to a narrow leadership-only subset.

## SECTION 7 - Anchor and Contamination Control Specification

Required anchor and comparator signals are diagnostic controls, not research candidates. They must not be ranked as candidate winners.

Static and path anchors:

| comparator | exact OHLCV-only definition | required use |
| --- | --- | --- |
| `static_dispersion_anchor_20` | `rank_cs(low_extension_20 * low_churn_5) * rank_cs(disp_z_20)` as a date-conditioned diagnostic score. | Tests whether candidate evidence is only static dispersion level plus security stability. |
| `dispersion_slope_anchor_10` | `rank_cs(low_extension_20 * low_churn_5) * rank_cs(disp_slope_10)` as a date-conditioned diagnostic score. | Tests whether candidate evidence is only simple rising/falling dispersion. |
| `dispersion_relapse_anchor_without_security_resilience` | `active_rank(liquidity_rank_20, relapse_active)` | Tests whether relapse activation alone explains `dpath_01`. |
| `elevated_dispersion_level_anchor` | `active_rank(low_extension_20 * liquidity_rank_20, lag(disp_z_20, 10) > 0.5)` | Tests whether elevated level alone explains `dpath_03`. |
| `dispersion_normalization_anchor` | `active_rank(low_extension_20 * liquidity_rank_20, consensus_active)` | Tests whether normalization activation alone explains `dpath_04`. |

Required contamination checks:

| control family | required diagnostic |
| --- | --- |
| VoV | Pairwise signal correlation and active co-activation versus available VoV candidates and `vov_path_10`. |
| Volatility compression | Compare behavior during falling `mkt_vol_20` and against volatility-compression references. |
| Hostile/stress repair | Compare active dates and signal behavior against hostile/stress repair references and `mkt_stress_20`. |
| Volume shock reversal | Compare against volume shock reversal reference and abnormal-volume diagnostics. |
| Rank coherence / persistence | Compare against rank coherence and persistence references; track max correlation and top/bottom overlap where tooling supports it. |
| Static dispersion anchors | Require positive anchor delta for any advance/watch claim. |
| Parked non-hostile transition | Mandatory for `dpath_04`; diagnostic for all candidates using low churn or low extension. |

Stop logic:

- If a candidate has positive h10 evidence but no positive delta versus its static/path anchor, it cannot advance.
- If a candidate is mostly explained by one contamination family, it must be parked, revised, or diagnostic-only.
- If family evidence depends on h20 while h5/h10 fail, the module must not be advanced under this specification.

## SECTION 8 - Panel Specification

Canonical panel shape:

- Long form.
- One row per `date` x `ticker` x `candidate_id`.
- Exactly four candidate IDs are allowed.
- The tuple `date`, `ticker`, `candidate_id` must be unique.

Canonical panel file:

- `dpath_signal_panel_long.parquet`

Required sort order:

1. `date`
2. `candidate_id`
3. `ticker`

Allowed candidate IDs:

- `dpath_01_relapse_resilience_after_calm`
- `dpath_02_disagreement_vol_stress_divergence`
- `dpath_03_elevated_disagreement_stabilization`
- `dpath_04_consensus_without_crowding`

Blocked candidate concepts:

- Smooth Versus Burst Resolution.
- Event clustering.
- Any `dpath_05` or higher ID.

## SECTION 9 - Required Panel Columns

Canonical long-form columns:

| column | type | required | rule |
| --- | --- | --- | --- |
| `date` | date | yes | Signal date using after-close availability. |
| `ticker` | string | yes | Existing OHLCV research ticker identifier. |
| `candidate_id` | string | yes | Must be one of four allowed IDs. |
| `candidate_name` | string | yes | Human-readable name from this specification. |
| `module_id` | string | yes | `dispersion_path_dependence_research_module_v1`. |
| `spec_id` | string | yes | `dispersion_path_dependence_formula_and_panel_specification_v1`. |
| `mechanism_family` | string | yes | One of four first-batch mechanisms. |
| `research_status` | string | yes | `RESEARCH_ONLY`. |
| `primary_horizon` | string | yes | `h10`. |
| `secondary_horizons` | string | yes | `h5|h20`. |
| `expected_sign` | string | yes | `positive`. |
| `signal_value` | float | yes | Final cross-sectional signal after activation handling. |
| `raw_score` | float | yes | Raw formula score after feature construction but before final rank. |
| `pre_activation_raw_score` | float | yes | Raw formula score before inactive neutralization. |
| `is_active` | bool | yes | True when activation condition is satisfied and features are finite. |
| `feature_warmup_complete` | bool | yes | True only after required warmup windows mature. |
| `finite_cross_section_count` | integer | yes | Finite count used for same-date ranking. |
| `rank_min_count` | integer | yes | Expected 50. |
| `missing_reason` | string | yes | Null or controlled reason code. |
| `timing_policy` | string | yes | `after_close_t_forward_returns_after_t`. |
| `formula_text` | string | yes | Exact formula string from this specification. |
| `activation_text` | string | yes | Exact activation rule from this specification. |
| `anchor_comparators` | string | yes | Pipe-delimited comparator IDs. |
| `contamination_controls` | string | yes | Pipe-delimited contamination families. |
| `primary_falsification_criterion` | string | yes | Candidate-level primary falsification criterion. |
| `created_by_spec` | string | yes | `dispersion_path_dependence_formula_and_panel_specification_v1`. |

Optional diagnostic columns may be emitted in the canonical panel if scalar and documented:

- `disp_20`
- `disp_z_20`
- `disp_slope_5`
- `disp_slope_10`
- `divergence_intensity`
- `mkt_vol_20`
- `mkt_vol_slope_10`
- `mkt_stress_20`
- `mkt_stress_slope_10`
- `vov_5_20`
- `rank_churn_5`
- `low_churn_5`
- `low_extension_20`
- `leadership_crowding_60`
- `emerging_improvement_5_20`

Missing reason vocabulary:

- `raw_ohlcv_missing`
- `rolling_warmup`
- `insufficient_cross_section`
- `nonfinite_feature`
- `inactive_neutralized`
- `date_level_feature_missing`
- `invalid_candidate_id`
- `blocked_deferred_mechanism`

## SECTION 10 - Metadata JSON Schema

Future panel generation must emit `metadata.json` at the artifact root.

Required JSON fields:

```json
{
  "run_id": "string",
  "module_id": "dispersion_path_dependence_research_module_v1",
  "spec_id": "dispersion_path_dependence_formula_and_panel_specification_v1",
  "classification": "FORMULA_SPEC_READY_WITH_SCIENTIFIC_NOTES",
  "candidate_ids": [
    "dpath_01_relapse_resilience_after_calm",
    "dpath_02_disagreement_vol_stress_divergence",
    "dpath_03_elevated_disagreement_stabilization",
    "dpath_04_consensus_without_crowding"
  ],
  "blocked_mechanisms": ["smooth_versus_burst_resolution"],
  "candidate_count": 4,
  "family": "dispersion_path_dependence",
  "research_status": "RESEARCH_ONLY",
  "timing_policy": "after_close_t_forward_returns_after_t",
  "rank_min_count": 50,
  "activation_neutralization": "inactive_signal_value_0_5_with_is_active_false",
  "panel_shape": "long",
  "artifact_root": "artifacts/research/dispersion_path_dependence_research_module_v1/panel_v1/",
  "source_data_access": "existing_local_ohlcv_only",
  "external_data_accessed": false,
  "formula_implementation_executed": false,
  "panel_generation_executed": false,
  "ic_scoring_executed": false,
  "validation_executed": false,
  "governance_modified": false,
  "production_registration": false,
  "threshold_changed": false,
  "ml_integration": false,
  "created_at_utc": "ISO-8601 timestamp"
}
```

## SECTION 11 - Panel Manifest Schema

Future panel generation must emit `panel_manifest.json`.

Required fields:

| field | type | rule |
| --- | --- | --- |
| `artifact_root` | string | Must equal proposed artifact root. |
| `canonical_panel_path` | string | Path to `dpath_signal_panel_long.parquet`. |
| `metadata_path` | string | Path to `metadata.json`. |
| `candidate_registry_path` | string | Path to future `candidate_registry.csv`. |
| `candidate_formula_manifest_path` | string | Path to future `candidate_formula_manifest.csv`. |
| `derived_feature_manifest_path` | string | Path to future `derived_feature_manifest.csv`. |
| `contamination_manifest_path` | string | Path to future `contamination_control_manifest.csv`. |
| `row_count` | integer | Total canonical panel rows. |
| `date_min` | date | Earliest signal date emitted. |
| `date_max` | date | Latest signal date emitted. |
| `ticker_count` | integer | Distinct ticker count. |
| `candidate_count` | integer | Must equal 4. |
| `candidate_ids` | list[string] | Must equal four approved IDs. |
| `blocked_deferred_candidate_count` | integer | Must equal 0 emitted rows. |
| `duplicate_key_count` | integer | Must equal 0. |
| `invalid_candidate_count` | integer | Must equal 0. |
| `missing_signal_count` | integer | Count of missing `signal_value` rows. |
| `inactive_row_count` | integer | Count of rows with `is_active = false`. |
| `warmup_incomplete_count` | integer | Count of warmup-incomplete rows. |
| `rank_min_count` | integer | Expected 50. |
| `dates_below_rank_min_count` | integer | Count of candidate-dates below rank minimum. |
| `timing_policy` | string | Must match metadata JSON. |
| `checksum_policy` | string | Required if local tooling supports checksums. |
| `input_data_checksum` | string or null | Required if source-data checksum is available. |
| `formula_manifest_checksum` | string or null | Required after formula manifest creation. |
| `stop_condition_triggered` | bool | True only if writer halted before canonical panel completion. |
| `stop_condition_reason` | string or null | Required when stopped. |

## SECTION 12 - Artifact Directory Plan

Future artifact root:

`artifacts/research/dispersion_path_dependence_research_module_v1/panel_v1/`

Required future artifacts:

- `metadata.json`
- `panel_manifest.json`
- `candidate_registry.csv`
- `candidate_formula_manifest.csv`
- `input_schema.csv`
- `derived_feature_manifest.csv`
- `contamination_control_manifest.csv`
- `dpath_signal_panel_long.parquet`
- `dpath_feature_diagnostics_long.parquet`
- `panel_integrity_summary.csv`
- `missing_data_summary.csv`
- `activation_summary.csv`
- `warmup_summary.csv`
- `duplicate_key_report.csv`
- `blocked_candidate_report.csv`
- `stop_condition_precheck.csv`

Optional future diagnostics:

- `dpath_signal_panel_diagnostic_wide.parquet`
- `anchor_comparator_panel_long.parquet`
- `contamination_reference_alignment.csv`

This specification does not create the artifact root or any artifact files.

## SECTION 13 - Candidate Lineage and Scientific Lineage Fields

Every future candidate registry row must include:

| field | rule |
| --- | --- |
| `candidate_id` | One of four approved IDs. |
| `candidate_name` | Must match this specification. |
| `module_id` | `dispersion_path_dependence_research_module_v1`. |
| `spec_id` | `dispersion_path_dependence_formula_and_panel_specification_v1`. |
| `mechanism_family` | One approved mechanism per candidate. |
| `scientific_review_note` | `dispersion_path_dependence_scientific_review_v1.md`. |
| `module_design_note` | `dispersion_path_dependence_research_module_design_v1.md`. |
| `mechanism_review_note` | `dispersion_path_dependence_scientific_mechanism_review_v1.md`. |
| `allocation_note` | `dispersion_path_dependence_candidate_allocation_and_formula_planning_v1.md`. |
| `hypothesis` | Candidate-specific hypothesis from Section 6. |
| `scientific_question` | Candidate-specific question from Section 6. |
| `observable_implication` | Candidate-specific implication from Section 6. |
| `primary_falsification_criterion` | Candidate-specific falsification criterion from Section 6. |
| `expected_orthogonality` | Candidate-specific orthogonality expectation from Section 6. |
| `contamination_risks` | Pipe-delimited contamination risks. |
| `anchor_comparators` | Pipe-delimited anchor IDs. |
| `formula_text` | Exact formula string. |
| `activation_text` | Exact activation string. |
| `primary_horizon` | h10. |
| `secondary_horizons` | h5|h20. |
| `research_status` | RESEARCH_ONLY. |

## SECTION 14 - Timing, Missing Data, and Warmup Rules

Timing policy:

- Signals are computed after the close of date `t`.
- Signals may use OHLCV data through date `t`.
- Forward returns for h1, h5, h10, and h20 must begin after date `t`.
- Same-date close usage must be documented as after-close signal availability.
- No intraday assumption is authorized.

Missing data policy:

- Do not impute missing OHLCV values.
- Do not convert nonfinite formulas to zero.
- Inactive but otherwise valid candidate states use neutral `0.5` and `is_active = false`.
- Warmup-incomplete rows may be emitted only if clearly marked and excluded from IC scoring.
- Any date-candidate with fewer than 50 finite cross-sectional values must be marked invalid for ranking.

Warmup policy:

- Minimum security history: 60 sessions for all candidates.
- Minimum date-level state history: 252 sessions for dispersion z-scores and path medians.
- If any candidate-specific warmup requirement is unmet, set `feature_warmup_complete = false`.

## SECTION 15 - Success Criteria and Stop Conditions

Candidate-level success criteria:

- h10 mean IC positive in the expected direction.
- h5 supportive or at least not directionally contradictory.
- IC IR and positive IC rate support the mean IC.
- Active coverage is sufficient for interpretation.
- Anchor delta is positive against required static/path comparators.
- Contamination references do not explain the core evidence.
- No h20-only rescue if h5/h10 fail.

Family-level success criteria:

- At least two candidates show coherent h5/h10 evidence.
- Evidence includes at least one highest-priority mechanism: relapse resilience or path divergence.
- Candidate evidence is not a sibling-duplicate cluster.
- Static dispersion anchors do not explain the family.
- Contamination checks do not reduce the family to VoV, volatility compression, hostile/stress repair, volume shock reversal, rank coherence, persistence, or parked non-hostile transition.

Stop conditions:

- Formulas collapse into static dispersion level.
- Formulas duplicate VoV, volatility compression, or stress repair.
- h5/h10 evidence is unstable, flat, negative, or directionally wrong.
- Activation is too sparse for stable interpretation.
- Performance depends on one crisis or transition window.
- No incremental information appears beyond anchors.
- Smooth Versus Burst Resolution or event-clustering logic appears in implementation.
- Candidate count expands beyond four without a new approved specification.
- Panel timing, duplicate-key, checksum, or missing-data integrity fails.

## SECTION 16 - Explicit Non-Goals

This specification does not:

- implement formulas;
- generate panels;
- create artifacts;
- compute IC;
- run validation;
- execute discovery;
- modify governance decisions;
- modify the production registry;
- change thresholds;
- introduce ML;
- authorize Smooth Versus Burst Resolution;
- authorize event clustering;
- authorize broad search or parameter grids;
- promote, demote, validate, or register any candidate.

## SECTION 17 - Verification

Verification:

- Required sections exist: lifecycle placement, candidate specifications, formula notation, panel specification, metadata schema, panel manifest schema, artifact directory plan, lineage fields, timing fields, contamination controls, success criteria, stop conditions, explicit non-goals, and classification.
- Every candidate has a scientific lineage block before the formula.
- Four total candidates are specified, within the four-to-six Platform v2 budget.
- No deferred Smooth Versus Burst Resolution candidate is included.
- No formulas are implemented.
- No panels are generated.
- No IC work is performed.
- No validation is performed.
- No governance decision is modified.
- No production file is changed.
- No threshold file is changed.
- No ML file is changed.

## SECTION 18 - Final Classification

Final classification:

- `FORMULA_SPEC_READY_WITH_SCIENTIFIC_NOTES`

The specification is ready for implementation review and future implementation, subject to the scientific notes, candidate budget, anchor controls, contamination checks, timing policy, and stop conditions frozen above.
