from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from pipelines.project_underdog_phase5_source_authority_reference_implementation_v1 import (
    AuthorityState,
    DiagnosticCode,
    SourceAuthorityRecord,
    canonical_source_authority_fixtures,
    evaluate_source_authority,
    source_authority_guardrail_manifest,
)


def _diagnostic_codes(result):
    return tuple(diag.code for diag in result.diagnostics)


def _fixture_by_id(fixture_id: str):
    return {fixture.fixture_id: fixture for fixture in canonical_source_authority_fixtures()}[fixture_id]


def _coverage_limited_record(**overrides):
    base = _fixture_by_id("SA1_authoritative").record
    values = {
        **base.__dict__,
        "coverage_sufficient": False,
        "coverage_conditionally_governed": True,
        "conditional_limitations": ("coverage limited",),
    }
    values.update(overrides)
    return SourceAuthorityRecord(**values)


def test_all_canonical_source_authority_fixtures_match_expected_states_and_diagnostics():
    fixtures = canonical_source_authority_fixtures()
    assert len(fixtures) == 11
    assert len({fixture.fixture_id for fixture in fixtures}) == 11

    for fixture in fixtures:
        result = evaluate_source_authority(fixture.record)
        assert result.authority_state == fixture.expected_authority_state
        assert result.fixture_id == fixture.fixture_id
        for expected_code in fixture.expected_diagnostic_codes:
            assert expected_code in _diagnostic_codes(result)


def test_authoritative_fixture_supports_requested_role_without_limitations():
    result = evaluate_source_authority(_fixture_by_id("SA1_authoritative").record)

    assert result.authority_state == AuthorityState.AUTHORITATIVE
    assert result.supported_roles == ("historical_classification_authority",)
    assert result.unsupported_roles == ()
    assert result.limitations == ()
    assert result.diagnostics == ()


def test_conditionally_acceptable_fixture_preserves_limitations():
    result = evaluate_source_authority(_fixture_by_id("SA2_conditional").record)

    assert result.authority_state == AuthorityState.CONDITIONAL
    assert result.supported_roles == ("historical_classification_authority",)
    assert result.limitations == ("role limited to synthetic 2000-2010 interval",)


def test_diagnostic_only_fixture_does_not_authorize_requested_role():
    result = evaluate_source_authority(_fixture_by_id("SA3_diagnostic_only").record)

    assert result.authority_state == AuthorityState.DIAGNOSTIC_ONLY
    assert result.supported_roles == ()
    assert result.unsupported_roles == ("historical_classification_authority",)
    assert DiagnosticCode.UNSUPPORTED_EVIDENCE in _diagnostic_codes(result)


def test_missing_provenance_fails_closed_to_insufficient_evidence():
    result = evaluate_source_authority(_fixture_by_id("SA7_missing_provenance").record)

    assert result.authority_state == AuthorityState.INSUFFICIENT
    assert DiagnosticCode.MISSING_PROVENANCE in _diagnostic_codes(result)
    assert result.supported_roles == ()


def test_missing_temporal_guarantee_fails_closed():
    result = evaluate_source_authority(_fixture_by_id("SA8_missing_temporal").record)

    assert result.authority_state == AuthorityState.INSUFFICIENT
    assert DiagnosticCode.MISSING_TEMPORAL_GUARANTEE in _diagnostic_codes(result)
    assert result.information_contract.temporal_guarantees.publication_or_availability_supported is False


def test_role_scope_violation_is_rejected():
    result = evaluate_source_authority(_fixture_by_id("SA9_role_scope_violation").record)

    assert result.authority_state == AuthorityState.REJECTED
    assert DiagnosticCode.ROLE_SCOPE_VIOLATION in _diagnostic_codes(result)
    assert result.supported_roles == ()
    assert result.unsupported_roles == ("shares_outstanding_authority",)


