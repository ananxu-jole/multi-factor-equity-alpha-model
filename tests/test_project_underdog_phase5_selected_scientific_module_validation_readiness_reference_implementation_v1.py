import json
import subprocess
import sys
from dataclasses import replace
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from pipelines import project_underdog_phase5_comparator_construction_reference_implementation_v1 as cc  # noqa: E402
from pipelines import project_underdog_phase5_pit_identity_and_context_evidence_reference_implementation_v1 as pic  # noqa: E402
from pipelines import project_underdog_phase5_prepared_observations_reference_implementation_v1 as po  # noqa: E402
from pipelines import project_underdog_phase5_scientific_module_activation_registry_and_execution_authorization_reference_implementation_v1 as ar  # noqa: E402
from pipelines import project_underdog_phase5_scientific_module_intake_reference_implementation_v1 as smi  # noqa: E402
from pipelines import project_underdog_phase5_selected_scientific_module_adapter_reference_implementation_v1 as ad  # noqa: E402
from pipelines import project_underdog_phase5_selected_scientific_module_scientific_execution_reference_implementation_v1 as se  # noqa: E402
from pipelines import project_underdog_phase5_selected_scientific_module_validation_readiness_reference_implementation_v1 as vr  # noqa: E402
from pipelines import project_underdog_phase5_source_authority_reference_implementation_v1 as sa  # noqa: E402


def _fixtures():
    return {fixture.fixture_id: fixture for fixture in vr.canonical_validation_readiness_fixtures()}


def _result(fixture_id):
    return vr.evaluate_validation_readiness(_fixtures()[fixture_id].request)


def _ready_execution_result():
    se_fixtures = {fixture.fixture_id: fixture for fixture in se.canonical_scientific_execution_fixtures()}
    return se.execute_selected_scientific_module(se_fixtures["SE01_common"].request)


def test_exact_readiness_state_inventory():
    assert {state.value for state in vr.ValidationReadinessState} == {
        "VALIDATION_READY",
        "VALIDATION_CONDITIONALLY_READY",
        "VALIDATION_UNRESOLVED",
        "VALIDATION_NOT_READY",
        "VALIDATION_EXCLUDED",
        "INSUFFICIENT_VALIDATION_EVIDENCE",
    }


def test_all_canonical_fixtures_match_expected_states_and_diagnostics():
    fixtures = vr.canonical_validation_readiness_fixtures()
    assert len(fixtures) == 26
    for fixture in fixtures:
        result = vr.evaluate_validation_readiness(fixture.request)
        assert result.readiness_state == fixture.expected_state, fixture.fixture_id
        for code in fixture.expected_diagnostic_codes:
            assert code in result.diagnostics.codes, fixture.fixture_id
        for limitation in fixture.expected_limitations:
            assert limitation in result.limitations.codes, fixture.fixture_id
        assert result.final_classification == vr.FINAL_CLASSIFICATION


def test_ready_and_conditionally_ready_states_are_metadata_only():
    ready = _result("VR01_ready")
    conditional = _result("VR02_conditionally_ready")

    assert ready.readiness_state == vr.ValidationReadinessState.READY
    assert ready.diagnostics.codes == ()
    assert conditional.readiness_state == vr.ValidationReadinessState.CONDITIONALLY_READY
    assert vr.ValidationReadinessDiagnosticCode.CONDITIONALLY_READY_LIMITATION in conditional.diagnostics.codes
    assert "bounded_population_review_required" in conditional.limitations.codes

    for result in (ready, conditional):
        assert result.empirical_evaluation_performed is False
        assert result.statistical_testing_performed is False
        assert result.validation_metrics_calculated is False
        assert result.alpha_quality_evaluated is False
        assert result.production_logic_performed is False
        assert result.optimization_performed is False
        assert result.model_training_performed is False


def test_unresolved_execution_and_insufficient_validation_evidence_are_distinct():
    unresolved = _result("VR03_unresolved_execution")
    insufficient = _result("VR21_negative_evidence_not_preserved")

    assert unresolved.readiness_state == vr.ValidationReadinessState.UNRESOLVED
    assert vr.ValidationReadinessDiagnosticCode.UNRESOLVED_SCIENTIFIC_EXECUTION in unresolved.diagnostics.codes
    assert insufficient.readiness_state == vr.ValidationReadinessState.INSUFFICIENT_EVIDENCE
    assert vr.ValidationReadinessDiagnosticCode.INSUFFICIENT_VALIDATION_EVIDENCE in insufficient.diagnostics.codes


