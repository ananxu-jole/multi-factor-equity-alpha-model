import hashlib
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from pipelines import project_underdog_phase5_scientific_module_activation_registry_and_execution_authorization_reference_implementation_v1 as ar  # noqa: E402


def _fixtures():
    return {fixture.fixture_id: fixture for fixture in ar.canonical_activation_registry_fixtures()}


def _activation(fixture_id):
    fixture = _fixtures()[fixture_id]
    return ar.evaluate_activation_readiness(
        fixture.activation_declaration,
        fixture.registry_snapshot,
        fixture.prerequisites,
        fixture.version_compatibility,
        fixture.lineage,
        fixture.reproducibility,
    )


def _execution(fixture_id):
    fixture = _fixtures()[fixture_id]
    activation = _activation(fixture_id)
    return ar.evaluate_execution_authorization(
        activation,
        fixture.execution_request,
        fixture.registry_snapshot,
        fixture.duplicate_metadata,
        fixture.lineage,
        fixture.reproducibility,
    )


def _activation_codes(result):
    return tuple(diagnostic.code for diagnostic in result.activation_diagnostics)


def _execution_codes(result):
    return tuple(diagnostic.code for diagnostic in result.authorization_diagnostics)


def _registry_codes(result):
    return tuple(diagnostic.code for diagnostic in result.registry_diagnostics)


def test_exact_activation_execution_and_adapter_state_inventories():
    assert {state.value for state in ar.ModuleActivationState} == {
        "MODULE_REGISTERED",
        "MODULE_ACTIVATION_READY",
        "MODULE_ACTIVATION_CONDITIONALLY_READY",
        "MODULE_ACTIVATION_UNRESOLVED",
        "MODULE_ACTIVATION_BLOCKED",
        "MODULE_ACTIVE",
        "MODULE_SUSPENDED",
        "MODULE_DEACTIVATED",
        "MODULE_RETIRED",
    }
    assert {state.value for state in ar.ExecutionAuthorizationState} == {
        "EXECUTION_AUTHORIZED",
        "EXECUTION_CONDITIONALLY_AUTHORIZED",
        "EXECUTION_UNRESOLVED",
        "EXECUTION_BLOCKED",
        "EXECUTION_EXCLUDED",
        "INSUFFICIENT_EXECUTION_AUTHORIZATION_EVIDENCE",
    }
    assert {state.value for state in ar.AdapterCompatibilityState} == {
        "ADAPTER_COMPATIBLE",
        "ADAPTER_CONDITIONALLY_COMPATIBLE",
        "ADAPTER_UNRESOLVED",
        "ADAPTER_INCOMPATIBLE",
        "ADAPTER_EXCLUDED",
        "INSUFFICIENT_ADAPTER_EVIDENCE",
    }


def test_all_canonical_fixtures_evaluate_with_expected_states_and_diagnostics():
    fixtures = ar.canonical_activation_registry_fixtures()
    assert len(fixtures) == 68
    for fixture in fixtures:
        activation = ar.evaluate_activation_readiness(
            fixture.activation_declaration,
            fixture.registry_snapshot,
            fixture.prerequisites,
            fixture.version_compatibility,
            fixture.lineage,
            fixture.reproducibility,
        )
        assert activation.activation_state == fixture.expected_activation_state, fixture.fixture_id
        for expected in fixture.expected_activation_diagnostics:
            assert expected.value in _activation_codes(activation), fixture.fixture_id
        if fixture.execution_request:
            execution = ar.evaluate_execution_authorization(
                activation,
                fixture.execution_request,
                fixture.registry_snapshot,
                fixture.duplicate_metadata,
                fixture.lineage,
                fixture.reproducibility,
            )
            assert execution.execution_authorization_state == fixture.expected_execution_state, fixture.fixture_id
            for expected in fixture.expected_execution_diagnostics:
                assert expected.value in _execution_codes(execution), fixture.fixture_id


def test_broad_research_program_and_narrow_activation_specification_are_separate():
    registration = ar.selected_module_registration()
    declaration = ar.selected_activation_declaration()
    assert registration.research_program_id == ar.SELECTED_RESEARCH_PROGRAM_ID
    assert declaration.research_program_id == ar.SELECTED_RESEARCH_PROGRAM_ID
    assert registration.activation_specification_id == ar.NARROW_ACTIVATION_SPECIFICATION_ID
    assert declaration.activation_specification_id == ar.NARROW_ACTIVATION_SPECIFICATION_ID
    assert declaration.research_program_id != declaration.activation_specification_id

    mismatch = _activation("ACT05_broad_program_narrow_spec_mismatch")
    assert mismatch.activation_state == ar.ModuleActivationState.MODULE_ACTIVATION_BLOCKED
    assert ar.ActivationDiagnosticCode.RESEARCH_PROGRAM_ACTIVATION_SPECIFICATION_MISMATCH.value in _activation_codes(mismatch)


def test_selected_real_module_remains_blocked_for_correct_scientific_reasons():
    activation, execution = ar.real_selected_module_blocked_result()
    assert activation.activation_state == ar.ModuleActivationState.MODULE_ACTIVATION_BLOCKED
    assert execution.execution_authorization_state == ar.ExecutionAuthorizationState.EXECUTION_BLOCKED
    for code in (
        ar.ActivationDiagnosticCode.SOURCE_AUTHORITY_EVIDENCE_ABSENT,
        ar.ActivationDiagnosticCode.PIT_IDENTITY_CONTEXT_EVIDENCE_ABSENT,
        ar.ActivationDiagnosticCode.COMPARATOR_EVIDENCE_ABSENT,
        ar.ActivationDiagnosticCode.PREPARED_OBSERVATIONS_UNAVAILABLE,
    ):
        assert code.value in _activation_codes(activation)
    assert ar.ExecutionDiagnosticCode.MODULE_NOT_ACTIVE.value in _execution_codes(execution)


