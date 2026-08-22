from __future__ import annotations

from dataclasses import dataclass, field, is_dataclass, replace
from enum import Enum
from functools import lru_cache
import hashlib
import json
from typing import Any

from pipelines import project_underdog_phase5_selected_scientific_module_scientific_execution_reference_implementation_v1 as scientific_execution
from pipelines import project_underdog_phase5_selected_scientific_module_validation_readiness_reference_implementation_v1 as validation_readiness


MODULE_ID = "project_underdog_phase5_selected_scientific_module_validation_interpretation_reference_implementation_v1"
MODULE_VERSION = "v1"
DESIGN_ID = "project_underdog_phase5_selected_scientific_module_validation_interpretation_and_empirical_evaluation_design_v1"
FINAL_CLASSIFICATION = "VALIDATION_INTERPRETATION_REFERENCE_IMPLEMENTATION_COMPLETE"
VALIDATION_INTERPRETATION_SCHEMA_VERSION = "selected_module_validation_interpretation_schema_v1"
REPRODUCIBILITY_SCHEMA_VERSION = "selected_module_validation_interpretation_reproducibility_schema_v1"
STABLE_SERIALIZATION_VERSION = "stable_json_v1"
INTERPRETATION_VERSION = "selected_module_validation_interpretation_v1"
REPORTING_VERSION = "selected_module_validation_interpretation_reporting_v1"
VALIDATION_PROTOCOL_VERSION = validation_readiness.VALIDATION_PROTOCOL_VERSION
EXECUTION_VERSION = scientific_execution.MODULE_VERSION
SELECTED_MODULE_ID = validation_readiness.SELECTED_MODULE_ID


class ValidationInterpretationState(str, Enum):
    INTERPRETATION_SUPPORTED = "INTERPRETATION_SUPPORTED"
    INTERPRETATION_CONDITIONALLY_SUPPORTED = "INTERPRETATION_CONDITIONALLY_SUPPORTED"
    INTERPRETATION_UNRESOLVED = "INTERPRETATION_UNRESOLVED"
    INTERPRETATION_NOT_SUPPORTED = "INTERPRETATION_NOT_SUPPORTED"
    INTERPRETATION_EXCLUDED = "INTERPRETATION_EXCLUDED"
    INSUFFICIENT_INTERPRETATION_EVIDENCE = "INSUFFICIENT_INTERPRETATION_EVIDENCE"


class EvidenceClassification(str, Enum):
    SUPPORTING = "SUPPORTING_EVIDENCE"
    CONFLICTING = "CONFLICTING_EVIDENCE"
    MIXED = "MIXED_EVIDENCE"
    UNRESOLVED = "UNRESOLVED_EVIDENCE"
    INSUFFICIENT = "INSUFFICIENT_EVIDENCE"
    NULL = "NULL_FINDINGS"
    NEGATIVE = "NEGATIVE_FINDINGS"


class AcceptanceRepresentation(str, Enum):
    ACCEPTED_FOR_CONTINUED_RESEARCH = "ACCEPTED_FOR_CONTINUED_RESEARCH"
    REQUIRES_ADDITIONAL_INVESTIGATION = "REQUIRES_ADDITIONAL_INVESTIGATION"
    UNRESOLVED = "UNRESOLVED"
    REJECTED_FOR_CURRENT_HYPOTHESIS = "REJECTED_FOR_CURRENT_HYPOTHESIS"
    EXCLUDED = "EXCLUDED"


class ValidationInterpretationDiagnosticCode(str, Enum):
    VALIDATION_INTERPRETATION_EXCLUDED = "VALIDATION_INTERPRETATION_EXCLUDED"
    DOWNSTREAM_SCOPE_PROHIBITED = "DOWNSTREAM_SCOPE_PROHIBITED"
    VALIDATION_READINESS_ARTIFACT_MISSING = "VALIDATION_READINESS_ARTIFACT_MISSING"
    INCOMPATIBLE_READINESS_ARTIFACT = "INCOMPATIBLE_READINESS_ARTIFACT"
    EMPIRICAL_ARTIFACT_MISSING = "EMPIRICAL_ARTIFACT_MISSING"
    EMPIRICAL_EVALUATION_NOT_COMPLETE = "EMPIRICAL_EVALUATION_NOT_COMPLETE"
    MISSING_INTERPRETATION_METADATA = "MISSING_INTERPRETATION_METADATA"
    MISSING_REPORTING_PROTOCOL = "MISSING_REPORTING_PROTOCOL"
    MISSING_REPORTING_METADATA = "MISSING_REPORTING_METADATA"
    INCONSISTENT_EVIDENCE_PACKAGE = "INCONSISTENT_EVIDENCE_PACKAGE"
    UNRESOLVED_EVALUATION = "UNRESOLVED_EVALUATION"
    INSUFFICIENT_INTERPRETATION_EVIDENCE = "INSUFFICIENT_INTERPRETATION_EVIDENCE"
    INCOMPLETE_LINEAGE = "INCOMPLETE_LINEAGE"
    INCOMPLETE_REPRODUCIBILITY = "INCOMPLETE_REPRODUCIBILITY"
    NEGATIVE_EVIDENCE_NOT_PRESERVED = "NEGATIVE_EVIDENCE_NOT_PRESERVED"
    CONDITIONAL_INTERPRETATION_LIMITATION = "CONDITIONAL_INTERPRETATION_LIMITATION"
    INTERPRETATION_NOT_SUPPORTED = "INTERPRETATION_NOT_SUPPORTED"


REFERENCE_LIMITATIONS = (
    "SYNTHETIC_IMPLEMENTATION_ONLY",
    "REFERENCE_IMPLEMENTATION_ONLY",
    "EMPIRICAL_INTERPRETATION_PENDING",
    "EMPIRICAL_EVIDENCE_NOT_CALCULATED_BY_THIS_LAYER",
    "PRODUCTION_UNAVAILABLE",
    "OPTIMIZATION_UNAVAILABLE",
    "ML_UNAVAILABLE",
    "STATISTICAL_CALCULATION_NOT_PERFORMED",
    "REPORT_GENERATION_NOT_PERFORMED",
)
CONDITIONAL_LIMITATION = "CONDITIONAL_INTERPRETATION_METADATA_PRESENT"
UNRESOLVED_LIMITATION = "INTERPRETATION_UNRESOLVED"
INSUFFICIENT_LIMITATION = "INSUFFICIENT_INTERPRETATION_EVIDENCE"
NEGATIVE_LIMITATION = "NEGATIVE_OR_NULL_EVIDENCE_PRESERVED"

