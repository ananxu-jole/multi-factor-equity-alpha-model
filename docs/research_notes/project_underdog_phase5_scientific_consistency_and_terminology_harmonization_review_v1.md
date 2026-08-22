# Project Underdog - Phase 5 Scientific Consistency And Terminology Harmonization Review v1

Date: 2026-07-16

## 1. Executive Scientific Classification

Final classification: `PHASE5_SCIENTIFIC_FRAMEWORK_HARMONIZED_WITH_MINOR_TERMINOLOGY_UPDATES`

This review assesses whether the current Project Underdog Phase 5 scientific corpus describes information roles, contextual reasoning, governance, and module boundaries using one coherent scientific language. It does not change scientific conclusions. It does not define measurements, formulas, candidates, registries, panels, implementation, validation, production logic, governance changes, or ML.

Repository basis:

- Phase 5 WS1-WS9: authority, identity, economic context, peer-relative hypotheses, contamination, falsification, reinterpretation, integrated inventory, and ML readiness.
- `docs/research_notes/project_underdog_phase5_first_module_scientific_boundary_definition_v1.md`: first empirical module boundary narrowed to `Common-Versus-Idiosyncratic Post-Stress Repair Decomposition`.
- `docs/research_notes/project_underdog_strategic_program_reassessment_v1.md`: `PROJECT_READY_FOR_NEXT_MAJOR_PHASE`; family diversity remains insufficient for ML; broad OHLCV-only discovery is no longer the main frontier.
- `docs/research_notes/project_underdog_phase5_external_information_integration_program_v1.md`: `PHASE_5_PROGRAM_DEFINED`; Phase 5 is scientific external-information integration, not implementation.
- `docs/research_notes/project_underdog_phase5_scientific_research_roadmap_v1.md`: `PHASE_5_SCIENTIFIC_ROADMAP_DEFINED`; external context and peer-relative science are sequenced before ML readiness.
- `docs/research_notes/project_underdog_phase5_integrated_scientific_information_inventory_v1.md`: `INTEGRATED_SCIENTIFIC_INFORMATION_INVENTORY_DEFINED_WITH_OPEN_GAPS`; role and maturity taxonomies are explicit.
- `docs/research_notes/project_underdog_phase5_ml_readiness_science_v1.md`: `ML_NOT_SCIENTIFICALLY_JUSTIFIED_YET`; continue Phase 5 without ML.
- Platform v2 and lifecycle/governance notes: hypothesis-first discipline, frozen horizons, bounded refinement, candidate discipline, validation separation, artifact lineage, reproducibility, and negative-evidence preservation remain authoritative.

Conclusion:

The Phase 5 repository now reflects one coherent scientific philosophy. Minor terminology updates are recommended to make that philosophy easier to carry into measurement specification and future readiness review. No conceptual reconciliation is required.

## 2. Repository-Wide Terminology Review

| Term class | Current status | Evidence in repository | Recommendation |
|---|---|---|---|
| Scientific information | Stable. | WS8 defines information by scientific role and maturity. | Preserve as top-level umbrella. |
| Alpha Information | Stable but recently formalized. | WS8/WS9 and first-module boundary distinguish alpha from context. | Use for predictive hypothesis-supporting information. |
| Contextual Information | Stable and should become preferred. | WS3, WS7, WS8, WS9, and boundary note use context as comparator, control, decomposition, interpretation, or conditioning. | Use for economic, market, and macro layers that interpret alpha. |
| Governance Information | Stable but should be named more consistently. | WS1/WS2/source/PIT/reproducibility notes define authority, identity, lineage, provenance, PIT semantics, and auditability as correctness gates. | Use for trust, time safety, authority, and reproducibility information. |
| External information | Stable but broad. | WS1 and Phase 5 program use it to describe source-origin information and authority science. | Keep when discussing source origin or authority; migrate to contextual information when discussing scientific role. |
| Economic context | Stable. | WS3 defines it as point-in-time comparison structure. | Preserve. |
| Market context | Stable but mostly implicit through existing OHLCV state families. | WS3/WS5/WS8/WS9 use market state, stress state, participation, volatility, liquidity, and transition as controls. | Name explicitly as a contextual layer. |
| Macroeconomic context | Underrepresented but conceptually coherent. | WS3 and first-module boundary defer macro because known-date and scope issues are unresolved. | Add as deferred contextual layer, not Phase 5 first-module scope. |
| Common-versus-idiosyncratic decomposition | Stable as scientific concept, slightly over-labeled as information role. | WS7/WS8/boundary note treat it as leading interpretation of the first module. | Prefer "interpretive outcome"; keep current code-like label only as inventory shorthand. |
| Evidence maturity | Stable. | WS8 defines maturity taxonomy; WS9 separates maturity from readiness. | Preserve and keep separate from role. |
| Implementation readiness | Stable. | WS8/WS9/boundary note define prerequisites without authorizing code. | Preserve as later review category. |
| Diagnostic-only | Stable. | Static/current metadata and fallback peer context remain diagnostic-only across WS1/WS3/WS8/WS9. | Preserve. |
| Peer-relative | Stable but must remain role-scoped. | WS4-WS7 and boundary note narrow broad peer-relative claims. | Use only when peer comparator is scientifically valid and PIT-safe. |

