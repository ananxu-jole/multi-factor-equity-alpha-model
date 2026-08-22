# Project Underdog - First Module Synthetic Fixture And Acceptance-Test Specification v1

Date: 2026-07-17

## 1. Executive Classification

Final classification: `SYNTHETIC_FIXTURE_AND_ACCEPTANCE_TEST_SPECIFICATION_DEFINED`

This note defines the source-independent synthetic fixture and acceptance-test specification for the first Project Underdog Phase 5 module:

`Common-Versus-Idiosyncratic Post-Stress Repair Decomposition`

This classification refers only to specification readiness. It does not authorize implementation, software architecture, APIs, schemas, source access, market-data retrieval, dataset construction, peer construction, parameter estimation, formula optimization, discovery, validation, candidates, registries, panels, IC, production artifacts, governance changes, survivor-status changes, or ML.

Repository basis:

- `docs/research_notes/project_underdog_phase5_first_module_scientific_boundary_definition_v1.md`: first-module boundary is common-versus-idiosyncratic post-stress repair decomposition.
- `docs/research_notes/project_underdog_first_module_source_independent_measurement_specification_v1.md`: observable concepts and measurement boundaries are defined.
- `docs/research_notes/project_underdog_first_module_formula_specification_v1.md`: symbol registry, temporal ordering, preferred decomposition formula, unresolved-state logic, and fixture/acceptance-test requirements are defined.
- `docs/research_notes/project_underdog_phase5_scientific_consistency_and_terminology_harmonization_review_v1.md`: Alpha Information, Contextual Information, Governance Information, maturity, readiness, and decomposition terminology are harmonized.
- `docs/research_notes/project_underdog_phase5_bounded_formula_and_implementation_readiness_review_v1.md`: lifecycle sequencing requires source-independent specification before implementation planning.
- Phase 5 WS1-WS9: authority, PIT identity and lineage, economic context, peer-relative hypothesis science, contamination, falsification, existing-family reinterpretation, integrated inventory, and ML-readiness constraints remain authoritative.
- `docs/research_notes/project_underdog_phase5_external_information_contamination_and_orthogonality_science_v1.md`: future behavior must expose own-feature, market-state, peer-definition, temporal, identity, survivorship, source, and interpretation contamination.
- `docs/research_notes/project_underdog_phase5_negative_evidence_and_falsification_science_v1.md`: future tests must preserve null, redundant, contaminated, and unresolved outcomes as scientific evidence.
- Platform v2 and lifecycle governance preserve hypothesis-first discipline, frozen horizons, bounded refinement, reproducibility, artifact lineage, validation separation, and anti-resurrection discipline.

## 2. Purpose Of Synthetic Fixtures

Synthetic fixtures exist to express the scientific behaviors every future implementation must satisfy before it may process real market data.

They are not real data. They are small conceptual worlds designed to make expected formula behavior unambiguous.

Distinctions:

| Concept | Meaning | Status here |
|---|---|---|
| Synthetic fixtures | Conceptual cases with controlled scientific conditions and expected behavior. | Defined here. |
| Implementation tests | Executable checks against code. | Not defined. |
| Empirical validation | Frozen-horizon evidence on real historical data. | Not performed. |
| IC evaluation | Cross-sectional predictive discovery or evaluation. | Not performed. |
| Production monitoring | Operational surveillance after production deployment. | Not relevant. |

Synthetic fixtures verify mathematical correctness, temporal correctness, conceptual correctness, traceability, fail-closed behavior, and implementation independence. They do not verify predictive performance.

## 3. Fixture Design Principles

Fixture principles:

| Principle | Requirement |
|---|---|
| Minimal sufficient scenarios | Each fixture isolates one scientific behavior unless an interaction is explicitly being tested. |
| One scientific purpose per fixture | The expected outcome must be traceable to a specific formula component or governance assumption. |
| Implementation independence | Fixture meaning must be identical across language, platform, source, or storage design. |
| Deterministic expected behavior | The expected scientific status must be knowable from the fixture setup. |
| No source dependence | No fixture uses vendor fields, proprietary data, real securities, or real classifications. |
| Bounded scope | Fixtures cover repair decomposition only, not stabilization, asymmetry, VoV, rank, transition, macro, event, portfolio, or ML mechanisms. |
| Reproducibility | Fixture inputs and expected outcomes must be preservable as scientific artifacts. |
| Traceability | Every fixture must map to a formula component, measurement concept, boundary rule, information role, and scientific claim. |
| Fail-closed discipline | Invalid authority, identity, context, timing, coverage, or observability must produce unresolved behavior. |
| Contamination visibility | Fixtures must reveal when common repair could be market, own-feature, peer-definition, or timing contamination. |

## 4. Canonical Synthetic Fixtures

The canonical fixture set contains 15 conceptual fixtures.

| Fixture | Scientific objective | Conceptual inputs | Conceptual expected behavior | Expected decomposition status | Acceptance conditions | Fail conditions |
|---|---|---|---|---|---|---|
| F1 Common repair | Verify peer-common decomposition. | \(S_i(t)\) eligible; \(R_i(t)\) and valid peer repairs align; \(C_i(t)\) explains target repair. | \(D_i(t)\) is not material under predeclared qualitative relation. | Predominantly common. | \(R_i(t)=C_i(t)+D_i(t)\); \(Z_i(t)\) common; comparator remains contextual. | Status becomes idiosyncratic, mixed without reason, or alpha claim. |
| F2 Idiosyncratic repair | Verify target-specific repair. | \(S_i(t)\) eligible; \(R_i(t)\) material; peer repair immaterial or directionally insufficient. | \(D_i(t)\) carries the repair interpretation. | Predominantly idiosyncratic. | Direct contrast identifies target-specific component; no peer optimization. | Peer-common component forced to explain target repair. |
| F3 Mixed repair | Verify common plus target-specific behavior. | Target and peers both repair, but target repair differs materially from peer-common repair. | Both \(C_i(t)\) and \(D_i(t)\) are scientifically meaningful. | Mixed. | Formula preserves both components. | One component is discarded or silently thresholded. |
| F4 Unresolved repair | Verify ambiguity preservation. | Valid inputs exist, but qualitative materiality relations cannot distinguish common, idiosyncratic, or mixed. | Interpretation is not forced. | Unresolved. | \(Z_i(t)\) unresolved. | Implementation forces common/idiosyncratic classification. |
| F5 Comparator unavailable | Verify comparator dependency. | Own repair observable; \(P_i(t)\) unavailable or not accepted. | Peer-common and idiosyncratic components unavailable. | Unresolved. | \(C_i(t)\), \(D_i(t)\), \(Z_i(t)\) unresolved. | Own repair is treated as idiosyncratic by default. |
| F6 Invalid identity | Verify identity gate. | Target or comparator identity is invalid or ambiguous. | Decomposition cannot be trusted. | Unresolved. | Fail closed before decomposition. | Ticker continuity or current identity is silently accepted. |
| F7 PIT violation | Verify no future membership. | Comparator membership uses future or current-state evidence historically. | Context is invalid. | Unresolved. | Fail closed and flag PIT violation. | Future-known peer set produces decomposition. |
| F8 Timing violation | Verify temporal ordering. | \(H_t\) precedes or overlaps improperly with \(B_t\), or \(F_t\) enters explanatory inputs. | Formula relationship invalid. | Unresolved. | Timing error blocks use. | Formula proceeds despite ordering failure. |
| F9 Market-wide repair | Verify market contamination visibility. | Target and peers repair while \(M(t)\) indicates broad market recovery. | Decomposition may be common, but market-contamination risk must be visible. | Predominantly common or unresolved if market confounding blocks interpretation. | Market context remains control; no third alpha term. | Market repair mislabeled as peer-specific alpha. |
| F10 Target-only repair | Verify own-feature contamination boundary. | Target repairs strongly; comparators do not; market does not. | Direct contrast shows target-specific repair if all validity gates pass. | Predominantly idiosyncratic. | Outcome remains interpretive, not validated alpha. | Own repair alone is promoted as alpha. |
| F11 Peer-only repair | Verify target shortfall behavior. | Valid peers repair; target does not repair. | \(C_i(t)\) is material and \(D_i(t)\) indicates target shortfall. | Mixed, idiosyncratic weakness, or unresolved depending on predeclared qualitative relation. | No positive repair claim for target. | Peer repair is assigned to target. |
| F12 Partial repair | Verify smaller target/common divergence. | Target and peer-common repair align directionally but only partially. | Formula preserves partial common and partial idiosyncratic meaning. | Mixed. | Both components remain visible. | Partial divergence is rounded away without declared relation. |
| F13 Missing observations | Verify missingness handling. | Target or comparator observations missing. | Missingness either governed or blocks interpretation. | Unresolved unless governed comparator exclusion leaves valid sufficient context. | Governed exclusion only; no imputation. | Missing values are filled or ignored silently. |
| F14 Ambiguous decomposition | Verify interpretive uncertainty. | \(R_i(t)\), \(C_i(t)\), and \(D_i(t)\) exist but relations conflict or are sign-unstable. | Decomposition not forced. | Unresolved. | Ambiguity preserved. | Status chosen through hidden rule. |
| F15 Unstable formulation input | Verify extreme or scale-unstable input behavior. | Repair observations are extreme, sign-changing, or unstable for admissible scaling. | Preferred direct contrast proceeds only if valid and interpretable; otherwise unresolved. | Mixed, idiosyncratic, common, or unresolved as governed by qualitative relation. | No hidden clipping, bounds, or optimization. | Undeclared stabilization, normalization, or bounding enters the result. |