def test_synthetic_ready_does_not_auto_activate_and_explicit_activation_is_required():
    ready = _activation("ACT19_activation_ready")
    assert ready.activation_state == ar.ModuleActivationState.MODULE_ACTIVATION_READY
    assert ar.ActivationDiagnosticCode.ACTIVATION_NOT_EXPLICITLY_AUTHORIZED.value not in _activation_codes(ready)

    not_explicit = _activation(
        "ACT23_explicitly_authorized_active"
    )
    assert not_explicit.activation_state == ar.ModuleActivationState.MODULE_ACTIVE

    declaration = ar.selected_activation_declaration(
        requested_activation_state=ar.ModuleActivationState.MODULE_ACTIVE,
        explicit_activation_authorized=False,
    )
    blocked = ar.evaluate_activation_readiness(declaration, ar.registry_snapshot(declaration=declaration))
    assert blocked.activation_state == ar.ModuleActivationState.MODULE_ACTIVATION_BLOCKED
    assert ar.ActivationDiagnosticCode.ACTIVATION_NOT_EXPLICITLY_AUTHORIZED.value in _activation_codes(blocked)


def test_activation_invariant_and_prerequisite_handling_fail_closed():
    for fixture_id, expected_code in {
        "ACT02_missing_module_registration": ar.ActivationDiagnosticCode.MODULE_REGISTRATION_MISSING,
        "ACT06_missing_intake_contract": ar.ActivationDiagnosticCode.INTAKE_CONTRACT_MISSING,
        "ACT07_missing_adapter": ar.ActivationDiagnosticCode.ADAPTER_MISSING,
        "ACT08_missing_input_contract": ar.ActivationDiagnosticCode.MODULE_INPUT_CONTRACT_MISSING,
        "ACT09_missing_output_contract": ar.ActivationDiagnosticCode.MODULE_OUTPUT_CONTRACT_MISSING,
        "ACT10_missing_scientific_specification": ar.ActivationDiagnosticCode.SCIENTIFIC_SPECIFICATION_MISSING,
        "ACT11_missing_frozen_horizon_specification": ar.ActivationDiagnosticCode.FROZEN_HORIZON_SPECIFICATION_MISSING,
        "ACT12_selected_authority_absent": ar.ActivationDiagnosticCode.SOURCE_AUTHORITY_EVIDENCE_ABSENT,
        "ACT13_selected_pit_absent": ar.ActivationDiagnosticCode.PIT_IDENTITY_CONTEXT_EVIDENCE_ABSENT,
        "ACT14_selected_comparator_absent": ar.ActivationDiagnosticCode.COMPARATOR_EVIDENCE_ABSENT,
        "ACT15_selected_prepared_observations_absent": ar.ActivationDiagnosticCode.PREPARED_OBSERVATIONS_UNAVAILABLE,
    }.items():
        result = _activation(fixture_id)
        assert result.activation_state == ar.ModuleActivationState.MODULE_ACTIVATION_BLOCKED
        assert expected_code.value in _activation_codes(result)


def test_policy_binding_version_lineage_reproducibility_and_intervals():
    for fixture_id, expected_code in {
        "ACT30_negative_evidence_policy_missing": ar.ActivationDiagnosticCode.NEGATIVE_EVIDENCE_POLICY_UNRESOLVED,
        "ACT31_falsification_policy_missing": ar.ActivationDiagnosticCode.FALSIFICATION_POLICY_UNRESOLVED,
        "ACT32_contamination_control_unresolved": ar.ActivationDiagnosticCode.CONTAMINATION_CONTROL_UNRESOLVED,
        "ACT33_lineage_incomplete": ar.ActivationDiagnosticCode.ACTIVATION_LINEAGE_INCOMPLETE,
        "ACT34_reproducibility_incomplete": ar.ActivationDiagnosticCode.ACTIVATION_REPRODUCIBILITY_INCOMPLETE,
        "ACT35_version_incompatible": ar.ActivationDiagnosticCode.ACTIVATION_VERSION_INCOMPATIBILITY,
        "ACT27_activation_interval_invalid": ar.ActivationDiagnosticCode.ACTIVATION_EFFECTIVE_INTERVAL_INVALID,
    }.items():
        assert expected_code.value in _activation_codes(_activation(fixture_id))


def test_suspension_deactivation_and_retirement_states_are_distinct():
    assert _activation("ACT24_module_suspended").activation_state == ar.ModuleActivationState.MODULE_SUSPENDED
    assert _activation("ACT25_module_deactivated").activation_state == ar.ModuleActivationState.MODULE_DEACTIVATED
    assert _activation("ACT26_module_retired").activation_state == ar.ModuleActivationState.MODULE_RETIRED
    assert _execution("ACT45_execution_excluded_retired").execution_authorization_state == ar.ExecutionAuthorizationState.EXECUTION_EXCLUDED


