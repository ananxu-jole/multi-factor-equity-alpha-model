from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from pipelines.project_underdog_first_module_reference_implementation_v1 import (
    canonical_fixtures as first_module_fixtures,
    run_first_module_reference,
)
from pipelines.project_underdog_phase5_comparator_construction_reference_implementation_v1 import (
    ComparatorConstructionRecord,
    ComparatorContextSupportMetadata,
    ComparatorCoverageMetadata,
    ComparatorDiagnosticCode,
    ComparatorEligibilityState,
    ComparatorIntervalMetadata,
    ComparatorRelationshipMetadata,
    TemporalApplicabilityState,
    canonical_comparator_construction_fixtures,
    comparator_construction_guardrail_manifest,
    evaluate_comparator_construction,
)
from pipelines.project_underdog_phase5_pit_identity_and_context_evidence_reference_implementation_v1 import (
    canonical_pit_identity_context_fixtures,
    evaluate_pit_identity_context,
)
from pipelines.project_underdog_phase5_source_authority_reference_implementation_v1 import (
    canonical_source_authority_fixtures,
    evaluate_source_authority,
)


def _diagnostic_codes(result):
    return tuple(diag.code for diag in result.diagnostics)


def _fixture_by_id(fixture_id: str):
    return {fixture.fixture_id: fixture for fixture in canonical_comparator_construction_fixtures()}[fixture_id]


def _base_record(**overrides):
    values = {**_fixture_by_id("CC1_eligible").record.__dict__}
    values.update(overrides)
    return ComparatorConstructionRecord(**values)


def _with_relationship(record, **overrides):
    values = {**record.relationship.__dict__}
    values.update(overrides)
    return ComparatorRelationshipMetadata(**values)


def _with_comparator_interval(record, interval):
    comparator = type(record.comparator)(
        identity_id=record.comparator.identity_id,
        applicability_interval_ids=(interval.interval_id,),
        interval=interval,
        pit_identity_trace=record.comparator.pit_identity_trace,
    )
    relationship = _with_relationship(record, comparator_interval_id=interval.interval_id)
    values = {**record.__dict__, "comparator": comparator, "relationship": relationship}
    return ComparatorConstructionRecord(**values)


def test_all_canonical_comparator_fixtures_match_expected_states_diagnostics_and_limitations():
    fixtures = canonical_comparator_construction_fixtures()
    assert len(fixtures) == 20
    assert len({fixture.fixture_id for fixture in fixtures}) == 20

    for fixture in fixtures:
        result = evaluate_comparator_construction(fixture.record)
        assert result.eligibility_state == fixture.expected_eligibility_state
        assert result.temporal_applicability_state == fixture.expected_temporal_state
        for expected_code in fixture.expected_diagnostic_codes:
            assert expected_code in _diagnostic_codes(result)
        for expected_limitation in fixture.expected_limitations:
            assert expected_limitation in result.limitations


def test_only_approved_eligibility_states_exist():
    assert {state.value for state in ComparatorEligibilityState} == {
        "COMPARATOR_ELIGIBLE",
        "COMPARATOR_CONDITIONALLY_ELIGIBLE",
        "COMPARATOR_UNRESOLVED",
        "COMPARATOR_INELIGIBLE",
        "COMPARATOR_EXCLUDED",
        "INSUFFICIENT_COMPARATOR_EVIDENCE",
    }


def test_comparator_record_registration_preserves_relationship_metadata():
    result = evaluate_comparator_construction(_fixture_by_id("CC1_eligible").record)

    assert result.eligibility_state == ComparatorEligibilityState.COMPARATOR_ELIGIBLE
    assert result.relationship.relationship_type == "synthetic_economic_comparator"
    assert result.target.identity_id == "synthetic_target"
    assert result.comparator.identity_id == "synthetic_comparator"


def test_relationship_invariant_requires_exactly_one_target_and_comparator_interval():
    missing_target = evaluate_comparator_construction(_fixture_by_id("CC7_missing_target_interval").record)
    missing_comparator = evaluate_comparator_construction(_fixture_by_id("CC8_missing_comparator_interval").record)

    assert ComparatorDiagnosticCode.MISSING_COMPARATOR_APPLICABILITY in _diagnostic_codes(missing_target)
    assert ComparatorDiagnosticCode.MISSING_COMPARATOR_APPLICABILITY in _diagnostic_codes(missing_comparator)
    assert missing_target.eligibility_state == ComparatorEligibilityState.INSUFFICIENT_COMPARATOR_EVIDENCE
    assert missing_comparator.eligibility_state == ComparatorEligibilityState.INSUFFICIENT_COMPARATOR_EVIDENCE