No real data is used.

## 5. Temporal Integrity Fixtures

| Fixture | Temporal property verified | Conceptual setup | Expected behavior |
|---|---|---|---|
| T1 Stress precedes repair | \(B_t \prec H_t\). | Stress-reference relationship is complete before repair observation. | Formula may proceed if all other gates pass. |
| T2 Repair precedes future evaluation | \(H_t \preceq t \prec F_t\). | Future evaluation period is later than decomposition inputs. | \(F_t\) is not usable in \(R_i(t)\), \(C_i(t)\), \(D_i(t)\), or \(Z_i(t)\). |
| T3 No future leakage | Future comparator membership or future repair outcome appears in explanatory inputs. | Any future-known evidence is introduced before \(t\). | Fail closed. |
| T4 Comparator alignment | Target and comparator repair share aligned \(B_t\) and \(H_t\) relationships. | Comparator observations are historically aligned. | Peer-common repair may be interpreted. |
| T5 PIT validity | Comparator context is known and valid as of the historical time. | PIT-valid membership is available. | Formula may proceed if other gates pass. |
| T6 Observation ordering | Identity, context, stress, own repair, comparator repair, and decomposition are ordered correctly. | All prerequisite relationships are available in order. | \(Z_i(t)\) may be assigned. |

Temporal fixture failure always produces unresolved status or fail-closed behavior.

## 6. Comparator Fixtures

| Fixture | Comparator behavior verified | Conceptual setup | Expected behavior |
|---|---|---|---|
| C1 Contextual role | Comparator repairs explain common repair only. | Valid peers repair with target. | \(C_i(t)\) is contextual; not alpha. |
| C2 Exclusion handling | One comparator invalid. | Invalid comparator is identified before aggregation. | Exclude only if missingness and validity rules allow; otherwise unresolved. |
| C3 Comparator insufficiency | Too few or no valid comparators after gates. | \(P_i^{*}(t)\) unavailable or insufficient. | \(C_i(t)\), \(D_i(t)\), \(Z_i(t)\) unresolved. |
| C4 Invalid membership | Membership uses current labels, future records, or unsupported lineage. | Comparator set not PIT-safe. | Fail closed. |
| C5 Comparator ambiguity | Two plausible comparator contexts conflict. | Source-role or context ambiguity affects interpretation. | Unresolved unless future authority resolves conflict. |
| C6 Comparator instability | Comparator set changes for unsupported reasons within the observation relation. | Unexplained membership instability. | Unresolved or contamination flag, not forced decomposition. |

