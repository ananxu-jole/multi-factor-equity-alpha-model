# Project Underdog - Research Integrity and Anti-Fabrication Audit v1

## SECTION 1 - Audit Objective

This note audits recent Project Underdog OHLCV Volatility-of-Volatility and bounded refinement work for signs of artificial, hardcoded, circular, fabricated, or non-genuine research results.

Audit classification:

- `RESEARCH_INTEGRITY_CONFIRMED_WITH_MINOR_NOTES`

No blocking integrity defect was found. The reviewed VoV and refinement IC/ranking evidence appears to be computed from approved panel artifacts and close-price forward returns rather than manually fabricated. Minor notes are recorded for artifact clarity and test-strengthening safeguards.

This audit did not modify formulas, regenerate panels, recompute production IC artifacts, change governance decisions, modify production registry files, change thresholds, or introduce ML.

## SECTION 2 - Audit Scope

Reviewed areas:

- `pipelines/`
- `tests/`
- `docs/research_notes/`
- `artifacts/research/ohlcv_volatility_of_volatility_research_module_v1/`
- `artifacts/research/ohlcv_volatility_of_volatility_refinement_v1/`

Primary VoV files inspected:

- `pipelines/run_ohlcv_volatility_of_volatility_ic_discovery_v1.py`
- `pipelines/run_ohlcv_volatility_of_volatility_refinement_ic_discovery_v1.py`
- `pipelines/run_ohlcv_volatility_of_volatility_refinement_panel_generation_v1.py`
- `pipelines/ohlcv_volatility_of_volatility_refinement_v1.py`
- `tests/test_ohlcv_volatility_of_volatility_ic_discovery_v1.py`
- `tests/test_ohlcv_volatility_of_volatility_refinement_ic_discovery_v1.py`
- `tests/test_ohlcv_volatility_of_volatility_refinement_panel_generation_v1.py`
- `tests/test_ohlcv_volatility_of_volatility_refinement_v1.py`

Primary artifact roots inspected:

- `artifacts/research/ohlcv_volatility_of_volatility_research_module_v1/panel_v1/`
- `artifacts/research/ohlcv_volatility_of_volatility_research_module_v1/ic_discovery_v1/`
- `artifacts/research/ohlcv_volatility_of_volatility_refinement_v1/panel_v1/`
- `artifacts/research/ohlcv_volatility_of_volatility_refinement_v1/ic_discovery_v1/`

## SECTION 3 - Methods Used

Hardcoding searches:

- Searched for classification and outcome labels including `ADVANCE_TO_VALIDATION_DESIGN`, `ADVANCE_TO_REFINEMENT`, `WATCH`, `REJECT`, `mean_ic`, `candidate_rankings`, `recommendation`, and `classification`.
- Searched VoV pipelines and tests for fixed-looking IC literals and suspicious manually written metrics.
- Inspected scoring paths that write `daily_ic.csv`, `candidate_horizon_ic_scores.csv`, `candidate_ic_summary.csv`, `candidate_rankings.csv`, and `manifest.json`.

Artifact-lineage checks:

- Compared panel manifests to actual parquet row counts.
- Checked duplicate `(date, ticker, candidate_id)` keys from parquet panels.
- Inspected panel metadata and generation manifests for lineage and guardrail fields.
- Compared candidate-horizon and candidate-summary artifact shapes for original and refinement IC outputs.

Test-integrity checks:

- Inspected focused VoV and refinement tests for synthetic input construction, blocked-candidate rejection, manifest guardrails, duplicate prevention, activation semantics, anchor equivalence, and timing checks.
- Ran the focused VoV/refinement test suite.

Commands run:

- `rg -n "ADVANCE_TO_VALIDATION_DESIGN|ADVANCE_TO_REFINEMENT|ADVANCE|WATCH|REJECT|mean_ic|candidate_rankings|ranking|recommendation|classification|hardcoded|expected" pipelines tests docs/research_notes artifacts/research/ohlcv_volatility_of_volatility_research_module_v1 artifacts/research/ohlcv_volatility_of_volatility_refinement_v1`
- `rg -n "0\\.0[0-9]{3,}|0\\.1[0-9]{3,}|0\\.5[0-9]{3,}|0\\.01[0-9]+|0\\.10[0-9]+|0\\.54[0-9]+|0\\.53[0-9]+|0\\.52[0-9]+|0\\.51[0-9]+" pipelines tests`
- `rg -n "to_csv|to_parquet|json.dump|write_text|DataFrame\\(|candidate_rankings|candidate_horizon_ic_scores|daily_ic|manifest|recommendation" pipelines/run_ohlcv_volatility_of_volatility_ic_discovery_v1.py pipelines/run_ohlcv_volatility_of_volatility_refinement_ic_discovery_v1.py pipelines/run_ohlcv_volatility_of_volatility_refinement_panel_generation_v1.py pipelines/ohlcv_volatility_of_volatility_refinement_v1.py`
- Manifest/parquet row-count and duplicate-key inspection via read-only Python commands.
- `python -m pytest tests/test_ohlcv_volatility_of_volatility_ic_discovery_v1.py tests/test_ohlcv_volatility_of_volatility_refinement_ic_discovery_v1.py tests/test_ohlcv_volatility_of_volatility_refinement_panel_generation_v1.py tests/test_ohlcv_volatility_of_volatility_refinement_v1.py -q`

