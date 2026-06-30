# Project Underdog - OHLCV Non-Hostile Transition and Leadership Rotation Panel Generation Readiness Review v1

## SECTION 1 - Executive Summary

This review assessed whether the OHLCV Non-Hostile Transition and Leadership Rotation candidate implementation is ready for candidate panel generation.

Review result: `NOT_READY_FOR_PANEL_GENERATION`.

The candidate implementation is registry-derived, internally consistent, and safe. The nine approved candidates are implemented as research-only candidate shells, `nhlr_06` remains excluded, implementation artifacts align with the authoritative registry, and the runner commands remain fail-closed.

However, panel generation should not begin yet. The implementation explicitly keeps formulas blocked through `FORMULA_NOT_DEFINED_PANEL_BLOCKED`, and neither horizons nor panel roles are defined in the implementation manifest. This is appropriate for the current implementation layer, but it is a blocking gap for actual panel generation.

No candidate panels were generated. No discovery, IC scoring, redundancy screening, refinement, validation, governance mutation, threshold change, production registration, or ML work was performed.

## SECTION 2 - Files Reviewed

Reviewed implementation module:

- `pipelines/ohlcv_non_hostile_transition_leadership_rotation_candidate_implementation.py`

Reviewed runner extensions:

- `pipelines/run_ohlcv_non_hostile_transition_and_leadership_rotation_discovery_v1.py`
- `--list-candidate-implementations`
- `--export-candidate-implementations`
- `--validate-candidate-implementations`

Reviewed implementation artifacts:

- `artifacts/research/ohlcv_non_hostile_transition_and_leadership_rotation_discovery_v1/candidate_implementation/candidate_implementation_manifest.csv`
- `artifacts/research/ohlcv_non_hostile_transition_and_leadership_rotation_discovery_v1/candidate_implementation/candidate_implementation_manifest.json`
- `artifacts/research/ohlcv_non_hostile_transition_and_leadership_rotation_discovery_v1/candidate_implementation/candidate_implementation_diagnostics.csv`
- `artifacts/research/ohlcv_non_hostile_transition_and_leadership_rotation_discovery_v1/candidate_implementation/candidate_implementation_summary.json`
- `artifacts/research/ohlcv_non_hostile_transition_and_leadership_rotation_discovery_v1/candidate_implementation/candidate_registration_map.csv`

Reviewed implementation note:

- `docs/research_notes/ohlcv_non_hostile_transition_and_leadership_rotation_candidate_implementation_v1.md`

Reviewed tests:

- `tests/test_ohlcv_non_hostile_transition_and_leadership_rotation_candidate_implementation.py`
- `tests/test_ohlcv_non_hostile_transition_and_leadership_rotation_candidate_registry.py`
- `tests/test_ohlcv_non_hostile_transition_and_leadership_rotation_discovery_scaffold.py`

## SECTION 3 - Readiness Findings

1. Is the candidate implementation registry-derived and consistent with the authoritative registry?

Yes. The implementation module derives implementation rows from `candidate_registry_rows()` and `APPROVED_CANDIDATE_IDS`. It does not maintain a separate candidate-definition table. The exported implementation manifest preserves registry identity, family, concept category, economic mechanism, priority, dependency, namespace, diagnostic identifier, and guardrail metadata.

During this review, implementation validation was strengthened to compare exported implementation metadata against current registry metadata, not just candidate IDs. This reduces stale-artifact and metadata drift risk before any later panel work.

2. Are candidate identities, names, families, horizons, roles, and metadata stable enough for panel generation?

Partially.

Stable enough:

- candidate identifiers;
- working names;
- family;
- concept categories;
- economic mechanisms;
- implementation priorities;
- dependency classes;
- required input families;
- prohibited dependencies;
- registry artifact namespaces;
- diagnostic identifiers.

Not yet stable enough:

- panel formulas are not defined;
- horizons are not defined;
- panel roles are not defined;
- output panel schema for these candidates is not yet specified;
- formula-to-registry mapping is not yet available.

The implementation is ready for a formula and panel-specification task, but not for panel generation itself.

3. Are there duplicate metadata declarations that could drift?

No active duplicate implementation registry was found. The implementation module derives records from registry helpers rather than redeclaring candidates.

