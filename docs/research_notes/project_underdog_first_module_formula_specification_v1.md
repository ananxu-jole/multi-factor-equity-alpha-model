# Project Underdog - First Module Formula Specification v1

Date: 2026-07-17

## 1. Executive Classification

Final classification: `FIRST_MODULE_FORMULA_SPECIFICATION_DEFINED`

This note defines the first bounded, source-independent formula specification for Project Underdog's first Phase 5 module:

`Common-Versus-Idiosyncratic Post-Stress Repair Decomposition`

This classification refers only to formula-specification readiness. It does not authorize implementation, source access, data retrieval, peer construction, candidate registration, panel generation, IC discovery, validation, production, governance changes, survivor-status changes, or ML.

Repository basis:

- `docs/research_notes/project_underdog_phase5_first_module_scientific_boundary_definition_v1.md`: first module is narrowed to common-versus-idiosyncratic post-stress repair decomposition; stabilization is a confounder; asymmetry is a later bounded extension; macroeconomic conditioning is deferred.
- `docs/research_notes/project_underdog_phase5_scientific_consistency_and_terminology_harmonization_review_v1.md`: Alpha Information, Contextual Information, Governance Information, information role, evidence maturity, readiness, and decomposition-as-interpretive-outcome language are harmonized.
- `docs/research_notes/project_underdog_phase5_bounded_formula_and_implementation_readiness_review_v1.md`: formula work follows measurement science and remains source-independent until authority and identity evidence are accepted.
- `docs/research_notes/project_underdog_first_module_source_independent_measurement_specification_v1.md`: measurement specification is defined and recommends this formula-specification step.
- Phase 5 WS1-WS9 define authority, identity, economic context, peer-relative hypotheses, contamination, falsification, reinterpretation, inventory, and ML-readiness constraints.
- `docs/research_notes/project_underdog_phase5_external_information_contamination_and_orthogonality_science_v1.md`: peer-relative repair must survive own-feature, market-state, repair-family, participation, volatility, VoV, persistence, rank, transition, peer-definition, temporal, identity, survivor, and source contamination controls.
- `docs/research_notes/project_underdog_phase5_negative_evidence_and_falsification_science_v1.md`: the selected module conceptually survives with open gaps, and future negative evidence must be preserved.
- `docs/research_notes/project_underdog_phase5_existing_family_reinterpretation_science_v1.md`: the leading interpretation is common-versus-idiosyncratic decomposition, with existing repair-family refinement as the strongest alternative.
- Platform v2 and lifecycle governance require hypothesis-first discipline, frozen horizons, bounded refinement, traceability, reproducibility, validation separation, candidate discipline, and anti-resurrection discipline.

Preserved conclusions:

- Contextual information is explanatory or conditioning before predictive.
- The comparator is contextual, not a hidden alpha signal.
- Common-versus-idiosyncratic decomposition is an interpretive outcome.
- No peer-relative empirical evidence has yet been established.
- No implementation or validation is authorized.

## 2. Formula-Specification Purpose

Formula science translates an approved measurement specification into source-independent mathematical relationships while preserving the scientific boundary.

Lifecycle distinctions:

| Lifecycle layer | Meaning | Status here |
|---|---|---|
| Scientific hypothesis | The claim that valid peers may separate common repair from security-specific repair. | Preserved from the boundary note. |
| Observable concept | What must be observed: stress context, own repair, peer-common repair, decomposition outcome, controls. | Inherited from the measurement specification. |
| Measurement specification | Source-independent definition of what must be measured. | Already defined. |
| Formula specification | Mathematical representation of approved observations and relationships. | Defined in this note. |
| Implementation | Code, schemas, interfaces, data access, and execution behavior. | Not authorized. |
| Discovery | Empirical search, IC, panels, candidate evaluation, or threshold estimation. | Not authorized. |
| Validation | Frozen-horizon validation and survivor-status review. | Not authorized. |

The formula layer may define symbols, abstract intervals, admissible operations, derived quantities, and unresolved-state behavior. It must not bind the design to a vendor, database, source schema, programming language, real peer group, or empirical threshold.

## 3. Symbol And Notation Registry

Notation is source-independent. Symbols are scientific notation, not data-column names or code variables.

