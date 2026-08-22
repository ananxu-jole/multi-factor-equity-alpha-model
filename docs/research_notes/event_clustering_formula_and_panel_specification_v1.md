# Project Underdog - Event Clustering Formula and Panel Specification v1

Platform reference: `v2.0.0-platform-scientific-methodology`

Lifecycle phase: Platform v2 Phase 2 - Formula and Panel Specification

Classification: `FORMULA_SPEC_READY_WITH_NOTES`

Recommendation: `ADVANCE_TO_IMPLEMENTATION_SPECIFICATION_REVIEW`

Scope: specification-only translation of the approved Event Clustering scientific review and research module design into exact OHLCV-only candidate formulas and panel contracts.

This note does not implement code, generate panels, compute IC, run validation, modify governance, change production files, change thresholds, introduce ML, or create artifacts.

## SECTION 1 - Inputs And Lifecycle Boundary

Inputs reviewed:

- `docs/research_notes/event_clustering_scientific_review_v1.md`
- `docs/research_notes/event_clustering_research_module_design_v1.md`
- `docs/research_notes/project_underdog_platform_v2_scientific_research_standard_v1.md`

Prior completed phases:

1. Platform v2 Phase 1A - Scientific Hypothesis And Orthogonality Review.
2. Platform v2 Phase 1B - Research Module Design.

Current phase:

- Platform v2 Phase 2 - Formula and Panel Specification.

This specification advances exactly one lifecycle phase. It does not advance to implementation, panel generation, IC discovery, validation, governance, production, threshold changes, or ML.

## SECTION 2 - Approved Mechanism Boundary

Only the approved mechanisms are authorized:

1. Event Concentration.
2. Event Alignment And Fragmentation.
3. Cluster Absorption Versus Deterioration.
4. Cluster Aging And Market Memory.

No extra mechanisms are introduced. Every candidate below maps to one of these four mechanisms.

## SECTION 3 - Candidate Registry

Candidate budget:

- Total candidates specified: 5.
- Platform v2 allowed range: 4 to 6.
- No broad search, horizon shopping, target hacking, candidate generation from results, or additional mechanism group is authorized.

| candidate_id | candidate_name | mechanism | primary horizon | secondary horizons | expected sign |
| --- | --- | --- | --- | --- | --- |
| `ecluster_01_concentrated_absorption` | Concentrated Event Absorption | Event Concentration | h10 | h5, h20 durability only | positive |
| `ecluster_02_aligned_pressure_resolution` | Aligned Event Pressure Resolution | Event Alignment And Fragmentation | h10 | h5, h20 durability only | positive |
| `ecluster_03_fragmented_event_absorption` | Fragmented Event Absorption | Event Alignment And Fragmentation | h5 | h10, h20 durability only | positive |
| `ecluster_04_deteriorating_cluster_avoidance` | Deteriorating Cluster Avoidance | Cluster Absorption Versus Deterioration | h5 | h10, h20 durability only | positive |
| `ecluster_05_aging_cluster_memory` | Aging Cluster Memory | Cluster Aging And Market Memory | h10 | h5, h20 durability only | positive |

## SECTION 4 - Formula Notation And Shared Features

All formulas are OHLCV-only and after-close. Signal date `t` may use only `open`, `high`, `low`, `close`, adjusted close if available, and `volume` through the close of `t`.

Shared notation:

| symbol | exact definition |
| --- | --- |
| `px_t` | adjusted close on `t` if available in the existing research dataset, otherwise close. |
| `ret_1` | `px_t / px_{t-1} - 1`. |
| `ret_k` | `px_t / px_{t-k} - 1`. |
| `gap_1` | `open_t / px_{t-1} - 1`. |
| `intraday_ret_1` | `close_t / open_t - 1`. |
| `range_1` | `(high_t - low_t) / px_{t-1}`. |
| `close_loc_1` | `(close_t - low_t) / max(high_t - low_t, epsilon)`, clipped to `[0, 1]`. |
| `vol_5` | `std_ts(ret_1, 5)`. |
| `dollar_volume_20` | `mean_ts(px_t * volume_t, 20)`. |
| `mean_ts(x, k)` | trailing time-series mean using values through `t`. |
| `sum_ts(x, k)` | trailing time-series sum using values through `t`. |
| `std_ts(x, k)` | trailing time-series standard deviation using values through `t`. |
| `z_ts(x, k)` | trailing time-series z-score using values through `t`. |
| `rank_cs(x)` | same-date cross-sectional percentile rank over finite active-universe values, scaled 0 to 1. |
| `mad_cs(x)` | same-date median absolute deviation over finite active-universe values. |
| `lag(x, k)` | value of `x` at `t-k`. |
| `clip(x, lo, hi)` | bound `x` to `[lo, hi]`. |
| `active_rank(raw, active)` | if `active` and `raw` are finite, output `rank_cs(raw)`; if inactive, output neutral `0.5` with `is_active = false`; if required data are missing, output null with `missing_reason`. |
| `epsilon` | smallest positive denominator guard already used by the research implementation standard; not a tunable research parameter. |

Shared event definitions:

| feature | exact definition |
| --- | --- |
| `price_event` | `1` if `abs(z_ts(ret_1, 60)) >= 1.5`, else `0`. |
| `gap_event` | `1` if `abs(z_ts(gap_1, 60)) >= 1.5`, else `0`. |
| `range_event` | `1` if `z_ts(range_1, 60) >= 1.5`, else `0`. |
| `volume_event` | `1` if `z_ts(log(1 + volume_t), 60) >= 1.5`, else `0`. |
| `vol_event` | `1` if `z_ts(vol_5, 60) >= 1.5`, else `0`. |
| `event_any` | `max(price_event, gap_event, range_event, volume_event, vol_event)`. |
| `event_type_count_1` | `price_event + gap_event + range_event + volume_event + vol_event`. |
| `cluster_count_5` | `sum_ts(event_any, 5)`. |
| `cluster_count_10` | `sum_ts(event_any, 10)`. |
| `event_type_count_5` | `sum_ts(event_type_count_1, 5)`. |
| `isolated_event_anchor_20` | `1` if `event_any = 1` and `sum_ts(event_any, 5) = 1` and `sum_ts(event_any, 20) <= 2`, else `0`. |
| `static_event_anchor_20` | `rank_cs(sum_ts(event_any, 20))`. |

Shared response and contamination features:

| feature | exact definition |
| --- | --- |
| `absorption_5` | `clip(1 - rank_cs(abs(ret_5)), 0, 1) * rank_cs(mean_ts(close_loc_1, 5))`. |
| `deterioration_5` | `rank_cs(-ret_5) * rank_cs(mean_ts(range_1, 5)) * (1 - rank_cs(mean_ts(close_loc_1, 5)))`. |
| `volume_intensity_5` | `rank_cs(sum_ts(volume_event, 5))`. |
| `range_intensity_5` | `rank_cs(sum_ts(range_event, 5))`. |
| `price_intensity_5` | `rank_cs(sum_ts(price_event, 5))`. |
| `gap_intensity_5` | `rank_cs(sum_ts(gap_event, 5))`. |
| `vol_intensity_5` | `rank_cs(sum_ts(vol_event, 5))`. |
| `alignment_score_5` | `rank_cs(event_type_count_5) * rank_cs(cluster_count_5)`. |
| `fragmentation_score_5` | `rank_cs(cluster_count_5) * rank_cs(abs(volume_intensity_5 - price_intensity_5) + abs(range_intensity_5 - gap_intensity_5) + abs(vol_intensity_5 - price_intensity_5))`. |
| `fresh_cluster_5` | `1` if `cluster_count_5 >= 2` and `lag(cluster_count_5, 5) <= 1`, else `0`. |
| `persistent_cluster_10` | `1` if `cluster_count_10 >= 4` and `cluster_count_5 >= 2`, else `0`. |
| `decaying_cluster_10` | `1` if `lag(cluster_count_5, 5) >= 2` and `cluster_count_5 <= 1`, else `0`. |
| `rank_ret_5` | `rank_cs(ret_5)`. |
| `low_extension_20` | `1 - rank_cs(abs(ret_20))`. |
| `low_churn_5` | `1 - rank_cs(abs(rank_cs(ret_5) - lag(rank_cs(ret_5), 5)))`. |
| `liquidity_rank_20` | `rank_cs(dollar_volume_20)`. |