def test_execution_requires_active_module_and_accepted_handoff():
    assert _execution("ACT39_execution_authorized_synthetic").execution_authorization_state == ar.ExecutionAuthorizationState.EXECUTION_AUTHORIZED
    assert _execution("ACT42_execution_blocked_module_inactive").execution_authorization_state == ar.ExecutionAuthorizationState.EXECUTION_BLOCKED
    for fixture_id, expected_code in {
        "ACT46_intake_state_not_accepted": ar.ExecutionDiagnosticCode.INTAKE_STATE_NOT_ACCEPTED,
        "ACT47_handoff_incomplete": ar.ExecutionDiagnosticCode.HANDOFF_INCOMPLETE,
        "ACT48_adapter_incompatible": ar.ExecutionDiagnosticCode.ADAPTER_INCOMPATIBLE,
        "ACT56_explicit_execution_authorization_absent": ar.ExecutionDiagnosticCode.EXECUTION_NOT_EXPLICITLY_AUTHORIZED,
    }.items():
        result = _execution(fixture_id)
        assert result.execution_authorization_state == ar.ExecutionAuthorizationState.EXECUTION_BLOCKED
        assert expected_code.value in _execution_codes(result)


def test_adapter_transformation_and_bypass_controls_block_execution():
    for fixture_id, expected_code in {
        "ACT36_scientific_transformation_enabled_in_adapter": ar.ExecutionDiagnosticCode.SCIENTIFIC_TRANSFORMATION_IN_ADAPTER,
        "ACT37_direct_upstream_bypass_permitted": ar.ExecutionDiagnosticCode.DIRECT_UPSTREAM_BYPASS,
        "ACT38_raw_prepared_observation_bypass_permitted": ar.ExecutionDiagnosticCode.RAW_PREPARED_OBSERVATION_BYPASS,
    }.items():
        result = _execution(fixture_id)
        assert result.execution_authorization_state == ar.ExecutionAuthorizationState.EXECUTION_BLOCKED
        assert expected_code.value in _execution_codes(result)


def test_duplicate_rerun_and_supersession_governance():
    assert _execution("ACT53_duplicate_execution").execution_authorization_state == ar.ExecutionAuthorizationState.EXECUTION_BLOCKED
    assert ar.ExecutionDiagnosticCode.DUPLICATE_EXECUTION.value in _execution_codes(_execution("ACT53_duplicate_execution"))
    assert ar.ExecutionDiagnosticCode.CONFLICTING_EXECUTION.value in _execution_codes(_execution("ACT54_conflicting_execution"))
    for fixture_id in ("ACT58_authorized_rerun", "ACT60_corrected_rerun", "ACT61_specification_changed_rerun", "ACT62_horizon_changed_rerun", "ACT63_superseding_execution"):
        assert _execution(fixture_id).execution_authorization_state == ar.ExecutionAuthorizationState.EXECUTION_CONDITIONALLY_AUTHORIZED
    assert ar.ExecutionDiagnosticCode.ACTIVATION_SUPERSEDED.value in _execution_codes(_execution("ACT29_activation_superseded"))


def test_deterministic_execution_identity_is_stable_and_excludes_operational_identity():
    first = ar.execution_request(requesting_execution_identity="operator_a")
    second = ar.execution_request(requesting_execution_identity="operator_b")
    assert ar.deterministic_execution_identity(first) == ar.deterministic_execution_identity(second)

    changed = ar.execution_request(adapter_version="v2")
    assert ar.deterministic_execution_identity(first) != ar.deterministic_execution_identity(changed)
    handoff_changed = ar.execution_request(handoff_contract_id="different_handoff_contract_v1")
    assert ar.deterministic_execution_identity(first) != ar.deterministic_execution_identity(handoff_changed)


def test_stable_serialization_and_repeated_result_equality_same_process():
    result_a = _activation("ACT16_selected_all_real_prerequisites_absent")
    result_b = _activation("ACT16_selected_all_real_prerequisites_absent")
    assert result_a == result_b
    assert result_a.stable_json() == result_b.stable_json()
    assert result_a.stable_json() == json.dumps(result_a.to_dict(), sort_keys=True, separators=(",", ":"))

    execution_a = _execution("ACT39_execution_authorized_synthetic")
    execution_b = _execution("ACT39_execution_authorized_synthetic")
    assert execution_a == execution_b
    assert execution_a.stable_json() == execution_b.stable_json()


def test_separate_process_stable_serialization_hash_is_stable():
    code = (
        "from pipelines import project_underdog_phase5_scientific_module_activation_registry_and_execution_authorization_reference_implementation_v1 as ar;"
        "a,e=ar.real_selected_module_blocked_result();"
        "import hashlib;"
        "print(hashlib.sha256(a.stable_json().encode()).hexdigest())"
    )
    first = subprocess.check_output([sys.executable, "-c", code], cwd=ROOT, text=True).strip()
    second = subprocess.check_output([sys.executable, "-c", code], cwd=ROOT, text=True).strip()
    local = hashlib.sha256(ar.real_selected_module_blocked_result()[0].stable_json().encode()).hexdigest()
    assert first == second == local