| Symbol | Scientific meaning | Information role | Temporal meaning | Observed or derived | Permitted use | Prohibited interpretation |
|---|---|---|---|---|---|---|
| \(i\) | Target security. | Governance-scoped research subject. | Valid only over its accepted identity interval. | Observed identity role after future authority acceptance. | Identify the target whose repair is interpreted. | Ticker, company, issuer, or economic-company identity by default. |
| \(P_i(t)\) | Valid comparator set for target \(i\) at observation time \(t\). | Contextual Information governed by authority and identity. | PIT-valid at \(t\). | Observed context role after future authority acceptance. | Define eligible economic comparators. | Real peer construction, optimized peer membership, current-state labels. |
| \(t\) | Observation time at which decomposition is interpreted. | Temporal governance. | After stress reference and repair observation relationships are established. | Formal time index. | Anchor PIT alignment. | Ingestion time, extraction time, or future outcome date unless separately defined. |
| \(B_t\) | Stress-reference period for \(i\) and eligible comparators. | Alpha/context anchor. | Ends before repair interpretation. | Formal bounded interval. | Provide the reference state for post-stress repair. | Empirically selected best window or future-informed stress label. |
| \(H_t\) | Repair-observation period. | Alpha/context observation interval. | Follows the stress-reference period and precedes any future evaluation. | Formal bounded interval. | Observe repair after stress. | Forecast period or validation horizon. |
| \(F_t\) | Future evaluation period. | Future predictive target context. | Strictly after explanatory observations. | Deferred formal interval. | Reserve room for later validation design. | Input to decomposition. |
| \(S_i(t)\) | Post-stress eligibility state for target \(i\). | Alpha/context anchor. | Knowable before repair interpretation. | Derived eligibility state from accepted stress evidence. | Gate whether decomposition is meaningful. | Retrospective inference from later recovery. |
| \(X_i(B_t,H_t)\) | Own-security repair observation basis. | Alpha Observation basis. | Uses only the stress-reference and repair-observation periods. | Observed approved input class. | Feed the own-repair function. | Source field, price-only assumption, or hidden liquidity/VoV input. |
| \(R_i(t)\) | Own-security repair. | Alpha Observation. | Interprets \(i\)'s repair over \(B_t\) and \(H_t\). | Derived from approved own observation basis. | Represent target repair after stress. | Validated alpha signal by itself. |
| \(R_j(t)\) | Comparator security repair for \(j \in P_i(t)\). | Contextual Observation. | Historically aligned with \(R_i(t)\). | Derived from each comparator's approved observation basis. | Feed peer-common repair. | Independent candidate, peer rank, or optimized peer score. |
| \(M(t)\) | Broad market-context control. | Contextual Information. | Aligned with \(B_t\), \(H_t\), and \(t\). | Observed or derived from existing accepted market-state evidence. | Identify market-wide repair or stress confounding. | Third alpha mechanism. |
| \(C_i(t)\) | Peer-common repair component. | Contextual derived quantity. | Aggregated from valid comparator repair observations aligned to \(t\). | Derived. | Represent common repair among valid comparators. | Alpha signal or optimized benchmark. |
| \(D_i(t)\) | Security-idiosyncratic repair component. | Interpretive derived quantity. | Same temporal relationship as \(R_i(t)\) and \(C_i(t)\). | Derived. | Represent target repair not described as peer-common repair. | Fitted residual, causal residual, or validated predictive signal. |
| \(Z_i(t)\) | Decomposition status. | Interpretive Outcome. | Assigned only after validity checks for the same observation relationship. | Derived qualitative status. | State common, idiosyncratic, mixed, or unresolved interpretation. | Candidate label, thresholded alpha label, production action. |
| \(V_i(t)\) | Validity or observability indicator. | Governance Information. | PIT-valid for the observation relationship. | Derived gate from authority, identity, context, timing, and coverage status. | Permit or block formula interpretation. | Data-quality afterthought or imputation trigger. |

## 4. Temporal Structure

Required ordering:

\[
B_t \prec H_t \preceq t \prec F_t
\]

where \(\prec\) means the earlier relationship must be complete before the later relationship is used for interpretation, and \(\preceq\) allows the observation time to coincide with the end of the repair-observation relationship.

Validity constraints:

\[
P_i(t),\ S_i(t),\ M(t),\ R_i(t),\ \{R_j(t): j \in P_i(t)\}
\]

must be knowable without using \(F_t\) or any information first available after the project-known relationship for \(t\).

The formula specification permits symbolic bounded intervals but selects no numeric horizon values. Future formula or fixture work may name bounded interval families only if they are frozen before empirical use and trace back to repository-authorized horizon discipline.

## 5. Post-Stress Context Formulation

Post-stress context is an eligibility and conditioning state, not a repair measurement.

Preferred formulation:

\[
S_i(t) \in \{\text{eligible},\ \text{not eligible},\ \text{unresolved}\}
\]

The decomposition is admissible only when:

\[
S_i(t)=\text{eligible}
\]

and all governance validity checks also pass.

Scientific requirements:

- \(S_i(t)\) must be established from stress evidence over \(B_t\), not inferred from later recovery over \(H_t\) or \(F_t\).
- \(S_i(t)\) gates interpretation; it is not combined with repair to manufacture a broader stress-repair score.
- If stress state is unresolved, decomposition status must be unresolved.
- If the security is not in a post-stress context, the first-module formula is not applicable.

Bounded alternatives:

- A binary eligible/not-eligible stress gate is simpler but cannot preserve unresolved evidence.
- A multi-state stress taxonomy may be useful later but risks expanding the first module into regime modeling.

The preferred v1 formulation is the three-state gate because it is minimal while preserving fail-closed behavior.

## 6. Own-Security Repair Formulation

Own-security repair is the target security's signed movement from the stress-reference relationship toward a repaired relationship over the repair-observation period.

General repair operator:

\[
R_i(t)=\mathcal{R}\left(X_i(B_t,H_t)\right)
\]

where \(\mathcal{R}\) is a future source-independent repair operator applied only to approved own-security observation inputs.

Required properties:

- Reference state: \(B_t\) supplies the stress-reference relationship.
- Observation interval: \(H_t\) supplies the repair-observation relationship.
- Repair direction: larger signed values must represent stronger repair under the selected repair operator, and weaker values must represent weaker repair or deterioration.
- Required comparison: \(R_i(t)\) must compare the repair-observation relationship to the stress-reference relationship.
- Non-observable cases: missing target observation, invalid target identity, unresolved stress, or incompatible timing must produce unresolved status.

Admissible scaling or normalization classes for future work:

- additive movement from stress reference;
- proportional movement from stress reference;
- bounded repair index;
- direction-preserving monotone transformation of an approved repair observation.

The formula does not assume that a single price return is sufficient. It also does not introduce hidden participation, liquidity, stabilization, VoV, rank, or transition mechanisms.

## 7. Comparator-Context Formulation

Comparator context supplies valid economic comparators. It does not construct them here.

Eligibility gate:

\[
P_i(t)=\{j:\ j \text{ is an accepted valid economic comparator for } i \text{ at } t\}
\]

The set is usable only if:

- comparator membership is PIT-valid;
- target and comparator identities are valid;
- comparator histories overlap the required \(B_t\) and \(H_t\) relationships;
- delistings and terminal states are governed;
- source authority exists for the relevant context roles;
- missingness is governed;
- no future-known membership or current-state classification is used historically.

Comparator observation input:

\[
\mathcal{P}_i(t)=\{R_j(t):j \in P_i(t),\ V_j(t)=1\}
\]

where \(V_j(t)=1\) means the comparator observation passes future authority, identity, timing, coverage, and reproducibility gates.

Fail-closed behavior:

If \(P_i(t)\) is invalid, empty, insufficiently observable, temporally misaligned, or source-conflicted in a way that affects interpretation, then \(C_i(t)\), \(D_i(t)\), and \(Z_i(t)\) are unresolved.

No peer groups are constructed. No comparator membership is optimized.

## 8. Peer-Common Repair Formulation

Peer-common repair represents common repair among valid economic comparators.

Defensible aggregation families:

| Aggregation family | Scientific advantage | Scientific risk |
|---|---|---|
| Equal aggregation | Minimal, transparent, no hidden weighting model. | Sensitive to invalid peers, duplicate share classes, and outliers. |
| Robust central tendency | Reduces outlier influence. | Adds a robustness design choice that can become hidden optimization. |
| Bounded weighted aggregation | Can handle size or relevance if scientifically justified. | Requires weight authority and may import size, liquidity, or taxonomy assumptions. |