Minor drift risk remains in exported artifacts if the registry changes and implementation artifacts are not regenerated. The added metadata-consistency validation now mitigates that risk by failing if implementation artifact metadata diverges from current registry metadata.

4. Are runner commands sufficient and safe?

Yes for implementation readiness. The runner supports listing, exporting, and validating candidate implementations. It does not expose panel generation, discovery, IC, redundancy, refinement, validation, production registration, governance mutation, threshold mutation, or ML commands for this track.

Runner output and manifests explicitly preserve fail-closed fields for panel generation and empirical work.

5. Are tests meaningful enough to catch implementation/registry drift?

Yes for the implementation layer. Tests verify:

- candidate registration;
- implementation completeness;
- registry ID alignment;
- `nhlr_06` exclusion;
- duplicate prevention;
- metadata drift against registry values;
- implementation artifact generation;
- fail-closed manifest fields;
- unsupported execution modes.

The tests do not verify formula correctness, horizon assignment, or panel values because those do not exist yet.

## SECTION 4 - Blocking Issues

Panel generation is blocked by design until formula and panel-generation boundaries are specified.

Blocking items:

- `formula_status` is `FORMULA_NOT_DEFINED_PANEL_BLOCKED` for every candidate.
- No candidate horizon metadata is present in the implementation manifest.
- No candidate panel role metadata is present.
- No formula or signal construction functions exist for the nine candidates.
- No panel output schema or required panel columns are defined for this OHLCV candidate family.
- No pre-panel formula-boundary review artifact exists.

These are not implementation-registry defects. They are missing prerequisites for actual panel generation.

## SECTION 5 - Minor Risks

- The implementation artifact manifest currently carries `READY_FOR_PANEL_GENERATION_REVIEW`, which is accurate for review readiness but should not be read as authorization to generate panels.
- The requested registry review note, `docs/research_notes/ohlcv_non_hostile_transition_and_leadership_rotation_candidate_registry_review_v1.md`, was not present in the workspace during the prior implementation task. The current review therefore relies on the registry implementation note and registry artifacts.
- Future formula work must avoid reintroducing candidate metadata tables. Formula modules should consume candidate metadata from the registry-derived implementation layer.

## SECTION 6 - Review Fix Applied

One limited readiness hardening fix was applied:

- `validate_candidate_implementations()` now checks implementation metadata values against current authoritative registry values, including working name, family, concept category, economic mechanism, implementation priority, dependency fields, artifact namespace, and diagnostic identifier.
- Focused tests now mutate a working name and confirm the validator catches `registry_metadata_consistency` drift.

This did not change candidate definitions.

## SECTION 7 - Verification Commands

Commands run:

- `python -m py_compile pipelines/run_ohlcv_non_hostile_transition_and_leadership_rotation_discovery_v1.py pipelines/ohlcv_non_hostile_transition_leadership_rotation_candidate_implementation.py` - passed
- `python pipelines/run_ohlcv_non_hostile_transition_and_leadership_rotation_discovery_v1.py --export-candidate-implementations` - passed
- `pytest tests/test_ohlcv_non_hostile_transition_and_leadership_rotation_candidate_implementation.py` - 6 passed
- `pytest tests/test_ohlcv_non_hostile_transition_and_leadership_rotation_candidate_registry.py tests/test_ohlcv_non_hostile_transition_and_leadership_rotation_discovery_scaffold.py` - 16 passed
- `python pipelines/run_ohlcv_non_hostile_transition_and_leadership_rotation_discovery_v1.py --validate-candidate-implementations` - passed
- `pytest` - 70 passed

## SECTION 8 - Recommended Next Step

The next task should be **Project Underdog - OHLCV Non-Hostile Transition and Leadership Rotation Formula and Panel Specification v1**.

That task should define, review-only or specification-first:

- formula boundaries for each of the nine approved candidates;
- candidate horizon policy;
- panel role metadata;
- panel output schema;
- input requirements and availability checks;
- formula-to-registry mapping;
- prohibited dependency checks for formula construction;
- pre-panel guardrails.

It should still not execute discovery, calculate IC, run redundancy screening, run refinement, run validation, modify governance, change thresholds, register production artifacts, or implement ML.

Final classification: `NOT_READY_FOR_PANEL_GENERATION`.