Deprecated or discouraged language:

- "external information feature" when the intended role is context, authority, or governance;
- "peer feature" before peer authority and context validity exist;
- "common/idiosyncratic information" when the intended meaning is decomposition outcome;
- "context alpha" unless predictive incrementality has been empirically demonstrated;
- "implementation-ready" for any Phase 5 framework artifact.

## 3. Alpha Information Review

Alpha Information is consistently defined in substance, even though the exact phrase is recent.

Repository-consistent meaning:

Alpha Information generates, supports, or validates predictive scientific hypotheses.

Current Alpha Information examples:

- hostile/stress repair;
- participation repair;
- liquidity repair;
- volatility compression;
- VoV;
- persistence;
- rank stability;
- transition-state evidence when used as an alpha or conditioning family.

Consistency assessment:

- Existing OHLCV families are consistently treated as the alpha-information anchor.
- Validated or conditional evidence is not treated as production readiness.
- Parked families remain negative information, not latent alpha.
- Contextual information is not automatically promoted into Alpha Information.

Minor terminology update:

Future notes should explicitly call existing repair/stabilization/participation/volatility/VoV/persistence/rank evidence `Alpha Information` when contrasting it with context.

## 4. Contextual Information Review

Contextual Information is consistently described as information that improves interpretation, conditioning, comparison, decomposition, attribution, or explanation of alpha information.

### Economic Context

Status: coherent and explicit.

Includes:

- peers;
- sector;
- industry;
- company identity;
- ticker lineage;
- company-security relationships;
- listing history;
- exchange history;
- size.

WS3 defines economic context as a point-in-time comparison structure, not a static metadata label. WS1 and WS2 define why authority and identity are prerequisites. WS4-WS8 preserve the rule that peer/economic context remains blocked for empirical use until authoritative evidence exists.

### Market Context

Status: coherent but should be named explicitly.

Includes:

- market state;
- participation state;
- stress state;
- transition state;
- volatility regime;
- liquidity regime.

These appear throughout existing OHLCV family evidence and contamination controls. They are already used as controls and conditioning information, but the repository should increasingly name them as `Market Context` to distinguish them from `Economic Context`.

### Macroeconomic Context

Status: scientifically coherent but not fully represented.

Potential future layers:

- interest-rate regime;
- inflation regime;
- monetary regime;
- credit conditions;
- business cycle;
- broader macroeconomic environment.

Macroeconomic context should be placed under Contextual Information as a deferred future layer. It should not expand the first Phase 5 module or be inserted into formulas without separate authority, known-date, and scope review.

## 5. Governance Information Review

Governance Information remains consistently separated from predictive information.

Repository-consistent examples:

- identity;
- lineage;
- provenance;
- PIT semantics;
- source authority;
- reproducibility;
- auditability;
- retention;
- artifact lineage;
- temporal validity;
- source-known dates;
- candidate lifecycle metadata;
- validation manifests and checksums.

Assessment:

- WS1 treats authority as a prerequisite, not a signal.
- WS2 treats identity and lineage as correctness constraints, not predictive features.
- Validation and lifecycle notes treat registries and artifacts as governance surfaces.
- WS8 and WS9 explicitly warn that governance information should constrain research, not become predictive input.

No conceptual inconsistency found.

