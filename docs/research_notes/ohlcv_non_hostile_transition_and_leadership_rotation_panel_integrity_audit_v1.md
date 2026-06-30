# Project Underdog - OHLCV Non-Hostile Transition and Leadership Rotation Panel Integrity Audit v1

## SECTION 1 - Executive Summary

This audit reviewed the generated OHLCV Non-Hostile Transition and Leadership Rotation research panels before any IC discovery.

Final classification: `PANELS_APPROVED_FOR_IC_DISCOVERY`.

The generated panels are internally consistent, registry-consistent, artifact-consistent, and safe for downstream IC discovery review. The audit found no blocking issues. No panel files were regenerated or rewritten during this audit.

Guardrails preserved:

- no IC calculation;
- no IR calculation;
- no discovery execution;
- no redundancy screening;
- no refinement;
- no validation execution;
- no formula modification;
- no governance change;
- no production registration;
- no threshold change;
- no ML.

## SECTION 2 - Files Reviewed

Reviewed panel artifacts:

- `artifacts/research/ohlcv_non_hostile_transition_and_leadership_rotation_discovery_v1/candidate_panels/nhlr_01.parquet`
- `artifacts/research/ohlcv_non_hostile_transition_and_leadership_rotation_discovery_v1/candidate_panels/nhlr_02.parquet`
- `artifacts/research/ohlcv_non_hostile_transition_and_leadership_rotation_discovery_v1/candidate_panels/nhlr_03.parquet`
- `artifacts/research/ohlcv_non_hostile_transition_and_leadership_rotation_discovery_v1/candidate_panels/nhlr_04.parquet`
- `artifacts/research/ohlcv_non_hostile_transition_and_leadership_rotation_discovery_v1/candidate_panels/nhlr_05.parquet`
- `artifacts/research/ohlcv_non_hostile_transition_and_leadership_rotation_discovery_v1/candidate_panels/nhlr_07.parquet`
- `artifacts/research/ohlcv_non_hostile_transition_and_leadership_rotation_discovery_v1/candidate_panels/nhlr_08.parquet`
- `artifacts/research/ohlcv_non_hostile_transition_and_leadership_rotation_discovery_v1/candidate_panels/nhlr_09.parquet`
- `artifacts/research/ohlcv_non_hostile_transition_and_leadership_rotation_discovery_v1/candidate_panels/nhlr_10.parquet`
- all companion `*.metadata.json` files under the same directory

Reviewed panel-generation artifacts:

- `artifacts/research/ohlcv_non_hostile_transition_and_leadership_rotation_discovery_v1/candidate_panel_generation/panel_manifest.csv`
- `artifacts/research/ohlcv_non_hostile_transition_and_leadership_rotation_discovery_v1/candidate_panel_generation/candidate_panel_generation_summary.csv`
- `artifacts/research/ohlcv_non_hostile_transition_and_leadership_rotation_discovery_v1/candidate_panel_generation/panel_generation_manifest.json`
- `artifacts/research/ohlcv_non_hostile_transition_and_leadership_rotation_discovery_v1/candidate_panel_generation/panel_schema_validation_report.csv`

Reviewed code/test support:

- `pipelines/run_ohlcv_non_hostile_transition_and_leadership_rotation_discovery_v1.py`
- `pipelines/ohlcv_non_hostile_transition_leadership_rotation_candidate_implementation.py`
- `tests/test_ohlcv_non_hostile_transition_and_leadership_rotation_panel_generation.py`
- registry/scaffold tests for the same research track

## SECTION 3 - Audit Methodology

The audit used read-only artifact inspection plus existing validation/test commands.

Checks performed:

