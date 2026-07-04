# Project Underdog Research State Audit v1

Date: 2026-06-17

## SECTION 1 – Executive Assessment

### Overall project maturity
- Rating: 5 / 10.
- The platform shows disciplined research process, clear candidate lifecycle stages, and strong documentation of Track B discovery/refinement/validation.
- It is not yet mature: the work is still in a narrow conditional research phase, the inventory remains small, and no candidate is ready for portfolio or ML deployment.

### Research quality
- High on process clarity: the project documents the transition from v2/v3 failure modes to v4/v5 conditional design, and it explicitly separates discovery from validation and governance.
- Evidence focus is strong: candidate decisions are based on h20 IC, WFV-style persistence, turnover refinement, state slices, and similarity diagnostics.
- Weakness: the current candidate base is concentrated in a narrow family of participation/liquidity/breadth state repairs, which increases the chance that the research is tracing a single mechanism rather than discovering independent edges.

### Governance quality
- Governance quality is good for a research stage: the audit notes explicitly preserve non-production boundaries, watch-monitor labels are used, and no production changes are claimed.
- The conditional inventory governance framework is well defined in `conditional_alpha_inventory_monitoring_v2.md` and `conditional_alpha_inventory_v2_governance_update.md`.
- Weakness: the master recap sometimes treats watch-monitor status as a stable anchor even though the underlying watch reasons (rolling h20 weakness, one-window dominance) are still present.

### Validation quality
- Validation is solid for research: the candidate lifecycle includes multiple layers of validation-like review, a fixed-variant package, and a clear distinction that recovery-quality targets remain diagnostic only.
- The validation anchor remains raw h10/h20 IC, which is appropriate and conservative.
- Weakness: the strongest candidate still has a low rolling h20 IC and watch-monitor status, meaning the validation evidence is not yet robust enough for a construction-ready decision.

### Risk of false discoveries
- Moderate to high.
- The project acknowledges a strong reversal manifold and is correctly cautious, but the current inventory is small and concentrated.
- The high co-activation between `participation_liquidity_state_shift_20_60` and `participation_breadth_repair_under_hostile_trend` is a signal the system may be reusing the same underlying mechanism in slightly different forms.

### Risk of overfitting
- Moderate.
- The focus on h20 and state-conditioned behavior makes the work more sophisticated than naive signal mining, but it also increases the risk of overfitting to specific hostile/stress regimes.
- Watch-monitor candidates with weak recent-window metrics and limited active coverage are particularly vulnerable to overfit.

### Current strengths
- Clear research governance and documentation.
- Strong process discipline: discovery, diagnostics, refinement, and monitoring are separated.
- Explicit non-production boundaries and metadata caution labels.
- Good handling of turnover risk and rank-churn diagnosis.
- A narrow, defensible current research direction (conditional active repair/stabilization).

### Current weaknesses
- Candidate set is narrow and concentrated on related participation/liquidity/breadth mechanisms.
- Economic Context Enrichment remains static-snapshot only and cannot support alpha validation or ML conditioning yet.
- The leading candidate is watch-monitor, not healthy production-ready.
- Metadata readiness is below the level needed for research-grade sector/peer conditioning.
- ML readiness is premature.

### Post-audit OHLCV frontier update
- The OHLCV Non-Hostile Transition and Leadership Rotation research cycle has completed and is now classified `FAMILY_PARKED_INVERSION_DIAGNOSTIC_OPTIONAL`.
- All nine approved candidates were classified `REJECT`; no candidate is recommended for refinement, watchlist status, validation, governance action, production registration, threshold change, or ML use.
- The generated panels and IC artifacts remain archived as research evidence.
- Direction inversion is optional only as a future design task, not an active refinement path.