## 6. Information-Role Consistency

| Corpus area | Consistency finding |
|---|---|
| Inventories | WS8 explicitly separates validated, supported, contextual, explanatory, diagnostic, negative, hypothetical, missing, and insufficiently evidenced information. |
| Workstreams | WS1-WS9 preserve the difference between source authority, identity, context, hypothesis, contamination, falsification, reinterpretation, inventory, and ML readiness. |
| Boundary definitions | First-module boundary correctly narrows the selected module to decomposition and separates alpha, context, and governance. |
| ML readiness | WS9 correctly treats information diversity, maturity, context authority, and governance as prerequisites rather than features. |
| Reinterpretation | WS7 treats external/economic context as explanation, decomposition, conditioning, benchmark, or refinement before new alpha. |
| Contamination | WS5 treats context, identity, timing, and source issues as contamination controls. |
| Falsification | WS6 preserves negative evidence and prevents resurrection through relabeling. |

Information roles are consistent. Minor improvement: future notes should explicitly state the role first, then maturity, then readiness.

## 7. Evidence-Maturity Consistency

Evidence maturity is consistently separated from:

- information role;
- implementation;
- validation;
- production.

Examples:

- VoV can be `VALIDATED` at candidate-lineage level without production readiness or full independence.
- persistence/rank can be conditional evidence without broad family proof.
- static metadata can be diagnostic regardless of coverage.
- context can be conceptually important while blocked pending authority.
- the first module can be `HYPOTHESIS_DEFINED` without formula readiness.
- ML can remain unjustified despite mature governance.

Recommendation:

Maintain a three-axis distinction in future documents:

1. Information role: Alpha, Contextual, Governance, Negative, Diagnostic, Explanatory.
2. Evidence maturity: conceptual, hypothesis-defined, diagnostic, discovery, refined discovery, validated, archived negative, retired, blocked.
3. Readiness state: measurement-ready, formula-ready, implementation-ready, validation-ready, production-ready, ML-ready.

## 8. Common-Versus-Idiosyncratic Terminology Review

Current term:

`COMMON_IDIOSYNCRATIC_DECOMPOSITION_INFORMATION`

Assessment:

The term is useful as an inventory shorthand, but the repository evidence now supports treating common-versus-idiosyncratic decomposition primarily as an interpretive outcome generated by combining Alpha Information and Contextual Information.

Preferred scientific phrasing:

`common-versus-idiosyncratic decomposition outcome`

Recommended usage:

- Use "common-versus-idiosyncratic decomposition" for the scientific concept.
- Use "decomposition outcome" when describing the result of combining alpha evidence with valid context.
- Keep `COMMON_IDIOSYNCRATIC_DECOMPOSITION_INFORMATION` only as a backward-compatible inventory role label until a future documentation cleanup replaces it.
- Do not treat decomposition as a standalone raw input or alpha family.

No scientific conclusion changes.

## 9. External Versus Contextual Terminology

The repository uses "external information" consistently for Phase 5's source-origin problem. It should remain valid for:

- source authority;
- provenance;
- vendor/source-independent evidence standards;
- PIT semantics;
- source-known dates;
- retention and reproducibility;
- external evidence acceptance.

When the scientific role is interpretation, comparison, conditioning, or decomposition, future notes should prefer:

- `Contextual Information`;
- `Economic Context`;
- `Market Context`;
- `Macroeconomic Context`;
- `contextual comparator`;
- `contextual control`;
- `contextual interpretation`.

Recommendation:

Gradually migrate role-based discussions from "external information" to "contextual information" where appropriate. Do not replace "External Information Authority Science"; that phrase correctly describes the authority gate for source-origin evidence.

## 10. First-Module Consistency

The selected first module remains consistent with the overall Phase 5 philosophy.

Current boundary:

`Common-Versus-Idiosyncratic Post-Stress Repair Decomposition`

Consistency findings:

- It is minimal and avoids bundling stabilization, asymmetry, participation/liquidity, VoV, rank, transition, and macro context.
- It treats existing repair evidence as Alpha Information.
- It treats peer/economic context as Contextual Information.
- It treats identity, lineage, authority, provenance, PIT semantics, and reproducibility as Governance Information.
- It treats decomposition as an interpretive outcome, not a formula or alpha claim.
- It preserves the strongest alternative interpretation: existing repair-family refinement.