Preferred first formulation:

\[
C_i(t)=\frac{1}{|P_i^{*}(t)|}\sum_{j\in P_i^{*}(t)} R_j(t)
\]

where \(P_i^{*}(t)\) is the subset of valid, observable comparators after all future governance gates pass.

Reason for selection:

Equal aggregation is the smallest scientifically defensible first formulation because it makes the comparator role explicit, avoids hidden weighting, avoids optimization, and keeps peer-common repair contextual rather than predictive. Its weaknesses should be addressed through synthetic fixtures and acceptance tests before implementation, not by adding unapproved weighting complexity.

No weights are estimated. No taxonomy or source-specific membership is selected.

## 9. Security-Idiosyncratic Repair Formulation

Security-idiosyncratic repair is the part of own repair not represented by peer-common repair.

Preferred first formulation:

\[
D_i(t)=R_i(t)-C_i(t)
\]

This is a direct contrast, not a fitted statistical residual.

Alternatives considered:

| Structure | Scientific advantage | Reason not preferred for v1 |
|---|---|---|
| Direct difference | Transparent and aligned with decomposition. | Preferred. |
| Scaled difference | Helps compare across differing repair magnitudes. | Requires scale choice and unstable-denominator rules. |
| Ratio | Intuitive for relative magnitude. | Can fail under small or sign-changing comparator values. |
| Bounded contrast | Controls extremes. | Requires additional transformation and bounds. |
| Residual-style interpretation | Familiar decomposition language. | Risks being mistaken for regression residualization. |

The preferred direct contrast is minimal and interpretable. If future work uses residual language, it must refer only to conceptual remainder after comparator contrast, never to a fitted model residual.

## 10. Common-Versus-Idiosyncratic Decomposition

The mathematical decomposition is:

\[
R_i(t)=C_i(t)+D_i(t)
\]

with:

\[
D_i(t)=R_i(t)-C_i(t)
\]

Interpretive status:

\[
Z_i(t)\in\{\text{predominantly common},\ \text{predominantly idiosyncratic},\ \text{mixed},\ \text{unresolved}\}
\]

Qualitative decision regions:

| Status | Symbolic relation | Scientific interpretation |
|---|---|---|
| Predominantly common | \(R_i(t)\) is directionally aligned with \(C_i(t)\), and \(D_i(t)\) is immaterial under a predeclared materiality relation. | Target repair is mostly common comparator repair. |
| Predominantly idiosyncratic | \(R_i(t)\) is material while \(C_i(t)\) is immaterial or directionally insufficient under a predeclared materiality relation. | Target repair appears security-specific. |
| Mixed | Both \(C_i(t)\) and \(D_i(t)\) are material and directionally coherent. | Target repair contains common and security-specific components. |
| Unresolved | Any required validity, observability, materiality, timing, or comparability condition is not satisfied. | Decomposition cannot be interpreted scientifically. |

No empirical classification thresholds are selected. Materiality relations must be frozen in a later lifecycle step before empirical use. \(Z_i(t)\) is an interpretive outcome and is not automatically an alpha signal.

## 11. Market-Context Control

Broad market context functions as a confounder control and bounded sensitivity input.

Market context symbol:

\[
M(t)
\]

Required current role:

- identify whether apparent peer-common repair may be broad market recovery;
- prevent market-wide stress repair from being mislabeled as economic-peer repair;
- preserve continuity with existing OHLCV-derived market state, stress state, participation state, volatility state, liquidity state, and transition-state evidence.

Deferred role:

- future formula work may define market-context sensitivity comparisons, but this note does not create a third decomposition component.

Prohibited role:

\[
R_i(t)\neq C_i(t)+M(t)+D_i(t)
\]

for this v1 first formulation. Market context is not silently inserted as a third alpha mechanism.

## 12. Existing Repair-Family Anchor

The formula remains anchored to existing hostile/stress-repair evidence through \(S_i(t)\), \(B_t\), \(H_t\), and \(R_i(t)\).

Inherited:

- repair after adverse or hostile states is the alpha-information anchor;
- repair must be interpreted under predeclared stress context;
- existing OHLCV repair evidence remains the starting scientific basis.

Reinterpreted:

- peer context may show that observed repair is common recovery rather than security-specific repair;
- existing repair may become better understood as common, idiosyncratic, mixed, or unresolved.

Not changed:

- existing survivor status;
- existing validation status;
- existing candidate status;
- existing formula lineage;
- existing production status.

Requires later incrementality testing:

- whether \(D_i(t)\), \(C_i(t)\), or \(Z_i(t)\) adds predictive information beyond existing repair-family anchors;
- whether the module is an independent alpha candidate or only an existing-family refinement;
- whether market-state, participation, volatility, VoV, persistence, rank, or transition controls explain the decomposition.

## 13. Preferred First Formulation

Preferred source-independent first formulation:

1. Gate the observation:

\[
V_i(t)=1 \quad \text{only if authority, identity, context, timing, coverage, reproducibility, and } S_i(t)=\text{eligible} \text{ all pass}
\]

2. Define own repair:

\[
R_i(t)=\mathcal{R}\left(X_i(B_t,H_t)\right)
\]

3. Define valid comparator observations:

\[
\mathcal{P}_i(t)=\{R_j(t):j\in P_i(t),\ V_j(t)=1\}
\]

4. Define peer-common repair by equal aggregation:

\[
C_i(t)=\frac{1}{|P_i^{*}(t)|}\sum_{j\in P_i^{*}(t)}R_j(t)
\]

5. Define security-idiosyncratic repair by direct contrast:

\[
D_i(t)=R_i(t)-C_i(t)
\]

6. Define decomposition:

\[
R_i(t)=C_i(t)+D_i(t)
\]

7. Assign interpretive status:

\[
Z_i(t)\in\{\text{predominantly common},\ \text{predominantly idiosyncratic},\ \text{mixed},\ \text{unresolved}\}
\]

Unresolved-state logic:

If any required input, gate, comparator, timing relationship, or materiality relation is unavailable or invalid, \(Z_i(t)=\text{unresolved}\), and \(C_i(t)\) and \(D_i(t)\) must not be treated as research inputs.

Why this is the smallest defensible formulation:

- it uses one own-repair observation;
- it uses one contextual peer-common observation;
- it uses one direct decomposition relationship;
- it keeps market context as a control rather than a third mechanism;
- it excludes stabilization, asymmetry, participation, liquidity, VoV, rank, transition, macro, events, portfolios, and ML;
- it is falsifiable by showing the comparator adds no interpretation beyond own repair and existing controls.

## 14. Bounded Alternative Formulations

| Alternative | Scientific advantage | Scientific risk | Contamination risk | Interpretability risk | Implementation burden | Reason not selected for v1 |
|---|---|---|---|---|---|---|
| Robust peer-common aggregation | Less sensitive to outlier comparators. | Requires a robustness choice before evidence exists. | Can hide peer-set defects. | May obscure what "common" means. | Higher. | Keep for later fixture sensitivity after equal aggregation is understood. |
| Size-weighted peer-common repair | May reflect economic scale if size authority exists. | Imports size context into core repair. | Size missingness and duplicate share classes can distort results. | Peer-common repair becomes size-policy dependent. | Higher. | Size is a future conditioning layer, not v1 core. |
| Market-adjusted peer-common repair | Separates broad market recovery from economic-peer recovery. | Can turn market context into a third mechanism. | Over-control or market-state leakage. | Decomposition becomes harder to explain. | Higher. | Market context is a control in v1. |
| Ratio-style idiosyncratic contrast | Expresses relative magnitude. | Fragile when comparator repair is near zero or sign-changing. | Can manufacture extremes. | Less stable than direct contrast. | Medium. | Direct contrast is clearer and safer. |
| Bounded contrast index | Limits extreme values. | Requires bounds not yet scientifically approved. | Bound selection can become hidden optimization. | Less transparent. | Medium. | No thresholds or bounds are authorized. |
| Regression residual | Familiar statistical decomposition. | Violates the no-regression design boundary for this task. | Can import target leakage, fitting choices, and coefficients. | Residual may be mistaken for causal idiosyncrasy. | High. | Explicitly not selected. |