LINEAGE_CHAIN = (
    "Source Authority",
    "PIT",
    "Comparator",
    "Prepared Observations",
    "Intake",
    "Activation",
    "Adapter",
    "Frozen Module Input",
    "Scientific Execution",
    "Validation Readiness",
    "Validation Interpretation",
)


def _to_jsonable(value: Any) -> Any:
    if isinstance(value, Enum):
        return value.value
    if is_dataclass(value):
        return {key: _to_jsonable(val) for key, val in value.__dict__.items()}
    if isinstance(value, tuple):
        return [_to_jsonable(item) for item in value]
    if isinstance(value, list):
        return [_to_jsonable(item) for item in value]
    if isinstance(value, dict):
        return {str(key): _to_jsonable(value[key]) for key in sorted(value)}
    return value


def _stable_json(value: Any) -> str:
    return json.dumps(_to_jsonable(value), sort_keys=True, separators=(",", ":"))


def _stable_digest(value: Any, prefix: str) -> str:
    digest = hashlib.sha256(_stable_json(value).encode("utf-8")).hexdigest()[:16]
    return f"{prefix}_{digest}"


@dataclass(frozen=True)
class ValidationInterpretationRegistration:
    registration_id: str = "selected_scientific_module_validation_interpretation_registration_v1"
    implementation_id: str = MODULE_ID
    implementation_version: str = MODULE_VERSION
    design_id: str = DESIGN_ID
    selected_module_id: str = SELECTED_MODULE_ID
    interpretation_version: str = INTERPRETATION_VERSION
    reporting_version: str = REPORTING_VERSION
    validation_protocol_version: str = VALIDATION_PROTOCOL_VERSION
    validation_interpretation_schema_version: str = VALIDATION_INTERPRETATION_SCHEMA_VERSION
    reproducibility_schema_version: str = REPRODUCIBILITY_SCHEMA_VERSION
    stable_serialization_version: str = STABLE_SERIALIZATION_VERSION
    performs_empirical_evaluation: bool = False
    performs_statistical_testing: bool = False
    calculates_validation_metrics: bool = False
    evaluates_alpha_quality: bool = False
    generates_reports: bool = False
    supports_production: bool = False
    supports_optimization: bool = False
    supports_ml: bool = False


@dataclass(frozen=True)
class CompletedEmpiricalEvidenceMetadata:
    empirical_artifact_id: str = "synthetic_completed_empirical_evaluation_artifact_v1"
    evidence_package_id: str = "synthetic_completed_evidence_package_v1"
    evaluation_completed: bool = True
    protocol_identity: str = VALIDATION_PROTOCOL_VERSION
    benchmark_identity: str = "synthetic_frozen_benchmark_identity_v1"
    evidence_complete: bool = True
    evidence_consistent: bool = True
    reproducibility_confirmed: bool = True
    reporting_complete: bool = True
    interpretation_metadata_complete: bool = True
    lineage_complete: bool = True
    evidence_classification: EvidenceClassification = EvidenceClassification.SUPPORTING
    conditional_support: bool = False
    failures_preserved: bool = True
    null_findings_preserved: bool = True
    negative_findings_preserved: bool = True
    contradictory_evidence_preserved: bool = True
    historical_failures_reconstructable: bool = True


@dataclass(frozen=True)
class ReportingGovernanceMetadata:
    report_identity: str = "synthetic_validation_interpretation_report_identity_v1"
    report_version: str = REPORTING_VERSION
    reporting_protocol: str = "synthetic_validation_interpretation_reporting_protocol_v1"
    interpretation_version: str = INTERPRETATION_VERSION
    evidence_version: str = "synthetic_completed_evidence_package_v1"
    review_status: str = "synthetic_review_complete"


@dataclass(frozen=True)
class ValidationInterpretationRequest:
    validation_readiness_result: validation_readiness.ValidationReadinessResult | None
    empirical_evidence: CompletedEmpiricalEvidenceMetadata = field(default_factory=CompletedEmpiricalEvidenceMetadata)
    reporting_governance: ReportingGovernanceMetadata = field(default_factory=ReportingGovernanceMetadata)
    registration: ValidationInterpretationRegistration = field(default_factory=ValidationInterpretationRegistration)
    fixture_id: str = "synthetic_validation_interpretation_request"
    excluded: bool = False
    conditional_limitations: tuple[str, ...] = ()
    requester_metadata: dict[str, str] = field(default_factory=dict)
    empirical_evaluation_requested: bool = False
    statistical_testing_requested: bool = False
    validation_metrics_requested: bool = False
    alpha_evaluation_requested: bool = False
    sharpe_requested: bool = False
    ic_requested: bool = False
    prediction_requested: bool = False
    ranking_requested: bool = False
    portfolio_requested: bool = False
    optimization_requested: bool = False
    production_requested: bool = False
    ml_requested: bool = False
    report_generation_requested: bool = False


@dataclass(frozen=True)
class ValidationInterpretationIdentity:
    validation_interpretation_id: str
    validation_readiness_id: str
    empirical_artifact_id: str
    evidence_package_id: str
    implementation_id: str
    implementation_version: str
    design_id: str
    interpretation_version: str
    reporting_version: str
    validation_protocol_version: str
    interpretation_state: ValidationInterpretationState
    acceptance_representation: AcceptanceRepresentation


@dataclass(frozen=True)
class ValidationInterpretationDiagnostics:
    codes: tuple[ValidationInterpretationDiagnosticCode, ...]
    entries: tuple[dict[str, str], ...]


@dataclass(frozen=True)
class ValidationInterpretationLimitations:
    codes: tuple[str, ...]


@dataclass(frozen=True)
class ValidationInterpretationLineage:
    lineage_chain: tuple[str, ...]
    upstream_artifacts: dict[str, Any]
    validation_readiness_artifact: str
    completed_empirical_evaluation_artifact: str
    validation_interpretation_artifact: str
    candidate_artifact: str = ""
    panel_artifact: str = ""
    portfolio_artifact: str = ""
    production_artifact: str = ""
    optimization_artifact: str = ""
    ml_artifact: str = ""


@dataclass(frozen=True)
class ValidationInterpretationReproducibility:
    interpretation_version: str
    reporting_version: str
    validation_protocol_version: str
    execution_version: str
    reproducibility_version: str
    serialization_version: str
    validation_readiness_artifact: str
    empirical_artifact_id: str
    evidence_package_id: str
    reporting_protocol: str
    deterministic_interpretation_identity: str


