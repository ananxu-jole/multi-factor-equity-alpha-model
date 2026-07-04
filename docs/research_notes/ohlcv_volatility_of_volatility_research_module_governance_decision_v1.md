# Project Underdog - OHLCV Volatility-of-Volatility Research Module Governance Decision v1

## SECTION 1 - Governance Objective

This note executes Phase 10 - Governance Decision of the Project Underdog Standard Research Module Lifecycle for the OHLCV Volatility-of-Volatility research module.

Classification: `MODULE_GOVERNANCE_APPROVED`

This is a governance decision record only. It does not perform refinement, regenerate panels, recompute IC, modify formulas, change governance thresholds, update production registry state, perform validation, or introduce ML.

Governance decision scope:

- Module: OHLCV Volatility-of-Volatility Research Module v1.
- Prior lifecycle phase: Phase 9 - Research Review.
- Phase 9 classification: `REFINEMENT_APPROVED`.
- Phase 8 IC discovery classification: `IC_DISCOVERY_COMPLETE_ADVANCE_CANDIDATES`.
- Candidate universe reviewed: `vov_01`, `vov_02`, `vov_03`, `vov_04`, `vov_05`.
- Authorized next work: refinement design for `vov_01` and `vov_03` only.

## SECTION 2 - Governance Inputs Reviewed

Reviewed governance inputs:

| input | path | classification / status | governance use |
| --- | --- | --- | --- |
| Phase 9 research review | `docs/research_notes/ohlcv_volatility_of_volatility_research_module_research_review_v1.md` | `REFINEMENT_APPROVED` | Primary governance recommendation source. |
| Phase 8 IC discovery note | `docs/research_notes/ohlcv_volatility_of_volatility_research_module_ic_discovery_v1.md` | `IC_DISCOVERY_COMPLETE_ADVANCE_CANDIDATES` | Candidate evidence, horizon behavior, rankings, and recommendations. |
| IC discovery artifacts | `artifacts/research/ohlcv_volatility_of_volatility_research_module_v1/ic_discovery_v1/` | Completed Phase 8 artifacts | Supporting research-only evidence. |
| Approved panel artifacts | `artifacts/research/ohlcv_volatility_of_volatility_research_module_v1/panel_v1/` | Previously approved for IC discovery | Input lineage for Phase 8 only; not modified here. |

The Phase 9 review concluded that refinement is scientifically justified for a bounded subset of the VoV module. The decision below records that conclusion as the official Phase 10 governance outcome.

## SECTION 3 - Official Candidate Decisions

| candidate_id | official outcome | refinement design authorized | rationale |
| --- | --- | --- | --- |
| `vov_01` | `ADVANCE` | Yes | Strong medium-horizon evidence with h20 mean IC of 0.010405, h20 IC IR of 0.093197, and h20 positive IC rate of 0.535383. Phase 9 found the mechanism interpretable and suitable for bounded refinement. |
| `vov_03` | `ADVANCE` | Yes | Strong h10 behavior with h10 mean IC of 0.008204, h10 IC IR of 0.074103, and h10 positive IC rate of 0.546996, with supportive medium-horizon structure. Phase 9 found the mechanism distinct enough to justify refinement design. |
| `vov_05` | `WATCH` | No | Best h20 mean IC in the discovery pass, but positive IC rate and stability were not strong enough for immediate refinement authorization. Retain as a watchlist comparator only. |
| `vov_02` | `PARK` | No | Negative primary-horizon evidence and weak medium-horizon behavior. Not eligible for refinement from this module pass. |
| `vov_04` | `PARK` | No | Negative h5/h10/h20 evidence and adverse rolling behavior. Not eligible for refinement from this module pass. |

Official governance outcome:

- `ADVANCE`: `vov_01`, `vov_03`.
- `WATCH`: `vov_05`.
- `PARK`: `vov_02`, `vov_04`.

## SECTION 4 - Governance Rationale