Shared market-state controls:

| control | exact definition |
| --- | --- |
| `security_vov_20` | `std_ts(vol_5, 20)`. |
| `vol_compression_20` | `rank_cs(-vol_5) * rank_cs(lag(vol_5, 10) - vol_5)`. |
| `stress_proxy_20` | `(rank_cs(-ret_20) + rank_cs(mean_ts(range_1, 20)) + rank_cs(-mean_ts(close_loc_1, 20))) / 3`. |
| `rank_coherence_proxy_20` | `low_churn_5 * rank_cs(abs(ret_20))`. |
| `persistence_proxy_20` | `rank_cs(ret_20)`. |
| `static_dispersion_20` | `mad_cs(ret_1)` smoothed by `mean_ts` over 20 dates at the market-date level. |
| `dispersion_path_proxy_10` | `static_dispersion_20 - lag(static_dispersion_20, 10)`. |
| `non_hostile_transition_proxy_20` | `rank_cs(ret_20) * low_churn_5 * (1 - stress_proxy_20)`. |

## SECTION 5 - Candidate Specifications

### 5.1 `ecluster_01_concentrated_absorption`

Scientific lineage block:

| field | specification |
| --- | --- |
| candidate_id | `ecluster_01_concentrated_absorption` |
| candidate_name | Concentrated Event Absorption |
| mechanism | Event Concentration |
| scientific question | Do securities with concentrated nearby events and controlled response behave differently from isolated-event names? |
| expected evidence | Positive h10 primary evidence, h5 support, h20 durability only; clustered-event behavior should improve over isolated-event anchors. |
| expected primary horizon | h10 |
| secondary horizons | h5, h20 durability only |
| expected sign | positive |

Formula specification:

| field | specification |
| --- | --- |
| exact OHLCV-only formula | `active_rank((rank_cs(cluster_count_5) * absorption_5 * low_extension_20 * liquidity_rank_20) - (0.5 * deterioration_5), concentration_active)` |
| required raw inputs | `date`, `ticker`, `open`, `high`, `low`, `close` or adjusted close, `volume`. |
| derived rolling features | `ret_1`, `ret_5`, `ret_20`, `gap_1`, `range_1`, `close_loc_1`, `vol_5`, `dollar_volume_20`, event flags, `cluster_count_5`, `absorption_5`, `deterioration_5`, `low_extension_20`, `liquidity_rank_20`. |
| activation conditions | `concentration_active = cluster_count_5 >= 2`. |
| missing-data rules | Missing raw OHLCV, nonpositive prices, negative volume, nonfinite required rolling features, or nonfinite raw score produce null `signal_value` and a populated `missing_reason`; inactive rows output neutral `0.5`. |
| warmup rules | Requires 60 observations for event z-scores, 20 observations for extension/liquidity, and 5 observations for cluster/absorption fields. |
| after-close timing policy | Signal for date `t` uses only data through close `t`; forward returns begin after `t`. |
| panel output schema fields | Must populate the canonical long-form schema in Section 6, including `cluster_count_5`, `event_type_count_5`, `is_active`, `raw_score`, `signal_value`, `primary_horizon`, `secondary_horizons`, and lineage fields. |
| contamination controls | Compare later against VoV, volatility compression, hostile/stress repair, volume shock reversal, rank coherence, persistence, dispersion path-dependence, non-hostile transition, static dispersion, and isolated-event anchors. |
| static / isolated-event anchor requirement | Required anchors: `static_event_anchor_20`, `isolated_event_anchor_20`, and an isolated absorption anchor using `absorption_5` only when `isolated_event_anchor_20 = 1`. |
| stop conditions | Stop if clustered activation is indistinguishable from isolated-event anchors, if volume shock reversal explains the effect, if activation is crisis-only, or if h10 fails while h20 is the only supportive horizon. |