@dataclass(frozen=True)
class ValidationInterpretationInformationContract:
    exposes_interpretation_state: bool = True
    exposes_diagnostics: bool = True
    exposes_limitations: bool = True
    exposes_interpretation_metadata: bool = True
    exposes_reporting_metadata: bool = True
    exposes_lineage: bool = True
    exposes_reproducibility: bool = True
    exposes_sharpe: bool = False
    exposes_ic: bool = False
    exposes_alpha: bool = False
    exposes_prediction: bool = False
    exposes_ranking: bool = False
    exposes_portfolio: bool = False
    exposes_validation_statistics: bool = False
    generates_reports: bool = False
    makes_production_recommendations: bool = False
    performs_optimization: bool = False
    exposes_ml_outputs: bool = False


@dataclass(frozen=True)
class ValidationInterpretationResult:
    validation_interpretation_id: str
    interpretation_state: ValidationInterpretationState
    acceptance_representation: AcceptanceRepresentation
    evidence_classification: EvidenceClassification
    diagnostics: ValidationInterpretationDiagnostics
    limitations: ValidationInterpretationLimitations
    identity: ValidationInterpretationIdentity
    lineage: ValidationInterpretationLineage
    reproducibility: ValidationInterpretationReproducibility
    information_contract: ValidationInterpretationInformationContract
    empirical_evidence_metadata: CompletedEmpiricalEvidenceMetadata
    reporting_governance: ReportingGovernanceMetadata
    final_classification: str = FINAL_CLASSIFICATION
    empirical_evaluation_performed: bool = False
    statistical_testing_performed: bool = False
    validation_metrics_calculated: bool = False
    alpha_quality_evaluated: bool = False
    sharpe_calculated: bool = False
    ic_calculated: bool = False
    prediction_created: bool = False
    ranking_created: bool = False
    portfolio_created: bool = False
    report_generated: bool = False
    production_logic_performed: bool = False
    optimization_performed: bool = False
    ml_feature_created: bool = False
    ml_label_created: bool = False
    model_training_performed: bool = False

    def to_ordered_dict(self) -> dict[str, Any]:
        return _to_jsonable(self)

    def stable_json(self) -> str:
        return _stable_json(self.to_ordered_dict())


@dataclass(frozen=True)
class ValidationInterpretationFixture:
    fixture_id: str
    description: str
    request: ValidationInterpretationRequest
    expected_state: ValidationInterpretationState
    expected_diagnostic_codes: tuple[ValidationInterpretationDiagnosticCode, ...] = ()
    expected_limitations: tuple[str, ...] = ()


def _diagnostic(code: ValidationInterpretationDiagnosticCode, stage: str, message: str) -> dict[str, str]:
    return {"code": code.value, "message": message, "stage": stage}


def _append_diagnostic(
    diagnostics: list[dict[str, str]],
    code: ValidationInterpretationDiagnosticCode,
    stage: str,
    message: str,
) -> None:
    diagnostics.append(_diagnostic(code, stage, message))


def _ordered_diagnostics(entries: list[dict[str, str]]) -> tuple[dict[str, str], ...]:
    return tuple(sorted(entries, key=lambda item: (item["code"], item["stage"], item["message"])))


def _add_limitations(limitations: list[str], *codes: str) -> None:
    for code in codes:
        if code not in limitations:
            limitations.append(code)


def _metadata_complete(*values: str) -> bool:
    return all(bool(value) for value in values)


def _registration_authoritative(registration: ValidationInterpretationRegistration) -> bool:
    return (
        registration.implementation_id == MODULE_ID
        and registration.implementation_version == MODULE_VERSION
        and registration.design_id == DESIGN_ID
        and registration.selected_module_id == SELECTED_MODULE_ID
        and registration.interpretation_version == INTERPRETATION_VERSION
        and registration.reporting_version == REPORTING_VERSION
        and registration.validation_protocol_version == VALIDATION_PROTOCOL_VERSION
        and registration.validation_interpretation_schema_version == VALIDATION_INTERPRETATION_SCHEMA_VERSION
        and registration.reproducibility_schema_version == REPRODUCIBILITY_SCHEMA_VERSION
        and registration.stable_serialization_version == STABLE_SERIALIZATION_VERSION
        and registration.performs_empirical_evaluation is False
        and registration.performs_statistical_testing is False
        and registration.calculates_validation_metrics is False
        and registration.evaluates_alpha_quality is False
        and registration.generates_reports is False
        and registration.supports_production is False
        and registration.supports_optimization is False
        and registration.supports_ml is False
    )


def _downstream_requested(request: ValidationInterpretationRequest) -> bool:
    return any(
        (
            request.empirical_evaluation_requested,
            request.statistical_testing_requested,
            request.validation_metrics_requested,
            request.alpha_evaluation_requested,
            request.sharpe_requested,
            request.ic_requested,
            request.prediction_requested,
            request.ranking_requested,
            request.portfolio_requested,
            request.optimization_requested,
            request.production_requested,
            request.ml_requested,
            request.report_generation_requested,
        )
    )


def _readiness_compatible(result: validation_readiness.ValidationReadinessResult | None) -> bool:
    if result is None:
        return False
    return result.readiness_state in (
        validation_readiness.ValidationReadinessState.READY,
        validation_readiness.ValidationReadinessState.CONDITIONALLY_READY,
    )


def _readiness_lineage_complete(result: validation_readiness.ValidationReadinessResult | None) -> bool:
    if result is None:
        return False
    return bool(result.lineage.validation_readiness_artifact) and bool(result.lineage.scientific_execution_artifact)


def _readiness_reproducibility_complete(result: validation_readiness.ValidationReadinessResult | None) -> bool:
    if result is None:
        return False
    repro = result.reproducibility
    return _metadata_complete(
        repro.validation_protocol_version,
        repro.execution_version,
        repro.reproducibility_version,
        repro.serialization_version,
        repro.deterministic_readiness_identity,
    )


def _negative_evidence_preserved(evidence: CompletedEmpiricalEvidenceMetadata) -> bool:
    return all(
        (
            evidence.failures_preserved,
            evidence.null_findings_preserved,
            evidence.negative_findings_preserved,
            evidence.contradictory_evidence_preserved,
            evidence.historical_failures_reconstructable,
        )
    )


def _reporting_complete(reporting: ReportingGovernanceMetadata) -> tuple[ValidationInterpretationDiagnosticCode, ...]:
    failures: list[ValidationInterpretationDiagnosticCode] = []
    if not reporting.reporting_protocol:
        failures.append(ValidationInterpretationDiagnosticCode.MISSING_REPORTING_PROTOCOL)
    if not _metadata_complete(
        reporting.report_identity,
        reporting.report_version,
        reporting.interpretation_version,
        reporting.evidence_version,
        reporting.review_status,
    ):
        failures.append(ValidationInterpretationDiagnosticCode.MISSING_REPORTING_METADATA)
    return tuple(failures)