No boundary correction is required.

## 11. Context Hierarchy Review

Project Underdog now supports this hierarchy:

1. Economic Context
2. Market Context
3. Macroeconomic Context

Scientific coherence:

- Economic Context explains whether securities or companies are economically comparable at a historical time.
- Market Context explains broad state, stress, participation, volatility, liquidity, and transition conditions already observable within the OHLCV evidence system.
- Macroeconomic Context would explain broader monetary, credit, inflation, rate, and business-cycle conditions, but remains deferred because authority, date semantics, and scope have not been defined.

Recommended hierarchy:

Scientific Information

Alpha Information

Contextual Information:

- Economic Context
- Market Context
- Macroeconomic Context

Governance Information

This hierarchy is scientifically coherent if the arrows are interpreted as role categories, not a strict inheritance tree. Contextual Information is not subordinate to Alpha Information in importance; it is subordinate only in the sense that it typically interprets Alpha Information before becoming predictive.

## 12. Module-Boundary Consistency

Current module boundaries are appropriately minimal.

Examples:

- WS1 defines source authority without accepting sources.
- WS2 defines identity and lineage without constructing records.
- WS3 defines economic context without building peer groups.
- WS4 defines hypotheses without formulas.
- WS5 defines contamination/orthogonality without empirical testing.
- WS6 defines falsification without retiring the selected module empirically.
- WS7 defines reinterpretation without claiming new alpha.
- WS8 inventories information without creating registries or implementation artifacts.
- WS9 assesses ML readiness without introducing ML.
- First-module boundary narrows the first future module to one claim.

The repository consistently avoids combining related mechanisms merely because they are adjacent.

## 13. Scientific Philosophy Summary

Project Underdog's Phase 5 scientific philosophy can be summarized as follows:

Project Underdog separates scientific information by role before source, maturity, or implementation. Alpha Information explains what happened and supports predictive hypotheses. Contextual Information explains how Alpha Information should be interpreted, conditioned, compared, decomposed, or attributed. Governance Information explains why scientific conclusions are trustworthy by enforcing authority, identity, lineage, PIT semantics, provenance, reproducibility, auditability, and artifact discipline.

Context is explanatory or conditioning before it is predictive. Common-versus-idiosyncratic decomposition is an interpretive outcome produced by combining alpha evidence with valid context, not a standalone raw signal. Evidence maturity is distinct from information role, and both are distinct from readiness for measurement, formulas, implementation, validation, production, or ML. Negative evidence is preserved as scientific knowledge. Module boundaries should remain minimal, falsifiable, and fail-closed.

## 14. Required Terminology Updates

Recommended bounded documentation updates:

| Update | Scope | Priority |
|---|---|---|
| Add an "Information Role" glossary entry using Alpha / Contextual / Governance / Negative / Diagnostic / Explanatory roles. | Future Phase 5 docs or a glossary note. | High |
| Add "Market Context" as explicit sibling to Economic Context and Macroeconomic Context. | Future context/harmonization docs. | Medium |
| Treat `COMMON_IDIOSYNCRATIC_DECOMPOSITION_INFORMATION` as inventory shorthand and prefer "decomposition outcome" in prose. | Future docs; no retroactive rewrite required. | Medium |
| Use "external information" for source-origin and authority questions; use "contextual information" for scientific role. | Future docs. | High |
| Separate role, maturity, and readiness headings in future readiness documents. | Future measurement/formula readiness review. | High |
| Avoid "context alpha" unless predictive incrementality has been demonstrated. | Future hypothesis/formula docs. | High |

No existing Phase 5 conclusion requires correction.

## 15. Readiness Implications

Harmonization improves later lifecycle steps without authorizing them.

| Future lifecycle area | Benefit of harmonization | Still not authorized |
|---|---|---|
| Measurement specification | Clarifies what must be measured: Alpha anchor, Context comparator, Governance gates, decomposition outcome. | No measurements defined here. |
| Formula design | Prevents context, governance, and decomposition from becoming accidental formula ingredients. | No formulas defined. |
| Implementation | Clarifies interfaces needed later: authority, identity, context, artifact lineage. | No code or architecture changes. |
| Validation | Clarifies what must be validated: predictive incrementality versus explanatory value versus governance correctness. | No validation run or design. |
| ML readiness | Reinforces why ML remains deferred until role, maturity, authority, and diversity are stronger. | No ML introduced. |

