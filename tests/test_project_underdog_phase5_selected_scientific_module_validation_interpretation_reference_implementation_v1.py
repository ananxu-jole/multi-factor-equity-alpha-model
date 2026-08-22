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
from pipelines import project_underdog_phase5_selected_scientific_module_validation_interpretation_reference_implementation_v1 as vi  # noqa: E402
from pipelines import project_underdog_phase5_selected_scientific_module_validation_readiness_reference_implementation_v1 as vr  # noqa: E402
from pipelines import project_underdog_phase5_source_authority_reference_implementation_v1 as sa  # noqa: E402


def _fixtures():
    return {fixture.fixture_id: fixture for fixture in vi.canonical_validation_interpretation_fixtures()}


def _result(fixture_id):
    return vi.evaluate_validation_interpretation(_fixtures()[fixture_id].request)


def test_exact_interpretation_state_inventory():
    assert {state.value for state in vi.ValidationInterpretationState} == {
        "INTERPRETATION_SUPPORTED",
        "INTERPRETATION_CONDITIONALLY_SUPPORTED",
        "INTERPRETATION_UNRESOLVED",
        "INTERPRETATION_NOT_SUPPORTED",
        "INTERPRETATION_EXCLUDED",
        "INSUFFICIENT_INTERPRETATION_EVIDENCE",
    }


def test_all_canonical_fixtures_match_expected_states_and_diagnostics():
    fixtures = vi.canonical_validation_interpretation_fixtures()
    assert len(fixtures) == 35
    for fixture in fixtures:
        result = vi.evaluate_validation_interpretation(fixture.request)
        assert result.interpretation_state == fixture.expected_state, fixture.fixture_id
        for code in fixture.expected_diagnostic_codes:
            assert code in result.diagnostics.codes, fixture.fixture_id
        for limitation in fixture.expected_limitations:
            assert limitation in result.limitations.codes, fixture.fixture_id
        assert result.final_classification == vi.FINAL_CLASSIFICATION


def test_supported_and_conditionally_supported_are_metadata_only():
    supported = _result("VI01_supported")
    conditional = _result("VI02_conditionally_supported")

    assert supported.interpretation_state == vi.ValidationInterpretationState.INTERPRETATION_SUPPORTED
    assert supported.acceptance_representation == vi.AcceptanceRepresentation.ACCEPTED_FOR_CONTINUED_RESEARCH
    assert supported.diagnostics.codes == ()
    assert conditional.interpretation_state == vi.ValidationInterpretationState.INTERPRETATION_CONDITIONALLY_SUPPORTED
    assert conditional.acceptance_representation == vi.AcceptanceRepresentation.REQUIRES_ADDITIONAL_INVESTIGATION
    assert vi.ValidationInterpretationDiagnosticCode.CONDITIONAL_INTERPRETATION_LIMITATION in conditional.diagnostics.codes

    for result in (supported, conditional):
        assert result.empirical_evaluation_performed is False
        assert result.statistical_testing_performed is False
        assert result.validation_metrics_calculated is False
        assert result.alpha_quality_evaluated is False
        assert result.production_logic_performed is False
        assert result.optimization_performed is False
        assert result.model_training_performed is False


def test_evidence_classes_map_to_bounded_interpretation_states():
    expectations = {
        "VI03_mixed_evidence": vi.ValidationInterpretationState.INTERPRETATION_CONDITIONALLY_SUPPORTED,
        "VI04_unresolved_evidence": vi.ValidationInterpretationState.INTERPRETATION_UNRESOLVED,
        "VI05_not_supported_negative": vi.ValidationInterpretationState.INTERPRETATION_NOT_SUPPORTED,
        "VI06_not_supported_null": vi.ValidationInterpretationState.INTERPRETATION_NOT_SUPPORTED,
        "VI07_not_supported_conflicting": vi.ValidationInterpretationState.INTERPRETATION_NOT_SUPPORTED,
        "VI30_insufficient_evidence_class": vi.ValidationInterpretationState.INSUFFICIENT_INTERPRETATION_EVIDENCE,
    }
    for fixture_id, expected_state in expectations.items():
        assert _result(fixture_id).interpretation_state == expected_state