def test_excluded_precedence_over_other_failures():
    request = replace(
        _fixtures()["VR25_combined_failures"].request,
        excluded=True,
        empirical_evaluation_requested=True,
    )
    result = vr.evaluate_validation_readiness(request)
    assert result.readiness_state == vr.ValidationReadinessState.EXCLUDED
    assert vr.ValidationReadinessDiagnosticCode.VALIDATION_READINESS_EXCLUDED in result.diagnostics.codes
    assert vr.ValidationReadinessDiagnosticCode.DOWNSTREAM_SCOPE_PROHIBITED in result.diagnostics.codes
    assert vr.ValidationReadinessDiagnosticCode.MISSING_PROTOCOL in result.diagnostics.codes


def test_conditional_readiness_never_bypasses_fatal_failures():
    request = replace(
        _fixtures()["VR06_missing_protocol"].request,
        conditional_limitations=("conditional_does_not_override_missing_protocol",),
    )
    result = vr.evaluate_validation_readiness(request)
    assert result.readiness_state == vr.ValidationReadinessState.NOT_READY
    assert vr.ValidationReadinessDiagnosticCode.MISSING_PROTOCOL in result.diagnostics.codes
    assert vr.ValidationReadinessDiagnosticCode.CONDITIONALLY_READY_LIMITATION in result.diagnostics.codes


def test_incompatible_specification_horizon_lineage_and_reproducibility_fail_closed():
    expectations = {
        "VR15_incompatible_scientific_spec": vr.ValidationReadinessDiagnosticCode.INCOMPATIBLE_SCIENTIFIC_SPECIFICATION,
        "VR16_incompatible_formula_spec": vr.ValidationReadinessDiagnosticCode.INCOMPATIBLE_FORMULA_SPECIFICATION,
        "VR17_incompatible_activation_spec": vr.ValidationReadinessDiagnosticCode.INCOMPATIBLE_ACTIVATION_SPECIFICATION,
        "VR18_incompatible_horizon": vr.ValidationReadinessDiagnosticCode.INCOMPATIBLE_FROZEN_HORIZON,
        "VR19_missing_lineage": vr.ValidationReadinessDiagnosticCode.INCOMPLETE_LINEAGE,
        "VR20_missing_reproducibility": vr.ValidationReadinessDiagnosticCode.MISSING_REPRODUCIBILITY_METADATA,
    }
    for fixture_id, code in expectations.items():
        result = _result(fixture_id)
        assert result.readiness_state == vr.ValidationReadinessState.NOT_READY
        assert code in result.diagnostics.codes


def test_governance_contamination_and_falsification_metadata_failures():
    expectations = {
        "VR06_missing_protocol": vr.ValidationReadinessDiagnosticCode.MISSING_PROTOCOL,
        "VR07_missing_benchmark": vr.ValidationReadinessDiagnosticCode.MISSING_BENCHMARK_DEFINITION,
        "VR08_missing_contamination_policy": vr.ValidationReadinessDiagnosticCode.MISSING_CONTAMINATION_POLICY,
        "VR09_missing_falsification_policy": vr.ValidationReadinessDiagnosticCode.MISSING_FALSIFICATION_POLICY,
        "VR10_missing_reporting_protocol": vr.ValidationReadinessDiagnosticCode.MISSING_REPORTING_PROTOCOL,
        "VR22_incomplete_contamination_controls": vr.ValidationReadinessDiagnosticCode.MISSING_CONTAMINATION_POLICY,
        "VR23_incomplete_falsification_metadata": vr.ValidationReadinessDiagnosticCode.MISSING_FALSIFICATION_POLICY,
    }
    for fixture_id, code in expectations.items():
        result = _result(fixture_id)
        assert result.readiness_state == vr.ValidationReadinessState.NOT_READY
        assert code in result.diagnostics.codes


def test_diagnostics_are_structural_and_sorted():
    result = _result("VR25_combined_failures")
    for code in (
        vr.ValidationReadinessDiagnosticCode.MISSING_PROTOCOL,
        vr.ValidationReadinessDiagnosticCode.MISSING_CONTAMINATION_POLICY,
        vr.ValidationReadinessDiagnosticCode.INCOMPLETE_LINEAGE,
        vr.ValidationReadinessDiagnosticCode.MISSING_REPRODUCIBILITY_METADATA,
        vr.ValidationReadinessDiagnosticCode.NEGATIVE_EVIDENCE_NOT_PRESERVED,
        vr.ValidationReadinessDiagnosticCode.INSUFFICIENT_VALIDATION_EVIDENCE,
    ):
        assert code in result.diagnostics.codes
    assert result.diagnostics.codes == tuple(sorted(result.diagnostics.codes, key=lambda code: code.value))
    assert all("Sharpe" not in entry["message"] for entry in result.diagnostics.entries)
    assert all("IC" not in entry["message"] for entry in result.diagnostics.entries)


