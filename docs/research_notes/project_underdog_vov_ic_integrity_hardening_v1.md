# Project Underdog - VoV IC Integrity Hardening v1

## SECTION 1 - Objective

This note records the integrity hardening applied after `project_underdog_research_integrity_and_anti_fabrication_audit_v1.md`.

Classification:

- `IC_INTEGRITY_HARDENING_COMPLETE`

The hardening addressed minor audit notes only. No IC formulas were changed, no existing IC artifacts were regenerated, no panels were modified, no discovery run was rerun against research artifacts, no candidate rankings were altered, no governance decisions were changed, no production registry files were changed, no thresholds were changed, and no ML was introduced.

## SECTION 2 - Inputs Reviewed

Reviewed:

- `docs/research_notes/project_underdog_research_integrity_and_anti_fabrication_audit_v1.md`
- `pipelines/run_ohlcv_volatility_of_volatility_ic_discovery_v1.py`
- `pipelines/run_ohlcv_volatility_of_volatility_refinement_ic_discovery_v1.py`
- `tests/test_ohlcv_volatility_of_volatility_ic_discovery_v1.py`
- `tests/test_ohlcv_volatility_of_volatility_refinement_ic_discovery_v1.py`
- relevant VoV/refinement panel-generation and implementation tests.

## SECTION 3 - Hardening Implemented

1. Known-answer IC fixture.

- Added tiny hand-computable Spearman IC tests for the original VoV IC runner.
- Added tiny hand-computable Spearman IC tests for the bounded refinement IC runner.
- The fixture uses 30 tickers so it exceeds the minimum daily observation threshold.
- The expected IC values are exactly `1.0` for matching ranks and `-1.0` for reversed ranks.
- Added a small forward-return timing fixture confirming `close.shift(-horizon) / close - 1.0` uses prices after signal date `t`.

2. Candidate-summary grain regression.

- Added regression tests confirming `candidate_ic_summary` is candidate-level, not candidate-horizon grain.
- Updated the original VoV IC runner so future `candidate_ic_summary.csv` outputs are true candidate-level summaries with one row per candidate.
- The bounded refinement runner already had candidate-level summary behavior; tests now lock that behavior.
- Existing research artifacts were not rewritten, so prior IC outputs and rankings remain unchanged.

3. Input manifest/source checksum expectations.

- Added SHA-256 checksum fields to future IC manifests for:
  - `panel_manifest.csv`
  - the close-price source used for forward returns.
- Added tests confirming these checksum fields are present and shaped as SHA-256 strings when the runners write test-fixture manifests.

4. Stable threshold documentation.

- Replaced inline classification threshold literals with named constants in the original and refinement IC runners.
- Added `classification_thresholds` to future IC manifests.
- Added tests confirming the manifest threshold block matches the runner constants.
- Threshold values were not changed.

## SECTION 4 - Files Changed

Pipeline files:

- `pipelines/run_ohlcv_volatility_of_volatility_ic_discovery_v1.py`
- `pipelines/run_ohlcv_volatility_of_volatility_refinement_ic_discovery_v1.py`

Test files:

- `tests/test_ohlcv_volatility_of_volatility_ic_discovery_v1.py`
- `tests/test_ohlcv_volatility_of_volatility_refinement_ic_discovery_v1.py`

Research note:

- `docs/research_notes/project_underdog_vov_ic_integrity_hardening_v1.md`

## SECTION 5 - Prior Result Preservation

Prior results changed:

- No.

Existing artifact roots were not regenerated or rewritten:

- `artifacts/research/ohlcv_volatility_of_volatility_research_module_v1/panel_v1/`
- `artifacts/research/ohlcv_volatility_of_volatility_research_module_v1/ic_discovery_v1/`
- `artifacts/research/ohlcv_volatility_of_volatility_refinement_v1/panel_v1/`
- `artifacts/research/ohlcv_volatility_of_volatility_refinement_v1/ic_discovery_v1/`

Candidate rankings changed:

- No existing ranking artifact was modified.

Threshold values changed:

- No. Thresholds were only named and emitted into future manifests for traceability.

IC formulas changed:

- No. Daily IC still uses cross-sectional rank correlation between `signal_value` and strictly forward returns.

## SECTION 6 - Verification

Verification commands run:

| command | result |
| --- | --- |
| `python -m py_compile pipelines/run_ohlcv_volatility_of_volatility_ic_discovery_v1.py pipelines/run_ohlcv_volatility_of_volatility_refinement_ic_discovery_v1.py tests/test_ohlcv_volatility_of_volatility_ic_discovery_v1.py tests/test_ohlcv_volatility_of_volatility_refinement_ic_discovery_v1.py` | passed |
| `python -m pytest tests/test_ohlcv_volatility_of_volatility_ic_discovery_v1.py tests/test_ohlcv_volatility_of_volatility_refinement_ic_discovery_v1.py -q` | passed, 16 tests |
| `python -m pytest tests/test_ohlcv_volatility_of_volatility_refinement_panel_generation_v1.py tests/test_ohlcv_volatility_of_volatility_refinement_v1.py tests/test_ohlcv_volatility_of_volatility_research_module_v1.py tests/test_ohlcv_volatility_of_volatility_panel_generation_v1.py -q` | passed, 29 tests |

Verification interpretation:

- Known-answer IC behavior is now directly tested.
- Forward-return timing is directly tested.
- Candidate-summary grain is directly tested.
- Manifest threshold and checksum metadata are directly tested.
- VoV/refinement panel-generation and implementation behavior remains intact.

## SECTION 7 - Guardrail Confirmation

Confirmed:

- No IC formula changes.
- No existing IC result changes.
- No candidate ranking changes.
- No panel changes.
- No research artifact regeneration.
- No governance decision changes.
- No production registry changes.
- No threshold value changes.
- No ML introduction.

## SECTION 8 - Final Classification

Final classification:

- `IC_INTEGRITY_HARDENING_COMPLETE`

The minor integrity audit notes have been addressed through code-path hardening, test coverage, and future manifest provenance metadata. Validation work may continue using the hardened IC runners, subject to the existing validation-design guardrails.
