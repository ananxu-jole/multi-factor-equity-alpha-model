import json
import subprocess
import sys
from dataclasses import replace
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from pipelines import project_underdog_phase5_selected_scientific_module_adapter_reference_implementation_v1 as ad  # noqa: E402
from pipelines import project_underdog_phase5_selected_scientific_module_scientific_execution_reference_implementation_v1 as se  # noqa: E402


def _fixtures():
    return {fixture.fixture_id: fixture for fixture in se.canonical_scientific_execution_fixtures()}


def _result(fixture_id):
    return se.execute_selected_scientific_module(_fixtures()[fixture_id].request)


def _replace_frozen(frozen_input, **overrides):
    payload = dict(frozen_input.__dict__)
    payload.update(overrides)
    return ad.FrozenModuleInputContract(**payload)


def _synthetic(fixture_id, target=1.0, comparators=(1.0, 1.0), relation="common", **overrides):
    return se._synthetic_frozen_input(fixture_id, target, tuple(comparators), relation, **overrides)


def _execute(frozen_input, fixture_id="direct_probe", **request_overrides):
    return se.execute_selected_scientific_module(
        se.ScientificExecutionRequest(
            frozen_module_input=frozen_input,
            fixture_id=fixture_id,
            **request_overrides,
        )
    )


def test_exact_decomposition_result_inventory():
    assert {state.value for state in se.DecompositionResult} == {
        "common",
        "idiosyncratic",
        "mixed",
        "unresolved",
    }


def test_exact_scientific_execution_state_inventory():
    assert {state.value for state in se.ScientificExecutionState} == {
        "SCIENTIFIC_EXECUTION_COMPLETE",
        "SCIENTIFIC_EXECUTION_UNRESOLVED",
        "SCIENTIFIC_EXECUTION_INCOMPLETE",
        "INSUFFICIENT_SCIENTIFIC_EXECUTION_EVIDENCE",
    }


def test_all_canonical_fixtures_match_expected_states_and_diagnostics():
    fixtures = se.canonical_scientific_execution_fixtures()
    assert len(fixtures) == 23
    for fixture in fixtures:
        result = se.execute_selected_scientific_module(fixture.request)
        assert result.execution_state == fixture.expected_state, fixture.fixture_id
        assert result.decomposition_result == fixture.expected_decomposition_result, fixture.fixture_id
        for expected_code in fixture.expected_diagnostic_codes:
            assert expected_code in result.diagnostics.codes, fixture.fixture_id
        for expected_limitation in fixture.expected_limitations:
            assert expected_limitation in result.limitations.codes, fixture.fixture_id


def test_common_idiosyncratic_and_mixed_formula_quantities_are_exact():
    common = _result("SE01_common")
    assert common.decomposition_result == se.DecompositionResult.COMMON
    assert common.target_repair == 1.0
    assert common.common_component == 1.0
    assert common.idiosyncratic_component == 0.0

    idiosyncratic = _result("SE02_idiosyncratic")
    assert idiosyncratic.decomposition_result == se.DecompositionResult.IDIOSYNCRATIC
    assert idiosyncratic.common_component == 1.0
    assert idiosyncratic.idiosyncratic_component == 1.0

    mixed = _result("SE03_mixed")
    assert mixed.decomposition_result == se.DecompositionResult.MIXED
    assert mixed.common_component == 1.0
    assert mixed.idiosyncratic_component == 0.5


def test_unresolved_preserves_negative_evidence_and_no_formula_promotion():
    result = _result("SE04_unresolved")
    assert result.decomposition_result == se.DecompositionResult.UNRESOLVED
    assert result.execution_state == se.ScientificExecutionState.INSUFFICIENT_EVIDENCE
    assert "UNRESOLVED_DECOMPOSITION" in result.limitations.codes
    assert "INSUFFICIENT_SCIENTIFIC_EVIDENCE" in result.limitations.codes
    assert se.ScientificExecutionDiagnosticCode.DECOMPOSITION_UNRESOLVED in result.diagnostics.codes