def test_unregistered_or_non_synthetic_source_is_rejected_without_retrieval():
    base = _fixture_by_id("SA1_authoritative").record
    non_synthetic_registration = type(base.registration)(
        source_id=base.registration.source_id,
        source_name=base.registration.source_name,
        requested_role=base.registration.requested_role,
        registered_roles=base.registration.registered_roles,
        source_registered=True,
        synthetic_record=False,
    )
    record = SourceAuthorityRecord(**{**base.__dict__, "registration": non_synthetic_registration})
    result = evaluate_source_authority(record)

    assert result.authority_state == AuthorityState.REJECTED
    assert DiagnosticCode.UNAUTHORIZED_SOURCE in _diagnostic_codes(result)
    assert result.external_retrieval_performed is False
    assert result.vendor_integration is False


def test_information_contract_refuses_prohibited_outputs():
    result = evaluate_source_authority(_fixture_by_id("SA1_authoritative").record)
    contract = result.information_contract

    assert contract.exposes_raw_values is False
    assert contract.exposes_retrieval is False
    assert contract.exposes_queries is False
    assert contract.constructs_identity is False
    assert contract.constructs_peers is False
    assert contract.exposes_formulas is False
    assert contract.creates_candidates is False
    assert contract.creates_panels is False
    assert contract.computes_ic is False
    assert contract.runs_validation is False
    assert contract.makes_production_decisions is False
    assert contract.exposes_ml_inputs is False


def test_result_boundary_flags_remain_false_for_all_fixtures():
    for fixture in canonical_source_authority_fixtures():
        result = evaluate_source_authority(fixture.record)
        assert result.external_retrieval_performed is False
        assert result.vendor_integration is False
        assert result.acquisition_performed is False
        assert result.identity_construction is False
        assert result.comparator_construction is False
        assert result.contextual_measurement is False
        assert result.formula_execution is False
        assert result.discovery_execution is False
        assert result.validation_execution is False
        assert result.production_logic is False
        assert result.optimization_performed is False
        assert result.ml_integration is False


def test_traceability_completeness_and_contract_fields():
    result = evaluate_source_authority(_fixture_by_id("SA1_authoritative").record)
    trace = result.traceability

    assert trace["layer_name"] == "Project Underdog Phase 5 Source Authority"
    assert "project_underdog_phase5_source_authority_implementation_design_v1" in trace["frozen_specifications"]
    assert trace["requested_role"] == "historical_classification_authority"
    assert trace["source_id"] == "synthetic_source_SA1_authoritative"
    assert trace["synthetic_record"] is True
    assert trace["authority_evidence_metadata"]["official_definitions"] is True
    assert trace["coverage_sufficient"] is True
    assert trace["revision_reconstructable"] is True
    assert trace["reproducibility_sufficient"] is True
    assert result.information_contract.traceability == trace


def test_incomplete_traceability_is_rejected():
    base = _fixture_by_id("SA1_authoritative").record
    record = SourceAuthorityRecord(**{**base.__dict__, "traceability_complete": False})
    result = evaluate_source_authority(record)

    assert result.authority_state == AuthorityState.REJECTED
    assert DiagnosticCode.TRACEABILITY_INCOMPLETE in _diagnostic_codes(result)


def test_deterministic_repeated_execution_and_serialization():
    record = _fixture_by_id("SA6_conflict").record
    first = evaluate_source_authority(record)
    second = evaluate_source_authority(record)

    assert first == second
    assert first.stable_json() == second.stable_json()
    assert json.loads(first.stable_json()) == first.to_ordered_dict()


def test_contract_mismatch_is_rejected():
    base = _fixture_by_id("SA1_authoritative").record
    record = SourceAuthorityRecord(**{**base.__dict__, "frozen_design_id": "unexpected_design"})
    result = evaluate_source_authority(record)

    assert result.authority_state == AuthorityState.REJECTED
    assert DiagnosticCode.CONTRACT_MISMATCH in _diagnostic_codes(result)


