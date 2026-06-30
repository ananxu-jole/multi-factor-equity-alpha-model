# Alpha Family Diversification Framework — Post-Implementation Dry-Run Review v2

Date: 2026-06-17

**Purpose**: review-only audit of the implemented research-only scaffold for the alpha-family diversification discovery framework. This review verifies safety, registry completeness, artifact readiness, redundancy-hook readiness, and lists required fixes before any discovery execution.

**Scope**: review of the following (inspection-only):
- `pipelines/run_alpha_family_diversification_discovery_v1.py`
- `docs/research_notes/alpha_family_diversification_framework_implementation_v1.md`
- `docs/research_notes/alpha_family_diversification_framework_dry_run_review_v1.md`
- `artifacts/research/alpha_family_diversification_discovery_v1/` and contained files

----

**SECTION 1 — Executive Review**

- **Implementation completeness**: The scaffold runner `pipelines/run_alpha_family_diversification_discovery_v1.py` and the expected artifact scaffold were implemented. Core pieces present: static candidate registry, artifact directories, manifest generation, and placeholder CSVs for redundancy, diagnostics, and governance review.
- **Dry-run readiness**: `--dry-run` creates artifact directories and files under `artifacts/research/alpha_family_diversification_discovery_v1/` without performing discovery. The runner supports `--list-candidates` and `--describe` for inspection. Dry-run was exercised and completed successfully.
- **Safety status**: The manifest and runner explicitly declare research-only behavior; production registration and state mutation flags are false. The `--run` path is intentionally unimplemented and returns an explanatory message.
- **Ready for discovery-logic implementation?** Yes — the scaffold is ready for developers to implement discovery logic, subject to the fixes and additions listed in SECTION 6.

----

**SECTION 2 — Safety and Guardrail Review**

- **Research-only behavior**: Confirmed. `RESEARCH_ONLY_GUARDRAIL` string exists and the manifest contains `research_only: true`.
- **No production registration**: Confirmed — manifest fields include `production_registration: false` and the runner does not call any registration APIs.
- **No governance mutation**: Confirmed — placeholder governance CSV exists but no code mutates governance state.
- **No validation threshold mutation**: Confirmed by manifest flags (`validation_thresholds_modified: false`) and absence of code that touches validation state.
- **No candidate promotion/demotion**: Confirmed — the scaffold writes local artifacts only; there is no promotion logic.
- **`--dry-run` safety**: Confirmed—creates files in `artifacts/research/...` only and prints a single informational line.
- **`--run` guard**: Confirmed—`--run` is present but intentionally unimplemented and returns a non-zero exit with an explanatory message.

Evidence: `artifacts/research/alpha_family_diversification_discovery_v1/manifest.json` contains research flags and `candidate_count` with expected values.

----

**SECTION 3 — Candidate Registry Review**

- **Required metadata present**: The registry CSV includes the following fields: `candidate_id`, `signal_name`, `family`, `theme`, `feature_group`, `horizon`, `redundancy_risk`, `research_status`, `mechanism_thesis`, `run_id`.
- **Dispersion vs Persistence separation**: Confirmed — entries are clearly grouped by `family` values `dispersion` and `persistence` and themes are appropriate.
- **Registry count**: The manifest reports `candidate_count: 17` and the CSV contains 17 rows — count matches the approved specification in the scaffold.
- **No stress/participation candidates included**: Confirmed — registry families are `dispersion` and `persistence`; no `stress`/`participation` families were introduced.

Observations: the registry is static and auditable. It would benefit from a small set of additional audit fields (see SECTION 6).

----

**SECTION 4 — Artifact Review**

- **Directory structure**: present and sane:
  - artifacts/research/alpha_family_diversification_discovery_v1/
    - candidate_inventory/
    - discovery_summary/
    - diagnostics/
    - redundancy_screening/
    - governance_review/
- **manifest completeness**: `manifest.json` contains run-level metadata and guardrail flags (`research_only`, `production_registration`, `validation_thresholds_modified`, `governance_modified`, `ml_integration`). Good baseline.
- **Placeholder outputs usefulness**: Placeholders exist for redundancy screening, diagnostics, and governance review with sensible column headers. They are useful as schema stubs but contain no rows — suitable for dry-run audit and follow-up development.
- **Governance review artifact readiness**: `framework_governance_review.csv` exists as a checklist scaffold; needs concrete review items and owners before discovery execution.
- **Compatibility with research standards**: The scaffold follows track-B runner conventions used elsewhere in the repo and keeps outputs under the `artifacts/research` namespace, preserving production isolation.

----

**SECTION 5 — Redundancy Screening Readiness**