def _build_identity_payload(
    request: ValidationInterpretationRequest,
    interpretation_state: ValidationInterpretationState,
    acceptance: AcceptanceRepresentation,
) -> dict[str, Any]:
    readiness_result = request.validation_readiness_result
    readiness_id = "" if readiness_result is None else readiness_result.validation_readiness_id
    evidence = request.empirical_evidence
    reporting = request.reporting_governance
    return {
        "fixture_id": request.fixture_id,
        "validation_readiness_id": readiness_id,
        "empirical_artifact_id": evidence.empirical_artifact_id,
        "evidence_package_id": evidence.evidence_package_id,
        "evidence_classification": evidence.evidence_classification.value,
        "implementation_id": request.registration.implementation_id,
        "implementation_version": request.registration.implementation_version,
        "design_id": request.registration.design_id,
        "interpretation_version": request.registration.interpretation_version,
        "reporting_version": reporting.report_version,
        "validation_protocol_version": request.registration.validation_protocol_version,
        "interpretation_state": interpretation_state.value,
        "acceptance_representation": acceptance.value,
    }


def _acceptance_for_state(state: ValidationInterpretationState) -> AcceptanceRepresentation:
    if state == ValidationInterpretationState.INTERPRETATION_SUPPORTED:
        return AcceptanceRepresentation.ACCEPTED_FOR_CONTINUED_RESEARCH
    if state == ValidationInterpretationState.INTERPRETATION_CONDITIONALLY_SUPPORTED:
        return AcceptanceRepresentation.REQUIRES_ADDITIONAL_INVESTIGATION
    if state == ValidationInterpretationState.INTERPRETATION_NOT_SUPPORTED:
        return AcceptanceRepresentation.REJECTED_FOR_CURRENT_HYPOTHESIS
    if state == ValidationInterpretationState.INTERPRETATION_EXCLUDED:
        return AcceptanceRepresentation.EXCLUDED
    return AcceptanceRepresentation.UNRESOLVED


def _lineage_payload(
    readiness_result: validation_readiness.ValidationReadinessResult | None,
    empirical_artifact_id: str,
    validation_interpretation_id: str,
) -> ValidationInterpretationLineage:
    if readiness_result is None:
        upstream = {}
        readiness_artifact = ""
    else:
        upstream = dict(readiness_result.lineage.upstream_artifacts)
        upstream["validation_readiness_artifact"] = readiness_result.validation_readiness_id
        readiness_artifact = readiness_result.validation_readiness_id
    return ValidationInterpretationLineage(
        lineage_chain=LINEAGE_CHAIN,
        upstream_artifacts=upstream,
        validation_readiness_artifact=readiness_artifact,
        completed_empirical_evaluation_artifact=empirical_artifact_id,
        validation_interpretation_artifact=validation_interpretation_id,
    )


