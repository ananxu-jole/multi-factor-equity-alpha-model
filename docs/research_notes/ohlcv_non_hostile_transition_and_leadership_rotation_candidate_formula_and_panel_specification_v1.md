# Project Underdog - OHLCV Non-Hostile Transition and Leadership Rotation Candidate Formula and Panel Specification v1

## SECTION 1 - Executive Summary

This note defines the candidate formula and panel specification for the nine approved OHLCV Non-Hostile Transition and Leadership Rotation candidates.

Scope: specification/design only.

No candidate panels were generated. No discovery was executed. No IC scoring, redundancy screening, refinement, validation, governance promotion/demotion, production registration, threshold change, or ML work was performed.

Readiness classification: `FORMULA_SPEC_READY_FOR_IMPLEMENTATION`.

The specification resolves the blockers identified in `ohlcv_non_hostile_transition_and_leadership_rotation_panel_generation_readiness_review_v1.md` by defining:

- candidate formulas;
- candidate family, role, and horizon mapping;
- required input schema;
- derived feature definitions;
- final panel output schema;
- warmup, missing-data, universe, and date-alignment rules;
- formula-to-registry consistency rules.

The formulas are fixed, OHLCV-only, research-only transformations. They are not optimized, tuned, validated, or production-authorized.

## SECTION 2 - Registry Authority

The authoritative candidate registry remains:

- `artifacts/research/ohlcv_non_hostile_transition_and_leadership_rotation_discovery_v1/candidate_registry/candidate_registry.csv`

Formula implementation must consume candidate identity and metadata from the registry-derived implementation layer. It must not redefine:

- candidate identifiers;
- working names;
- family;
- concept categories;
- economic mechanisms;
- implementation priorities;
- dependency classes;
- artifact namespaces;
- diagnostic identifiers.

Approved candidates:

- `nhlr_01`
- `nhlr_02`
- `nhlr_03`
- `nhlr_04`
- `nhlr_05`
- `nhlr_07`
- `nhlr_08`
- `nhlr_09`
- `nhlr_10`

Excluded candidate:

- `nhlr_06`

## SECTION 3 - Required Input Schema

Required raw OHLCV input columns:

| column | type | rule |
| --- | --- | --- |
| `date` | date-like | Trading date. Must be normalized to date and sorted ascending. |
| `ticker` | string | Security identifier used by existing OHLCV data. No CRSP/PIT identifier reopening. |
| `open` | float | Positive where available. |
| `high` | float | Positive where available and greater than or equal to `low`. |
| `low` | float | Positive where available and less than or equal to `high`. |
| `close` | float | Positive adjusted close if available; otherwise close from existing OHLCV feed. |
| `volume` | float | Non-negative trading volume. |

Optional input columns:

| column | use |
| --- | --- |
| `adjusted_close` | May replace `close` if the existing OHLCV layer already provides it consistently. |
| `dollar_volume` | May be consumed if already present; otherwise compute as `close * volume`. |

Forbidden inputs:

- CRSP/PIT metadata;
- sector, industry, peer-group, or point-in-time classification data;
- drawdown recovery labels;
- hostile/stress-repair gates;
- validation labels;
- future returns;
- target variables;
- model predictions.

## SECTION 4 - Derived Feature Definitions

All features are computed using information available at or before `date`. Rolling windows are trailing windows by ticker unless explicitly marked cross-sectional.

Notation:

- `rank_cs(x)`: cross-sectional percentile rank by date, scaled 0 to 1, higher is better.
- `z_cs(x)`: cross-sectional z-score by date after winsorizing to the 1st/99th percentiles.
- `ts_z(x, n)`: trailing ticker-level z-score over `n` trading days.
- `clip(x, lo, hi)`: bound values between `lo` and `hi`.
- `safe_mean(...)`: average available non-null components; null if fewer than the required component count.
- `ret_n`: `close / close.shift(n) - 1`.
- `log_ret_1`: `log(close / close.shift(1))`.
- `ma_n`: trailing mean of `close` over `n` days.
- `vol_n`: trailing standard deviation of `log_ret_1` over `n` days.
- `range_pct`: `(high - low) / close`.
- `range_n`: trailing mean of `range_pct` over `n` days.
- `dollar_volume`: `close * volume`.
- `dv_z_n`: `ts_z(log1p(dollar_volume), n)`.
- `rel_strength_n`: `rank_cs(ret_n)`.
- `trend_rank_n`: `rank_cs(close / ma_n - 1)`.
- `range_control_n`: `1 - rank_cs(range_n)`.
- `vol_control_n`: `1 - rank_cs(vol_n)`.
- `participation_n`: `rank_cs(ts_z(log1p(dollar_volume), n))`.
- `leadership_score`: `safe_mean(rel_strength_20, rel_strength_60, trend_rank_50)`.
- `leadership_delta_20`: `leadership_score - leadership_score.shift(20)`.
- `leadership_delta_60`: `leadership_score - leadership_score.shift(60)`.
- `rank_velocity_20`: `rel_strength_20 - rel_strength_20.shift(20)`.
- `rank_acceleration_20`: `rank_velocity_20 - rank_velocity_20.shift(20)`.
- `above_ma_50`: `1` when `close > ma_50`, else `0`.
- `above_ma_100`: `1` when `close > ma_100`, else `0`.
- `universe_breadth_50`: date-level mean of `above_ma_50` across eligible tickers.
- `universe_breadth_delta_20`: `universe_breadth_50 - universe_breadth_50.shift(20)`.
- `breadth_contribution_20`: ticker-level `above_ma_50 * rank_cs(ret_20)`.
- `non_hostile_market_state`: `1` when `universe_breadth_50 >= 0.35` and `universe_breadth_delta_20 >= -0.10`, else `0`.

Default component normalization:

- Formula components should be converted to cross-sectional ranks where possible.
- Final `signal_value` should be a cross-sectional z-score by date, winsorized to [-5, 5].
- Higher `signal_value` must always mean more preferred candidate exposure.

## SECTION 5 - Candidate Formula Table

All formulas are fixed equal-weight or explicitly weighted combinations. No thresholds may be optimized during panel generation.

| candidate_id | formula name | formula specification | implementation notes |
| --- | --- | --- | --- |
| `nhlr_01` | `neutral_base_emergence_score` | `z_cs(0.30 * rank_cs(leadership_delta_60) + 0.25 * rank_cs(leadership_delta_20) + 0.20 * rel_strength_20 + 0.15 * trend_rank_50 + 0.10 * range_control_20 - 0.20 * rank_cs(abs(rel_strength_60.shift(60) - 0.50)))` | Captures emergence from neutral/middling leadership. Penalizes candidates that were already extreme leaders or laggards 60 days earlier. |
| `nhlr_02` | `quiet_accumulation_before_leadership_score` | `z_cs(0.30 * participation_60 + 0.25 * rank_cs(dv_z_60 - dv_z_20.abs()) + 0.20 * range_control_20 + 0.15 * vol_control_20 + 0.10 * rank_cs(ret_20) - 0.20 * rank_cs(abs(ret_20)))` | Rewards improving participation with restrained price extension and controlled range. Does not use volume shock reversal or liquidity repair framing. |
| `nhlr_03` | `post_transition_leadership_durability_score` | `z_cs(0.30 * leadership_score + 0.25 * rank_cs(-abs(leadership_delta_20)) + 0.20 * rel_strength_60 + 0.15 * participation_60 + 0.10 * range_control_20)` | Measures healthy persistence after leadership emergence without drawdown windows or post-drawdown repair gates. |
| `nhlr_04` | `smooth_trend_handoff_score` | `z_cs(0.30 * rank_cs(trend_rank_50 - trend_rank_50.shift(20)) + 0.25 * trend_rank_50 + 0.20 * range_control_20 + 0.15 * vol_control_20 + 0.10 * rel_strength_20)` | Captures controlled handoff from neutral/consolidating trend into orderly trend participation. |
| `nhlr_05` | `broadening_participation_without_stress_score` | `z_cs(non_hostile_market_state * (0.30 * participation_60 + 0.25 * rank_cs(participation_60 - participation_60.shift(20)) + 0.20 * breadth_contribution_20 + 0.15 * range_control_20 + 0.10 * rel_strength_20))` | Requires constructive or neutral breadth, not stress-repair. If `non_hostile_market_state = 0`, the score is neutralized before cross-sectional z-scoring. |
| `nhlr_07` | `rotation_acceleration_leader_score` | `z_cs(0.35 * rank_cs(rank_acceleration_20) + 0.25 * rank_cs(rank_velocity_20) + 0.20 * rel_strength_20 + 0.10 * trend_rank_50 + 0.10 * range_control_20)` | Measures early leadership during accelerating rotation. Must not be simplified to raw momentum acceleration alone. |
| `nhlr_08` | `mature_leadership_deceleration_avoidance_score` | `z_cs(0.30 * leadership_score + 0.30 * rank_cs(-rank_acceleration_20.clip(upper=0)) + 0.20 * rank_cs(-abs(rank_velocity_20)) + 0.10 * participation_60 + 0.10 * range_control_20)` | Favors leaders not showing late-stage sponsorship loss. Lower priority; should be monitored for persistence/rank-coherence overlap. |
| `nhlr_09` | `volume_confirmed_leadership_shift_score` | `z_cs(0.30 * rel_strength_20 + 0.25 * rank_cs(leadership_delta_20) + 0.25 * rank_cs(clip(dv_z_60, -1.0, 2.0)) + 0.10 * range_control_20 + 0.10 * trend_rank_50 - 0.20 * rank_cs((dv_z_20 > 3.0).astype(int)))` | Confirms leadership shift with orderly volume, while penalizing one-off volume shocks. |
| `nhlr_10` | `healthy_breadth_contributor_score` | `z_cs(non_hostile_market_state * (0.30 * breadth_contribution_20 + 0.25 * rank_cs(above_ma_50 + above_ma_100) + 0.20 * rel_strength_20 + 0.15 * participation_60 + 0.10 * range_control_20))` | Identifies names contributing to healthy breadth expansion without sector, peer, PIT, or weak-breadth repair claims. |