### 5.2 `ecluster_02_aligned_pressure_resolution`

Scientific lineage block:

| field | specification |
| --- | --- |
| candidate_id | `ecluster_02_aligned_pressure_resolution` |
| candidate_name | Aligned Event Pressure Resolution |
| mechanism | Event Alignment And Fragmentation |
| scientific question | Does coherent multi-event alignment followed by controlled response identify resolved event pressure? |
| expected evidence | Positive h10 primary evidence when multiple event types align but deterioration remains contained. |
| expected primary horizon | h10 |
| secondary horizons | h5, h20 durability only |
| expected sign | positive |

Formula specification:

| field | specification |
| --- | --- |
| exact OHLCV-only formula | `active_rank(alignment_score_5 * absorption_5 * low_churn_5 * liquidity_rank_20 * (1 - deterioration_5), alignment_active)` |
| required raw inputs | `date`, `ticker`, `open`, `high`, `low`, `close` or adjusted close, `volume`. |
| derived rolling features | event flags, `event_type_count_1`, `event_type_count_5`, `cluster_count_5`, `alignment_score_5`, `absorption_5`, `deterioration_5`, `low_churn_5`, `liquidity_rank_20`. |
| activation conditions | `alignment_active = cluster_count_5 >= 2 and event_type_count_5 >= 4 and alignment_score_5 >= 0.60`. |
| missing-data rules | Null output when any required OHLCV input, event flag, alignment score, or response feature is missing; inactive rows output neutral `0.5`. |
| warmup rules | Requires 60 observations for event z-scores and at least 20 observations for liquidity and churn support. |
| after-close timing policy | Signal for date `t` uses only data through close `t`; forward returns begin after `t`. |
| panel output schema fields | Must populate canonical fields plus `alignment_score_5`, `volume_intensity_5`, `range_intensity_5`, `price_intensity_5`, `gap_intensity_5`, and `vol_intensity_5`. |
| contamination controls | Later comparison required against VoV, volatility compression, hostile/stress repair, volume shock reversal, rank coherence, persistence, dispersion path-dependence, non-hostile transition, static dispersion, and isolated-event anchors. |
| static / isolated-event anchor requirement | Required anchors: same event-type mix without clustering, `static_event_anchor_20`, and isolated aligned one-day event anchor. |
| stop conditions | Stop if alignment is only volatility instability, if volume dominates all aligned states, if low churn explains the signal, or if aligned clusters do not differ from isolated aligned events. |

### 5.3 `ecluster_03_fragmented_event_absorption`

Scientific lineage block:

| field | specification |
| --- | --- |
| candidate_id | `ecluster_03_fragmented_event_absorption` |
| candidate_name | Fragmented Event Absorption |
| mechanism | Event Alignment And Fragmentation |
| scientific question | Do fragmented event clusters that are absorbed carry short-to-medium horizon information distinct from noisy disagreement? |
| expected evidence | Positive h5 primary evidence with h10 support if event-type disagreement reflects absorption rather than unresolved deterioration. |
| expected primary horizon | h5 |
| secondary horizons | h10, h20 durability only |
| expected sign | positive |

Formula specification:

| field | specification |
| --- | --- |
| exact OHLCV-only formula | `active_rank(fragmentation_score_5 * absorption_5 * low_extension_20 * liquidity_rank_20 * (1 - rank_cs(abs(ret_5))), fragmentation_active)` |
| required raw inputs | `date`, `ticker`, `open`, `high`, `low`, `close` or adjusted close, `volume`. |
| derived rolling features | event flags, `cluster_count_5`, intensity features, `fragmentation_score_5`, `absorption_5`, `ret_5`, `ret_20`, `low_extension_20`, `liquidity_rank_20`. |
| activation conditions | `fragmentation_active = cluster_count_5 >= 2 and fragmentation_score_5 >= 0.60 and alignment_score_5 < 0.80`. |
| missing-data rules | Null output for missing required features; inactive rows output neutral `0.5`; same-date fragmented events with missing volume are null, not imputed. |
| warmup rules | Requires 60 observations for event z-scores and 20 observations for extension/liquidity. |
| after-close timing policy | Signal for date `t` uses only data through close `t`; forward returns begin after `t`. |
| panel output schema fields | Must populate canonical fields plus `fragmentation_score_5`, `alignment_score_5`, and component intensity fields. |
| contamination controls | Later comparison required against VoV, volatility compression, hostile/stress repair, volume shock reversal, rank coherence, persistence, dispersion path-dependence, non-hostile transition, static dispersion, and isolated-event anchors. |
| static / isolated-event anchor requirement | Required anchors: isolated fragmented one-day event anchor and static high event-count anchor without fragmentation. |
| stop conditions | Stop if fragmentation is pure noise, if evidence is h1-only, if hostile/stress state explains the signal, or if no h5/h10 distinction from isolated fragmented events exists. |

### 5.4 `ecluster_04_deteriorating_cluster_avoidance`

Scientific lineage block:

| field | specification |
| --- | --- |
| candidate_id | `ecluster_04_deteriorating_cluster_avoidance` |
| candidate_name | Deteriorating Cluster Avoidance |
| mechanism | Cluster Absorption Versus Deterioration |
| scientific question | Does avoiding securities with deteriorating repeated-event pressure add information beyond stress repair and reversal? |
| expected evidence | Positive h5 primary evidence because higher scores represent lower deterioration inside active cluster states. |
| expected primary horizon | h5 |
| secondary horizons | h10, h20 durability only |
| expected sign | positive |

Formula specification:

| field | specification |
| --- | --- |
| exact OHLCV-only formula | `active_rank((1 - deterioration_5) * rank_cs(cluster_count_5) * low_extension_20 * liquidity_rank_20 * (1 - stress_proxy_20), deterioration_active)` |
| required raw inputs | `date`, `ticker`, `open`, `high`, `low`, `close` or adjusted close, `volume`. |
| derived rolling features | event flags, `cluster_count_5`, `deterioration_5`, `range_1`, `close_loc_1`, `ret_5`, `ret_20`, `stress_proxy_20`, `low_extension_20`, `liquidity_rank_20`. |
| activation conditions | `deterioration_active = cluster_count_5 >= 2 and rank_cs(cluster_count_5) >= 0.60`. |
| missing-data rules | Missing OHLCV, missing range/close-location, or nonfinite stress proxy produces null output; inactive cluster states output neutral `0.5`. |
| warmup rules | Requires 60 observations for event z-scores and 20 observations for stress, extension, and liquidity features. |
| after-close timing policy | Signal for date `t` uses only data through close `t`; forward returns begin after `t`. |
| panel output schema fields | Must populate canonical fields plus `deterioration_5`, `stress_proxy_20`, `cluster_count_5`, and `event_type_count_5`. |
| contamination controls | Later comparison required against hostile/stress repair, volume shock reversal, rank coherence, persistence, VoV, volatility compression, dispersion path-dependence, non-hostile transition, static dispersion, and isolated-event anchors. |
| static / isolated-event anchor requirement | Required anchors: isolated deterioration anchor, static stress anchor, and static event-count anchor. |
| stop conditions | Stop if the candidate is just hostile/stress repair, if reversal explains the signal, if low stress alone explains the signal, or if h5/h10 evidence does not differ from static deterioration anchors. |

### 5.5 `ecluster_05_aging_cluster_memory`

Scientific lineage block:

| field | specification |
| --- | --- |
| candidate_id | `ecluster_05_aging_cluster_memory` |
| candidate_name | Aging Cluster Memory |
| mechanism | Cluster Aging And Market Memory |
| scientific question | Does cluster age change the interpretation of repeated events beyond volatility compression or stress repair? |
| expected evidence | Positive h10 primary evidence when aging or decaying clusters retain absorption quality without fresh deterioration. |
| expected primary horizon | h10 |
| secondary horizons | h5, h20 durability only |
| expected sign | positive |

