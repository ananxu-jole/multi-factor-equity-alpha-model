import hashlib
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from pipelines import project_underdog_phase5_prepared_observations_reference_implementation_v1 as po  # noqa: E402
from pipelines import project_underdog_first_module_reference_implementation_v1 as first_module  # noqa: E402
from pipelines.project_underdog_phase5_scientific_module_intake_reference_implementation_v1 import (
    APPROVED_INFORMATION_ROLES,
    AttachmentRequirement,
    IntakeCompatibilityState,
    IntakeDiagnosticCode,
    ModuleIntakeContract,
    RoleCardinalityRule,
    canonical_scientific_module_intake_fixtures,
    evaluate_scientific_module_intake,
    scientific_module_intake_guardrail_manifest,
    _contract,
    _module,
    _po_result,
    _request,
)  # noqa: E402


def _fixture_by_id(fixture_id):
    return {fixture.fixture_id: fixture for fixture in canonical_scientific_module_intake_fixtures()}[fixture_id]


def _diagnostic_codes(result):
    return tuple(diag.code for diag in result.intake_diagnostics)


def _result(fixture_id):
    return evaluate_scientific_module_intake(_fixture_by_id(fixture_id).request)


def test_all_canonical_scientific_module_intake_fixtures_match_expected_contracts():
    fixtures = canonical_scientific_module_intake_fixtures()
    assert len(fixtures) == 66

    for fixture in fixtures:
        result = evaluate_scientific_module_intake(fixture.request)
        assert result.compatibility_state == fixture.expected_state
        for expected_code in fixture.expected_diagnostic_codes:
            assert expected_code in _diagnostic_codes(result), fixture.fixture_id
        for expected_limitation in fixture.expected_limitations:
            assert expected_limitation in result.intake_limitations, fixture.fixture_id


def test_exact_compatibility_state_inventory_and_no_undocumented_states():
    assert {state.value for state in IntakeCompatibilityState} == {
        "INTAKE_COMPATIBLE",
        "INTAKE_CONDITIONALLY_COMPATIBLE",
        "INTAKE_UNRESOLVED",
        "INTAKE_INCOMPATIBLE",
        "INTAKE_EXCLUDED",
        "INSUFFICIENT_INTAKE_EVIDENCE",
    }
    for fixture in canonical_scientific_module_intake_fixtures():
        result = evaluate_scientific_module_intake(fixture.request)
        assert result.compatibility_state in set(IntakeCompatibilityState)


def test_prepared_observation_structural_readiness_is_not_intake_compatibility():
    missing_role_contract = _contract(required_roles=(po.InformationRole.VALIDATED_ALPHA_INFORMATION.value,))
    request = _request("SMI_structural_ready_missing_role", contract=missing_role_contract)
    assert request.prepared_observation.readiness_state == po.PreparedObservationReadinessState.STRUCTURALLY_READY

    result = evaluate_scientific_module_intake(request)
    assert result.compatibility_state == IntakeCompatibilityState.INCOMPATIBLE
    assert IntakeDiagnosticCode.MISSING_REQUIRED_ROLE in _diagnostic_codes(result)


def test_deterministic_prepared_observation_admission_states():
    cases = {
        "SMI11_excluded_po": IntakeCompatibilityState.EXCLUDED,
        "SMI12_structurally_incomplete_po": IntakeCompatibilityState.INCOMPATIBLE,
        "SMI13_unresolved_po": IntakeCompatibilityState.UNRESOLVED,
        "SMI14_insufficient_po": IntakeCompatibilityState.INSUFFICIENT_EVIDENCE,
        "SMI15_conditional_rejected": IntakeCompatibilityState.INCOMPATIBLE,
        "SMI06_accepted_conditional": IntakeCompatibilityState.CONDITIONALLY_COMPATIBLE,
    }
    for fixture_id, expected_state in cases.items():
        assert _result(fixture_id).compatibility_state == expected_state


def test_exact_information_role_matching_and_prohibited_substitutions():
    assert po.InformationRole.DIAGNOSTIC_INFORMATION.value in APPROVED_INFORMATION_ROLES
    assert _result("SMI25_missing_required_role").compatibility_state == IntakeCompatibilityState.INCOMPATIBLE
    assert _result("SMI26_prohibited_role").compatibility_state == IntakeCompatibilityState.EXCLUDED
    assert _result("SMI27_unsupported_role").compatibility_state == IntakeCompatibilityState.INSUFFICIENT_EVIDENCE
    assert IntakeDiagnosticCode.ROLE_CARDINALITY_MISMATCH in _diagnostic_codes(_result("SMI28_role_cardinality"))
    assert IntakeDiagnosticCode.ROLE_ATTACHMENT_MISMATCH in _diagnostic_codes(_result("SMI29_role_attachment"))

    for fixture_id in (
        "SMI30_diag_alpha_substitution",
        "SMI31_explain_supported_substitution",
        "SMI32_negative_alpha_substitution",
        "SMI33_comparator_target_alpha_substitution",
    ):
        result = _result(fixture_id)
        assert result.compatibility_state == IntakeCompatibilityState.INCOMPATIBLE
        assert IntakeDiagnosticCode.MISSING_REQUIRED_ROLE in _diagnostic_codes(result)