## 15. Formula Traceability Matrix

| Formula component | Observable concept | Measurement-spec section | First-module boundary | Information role | Scientific purpose | Contamination or falsification consideration |
|---|---|---|---|---|---|---|
| \(i\) | Target security | Sections 4-5 | Own-security repair indispensable | Governance-scoped subject | Identify repair target | Identity and ticker-lineage contamination. |
| \(P_i(t)\) | Comparator context | Sections 4-8 | Valid peer-common repair indispensable | Contextual Information | Define economic comparators | Peer-definition, current metadata, survivorship, source contamination. |
| \(B_t\) | Post-stress context | Sections 5-6 | Post-stress context indispensable | Alpha/context anchor | Define stress reference | Horizon shopping and retrospective stress inference. |
| \(H_t\) | Own and comparator repair timing | Section 6 | Repair observation required | Temporal governance | Observe post-stress repair | Timing misalignment and look-ahead. |
| \(S_i(t)\) | Post-stress eligibility | Sections 5-6 | Stress context required | Alpha/context gate | Gate applicability | Inferred-after-recovery contamination. |
| \(R_i(t)\) | Own-security repair | Sections 4-6 | Own repair indispensable | Alpha Observation | Observe target repair | Own-feature duplication. |
| \(R_j(t)\) | Comparator repair | Sections 4, 7-8 | Peer-common repair indispensable | Contextual Observation | Observe comparator repair | Invalid comparators and source-role mismatch. |
| \(C_i(t)\) | Peer-common repair | Sections 4, 7-8 | Primary comparator | Contextual derived quantity | Represent common comparator repair | Peer ablation and market contamination. |
| \(D_i(t)\) | Security-specific repair | Sections 4-5 | Interpretive remainder | Interpretive derived quantity | Represent target-specific component | Redundancy with own repair or fitted residual confusion. |
| \(M(t)\) | Market-context control | Section 8 | Broad market-state control | Contextual control | Prevent market recovery mislabeling | Market-state duplication. |
| \(Z_i(t)\) | Decomposition outcome | Sections 4-5, 9 | Core interpretive purpose | Interpretive Outcome | Classify meaning of repair | Must not become alpha without later evidence. |
| \(V_i(t)\) | Validity indicator | Sections 9-12 | Governance gates | Governance Information | Fail closed when prerequisites fail | Authority, identity, PIT, reproducibility gaps. |

## 16. Assumptions And Invariants

Every future implementation or formula refinement must preserve:

- PIT validity for identity, comparator membership, market context, and source-known timing;
- identity validity for target and comparators;
- comparator validity before peer-common repair is used;
- temporal alignment across \(B_t\), \(H_t\), \(t\), comparator observations, and market context;
- source independence from vendors, database schemas, source fields, programming languages, and architectures;
- no look-ahead from \(F_t\) or later source availability;
- no post hoc peer selection;
- no hidden optimization of comparator membership, aggregation, materiality, or horizons;
- no future leakage through current classifications or retrospective metadata;
- bounded module scope around post-stress repair decomposition;
- reproducibility and artifact-lineage readiness before empirical work;
- fail-closed behavior for invalid or unresolved prerequisites;
- role separation among Alpha Information, Contextual Information, Governance Information, and interpretive outcomes.

## 17. Undefined And Unresolved Cases

The formula must produce unresolved or unavailable status when:

| Case | Required behavior |
|---|---|
| Invalid target identity | \(Z_i(t)=\text{unresolved}\); no decomposition. |
| Invalid comparator identity | Exclude invalid comparator; if comparator set becomes insufficient or biased, unresolved. |
| Insufficient comparator context | \(C_i(t)\), \(D_i(t)\), and \(Z_i(t)\) unresolved. |
| Non-overlapping history | Unresolved because target and comparator repair are not aligned. |
| Unresolved stress | \(S_i(t)=\text{unresolved}\); decomposition unavailable. |
| Missing own observation | \(R_i(t)\) unavailable; decomposition unavailable. |
| Missing comparator observation | Exclude only if missingness is governed; otherwise unresolved. |
| Unstable denominator in alternative designs | Alternative unavailable; preferred direct contrast avoids this where possible. |
| Incompatible timing | Unresolved due to look-ahead or misalignment risk. |
| Ambiguous decomposition | \(Z_i(t)=\text{unresolved}\) unless predeclared materiality relations support common, idiosyncratic, or mixed interpretation. |
| Source conflict | Unresolved unless future source-role authority resolves the conflict. |