def test_missing_frozen_input_fails_closed():
    result = _result("SE05_missing_frozen_input")
    assert result.execution_state == se.ScientificExecutionState.INCOMPLETE
    assert result.decomposition_result == se.DecompositionResult.UNRESOLVED
    assert se.ScientificExecutionDiagnosticCode.FROZEN_INPUT_MISSING in result.diagnostics.codes
    assert result.common_component is None
    assert result.idiosyncratic_component is None


def test_frozen_spec_horizon_and_scientific_spec_mismatches_fail_closed():
    assert se.ScientificExecutionDiagnosticCode.FROZEN_ACTIVATION_SPECIFICATION_MISMATCH in _result("SE06_frozen_spec_mismatch").diagnostics.codes
    assert se.ScientificExecutionDiagnosticCode.FROZEN_HORIZON_MISMATCH in _result("SE07_frozen_horizon_mismatch").diagnostics.codes
    assert se.ScientificExecutionDiagnosticCode.SCIENTIFIC_SPECIFICATION_MISMATCH in _result("SE08_scientific_spec_mismatch").diagnostics.codes
    for fixture_id in ("SE06_frozen_spec_mismatch", "SE07_frozen_horizon_mismatch", "SE08_scientific_spec_mismatch"):
        assert _result(fixture_id).decomposition_result == se.DecompositionResult.UNRESOLVED


def test_lineage_and_reproducibility_failures_block_ready_output():
    lineage = _result("SE09_lineage_failure")
    repro = _result("SE10_reproducibility_failure")
    assert se.ScientificExecutionDiagnosticCode.LINEAGE_INCOMPLETE in lineage.diagnostics.codes
    assert se.ScientificExecutionDiagnosticCode.REPRODUCIBILITY_INCOMPLETE in repro.diagnostics.codes
    assert lineage.execution_state == se.ScientificExecutionState.INCOMPLETE
    assert repro.execution_state == se.ScientificExecutionState.INCOMPLETE


def test_precondition_failures_do_not_compute_partial_formula_quantities():
    for fixture_id in (
        "SE11_post_stress_unresolved",
        "SE12_insufficient_comparator_evidence",
        "SE13_missing_target_repair",
        "SE14_missing_comparator_repair",
    ):
        result = _result(fixture_id)
        assert result.decomposition_result == se.DecompositionResult.UNRESOLVED
        assert result.common_component is None
        assert result.idiosyncratic_component is None


def test_combined_failures_accumulate_deterministically():
    result = _result("SE15_combined_failures")
    for code in (
        se.ScientificExecutionDiagnosticCode.FROZEN_ACTIVATION_SPECIFICATION_MISMATCH,
        se.ScientificExecutionDiagnosticCode.FROZEN_HORIZON_MISMATCH,
        se.ScientificExecutionDiagnosticCode.SCIENTIFIC_SPECIFICATION_MISMATCH,
        se.ScientificExecutionDiagnosticCode.LINEAGE_INCOMPLETE,
        se.ScientificExecutionDiagnosticCode.REPRODUCIBILITY_INCOMPLETE,
        se.ScientificExecutionDiagnosticCode.POST_STRESS_CONTEXT_UNRESOLVED,
        se.ScientificExecutionDiagnosticCode.TARGET_REPAIR_UNAVAILABLE,
        se.ScientificExecutionDiagnosticCode.INSUFFICIENT_COMPARATOR_EVIDENCE,
        se.ScientificExecutionDiagnosticCode.DECOMPOSITION_RELATION_UNAVAILABLE,
    ):
        assert code in result.diagnostics.codes
    assert result.diagnostics.codes == tuple(sorted(result.diagnostics.codes, key=lambda code: code.value))


def test_formula_version_substitution_and_upstream_scientific_output_are_rejected():
    assert se.ScientificExecutionDiagnosticCode.FORMULA_VERSION_MISMATCH in _result("SE16_formula_version_mismatch").diagnostics.codes
    assert se.ScientificExecutionDiagnosticCode.PROHIBITED_UPSTREAM_OUTPUT in _result("SE17_prohibited_upstream_output").diagnostics.codes
    assert se.ScientificExecutionDiagnosticCode.SCIENTIFIC_EXECUTION_FORMULA_BINDING_MISMATCH in _result("SE19_formula_registration_spoofing").diagnostics.codes