def test_target_context_and_comparator_compatibility_behavior():
    assert IntakeDiagnosticCode.MISSING_TARGET_OBSERVATION in _diagnostic_codes(_result("SMI34_missing_target"))
    assert IntakeDiagnosticCode.UNSUPPORTED_TARGET_OBSERVATION_TYPE in _diagnostic_codes(_result("SMI35_unsupported_target_type"))
    assert IntakeDiagnosticCode.MISSING_REQUIRED_CONTEXT in _diagnostic_codes(_result("SMI36_missing_context"))
    assert _result("SMI37_prohibited_context").compatibility_state == IntakeCompatibilityState.EXCLUDED
    assert IntakeDiagnosticCode.MISSING_REQUIRED_CONTEXT in _diagnostic_codes(_result("SMI38_context_cardinality"))
    assert IntakeDiagnosticCode.CONTEXT_BINDING_CONFLICT in _diagnostic_codes(_result("SMI39_context_conflict"))
    assert IntakeDiagnosticCode.MISSING_REQUIRED_COMPARATOR in _diagnostic_codes(_result("SMI40_missing_comparator"))
    assert _result("SMI41_prohibited_comparator").compatibility_state == IntakeCompatibilityState.EXCLUDED
    assert IntakeDiagnosticCode.MISSING_REQUIRED_COMPARATOR in _diagnostic_codes(_result("SMI42_comparator_cardinality"))
    assert IntakeDiagnosticCode.COMPARATOR_BINDING_CONFLICT in _diagnostic_codes(_result("SMI43_comparator_conflict"))
    assert IntakeDiagnosticCode.COMPARATOR_BINDING_CONFLICT in _diagnostic_codes(_result("SMI44_expired_comparator"))


def test_temporal_coverage_and_missingness_compatibility_behavior():
    assert IntakeDiagnosticCode.TEMPORAL_NON_OVERLAP in _diagnostic_codes(_result("SMI45_temporal_non_overlap"))
    assert _result("SMI46_unknown_temporal").compatibility_state == IntakeCompatibilityState.UNRESOLVED
    assert IntakeDiagnosticCode.UNSUPPORTED_OPEN_INTERVAL in _diagnostic_codes(_result("SMI47_open_interval"))
    assert IntakeDiagnosticCode.UNSUPPORTED_MIXED_FREQUENCY in _diagnostic_codes(_result("SMI48_mixed_frequency"))
    assert IntakeDiagnosticCode.TEMPORAL_INCOMPATIBILITY in _diagnostic_codes(_result("SMI49_discontinuous_identity"))
    assert _result("SMI50_incomplete_temporal_trace").compatibility_state == IntakeCompatibilityState.UNRESOLVED
    assert _result("SMI51_insufficient_target_coverage").compatibility_state == IntakeCompatibilityState.INSUFFICIENT_EVIDENCE
    assert _result("SMI52_insufficient_comparator_coverage").compatibility_state == IntakeCompatibilityState.INSUFFICIENT_EVIDENCE
    assert _result("SMI53_insufficient_context_coverage").compatibility_state == IntakeCompatibilityState.INSUFFICIENT_EVIDENCE
    assert IntakeDiagnosticCode.UNACCEPTABLE_REQUIRED_MISSINGNESS in _diagnostic_codes(_result("SMI54_required_missingness"))


def test_inherited_diagnostics_limitations_and_prohibited_inherited_behavior_are_preserved():
    fatal = _result("SMI58_prohibited_inherited_fatal")
    assert IntakeDiagnosticCode.INHERITED_FATAL_DIAGNOSTIC in _diagnostic_codes(fatal)
    assert any(diag.code == po.PreparedObservationDiagnosticCode.INHERITED_FATAL_UPSTREAM_DIAGNOSTIC for diag in fatal.inherited_diagnostics)

    unresolved = _result("SMI59_inherited_unresolved")
    assert IntakeDiagnosticCode.INHERITED_UNRESOLVED_DIAGNOSTIC in _diagnostic_codes(unresolved)
    assert any(diag.code == po.PreparedObservationDiagnosticCode.UNRESOLVED_TEMPORAL_ALIGNMENT for diag in unresolved.inherited_diagnostics)

    conditional = _result("SMI06_accepted_conditional")
    assert "relationship conditionally governed" in conditional.inherited_limitations
    assert "accepted conditional Prepared Observation" in conditional.intake_limitations