def test_information_contract_and_result_refuse_downstream_outputs():
    result = _result("VR01_ready")
    contract = result.information_contract

    assert contract.exposes_readiness_state is True
    assert contract.exposes_diagnostics is True
    assert contract.exposes_limitations is True
    assert contract.exposes_evaluation_metadata is True
    assert contract.exposes_lineage is True
    assert contract.exposes_reproducibility is True
    for field in (
        "exposes_sharpe",
        "exposes_ic",
        "exposes_alpha",
        "exposes_prediction",
        "exposes_ranking",
        "exposes_portfolio",
        "exposes_validation_statistics",
        "makes_production_decisions",
        "performs_optimization",
        "exposes_ml_outputs",
    ):
        assert getattr(contract, field) is False
    for field in (
        "empirical_evaluation_performed",
        "statistical_testing_performed",
        "validation_metrics_calculated",
        "alpha_quality_evaluated",
        "sharpe_calculated",
        "ic_calculated",
        "prediction_created",
        "ranking_created",
        "portfolio_created",
        "validation_logic_executed",
        "production_logic_performed",
        "optimization_performed",
        "ml_feature_created",
        "ml_label_created",
        "model_training_performed",
    ):
        assert getattr(result, field) is False


def test_lineage_propagates_upstream_and_creates_no_empirical_artifacts():
    result = _result("VR01_ready")
    assert result.lineage.lineage_chain == vr.LINEAGE_CHAIN
    assert result.lineage.scientific_execution_artifact == result.identity.scientific_execution_id
    assert result.lineage.validation_readiness_artifact == result.validation_readiness_id
    assert result.lineage.upstream_artifacts["source_authority_artifact"]
    assert result.lineage.upstream_artifacts["pit_artifact"]
    assert result.lineage.upstream_artifacts["comparator_artifact"]
    assert result.lineage.upstream_artifacts["prepared_observation_artifact"]
    assert result.lineage.upstream_artifacts["frozen_module_input_artifact"]
    assert result.lineage.empirical_evaluation_artifact == ""
    assert result.lineage.validation_artifact == ""
    assert result.lineage.candidate_artifact == ""
    assert result.lineage.panel_artifact == ""
    assert result.lineage.production_artifact == ""
    assert result.lineage.ml_artifact == ""


def test_reproducibility_versions_are_deterministic_metadata_only():
    result = _result("VR01_ready")
    assert result.reproducibility.validation_protocol_version == vr.VALIDATION_PROTOCOL_VERSION
    assert result.reproducibility.execution_version == se.MODULE_VERSION
    assert result.reproducibility.scientific_specification_version == ad.DEFAULT_SCIENTIFIC_SPECIFICATION_VERSION
    assert result.reproducibility.formula_specification_version == se.FORMULA_VERSION
    assert result.reproducibility.frozen_activation_specification_version == ad.NARROW_ACTIVATION_SPECIFICATION_VERSION
    assert result.reproducibility.frozen_horizon_version == ad.DEFAULT_FROZEN_HORIZON_SPECIFICATION_VERSION
    assert result.reproducibility.reproducibility_version == vr.REPRODUCIBILITY_SCHEMA_VERSION
    assert result.reproducibility.deterministic_readiness_identity == result.validation_readiness_id


def test_identity_and_stable_json_are_deterministic_and_metadata_sensitive():
    fixture = _fixtures()["VR26_deterministic_repeat"]
    first = vr.evaluate_validation_readiness(fixture.request)
    second = vr.evaluate_validation_readiness(fixture.request)
    assert first == second
    assert first.validation_readiness_id == second.validation_readiness_id
    assert first.stable_json() == second.stable_json()
    assert json.loads(first.stable_json()) == json.loads(second.stable_json())

    metadata_only = vr.evaluate_validation_readiness(replace(fixture.request, requester_metadata={"operator": "review"}))
    assert metadata_only.validation_readiness_id == first.validation_readiness_id

    changed_governance = vr.evaluate_validation_readiness(
        replace(
            fixture.request,
            evaluation_governance=replace(fixture.request.evaluation_governance, evaluation_version="v2"),
        )
    )
    assert changed_governance.validation_readiness_id != first.validation_readiness_id

    changed_execution = vr.evaluate_validation_readiness(
        replace(
            fixture.request,
            scientific_execution_result=replace(
                fixture.request.scientific_execution_result,
                scientific_execution_id="changed_scientific_execution_id",
            ),
        )
    )
    assert changed_execution.validation_readiness_id != first.validation_readiness_id


