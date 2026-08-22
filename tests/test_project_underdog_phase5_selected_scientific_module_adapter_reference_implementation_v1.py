import hashlib
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from pipelines import project_underdog_phase5_selected_scientific_module_adapter_reference_implementation_v1 as ad  # noqa: E402


def _fixtures():
    return {fixture.fixture_id: fixture for fixture in ad.canonical_selected_module_adapter_fixtures()}


def _result(fixture_id):
    return ad.evaluate_selected_module_adapter(_fixtures()[fixture_id].request)


def _codes(result):
    return tuple(diagnostic.code for diagnostic in result.adapter_diagnostics)


def test_exact_adapter_state_inventory():
    assert {state.value for state in ad.SelectedModuleAdapterState} == {
        "SELECTED_MODULE_ADAPTER_COMPATIBLE",
        "SELECTED_MODULE_ADAPTER_CONDITIONALLY_COMPATIBLE",
        "SELECTED_MODULE_ADAPTER_UNRESOLVED",
        "SELECTED_MODULE_ADAPTER_INCOMPATIBLE",
        "SELECTED_MODULE_ADAPTER_EXCLUDED",
        "INSUFFICIENT_SELECTED_MODULE_ADAPTER_EVIDENCE",
    }


def test_exact_frozen_input_state_inventory():
    assert {state.value for state in ad.FrozenModuleInputState} == {
        "FROZEN_MODULE_INPUT_READY",
        "FROZEN_MODULE_INPUT_CONDITIONALLY_READY",
        "FROZEN_MODULE_INPUT_UNRESOLVED",
        "FROZEN_MODULE_INPUT_INCOMPLETE",
        "FROZEN_MODULE_INPUT_EXCLUDED",
        "INSUFFICIENT_FROZEN_MODULE_INPUT_EVIDENCE",
    }


def test_all_canonical_fixtures_match_expected_states_and_diagnostics():
    fixtures = ad.canonical_selected_module_adapter_fixtures()
    assert len(fixtures) == 47
    for fixture in fixtures:
        result = ad.evaluate_selected_module_adapter(fixture.request)
        assert result.adapter_state == fixture.expected_adapter_state, fixture.fixture_id
        assert result.frozen_module_input_state == fixture.expected_frozen_input_state, fixture.fixture_id
        for expected in fixture.expected_diagnostic_codes:
            assert expected in _codes(result), fixture.fixture_id
        for expected_limitation in fixture.expected_limitations:
            assert expected_limitation in result.adapter_limitations, fixture.fixture_id


def test_real_selected_module_cannot_produce_ready_input():
    result = ad.real_selected_module_adapter_result()
    assert result.adapter_state == ad.SelectedModuleAdapterState.INCOMPATIBLE
    assert result.frozen_module_input_state == ad.FrozenModuleInputState.INCOMPLETE
    assert ad.AdapterDiagnosticCode.EXECUTION_NOT_AUTHORIZED in _codes(result)
    assert "REAL_SELECTED_MODULE_EXECUTION_BLOCKED_UPSTREAM" in result.adapter_limitations


def test_synthetic_authorized_input_maps_successfully():
    result = _result("AD04_valid_target_context_comparator")
    assert result.adapter_state == ad.SelectedModuleAdapterState.COMPATIBLE
    assert result.frozen_module_input_state == ad.FrozenModuleInputState.READY
    assert result.adapter_diagnostics == ()


def test_execution_authorization_required_and_non_authorized_states_are_distinct():
    assert _result("AD09_execution_blocked").adapter_state == ad.SelectedModuleAdapterState.INCOMPATIBLE
    assert _result("AD10_execution_unresolved").adapter_state == ad.SelectedModuleAdapterState.UNRESOLVED
    assert _result("AD12_execution_insufficient").adapter_state == ad.SelectedModuleAdapterState.INSUFFICIENT_EVIDENCE
    for fixture_id in ("AD09_execution_blocked", "AD10_execution_unresolved", "AD12_execution_insufficient"):
        assert ad.AdapterDiagnosticCode.EXECUTION_NOT_AUTHORIZED in _codes(_result(fixture_id))