Formula implementation note:

- `rank_acceleration_20.clip(upper=0)` means retain only non-positive acceleration values before sign reversal in `nhlr_08`.
- Boolean expressions should be cast to 0/1 only inside formula components.
- If a formula has fewer than three available non-null components for a row, `signal_value` must be null.

## SECTION 6 - Candidate Family, Role, and Horizon Mapping

| candidate_id | family | panel role | primary horizon | secondary review horizons | rationale |
| --- | --- | --- | --- | --- | --- |
| `nhlr_01` | `ohlcv_non_hostile_transition_leadership_rotation` | core early-emergence candidate | `h20` | `h10`, `h5` | Leadership emergence is expected to develop over medium horizons. |
| `nhlr_02` | `ohlcv_non_hostile_transition_leadership_rotation` | core accumulation candidate | `h20` | `h10`, `h5` | Quiet accumulation should precede later recognition, not same-day reversal. |
| `nhlr_03` | `ohlcv_non_hostile_transition_leadership_rotation` | durability support candidate | `h20` | `h10` | Durability is a medium-horizon concept and should not be evaluated as short reversal. |
| `nhlr_04` | `ohlcv_non_hostile_transition_leadership_rotation` | core trend-handoff candidate | `h20` | `h10`, `h5` | Smooth handoff should survive beyond short-term trend noise. |
| `nhlr_05` | `ohlcv_non_hostile_transition_leadership_rotation` | breadth/participation support candidate | `h20` | `h10` | Healthy participation expansion should be tested at medium horizons. |
| `nhlr_07` | `ohlcv_non_hostile_transition_leadership_rotation` | rotation acceleration candidate | `h10` | `h20`, `h5` | Rotation acceleration may express faster than other leadership-transition concepts. |
| `nhlr_08` | `ohlcv_non_hostile_transition_leadership_rotation` | lower-priority deceleration-avoidance candidate | `h20` | `h10` | Mature leadership quality is expected to be medium horizon and overlap-prone. |
| `nhlr_09` | `ohlcv_non_hostile_transition_leadership_rotation` | core confirmation candidate | `h10` | `h20`, `h5` | Volume confirmation may act faster than quiet accumulation. |
| `nhlr_10` | `ohlcv_non_hostile_transition_leadership_rotation` | core breadth-contribution candidate | `h20` | `h10` | Breadth contribution is expected to be a medium-horizon leadership-broadening signal. |

Panel generation should write one panel per candidate using the `primary horizon` as the panel `horizon` value. Secondary review horizons are for later discovery/scoring design and must not create extra candidate IDs.

## SECTION 7 - Final Panel Output Schema

Required long-form panel columns:

| column | type | rule |
| --- | --- | --- |
| `date` | date | Signal date. |
| `ticker` | string | Security identifier. |
| `candidate_id` | string | Must match authoritative registry exactly. |
| `signal_value` | float | Final cross-sectional z-score, higher is better. |
| `family` | string | Must equal registry family. |
| `theme` | string | Use registry `concept_category`. |
| `horizon` | string | Primary horizon from Section 6. |

Required metadata columns:

| column | type | rule |
| --- | --- | --- |
| `working_name` | string | Registry-derived. |
| `economic_mechanism` | string | Registry-derived. |
| `implementation_priority` | string | Registry-derived. |
| `panel_role` | string | From Section 6. |
| `formula_name` | string | From Section 5. |
| `formula_version` | string | `v1`. |
| `dependency_class` | string | Registry-derived; must be `OHLCV_ONLY`. |
| `required_input_family` | string | Registry-derived; must be `OHLCV_DERIVED_ONLY`. |

Optional diagnostic columns:

- `component_coverage_count`
- `warmup_complete`
- `non_hostile_market_state`
- `source_close_column`
- `missing_data_reason`

Panel file convention for later implementation:

- `artifacts/research/ohlcv_non_hostile_transition_and_leadership_rotation_discovery_v1/candidate_panels/{candidate_id}.parquet`
- `artifacts/research/ohlcv_non_hostile_transition_and_leadership_rotation_discovery_v1/candidate_panels/{candidate_id}.metadata.json`

## SECTION 8 - Warmup, Missing-Data, Universe, and Date-Alignment Rules

Warmup rules:

- Minimum warmup is 120 trading days because formulas use up to 100-day moving averages plus 60-day lagged leadership deltas.
- Rows before warmup completion must have null `signal_value` or be excluded from emitted panels, but the chosen behavior must be consistent across all candidates.
- Candidate panel metadata must record `warmup_window = 120`.

Missing-data rules:

- If `close <= 0`, `high < low`, `volume < 0`, or required OHLCV values are missing for a row, all derived features for that row are null.
- If fewer than three formula components are non-null for a row, final `signal_value` is null.
- Cross-sectional ranks and z-scores require at least 30 eligible tickers on a date.
- Missing values must not be forward-filled across tickers.
- Price and volume values may not be backfilled from future dates.

Universe rules:

- Use the existing OHLCV research universe available to the project.
- Do not reopen CRSP/PIT universe construction.
- Exclude tickers with insufficient warmup history on a given date.
- Exclude tickers with non-positive close or invalid high/low data on a given date.
- Universe breadth features must be computed only from eligible same-date tickers.

Date-alignment rules:

- All rolling features must be aligned to the same signal date.
- No formula may use forward returns or future OHLCV values.
- If optional `adjusted_close` is used, it must be used consistently for all price-derived features in a run.
- Panel dates should be the intersection of dates with sufficient raw OHLCV coverage and sufficient cross-sectional count.

## SECTION 9 - Formula-to-Registry Consistency Rules

Future formula implementation must enforce:

- every formula candidate ID exists in the authoritative registry;
- every registry candidate has exactly one formula row;
- `nhlr_06` has no formula row;
- formula metadata must be joined from the registry or registry-derived implementation layer;
- formula implementation must fail if registry metadata and formula manifest metadata disagree;
- candidate IDs must not be renamed by formula code;
- formula output files must use registry candidate IDs, not working names;
- panel `family`, `theme`, and metadata columns must be registry-derived;
- formula code must preserve prohibited dependency constraints for each candidate.

Formula manifest required fields for later implementation:

- `candidate_id`
- `formula_name`
- `formula_version`
- `primary_horizon`
- `secondary_review_horizons`
- `panel_role`
- `required_raw_inputs`
- `required_derived_features`
- `registry_source_path`
- `registry_alignment_status`
- `formula_status`
- `panel_generation_status`

## SECTION 10 - Non-Goals

This specification does not:

- generate candidate panels;
- implement executable formulas;
- run discovery;
- calculate IC;
- run redundancy screening;
- run refinement;
- run validation;
- modify governance;
- change thresholds;
- register production candidates;
- implement ML;
- promote or demote candidates;
- reopen CRSP/PIT work;
- introduce new candidate concepts;
- merge or remove registry candidates.

## SECTION 11 - Readiness Assessment

The formula specification is ready for implementation because:

- all nine registry candidates have fixed formula definitions;
- `nhlr_06` remains excluded;
- panel output schema is defined;
- horizon and role mapping is defined;
- required raw and derived inputs are defined;
- warmup, missing-data, universe, and date-alignment rules are defined;
- formula-to-registry consistency rules are defined;
- non-goals and guardrails are explicit.

Remaining work is implementation-only:

- add formula manifest helpers;
- add formula validation tests;
- add panel-generation runner mode only after formula implementation review;
- keep discovery, IC, redundancy, refinement, validation, governance, production, thresholds, and ML blocked.

Final classification: `FORMULA_SPEC_READY_FOR_IMPLEMENTATION`.