The VoV module produced candidate-level evidence strong enough to justify a narrow refinement path, but not broad family-level validation evidence. The approved candidates share a volatility-of-volatility mechanism but express it through different enough horizon and stability profiles to support a controlled refinement design.

`vov_01` is approved because its h20-led evidence is aligned with the module's medium-horizon thesis and has a stronger positive IC rate than the watch candidate. `vov_03` is approved because its h10 behavior is the cleanest primary-horizon evidence in the module and provides a complementary refinement target to the h20-led candidate.

`vov_05` remains on watch because it produced the strongest h20 mean IC, but the review did not find sufficient hit-rate and stability evidence to authorize immediate refinement. `vov_02` and `vov_04` are parked because their primary-horizon evidence is negative or materially weak.

This decision is conservative: it authorizes refinement design for only two candidates and preserves all other candidates as watch or parked evidence.

## SECTION 5 - Authorized Next Work

Authorized:

- Phase 11 - Master Research State Update for the VoV module.
- A future separate refinement design task for `vov_01`.
- A future separate refinement design task for `vov_03`.
- Refinement design may include anchor preservation, small predeclared variants, anti-redundancy controls, and contamination checks against existing OHLCV families.

Refinement design requirements for any future task:

- Keep `vov_01` and `vov_03` as the only approved refinement seeds.
- Preserve original discovery anchors for comparison.
- Limit variants to interpretable mechanism changes.
- Include redundancy checks versus volatility compression, stress repair, persistence, rank-coherence, reversal, and volume shock reversal families.
- Keep h10/h20 as primary review horizons unless a predeclared diagnostic reason is documented.

## SECTION 6 - Non-Authorized Work

Not authorized by this decision:

- Refinement execution.
- Refinement design or execution for `vov_05`.
- Refinement design or execution for `vov_02`.
- Refinement design or execution for `vov_04`.
- Panel regeneration.
- IC recomputation.
- Validation.
- Formula changes.
- Family B Dispersion Path-Dependence implementation or execution.
- Family C Event Clustering implementation or execution.
- Governance threshold changes.
- Production registry changes.
- ML modeling or ML-assisted candidate generation.

## SECTION 7 - Archival Guidance

The Phase 8 and Phase 9 artifacts should remain archived as research-only evidence for the VoV module.

Archival treatment by candidate:

- `vov_01`: preserve as an approved refinement seed and original discovery anchor.
- `vov_03`: preserve as an approved refinement seed and original discovery anchor.
- `vov_05`: preserve as a watchlist comparator, not a refinement seed.
- `vov_02`: preserve as parked negative evidence.
- `vov_04`: preserve as parked negative evidence.

The panel artifacts and IC discovery artifacts should remain immutable inputs for the Phase 9 and Phase 10 record. Any future refinement work should write to a new artifact root and should not overwrite the Phase 8 discovery artifacts.

## SECTION 8 - Explicit Non-Goals

This governance decision does not:

- Promote any candidate to validation.
- Promote any candidate to production.
- Declare VoV a validated alpha family.
- Expand the candidate universe.
- Authorize additional discovery.
- Authorize refinement for watch or parked candidates.
- Modify formulas, panel schemas, IC methodology, or research thresholds.

## SECTION 9 - Recommended Phase 11 State Update

The next lifecycle task should be:

**Project Underdog - OHLCV Volatility-of-Volatility Master Research State Update v1**

The Phase 11 update should record:

- VoV module Phase 10 classification: `MODULE_GOVERNANCE_APPROVED`.
- `vov_01` and `vov_03` advanced to refinement-design eligibility.
- `vov_05` retained on watch only.
- `vov_02` and `vov_04` parked.
- No validation, production registration, threshold change, governance mutation, or ML authorization.

## SECTION 10 - Verification Summary

Verification status:

- No implementation files were changed by this governance decision.
- No panel artifacts were changed.
- No IC artifacts were changed.
- No refinement was executed.
- No validation was executed.
- No production registry changes were made.
- No governance threshold changes were made.
- No ML was introduced.

This note is documentation-only and records the official Phase 10 governance decision for the completed VoV research module.