def test_authoritative_chain_required_and_wrong_nonblank_references_fail_closed():
    cases = {
        "AD13_wrong_activation_id": ad.AdapterDiagnosticCode.ACTIVATION_REFERENCE_MISMATCH,
        "AD14_wrong_intake_id": ad.AdapterDiagnosticCode.INTAKE_EVALUATION_REFERENCE_MISMATCH,
        "AD16_wrong_handoff_id": ad.AdapterDiagnosticCode.HANDOFF_REFERENCE_MISMATCH,
        "AD17_wrong_adapter_id": ad.AdapterDiagnosticCode.ADAPTER_REFERENCE_MISMATCH,
        "AD23_wrong_input_contract": ad.AdapterDiagnosticCode.MODULE_INPUT_CONTRACT_REFERENCE_MISMATCH,
    }
    for fixture_id, code in cases.items():
        result = _result(fixture_id)
        assert result.frozen_module_input_state == ad.FrozenModuleInputState.INCOMPLETE
        assert code in _codes(result)


def test_broad_program_cannot_replace_narrow_activation_specification():
    result = _result("AD20_wrong_activation_spec")
    assert result.adapter_state == ad.SelectedModuleAdapterState.EXCLUDED
    assert result.frozen_module_input_state == ad.FrozenModuleInputState.EXCLUDED
    assert ad.AdapterDiagnosticCode.ACTIVATION_SPECIFICATION_REFERENCE_MISMATCH in _codes(result)


def test_no_scientific_transformation_and_guardrail_manifest_refuses_science():
    result = _result("AD42_scientific_transformation_enabled")
    assert result.adapter_state == ad.SelectedModuleAdapterState.INCOMPATIBLE
    assert ad.AdapterDiagnosticCode.SCIENTIFIC_TRANSFORMATION_PROHIBITED in _codes(result)
    assert all(value is False for value in ad.selected_module_adapter_guardrail_manifest().values())


def test_role_preservation_and_prohibited_role_controls():
    prohibited = _result("AD34_prohibited_role")
    assert ad.AdapterDiagnosticCode.PROHIBITED_INFORMATION_ROLE in _codes(prohibited)
    assert ad.AdapterDiagnosticCode.REQUIRED_INFORMATION_ROLE_MISSING in _codes(prohibited)
    missing = _result("AD35_missing_required_role")
    assert ad.AdapterDiagnosticCode.REQUIRED_INFORMATION_ROLE_MISSING in _codes(missing)


def test_temporal_preservation_and_horizon_binding():
    valid = _result("AD04_valid_target_context_comparator")
    assert valid.observation_time_metadata["observation_time"] == 5
    assert valid.information_contract["temporal_metadata_preserved"] is True
    assert valid.temporal_metadata["temporal_alignment_state"] == "fully_aligned"
    horizon = _result("AD22_wrong_frozen_horizon")
    assert ad.AdapterDiagnosticCode.FROZEN_HORIZON_REFERENCE_MISMATCH in _codes(horizon)
    assert _result("AD29_frozen_horizon_version_mismatch").adapter_state == ad.SelectedModuleAdapterState.INCOMPATIBLE