def test_acceptance_representation_is_metadata_only_and_never_production():
    expectations = {
        "VI01_supported": vi.AcceptanceRepresentation.ACCEPTED_FOR_CONTINUED_RESEARCH,
        "VI02_conditionally_supported": vi.AcceptanceRepresentation.REQUIRES_ADDITIONAL_INVESTIGATION,
        "VI04_unresolved_evidence": vi.AcceptanceRepresentation.UNRESOLVED,
        "VI05_not_supported_negative": vi.AcceptanceRepresentation.REJECTED_FOR_CURRENT_HYPOTHESIS,
        "VI08_excluded_request": vi.AcceptanceRepresentation.EXCLUDED,
        "VI12_missing_empirical_artifact": vi.AcceptanceRepresentation.UNRESOLVED,
    }
    for fixture_id, expected_acceptance in expectations.items():
        result = _result(fixture_id)
        assert result.acceptance_representation == expected_acceptance
        assert result.information_contract.makes_production_recommendations is False


def test_excluded_precedence_over_other_failures():
    result = _result("VI32_excluded_combined_failures")
    assert result.interpretation_state == vi.ValidationInterpretationState.INTERPRETATION_EXCLUDED
    assert vi.ValidationInterpretationDiagnosticCode.VALIDATION_INTERPRETATION_EXCLUDED in result.diagnostics.codes
    assert vi.ValidationInterpretationDiagnosticCode.EMPIRICAL_ARTIFACT_MISSING in result.diagnostics.codes


def test_conditional_support_never_overrides_fatal_deficiencies():
    result = _result("VI33_conditional_does_not_override_missing_artifact")
    assert result.interpretation_state == vi.ValidationInterpretationState.INSUFFICIENT_INTERPRETATION_EVIDENCE
    assert vi.ValidationInterpretationDiagnosticCode.CONDITIONAL_INTERPRETATION_LIMITATION in result.diagnostics.codes
    assert vi.ValidationInterpretationDiagnosticCode.EMPIRICAL_ARTIFACT_MISSING in result.diagnostics.codes


def test_structural_failure_precedence_categories():
    expectations = {
        "VI10_missing_readiness_artifact": vi.ValidationInterpretationDiagnosticCode.VALIDATION_READINESS_ARTIFACT_MISSING,
        "VI11_readiness_not_ready": vi.ValidationInterpretationDiagnosticCode.INCOMPATIBLE_READINESS_ARTIFACT,
        "VI12_missing_empirical_artifact": vi.ValidationInterpretationDiagnosticCode.EMPIRICAL_ARTIFACT_MISSING,
        "VI14_evaluation_not_complete": vi.ValidationInterpretationDiagnosticCode.EMPIRICAL_EVALUATION_NOT_COMPLETE,
        "VI19_missing_reporting_protocol": vi.ValidationInterpretationDiagnosticCode.MISSING_REPORTING_PROTOCOL,
        "VI23_incomplete_readiness_lineage": vi.ValidationInterpretationDiagnosticCode.INCOMPLETE_LINEAGE,
        "VI25_incomplete_readiness_reproducibility": vi.ValidationInterpretationDiagnosticCode.INCOMPLETE_REPRODUCIBILITY,
    }
    for fixture_id, code in expectations.items():
        result = _result(fixture_id)
        assert result.interpretation_state == vi.ValidationInterpretationState.INSUFFICIENT_INTERPRETATION_EVIDENCE
        assert code in result.diagnostics.codes


def test_negative_null_contradictory_and_historical_failures_are_preserved_or_fail_closed():
    for fixture_id in (
        "VI27_negative_evidence_not_preserved",
        "VI28_contradictory_evidence_not_preserved",
        "VI29_historical_failures_not_reconstructable",
    ):
        result = _result(fixture_id)
        assert result.interpretation_state == vi.ValidationInterpretationState.INSUFFICIENT_INTERPRETATION_EVIDENCE
        assert vi.ValidationInterpretationDiagnosticCode.NEGATIVE_EVIDENCE_NOT_PRESERVED in result.diagnostics.codes

    negative = _result("VI05_not_supported_negative")
    null = _result("VI06_not_supported_null")
    assert negative.empirical_evidence_metadata.negative_findings_preserved is True
    assert null.empirical_evidence_metadata.null_findings_preserved is True