def test_execution_identity_and_stable_json_are_deterministic():
    fixture = _fixtures()["SE18_deterministic_repeat"]
    first = se.execute_selected_scientific_module(fixture.request)
    second = se.execute_selected_scientific_module(fixture.request)
    assert first == second
    assert first.scientific_execution_id == second.scientific_execution_id
    assert first.stable_json() == second.stable_json()
    assert json.loads(first.stable_json()) == json.loads(second.stable_json())


def test_execution_identity_sensitivity_and_operational_metadata_exclusion():
    base = _synthetic("identity_sensitivity", target=1.0, comparators=(1.0,), relation="common")
    base_request = se.ScientificExecutionRequest(
        frozen_module_input=base,
        fixture_id="identity_sensitivity",
        requester_metadata={"operator": "first"},
    )
    base_result = se.execute_selected_scientific_module(base_request)
    metadata_only = se.execute_selected_scientific_module(replace(base_request, requester_metadata={"operator": "second"}))
    assert base_result.scientific_execution_id == metadata_only.scientific_execution_id

    different_frozen_input = se.execute_selected_scientific_module(
        replace(
            base_request,
            frozen_module_input=_replace_frozen(base, frozen_module_input_id="different_frozen_module_input_id"),
        )
    )
    scientific_spec = se.execute_selected_scientific_module(
        replace(base_request, frozen_module_input=_replace_frozen(base, scientific_specification_version="v2"))
    )
    horizon = se.execute_selected_scientific_module(
        replace(base_request, frozen_module_input=_replace_frozen(base, frozen_horizon_specification_version="v2"))
    )
    activation = se.execute_selected_scientific_module(
        replace(base_request, frozen_module_input=_replace_frozen(base, activation_specification_version="v2"))
    )
    formula = se.execute_selected_scientific_module(replace(base_request, requested_formula_version="formula_v2"))
    for result in (different_frozen_input, scientific_spec, horizon, activation, formula):
        assert result.scientific_execution_id != base_result.scientific_execution_id


def test_separate_process_stable_serialization_is_identical():
    code = (
        "from pipelines import project_underdog_phase5_selected_scientific_module_scientific_execution_reference_implementation_v1 as se;"
        "fixtures={f.fixture_id:f for f in se.canonical_scientific_execution_fixtures()};"
        "print(se.execute_selected_scientific_module(fixtures['SE18_deterministic_repeat'].request).stable_json())"
    )
    first = subprocess.check_output([sys.executable, "-c", code], cwd=ROOT, text=True)
    second = subprocess.check_output([sys.executable, "-c", code], cwd=ROOT, text=True)
    assert first == second


def test_information_contract_and_refusal_flags_exclude_downstream_outputs():
    result = _result("SE01_common")
    assert result.information_contract.exposes_decomposition_result is True
    assert result.information_contract.exposes_common_component is True
    assert result.information_contract.exposes_idiosyncratic_component is True
    for field in (
        "exposes_alpha",
        "exposes_prediction",
        "exposes_ranking",
        "exposes_candidate",
        "exposes_portfolio",
        "computes_ic",
        "performs_validation",
        "performs_regression",
        "performs_residualization",
        "performs_optimization",
        "supports_production",
        "ml_feature_created",
        "ml_label_created",
        "model_training_performed",
    ):
        assert getattr(result.information_contract, field) is False
    assert result.alpha_claim is False
    assert result.prediction_created is False
    assert result.ranking_created is False
    assert result.candidate_created is False
    assert result.portfolio_created is False
    assert result.ic_calculation_performed is False
    assert result.validation_performed is False
    assert result.production_logic_performed is False
    assert result.optimization_performed is False
    assert result.ml_feature_created is False
    assert result.ml_label_created is False
    assert result.model_training_performed is False