def test_scientific_specification_and_contract_version_checks():
    assert ad.AdapterDiagnosticCode.SCIENTIFIC_SPECIFICATION_REFERENCE_MISMATCH in _codes(_result("AD21_wrong_scientific_spec"))
    for fixture_id, code in {
        "AD24_adapter_version_mismatch": ad.AdapterDiagnosticCode.ADAPTER_VERSION_INCOMPATIBLE,
        "AD25_handoff_version_mismatch": ad.AdapterDiagnosticCode.HANDOFF_CONTRACT_VERSION_INCOMPATIBLE,
        "AD26_input_contract_version_mismatch": ad.AdapterDiagnosticCode.MODULE_INPUT_CONTRACT_VERSION_INCOMPATIBLE,
        "AD27_scientific_spec_version_mismatch": ad.AdapterDiagnosticCode.SCIENTIFIC_SPECIFICATION_VERSION_INCOMPATIBLE,
        "AD28_frozen_activation_version_mismatch": ad.AdapterDiagnosticCode.FROZEN_ACTIVATION_SPECIFICATION_VERSION_INCOMPATIBLE,
        "AD30_role_schema_mismatch": ad.AdapterDiagnosticCode.INFORMATION_ROLE_SCHEMA_VERSION_INCOMPATIBLE,
        "AD31_diagnostic_schema_mismatch": ad.AdapterDiagnosticCode.DIAGNOSTIC_SCHEMA_VERSION_INCOMPATIBLE,
        "AD32_lineage_schema_mismatch": ad.AdapterDiagnosticCode.LINEAGE_SCHEMA_VERSION_INCOMPATIBLE,
        "AD33_repro_schema_mismatch": ad.AdapterDiagnosticCode.REPRODUCIBILITY_SCHEMA_VERSION_INCOMPATIBLE,
    }.items():
        assert code in _codes(_result(fixture_id))


def test_target_context_and_comparator_mapping_preserves_metadata():
    result = _result("AD04_valid_target_context_comparator")
    assert result.target_observation_metadata["target_identity_id"] == "synthetic_target"
    assert len(result.context_attachments) == 1
    assert len(result.comparator_attachments) == 1
    assert result.information_role_bindings[0]["information_role"] == ad.DEFAULT_REQUIRED_ROLE
    assert result.context_attachments[0]["information_role"] == ad.DEFAULT_REQUIRED_ROLE
    assert result.comparator_attachments[0]["information_role"] == ad.DEFAULT_REQUIRED_ROLE


def test_mapping_coverage_and_missingness_behaviors():
    assert ad.AdapterDiagnosticCode.TARGET_MAPPING_INCOMPLETE in _codes(_result("AD36_target_mapping_incomplete"))
    assert ad.AdapterDiagnosticCode.CONTEXT_MAPPING_INCOMPLETE in _codes(_result("AD37_context_mapping_incomplete"))
    assert ad.AdapterDiagnosticCode.COMPARATOR_MAPPING_INCOMPLETE in _codes(_result("AD38_comparator_mapping_incomplete"))
    assert _result("AD46_insufficient_coverage").adapter_state == ad.SelectedModuleAdapterState.INSUFFICIENT_EVIDENCE
    assert ad.AdapterDiagnosticCode.UNACCEPTABLE_MAPPING_MISSINGNESS in _codes(_result("AD47_unacceptable_missingness"))


def test_lineage_reproducibility_and_artifact_absence():
    valid = _result("AD04_valid_target_context_comparator")
    assert valid.artifact_lineage["source_authority_artifact"]
    assert valid.artifact_lineage["pit_artifact"]
    assert valid.artifact_lineage["comparator_artifact"]
    assert valid.artifact_lineage["scientific_execution_artifact"] == ""
    assert valid.artifact_lineage["scientific_output_artifact"] == ""
    assert ad.AdapterDiagnosticCode.ADAPTER_LINEAGE_INCOMPLETE in _codes(_result("AD40_lineage_incomplete"))
    assert ad.AdapterDiagnosticCode.ADAPTER_REPRODUCIBILITY_INCOMPLETE in _codes(_result("AD41_reproducibility_incomplete"))


def test_deterministic_frozen_input_identity_and_repeated_result_equality():
    request = _fixtures()["AD04_valid_target_context_comparator"].request
    first = ad.evaluate_selected_module_adapter(request)
    second = ad.evaluate_selected_module_adapter(request)
    assert first == second
    assert first.stable_json() == second.stable_json()
    assert first.frozen_module_input_id == ad.deterministic_frozen_input_identity(request)


def test_requester_metadata_does_not_affect_identity_but_governance_changes_do():
    base_request = _fixtures()["AD04_valid_target_context_comparator"].request
    with_requester = ad.AdapterEvaluationRequest(
        **{**base_request.__dict__, "requester_metadata": {"operator": "synthetic_user"}}
    )
    changed_horizon = ad.AdapterEvaluationRequest(
        **{
            **base_request.__dict__,
            "frozen_activation_specification": ad._frozen_specification(frozen_horizon_specification_version="v2"),
        }
    )
    assert ad.deterministic_frozen_input_identity(base_request) == ad.deterministic_frozen_input_identity(with_requester)
    assert ad.deterministic_frozen_input_identity(base_request) != ad.deterministic_frozen_input_identity(changed_horizon)