def test_diagnostics_are_structural_and_sorted():
    result = _result("VI31_combined_failures")
    for code in (
        vi.ValidationInterpretationDiagnosticCode.MISSING_REPORTING_PROTOCOL,
        vi.ValidationInterpretationDiagnosticCode.INCOMPLETE_LINEAGE,
        vi.ValidationInterpretationDiagnosticCode.NEGATIVE_EVIDENCE_NOT_PRESERVED,
        vi.ValidationInterpretationDiagnosticCode.INSUFFICIENT_INTERPRETATION_EVIDENCE,
    ):
        assert code in result.diagnostics.codes
    assert result.diagnostics.codes == tuple(sorted(result.diagnostics.codes, key=lambda code: code.value))
    forbidden_terms = ("Sharpe", "IC", "p-value", "t-statistic", "prediction quality")
    for entry in result.diagnostics.entries:
        assert all(term not in entry["message"] for term in forbidden_terms)


def test_information_contract_and_result_refuse_downstream_outputs():
    result = _result("VI01_supported")
    contract = result.information_contract

    assert contract.exposes_interpretation_state is True
    assert contract.exposes_diagnostics is True
    assert contract.exposes_limitations is True
    assert contract.exposes_interpretation_metadata is True
    assert contract.exposes_reporting_metadata is True
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
        "generates_reports",
        "makes_production_recommendations",
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
        "report_generated",
        "production_logic_performed",
        "optimization_performed",
        "ml_feature_created",
        "ml_label_created",
        "model_training_performed",
    ):
        assert getattr(result, field) is False


def test_lineage_propagates_upstream_and_creates_no_production_artifacts():
    result = _result("VI01_supported")
    assert result.lineage.lineage_chain == vi.LINEAGE_CHAIN
    assert result.lineage.validation_readiness_artifact == result.identity.validation_readiness_id
    assert result.lineage.completed_empirical_evaluation_artifact == result.identity.empirical_artifact_id
    assert result.lineage.validation_interpretation_artifact == result.validation_interpretation_id
    assert result.lineage.upstream_artifacts["source_authority_artifact"]
    assert result.lineage.upstream_artifacts["pit_artifact"]
    assert result.lineage.upstream_artifacts["comparator_artifact"]
    assert result.lineage.upstream_artifacts["prepared_observation_artifact"]
    assert result.lineage.upstream_artifacts["frozen_module_input_artifact"]
    assert result.lineage.upstream_artifacts["scientific_execution_artifact"]
    assert result.lineage.candidate_artifact == ""
    assert result.lineage.panel_artifact == ""
    assert result.lineage.portfolio_artifact == ""
    assert result.lineage.production_artifact == ""
    assert result.lineage.optimization_artifact == ""
    assert result.lineage.ml_artifact == ""


def test_reproducibility_versions_are_deterministic_metadata_only():
    result = _result("VI01_supported")
    assert result.reproducibility.interpretation_version == vi.INTERPRETATION_VERSION
    assert result.reproducibility.reporting_version == vi.REPORTING_VERSION
    assert result.reproducibility.validation_protocol_version == vr.VALIDATION_PROTOCOL_VERSION
    assert result.reproducibility.execution_version == se.MODULE_VERSION
    assert result.reproducibility.reproducibility_version == vi.REPRODUCIBILITY_SCHEMA_VERSION
    assert result.reproducibility.serialization_version == vi.STABLE_SERIALIZATION_VERSION
    assert result.reproducibility.validation_readiness_artifact == result.identity.validation_readiness_id
    assert result.reproducibility.empirical_artifact_id == result.identity.empirical_artifact_id
    assert result.reproducibility.evidence_package_id == result.identity.evidence_package_id
    assert result.reproducibility.reporting_protocol == result.reporting_governance.reporting_protocol
    assert result.reproducibility.deterministic_interpretation_identity == result.validation_interpretation_id