def test_multiple_interval_references_fail_closed_to_insufficient_evidence():
    base = _fixture_by_id("CC1_eligible").record
    target = type(base.target)(
        identity_id=base.target.identity_id,
        applicability_interval_ids=(base.target.interval.interval_id, "extra_target_interval"),
        interval=base.target.interval,
        pit_identity_trace=base.target.pit_identity_trace,
    )
    result = evaluate_comparator_construction(_base_record(target=target))

    assert result.eligibility_state == ComparatorEligibilityState.INSUFFICIENT_COMPARATOR_EVIDENCE
    assert ComparatorDiagnosticCode.MISSING_COMPARATOR_APPLICABILITY in _diagnostic_codes(result)


def test_identity_to_interval_mismatch_is_ineligible():
    result = evaluate_comparator_construction(_fixture_by_id("CC9_identity_interval_mismatch").record)

    assert result.eligibility_state == ComparatorEligibilityState.COMPARATOR_INELIGIBLE
    assert ComparatorDiagnosticCode.CONFLICTING_COMPARATOR in _diagnostic_codes(result)


def test_self_comparison_or_same_interval_is_ineligible_duplicate_exposure():
    base = _fixture_by_id("CC1_eligible").record
    comparator = type(base.comparator)(
        identity_id=base.target.identity_id,
        applicability_interval_ids=(base.target.interval.interval_id,),
        interval=base.target.interval,
        pit_identity_trace=base.comparator.pit_identity_trace,
    )
    relationship = _with_relationship(
        base,
        comparator_identity_id=base.target.identity_id,
        comparator_interval_id=base.target.interval.interval_id,
    )
    result = evaluate_comparator_construction(_base_record(comparator=comparator, relationship=relationship))

    assert result.eligibility_state == ComparatorEligibilityState.COMPARATOR_INELIGIBLE
    assert ComparatorDiagnosticCode.DUPLICATE_EXPOSURE_UNRESOLVED in _diagnostic_codes(result)


def test_temporal_overlap_states_are_deterministic():
    valid = evaluate_comparator_construction(_fixture_by_id("CC10_valid_temporal_overlap").record)
    invalid = evaluate_comparator_construction(_fixture_by_id("CC11_invalid_temporal_overlap").record)
    partial = evaluate_comparator_construction(_fixture_by_id("CC12_partial_overlap").record)

    assert valid.temporal_applicability_state == TemporalApplicabilityState.VALID_OVERLAP
    assert invalid.temporal_applicability_state == TemporalApplicabilityState.NO_OVERLAP
    assert partial.temporal_applicability_state == TemporalApplicabilityState.PARTIAL_OVERLAP
    assert "partial temporal overlap" in partial.limitations


def test_open_unknown_superseded_and_expired_interval_handling():
    base = _fixture_by_id("CC1_eligible").record
    open_interval = ComparatorIntervalMetadata("open_interval", "synthetic_comparator", 1, None, open_interval=True)
    unknown_interval = ComparatorIntervalMetadata("unknown_interval", "synthetic_comparator", None, None, unknown_interval=True)

    open_result = evaluate_comparator_construction(_with_comparator_interval(base, open_interval))
    unknown_result = evaluate_comparator_construction(_with_comparator_interval(base, unknown_interval))
    superseded_result = evaluate_comparator_construction(_fixture_by_id("CC13_superseded_interval").record)
    expired_result = evaluate_comparator_construction(_fixture_by_id("CC14_expired_interval").record)

    assert open_result.eligibility_state == ComparatorEligibilityState.COMPARATOR_CONDITIONALLY_ELIGIBLE
    assert "open interval" in open_result.limitations
    assert unknown_result.eligibility_state == ComparatorEligibilityState.INSUFFICIENT_COMPARATOR_EVIDENCE
    assert ComparatorDiagnosticCode.MISSING_COMPARATOR_APPLICABILITY in _diagnostic_codes(unknown_result)
    assert "superseded interval" in superseded_result.limitations
    assert "expired interval" in expired_result.limitations


def test_exclusion_precedence_over_conditional_context():
    base = _fixture_by_id("CC1_eligible").record
    result = evaluate_comparator_construction(
        _base_record(
            relationship=_with_relationship(base, excluded_relationship=True),
            context_support=ComparatorContextSupportMetadata(conditionally_governed=True),
        )
    )

    assert result.eligibility_state == ComparatorEligibilityState.COMPARATOR_EXCLUDED
    assert ComparatorDiagnosticCode.EXCLUDED_COMPARATOR in _diagnostic_codes(result)
    assert "context support conditionally governed" in result.limitations