def test_lineage_chain_preserves_upstream_and_adds_only_execution_and_result():
    result = _result("SE01_common")
    assert result.lineage.lineage_chain == se.LINEAGE_CHAIN
    for key in se.UPSTREAM_LINEAGE_KEYS:
        assert result.lineage.upstream_artifacts[key]
    assert result.lineage.scientific_execution_artifact == result.scientific_execution_id
    assert result.lineage.scientific_result_artifact
    assert result.lineage.validation_artifact == ""
    assert result.lineage.candidate_artifact == ""
    assert result.lineage.panel_artifact == ""
    assert result.lineage.production_artifact == ""
    assert result.lineage.ml_artifact == ""


def test_reproducibility_metadata_carries_required_versions():
    result = _result("SE01_common")
    repro = result.reproducibility
    assert repro.execution_version == se.MODULE_VERSION
    assert repro.formula_version == se.FORMULA_VERSION
    assert repro.scientific_specification_version == ad.DEFAULT_SCIENTIFIC_SPECIFICATION_VERSION
    assert repro.frozen_activation_specification_version == ad.NARROW_ACTIVATION_SPECIFICATION_VERSION
    assert repro.frozen_horizon_version == ad.DEFAULT_FROZEN_HORIZON_SPECIFICATION_VERSION
    assert repro.serialization_version == se.STABLE_SERIALIZATION_VERSION
    assert repro.reproducibility_schema_version == se.REPRODUCIBILITY_SCHEMA_VERSION
    assert repro.deterministic_execution_identity == result.scientific_execution_id


def test_execution_consumes_public_frozen_input_without_upstream_recomputation():
    fixture = _fixtures()["SE01_common"]
    assert isinstance(fixture.request.frozen_module_input, ad.FrozenModuleInputContract)
    result = se.execute_selected_scientific_module(fixture.request)
    assert result.identity.frozen_module_input_id == fixture.request.frozen_module_input.frozen_module_input_id
    assert fixture.request.frozen_module_input.source_retrieval_performed is False
    assert fixture.request.frozen_module_input.authority_evaluation_performed is False
    assert fixture.request.frozen_module_input.pit_construction_performed is False
    assert fixture.request.frozen_module_input.comparator_construction_performed is False
    assert fixture.request.frozen_module_input.prepared_observation_construction_performed is False


def test_guardrail_manifest_prohibits_out_of_scope_capabilities():
    manifest = se.scientific_execution_guardrail_manifest()
    assert manifest
    assert all(value is False for value in manifest.values())


def test_adapter_ready_input_remains_structural_without_formula_metadata():
    ready_adapter_fixtures = {fixture.fixture_id: fixture for fixture in ad.canonical_selected_module_adapter_fixtures()}
    frozen_input = ad.evaluate_selected_module_adapter(ready_adapter_fixtures["AD04_valid_target_context_comparator"].request)
    result = se.execute_selected_scientific_module(se.ScientificExecutionRequest(frozen_module_input=frozen_input))
    assert result.decomposition_result == se.DecompositionResult.UNRESOLVED
    assert se.ScientificExecutionDiagnosticCode.DECOMPOSITION_RELATION_UNAVAILABLE in result.diagnostics.codes
    assert se.ScientificExecutionDiagnosticCode.TARGET_REPAIR_UNAVAILABLE in result.diagnostics.codes
    assert se.ScientificExecutionDiagnosticCode.COMPARATOR_REPAIR_UNAVAILABLE in result.diagnostics.codes


def test_authoritative_formula_registration_succeeds_and_spoofed_registration_fails_closed():
    valid = _execute(_synthetic("valid_authoritative_formula"), fixture_id="valid_authoritative_formula")
    assert valid.execution_state == se.ScientificExecutionState.COMPLETE
    assert valid.decomposition_result == se.DecompositionResult.COMMON

    spoofed_registration = se.ScientificExecutionRegistration(formula_version="formula_v2")
    spoofed = _execute(
        _synthetic("spoofed_formula_registration"),
        fixture_id="spoofed_formula_registration",
        registration=spoofed_registration,
        requested_formula_version="formula_v2",
    )
    assert spoofed.execution_state == se.ScientificExecutionState.INCOMPLETE
    assert spoofed.decomposition_result == se.DecompositionResult.UNRESOLVED
    assert se.ScientificExecutionDiagnosticCode.SCIENTIFIC_EXECUTION_FORMULA_BINDING_MISMATCH in spoofed.diagnostics.codes
    assert spoofed.common_component is None
    assert spoofed.idiosyncratic_component is None