def evaluate_validation_interpretation(request: ValidationInterpretationRequest) -> ValidationInterpretationResult:
    diagnostics: list[dict[str, str]] = []
    limitations: list[str] = list(REFERENCE_LIMITATIONS)
    readiness_result = request.validation_readiness_result
    evidence = request.empirical_evidence
    reporting = request.reporting_governance

    if request.excluded or _downstream_requested(request) or not _registration_authoritative(request.registration):
        _append_diagnostic(
            diagnostics,
            ValidationInterpretationDiagnosticCode.VALIDATION_INTERPRETATION_EXCLUDED,
            "scope",
            "Request is outside the validation-interpretation reference implementation boundary.",
        )
    if _downstream_requested(request):
        _append_diagnostic(
            diagnostics,
            ValidationInterpretationDiagnosticCode.DOWNSTREAM_SCOPE_PROHIBITED,
            "scope",
            "Empirical evaluation, statistics, reports, production, optimization, and ML are prohibited.",
        )

    if readiness_result is None:
        _append_diagnostic(
            diagnostics,
            ValidationInterpretationDiagnosticCode.VALIDATION_READINESS_ARTIFACT_MISSING,
            "readiness",
            "Validation interpretation requires a validation-readiness artifact.",
        )
    elif not _readiness_compatible(readiness_result):
        _append_diagnostic(
            diagnostics,
            ValidationInterpretationDiagnosticCode.INCOMPATIBLE_READINESS_ARTIFACT,
            "readiness",
            "Validation-readiness artifact is not ready for completed-evidence interpretation.",
        )

    if not evidence.empirical_artifact_id or not evidence.evidence_package_id:
        _append_diagnostic(
            diagnostics,
            ValidationInterpretationDiagnosticCode.EMPIRICAL_ARTIFACT_MISSING,
            "empirical_evidence",
            "Completed empirical-evaluation artifact identity or evidence package identity is missing.",
        )
    if not evidence.evaluation_completed:
        _append_diagnostic(
            diagnostics,
            ValidationInterpretationDiagnosticCode.EMPIRICAL_EVALUATION_NOT_COMPLETE,
            "empirical_evidence",
            "Empirical evaluation completion metadata is false.",
        )
    if not _metadata_complete(evidence.protocol_identity, evidence.benchmark_identity) or not evidence.interpretation_metadata_complete:
        _append_diagnostic(
            diagnostics,
            ValidationInterpretationDiagnosticCode.MISSING_INTERPRETATION_METADATA,
            "empirical_evidence",
            "Required protocol, benchmark, or interpretation metadata is missing.",
        )
    if not evidence.evidence_complete:
        _append_diagnostic(
            diagnostics,
            ValidationInterpretationDiagnosticCode.INSUFFICIENT_INTERPRETATION_EVIDENCE,
            "empirical_evidence",
            "Evidence package is incomplete for interpretation.",
        )
        _add_limitations(limitations, INSUFFICIENT_LIMITATION)
    if not evidence.evidence_consistent:
        _append_diagnostic(
            diagnostics,
            ValidationInterpretationDiagnosticCode.INCONSISTENT_EVIDENCE_PACKAGE,
            "empirical_evidence",
            "Evidence package is internally inconsistent.",
        )
    if not evidence.reproducibility_confirmed:
        _append_diagnostic(
            diagnostics,
            ValidationInterpretationDiagnosticCode.INCOMPLETE_REPRODUCIBILITY,
            "empirical_evidence",
            "Completed evidence package lacks reproducibility confirmation.",
        )
    if not evidence.reporting_complete:
        _append_diagnostic(
            diagnostics,
            ValidationInterpretationDiagnosticCode.MISSING_REPORTING_METADATA,
            "reporting",
            "Evidence package is not reporting-complete.",
        )
    if not evidence.lineage_complete or not _readiness_lineage_complete(readiness_result):
        _append_diagnostic(
            diagnostics,
            ValidationInterpretationDiagnosticCode.INCOMPLETE_LINEAGE,
            "lineage",
            "Required upstream-to-interpretation lineage is incomplete.",
        )
    if not _readiness_reproducibility_complete(readiness_result):
        _append_diagnostic(
            diagnostics,
            ValidationInterpretationDiagnosticCode.INCOMPLETE_REPRODUCIBILITY,
            "reproducibility",
            "Required readiness-to-interpretation reproducibility metadata is incomplete.",
        )

    for code in _reporting_complete(reporting):
        _append_diagnostic(diagnostics, code, "reporting", "Required reporting governance metadata is missing.")
    if not _negative_evidence_preserved(evidence):
        _append_diagnostic(
            diagnostics,
            ValidationInterpretationDiagnosticCode.NEGATIVE_EVIDENCE_NOT_PRESERVED,
            "negative_evidence",
            "Failures, null findings, negative findings, contradictory evidence, or historical failures are not fully preserved.",
        )
        _add_limitations(limitations, INSUFFICIENT_LIMITATION)
    if request.conditional_limitations or evidence.conditional_support:
        _append_diagnostic(
            diagnostics,
            ValidationInterpretationDiagnosticCode.CONDITIONAL_INTERPRETATION_LIMITATION,
            "conditional_interpretation",
            "Conditional support metadata is present and must remain visible.",
        )
        _add_limitations(limitations, CONDITIONAL_LIMITATION, *request.conditional_limitations)

    if evidence.evidence_classification == EvidenceClassification.UNRESOLVED:
        _append_diagnostic(
            diagnostics,
            ValidationInterpretationDiagnosticCode.UNRESOLVED_EVALUATION,
            "empirical_evidence",
            "Completed evidence remains unresolved under the interpretation protocol.",
        )
        _add_limitations(limitations, UNRESOLVED_LIMITATION)
    if evidence.evidence_classification == EvidenceClassification.INSUFFICIENT:
        _append_diagnostic(
            diagnostics,
            ValidationInterpretationDiagnosticCode.INSUFFICIENT_INTERPRETATION_EVIDENCE,
            "empirical_evidence",
            "Evidence classification is insufficient.",
        )
        _add_limitations(limitations, INSUFFICIENT_LIMITATION)
    if evidence.evidence_classification in (
        EvidenceClassification.CONFLICTING,
        EvidenceClassification.NULL,
        EvidenceClassification.NEGATIVE,
    ):
        _append_diagnostic(
            diagnostics,
            ValidationInterpretationDiagnosticCode.INTERPRETATION_NOT_SUPPORTED,
            "empirical_evidence",
            "Completed evidence does not support the current hypothesis interpretation.",
        )
        _add_limitations(limitations, NEGATIVE_LIMITATION)

    diagnostic_entries = _ordered_diagnostics(diagnostics)
    diagnostic_codes = tuple(ValidationInterpretationDiagnosticCode(entry["code"]) for entry in diagnostic_entries)

    if ValidationInterpretationDiagnosticCode.VALIDATION_INTERPRETATION_EXCLUDED in diagnostic_codes:
        interpretation_state = ValidationInterpretationState.INTERPRETATION_EXCLUDED
    elif any(
        code in diagnostic_codes
        for code in (
            ValidationInterpretationDiagnosticCode.VALIDATION_READINESS_ARTIFACT_MISSING,
            ValidationInterpretationDiagnosticCode.INCOMPATIBLE_READINESS_ARTIFACT,
            ValidationInterpretationDiagnosticCode.EMPIRICAL_ARTIFACT_MISSING,
            ValidationInterpretationDiagnosticCode.EMPIRICAL_EVALUATION_NOT_COMPLETE,
            ValidationInterpretationDiagnosticCode.MISSING_INTERPRETATION_METADATA,
            ValidationInterpretationDiagnosticCode.MISSING_REPORTING_PROTOCOL,
            ValidationInterpretationDiagnosticCode.MISSING_REPORTING_METADATA,
            ValidationInterpretationDiagnosticCode.INCOMPLETE_LINEAGE,
            ValidationInterpretationDiagnosticCode.INCOMPLETE_REPRODUCIBILITY,
            ValidationInterpretationDiagnosticCode.NEGATIVE_EVIDENCE_NOT_PRESERVED,
            ValidationInterpretationDiagnosticCode.INSUFFICIENT_INTERPRETATION_EVIDENCE,
        )
    ):
        interpretation_state = ValidationInterpretationState.INSUFFICIENT_INTERPRETATION_EVIDENCE
    elif ValidationInterpretationDiagnosticCode.INCONSISTENT_EVIDENCE_PACKAGE in diagnostic_codes:
        interpretation_state = ValidationInterpretationState.INTERPRETATION_UNRESOLVED
    elif ValidationInterpretationDiagnosticCode.UNRESOLVED_EVALUATION in diagnostic_codes:
        interpretation_state = ValidationInterpretationState.INTERPRETATION_UNRESOLVED
    elif ValidationInterpretationDiagnosticCode.INTERPRETATION_NOT_SUPPORTED in diagnostic_codes:
        interpretation_state = ValidationInterpretationState.INTERPRETATION_NOT_SUPPORTED
    elif (
        ValidationInterpretationDiagnosticCode.CONDITIONAL_INTERPRETATION_LIMITATION in diagnostic_codes
        or evidence.evidence_classification == EvidenceClassification.MIXED
    ):
        interpretation_state = ValidationInterpretationState.INTERPRETATION_CONDITIONALLY_SUPPORTED
    else:
        interpretation_state = ValidationInterpretationState.INTERPRETATION_SUPPORTED

    acceptance = _acceptance_for_state(interpretation_state)
    validation_interpretation_id = _stable_digest(_build_identity_payload(request, interpretation_state, acceptance), "validation_interpretation")
    readiness_id = "" if readiness_result is None else readiness_result.validation_readiness_id
    identity = ValidationInterpretationIdentity(
        validation_interpretation_id=validation_interpretation_id,
        validation_readiness_id=readiness_id,
        empirical_artifact_id=evidence.empirical_artifact_id,
        evidence_package_id=evidence.evidence_package_id,
        implementation_id=request.registration.implementation_id,
        implementation_version=request.registration.implementation_version,
        design_id=request.registration.design_id,
        interpretation_version=request.registration.interpretation_version,
        reporting_version=reporting.report_version,
        validation_protocol_version=request.registration.validation_protocol_version,
        interpretation_state=interpretation_state,
        acceptance_representation=acceptance,
    )
    lineage = _lineage_payload(readiness_result, evidence.empirical_artifact_id, validation_interpretation_id)
    reproducibility = ValidationInterpretationReproducibility(
        interpretation_version=request.registration.interpretation_version,
        reporting_version=reporting.report_version,
        validation_protocol_version=request.registration.validation_protocol_version,
        execution_version="" if readiness_result is None else readiness_result.reproducibility.execution_version,
        reproducibility_version=REPRODUCIBILITY_SCHEMA_VERSION,
        serialization_version=request.registration.stable_serialization_version,
        validation_readiness_artifact=readiness_id,
        empirical_artifact_id=evidence.empirical_artifact_id,
        evidence_package_id=evidence.evidence_package_id,
        reporting_protocol=reporting.reporting_protocol,
        deterministic_interpretation_identity=validation_interpretation_id,
    )

    return ValidationInterpretationResult(
        validation_interpretation_id=validation_interpretation_id,
        interpretation_state=interpretation_state,
        acceptance_representation=acceptance,
        evidence_classification=evidence.evidence_classification,
        diagnostics=ValidationInterpretationDiagnostics(codes=diagnostic_codes, entries=diagnostic_entries),
        limitations=ValidationInterpretationLimitations(codes=tuple(limitations)),
        identity=identity,
        lineage=lineage,
        reproducibility=reproducibility,
        information_contract=ValidationInterpretationInformationContract(),
        empirical_evidence_metadata=evidence,
        reporting_governance=reporting,
    )