def test_diagnostic_and_limitation_ordering_is_deterministic():
    result = _activation("ACT16_selected_all_real_prerequisites_absent")
    assert _activation_codes(result) == (
        ar.ActivationDiagnosticCode.SOURCE_AUTHORITY_EVIDENCE_ABSENT.value,
        ar.ActivationDiagnosticCode.PIT_IDENTITY_CONTEXT_EVIDENCE_ABSENT.value,
        ar.ActivationDiagnosticCode.COMPARATOR_EVIDENCE_ABSENT.value,
        ar.ActivationDiagnosticCode.PREPARED_OBSERVATIONS_UNAVAILABLE.value,
    )
    assert result.activation_limitations == tuple(sorted(result.activation_limitations))

    execution = _execution("ACT54_conflicting_execution")
    assert execution.authorization_limitations == tuple(sorted(execution.authorization_limitations))


def test_artifact_lineage_reproducibility_and_no_scientific_artifacts():
    activation = _activation("ACT39_execution_authorized_synthetic")
    execution = _execution("ACT39_execution_authorized_synthetic")
    assert activation.lineage_metadata.complete()
    assert execution.lineage_metadata.complete()
    assert activation.lineage_metadata.scientific_execution_artifact == ""
    assert activation.lineage_metadata.scientific_output_artifact == ""
    assert execution.lineage_metadata.scientific_execution_artifact == ""
    assert execution.lineage_metadata.scientific_output_artifact == ""
    assert activation.reproducibility_metadata.complete()
    assert execution.reproducibility_metadata.complete()
    assert activation.lineage_metadata.negative_evidence_artifacts_preserved is True


def test_negative_evidence_falsification_and_contamination_metadata_are_bound():
    declaration = ar.selected_activation_declaration()
    assert declaration.negative_evidence_policy == "negative_evidence_preserved_v1"
    assert declaration.falsification_policy == "falsification_policy_bound_v1"
    assert declaration.contamination_control_policy == "contamination_controls_bound_v1"
    assert "negative_evidence" in declaration.negative_evidence_policy
    assert "falsification" in declaration.falsification_policy
    assert "contamination" in declaration.contamination_control_policy


def test_registry_authority_diagnostics():
    for fixture_id, expected_code in {
        "ACT64_duplicate_registry_key": ar.RegistryDiagnosticCode.DUPLICATE_REGISTRY_KEY,
        "ACT65_conflicting_registry_version": ar.RegistryDiagnosticCode.CONFLICTING_REGISTRY_VERSION,
        "ACT66_ambiguous_authoritative_record": ar.RegistryDiagnosticCode.AMBIGUOUS_AUTHORITATIVE_RECORD,
        "ACT67_superseded_record_selected": ar.RegistryDiagnosticCode.SUPERSEDED_RECORD_SELECTED,
        "ACT68_inactive_record_selected": ar.RegistryDiagnosticCode.INACTIVE_RECORD_SELECTED,
    }.items():
        result = _activation(fixture_id)
        assert result.activation_state == ar.ModuleActivationState.MODULE_ACTIVATION_BLOCKED
        assert expected_code.value in _registry_codes(result)


def test_blank_activation_metadata_and_policy_bindings_fail_closed():
    blank_cases = {
        "blank_negative_policy": (
            ar.selected_activation_declaration(negative_evidence_policy=""),
            ar.ActivationDiagnosticCode.NEGATIVE_EVIDENCE_POLICY_UNRESOLVED,
        ),
        "blank_falsification_policy": (
            ar.selected_activation_declaration(falsification_policy=""),
            ar.ActivationDiagnosticCode.FALSIFICATION_POLICY_UNRESOLVED,
        ),
        "blank_contamination_policy": (
            ar.selected_activation_declaration(contamination_control_policy=""),
            ar.ActivationDiagnosticCode.CONTAMINATION_CONTROL_UNRESOLVED,
        ),
        "blank_governing_design_versions": (
            ar.selected_activation_declaration(governing_design_versions=()),
            ar.ActivationDiagnosticCode.ACTIVATION_INVARIANT_INCOMPLETE,
        ),
        "whitespace_research_program": (
            ar.selected_activation_declaration(research_program_id="   "),
            ar.ActivationDiagnosticCode.RESEARCH_PROGRAM_ID_MISSING,
        ),
        "blank_activation_specification_with_broad_program": (
            ar.selected_activation_declaration(activation_specification_id="", research_program_id=ar.SELECTED_RESEARCH_PROGRAM_ID),
            ar.ActivationDiagnosticCode.ACTIVATION_SPECIFICATION_MISSING,
        ),
        "blank_artifact_lineage_requirements": (
            ar.selected_activation_declaration(artifact_lineage_requirements=()),
            ar.ActivationDiagnosticCode.ACTIVATION_LINEAGE_INCOMPLETE,
        ),
        "blank_reproducibility_requirements": (
            ar.selected_activation_declaration(reproducibility_requirements=()),
            ar.ActivationDiagnosticCode.ACTIVATION_REPRODUCIBILITY_INCOMPLETE,
        ),
    }
    for label, (declaration, expected_code) in blank_cases.items():
        result = ar.evaluate_activation_readiness(declaration, ar.registry_snapshot(declaration=declaration))
        assert result.activation_state == ar.ModuleActivationState.MODULE_ACTIVATION_BLOCKED, label
        assert expected_code.value in _activation_codes(result), label