def test_version_compatibility_and_lineage_reproducibility_fail_closed():
    for fixture_id, code in {
        "SMI18_contract_version_mismatch": IntakeDiagnosticCode.INTAKE_CONTRACT_VERSION_MISMATCH,
        "SMI19_module_version_mismatch": IntakeDiagnosticCode.UNKNOWN_MODULE_VERSION,
        "SMI20_po_contract_version_mismatch": IntakeDiagnosticCode.PREPARED_OBSERVATION_CONTRACT_VERSION_MISMATCH,
        "SMI21_role_schema_mismatch": IntakeDiagnosticCode.INFORMATION_ROLE_SCHEMA_VERSION_MISMATCH,
        "SMI22_diagnostic_schema_mismatch": IntakeDiagnosticCode.DIAGNOSTIC_SCHEMA_VERSION_MISMATCH,
        "SMI23_lineage_schema_mismatch": IntakeDiagnosticCode.ARTIFACT_LINEAGE_SCHEMA_VERSION_MISMATCH,
        "SMI24_repro_schema_mismatch": IntakeDiagnosticCode.REPRODUCIBILITY_SCHEMA_VERSION_MISMATCH,
        "SMI55_missing_po_lineage": IntakeDiagnosticCode.MISSING_PREPARED_OBSERVATION_LINEAGE,
        "SMI56_missing_module_lineage": IntakeDiagnosticCode.MISSING_MODULE_LINEAGE,
        "SMI57_incomplete_repro": IntakeDiagnosticCode.INCOMPLETE_REPRODUCIBILITY_METADATA,
    }.items():
        assert code in _diagnostic_codes(_result(fixture_id))


def test_duplicate_supersession_and_bypass_behavior():
    assert _result("SMI60_raw_bypass").compatibility_state == IntakeCompatibilityState.EXCLUDED
    assert _result("SMI61_direct_upstream_bypass").compatibility_state == IntakeCompatibilityState.EXCLUDED
    assert IntakeDiagnosticCode.DUPLICATE_INTAKE_EXPOSURE in _diagnostic_codes(_result("SMI62_duplicate_intake"))
    assert IntakeDiagnosticCode.CONFLICTING_INTAKE_BINDING in _diagnostic_codes(_result("SMI63_conflicting_intake"))
    assert _result("SMI64_superseded_po").compatibility_state == IntakeCompatibilityState.EXCLUDED
    assert _result("SMI65_superseded_optional_context").compatibility_state == IntakeCompatibilityState.CONDITIONALLY_COMPATIBLE
    assert IntakeDiagnosticCode.COMPARATOR_BINDING_CONFLICT in _diagnostic_codes(_result("SMI66_duplicate_comparator"))


def test_combined_failure_precedence_and_diagnostic_accumulation():
    base_package = _po_result("SMI_combined", coverage=po.CoverageMetadata(target_coverage=False))
    request = _request(
        "SMI_combined",
        package=base_package,
        contract=_contract(prohibited_roles=(po.InformationRole.CONTEXTUAL_CONTROL_INFORMATION.value,), required_roles=(po.InformationRole.VALIDATED_ALPHA_INFORMATION.value,)),
        duplicate_intake_exposure=True,
        conflicting_intake_binding=True,
    )
    result = evaluate_scientific_module_intake(request)
    assert result.compatibility_state == IntakeCompatibilityState.EXCLUDED
    for code in (
        IntakeDiagnosticCode.PREPARED_OBSERVATION_INSUFFICIENT,
        IntakeDiagnosticCode.PROHIBITED_ROLE_PRESENT,
        IntakeDiagnosticCode.MISSING_REQUIRED_ROLE,
        IntakeDiagnosticCode.INSUFFICIENT_REQUIRED_COVERAGE,
        IntakeDiagnosticCode.DUPLICATE_INTAKE_EXPOSURE,
        IntakeDiagnosticCode.CONFLICTING_INTAKE_BINDING,
    ):
        assert code in _diagnostic_codes(result)


def test_deterministic_diagnostic_and_limitation_ordering():
    result = _result("SMI06_accepted_conditional")
    assert result.intake_limitations == (
        "accepted conditional Prepared Observation",
        "relationship conditionally governed",
    )

    combined = evaluate_scientific_module_intake(
        _request(
            "SMI_order",
            package=_po_result("SMI_order", incomplete_traceability=True),
            duplicate_intake_exposure=True,
            conflicting_intake_binding=True,
        )
    )
    assert _diagnostic_codes(combined) == (
        IntakeDiagnosticCode.PREPARED_OBSERVATION_STRUCTURALLY_INCOMPLETE,
        IntakeDiagnosticCode.DUPLICATE_INTAKE_EXPOSURE,
        IntakeDiagnosticCode.CONFLICTING_INTAKE_BINDING,
    )