### Post-audit VoV module update
- The OHLCV Volatility-of-Volatility Research Module v1 has completed the full standard lifecycle through Phase 11 and is synchronized as `MODULE_STATE_SYNCHRONIZED`.
- Phase 10 governance classification was `MODULE_GOVERNANCE_APPROVED`.
- Official candidate outcomes are: `vov_01` and `vov_03` `ADVANCE`; `vov_05` `WATCH`; `vov_02` and `vov_04` `PARK`.
- The OHLCV Volatility-of-Volatility Bounded Refinement v1 has also completed one bounded refinement cycle and is synchronized as `REFINEMENT_STATE_SYNCHRONIZED`.
- Refinement governance classification is `REFINEMENT_GOVERNANCE_APPROVED`.
- Official refinement outcomes are: `vov_03_ref_strict_chop` and `vov_01_ref_smoothed_calm` `VALIDATION-DESIGN APPROVED`; `vov_01_ref_anchor` and `vov_03_ref_anchor` baseline comparators; `vov_01_ref_longer_memory` `WATCH`; `vov_01_ref_strict_calm`, `vov_03_ref_longer_chop`, and `vov_03_ref_extension_controlled` `PARK`.
- Validation-design work is authorized only for `vov_03_ref_strict_chop` and `vov_01_ref_smoothed_calm`; no additional refinement cycle is authorized.
- The generated original and refinement panels and IC artifacts remain archived as research evidence and should not be overwritten by future work.

## SECTION 2 – Candidate Inventory Audit

### participation_liquidity_state_shift_20_60
- Current status: `WATCH_MONITOR`, `CONDITIONAL_ALPHA_REVIEW_READY_WITH_GUARDRAILS`.
- Supporting evidence: v4 conditional diagnostics, focused refinement, conditional validation, fixed four-variant package, h20 IC ~0.0284, WFV persistence/sign consistency 1.00/1.00.
- Weaknesses: rolling h20 IC near zero; recent-window evidence weak; high turnover proxy ~0.0964; watch-monitor status means it is not yet reliable.
- Redundancy risk: moderate; co-activation with `participation_breadth_repair_under_hostile_trend` is high (~0.80 in one direction), indicating the same underlying participation/breadth repair family.
- Confidence level: medium.
- Recommendation: deserves additional refinement and equivalence testing, not archive.

### participation_breadth_repair_under_hostile_trend
- Current status: `HEALTHY_ACTIVE_RESEARCH`, `CONDITIONAL_REFINEMENT_CANDIDATE`.
- Supporting evidence: v5 focused discovery, h20 mean IC ~0.0307, positive IC rate ~58%, WFV persistence/sign consistency 1.00/1.00, low turnover proxy ~0.0136.
- Weaknesses: low active coverage (~14%), still a research candidate rather than a validation anchor, and it is close to the same mechanism cluster as the existing Track B candidate.
- Redundancy risk: high relative to the existing participation/liquidity candidate; similarity and co-activation suggest this may be more of a variant than a truly independent edge.
- Confidence level: medium-high.
- Recommendation: deserves additional refinement and focused diagnostics, with a strong emphasis on proving orthogonality and independent state semantics.

### volatility_compression_after_stress_stabilization
- Current status: `WATCH_MONITOR`, `INVENTORY_ACTIVE_RESEARCH_WITH_GUARDRAILS`.
- Supporting evidence: moderate h20 metrics (~0.0284 mean IC, ~57% positive rate), moderate turnover, and explicit guardrail reasons.
- Weaknesses: one-window dominance, weak recent positive rate, and still not clearly separated from broader stress/volatility behavior.
- Redundancy risk: low to moderate; it appears structurally different from the participation/breadth cluster, but it remains within the same hostile/stress regime family.
- Confidence level: medium-low.
- Recommendation: keep as monitored research; do not promote until the concentration and recent-window issues are resolved.

### nonprice_liquidity_repair_without_price_extension
- Current status: `CONDITIONAL_ONLY_RESEARCH`.
- Supporting evidence: a concept from the v5 screening and focused discovery with low baseline correlation to the prior participation/liquidity candidate.
- Weaknesses: weak best-horizon IC, weak persistence, weak positive IC rate, and status is explicitly research-only.
- Redundancy risk: moderate; it may still be in the broader liquidity/participation family and not truly orthogonal.
- Confidence level: low.
- Recommendation: archive or hold for redesign; it does not deserve additional refinement unless its state thesis is made much sharper.