def test_blank_and_inconsistent_execution_metadata_fail_closed():
    active_declaration = ar.selected_activation_declaration(
        requested_activation_state=ar.ModuleActivationState.MODULE_ACTIVE,
        explicit_activation_authorized=True,
    )
    active = ar.evaluate_activation_readiness(active_declaration, ar.registry_snapshot(declaration=active_declaration))
    blank_cases = {
        "blank_activation_id": ({"activation_id": ""}, ar.ExecutionDiagnosticCode.INSUFFICIENT_EXECUTION_EVIDENCE),
        "wrong_activation_id": ({"activation_id": "wrong_activation"}, ar.ExecutionDiagnosticCode.INSUFFICIENT_EXECUTION_EVIDENCE),
        "blank_activation_specification": ({"activation_specification_id": ""}, ar.ExecutionDiagnosticCode.EXECUTION_VERSION_INCOMPATIBILITY),
        "wrong_activation_specification": ({"activation_specification_id": "wrong_specification"}, ar.ExecutionDiagnosticCode.EXECUTION_VERSION_INCOMPATIBILITY),
        "blank_prepared_observation_package": ({"prepared_observation_package_id": ""}, ar.ExecutionDiagnosticCode.HANDOFF_INCOMPLETE),
        "blank_handoff_id_with_complete_flag": ({"handoff_contract_id": "", "handoff_complete": True}, ar.ExecutionDiagnosticCode.HANDOFF_INCOMPLETE),
        "blank_duplicate_policy": ({"duplicate_policy": ""}, ar.ExecutionDiagnosticCode.INSUFFICIENT_EXECUTION_EVIDENCE),
        "blank_intake_evaluation": ({"intake_evaluation_id": ""}, ar.ExecutionDiagnosticCode.HANDOFF_INCOMPLETE),
        "blank_input_contract": ({"module_input_contract_id": ""}, ar.ExecutionDiagnosticCode.EXECUTION_INPUT_CONTRACT_MISSING),
        "blank_output_contract": ({"module_output_contract_id": ""}, ar.ExecutionDiagnosticCode.EXECUTION_OUTPUT_CONTRACT_MISSING),
        "blank_scientific_specification": ({"scientific_specification_id": ""}, ar.ExecutionDiagnosticCode.EXECUTION_SCIENTIFIC_SPECIFICATION_MISSING),
        "blank_frozen_horizon": ({"frozen_horizon_specification_id": ""}, ar.ExecutionDiagnosticCode.EXECUTION_FROZEN_HORIZON_MISSING),
        "whitespace_execution_request": ({"execution_authorization_request_id": "   "}, ar.ExecutionDiagnosticCode.INSUFFICIENT_EXECUTION_EVIDENCE),
        "blank_requesting_identity": ({"requesting_execution_identity": ""}, ar.ExecutionDiagnosticCode.INSUFFICIENT_EXECUTION_EVIDENCE),
        "blank_governing_versions": ({"governing_versions": {}}, ar.ExecutionDiagnosticCode.INSUFFICIENT_EXECUTION_EVIDENCE),
    }
    for label, (overrides, expected_code) in blank_cases.items():
        result = ar.evaluate_execution_authorization(
            active,
            ar.execution_request(explicit_execution_authorized=True, **overrides),
        )
        assert result.execution_authorization_state == ar.ExecutionAuthorizationState.EXECUTION_BLOCKED, label
        assert expected_code.value in _execution_codes(result), label


def test_wrong_nonblank_handoff_chain_references_fail_closed():
    active_declaration = ar.selected_activation_declaration(
        requested_activation_state=ar.ModuleActivationState.MODULE_ACTIVE,
        explicit_activation_authorized=True,
    )
    active = ar.evaluate_activation_readiness(active_declaration, ar.registry_snapshot(declaration=active_declaration))
    cases = {
        "wrong_intake_evaluation": {"intake_evaluation_id": "wrong_intake_eval_v1"},
        "intake_from_another_package": {"intake_evaluation_id": "other_package_intake_eval_v1"},
        "intake_from_another_module": {"intake_evaluation_id": "other_module_intake_eval_v1"},
        "intake_from_another_activation": {"intake_evaluation_id": "other_activation_intake_eval_v1"},
        "wrong_prepared_observation_package": {"prepared_observation_package_id": "wrong_prepared_package_v1"},
        "package_from_another_intake": {"prepared_observation_package_id": "other_intake_prepared_package_v1"},
        "package_from_another_activation": {"prepared_observation_package_id": "other_activation_prepared_package_v1"},
        "package_mismatch_with_valid_handoff": {"prepared_observation_package_id": "valid_handoff_wrong_package_v1"},
        "wrong_handoff_contract": {"handoff_contract_id": "wrong_handoff_v1"},
        "handoff_from_another_intake": {"handoff_contract_id": "other_intake_handoff_v1"},
        "handoff_from_another_module": {"handoff_contract_id": "other_module_handoff_v1"},
        "handoff_from_another_activation": {"handoff_contract_id": "other_activation_handoff_v1"},
        "handoff_mismatch_complete_flag": {"handoff_contract_id": "wrong_complete_handoff_v1", "handoff_complete": True},
    }
    for label, overrides in cases.items():
        result = ar.evaluate_execution_authorization(
            active,
            ar.execution_request(explicit_execution_authorized=True, **overrides),
        )
        assert result.execution_authorization_state == ar.ExecutionAuthorizationState.EXECUTION_BLOCKED, label
        assert ar.ExecutionDiagnosticCode.HANDOFF_INCOMPLETE.value in _execution_codes(result), label


