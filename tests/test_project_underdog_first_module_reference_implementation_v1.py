from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from pipelines.project_underdog_first_module_reference_implementation_v1 import (
    DiagnosticCode,
    FirstModuleInput,
    PostStressState,
    QualitativeRelation,
    RepairObservation,
    TimeBounds,
    ValidityState,
    canonical_fixtures,
    module_guardrail_manifest,
    run_first_module_reference,
)


def _diagnostic_codes(result):
    return tuple(diag.code for diag in result.diagnostics)


def _fixture_by_id(fixture_id: str):
    return {fixture.fixture_id: fixture for fixture in canonical_fixtures()}[fixture_id]


def test_all_canonical_fixtures_execute_with_expected_statuses_and_diagnostics():
    fixtures = canonical_fixtures()
    assert len(fixtures) == 15
    assert len({fixture.fixture_id for fixture in fixtures}) == 15

    for fixture in fixtures:
        result = run_first_module_reference(fixture.module_input)
        assert result.validity_state == fixture.expected_validity_state
        assert result.decomposition_status == fixture.expected_decomposition_status
        for expected_code in fixture.expected_diagnostic_codes:
            assert expected_code in _diagnostic_codes(result)
        assert result.fixture_id == fixture.fixture_id
        assert result.alpha_claim is False
        assert result.candidate_record is False
        assert result.panel_record is False
        assert result.discovery_output is False
        assert result.validation_input is False
        assert result.production_output is False
        assert result.ranking_output is False
        assert result.predictive_output is False


def test_algebraic_consistency_for_valid_fixture_outputs():
    for fixture in canonical_fixtures():
        result = run_first_module_reference(fixture.module_input)
        if result.validity_state == ValidityState.VALID:
            assert result.target_repair is not None
            assert result.peer_common_repair is not None
            assert result.idiosyncratic_repair is not None
            assert result.target_repair == pytest.approx(
                result.peer_common_repair + result.idiosyncratic_repair
            )


def test_equal_peer_common_aggregation_and_direct_idiosyncratic_contrast():
    fixture = _fixture_by_id("F3_mixed_repair")
    result = run_first_module_reference(fixture.module_input)

    assert result.target_repair == 2.0
    assert result.peer_common_repair == 1.0
    assert result.idiosyncratic_repair == 1.0


def test_temporal_failure_prevents_formula_quantities():
    fixture = _fixture_by_id("F8_timing_violation")
    result = run_first_module_reference(fixture.module_input)

    assert result.validity_state == ValidityState.FAIL_CLOSED
    assert DiagnosticCode.TEMPORAL_OVERLAP_OR_REVERSAL in _diagnostic_codes(result)
    assert result.target_repair is None
    assert result.peer_common_repair is None
    assert result.idiosyncratic_repair is None


def test_future_leakage_fails_closed_before_formula_use():
    base = _fixture_by_id("F1_common_repair").module_input
    contaminated = FirstModuleInput(**{**base.__dict__, "future_leakage": True})
    result = run_first_module_reference(contaminated)

    assert result.validity_state == ValidityState.FAIL_CLOSED
    assert DiagnosticCode.FUTURE_LEAKAGE in _diagnostic_codes(result)
    assert result.decomposition_status.value == "unresolved"


def test_comparator_context_unavailable_does_not_default_to_idiosyncratic():
    fixture = _fixture_by_id("F5_comparator_unavailable")
    result = run_first_module_reference(fixture.module_input)

    assert result.validity_state == ValidityState.UNRESOLVED
    assert result.decomposition_status.value == "unresolved"
    assert result.peer_common_repair is None
    assert result.idiosyncratic_repair is None


def test_invalid_identity_and_pit_failures_are_distinct_diagnostics():
    identity_result = run_first_module_reference(_fixture_by_id("F6_invalid_identity").module_input)
    pit_result = run_first_module_reference(_fixture_by_id("F7_pit_violation").module_input)

    assert DiagnosticCode.INVALID_IDENTITY in _diagnostic_codes(identity_result)
    assert DiagnosticCode.INVALID_PIT_STATE in _diagnostic_codes(pit_result)
    assert identity_result.validity_state == ValidityState.UNRESOLVED
    assert pit_result.validity_state == ValidityState.FAIL_CLOSED


def test_governed_missing_comparator_is_excluded_without_imputation():
    base = _fixture_by_id("F1_common_repair").module_input
    missing_peer = base.comparator_observations[0]
    governed_missing = type(missing_peer)(
        RepairObservation(
            entity_id=missing_peer.observation.entity_id,
            repair_value=None,
            missing_governed=True,
            trace_id=missing_peer.observation.trace_id,
        )
    )
    adjusted = FirstModuleInput(
        **{
            **base.__dict__,
            "comparator_observations": (governed_missing, base.comparator_observations[1]),
        }
    )
    result = run_first_module_reference(adjusted)

    assert result.validity_state == ValidityState.VALID
    assert result.peer_common_repair == 1.0
    assert DiagnosticCode.MISSING_COMPARATOR_OBSERVATION in _diagnostic_codes(result)
    assert result.comparator_ids == ("peer_2",)