- loaded `panel_manifest.csv`, `candidate_panel_generation_summary.csv`, `panel_generation_manifest.json`, and `panel_schema_validation_report.csv`;
- loaded each parquet panel and each companion metadata JSON file;
- compared manifest rows to actual files;
- compared metadata JSON values to parquet contents;
- compared panel schema to the approved panel schema;
- compared candidate IDs, family, theme, horizon, formula name, formula version, working name, economic mechanism, implementation priority, and panel role to registry/formula manifest values;
- checked duplicate `(date, ticker, candidate_id)` keys;
- checked warmup trimming;
- checked date/ticker ordering;
- checked cross-panel calendar, ticker universe, and date/ticker grid consistency;
- checked missing-value reason values;
- checked artifact completeness and guardrail flags;
- computed file hashes for reproducibility reference without rewriting panel files.

## SECTION 4 - Registry Findings

Registry consistency passed.

Approved panel candidate IDs:

- `nhlr_01`
- `nhlr_02`
- `nhlr_03`
- `nhlr_04`
- `nhlr_05`
- `nhlr_07`
- `nhlr_08`
- `nhlr_09`
- `nhlr_10`

Registry findings:

- candidate ID order matches the authoritative registry;
- `nhlr_06` is absent from panel files, metadata files, manifests, summaries, and schema reports;
- each panel has exactly one candidate ID;
- panel `family`, `theme`, `horizon`, `working_name`, `economic_mechanism`, `implementation_priority`, `panel_role`, `formula_name`, and `formula_version` match registry/formula manifest expectations;
- `dependency_class = OHLCV_ONLY` for all panels;
- `required_input_family = OHLCV_DERIVED_ONLY` for all panels.

## SECTION 5 - Panel Integrity Findings

Panel integrity passed.

| candidate_id | row count | non-null signals | null signals | dates | tickers | start date | end date |
| --- | ---: | ---: | ---: | ---: | ---: | --- | --- |
| `nhlr_01` | 967731 | 935383 | 32348 | 1979 | 489 | 2018-06-22 | 2026-05-07 |
| `nhlr_02` | 967731 | 935847 | 31884 | 1979 | 489 | 2018-06-22 | 2026-05-07 |
| `nhlr_03` | 967731 | 935207 | 32524 | 1979 | 489 | 2018-06-22 | 2026-05-07 |
| `nhlr_04` | 967731 | 935847 | 31884 | 1979 | 489 | 2018-06-22 | 2026-05-07 |
| `nhlr_05` | 967731 | 586125 | 381606 | 1979 | 489 | 2018-06-22 | 2026-05-07 |
| `nhlr_07` | 967731 | 935527 | 32204 | 1979 | 489 | 2018-06-22 | 2026-05-07 |
| `nhlr_08` | 967731 | 935223 | 32508 | 1979 | 489 | 2018-06-22 | 2026-05-07 |
| `nhlr_09` | 967731 | 935847 | 31884 | 1979 | 489 | 2018-06-22 | 2026-05-07 |
| `nhlr_10` | 967731 | 586125 | 381606 | 1979 | 489 | 2018-06-22 | 2026-05-07 |

Integrity findings:

- no duplicate `(date, ticker, candidate_id)` keys were found;
- all panels are warmup-trimmed and contain only `warmup_complete = True` rows;
- all panels are ordered by `date`, then `ticker`;
- all panels use the approved long-form schema;
- missing values are labeled only by expected reasons: `insufficient_formula_components` and `invalid_or_missing_ohlcv`;
- lower non-null counts for `nhlr_05` and `nhlr_10` are expected because those candidates are gated by non-hostile market state and breadth-related components.

## SECTION 6 - Artifact Findings

Artifact consistency passed.

Manifest and summary checks:

- `panel_manifest.csv` contains 9 rows;
- `candidate_panel_generation_summary.csv` contains 9 rows;
- `panel_schema_validation_report.csv` contains 9 rows;
- manifest, summary, and schema report candidate IDs match the approved registry order;
- manifest row counts match parquet row counts;
- manifest non-null signal counts match parquet contents;
- metadata JSON row counts match parquet row counts;
- metadata JSON candidate IDs match parquet candidate IDs;
- panel paths and metadata paths exist for every manifest row;
- no duplicate panel paths were found.

Generation manifest checks:

- `final_classification = PANEL_GENERATION_COMPLETE_READY_FOR_IC_DISCOVERY`;
- `candidate_panels_generated = true`;
- `panel_generation_executed = true`;
- discovery, IC, redundancy, refinement, validation, governance, thresholds, production, and ML flags remain false.

## SECTION 7 - Cross-Panel Consistency Findings

Cross-panel consistency passed.

Findings:

- every panel has the same 1979-date calendar;
- every panel has the same 489-ticker universe;
- every panel has the same sorted `(date, ticker)` grid;
- every panel has 967731 rows;
- cross-panel date range is consistently `2018-06-22` through `2026-05-07`;
- cross-panel date/ticker grid hash reference begins with `96fd27014849`.

No unexpected universe, calendar, schema, or metadata drift was detected.

## SECTION 8 - Reproducibility Findings

Reproducibility checks passed for the audit boundary.

The audit confirmed:

- all expected artifacts are present;
- parquet files are readable;
- companion metadata files are readable;
- manifest values match serialized data;
- schema report status agrees with panel contents;
- deterministic artifact references can be tracked with file hashes.

Panel file SHA-256 prefixes recorded during audit:

| candidate_id | parquet SHA-256 prefix |
| --- | --- |
| `nhlr_01` | `8d308cbfc25c` |
| `nhlr_02` | `498f36aaabe8` |
| `nhlr_03` | `260b0ed6deac` |
| `nhlr_04` | `2b78a52e9d8e` |
| `nhlr_05` | `7129a4f3be6e` |
| `nhlr_07` | `bfe2601c34c6` |
| `nhlr_08` | `a81d6c6f938c` |
| `nhlr_09` | `7b0d81a643de` |
| `nhlr_10` | `7a5dfbe59a8c` |

## SECTION 9 - Test and Verification Results

Commands executed:

- `python pipelines/run_ohlcv_non_hostile_transition_and_leadership_rotation_discovery_v1.py --validate-candidate-panels` - passed
- read-only panel integrity audit script - passed with zero errors
- `pytest tests/test_ohlcv_non_hostile_transition_and_leadership_rotation_panel_generation.py` - 3 passed
- `pytest tests/test_ohlcv_non_hostile_transition_and_leadership_rotation_candidate_implementation.py tests/test_ohlcv_non_hostile_transition_and_leadership_rotation_candidate_registry.py tests/test_ohlcv_non_hostile_transition_and_leadership_rotation_discovery_scaffold.py` - 22 passed
- `pytest` - 79 passed
- final `python pipelines/run_ohlcv_non_hostile_transition_and_leadership_rotation_discovery_v1.py --validate-candidate-panels` - passed

One small test-safety fix was applied:

- `tests/test_ohlcv_non_hostile_transition_and_leadership_rotation_panel_generation.py` now writes focused test panels to temporary artifact directories instead of the approved research artifact directory.

This did not modify formulas, panel files, registry metadata, or generated research panels.

## SECTION 10 - Blocking Issues

No blocking issues were found.

## SECTION 11 - Minor Risks

Minor non-blocking notes:

- pandas emits a `FutureWarning` for the current wide OHLCV `stack` normalization path in the panel writer; this does not affect current panel integrity.
- `nhlr_05` and `nhlr_10` have materially lower non-null signal counts than the other candidates because of expected non-hostile/breadth gating. IC discovery should report coverage alongside IC metrics.
- The current audit verifies serialized artifact consistency and reproducibility references, but does not compute IC, IR, or any predictive statistic.

## SECTION 12 - Recommended Next Step

IC discovery may begin next, subject to a separately scoped IC discovery task.

Recommended next task: **Project Underdog - OHLCV Non-Hostile Transition and Leadership Rotation IC Discovery v1**.

That task may load these approved panels and compute predeclared IC diagnostics. It should continue to block redundancy screening, refinement, validation, governance mutation, production registration, threshold changes, and ML unless separately authorized.

Final classification: `PANELS_APPROVED_FOR_IC_DISCOVERY`.