The repository is now conceptually ready for a bounded readiness review, not for formula implementation.

## 16. Recommended Next Lifecycle Step

Recommended next Project Underdog lifecycle step:

`Phase 5 Bounded Formula And Implementation Readiness Review v1`

Reason:

The harmonization review finds a coherent Phase 5 scientific philosophy with only minor terminology updates. The first-module boundary is defined, ML remains deferred, and no further conceptual dependency blocks a bounded readiness review. The next step should determine whether Project Underdog can proceed to a source-independent measurement specification or whether authority, identity, context, and governance gaps still block formula and implementation readiness.

This next step must not define formulas, implement code, create candidates, create registries, generate panels, construct peer groups, run IC, run validation, change governance, modify production, or introduce ML.

## Conclusion

Final classification: `PHASE5_SCIENTIFIC_FRAMEWORK_HARMONIZED_WITH_MINOR_TERMINOLOGY_UPDATES`

The current Phase 5 repository reflects one coherent scientific philosophy. It consistently distinguishes Alpha Information, Contextual Information, and Governance Information; separates information role from evidence maturity; separates evidence maturity from implementation readiness; treats context as explanatory or conditioning before predictive; preserves explanatory value even without predictive incrementality; preserves negative evidence; and keeps module boundaries scientifically minimal.

Minor terminology updates are recommended, especially around common-versus-idiosyncratic decomposition and external-versus-contextual wording. No scientific conclusions are changed.

## Searches And Lightweight Verification

Repository searches and checks used:

- `rg -n "Final classification|Alpha Information|Contextual Information|Governance Information|COMMON_IDIOSYNCRATIC|common-versus-idiosyncratic|external information|contextual information|economic context|market context|macroeconomic|macro context|information role|evidence maturity|implementation readiness|formula readiness|measurement specification|scientific philosophy|terminology|harmonization" docs/research_notes/project_underdog_phase5_*.md docs/research_notes/project_underdog_strategic_program_reassessment_v1.md docs/research_notes/project_underdog_master_status_recap_2026-06-17.md`
- `rg -n "Platform v2|hypothesis-first|orthogonality|falsifi|frozen horizon|bounded refinement|candidate discipline|negative evidence|validation separation|registry|artifact lineage|provenance|reproducibility|auditability|source authority|PIT semantics|identity|lineage" docs/research_notes/project_underdog_platform_v2_scientific_research_standard_v1.md docs/research_notes/project_underdog_standard_research_module_lifecycle_and_governance_standard_v1.md docs/research_notes/*validation* docs/research_notes/*registry* docs/research_notes/*lineage* docs/research_notes/*source* docs/research_notes/*pit*`
- `rg -n "hostile/stress|stress repair|participation repair|liquidity repair|volatility compression|VoV|persistence|rank stability|transition state|Non-Hostile Leadership|Event Clustering|Dispersion Path|PARK|parked|retired|negative evidence|validated|conditional|diagnostic-only|ML remains deferred|ML_NOT" docs/research_notes/project_underdog_master_status_recap_2026-06-17.md docs/research_notes/project_underdog_strategic_program_reassessment_v1.md docs/research_notes/project_underdog_phase5_integrated_scientific_information_inventory_v1.md docs/research_notes/project_underdog_phase5_ml_readiness_science_v1.md docs/research_notes/project_underdog_phase5_first_module_scientific_boundary_definition_v1.md`
- Direct review of Phase 5 WS1-WS9, first-module boundary definition, strategic reassessment, Phase 5 program and roadmap, integrated inventory, ML readiness, Platform v2 governance, master recap, validation methodology, candidate lifecycle, bounded refinement, frozen-horizon discipline, contamination and orthogonality notes, falsification and negative-evidence notes, reproducibility and artifact-lineage materials, source/PIT authority notes, and identity/lineage materials.

Boundary verification:

- No formulas, measurements, thresholds, regressions, residualization procedures, candidates, registries, panels, peer groups, implementation code, validation, production changes, governance changes, architecture changes, survivor-status changes, or ML were created or changed.