def test_combined_handoff_chain_mismatches_preserve_diagnostics():
    active_declaration = ar.selected_activation_declaration(
        requested_activation_state=ar.ModuleActivationState.MODULE_ACTIVE,
        explicit_activation_authorized=True,
    )
    active = ar.evaluate_activation_readiness(active_declaration, ar.registry_snapshot(declaration=active_declaration))
    cases = {
        "wrong_intake_wrong_package": {"intake_evaluation_id": "wrong_intake", "prepared_observation_package_id": "wrong_package"},
        "wrong_package_wrong_handoff": {"prepared_observation_package_id": "wrong_package", "handoff_contract_id": "wrong_handoff"},
        "wrong_intake_wrong_handoff": {"intake_evaluation_id": "wrong_intake", "handoff_contract_id": "wrong_handoff"},
        "all_three_wrong": {
            "intake_evaluation_id": "wrong_intake",
            "prepared_observation_package_id": "wrong_package",
            "handoff_contract_id": "wrong_handoff",
        },
        "correct_intake_wrong_package_correct_handoff": {"prepared_observation_package_id": "wrong_package"},
        "correct_package_wrong_intake_correct_handoff": {"intake_evaluation_id": "wrong_intake"},
        "correct_intake_package_wrong_handoff": {"handoff_contract_id": "wrong_handoff"},
    }
    for label, overrides in cases.items():
        result = ar.evaluate_execution_authorization(
            active,
            ar.execution_request(explicit_execution_authorized=True, **overrides),
        )
        assert result.execution_authorization_state == ar.ExecutionAuthorizationState.EXECUTION_BLOCKED, label
        codes = _execution_codes(result)
        assert ar.ExecutionDiagnosticCode.HANDOFF_INCOMPLETE.value in codes, label
        if label == "all_three_wrong":
            assert codes.count(ar.ExecutionDiagnosticCode.HANDOFF_INCOMPLETE.value) == 3


def test_matching_alternate_authoritative_handoff_chain_authorizes():
    alternate_lineage = ar.ArtifactLineage(
        intake_evaluation_artifact="alternate_intake_eval_v1",
        prepared_observation_artifact="alternate_prepared_observation_package_v1",
        handoff_artifact="alternate_handoff_contract_v1",
    )
    active_declaration = ar.selected_activation_declaration(
        requested_activation_state=ar.ModuleActivationState.MODULE_ACTIVE,
        explicit_activation_authorized=True,
    )
    active = ar.evaluate_activation_readiness(
        active_declaration,
        ar.registry_snapshot(declaration=active_declaration),
        lineage=alternate_lineage,
    )
    execution = ar.evaluate_execution_authorization(
        active,
        ar.execution_request(
            explicit_execution_authorized=True,
            intake_evaluation_id="alternate_intake_eval_v1",
            prepared_observation_package_id="alternate_prepared_observation_package_v1",
            handoff_contract_id="alternate_handoff_contract_v1",
        ),
    )
    assert execution.execution_authorization_state == ar.ExecutionAuthorizationState.EXECUTION_AUTHORIZED
    assert ar.ExecutionDiagnosticCode.HANDOFF_INCOMPLETE.value not in _execution_codes(execution)

    mismatched = ar.evaluate_execution_authorization(
        active,
        ar.execution_request(
            explicit_execution_authorized=True,
            intake_evaluation_id=ar.DEFAULT_INTAKE_EVALUATION_ID,
            prepared_observation_package_id="alternate_prepared_observation_package_v1",
            handoff_contract_id="alternate_handoff_contract_v1",
        ),
    )
    assert mismatched.execution_authorization_state == ar.ExecutionAuthorizationState.EXECUTION_BLOCKED
    assert ar.ExecutionDiagnosticCode.HANDOFF_INCOMPLETE.value in _execution_codes(mismatched)


def test_registry_fatal_activation_cannot_authorize_execution():
    active_declaration = ar.selected_activation_declaration(
        requested_activation_state=ar.ModuleActivationState.MODULE_ACTIVE,
        explicit_activation_authorized=True,
    )
    duplicate_registration = ar.selected_module_registration()
    registry = ar.registry_snapshot(
        declaration=active_declaration,
        module_registrations=(duplicate_registration, duplicate_registration),
    )
    activation = ar.evaluate_activation_readiness(active_declaration, registry)
    assert activation.activation_state == ar.ModuleActivationState.MODULE_ACTIVATION_BLOCKED
    assert ar.RegistryDiagnosticCode.DUPLICATE_REGISTRY_KEY.value in _registry_codes(activation)

    execution = ar.evaluate_execution_authorization(
        activation,
        ar.execution_request(explicit_execution_authorized=True),
        registry=registry,
    )
    assert execution.execution_authorization_state == ar.ExecutionAuthorizationState.EXECUTION_BLOCKED
    assert ar.ExecutionDiagnosticCode.MODULE_NOT_ACTIVE.value in _execution_codes(execution)
    assert ar.ExecutionDiagnosticCode.INSUFFICIENT_EXECUTION_EVIDENCE.value in _execution_codes(execution)