No real peers are constructed.

## 7. Decomposition Fixtures

| Fixture | Formula relation verified | Conceptual setup | Expected status |
|---|---|---|---|
| D1 Predominantly common | \(R_i(t)\) is explained primarily by \(C_i(t)\). | Target and peer-common repair are directionally aligned; \(D_i(t)\) is not material. | Predominantly common. |
| D2 Predominantly idiosyncratic | \(R_i(t)\) is not explained by \(C_i(t)\). | Target repair is material; peer-common repair is not. | Predominantly idiosyncratic. |
| D3 Mixed | \(C_i(t)\) and \(D_i(t)\) both matter. | Target repair includes common and target-specific components. | Mixed. |
| D4 Unresolved | Required relationship is ambiguous or invalid. | Materiality, sign, timing, or validity is unresolved. | Unresolved. |

These fixtures do not define empirical thresholds. They verify that a future implementation can preserve qualitative decomposition statuses without inventing hidden numeric cutoffs.

## 8. Confounder Fixtures

| Confounder fixture | Scientific risk | Expected behavior |
|---|---|---|
| X1 Stabilization | Volatility stabilization is silently treated as repair. | Fixture must fail if stabilization enters \(R_i(t)\), \(C_i(t)\), or \(D_i(t)\) without approved repair-only definition. |
| X2 Participation | Participation recovery is hidden inside repair. | Fixture must show no participation input is required for v1 decomposition. |
| X3 Liquidity | Liquidity recovery drives apparent repair. | Fixture must flag liquidity as confounder/control, not formula input. |
| X4 VoV | VoV normalization is imported as repair. | Fixture must reject hidden VoV dependence. |
| X5 Transition timing | Early/late transition is relabeled as repair decomposition. | Fixture must preserve temporal order but not create transition-order mechanism. |
| X6 Asymmetry | Positive/negative asymmetry is added to status logic. | Fixture must reject asymmetry-specific interpretation in v1. |
| X7 Macro conditioning | Macro state enters comparator interpretation. | Fixture must keep macro deferred and outside v1 formula. |

Confounder fixtures ensure the preferred formula remains the smallest repair-decomposition design.

## 9. Fail-Closed Fixtures

| Fail-closed case | Required outcome |
|---|---|
| Invalid identity | Unresolved before decomposition. |
| Missing comparator context | \(C_i(t)\), \(D_i(t)\), and \(Z_i(t)\) unresolved. |
| Timing inconsistency | Unresolved. |
| Missing target observations | Unresolved. |
| Missing comparator observations | Governed exclusion or unresolved; no silent imputation. |
| Incompatible observation windows | Unresolved. |
| Ambiguous interpretation | Unresolved. |
| Undefined inputs | Unresolved. |
| Unaccepted source-role evidence | Diagnostic-only or unresolved. |
| Unresolved delisting or terminal state | Unresolved. |
| Current-state metadata used historically | Fail closed. |
| Comparator-source conflict | Unresolved unless future authority resolves it. |

The fixture specification favors unresolved status over forced values whenever scientific assumptions fail.

## 10. Traceability Matrix