### nonprice_liquidity_persistence_20_60
- Current status: `CONDITIONAL_ONLY_KEEP`.
- Supporting evidence: prior Track B non-price liquidity work with structural distance from price rank.
- Weaknesses: insufficient standalone evidence, likely weaker than the current inventory candidates.
- Redundancy risk: moderate; it is likely an ingredient rather than an independent candidate.
- Confidence level: low.
- Recommendation: archive as a reference ingredient unless a future design explicitly repurposes it.

### Rejected candidates to archive
- `stress_to_normalization_participation_repair` — sparse activation and insufficient stable evidence.
- `conditional_low_overextension_breakout_20` — likely reversal contamination and weak state activation.
- `gap_followthrough_low_churn_10` — event-quality/state coverage concerns and weak orthogonality.
- OHLCV Non-Hostile Transition and Leadership Rotation approved set (`nhlr_01`, `nhlr_02`, `nhlr_03`, `nhlr_04`, `nhlr_05`, `nhlr_07`, `nhlr_08`, `nhlr_09`, `nhlr_10`) — broad negative h10/h20 IC evidence; best candidate `nhlr_05` h10 mean IC -0.000173; family classification `FAMILY_PARKED_INVERSION_DIAGNOSTIC_OPTIONAL`.
- OHLCV Volatility-of-Volatility parked set (`vov_02`, `vov_04`) — parked after Phase 10 governance due weak or negative primary-horizon evidence; retain as negative evidence only. `vov_05` is watch-only and should not be treated as a refinement seed. Bounded refinement parked set (`vov_01_ref_strict_calm`, `vov_03_ref_longer_chop`, `vov_03_ref_extension_controlled`) should remain archived; `vov_01_ref_longer_memory` is watch-only.
- Recommendation: archive these as rejected research clues; do not re-open without a clearly new thesis.

## SECTION 3 – Research Coverage Analysis

### Over-explored areas
- OHLCV interactions: the current work is already dense in participation/liquidity/breadth interactions and state-transition combinations.
- Participation signals: heavily explored as the core conditional family, especially participation repair under hostile or weak breadth states.
- Breadth signals: also heavily explored in the current inventory and v5 concept set.
- Liquidity signals: well covered through participation/liquidity state shift and non-price liquidity concepts.
- Recovery/stress signals: covered in the current inventory and v5 candidate set, particularly through stress/stabilization and volatility compression themes.

### Moderately explored areas
- Volatility interactions: present, but largely in the stress/volatility-compression family rather than broader dispersion or range-structure research.
- Volatility-of-volatility: now completed as a standard OHLCV module and one bounded refinement cycle; validation-design is approved only for `vov_03_ref_strict_chop` and `vov_01_ref_smoothed_calm`, with `vov_01_ref_anchor`/`vov_03_ref_anchor` retained as baseline comparators. Evidence is candidate-level and validation-design eligible, not validation-ready.
- Recovery/stress: explored mainly through a few specific stress transition concepts, not a diverse set of stress regimes.

### Under-explored areas
- Economic context and peer-relative mechanisms: appropriately blocked by current metadata readiness, but still under-explored as research content.
- Sector/industry controls and peer-group conditional behavior: no validation-quality work yet.
- Alternative horizons below h20 in a state-aware way: h10/h15 are noted but not strongly represented.
- Dispersion transition and cross-sectional stability outside the current candidate family.
- Non-OLHCV metadata-based signals, once point-in-time data is available.
- Portfolio-level interaction or construction-layer diagnostics, which are intentionally deferred.

## SECTION 4 – Economic Context Assessment

### Status determination
- Economic Context Enrichment is: **Diagnostic Only**.

### Justification
- The documentation explicitly states the metadata layer is static snapshot only (`STATIC_SNAPSHOT_RESEARCH_ONLY`) and not point-in-time safe.
- Coverage expansion has improved descriptive diagnostics, but the source notes and readiness review still block sector-relative alpha research, peer-relative transforms, and validation claims.
- The current state is useful for coverage repair, inventory exposure audits, and peer-group refinement planning, but not for production or ML readiness.
- Therefore, the correct classification is Diagnostic Only, not Research Ready or Production Ready.

## SECTION 5 – ML Readiness Audit