@lru_cache(maxsize=None)
def _ready_readiness_result(fixture_id: str = "VR01_ready") -> validation_readiness.ValidationReadinessResult:
    fixtures = {fixture.fixture_id: fixture for fixture in validation_readiness.canonical_validation_readiness_fixtures()}
    return validation_readiness.evaluate_validation_readiness(fixtures[fixture_id].request)


def _fixture(
    fixture_id: str,
    description: str,
    expected_state: ValidationInterpretationState,
    expected_diagnostic_codes: tuple[ValidationInterpretationDiagnosticCode, ...] = (),
    expected_limitations: tuple[str, ...] = (),
    readiness_result: validation_readiness.ValidationReadinessResult | None | str = "ready",
    empirical_evidence: CompletedEmpiricalEvidenceMetadata | None = None,
    reporting_governance: ReportingGovernanceMetadata | None = None,
    **request_overrides: Any,
) -> ValidationInterpretationFixture:
    if readiness_result == "ready":
        readiness = _ready_readiness_result()
    elif isinstance(readiness_result, str):
        readiness = _ready_readiness_result(readiness_result)
    else:
        readiness = readiness_result
    request = ValidationInterpretationRequest(
        validation_readiness_result=readiness,
        empirical_evidence=CompletedEmpiricalEvidenceMetadata() if empirical_evidence is None else empirical_evidence,
        reporting_governance=ReportingGovernanceMetadata() if reporting_governance is None else reporting_governance,
        fixture_id=fixture_id,
        **request_overrides,
    )
    return ValidationInterpretationFixture(
        fixture_id=fixture_id,
        description=description,
        request=request,
        expected_state=expected_state,
        expected_diagnostic_codes=expected_diagnostic_codes,
        expected_limitations=expected_limitations,
    )