| Fixture group | Formula component | Measurement concept | Scientific boundary | Information role | Scientific claim |
|---|---|---|---|---|---|
| F1, D1 | \(R_i(t)\), \(C_i(t)\), \(D_i(t)\), \(Z_i(t)\) | Own repair, peer-common repair, decomposition outcome | Common repair interpretation | Alpha Observation, Contextual Observation, Interpretive Outcome | Valid peers may explain observed repair as common. |
| F2, F10, D2 | \(R_i(t)\), \(C_i(t)\), \(D_i(t)\) | Security-specific repair | Idiosyncratic repair interpretation | Alpha Observation and Interpretive Outcome | Target repair may remain security-specific after comparator contrast. |
| F3, F12, D3 | \(R_i(t)=C_i(t)+D_i(t)\) | Mixed decomposition | Common plus idiosyncratic interpretation | Interpretive Outcome | Repair can contain both common and target-specific components. |
| F4, F14, D4 | \(Z_i(t)\) | Unresolved decomposition | No forced interpretation | Governance Information and Interpretive Outcome | Ambiguity must be preserved. |
| F5, C1-C6 | \(P_i(t)\), \(P_i^{*}(t)\), \(C_i(t)\) | Comparator context, peer-common repair | Comparator is contextual | Contextual Information | Comparator role must not become hidden alpha or peer optimization. |
| F6, F7, F13, fail-closed group | \(V_i(t)\), \(V_j(t)\) | Validity and observability | Governance gates | Governance Information | Authority, identity, context, coverage, and timing control use. |
| F8, T1-T6 | \(B_t\), \(H_t\), \(t\), \(F_t\) | Observation timing | Temporal ordering | Governance Information | Decomposition cannot use future information. |
| F9 | \(M(t)\) | Market context | Market context as control | Contextual Information | Market-wide repair must not be mislabeled as peer-specific alpha. |
| F11 | \(C_i(t)\), \(D_i(t)\), \(Z_i(t)\) | Peer-only repair, target shortfall | Target does not inherit peer repair | Contextual Observation and Interpretive Outcome | Peer repair can reveal target non-participation without creating target repair. |
| F15 | \(R_i(t)\), \(C_i(t)\), \(D_i(t)\), \(Z_i(t)\) | Unstable input handling | No hidden transformations | Governance and Interpretive Outcome | Extreme or unstable inputs must not trigger undeclared normalization. |
| X1-X7 | Exclusion boundaries | Confounder controls | Stabilization/asymmetry/macro and other exclusions | Contextual/Governance Information | First module remains bounded to repair decomposition. |

No fixture lacks a traceable scientific purpose.

## 11. Acceptance-Test Categories

Acceptance-test categories for a future implementation-independent test specification:

| Category | Required scientific expectation |
|---|---|
| Algebraic consistency | Valid cases must preserve \(R_i(t)=C_i(t)+D_i(t)\). |
| Temporal consistency | \(B_t \prec H_t \preceq t \prec F_t\) and no future information enters inputs. |
| Decomposition consistency | Common, idiosyncratic, mixed, and unresolved states follow predeclared qualitative relations. |
| Comparator correctness | Comparator context remains PIT-valid, contextual, non-optimized, and source-independent. |
| Unresolved-state behavior | Invalid or ambiguous prerequisites produce unresolved status. |
| Traceability | Every fixture and future test maps to formula, measurement, boundary, role, and claim. |
| Reproducibility | Expected behavior is deterministic and artifact-preservable. |
| Implementation independence | Scientific outcomes are independent of programming language, storage, source representation, or architecture. |
| Fail-closed behavior | Authority, identity, context, timing, coverage, missingness, and source conflicts block use. |
| Contamination visibility | Own-feature, market, repair-family, peer-definition, temporal, identity, survivor, source, and interpretation contamination are surfaced. |

No executable tests are defined.

## 12. Acceptance Invariants

Every future implementation must satisfy these invariants:

- identical scientific interpretation for the same accepted conceptual fixture;
- identical temporal ordering expectations;
- identical unresolved behavior for failed prerequisites;
- identical decomposition logic: own repair, peer-common repair, direct idiosyncratic contrast, interpretive status;
- identical comparator role as contextual information;
- identical rejection of hidden stabilization, participation, liquidity, VoV, rank, transition, asymmetry, macro, event, portfolio, or ML mechanisms;
- identical traceability from test behavior to formula component and scientific claim;
- identical fail-closed behavior for authority, identity, context, PIT, timing, missingness, source conflict, and reproducibility failures;
- identical separation between fixture correctness and predictive validation;
- identical source independence across vendors, schemas, programming languages, and architectures.

## 13. Non-Goals

This note explicitly excludes:

- implementation benchmarks;
- runtime optimization;
- statistical power;
- prediction quality;
- IC;
- validation metrics;
- production monitoring;
- hyperparameter tuning;
- peer optimization;
- source-specific behavior;
- APIs;
- software architecture;
- database schemas;
- code;
- datasets;
- real market data;
- candidates;
- registries;
- panels;
- formula optimization;
- parameter estimation;
- governance changes;
- survivor-status changes;
- ML.