def test_blank_whitespace_wrong_and_alternate_formula_versions_fail_closed():
    for version in ("", "   ", "formula_v2", "project_underdog_first_module_alternate_formula_v1"):
        result = _execute(
            _synthetic(f"formula_version_{version!r}"),
            fixture_id=f"formula_version_{version!r}",
            requested_formula_version=version,
        )
        assert result.execution_state == se.ScientificExecutionState.INCOMPLETE
        assert result.decomposition_result == se.DecompositionResult.UNRESOLVED
        assert se.ScientificExecutionDiagnosticCode.FORMULA_VERSION_MISMATCH in result.diagnostics.codes
        assert se.ScientificExecutionDiagnosticCode.SCIENTIFIC_EXECUTION_FORMULA_BINDING_MISMATCH in result.diagnostics.codes


def test_frozen_formula_metadata_mismatch_fails_closed_when_supplied():
    target_metadata = dict(_synthetic("formula_metadata_base").target_observation_metadata)
    target_metadata["formula_specification_id"] = se.FORMULA_SPECIFICATION_ID
    target_metadata["formula_version"] = "wrong_formula_version"
    result = _execute(
        _replace_frozen(_synthetic("formula_metadata_mismatch"), target_observation_metadata=target_metadata),
        fixture_id="formula_metadata_mismatch",
    )
    assert result.execution_state == se.ScientificExecutionState.INCOMPLETE
    assert result.decomposition_result == se.DecompositionResult.UNRESOLVED
    assert se.ScientificExecutionDiagnosticCode.SCIENTIFIC_EXECUTION_FORMULA_BINDING_MISMATCH in result.diagnostics.codes


def test_formula_correct_with_wrong_scientific_spec_activation_or_horizon_fails_closed():
    cases = (
        _synthetic("correct_formula_wrong_scientific_spec", scientific_specification_id="wrong_scientific_spec"),
        _synthetic("correct_formula_wrong_activation_spec", activation_specification_id="wrong_activation_spec"),
        _synthetic("correct_formula_wrong_horizon", frozen_horizon_specification_id="wrong_horizon"),
    )
    expected_codes = (
        se.ScientificExecutionDiagnosticCode.SCIENTIFIC_SPECIFICATION_MISMATCH,
        se.ScientificExecutionDiagnosticCode.FROZEN_ACTIVATION_SPECIFICATION_MISMATCH,
        se.ScientificExecutionDiagnosticCode.FROZEN_HORIZON_MISMATCH,
    )
    for frozen_input, expected_code in zip(cases, expected_codes):
        result = _execute(frozen_input, fixture_id=expected_code.value)
        assert result.execution_state == se.ScientificExecutionState.INCOMPLETE
        assert result.decomposition_result == se.DecompositionResult.UNRESOLVED
        assert expected_code in result.diagnostics.codes


def test_valid_target_and_comparator_roles_execute_normally():
    frozen_input = _synthetic("valid_target_and_comparator_roles")
    target_metadata = dict(frozen_input.target_observation_metadata)
    target_metadata["information_role"] = ad.DEFAULT_REQUIRED_ROLE
    frozen_input = _replace_frozen(frozen_input, target_observation_metadata=target_metadata)
    result = _execute(frozen_input, fixture_id="valid_target_and_comparator_roles")
    assert result.execution_state == se.ScientificExecutionState.COMPLETE
    assert result.decomposition_result == se.DecompositionResult.COMMON
    assert result.diagnostics.codes == ()