def test_coverage_limitation_plus_revision_failure_is_rejected_with_both_diagnostics():
    record = _coverage_limited_record(revision_reconstructable=False)
    result = evaluate_source_authority(record)

    assert result.authority_state == AuthorityState.REJECTED
    assert result.limitations == ("coverage limited",)
    assert DiagnosticCode.COVERAGE_INSUFFICIENT in _diagnostic_codes(result)
    assert DiagnosticCode.REVISION_UNRECONSTRUCTABLE in _diagnostic_codes(result)
    assert [gate.gate for gate in result.gate_outcomes][-1] == "traceability"


def test_coverage_limitation_plus_reproducibility_failure_is_insufficient_with_both_diagnostics():
    record = _coverage_limited_record(reproducibility_sufficient=False)
    result = evaluate_source_authority(record)

    assert result.authority_state == AuthorityState.INSUFFICIENT
    assert result.limitations == ("coverage limited",)
    assert DiagnosticCode.COVERAGE_INSUFFICIENT in _diagnostic_codes(result)
    assert DiagnosticCode.REPRODUCIBILITY_INSUFFICIENT in _diagnostic_codes(result)
    assert [gate.gate for gate in result.gate_outcomes][-1] == "traceability"


def test_coverage_limitation_plus_unresolved_authority_is_insufficient_with_both_diagnostics():
    record = _coverage_limited_record(unresolved_authority=True)
    result = evaluate_source_authority(record)

    assert result.authority_state == AuthorityState.INSUFFICIENT
    assert result.limitations == ("coverage limited",)
    assert DiagnosticCode.UNRESOLVED_AUTHORITY in _diagnostic_codes(result)
    assert DiagnosticCode.COVERAGE_INSUFFICIENT in _diagnostic_codes(result)
    assert [gate.gate for gate in result.gate_outcomes][-1] == "traceability"


def test_coverage_limitation_plus_traceability_failure_is_rejected_with_both_diagnostics():
    record = _coverage_limited_record(traceability_complete=False)
    result = evaluate_source_authority(record)

    assert result.authority_state == AuthorityState.REJECTED
    assert result.limitations == ("coverage limited",)
    assert DiagnosticCode.COVERAGE_INSUFFICIENT in _diagnostic_codes(result)
    assert DiagnosticCode.TRACEABILITY_INCOMPLETE in _diagnostic_codes(result)
    assert [gate.gate for gate in result.gate_outcomes][-1] == "traceability"


def test_direct_unresolved_authority_is_insufficient():
    base = _fixture_by_id("SA1_authoritative").record
    record = SourceAuthorityRecord(**{**base.__dict__, "unresolved_authority": True})
    result = evaluate_source_authority(record)

    assert result.authority_state == AuthorityState.INSUFFICIENT
    assert DiagnosticCode.UNRESOLVED_AUTHORITY in _diagnostic_codes(result)
    assert result.supported_roles == ()


def test_ungoverned_insufficient_coverage_is_insufficient_not_conditional():
    base = _fixture_by_id("SA1_authoritative").record
    record = SourceAuthorityRecord(**{**base.__dict__, "coverage_sufficient": False})
    result = evaluate_source_authority(record)

    assert result.authority_state == AuthorityState.INSUFFICIENT
    assert DiagnosticCode.COVERAGE_INSUFFICIENT in _diagnostic_codes(result)
    assert result.limitations == ()
    assert result.supported_roles == ()


def test_guardrail_manifest_confirms_no_scope_expansion():
    manifest = source_authority_guardrail_manifest()

    assert manifest["source_independent"] is True
    assert manifest["synthetic_records_only"] is True
    assert manifest["external_data_retrieval"] is False
    assert manifest["vendor_integration"] is False
    assert manifest["acquisition_performed"] is False
    assert manifest["identity_construction"] is False
    assert manifest["comparator_construction"] is False
    assert manifest["contextual_measurement"] is False
    assert manifest["formula_execution"] is False
    assert manifest["candidate_generation"] is False
    assert manifest["panel_generation"] is False
    assert manifest["ic_computation"] is False
    assert manifest["discovery_executed"] is False
    assert manifest["validation_executed"] is False
    assert manifest["production_logic"] is False
    assert manifest["optimization_performed"] is False
    assert manifest["ml_integration"] is False