## 14. Coverage Assessment

Observable concept coverage:

| Observable concept | Covered by fixture(s) | Covered by acceptance category |
|---|---|---|
| Post-stress context | F4, F8, T1, T2 | Temporal consistency, unresolved-state behavior |
| Own-security repair | F1-F4, F10-F12, F13-F15 | Algebraic consistency, decomposition consistency |
| Peer-common repair | F1-F5, F11-F12, C1-C6 | Comparator correctness, decomposition consistency |
| Security-specific repair | F2, F3, F10-F12, D2-D3 | Algebraic consistency, decomposition consistency |
| Comparator context | F5, F7, C1-C6 | Comparator correctness, fail-closed behavior |
| Decomposition outcome | F1-F4, F14, D1-D4 | Decomposition consistency, unresolved-state behavior |
| Existing repair-family anchor | F1-F4, T1-T2 | Traceability, contamination visibility |
| Contextual controls | F9, X1-X7 | Contamination visibility, fail-closed behavior |

Formula component coverage:

| Formula component | Covered by fixture(s) | Covered by acceptance category |
|---|---|---|
| \(i\) | F6 | Fail-closed behavior |
| \(P_i(t)\), \(P_i^{*}(t)\) | F5, F7, C1-C6 | Comparator correctness |
| \(t\), \(B_t\), \(H_t\), \(F_t\) | F8, T1-T6 | Temporal consistency |
| \(S_i(t)\) | F4, T1 | Temporal consistency, unresolved-state behavior |
| \(X_i(B_t,H_t)\) | F13, F15 | Reproducibility, unresolved-state behavior |
| \(R_i(t)\) | F1-F4, F10-F15 | Algebraic consistency |
| \(R_j(t)\) | F1, F3, F5, F11-F13, C1-C6 | Comparator correctness |
| \(C_i(t)\) | F1-F5, F11-F12 | Algebraic consistency, comparator correctness |
| \(D_i(t)\) | F2-F4, F10-F12 | Algebraic consistency, decomposition consistency |
| \(M(t)\) | F9 | Contamination visibility |
| \(Z_i(t)\) | F1-F4, F14, D1-D4 | Decomposition consistency |
| \(V_i(t)\), \(V_j(t)\) | F6, F7, F13, fail-closed group | Fail-closed behavior |

Coverage conclusion:

No conceptual coverage gaps remain for the pre-implementation scientific specification. The remaining gaps are lifecycle gaps outside this note: implementation architecture, executable tests, source authority, identity evidence, context evidence, real peer construction, discovery, validation, production, and ML remain unauthorized.

## 15. Readiness Conclusion

Project Underdog now possesses a complete pre-implementation scientific specification for the first module.

Repository support:

- the scientific boundary defines the smallest module;
- the measurement specification defines what must be observed;
- the formula specification defines symbols, temporal ordering, decomposition, preferred formulation, unresolved states, synthetic fixture needs, and acceptance-test categories;
- this note defines conceptual fixtures, fixture groups, acceptance categories, invariants, traceability, and coverage;
- contamination, falsification, governance, reproducibility, frozen-horizon, and lifecycle constraints are preserved.

This readiness conclusion does not authorize implementation. It supports only beginning source-independent implementation architecture planning in a separate lifecycle note.

Final classification restated: `SYNTHETIC_FIXTURE_AND_ACCEPTANCE_TEST_SPECIFICATION_DEFINED`

## 16. Recommended Next Lifecycle Step

Recommended exactly one next lifecycle step:

`Project Underdog - First Module Implementation Architecture Specification v1`

This next step should define source-independent implementation architecture planning only. It must not write code, define production APIs, bind to sources, construct datasets, retrieve market data, construct real peers, perform discovery, perform validation, optimize formulas, estimate parameters, create candidates, create registries, create panels, compute IC, modify governance, modify scientific conclusions, create production artifacts, alter survivor status, or introduce ML.