def test_identity_and_stable_json_are_deterministic_and_metadata_sensitive():
    fixture = _fixtures()["VI35_deterministic_repeat"]
    first = vi.evaluate_validation_interpretation(fixture.request)
    second = vi.evaluate_validation_interpretation(fixture.request)
    assert first == second
    assert first.validation_interpretation_id == second.validation_interpretation_id
    assert first.stable_json() == second.stable_json()
    assert json.loads(first.stable_json()) == json.loads(second.stable_json())

    metadata_only = vi.evaluate_validation_interpretation(replace(fixture.request, requester_metadata={"operator": "review"}))
    assert metadata_only.validation_interpretation_id == first.validation_interpretation_id

    changed_evidence = vi.evaluate_validation_interpretation(
        replace(
            fixture.request,
            empirical_evidence=replace(fixture.request.empirical_evidence, evidence_package_id="synthetic_package_v2"),
        )
    )
    assert changed_evidence.validation_interpretation_id != first.validation_interpretation_id

    changed_reporting = vi.evaluate_validation_interpretation(
        replace(
            fixture.request,
            reporting_governance=replace(fixture.request.reporting_governance, report_version="v2"),
        )
    )
    assert changed_reporting.validation_interpretation_id != first.validation_interpretation_id


def test_separate_process_stable_serialization_is_identical():
    code = (
        "from pipelines import project_underdog_phase5_selected_scientific_module_validation_interpretation_reference_implementation_v1 as vi;"
        "fixtures={f.fixture_id:f for f in vi.canonical_validation_interpretation_fixtures()};"
        "print(vi.evaluate_validation_interpretation(fixtures['VI35_deterministic_repeat'].request).stable_json())"
    )
    first = subprocess.check_output([sys.executable, "-c", code], cwd=ROOT, text=True)
    second = subprocess.check_output([sys.executable, "-c", code], cwd=ROOT, text=True)
    assert first == second


def test_guardrail_manifest_excludes_prohibited_behavior():
    assert vi.validation_interpretation_guardrail_manifest() == {
        "empirical_evaluation": False,
        "statistical_testing": False,
        "validation_metrics": False,
        "alpha_evaluation": False,
        "sharpe_calculation": False,
        "ic_calculation": False,
        "prediction": False,
        "ranking": False,
        "portfolio_construction": False,
        "report_generation": False,
        "candidate_generation": False,
        "panel_generation": False,
        "production": False,
        "optimization": False,
        "machine_learning": False,
        "datasets_loaded": False,
        "regression": False,
        "residualization": False,
        "contamination_testing": False,
        "falsification_testing": False,
    }


def test_registration_mismatch_and_downstream_requests_are_excluded():
    ready = _fixtures()["VI01_supported"].request.validation_readiness_result
    bad_registration = vi.ValidationInterpretationRegistration(performs_statistical_testing=True)
    registration_result = vi.evaluate_validation_interpretation(
        vi.ValidationInterpretationRequest(validation_readiness_result=ready, registration=bad_registration)
    )
    assert registration_result.interpretation_state == vi.ValidationInterpretationState.INTERPRETATION_EXCLUDED
    assert vi.ValidationInterpretationDiagnosticCode.VALIDATION_INTERPRETATION_EXCLUDED in registration_result.diagnostics.codes

    downstream_result = vi.evaluate_validation_interpretation(
        vi.ValidationInterpretationRequest(validation_readiness_result=ready, prediction_requested=True, ml_requested=True)
    )
    assert downstream_result.interpretation_state == vi.ValidationInterpretationState.INTERPRETATION_EXCLUDED
    assert vi.ValidationInterpretationDiagnosticCode.DOWNSTREAM_SCOPE_PROHIBITED in downstream_result.diagnostics.codes


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
    execution_result = se.execute_selected_scientific_module({fixture.fixture_id: fixture for fixture in se.canonical_scientific_execution_fixtures()}["SE01_common"].request)
    readiness_result = vr.evaluate_validation_readiness(vr.ValidationReadinessRequest(scientific_execution_result=execution_result))
    interpretation_result = vi.evaluate_validation_interpretation(
        vi.ValidationInterpretationRequest(validation_readiness_result=readiness_result)
    )

    assert source_result.information_contract.runs_validation is False
    assert pit_result.information_contract.runs_validation is False
    assert comparator_result.information_contract.runs_validation is False
    assert prepared_result.information_contract.runs_validation is False
    assert intake_result.information_contract.creates_validation_result is False
    assert activation_result.exposes_validation_results is False
    assert adapter_result.validation_performed is False
    assert execution_result.information_contract.performs_validation is False
    assert readiness_result.information_contract.exposes_validation_statistics is False
    assert interpretation_result.information_contract.exposes_validation_statistics is False
    assert interpretation_result.interpretation_state == vi.ValidationInterpretationState.INTERPRETATION_SUPPORTED