def test_artifact_lineage_reconstructs_upstream_and_intake_artifacts():
    result = _result("SMI05_context_and_comparator")
    lineage = result.artifact_lineage
    assert lineage["source_authority_artifacts"] == ["SA_SMI05_context_and_comparator"]
    assert lineage["pit_identity_context_artifacts"] == ["PIC_SMI05_context_and_comparator"]
    assert lineage["comparator_construction_artifacts"] == ["CC_SMI05_context_and_comparator"]
    assert lineage["prepared_observation_artifact"] == "prepared_observation_artifact_prepared_package_SMI05_context_and_comparator"
    assert lineage["intake_evaluation_artifact"].startswith("intake_artifact_intake_eval_")
    assert lineage["handoff_contract_artifact"].startswith("handoff_contract_intake_eval_")
    assert lineage["scientific_execution_artifact"] == ""
    assert result.information_contract.artifact_lineage == lineage


def test_reproducibility_metadata_and_stable_serialization_are_deterministic():
    request = _fixture_by_id("SMI05_context_and_comparator").request
    first = evaluate_scientific_module_intake(request)
    second = evaluate_scientific_module_intake(request)
    assert first == second
    assert first.stable_json() == second.stable_json()
    assert json.loads(first.stable_json()) == first.to_ordered_dict()
    assert hashlib.sha256(first.stable_json().encode("utf-8")).hexdigest()
    assert first.reproducibility_sufficiency["deterministic_serialization"] is True
    assert first.governing_versions["stable_serialization"] == "stable_json_v1"


def test_handoff_information_contract_is_bounded_and_refuses_scientific_outputs():
    contract = _result("SMI05_context_and_comparator").information_contract
    assert contract.exposes_scientific_result is False
    assert contract.exposes_formula_output is False
    assert contract.creates_signal is False
    assert contract.creates_factor is False
    assert contract.creates_rank is False
    assert contract.creates_score is False
    assert contract.computes_ic is False
    assert contract.computes_sharpe is False
    assert contract.creates_prediction is False
    assert contract.creates_model_feature is False
    assert contract.creates_model_label is False
    assert contract.creates_validation_result is False
    assert contract.makes_production_decision is False


def test_result_guardrail_flags_and_manifest_refuse_prohibited_operations():
    result = _result("SMI05_context_and_comparator")
    flags = {
        key: value
        for key, value in result.to_ordered_dict().items()
        if key.endswith("_performed") or key.endswith("_created")
    }
    assert all(value is False for value in flags.values())

    manifest = scientific_module_intake_guardrail_manifest()
    assert manifest["synthetic_metadata_only"] is True
    assert all(value is False for key, value in manifest.items() if key != "synthetic_metadata_only")


def test_prepared_observations_compatibility_and_upstream_trace_preservation_without_recomputation():
    package = _po_result("SMI_trace")
    result = evaluate_scientific_module_intake(_request("SMI_trace", package=package))
    assert result.inherited_prepared_observation_readiness == package.readiness_state
    assert result.information_contract.inherited_diagnostics == tuple(diag.to_dict() for diag in package.diagnostics)
    assert result.information_contract.inherited_limitations == package.limitations
    assert result.information_contract.artifact_lineage["source_authority_artifacts"] == ["SA_SMI_trace"]
    assert result.information_contract.artifact_lineage["pit_identity_context_artifacts"] == ["PIC_SMI_trace"]
    assert result.information_contract.artifact_lineage["comparator_construction_artifacts"] == ["CC_SMI_trace"]


def test_first_module_conceptual_compatibility_without_retrofit_or_execution_dependency():
    result = _result("SMI05_context_and_comparator")
    assert result.compatibility_state == IntakeCompatibilityState.COMPATIBLE
    assert first_module.MODULE_ID == "project_underdog_first_module_reference_implementation_v1"
    assert result.information_contract.exposes_scientific_result is False
    assert result.information_contract.accepted_target_observation_metadata["target_identity_id"] == "synthetic_target"
    assert result.information_contract.accepted_comparator_attachments
    assert result.formula_execution_performed is False


def test_no_upstream_recomputation_when_prepared_observation_is_supplied():
    package = _po_result("SMI_no_recompute")
    result = evaluate_scientific_module_intake(_request("SMI_no_recompute", package=package))
    assert result.inherited_diagnostics == package.diagnostics
    assert result.inherited_limitations == package.limitations
    assert result.traceability_sufficiency["source_authority_trace_present"] is True
    assert result.traceability_sufficiency["pit_trace_present"] is True
    assert result.traceability_sufficiency["comparator_traces_present"] is True