def test_separate_process_stable_serialization_is_identical():
    code = (
        "from pipelines import project_underdog_phase5_selected_scientific_module_validation_readiness_reference_implementation_v1 as vr;"
        "fixtures={f.fixture_id:f for f in vr.canonical_validation_readiness_fixtures()};"
        "print(vr.evaluate_validation_readiness(fixtures['VR26_deterministic_repeat'].request).stable_json())"
    )
    first = subprocess.check_output([sys.executable, "-c", code], cwd=ROOT, text=True)
    second = subprocess.check_output([sys.executable, "-c", code], cwd=ROOT, text=True)
    assert first == second


def test_guardrail_manifest_excludes_prohibited_behavior():
    assert vr.validation_readiness_guardrail_manifest() == {
        "scientific_execution": False,
        "empirical_evaluation": False,
        "statistical_testing": False,
        "validation_metrics": False,
        "alpha_evaluation": False,
        "sharpe_calculation": False,
        "ic_calculation": False,
        "prediction": False,
        "ranking": False,
        "portfolio_construction": False,
        "candidate_generation": False,
        "panel_generation": False,
        "production": False,
        "optimization": False,
        "machine_learning": False,
        "datasets_loaded": False,
        "contamination_testing": False,
        "falsification_testing": False,
    }


def test_registration_mismatch_and_downstream_requests_are_excluded():
    ready = _ready_execution_result()
    bad_registration = vr.ValidationReadinessRegistration(performs_empirical_evaluation=True)
    registration_result = vr.evaluate_validation_readiness(
        vr.ValidationReadinessRequest(scientific_execution_result=ready, registration=bad_registration)
    )
    assert registration_result.readiness_state == vr.ValidationReadinessState.EXCLUDED
    assert vr.ValidationReadinessDiagnosticCode.VALIDATION_READINESS_EXCLUDED in registration_result.diagnostics.codes

    downstream_result = vr.evaluate_validation_readiness(
        vr.ValidationReadinessRequest(scientific_execution_result=ready, statistical_testing_requested=True, ml_requested=True)
    )
    assert downstream_result.readiness_state == vr.ValidationReadinessState.EXCLUDED
    assert vr.ValidationReadinessDiagnosticCode.DOWNSTREAM_SCOPE_PROHIBITED in downstream_result.diagnostics.codes


def test_compatible_with_completed_upstream_phase5_layers():
    source_result = sa.evaluate_source_authority({fixture.fixture_id: fixture for fixture in sa.canonical_source_authority_fixtures()}["SA1_authoritative"].record)
    pit_result = pic.evaluate_pit_identity_context({fixture.fixture_id: fixture for fixture in pic.canonical_pit_identity_context_fixtures()}["PIC1_normal_identity"].record)
    comparator_result = cc.evaluate_comparator_construction({fixture.fixture_id: fixture for fixture in cc.canonical_comparator_construction_fixtures()}["CC1_eligible"].record)
    prepared_result = po.evaluate_prepared_observation({fixture.fixture_id: fixture for fixture in po.canonical_prepared_observation_fixtures()}["PO1_ready"].record)
    intake_result = smi.evaluate_scientific_module_intake({fixture.fixture_id: fixture for fixture in smi.canonical_scientific_module_intake_fixtures()}["SMI05_context_and_comparator"].request)
    activation_fixture = {fixture.fixture_id: fixture for fixture in ar.canonical_activation_registry_fixtures()}["ACT01_valid_module_registration"]
    activation_result = ar.evaluate_activation_readiness(
        activation_fixture.activation_declaration,
        activation_fixture.registry_snapshot,
        activation_fixture.prerequisites,
        activation_fixture.version_compatibility,
        activation_fixture.lineage,
        activation_fixture.reproducibility,
    )
    adapter_result = ad.evaluate_selected_module_adapter({fixture.fixture_id: fixture for fixture in ad.canonical_selected_module_adapter_fixtures()}["AD04_valid_target_context_comparator"].request)
    execution_result = _ready_execution_result()
    readiness_result = vr.evaluate_validation_readiness(vr.ValidationReadinessRequest(scientific_execution_result=execution_result))

    assert source_result.information_contract.runs_validation is False
    assert pit_result.information_contract.runs_validation is False
    assert comparator_result.information_contract.runs_validation is False
    assert prepared_result.information_contract.runs_validation is False
    assert intake_result.information_contract.creates_validation_result is False
    assert activation_result.exposes_validation_results is False
    assert adapter_result.validation_performed is False
    assert execution_result.information_contract.performs_validation is False
    assert readiness_result.information_contract.exposes_validation_statistics is False
    assert readiness_result.readiness_state == vr.ValidationReadinessState.READY