def test_ungoverned_missing_comparator_fails_closed_to_unresolved():
    base = _fixture_by_id("F1_common_repair").module_input
    missing_peer = base.comparator_observations[0]
    ungoverned_missing = type(missing_peer)(
        RepairObservation(
            entity_id=missing_peer.observation.entity_id,
            repair_value=None,
            missing_governed=False,
            trace_id=missing_peer.observation.trace_id,
        )
    )
    adjusted = FirstModuleInput(
        **{
            **base.__dict__,
            "comparator_observations": (ungoverned_missing, base.comparator_observations[1]),
        }
    )
    result = run_first_module_reference(adjusted)

    assert result.validity_state == ValidityState.UNRESOLVED
    assert DiagnosticCode.MISSING_COMPARATOR_OBSERVATION in _diagnostic_codes(result)
    assert result.peer_common_repair is None


def test_absent_post_stress_context_is_unresolved_not_repaired():
    base = _fixture_by_id("F1_common_repair").module_input
    no_stress = FirstModuleInput(**{**base.__dict__, "post_stress_state": PostStressState.NOT_ELIGIBLE})
    result = run_first_module_reference(no_stress)

    assert result.validity_state == ValidityState.UNRESOLVED
    assert DiagnosticCode.ABSENT_POST_STRESS_CONTEXT in _diagnostic_codes(result)


def test_ambiguous_decomposition_preserves_formula_values_but_unresolved_status():
    result = run_first_module_reference(_fixture_by_id("F4_unresolved_repair").module_input)

    assert result.decomposition_status.value == "unresolved"
    assert result.target_repair is not None
    assert result.peer_common_repair is not None
    assert result.idiosyncratic_repair is not None
    assert DiagnosticCode.AMBIGUOUS_DECOMPOSITION in _diagnostic_codes(result)


def test_traceability_completeness_is_required():
    base = _fixture_by_id("F1_common_repair").module_input
    no_trace = FirstModuleInput(**{**base.__dict__, "traceability_complete": False})
    result = run_first_module_reference(no_trace)

    assert result.validity_state == ValidityState.REJECTED
    assert result.decomposition_status.value == "unresolved"
    assert DiagnosticCode.TRACEABILITY_FAILURE in _diagnostic_codes(result)


def test_result_traceability_contains_required_frozen_stack_fields():
    result = run_first_module_reference(_fixture_by_id("F1_common_repair").module_input)
    trace = result.traceability

    assert trace["module_name"] == "Common-Versus-Idiosyncratic Post-Stress Repair Decomposition"
    assert "project_underdog_first_module_formula_specification_v1" in trace["frozen_specifications"]
    assert "R_i(t)" in trace["accepted_formula_components"]
    assert "peer_common_repair" in trace["accepted_measurement_concepts"]
    assert trace["target_observation"]["entity_id"] == "target_security"
    assert trace["comparator_observations"]


def test_deterministic_repeated_execution_and_serialization():
    fixture = _fixture_by_id("F9_market_wide_repair")
    first = run_first_module_reference(fixture.module_input)
    second = run_first_module_reference(fixture.module_input)

    assert first == second
    assert first.stable_json() == second.stable_json()
    assert json.loads(first.stable_json()) == first.to_ordered_dict()


def test_source_specific_input_is_rejected():
    base = _fixture_by_id("F1_common_repair").module_input
    source_specific = FirstModuleInput(**{**base.__dict__, "source_independent": False})
    result = run_first_module_reference(source_specific)

    assert result.validity_state == ValidityState.REJECTED
    assert DiagnosticCode.SOURCE_SPECIFIC_INPUT in _diagnostic_codes(result)


def test_prohibited_output_roles_are_rejected():
    base = _fixture_by_id("F1_common_repair").module_input
    bad_output = FirstModuleInput(**{**base.__dict__, "requested_output_roles": ("scientific_interpretation", "alpha_score")})
    result = run_first_module_reference(bad_output)

    assert result.validity_state == ValidityState.REJECTED
    assert DiagnosticCode.SOURCE_SPECIFIC_INPUT in _diagnostic_codes(result)
    assert result.alpha_claim is False
    assert result.predictive_output is False


def test_guardrail_manifest_confirms_no_scope_expansion():
    manifest = module_guardrail_manifest()

    assert manifest["source_independent"] is True
    assert manifest["external_data_retrieval"] is False
    assert manifest["real_peer_construction"] is False
    assert manifest["candidate_generation"] is False
    assert manifest["panel_generation"] is False
    assert manifest["ic_computation"] is False
    assert manifest["discovery_executed"] is False
    assert manifest["validation_executed"] is False
    assert manifest["production_logic"] is False
    assert manifest["survivor_status_changed"] is False
    assert manifest["formula_optimization"] is False
    assert manifest["ml_integration"] is False