def test_target_role_substitutions_fail_closed():
    invalid_roles = (
        "DIAGNOSTIC_INFORMATION",
        "EXPLANATORY_ONLY_INFORMATION",
        "NEGATIVE_INFORMATION",
        "COMPARATOR_OR_BENCHMARK_INFORMATION",
        "CONTEXTUAL_CONTROL_INFORMATION",
        "UNKNOWN_INFORMATION_ROLE",
        ad.DEFAULT_REQUIRED_ROLE.lower(),
        f" {ad.DEFAULT_REQUIRED_ROLE} ",
    )
    for role in invalid_roles:
        frozen_input = _synthetic(f"invalid_target_role_{role}")
        target_metadata = dict(frozen_input.target_observation_metadata)
        target_metadata["information_role"] = role
        result = _execute(
            _replace_frozen(frozen_input, target_observation_metadata=target_metadata),
            fixture_id=f"invalid_target_role_{role}",
        )
        assert result.execution_state == se.ScientificExecutionState.INCOMPLETE
        assert result.decomposition_result == se.DecompositionResult.UNRESOLVED
        assert se.ScientificExecutionDiagnosticCode.SCIENTIFIC_EXECUTION_ROLE_BINDING_MISMATCH in result.diagnostics.codes
        assert result.common_component is None
        assert result.idiosyncratic_component is None


def test_comparator_role_substitutions_fail_closed():
    invalid_roles = (
        "DIAGNOSTIC_INFORMATION",
        "EXPLANATORY_ONLY_INFORMATION",
        "NEGATIVE_INFORMATION",
        "synthetic_target_observation",
        "UNKNOWN_INFORMATION_ROLE",
        ad.DEFAULT_REQUIRED_ROLE.lower(),
        f" {ad.DEFAULT_REQUIRED_ROLE} ",
    )
    for role in invalid_roles:
        frozen_input = _synthetic(f"invalid_comparator_role_{role}")
        comparator_attachments = tuple({**attachment, "information_role": role} for attachment in frozen_input.comparator_attachments)
        result = _execute(
            _replace_frozen(frozen_input, comparator_attachments=comparator_attachments),
            fixture_id=f"invalid_comparator_role_{role}",
        )
        assert result.execution_state == se.ScientificExecutionState.INCOMPLETE
        assert result.decomposition_result == se.DecompositionResult.UNRESOLVED
        assert se.ScientificExecutionDiagnosticCode.SCIENTIFIC_EXECUTION_ROLE_BINDING_MISMATCH in result.diagnostics.codes


def test_information_role_binding_unknown_alias_and_prohibited_roles_fail_closed():
    invalid_binding_sets = (
        ({"information_role": "UNKNOWN_INFORMATION_ROLE"},),
        ({"information_role": ad.DEFAULT_REQUIRED_ROLE.lower()},),
        ({"information_role": f" {ad.DEFAULT_REQUIRED_ROLE} "},),
        ({"information_role": ad.DEFAULT_REQUIRED_ROLE}, {"information_role": "NEGATIVE_INFORMATION"}),
        ({"information_role": "DIAGNOSTIC_INFORMATION"}, {"information_role": "NEGATIVE_INFORMATION"}),
    )
    for bindings in invalid_binding_sets:
        result = _execute(
            _synthetic(f"invalid_bindings_{len(bindings)}", information_role_bindings=bindings),
            fixture_id=f"invalid_bindings_{len(bindings)}",
        )
        assert result.execution_state == se.ScientificExecutionState.INCOMPLETE
        assert result.decomposition_result == se.DecompositionResult.UNRESOLVED
        assert (
            se.ScientificExecutionDiagnosticCode.SCIENTIFIC_EXECUTION_PROHIBITED_ROLE in result.diagnostics.codes
            or se.ScientificExecutionDiagnosticCode.SCIENTIFIC_EXECUTION_ROLE_BINDING_MISMATCH in result.diagnostics.codes
        )