No imputation logic is invented.

## 18. Confounders And Exclusions

| Concept | Formula treatment | How v1 avoids silent dependence |
|---|---|---|
| Stabilization | Confounder, not core component. | Not included in \(R_i\), \(C_i\), or \(D_i\) unless future repair operator explicitly remains repair-only. |
| Volatility normalization | Existing-family control. | Not a decomposition term. |
| Participation recovery | Existing-family confounder. | Not included in preferred repair operator. |
| Liquidity recovery | Existing-family confounder. | Not included in preferred repair operator. |
| VoV | Deferred contamination check. | No VoV observation enters v1 formula. |
| Rank persistence | Excluded. | No peer rank or ranking relation is defined. |
| Transition sequencing | Excluded/control. | Temporal ordering is required, but transition order is not a mechanism. |
| Leadership rotation | Excluded negative-evidence constraint. | No leadership status is defined. |
| Peer dispersion | Excluded. | Equal aggregation is used only for peer-common repair, not dispersion. |
| Asymmetry | Later bounded extension. | \(Z_i(t)\) permits interpretation without positive/negative asymmetry module logic. |
| Macroeconomic conditioning | Deferred. | No macro term appears. |
| Corporate events | Governance/confounder. | Event ambiguity forces unresolved status rather than event-specific formula behavior. |
| Source-specific taxonomy choices | Excluded. | \(P_i(t)\) requires future accepted context; no taxonomy is selected. |
| Portfolio construction | Excluded. | No action, weighting, or portfolio output appears. |
| ML | Excluded. | No learned representation, embedding, or model is defined. |

## 19. Falsification Implications

Future evidence would challenge the measurement if:

- \(R_i(t)\) cannot be observed reproducibly without source-specific assumptions;
- stress eligibility cannot be separated from later repair;
- comparator observations cannot be aligned historically.

Future evidence would challenge the decomposition if:

- \(C_i(t)\) fails to represent meaningful common comparator repair;
- \(D_i(t)\) is only a restatement of own-security repair;
- \(Z_i(t)\) is unstable under predeclared valid comparator ablations.

Future evidence would challenge the comparator role if:

- peer-common repair behaves like broad market recovery;
- results depend on current-state peers or survivor-only peers;
- invalid identity or missing delisted securities drive apparent decomposition.

Future evidence would challenge the idiosyncratic interpretation if:

- direct contrast collapses into existing repair, volatility compression, participation, VoV, persistence, rank, or transition families;
- materiality relations cannot distinguish common, idiosyncratic, mixed, and unresolved outcomes consistently.

Future evidence would challenge the relationship to existing repair evidence if:

- the formula only refines when existing repair works and adds no separate interpretive value;
- peer context changes labels but not scientific meaning;
- negative controls produce apparently useful decomposition.

No falsification or validation is performed here.

## 20. Synthetic Fixture Requirements

Conceptual synthetic cases required before implementation:

| Case | Setup | Expected qualitative formula behavior |
|---|---|---|
| Target and peers repair together | \(R_i(t)\) and most \(R_j(t)\) show aligned repair. | \(C_i(t)\) explains most repair; \(Z_i(t)\) predominantly common if validity passes. |
| Target repairs while peers do not | \(R_i(t)\) material; \(C_i(t)\) immaterial or insufficient. | \(D_i(t)\) captures target-specific repair; \(Z_i(t)\) predominantly idiosyncratic if valid. |
| Peers repair while target does not | \(C_i(t)\) material; \(R_i(t)\) weak. | \(D_i(t)\) indicates target shortfall; \(Z_i(t)\) mixed or idiosyncratic weakness only if materiality rules allow; otherwise unresolved. |
| Target and peers diverge partially | Both \(C_i(t)\) and \(D_i(t)\) are material. | \(Z_i(t)\) mixed. |
| Comparator context invalid | \(P_i(t)\) not accepted or not PIT-valid. | \(C_i(t)\), \(D_i(t)\), and \(Z_i(t)\) unresolved. |
| Stress unresolved | \(S_i(t)=\text{unresolved}\). | Formula unavailable for first-module interpretation. |
| Market-wide repair | \(M(t)\) indicates broad recovery aligned with peers. | Decomposition remains available only as contextual interpretation; future tests must flag market contamination risk. |
| Target observation missing | \(R_i(t)\) unavailable. | Decomposition unresolved. |
| Comparator observation missing | Some or all \(R_j(t)\) unavailable. | Governed missingness may exclude comparators; ungoverned or insufficient coverage forces unresolved. |
| Timing misalignment | Comparator or context observation uses a different historical relationship. | Unresolved. |
| PIT membership violation | Future peer membership enters \(P_i(t)\). | Fail closed. |
| Extreme or unstable input case | Repair observations are extreme, sign-changing, or scale-unstable. | Preferred direct contrast remains defined only if materiality and observability gates pass; otherwise unresolved. |