def test_remediated_combined_failures_preserve_diagnostics():
    active_declaration = ar.selected_activation_declaration(
        requested_activation_state=ar.ModuleActivationState.MODULE_ACTIVE,
        explicit_activation_authorized=True,
    )
    active = ar.evaluate_activation_readiness(active_declaration, ar.registry_snapshot(declaration=active_declaration))

    execution = ar.evaluate_execution_authorization(
        active,
        ar.execution_request(
            explicit_execution_authorized=True,
            activation_id="",
            handoff_contract_id="",
            duplicate_policy="",
            direct_upstream_bypass=True,
            raw_prepared_observation_bypass=True,
        ),
        duplicate_metadata=ar.DuplicateExecutionMetadata(ar.DuplicateExecutionState.CONFLICTING_DUPLICATE),
    )
    assert execution.execution_authorization_state == ar.ExecutionAuthorizationState.EXECUTION_BLOCKED
    for code in (
        ar.ExecutionDiagnosticCode.INSUFFICIENT_EXECUTION_EVIDENCE,
        ar.ExecutionDiagnosticCode.HANDOFF_INCOMPLETE,
        ar.ExecutionDiagnosticCode.DIRECT_UPSTREAM_BYPASS,
        ar.ExecutionDiagnosticCode.RAW_PREPARED_OBSERVATION_BYPASS,
        ar.ExecutionDiagnosticCode.CONFLICTING_EXECUTION,
    ):
        assert code.value in _execution_codes(execution)

    activation = ar.evaluate_activation_readiness(
        ar.selected_activation_declaration(negative_evidence_policy="", governing_design_versions=()),
        ar.registry_snapshot(),
        version_compatibility=ar.VersionCompatibility(adapter_version_compatible=False),
    )
    assert activation.activation_state == ar.ModuleActivationState.MODULE_ACTIVATION_BLOCKED
    for code in (
        ar.ActivationDiagnosticCode.NEGATIVE_EVIDENCE_POLICY_UNRESOLVED,
        ar.ActivationDiagnosticCode.ACTIVATION_INVARIANT_INCOMPLETE,
        ar.ActivationDiagnosticCode.ACTIVATION_VERSION_INCOMPATIBILITY,
        ar.ActivationDiagnosticCode.ADAPTER_VERSION_INCOMPATIBILITY,
    ):
        assert code.value in _activation_codes(activation)


def test_combined_failure_probes_preserve_all_applicable_diagnostics():
    registration = ar.selected_module_registration()
    declaration = ar.selected_activation_declaration()
    active = ar.selected_activation_declaration(
        requested_activation_state=ar.ModuleActivationState.MODULE_ACTIVE,
        explicit_activation_authorized=True,
    )
    combined_cases = [
        ar.evaluate_activation_readiness(declaration, ar.registry_snapshot(registration=None), ar.ActivationPrerequisiteState(source_authority_evidence_ready=False)),
        ar.evaluate_activation_readiness(ar.selected_activation_declaration(activation_specification_id=ar.SELECTED_RESEARCH_PROGRAM_ID), ar.registry_snapshot()),
        ar.evaluate_activation_readiness(ar.selected_activation_declaration(scientific_specification_id="", frozen_horizon_specification_id=""), ar.registry_snapshot()),
        ar.evaluate_activation_readiness(declaration, ar.registry_snapshot(), lineage=ar.ArtifactLineage(source_authority_artifact=""), reproducibility=ar.ReproducibilityMetadata(fixture_identifier="combined", controlled_reference=False)),
        ar.evaluate_activation_readiness(declaration, ar.registry_snapshot(), ar.ActivationPrerequisiteState(contamination_controls_ready=False, negative_evidence_policy_ready=False)),
        ar.evaluate_activation_readiness(declaration, ar.registry_snapshot(), ar.ActivationPrerequisiteState(source_authority_evidence_ready=False, pit_identity_context_evidence_ready=False, comparator_evidence_ready=False, prepared_observations_ready=False, intake_platform_ready=False)),
    ]
    assert ar.ActivationDiagnosticCode.MODULE_REGISTRATION_MISSING.value in _activation_codes(combined_cases[0])
    assert ar.ActivationDiagnosticCode.SOURCE_AUTHORITY_EVIDENCE_ABSENT.value in _activation_codes(combined_cases[0])
    assert ar.ActivationDiagnosticCode.RESEARCH_PROGRAM_ACTIVATION_SPECIFICATION_MISMATCH.value in _activation_codes(combined_cases[1])
    assert ar.ActivationDiagnosticCode.SCIENTIFIC_SPECIFICATION_MISSING.value in _activation_codes(combined_cases[2])
    assert ar.ActivationDiagnosticCode.FROZEN_HORIZON_SPECIFICATION_MISSING.value in _activation_codes(combined_cases[2])
    assert ar.ActivationDiagnosticCode.ACTIVATION_LINEAGE_INCOMPLETE.value in _activation_codes(combined_cases[3])
    assert ar.ActivationDiagnosticCode.ACTIVATION_REPRODUCIBILITY_INCOMPLETE.value in _activation_codes(combined_cases[3])
    assert ar.ActivationDiagnosticCode.CONTAMINATION_CONTROL_UNRESOLVED.value in _activation_codes(combined_cases[4])
    assert ar.ActivationDiagnosticCode.NEGATIVE_EVIDENCE_POLICY_UNRESOLVED.value in _activation_codes(combined_cases[4])

    active_eval = ar.evaluate_activation_readiness(active, ar.registry_snapshot(declaration=active))
    execution_cases = [
        ar.evaluate_execution_authorization(_activation("ACT24_module_suspended"), ar.execution_request(explicit_execution_authorized=True), duplicate_metadata=ar.DuplicateExecutionMetadata(ar.DuplicateExecutionState.EXACT_RERUN)),
        ar.evaluate_execution_authorization(_activation("ACT26_module_retired"), ar.execution_request(explicit_execution_authorized=True)),
        ar.evaluate_execution_authorization(_activation("ACT19_activation_ready"), ar.execution_request(explicit_execution_authorized=True, intake_state="INTAKE_COMPATIBLE")),
        ar.evaluate_execution_authorization(active_eval, ar.execution_request(explicit_execution_authorized=True, direct_upstream_bypass=True)),
        ar.evaluate_execution_authorization(
            ar.evaluate_activation_readiness(active, ar.registry_snapshot(declaration=active, adapter=ar.selected_adapter_registration(scientific_transformation_permitted=True))),
            ar.execution_request(explicit_execution_authorized=True),
        ),
        ar.evaluate_execution_authorization(active_eval, ar.execution_request(explicit_execution_authorized=True, blocking_inherited_diagnostic=True)),
        ar.evaluate_execution_authorization(active_eval, ar.execution_request(explicit_execution_authorized=True, blocking_intake_diagnostic=True)),
        ar.evaluate_execution_authorization(active_eval, ar.execution_request(explicit_execution_authorized=True, raw_prepared_observation_bypass=True)),
        ar.evaluate_execution_authorization(active_eval, ar.execution_request(explicit_execution_authorized=True, direct_upstream_bypass=True, raw_prepared_observation_bypass=True, handoff_complete=False), duplicate_metadata=ar.DuplicateExecutionMetadata(ar.DuplicateExecutionState.CONFLICTING_DUPLICATE)),
    ]
    assert ar.ExecutionDiagnosticCode.MODULE_NOT_ACTIVE.value in _execution_codes(execution_cases[0])
    assert ar.ExecutionDiagnosticCode.DUPLICATE_EXECUTION.value in _execution_codes(execution_cases[0])
    assert execution_cases[1].execution_authorization_state == ar.ExecutionAuthorizationState.EXECUTION_EXCLUDED
    assert ar.ExecutionDiagnosticCode.MODULE_NOT_ACTIVE.value in _execution_codes(execution_cases[2])
    assert ar.ExecutionDiagnosticCode.DIRECT_UPSTREAM_BYPASS.value in _execution_codes(execution_cases[3])
    assert ar.ExecutionDiagnosticCode.SCIENTIFIC_TRANSFORMATION_IN_ADAPTER.value in _execution_codes(execution_cases[4])
    assert ar.ExecutionDiagnosticCode.BLOCKING_INHERITED_DIAGNOSTIC.value in _execution_codes(execution_cases[5])
    assert ar.ExecutionDiagnosticCode.BLOCKING_INTAKE_DIAGNOSTIC.value in _execution_codes(execution_cases[6])
    assert ar.ExecutionDiagnosticCode.RAW_PREPARED_OBSERVATION_BYPASS.value in _execution_codes(execution_cases[7])
    for code in (
        ar.ExecutionDiagnosticCode.DIRECT_UPSTREAM_BYPASS,
        ar.ExecutionDiagnosticCode.RAW_PREPARED_OBSERVATION_BYPASS,
        ar.ExecutionDiagnosticCode.HANDOFF_INCOMPLETE,
        ar.ExecutionDiagnosticCode.CONFLICTING_EXECUTION,
    ):
        assert code.value in _execution_codes(execution_cases[8])