Formula specification:

| field | specification |
| --- | --- |
| exact OHLCV-only formula | `active_rank(((0.6 * decaying_cluster_10) + (0.4 * persistent_cluster_10)) * absorption_5 * low_churn_5 * liquidity_rank_20 * (1 - deterioration_5), aging_active)` |
| required raw inputs | `date`, `ticker`, `open`, `high`, `low`, `close` or adjusted close, `volume`. |
| derived rolling features | event flags, `cluster_count_5`, `cluster_count_10`, `fresh_cluster_5`, `persistent_cluster_10`, `decaying_cluster_10`, `absorption_5`, `deterioration_5`, `low_churn_5`, `liquidity_rank_20`. |
| activation conditions | `aging_active = persistent_cluster_10 = 1 or decaying_cluster_10 = 1`. |
| missing-data rules | Missing cluster age state or required response features produces null output; inactive rows output neutral `0.5`. |
| warmup rules | Requires 60 observations for event z-scores, 20 observations for liquidity/churn support, and 10 observations for cluster age states. |
| after-close timing policy | Signal for date `t` uses only data through close `t`; forward returns begin after `t`. |
| panel output schema fields | Must populate canonical fields plus `fresh_cluster_5`, `persistent_cluster_10`, `decaying_cluster_10`, `cluster_age_state`, and response fields. |
| contamination controls | Later comparison required against volatility compression, VoV, hostile/stress repair, rank coherence, persistence, dispersion path-dependence, non-hostile transition, static dispersion, volume shock reversal, and isolated-event anchors. |
| static / isolated-event anchor requirement | Required anchors: fresh-only cluster anchor, static event-count anchor, isolated-event anchor, and volatility-compression anchor. |
| stop conditions | Stop if aging is plain volatility compression, if persistence or rank coherence explains the signal, if h20-only evidence is required, or if fresh/persistent/decaying states are not distinguishable. |

## SECTION 6 - Canonical Long-Form Panel Schema

Future panel output must be long-form with one row per `date`, `ticker`, and `candidate_id`.

Required columns:

| column | type | requirement |
| --- | --- | --- |
| `date` | date | Signal date after close. |
| `ticker` | string | Security identifier used by current research data. |
| `candidate_id` | string | One of the five specified candidate IDs. |
| `candidate_name` | string | Human-readable candidate name. |
| `module_name` | string | `event_clustering_research_module_v1`. |
| `platform_version` | string | `v2.0.0-platform-scientific-methodology`. |
| `mechanism` | string | Approved mechanism label. |
| `primary_horizon` | string | `h5` or `h10` as specified. |
| `secondary_horizons` | string | Comma-separated secondary horizons. |
| `expected_sign` | string | `positive`. |
| `raw_score` | float | Pre-rank formula value when active and finite. |
| `signal_value` | float | Ranked signal value, neutral inactive value, or null if missing. |
| `is_active` | boolean | Candidate activation state. |
| `activation_reason` | string | Candidate-specific active/inactive label. |
| `missing_reason` | string nullable | Null if valid; controlled reason when null output is required. |
| `feature_warmup_complete` | boolean | Whether all required rolling features are mature. |
| `after_close_timing_policy` | string | `after_close_t_forward_returns_after_t`. |
| `formula_version` | string | `v1`. |
| `source_specification` | string | Path to this document. |
| `source_review` | string | Path to scientific review. |
| `source_design` | string | Path to research module design. |
| `cluster_count_5` | float | Shared cluster feature. |
| `cluster_count_10` | float nullable | Required where used, nullable otherwise. |
| `event_type_count_5` | float | Shared event-type feature. |
| `alignment_score_5` | float nullable | Required for alignment/fragmentation candidates. |
| `fragmentation_score_5` | float nullable | Required for fragmentation candidate. |
| `absorption_5` | float nullable | Required for response candidates. |
| `deterioration_5` | float nullable | Required for response candidates. |
| `cluster_age_state` | string nullable | Required for aging candidate. |
| `static_event_anchor_20` | float | Static event-count anchor value. |
| `isolated_event_anchor_20` | integer | Isolated-event anchor flag. |
| `contamination_reference_set` | string | Pipe-delimited list of required later contamination controls. |