No fixtures are implemented.

## 21. Acceptance-Test Requirements

Future acceptance-test categories:

| Category | Required future test purpose |
|---|---|
| Algebraic consistency | Confirm \(R_i(t)=C_i(t)+D_i(t)\) where all terms are valid. |
| Temporal integrity | Confirm \(B_t \prec H_t \preceq t \prec F_t\) and no future information enters decomposition. |
| Decomposition consistency | Confirm common, idiosyncratic, mixed, and unresolved states follow predeclared relations. |
| Unresolved-state handling | Confirm invalid prerequisites never force numeric interpretation. |
| Invariance to source representation | Confirm equivalent accepted evidence yields the same scientific interpretation independent of source schema. |
| Comparator validity | Confirm invalid, future-known, empty, or misaligned comparators fail closed. |
| Reproducibility | Confirm formula inputs and derived quantities can be traced to preserved evidence. |
| Traceability | Confirm every term maps to an approved observable concept. |
| Fail-closed behavior | Confirm authority, identity, context, timing, coverage, and source conflicts block use. |
| Contamination visibility | Confirm market, own-feature, repair-family, peer-definition, survivorship, and temporal risks are surfaced. |

No code or executable tests are written here.

## 22. Remaining Work Before Implementation

Formula completion items:

- Preferred v1 formulation is defined.
- Materiality relations remain symbolic and must be frozen before empirical use.
- Future formula documentation must preserve the exclusions and unresolved-state logic.

Synthetic fixture work:

- Conceptual fixture cases must be translated into a fixture specification without real data.

Acceptance-test work:

- Acceptance-test categories must be converted into source-independent, non-source-specific test specifications.

Interface work:

- Abstract input/output roles may be specified later, but no source fields, schemas, or code interfaces are approved here.

Implementation work:

- No implementation may begin until fixture and acceptance-test specifications exist and a separate implementation authorization is granted.

Discovery work:

- No discovery, candidates, panels, IC, threshold estimation, or empirical tuning may begin.

Validation work:

- No validation may begin until implementation, panel, discovery, contamination, and governance gates are separately satisfied.

Primary remaining gap:

`SYNTHETIC_FIXTURE_AND_ACCEPTANCE_TEST_SPECIFICATION_ABSENT`

## 23. Readiness Conclusion

Project Underdog is ready to proceed to synthetic fixture and acceptance-test specification for the first module.

This conclusion is limited to the next specification step. It does not authorize code implementation, data retrieval, real peer construction, source selection, candidate creation, registry creation, panel generation, IC discovery, empirical validation, production changes, threshold changes, survivor-status changes, or ML.

Final classification restated: `FIRST_MODULE_FORMULA_SPECIFICATION_DEFINED`

## 24. Recommended Next Lifecycle Step

Recommended exactly one next lifecycle step:

`Project Underdog - First Module Synthetic Fixture And Acceptance-Test Specification v1`

This next step should turn the preferred source-independent formula, unresolved-state logic, fixture cases, and acceptance-test categories into a bounded non-implementation specification. It must not write code, retrieve data, contact sources, construct real peer groups, optimize peer membership, estimate coefficients, estimate thresholds, run regressions, create candidates, create registries, create panels, compute IC, perform discovery, perform validation, modify survivor status, modify governance, create production artifacts, or introduce ML.