def test_information_contract_refuses_prohibited_outputs():
    activation, execution = ar.real_selected_module_blocked_result()
    for field in (
        "exposes_scientific_measurements",
        "exposes_formulas",
        "exposes_signals",
        "exposes_factors",
        "exposes_candidates",
        "exposes_panels",
        "computes_ic",
        "computes_sharpe",
        "exposes_predictions",
        "exposes_validation_results",
        "makes_portfolio_decisions",
        "makes_production_decisions",
        "exposes_ml_features",
        "exposes_ml_labels",
        "trains_models",
    ):
        assert getattr(activation, field) is False
        assert getattr(execution, field) is False
    assert execution.exposes_scientific_execution_artifact is False
    assert execution.exposes_scientific_output is False
    assert ar.activation_registry_guardrail_manifest() == {
        "creates_scientific_execution_artifact": False,
        "creates_scientific_output_artifact": False,
        "retrieves_data": False,
        "constructs_identity": False,
        "constructs_comparators": False,
        "constructs_prepared_observations": False,
        "recomputes_intake": False,
        "defines_formulas": False,
        "generates_signals": False,
        "generates_factors": False,
        "creates_candidates": False,
        "creates_panels": False,
        "calculates_ic": False,
        "runs_validation": False,
        "makes_production_decisions": False,
        "optimizes": False,
        "introduces_ml": False,
    }


def test_upstream_compatibility_is_metadata_only():
    activation = _activation("ACT39_execution_authorized_synthetic")
    assert activation.registry_references["registry_snapshot_id"] == "synthetic_activation_registry_snapshot_v1"
    assert activation.activation_declaration.intake_contract_id == ar.DEFAULT_INTAKE_CONTRACT_ID
    assert activation.activation_declaration.adapter_id == ar.DEFAULT_ADAPTER_ID
    assert activation.activation_declaration.module_input_contract_id == ar.DEFAULT_INPUT_CONTRACT_ID
    assert activation.activation_declaration.module_output_contract_id == ar.DEFAULT_OUTPUT_CONTRACT_ID
    assert activation.governing_versions["information_role_schema"] == ar.DEFAULT_INFORMATION_ROLE_SCHEMA_VERSION