- **Current state**: The redundancy artifact is a placeholder CSV with columns: `candidate_id,signal_name,comparison_signal,value_correlation,rank_correlation,notes`.
- **Sufficiency for next phase**: The placeholder is a good hook but insufficient alone. For a production-ready redundancy screening module we need:
  - a canonical mapping from `signal_name` to the actual signal generation pipeline/module (source handle)
  - time-window and sample-size parameters for correlation calculations
  - clear thresholds and decision rules (e.g., rank_corr > 0.85 => high redundancy)
  - automated comparison targets (existing participation/stress families, survivor/watchlist panels)
  - reproducible summary statistics and provenance fields (calculation_date, lookback, universe_filter)

These elements are required before discovery execution so that redundancy decisions are auditable and deterministic.

----

**SECTION 6 — Required Fixes Before Discovery Logic**

Blocking fixes (must be implemented before running discovery):
- **Signal-to-source mapping**: add a deterministic mapping (registry column or separate manifest) that ties `signal_name` to the generating function/module and input data feeds. Discovery must not implicitly assume names map to existing code.
- **Registry schema validation**: implement a small validation routine (ran during `--dry-run` or CI) that enforces unique `candidate_id`, present required fields, and valid `redundancy_risk` enumerations.
- **Redundancy screening implementation**: implement the redundancy metrics (value and rank correlations over defined lookbacks), include provenance fields, and write machine-readable decisions (pass/fail and reason). Define thresholds in-code and in the manifest for auditability.
- **Governance checklist completion**: populate `framework_governance_review.csv` with review items, owners, and acceptance criteria; require a governance-approval flag before `--run` is enabled.

Recommended improvements (implement before enabling `--run`, but not strictly blocking for developer testing):
- **Add audit metadata**: `owner`, `approval_date`, `source_reference`, `expected_data_requirements`, and `notes` in registry rows.
- **Unit tests and CI checks**: small tests for registry parsing, manifest generation, and `--dry-run` idempotency.
- **Registry JSON Schema**: include a JSON Schema or pydantic model for the registry for machine validation and editor autocompletion.
- **Logging and dry-run verbosity**: add structured logging (timestamp, run_id, action) so dry-run outputs are reproducible in logs.

Optional improvements (nice-to-have):
- **Schema-backed manifest** and versioning for the framework run (semantic run versioning).
- **Sample data harness** to validate redundancy metrics on a small, synthetic sample during CI.
- **Integration stubs for dashboards** (summary JSON or saved fig) to accelerate review sessions.

----

**SECTION 7 — Final Recommendation**

1. **Is the scaffold safe and complete?**
- Answer: Yes — the scaffold is safe (research-only, manifests and placeholders in-place) and functionally complete as a scaffold.

2. **Is it ready for discovery logic implementation?**
- Answer: Yes — developers can implement discovery logic inside the scaffold, provided they first implement the blocking fixes in SECTION 6 (signal mapping, registry validation, redundancy implementation, governance checklist completion).

3. **Is it ready for actual discovery execution?**
- Answer: No — do not run `--run` yet. The scaffold lacks redundancy decision logic, source mapping, schema validation, and a completed governance checklist. These are required for auditable execution.

4. **What must be implemented next?**
- Answer: Implement the blocking fixes listed in SECTION 6. Prioritize: (a) signal-to-source mapping, (b) redundancy screening module with thresholds and provenance fields, (c) registry schema validation and CI checks, (d) populate governance checklist and require governance approval gating.

5. **What should the next Codex task be?**
- Answer: Implement the `redundancy_screening` module and integrate it with the runner. Deliverables for that task:
  - a `pipelines/utils/redundancy.py` (or similar) implementing value/rank correlation calculations, lookback config, and decision rules;
  - registry-to-source mapping implemented and validated;
  - unit tests exercising redundancy calculations on synthetic data;
  - update `--dry-run` to perform a simulated redundancy pass that writes non-destructive output.

----

**Appendix — Evidence snapshot**

- `manifest.json` flags: `research_only: true`, `production_registration: false`, `validation_thresholds_modified: false`, `governance_modified: false`.
- Registry sample: 17 candidates split between `dispersion` and `persistence` families; headers include `candidate_id,signal_name,family,theme,feature_group,horizon,redundancy_risk,research_status,mechanism_thesis,run_id`.
- Placeholders: `redundancy_screening/redundancy_screening_placeholder.csv`, `diagnostics/panel_diagnostics_placeholder.csv`, `governance_review/framework_governance_review.csv` (headers-only stubs).

----

If you want, I can now: (a) implement the registry validation and a small JSON Schema (blocking), or (b) start the `redundancy_screening` module with tests (next Codex task recommendation). Which should I start? 