def canonical_validation_interpretation_fixtures() -> tuple[ValidationInterpretationFixture, ...]:
    ready = _ready_readiness_result()
    missing_lineage_readiness = replace(ready, lineage=replace(ready.lineage, validation_readiness_artifact=""))
    missing_repro_readiness = replace(ready, reproducibility=replace(ready.reproducibility, deterministic_readiness_identity=""))
    fixtures = [
        _fixture("VI01_supported", "Supporting completed evidence.", ValidationInterpretationState.INTERPRETATION_SUPPORTED),
        _fixture(
            "VI02_conditionally_supported",
            "Conditional support remains bounded.",
            ValidationInterpretationState.INTERPRETATION_CONDITIONALLY_SUPPORTED,
            (ValidationInterpretationDiagnosticCode.CONDITIONAL_INTERPRETATION_LIMITATION,),
            (CONDITIONAL_LIMITATION, "bounded_followup_required"),
            empirical_evidence=CompletedEmpiricalEvidenceMetadata(conditional_support=True),
            conditional_limitations=("bounded_followup_required",),
        ),
        _fixture(
            "VI03_mixed_evidence",
            "Mixed evidence is conditionally supported.",
            ValidationInterpretationState.INTERPRETATION_CONDITIONALLY_SUPPORTED,
            empirical_evidence=CompletedEmpiricalEvidenceMetadata(evidence_classification=EvidenceClassification.MIXED),
        ),
        _fixture(
            "VI04_unresolved_evidence",
            "Unresolved evidence remains unresolved.",
            ValidationInterpretationState.INTERPRETATION_UNRESOLVED,
            (ValidationInterpretationDiagnosticCode.UNRESOLVED_EVALUATION,),
            (UNRESOLVED_LIMITATION,),
            empirical_evidence=CompletedEmpiricalEvidenceMetadata(evidence_classification=EvidenceClassification.UNRESOLVED),
        ),
        _fixture(
            "VI05_not_supported_negative",
            "Negative evidence rejects current interpretation.",
            ValidationInterpretationState.INTERPRETATION_NOT_SUPPORTED,
            (ValidationInterpretationDiagnosticCode.INTERPRETATION_NOT_SUPPORTED,),
            (NEGATIVE_LIMITATION,),
            empirical_evidence=CompletedEmpiricalEvidenceMetadata(evidence_classification=EvidenceClassification.NEGATIVE),
        ),
        _fixture(
            "VI06_not_supported_null",
            "Null findings reject current support claim.",
            ValidationInterpretationState.INTERPRETATION_NOT_SUPPORTED,
            (ValidationInterpretationDiagnosticCode.INTERPRETATION_NOT_SUPPORTED,),
            (NEGATIVE_LIMITATION,),
            empirical_evidence=CompletedEmpiricalEvidenceMetadata(evidence_classification=EvidenceClassification.NULL),
        ),
        _fixture(
            "VI07_not_supported_conflicting",
            "Conflicting evidence is not support.",
            ValidationInterpretationState.INTERPRETATION_NOT_SUPPORTED,
            (ValidationInterpretationDiagnosticCode.INTERPRETATION_NOT_SUPPORTED,),
            (NEGATIVE_LIMITATION,),
            empirical_evidence=CompletedEmpiricalEvidenceMetadata(evidence_classification=EvidenceClassification.CONFLICTING),
        ),
        _fixture(
            "VI08_excluded_request",
            "Excluded request refuses interpretation.",
            ValidationInterpretationState.INTERPRETATION_EXCLUDED,
            (ValidationInterpretationDiagnosticCode.VALIDATION_INTERPRETATION_EXCLUDED,),
            excluded=True,
        ),
        _fixture(
            "VI09_downstream_scope_request",
            "Downstream requests are excluded.",
            ValidationInterpretationState.INTERPRETATION_EXCLUDED,
            (
                ValidationInterpretationDiagnosticCode.VALIDATION_INTERPRETATION_EXCLUDED,
                ValidationInterpretationDiagnosticCode.DOWNSTREAM_SCOPE_PROHIBITED,
            ),
            statistical_testing_requested=True,
            production_requested=True,
        ),
        _fixture(
            "VI10_missing_readiness_artifact",
            "Missing readiness artifact is insufficient.",
            ValidationInterpretationState.INSUFFICIENT_INTERPRETATION_EVIDENCE,
            (ValidationInterpretationDiagnosticCode.VALIDATION_READINESS_ARTIFACT_MISSING,),
            readiness_result=None,
        ),
        _fixture(
            "VI11_readiness_not_ready",
            "Non-ready readiness artifact is incompatible.",
            ValidationInterpretationState.INSUFFICIENT_INTERPRETATION_EVIDENCE,
            (ValidationInterpretationDiagnosticCode.INCOMPATIBLE_READINESS_ARTIFACT,),
            readiness_result="VR06_missing_protocol",
        ),
        _fixture(
            "VI12_missing_empirical_artifact",
            "Missing completed evidence identity fails closed.",
            ValidationInterpretationState.INSUFFICIENT_INTERPRETATION_EVIDENCE,
            (ValidationInterpretationDiagnosticCode.EMPIRICAL_ARTIFACT_MISSING,),
            empirical_evidence=CompletedEmpiricalEvidenceMetadata(empirical_artifact_id=""),
        ),
        _fixture(
            "VI13_missing_evidence_package",
            "Missing evidence package identity fails closed.",
            ValidationInterpretationState.INSUFFICIENT_INTERPRETATION_EVIDENCE,
            (ValidationInterpretationDiagnosticCode.EMPIRICAL_ARTIFACT_MISSING,),
            empirical_evidence=CompletedEmpiricalEvidenceMetadata(evidence_package_id=""),
        ),
        _fixture(
            "VI14_evaluation_not_complete",
            "Incomplete empirical evaluation cannot be interpreted.",
            ValidationInterpretationState.INSUFFICIENT_INTERPRETATION_EVIDENCE,
            (ValidationInterpretationDiagnosticCode.EMPIRICAL_EVALUATION_NOT_COMPLETE,),
            empirical_evidence=CompletedEmpiricalEvidenceMetadata(evaluation_completed=False),
        ),
        _fixture(
            "VI15_missing_protocol_identity",
            "Missing protocol identity is missing interpretation metadata.",
            ValidationInterpretationState.INSUFFICIENT_INTERPRETATION_EVIDENCE,
            (ValidationInterpretationDiagnosticCode.MISSING_INTERPRETATION_METADATA,),
            empirical_evidence=CompletedEmpiricalEvidenceMetadata(protocol_identity=""),
        ),
        _fixture(
            "VI16_missing_benchmark_identity",
            "Missing benchmark identity is missing interpretation metadata.",
            ValidationInterpretationState.INSUFFICIENT_INTERPRETATION_EVIDENCE,
            (ValidationInterpretationDiagnosticCode.MISSING_INTERPRETATION_METADATA,),
            empirical_evidence=CompletedEmpiricalEvidenceMetadata(benchmark_identity=""),
        ),
        _fixture(
            "VI17_incomplete_evidence",
            "Incomplete evidence is insufficient.",
            ValidationInterpretationState.INSUFFICIENT_INTERPRETATION_EVIDENCE,
            (ValidationInterpretationDiagnosticCode.INSUFFICIENT_INTERPRETATION_EVIDENCE,),
            (INSUFFICIENT_LIMITATION,),
            empirical_evidence=CompletedEmpiricalEvidenceMetadata(evidence_complete=False),
        ),
        _fixture(
            "VI18_inconsistent_evidence",
            "Inconsistent evidence remains unresolved.",
            ValidationInterpretationState.INTERPRETATION_UNRESOLVED,
            (ValidationInterpretationDiagnosticCode.INCONSISTENT_EVIDENCE_PACKAGE,),
            empirical_evidence=CompletedEmpiricalEvidenceMetadata(evidence_consistent=False),
        ),
        _fixture(
            "VI19_missing_reporting_protocol",
            "Missing reporting protocol is insufficient.",
            ValidationInterpretationState.INSUFFICIENT_INTERPRETATION_EVIDENCE,
            (ValidationInterpretationDiagnosticCode.MISSING_REPORTING_PROTOCOL,),
            reporting_governance=ReportingGovernanceMetadata(reporting_protocol=""),
        ),
        _fixture(
            "VI20_missing_reporting_metadata",
            "Missing report identity is insufficient.",
            ValidationInterpretationState.INSUFFICIENT_INTERPRETATION_EVIDENCE,
            (ValidationInterpretationDiagnosticCode.MISSING_REPORTING_METADATA,),
            reporting_governance=ReportingGovernanceMetadata(report_identity=""),
        ),
        _fixture(
            "VI21_missing_interpretation_metadata",
            "Missing interpretation metadata is insufficient.",
            ValidationInterpretationState.INSUFFICIENT_INTERPRETATION_EVIDENCE,
            (ValidationInterpretationDiagnosticCode.MISSING_INTERPRETATION_METADATA,),
            empirical_evidence=CompletedEmpiricalEvidenceMetadata(interpretation_metadata_complete=False),
        ),
        _fixture(
            "VI22_incomplete_lineage",
            "Incomplete empirical lineage is insufficient.",
            ValidationInterpretationState.INSUFFICIENT_INTERPRETATION_EVIDENCE,
            (ValidationInterpretationDiagnosticCode.INCOMPLETE_LINEAGE,),
            empirical_evidence=CompletedEmpiricalEvidenceMetadata(lineage_complete=False),
        ),
        _fixture(
            "VI23_incomplete_readiness_lineage",
            "Incomplete readiness lineage is insufficient.",
            ValidationInterpretationState.INSUFFICIENT_INTERPRETATION_EVIDENCE,
            (ValidationInterpretationDiagnosticCode.INCOMPLETE_LINEAGE,),
            readiness_result=missing_lineage_readiness,
        ),
        _fixture(
            "VI24_incomplete_reproducibility",
            "Incomplete evidence reproducibility is insufficient.",
            ValidationInterpretationState.INSUFFICIENT_INTERPRETATION_EVIDENCE,
            (ValidationInterpretationDiagnosticCode.INCOMPLETE_REPRODUCIBILITY,),
            empirical_evidence=CompletedEmpiricalEvidenceMetadata(reproducibility_confirmed=False),
        ),
        _fixture(
            "VI25_incomplete_readiness_reproducibility",
            "Incomplete readiness reproducibility is insufficient.",
            ValidationInterpretationState.INSUFFICIENT_INTERPRETATION_EVIDENCE,
            (ValidationInterpretationDiagnosticCode.INCOMPLETE_REPRODUCIBILITY,),
            readiness_result=missing_repro_readiness,
        ),
        _fixture(
            "VI26_reporting_incomplete",
            "Evidence package not reporting-complete is insufficient.",
            ValidationInterpretationState.INSUFFICIENT_INTERPRETATION_EVIDENCE,
            (ValidationInterpretationDiagnosticCode.MISSING_REPORTING_METADATA,),
            empirical_evidence=CompletedEmpiricalEvidenceMetadata(reporting_complete=False),
        ),
        _fixture(
            "VI27_negative_evidence_not_preserved",
            "Negative evidence preservation is mandatory.",
            ValidationInterpretationState.INSUFFICIENT_INTERPRETATION_EVIDENCE,
            (ValidationInterpretationDiagnosticCode.NEGATIVE_EVIDENCE_NOT_PRESERVED,),
            (INSUFFICIENT_LIMITATION,),
            empirical_evidence=CompletedEmpiricalEvidenceMetadata(null_findings_preserved=False),
        ),
        _fixture(
            "VI28_contradictory_evidence_not_preserved",
            "Contradictory evidence preservation is mandatory.",
            ValidationInterpretationState.INSUFFICIENT_INTERPRETATION_EVIDENCE,
            (ValidationInterpretationDiagnosticCode.NEGATIVE_EVIDENCE_NOT_PRESERVED,),
            (INSUFFICIENT_LIMITATION,),
            empirical_evidence=CompletedEmpiricalEvidenceMetadata(contradictory_evidence_preserved=False),
        ),
        _fixture(
            "VI29_historical_failures_not_reconstructable",
            "Historical failures must remain reconstructable.",
            ValidationInterpretationState.INSUFFICIENT_INTERPRETATION_EVIDENCE,
            (ValidationInterpretationDiagnosticCode.NEGATIVE_EVIDENCE_NOT_PRESERVED,),
            (INSUFFICIENT_LIMITATION,),
            empirical_evidence=CompletedEmpiricalEvidenceMetadata(historical_failures_reconstructable=False),
        ),
        _fixture(
            "VI30_insufficient_evidence_class",
            "Insufficient evidence classification is insufficient.",
            ValidationInterpretationState.INSUFFICIENT_INTERPRETATION_EVIDENCE,
            (ValidationInterpretationDiagnosticCode.INSUFFICIENT_INTERPRETATION_EVIDENCE,),
            (INSUFFICIENT_LIMITATION,),
            empirical_evidence=CompletedEmpiricalEvidenceMetadata(evidence_classification=EvidenceClassification.INSUFFICIENT),
        ),
        _fixture(
            "VI31_combined_failures",
            "Combined failures accumulate and fail closed.",
            ValidationInterpretationState.INSUFFICIENT_INTERPRETATION_EVIDENCE,
            (
                ValidationInterpretationDiagnosticCode.MISSING_REPORTING_PROTOCOL,
                ValidationInterpretationDiagnosticCode.INCOMPLETE_LINEAGE,
                ValidationInterpretationDiagnosticCode.NEGATIVE_EVIDENCE_NOT_PRESERVED,
                ValidationInterpretationDiagnosticCode.INSUFFICIENT_INTERPRETATION_EVIDENCE,
            ),
            (INSUFFICIENT_LIMITATION,),
            empirical_evidence=CompletedEmpiricalEvidenceMetadata(
                evidence_complete=False,
                lineage_complete=False,
                failures_preserved=False,
            ),
            reporting_governance=ReportingGovernanceMetadata(reporting_protocol=""),
        ),
        _fixture(
            "VI32_excluded_combined_failures",
            "Exclusion takes precedence while diagnostics remain visible.",
            ValidationInterpretationState.INTERPRETATION_EXCLUDED,
            (
                ValidationInterpretationDiagnosticCode.VALIDATION_INTERPRETATION_EXCLUDED,
                ValidationInterpretationDiagnosticCode.EMPIRICAL_ARTIFACT_MISSING,
            ),
            excluded=True,
            empirical_evidence=CompletedEmpiricalEvidenceMetadata(empirical_artifact_id=""),
        ),
        _fixture(
            "VI33_conditional_does_not_override_missing_artifact",
            "Conditional support cannot override fatal missing artifacts.",
            ValidationInterpretationState.INSUFFICIENT_INTERPRETATION_EVIDENCE,
            (
                ValidationInterpretationDiagnosticCode.CONDITIONAL_INTERPRETATION_LIMITATION,
                ValidationInterpretationDiagnosticCode.EMPIRICAL_ARTIFACT_MISSING,
            ),
            (CONDITIONAL_LIMITATION,),
            empirical_evidence=CompletedEmpiricalEvidenceMetadata(empirical_artifact_id="", conditional_support=True),
        ),
        _fixture(
            "VI34_readiness_conditionally_ready",
            "Conditionally ready upstream artifact can support conditional interpretation metadata.",
            ValidationInterpretationState.INTERPRETATION_CONDITIONALLY_SUPPORTED,
            (ValidationInterpretationDiagnosticCode.CONDITIONAL_INTERPRETATION_LIMITATION,),
            (CONDITIONAL_LIMITATION, "upstream_condition_preserved"),
            readiness_result="VR02_conditionally_ready",
            conditional_limitations=("upstream_condition_preserved",),
        ),
        _fixture(
            "VI35_deterministic_repeat",
            "Repeat fixture for deterministic identity and serialization.",
            ValidationInterpretationState.INTERPRETATION_SUPPORTED,
        ),
    ]
    return tuple(fixtures)


def validation_interpretation_guardrail_manifest() -> dict[str, bool]:
    return {
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