## SECTION 7 - Metadata JSON Schema

A future metadata JSON file must contain one object per candidate with the following required keys:

| key | type | requirement |
| --- | --- | --- |
| `candidate_id` | string | Must match Section 3. |
| `candidate_name` | string | Must match Section 3. |
| `module_name` | string | `event_clustering_research_module_v1`. |
| `mechanism` | string | One of the four approved mechanisms. |
| `scientific_question` | string | Candidate-specific question from Section 5. |
| `expected_evidence` | string | Candidate-specific expected evidence. |
| `primary_horizon` | string | Candidate-specific primary horizon. |
| `secondary_horizons` | array[string] | Candidate-specific secondary horizons. |
| `expected_sign` | string | `positive`. |
| `formula_version` | string | `v1`. |
| `formula_text` | string | Exact formula from Section 5. |
| `activation_text` | string | Exact activation condition from Section 5. |
| `raw_inputs` | array[string] | OHLCV-only raw inputs. |
| `derived_features` | array[string] | Candidate-required rolling features. |
| `warmup_rules` | string | Candidate-specific warmup rule. |
| `missing_data_rules` | string | Candidate-specific missing-data rule. |
| `after_close_timing_policy` | string | `after_close_t_forward_returns_after_t`. |
| `contamination_controls` | array[string] | Required reference controls. |
| `anchor_requirements` | array[string] | Static and isolated-event anchors. |
| `stop_conditions` | array[string] | Candidate stop conditions. |
| `source_documents` | array[string] | Review, design, Platform v2 standard, and this specification. |

## SECTION 8 - Manifest Schemas

Artifact root for future panel generation:

`artifacts/research/event_clustering_research_module_v1/panel_v1/`

This note does not create the artifact root or any manifest files.

### 8.1 Panel Manifest Schema

Required fields:

- `module_name`
- `panel_version`
- `artifact_root`
- `panel_file`
- `row_count`
- `date_min`
- `date_max`
- `ticker_count`
- `candidate_count`
- `candidate_ids`
- `schema_version`
- `created_at_utc`
- `created_by_phase`
- `source_specification`
- `input_schema_manifest`
- `formula_manifest`
- `feature_manifest`
- `checksum_sha256`

### 8.2 Formula Manifest Schema

Required fields:

- `candidate_id`
- `candidate_name`
- `formula_version`
- `mechanism`
- `formula_text`
- `activation_text`
- `expected_sign`
- `primary_horizon`
- `secondary_horizons`
- `after_close_timing_policy`
- `source_specification`
- `source_review`
- `source_design`

### 8.3 Feature Manifest Schema

Required fields:

- `feature_name`
- `feature_type`
- `definition_text`
- `raw_input_dependencies`
- `rolling_window`
- `cross_sectional_dependency`
- `warmup_requirement`
- `missing_data_policy`
- `used_by_candidate_ids`
- `timing_policy`

### 8.4 Input Schema Manifest

Required fields:

- `date`
- `ticker`
- `open`
- `high`
- `low`
- `close`
- `adjusted_close_available`
- `volume`
- `universe_membership_flag`
- `data_vendor_or_source`
- `input_date_min`
- `input_date_max`
- `input_row_count`
- `input_checksum_sha256`
- `point_in_time_policy`

## SECTION 9 - Required Contamination Controls

Later phases must compare every candidate against:

- VoV.
- Volatility compression.
- Hostile/stress repair.
- Volume shock reversal.
- Rank coherence.
- Persistence.
- Dispersion path-dependence.
- Non-hostile transition.
- Static dispersion.
- Isolated-event anchors.

Required interpretation:

- If VoV or volatility compression explains the evidence, Event Clustering should not receive family credit.
- If hostile/stress repair explains the evidence, the candidate should be parked or reclassified.
- If volume shock reversal explains the evidence, the result should be treated as event/reversal contamination.
- If rank coherence or persistence explains the evidence, absorption claims should be downgraded.
- If dispersion path-dependence or static dispersion explains the evidence, sequence-level event topology is not established.
- If non-hostile transition explains the evidence, the candidate should not revive parked leadership-transition logic.
- If isolated-event anchors match or exceed clustered-event behavior, the clustering mechanism fails.

## SECTION 10 - Missing Data And Warmup Policy

Global missing-data policy:

- Required OHLCV fields must be finite.
- Prices must be positive.
- Volume must be nonnegative and finite.
- Rolling features must not use future data.
- Cross-sectional ranks are computed only over finite active-universe values on the same date.
- A row with inactive activation but complete features receives neutral `signal_value = 0.5`.
- A row with missing required features receives null `signal_value`, `is_active = false`, and a controlled `missing_reason`.

Global warmup policy:

- Event z-scores require 60 observations.
- Candidate response features require the maximum rolling lookback listed for the candidate.
- Rows before warmup completion must set `feature_warmup_complete = false`.
- No backfilling from future data is permitted.

## SECTION 11 - Timing Policy

All candidate formulas are after-close research signals:

- Signal date `t` uses only OHLCV data available through the close of `t`.
- Forward return horizons begin after `t`.
- Same-date forward return leakage is prohibited.
- Later implementation must preserve this timing policy in panel metadata and manifests.

## SECTION 12 - Success And Stop Criteria

Module-level success criteria:

- At least two distinct candidates should show coherent h5/h10 evidence before family-level Event Clustering claims are considered.
- Positive evidence must remain interpretable after isolated-event anchor comparison.
- Evidence must not be dominated by the required contamination references.
- h20 may support durability only and may not rescue failed h5/h10 evidence.
- Activation must be episodic, interpretable, and not one-window dominated.

Module-level stop criteria:

- Clustered-event behavior does not differ from isolated-event behavior.
- Results require post-hoc horizon switching.
- Evidence is h1-only or h20-only.
- Activation is too sparse, too continuous, or crisis-window dominated.
- The formulas become proxies for volatility, volume, stress, rank, persistence, dispersion, reversal, or leadership transition.
- Timing integrity cannot be preserved.
- The module requires additional unapproved mechanisms or broad search to become plausible.

## SECTION 13 - Guardrails

This specification authorizes only future implementation review preparation.

It does not authorize:

- implementation;
- executable candidate code;
- panel generation;
- IC discovery;
- validation;
- governance mutation;
- production changes;
- threshold changes;
- ML;
- additional candidates;
- additional mechanisms;
- artifact creation.

## SECTION 14 - Classification

Classification: `FORMULA_SPEC_READY_WITH_NOTES`

Rationale:

- Required sections exist.
- Five candidates are specified, within the Platform v2 4 to 6 candidate budget.
- All candidates map to approved mechanisms.
- Exact OHLCV-only formulas, inputs, features, activation conditions, missing-data rules, warmup rules, timing policy, panel schema, manifests, contamination controls, anchors, and stop conditions are specified.
- Notes remain because Event Clustering has high contamination risk from volume shock reversal, hostile/stress repair, VoV, volatility compression, rank coherence, persistence, dispersion behavior, and isolated-event effects.

## SECTION 15 - Verification

Confirmed:

- Required sections exist.
- 5 candidates specified.
- Candidate count is within the required 4 to 6 range.
- All candidates map to approved mechanisms.
- No implementation files changed.
- No executable candidate code created.
- No panel files created.
- No IC files created.
- No validation files created.
- No governance files changed.
- No production files changed.
- No threshold files changed.
- No ML files changed.

## SECTION 16 - Final Recommendation

Recommended next lifecycle phase:

- Event Clustering Implementation Specification Review v1.

Event Clustering may advance exactly one lifecycle phase to implementation specification review. It may not advance directly to panel generation, IC discovery, validation, governance mutation, production registration, threshold changes, or ML.