def test_hand_mutated_ready_frozen_input_with_invalid_role_fails_closed_before_formula():
    frozen_input = _synthetic(
        "hand_mutated_ready_invalid_role",
        information_role_bindings=({"information_role": ad.DEFAULT_REQUIRED_ROLE}, {"information_role": "PROHIBITED"}),
    )
    assert frozen_input.frozen_module_input_state == ad.FrozenModuleInputState.READY
    result = _execute(frozen_input, fixture_id="hand_mutated_ready_invalid_role")
    assert result.execution_state == se.ScientificExecutionState.INCOMPLETE
    assert result.decomposition_result == se.DecompositionResult.UNRESOLVED
    assert se.ScientificExecutionDiagnosticCode.SCIENTIFIC_EXECUTION_PROHIBITED_ROLE in result.diagnostics.codes
    assert result.common_component is None
    assert result.idiosyncratic_component is None


def test_combined_formula_role_lineage_and_repro_failures_accumulate():
    base = _synthetic(
        "combined_formula_role_lineage_repro",
        information_role_bindings=({"information_role": "NEGATIVE_INFORMATION"},),
    )
    bad_lineage = dict(base.artifact_lineage)
    bad_lineage["source_authority_artifact"] = ""
    bad_repro = dict(base.reproducibility_metadata)
    bad_repro["controlled_reference"] = ""
    spoofed_registration = se.ScientificExecutionRegistration(formula_version="formula_v2")
    result = _execute(
        _replace_frozen(base, artifact_lineage=bad_lineage, reproducibility_metadata=bad_repro),
        fixture_id="combined_formula_role_lineage_repro",
        registration=spoofed_registration,
        requested_formula_version="formula_v2",
    )
    for code in (
        se.ScientificExecutionDiagnosticCode.SCIENTIFIC_EXECUTION_FORMULA_BINDING_MISMATCH,
        se.ScientificExecutionDiagnosticCode.SCIENTIFIC_EXECUTION_PROHIBITED_ROLE,
        se.ScientificExecutionDiagnosticCode.SCIENTIFIC_EXECUTION_ROLE_BINDING_MISMATCH,
        se.ScientificExecutionDiagnosticCode.LINEAGE_INCOMPLETE,
        se.ScientificExecutionDiagnosticCode.REPRODUCIBILITY_INCOMPLETE,
    ):
        assert code in result.diagnostics.codes
    assert result.execution_state == se.ScientificExecutionState.INCOMPLETE
    assert result.decomposition_result == se.DecompositionResult.UNRESOLVED


def test_equal_aggregation_direct_subtraction_and_algebraic_identity_regression_cases():
    cases = (
        ("one_comparator", 10.0, (6.0,), 6.0, 4.0),
        ("two_comparators", 10.0, (4.0, 8.0), 6.0, 4.0),
        ("three_comparators", 10.0, (3.0, 6.0, 9.0), 6.0, 4.0),
        ("negative_values", -2.0, (-5.0,), -5.0, 3.0),
        ("zero_values", 0.0, (0.0,), 0.0, 0.0),
        ("mixed_signs", 1.0, (-2.0, 4.0), 1.0, 0.0),
        ("small_decimals", 0.3, (0.1, 0.2), 0.15000000000000002, 0.14999999999999997),
        ("large_finite", 1e12, (1e12 - 2, 1e12 + 2), 1e12, 0.0),
    )
    for fixture_id, target, comparators, expected_common, expected_idiosyncratic in cases:
        result = _execute(
            _synthetic(fixture_id, target=target, comparators=comparators, relation="mixed"),
            fixture_id=fixture_id,
        )
        assert result.execution_state == se.ScientificExecutionState.COMPLETE
        assert result.common_component == expected_common
        assert result.idiosyncratic_component == expected_idiosyncratic
        assert result.common_component + result.idiosyncratic_component == result.target_repair

    ordered = _execute(_synthetic("ordered", target=10.0, comparators=(3.0, 6.0, 9.0), relation="mixed"), fixture_id="ordered")
    shuffled = _execute(_synthetic("shuffled", target=10.0, comparators=(9.0, 3.0, 6.0), relation="mixed"), fixture_id="shuffled")
    assert ordered.common_component == shuffled.common_component == 6.0