## SECTION 4 - Hardcoding Search Results

No evidence was found that recent VoV IC values, rankings, or candidate outcomes were hardcoded into the scoring outputs.

Findings:

- IC values in `candidate_rankings.csv`, `candidate_horizon_ic_scores.csv`, `daily_ic.csv`, and research notes appear as generated artifacts or documentation of generated artifacts, not as fixed literals used by scoring code.
- Candidate IDs are hardcoded in approved-scope lists and blocked-candidate controls. This is expected governance behavior, not evidence fabrication.
- Recommendation strings such as `ADVANCE_TO_REFINEMENT`, `ADVANCE_TO_VALIDATION_DESIGN`, `WATCH`, and `REJECT` are generated by classification functions after computed metrics are available.
- Threshold constants such as mean-IC, IC-IR, positive-IC-rate, and coverage cutoffs are present in classification logic. These are decision thresholds, not fabricated output values.
- Documentation notes manually record governance outcomes, but those notes reference computed artifacts and review decisions rather than writing scoring artifacts.

Minor note:

- The original VoV IC discovery runner writes `candidate_ic_summary.csv` using the same candidate-horizon table written to `candidate_horizon_ic_scores.csv`. In the inspected artifacts, both original-module files have shape `(20, 20)` and identical columns. This is not fabricated evidence, but the filename overstates the aggregation level and should be corrected in a future cleanup. The refinement IC runner already writes a true candidate summary with shape `(8, 17)`.

## SECTION 5 - Artifact Lineage Findings

Panel artifact checks passed.

Original VoV panels:

- Manifest rows: 5.
- Total manifest row count: 5,129,610.
- Each candidate parquet row count matched its manifest row count.
- Duplicate `(date, ticker, candidate_id)` keys: 0 for all five candidates.
- Metadata and panel-generation manifests include candidate IDs, classification, timing, blocked-family, and guardrail fields.

Bounded refinement panels:

- Manifest rows: 8.
- Total manifest row count: 8,207,376.
- Each candidate parquet row count matched its manifest row count.
- Duplicate `(date, ticker, candidate_id)` keys: 0 for all eight variants.
- Metadata and panel-generation manifests include candidate IDs, formula hashes, anchor equivalence status, blocked-candidate checks, timing, and guardrail fields.

IC artifact lineage:

- Original IC manifest references approved panel root, close-price source, horizons, primary review horizons, output files, and fail-closed guardrails.
- Refinement IC manifest references approved refinement panel root, close-price source, horizons, primary review horizons, anchor mapping, output files, and fail-closed guardrails.
- `approved_panel_manifest.csv` is copied into both IC artifact roots.

No evidence was found that artifacts were overwritten without traceability during this audit.

## SECTION 6 - Pipeline Integrity Findings

Original VoV IC pipeline:

- Loads panel manifest and validates it before scoring.
- Rejects unexpected candidate IDs and Family B/C candidates.
- Loads each candidate parquet and verifies schema, candidate ID, module ID, family, and timing policy.
- Computes forward returns from close prices using `close.shift(-horizon) / close - 1.0`.
- Computes daily cross-sectional Spearman IC from `signal_value` and forward returns.
- Computes candidate-horizon scores, horizon summaries, family summaries, rolling IC diagnostics, rankings, and manifest outputs from the computed daily IC data.
- Assigns recommendations with a threshold function after metric computation.

Refinement IC pipeline:

- Loads and validates refinement panel artifacts before scoring.
- Rejects blocked candidates including original watch/park VoV IDs and `dpath_*`/`ecluster_*`.
- Loads each approved refinement parquet and verifies schema, candidate ID, module ID, family, refinement family, and timing policy.
- Computes daily cross-sectional Spearman IC from approved panels and close-price forward returns.
- Computes anchor deltas from branch anchors rather than hand-entered deltas.
- Computes rankings and recommendation labels after candidate-horizon metrics are computed.

Panel generation pipeline:

- Builds refinement panels from OHLCV source data and registry-derived refinement definitions.
- Writes manifests, formula hashes, feature manifests, input-schema manifests, schema reports, and metadata.
- Validates exactly eight expected refinement panels.
- Validates anchor equivalence before writing panels.
- Rejects unexpected extra parquet artifacts in validate-only mode.

No code path was found that changes a candidate outcome based on a desired final classification.

## SECTION 7 - Test Integrity Findings

Focused tests are meaningful rather than purely circular.

Positive findings:

- IC tests build synthetic panels and close prices, run the actual IC discovery functions, and assert generated artifact structure and guardrails.
- Blocked candidate tests mutate manifests to ensure disallowed candidates fail preflight.
- Timing tests verify expected horizons and timing policy labels.
- Refinement ranking tests verify primary-horizon ranking shape and branch anchor mapping.
- Panel-generation tests build synthetic OHLCV input, generate panels, validate exact panel IDs, verify manifests, reject duplicates, reject blocked candidates, validate inactive-zero semantics, and check validate-only behavior.
- Refinement implementation tests verify exactly eight variants, blocked candidate exclusion, long-form schema, duplicate prevention, warmup handling, inactive neutralization, original-anchor equivalence, and guardrail manifest flags.

Minor test-strengthening notes:

- IC tests do not yet include a small hand-computable Spearman IC fixture with known expected IC values. Adding one would further reduce the risk of accidental scoring drift.
- Original VoV IC tests verify artifact presence and recommendation label vocabulary, but they do not catch that `candidate_ic_summary.csv` duplicates the candidate-horizon table. A regression test should assert candidate-summary grain.
- Some tests check broad label sets rather than exact recommendation behavior under controlled metric inputs. A targeted unit test for `classify_candidate` threshold boundaries would improve assurance.

## SECTION 8 - Data Leakage And Timing Findings

No same-bar or look-ahead scoring defect was found in the inspected VoV IC runners.

Timing evidence:

- Both IC runners compute forward returns as `close.shift(-horizon) / close - 1.0`.
- Daily IC aligns signal at date `t` with the forward return from after `t`.
- Panel manifests and loaded panel rows require the timing policy `after_close_t_forward_returns_after_t`.
- Tests verify the timing-policy field and horizon set.

Residual caution:

- The forward-return expression is correct for after-close signal timing if the panel signal is indeed available after close on `t`. Panel audits and manifests record this policy, but future validation should continue to assert it at artifact load time.

## SECTION 9 - Provenance Findings

Provenance is generally strong.

Evidence:

- Panel artifacts include manifests, metadata, schema validation reports, formula manifests, feature manifests, and input schema manifests.
- IC artifacts include copied approved panel manifests, output manifests, candidate-horizon scores, rankings, rolling diagnostics, horizon summaries, and family summaries.
- Refinement artifacts include parent candidate IDs, source spec IDs, refinement families, anchor equivalence status, and formula hashes.
- Guardrail flags explicitly record whether panel generation, IC discovery, validation, governance mutation, production registration, threshold changes, and ML occurred.

Minor provenance issue:

- The original VoV `candidate_ic_summary.csv` naming/shape issue should be corrected or explicitly documented because it can confuse downstream readers expecting one row per candidate.

## SECTION 10 - Issues Found

No blocking integrity issues were found.

Minor issues:

| issue | severity | impact | recommended action |
| --- | --- | --- | --- |
| Original VoV `candidate_ic_summary.csv` duplicates candidate-horizon grain. | minor | Artifact naming is misleading; does not fabricate results. | Future cleanup should write a true candidate-level summary and add a regression test for summary grain. |
| IC tests lack a tiny hand-computable known-answer Spearman fixture. | minor | Existing tests verify behavior and guardrails, but a known-answer test would improve scoring assurance. | Add a deterministic 3-date/30-ticker fixture with manually recomputed expected IC and ranking behavior. |
| Classification thresholds are embedded in scoring runners. | minor | Acceptable as predeclared decision rules, but should stay documented and reviewed when standards evolve. | Keep threshold constants documented in discovery notes and avoid changing them during a run. |

## SECTION 11 - Corrective Actions Required

Blocking corrective actions:

- None.

Recommended safeguards:

- Add a known-answer IC unit test for original and refinement discovery runners.
- Add a candidate-summary grain regression test for original and refinement IC artifacts.
- Add hash or checksum fields for approved input panel manifests and close-price source in future IC manifests.
- Preserve the rule that docs may summarize governance decisions, but scoring artifacts must be produced only by pipeline code from approved panels.
- Keep validation-design and validation-execution artifact roots separate from IC discovery roots.

## SECTION 12 - Confidence Assessment

Confidence level in recent VoV/refinement evidence:

- Moderate-high.

Rationale:

- IC/ranking outputs are genuinely computed from approved panel artifacts and close-price forward returns.
- Panel manifests reconcile to parquet row counts.
- Duplicate key counts are zero.
- Blocked candidate checks are present in code, manifests, and tests.
- Guardrail metadata is explicit.
- Tests exercise real synthetic data paths and fail-closed behaviors.

Confidence is not rated "high" only because:

- The original candidate-summary artifact has a naming/grain defect.
- Known-answer IC tests would provide stronger protection against accidental scoring drift.
- Contamination and validation checks remain future work, not completed proof.

## SECTION 13 - Final Classification

Final classification:

- `RESEARCH_INTEGRITY_CONFIRMED_WITH_MINOR_NOTES`

No fabricated, hardcoded, circular, or non-genuine VoV/refinement research evidence was found. The recent IC/ranking evidence appears to be computed from approved panels, with minor documentation and test-hardening improvements recommended before future validation execution.