def test_coverage_context_and_duplicate_metadata_are_preserved():
    coverage = evaluate_comparator_construction(_fixture_by_id("CC16_insufficient_coverage").record)
    context = evaluate_comparator_construction(_fixture_by_id("CC17_insufficient_context").record)
    duplicate = evaluate_comparator_construction(_fixture_by_id("CC18_duplicate_exposure").record)

    assert coverage.coverage.sufficient is False
    assert ComparatorDiagnosticCode.INSUFFICIENT_COMPARATOR_COVERAGE in _diagnostic_codes(coverage)
    assert context.context_support.sufficient is False
    assert ComparatorDiagnosticCode.COMPARATOR_CONTEXT_INSUFFICIENT in _diagnostic_codes(context)
    assert ComparatorDiagnosticCode.DUPLICATE_EXPOSURE_UNRESOLVED in _diagnostic_codes(duplicate)


def test_combined_failure_precedence_and_diagnostic_preservation():
    base = _fixture_by_id("CC1_eligible").record
    no_overlap = ComparatorIntervalMetadata("combined_no_overlap", "synthetic_comparator", 20, 30)
    cases = (
        (
            _with_comparator_interval(
                _base_record(coverage=ComparatorCoverageMetadata(sufficient=False, conditionally_governed=True)),
                no_overlap,
            ),
            ComparatorEligibilityState.COMPARATOR_INELIGIBLE,
            (ComparatorDiagnosticCode.INSUFFICIENT_COMPARATOR_COVERAGE, ComparatorDiagnosticCode.INVALID_TEMPORAL_OVERLAP),
        ),
        (
            _base_record(
                relationship=_with_relationship(base, excluded_relationship=True),
                context_support=ComparatorContextSupportMetadata(sufficient=False, conditionally_governed=True),
            ),
            ComparatorEligibilityState.COMPARATOR_EXCLUDED,
            (ComparatorDiagnosticCode.EXCLUDED_COMPARATOR, ComparatorDiagnosticCode.COMPARATOR_CONTEXT_INSUFFICIENT),
        ),
        (
            _base_record(duplicate_exposure=True, traceability_complete=False),
            ComparatorEligibilityState.COMPARATOR_INELIGIBLE,
            (ComparatorDiagnosticCode.DUPLICATE_EXPOSURE_UNRESOLVED, ComparatorDiagnosticCode.INCOMPLETE_COMPARATOR_TRACEABILITY),
        ),
        (
            _base_record(
                relationship=_with_relationship(base, lineage_unresolved=True),
                coverage=ComparatorCoverageMetadata(sufficient=False),
            ),
            ComparatorEligibilityState.INSUFFICIENT_COMPARATOR_EVIDENCE,
            (ComparatorDiagnosticCode.UNRESOLVED_COMPARATOR_LINEAGE, ComparatorDiagnosticCode.INSUFFICIENT_COMPARATOR_COVERAGE),
        ),
        (
            _base_record(
                relationship=_with_relationship(base, conflicting_relationship=True),
                comparator=type(base.comparator)(
                    base.comparator.identity_id,
                    (),
                    base.comparator.interval,
                    base.comparator.pit_identity_trace,
                ),
            ),
            ComparatorEligibilityState.COMPARATOR_INELIGIBLE,
            (ComparatorDiagnosticCode.CONFLICTING_COMPARATOR, ComparatorDiagnosticCode.MISSING_COMPARATOR_APPLICABILITY),
        ),
        (
            _fixture_by_id("CC13_superseded_interval").record,
            ComparatorEligibilityState.COMPARATOR_CONDITIONALLY_ELIGIBLE,
            (),
        ),
    )

    for record, expected_state, expected_codes in cases:
        result = evaluate_comparator_construction(record)
        assert result.eligibility_state == expected_state
        for expected_code in expected_codes:
            assert expected_code in _diagnostic_codes(result)


def test_information_contract_refuses_prohibited_outputs():
    contract = evaluate_comparator_construction(_fixture_by_id("CC1_eligible").record).information_contract

    assert contract.exposes_raw_source_values is False
    assert contract.exposes_retrieval_instructions is False
    assert contract.performs_authority_evaluation is False
    assert contract.performs_identity_construction is False
    assert contract.performs_identity_resolution is False
    assert contract.ranks_comparators is False
    assert contract.exposes_similarity_scores is False
    assert contract.performs_peer_discovery is False
    assert contract.exposes_contextual_measurements is False
    assert contract.exposes_formulas is False
    assert contract.performs_scientific_interpretation is False
    assert contract.creates_candidates is False
    assert contract.constructs_panels is False
    assert contract.computes_ic is False
    assert contract.runs_validation is False
    assert contract.makes_production_decisions is False
    assert contract.exposes_ml_features is False
    assert contract.exposes_ml_labels is False