def test_stable_serialization_and_sha256_are_deterministic():
    result = _result("AD04_valid_target_context_comparator")
    payload = result.stable_json()
    assert payload == json.dumps(json.loads(payload), sort_keys=True, separators=(",", ":"))
    assert hashlib.sha256(payload.encode("utf-8")).hexdigest() == hashlib.sha256(result.stable_json().encode("utf-8")).hexdigest()


def test_information_contract_refusal_flags_and_scientific_output_absence():
    result = _result("AD04_valid_target_context_comparator")
    for flag in ad.PROHIBITED_INFORMATION_CONTRACT_FLAGS:
        assert result.information_contract[flag] is False
    for field in (
        "exposes_scientific_execution_artifact",
        "exposes_scientific_result_artifact",
        "exposes_measurement_artifact",
        "exposes_validation_artifact",
        "repair_calculation_performed",
        "decomposition_calculation_performed",
        "formula_execution_performed",
        "signal_generation_performed",
        "factor_generation_performed",
        "candidate_generation_performed",
        "panel_generation_performed",
        "ic_calculation_performed",
        "validation_performed",
        "production_logic_performed",
        "ml_feature_created",
        "model_training_performed",
    ):
        assert getattr(result, field) is False


def test_limitation_ordering_is_deterministic():
    result = _result("AD04_valid_target_context_comparator")
    assert result.adapter_limitations[:5] == (
        "REFERENCE_IMPLEMENTATION_ONLY",
        "SYNTHETIC_ADAPTER_ONLY",
        "SYNTHETIC_AUTHORIZED_EXECUTION_ONLY",
        "REAL_ADAPTER_NOT_PLATFORM_INTEGRATED",
        "REAL_MODULE_EXECUTION_NOT_IMPLEMENTED",
    )


def test_direct_and_raw_bypasses_are_excluded():
    assert _result("AD43_direct_upstream_bypass").adapter_state == ad.SelectedModuleAdapterState.EXCLUDED
    assert _result("AD44_raw_prepared_observation_bypass").adapter_state == ad.SelectedModuleAdapterState.EXCLUDED


def test_combined_failure_diagnostic_accumulation():
    base = _fixtures()["AD04_valid_target_context_comparator"].request
    combined = ad.AdapterEvaluationRequest(
        **{
            **base.__dict__,
            "adapter_registration": ad._adapter_registration(
                adapter_id="wrong_adapter",
                module_input_contract_id="wrong_input_contract",
                scientific_transformation_permitted=True,
            ),
            "target_mapping_complete": False,
            "context_mapping_complete": False,
        }
    )
    result = ad.evaluate_selected_module_adapter(combined)
    for code in (
        ad.AdapterDiagnosticCode.ADAPTER_REFERENCE_MISMATCH,
        ad.AdapterDiagnosticCode.MODULE_INPUT_CONTRACT_REFERENCE_MISMATCH,
        ad.AdapterDiagnosticCode.SCIENTIFIC_TRANSFORMATION_PROHIBITED,
        ad.AdapterDiagnosticCode.TARGET_MAPPING_INCOMPLETE,
        ad.AdapterDiagnosticCode.CONTEXT_MAPPING_INCOMPLETE,
    ):
        assert code in _codes(result)
    assert result.adapter_state == ad.SelectedModuleAdapterState.INCOMPATIBLE


def test_upstream_platform_compatibility_imports_and_real_blocked_behavior():
    result = ad.real_selected_module_adapter_result()
    assert result.execution_authorization_state == "EXECUTION_BLOCKED"
    assert result.frozen_module_input_state != ad.FrozenModuleInputState.READY
    assert ad.po.MODULE_VERSION
    assert ad.smi.MODULE_VERSION
    assert ad.ar.MODULE_VERSION