### Feature quality
- Raw features exist and the candidate pipeline produces conditional state features.
- Current features are still research-stage and not frozen; the strongest features are associated with watch-monitor candidates.
- Data quality is moderate, but feature readiness is limited by the lack of resilient economic metadata and by the narrow candidate set.

### Label quality
- Raw h10/h20 IC labels are appropriate and remain the core validation anchor.
- Recovery-quality targets are explicitly diagnostic and should not be used as labels yet.
- Label quality is good for research diagnostics, but not sufficient for production ML.

### Sample size
- Candidate exposure is small: only a handful of active inventory candidates, limited active coverage, and heavy state dependence.
- A true ML experiment would require more diverse candidate representation and more stable sample coverage.
- Sample size is therefore too small for robust ML deployment.

### Validation framework
- The research framework has a strong offline validation culture, but it is not yet an ML-ready validation framework.
- The current framework is designed around candidate-level metrics, not model-level cross-validation or held-out generalization tests.
- The conditional-alpha path lacks a dedicated ML validation layer.

### Metadata readiness
- Metadata is not ready for ML: static snapshot only, no point-in-time, and explicitly blocked for alpha conditioning.
- This means any metadata-enriched ML would risk look-ahead and mis-specified peer controls.

### Explicit answers
1. Is ML introduction justified now?
   - No.
2. What prerequisites remain?
   - Stabilize the candidate inventory and resolve watch-monitor risks.
   - Complete point-in-time economic metadata sourcing and lineage.
   - Freeze a fixed candidate package and prove rebuild/equivalence.
   - Define an ML validation framework separate from candidate-level signal validation.
3. What is the estimated project stage relative to ML deployment?
   - Early stage. The project is in a pre-ML research stabilization phase, likely 2–3 out of 10 on an ML deployment maturity scale.

## SECTION 6 – Highest Expected Value Next Step

### Ranked options
1. Candidate consolidation
   - Rationale: the current inventory is small and concentrated; consolidating and stabilizing the strongest candidates will reduce false-discovery risk and clarify the next research frontier.
2. Metadata-enriched conditional alpha research
   - Rationale: the next high-value work is to complete the metadata readiness path and then carefully test economic-context conditioning, but only after candidate stabilization.
3. Peer-relative / economic-context readiness
   - Rationale: this remains the highest-value diversification direction once point-in-time metadata evidence is available.
4. Optional OHLCV direction-inversion diagnostic design
   - Rationale: the parked non-hostile transition/leadership-rotation family showed broad negative primary-horizon signs, but any inversion work should be design-only and diagnostic rather than continuation discovery.
5. Portfolio-level research
   - Rationale: premature until the inventory is stabilized and the candidate families are clearly distinct.
6. ML preparation
   - Rationale: necessary later, but current stage is too early; ML prep should follow candidate consolidation and metadata readiness.

## SECTION 7 – Research Roadmap

### 30-day plan
- Conduct a focused audit and rebuild/equivalence pass for `participation_liquidity_state_shift_20_60`.
- Refresh conditional inventory monitoring and verify whether watch-monitor issues persist.
- Complete metadata source lineage and point-in-time planning work; do not begin sector-relative research.
- Narrowly refine `participation_breadth_repair_under_hostile_trend` and test its orthogonality to the existing inventory.
- Add a validation-design review task for VoV refinement variants `vov_03_ref_strict_chop` and `vov_01_ref_smoothed_calm`, after preserving the original and refinement evidence archives.

### 60-day plan
- Consolidate the inventory around the strongest stable candidates and archive the weaker research-only items.
- If metadata planning is successful, begin one controlled metadata-enriched conditional alpha diagnostic experiment, but keep it descriptive and isolated.
- Document explicit candidate consolidation criteria and a reduced research candidate list.
- Continue monitoring and update the watch-monitor governance notes.

### 90-day plan
- If the candidate inventory is consolidated and metadata readiness is improved, execute a second narrow conditional alpha research pass with one or two metadata-enriched concepts.
- Keep portfolio-level or ML preparation deferred until the new inventory is proven stable.
- Produce a second audit or readiness review before any construction-layer or ML-layer escalation.

---

## Audit caveat
- This assessment is based on the referenced documents in the workspace and the newly created master recap.
- It does not rely on new pipeline runs, signal generation, or production code changes.