def test_result_boundary_flags_remain_false_for_all_fixtures():
    for fixture in canonical_comparator_construction_fixtures():
        result = evaluate_comparator_construction(fixture.record)
        assert result.acquisition_performed is False
        assert result.retrieval_performed is False
        assert result.vendor_integration is False
        assert result.authority_evaluation_performed is False
        assert result.identity_construction is False
        assert result.identity_resolution is False
        assert result.scientific_similarity is False
        assert result.comparator_ranking is False
        assert result.peer_discovery is False
        assert result.contextual_measurement is False
        assert result.formula_execution is False
        assert result.candidate_generation is False
        assert result.panel_generation is False
        assert result.discovery_execution is False
        assert result.validation_execution is False
        assert result.ic_computation is False
        assert result.production_logic is False
        assert result.optimization_performed is False
        assert result.ml_integration is False


def test_inherited_source_authority_and_pit_traces_are_propagated_without_reevaluation():
    source_result = evaluate_source_authority(
        {fixture.fixture_id: fixture for fixture in canonical_source_authority_fixtures()}["SA1_authoritative"].record
    )
    pit_result = evaluate_pit_identity_context(
        {fixture.fixture_id: fixture for fixture in canonical_pit_identity_context_fixtures()}["PIC1_normal_identity"].record
    )
    result = evaluate_comparator_construction(
        _base_record(
            source_authority_trace=source_result.traceability,
            pit_identity_trace=pit_result.traceability,
        )
    )

    assert result.source_authority_trace["source_id"] == "synthetic_source_SA1_authoritative"
    assert result.pit_identity_trace["identity_interval_id"] == "identity_interval_PIC1_normal_identity"
    assert result.authority_evaluation_performed is False
    assert result.identity_construction is False


def test_traceability_contains_reconstructable_comparator_metadata():
    result = evaluate_comparator_construction(_fixture_by_id("CC1_eligible").record)
    trace = result.traceability

    assert trace["layer_name"] == "Project Underdog Phase 5 Comparator Construction"
    assert trace["governing_design"] == "project_underdog_phase5_comparator_construction_implementation_design_v1"
    assert trace["target_identity_id"] == "synthetic_target"
    assert trace["comparator_identity_id"] == "synthetic_comparator"
    assert trace["relationship_id"] == "relationship_CC1_eligible"
    assert result.information_contract.traceability == trace


def test_deterministic_repeated_execution_and_serialization():
    record = _fixture_by_id("CC19_conflicting_relationship").record
    first = evaluate_comparator_construction(record)
    second = evaluate_comparator_construction(record)

    assert first == second
    assert first.stable_json() == second.stable_json()
    assert json.loads(first.stable_json()) == first.to_ordered_dict()


def test_diagnostic_ordering_is_stable_for_combined_failures():
    result = evaluate_comparator_construction(_base_record(duplicate_exposure=True, traceability_complete=False))

    assert _diagnostic_codes(result) == (
        ComparatorDiagnosticCode.DUPLICATE_EXPOSURE_UNRESOLVED,
        ComparatorDiagnosticCode.INCOMPLETE_COMPARATOR_TRACEABILITY,
    )


def test_guardrail_manifest_is_synthetic_only_and_disables_prohibited_operations():
    manifest = comparator_construction_guardrail_manifest()

    assert manifest["synthetic_metadata_only"] is True
    for key, value in manifest.items():
        if key != "synthetic_metadata_only":
            assert value is False


def test_first_module_compatibility_preserves_prepared_observation_boundary():
    comparator_result = evaluate_comparator_construction(_fixture_by_id("CC1_eligible").record)
    first_result = run_first_module_reference(
        {fixture.fixture_id: fixture for fixture in first_module_fixtures()}["F1_common_repair"].module_input
    )

    assert comparator_result.eligibility_state == ComparatorEligibilityState.COMPARATOR_ELIGIBLE
    assert comparator_result.formula_execution is False
    assert first_result.target_repair is not None
    assert first_result.candidate_record is False
    assert first_result.panel_record is False
    assert first_result.validation_input is False
