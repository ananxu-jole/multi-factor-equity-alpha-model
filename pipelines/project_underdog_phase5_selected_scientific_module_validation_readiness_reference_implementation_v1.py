from __future__ import annotations

from dataclasses import dataclass, field, is_dataclass, replace
from enum import Enum
import hashlib
import json
from typing import Any

from pipelines import project_underdog_phase5_selected_scientific_module_adapter_reference_implementation_v1 as adapter
from pipelines import project_underdog_phase5_selected_scientific_module_scientific_execution_reference_implementation_v1 as scientific_execution


MODULE_ID = "project_underdog_phase5_selected_scientific_module_validation_readiness_reference_implementation_v1"
MODULE_VERSION = "v1"
DESIGN_ID = "project_underdog_phase5_selected_scientific_module_validation_readiness_and_empirical_evaluation_design_v1"
FINAL_CLASSIFICATION = "VALIDATION_READINESS_REFERENCE_IMPLEMENTATION_COMPLETE"
VALIDATION_READINESS_SCHEMA_VERSION = "selected_module_validation_readiness_schema_v1"
REPRODUCIBILITY_SCHEMA_VERSION = "selected_module_validation_readiness_reproducibility_schema_v1"
STABLE_SERIALIZATION_VERSION = "stable_json_v1"
VALIDATION_PROTOCOL_VERSION = "selected_module_validation_readiness_protocol_v1"
EVALUATION_VERSION = "selected_module_empirical_evaluation_governance_v1"
SELECTED_MODULE_ID = scientific_execution.SELECTED_MODULE_ID
FORMULA_SPECIFICATION_ID = scientific_execution.FORMULA_SPECIFICATION_ID
FORMULA_VERSION = scientific_execution.FORMULA_VERSION
SCIENTIFIC_SPECIFICATION_ID = adapter.DEFAULT_SCIENTIFIC_SPECIFICATION_ID
SCIENTIFIC_SPECIFICATION_VERSION = adapter.DEFAULT_SCIENTIFIC_SPECIFICATION_VERSION
ACTIVATION_SPECIFICATION_ID = adapter.NARROW_ACTIVATION_SPECIFICATION_ID
ACTIVATION_SPECIFICATION_VERSION = adapter.NARROW_ACTIVATION_SPECIFICATION_VERSION
FROZEN_HORIZON_SPECIFICATION_ID = adapter.DEFAULT_FROZEN_HORIZON_SPECIFICATION_ID
FROZEN_HORIZON_SPECIFICATION_VERSION = adapter.DEFAULT_FROZEN_HORIZON_SPECIFICATION_VERSION


class ValidationReadinessState(str, Enum):
    READY = "VALIDATION_READY"
    CONDITIONALLY_READY = "VALIDATION_CONDITIONALLY_READY"
    UNRESOLVED = "VALIDATION_UNRESOLVED"
    NOT_READY = "VALIDATION_NOT_READY"
    EXCLUDED = "VALIDATION_EXCLUDED"
    INSUFFICIENT_EVIDENCE = "INSUFFICIENT_VALIDATION_EVIDENCE"


class ValidationReadinessDiagnosticCode(str, Enum):
    VALIDATION_READINESS_EXCLUDED = "VALIDATION_READINESS_EXCLUDED"
    SCIENTIFIC_EXECUTION_ARTIFACT_MISSING = "SCIENTIFIC_EXECUTION_ARTIFACT_MISSING"
    SCIENTIFIC_EXECUTION_NOT_COMPLETE = "SCIENTIFIC_EXECUTION_NOT_COMPLETE"
    FROZEN_SCIENTIFIC_SPECIFICATION_MISSING = "FROZEN_SCIENTIFIC_SPECIFICATION_MISSING"
    FROZEN_FORMULA_SPECIFICATION_MISSING = "FROZEN_FORMULA_SPECIFICATION_MISSING"
    FROZEN_ACTIVATION_SPECIFICATION_MISSING = "FROZEN_ACTIVATION_SPECIFICATION_MISSING"
    FROZEN_HORIZON_MISSING = "FROZEN_HORIZON_MISSING"
    SCIENTIFIC_DIAGNOSTICS_NOT_PRESERVED = "SCIENTIFIC_DIAGNOSTICS_NOT_PRESERVED"
    SCIENTIFIC_LIMITATIONS_NOT_PRESERVED = "SCIENTIFIC_LIMITATIONS_NOT_PRESERVED"
    MISSING_PROTOCOL = "MISSING_PROTOCOL"
    MISSING_BENCHMARK_DEFINITION = "MISSING_BENCHMARK_DEFINITION"
    MISSING_CONTAMINATION_POLICY = "MISSING_CONTAMINATION_POLICY"
    MISSING_FALSIFICATION_POLICY = "MISSING_FALSIFICATION_POLICY"
    MISSING_REPORTING_PROTOCOL = "MISSING_REPORTING_PROTOCOL"
    INCOMPATIBLE_SCIENTIFIC_SPECIFICATION = "INCOMPATIBLE_SCIENTIFIC_SPECIFICATION"
    INCOMPATIBLE_FORMULA_SPECIFICATION = "INCOMPATIBLE_FORMULA_SPECIFICATION"
    INCOMPATIBLE_ACTIVATION_SPECIFICATION = "INCOMPATIBLE_ACTIVATION_SPECIFICATION"
    INCOMPATIBLE_FROZEN_HORIZON = "INCOMPATIBLE_FROZEN_HORIZON"
    INCOMPLETE_LINEAGE = "INCOMPLETE_LINEAGE"
    MISSING_REPRODUCIBILITY_METADATA = "MISSING_REPRODUCIBILITY_METADATA"
    UNRESOLVED_SCIENTIFIC_EXECUTION = "UNRESOLVED_SCIENTIFIC_EXECUTION"
    INSUFFICIENT_VALIDATION_EVIDENCE = "INSUFFICIENT_VALIDATION_EVIDENCE"
    NEGATIVE_EVIDENCE_NOT_PRESERVED = "NEGATIVE_EVIDENCE_NOT_PRESERVED"
    CONDITIONALLY_READY_LIMITATION = "CONDITIONALLY_READY_LIMITATION"
    DOWNSTREAM_SCOPE_PROHIBITED = "DOWNSTREAM_SCOPE_PROHIBITED"


REFERENCE_LIMITATIONS = (
    "SYNTHETIC_IMPLEMENTATION_ONLY",
    "REFERENCE_IMPLEMENTATION_ONLY",
    "EMPIRICAL_EVALUATION_UNAVAILABLE",
    "VALIDATION_PENDING",
    "PRODUCTION_UNAVAILABLE",
)

CONDITIONAL_LIMITATION = "CONDITIONAL_READINESS_METADATA_PRESENT"
UNRESOLVED_LIMITATION = "SCIENTIFIC_EXECUTION_UNRESOLVED"
INSUFFICIENT_LIMITATION = "INSUFFICIENT_VALIDATION_EVIDENCE"

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
class ValidationReadinessRegistration:
    registration_id: str = "selected_scientific_module_validation_readiness_registration_v1"
    implementation_id: str = MODULE_ID
    implementation_version: str = MODULE_VERSION
    design_id: str = DESIGN_ID
    selected_module_id: str = SELECTED_MODULE_ID
    validation_protocol_version: str = VALIDATION_PROTOCOL_VERSION
    validation_readiness_schema_version: str = VALIDATION_READINESS_SCHEMA_VERSION
    reproducibility_schema_version: str = REPRODUCIBILITY_SCHEMA_VERSION
    stable_serialization_version: str = STABLE_SERIALIZATION_VERSION
    performs_empirical_evaluation: bool = False
    performs_statistical_testing: bool = False
    calculates_validation_metrics: bool = False
    evaluates_alpha_quality: bool = False
    supports_production: bool = False
    supports_optimization: bool = False
    supports_ml: bool = False


@dataclass(frozen=True)
class ValidationPrerequisiteMetadata:
    scientific_execution_complete: bool = True
    frozen_scientific_specification: bool = True
    frozen_formula_specification: bool = True
    frozen_activation_specification: bool = True
    frozen_horizon: bool = True
    complete_lineage: bool = True
    reproducibility_metadata: bool = True
    diagnostics_preserved: bool = True
    limitations_preserved: bool = True
    negative_evidence_preserved: bool = True


@dataclass(frozen=True)
class EvaluationGovernanceMetadata:
    evaluation_identity: str = "synthetic_selected_module_evaluation_identity_v1"
    evaluation_version: str = EVALUATION_VERSION
    protocol_version: str = VALIDATION_PROTOCOL_VERSION
    benchmark_protocol: str = "synthetic_benchmark_protocol_v1"
    contamination_protocol: str = "synthetic_contamination_protocol_v1"
    falsification_protocol: str = "synthetic_falsification_protocol_v1"
    reporting_protocol: str = "synthetic_reporting_protocol_v1"
    conditional_governance: bool = False


@dataclass(frozen=True)
class ContaminationReadinessMetadata:
    future_leakage_controls: bool = True
    lookahead_controls: bool = True
    benchmark_contamination_controls: bool = True
    comparator_contamination_controls: bool = True
    role_contamination_controls: bool = True
    horizon_contamination_controls: bool = True
    specification_contamination_controls: bool = True


@dataclass(frozen=True)
class NegativeEvidencePreservationMetadata:
    failures_preserved: bool = True
    unresolved_outcomes_preserved: bool = True
    insufficient_evidence_preserved: bool = True
    null_findings_preserved: bool = True
    negative_findings_preserved: bool = True


@dataclass(frozen=True)
class FalsificationReadinessMetadata:
    negative_controls: bool = True
    placebo_tests: bool = True
    ablations: bool = True
    mechanism_challenges: bool = True
    competing_explanations: bool = True


@dataclass(frozen=True)
class ValidationReadinessRequest:
    scientific_execution_result: scientific_execution.ScientificExecutionResult | None
    registration: ValidationReadinessRegistration = field(default_factory=ValidationReadinessRegistration)
    prerequisites: ValidationPrerequisiteMetadata = field(default_factory=ValidationPrerequisiteMetadata)
    evaluation_governance: EvaluationGovernanceMetadata = field(default_factory=EvaluationGovernanceMetadata)
    contamination_readiness: ContaminationReadinessMetadata = field(default_factory=ContaminationReadinessMetadata)
    negative_evidence: NegativeEvidencePreservationMetadata = field(default_factory=NegativeEvidencePreservationMetadata)
    falsification_readiness: FalsificationReadinessMetadata = field(default_factory=FalsificationReadinessMetadata)
    fixture_id: str = "synthetic_validation_readiness_request"
    excluded: bool = False
    conditional_limitations: tuple[str, ...] = ()
    requester_metadata: dict[str, str] = field(default_factory=dict)
    empirical_evaluation_requested: bool = False
    statistical_testing_requested: bool = False
    validation_metrics_requested: bool = False
    alpha_evaluation_requested: bool = False
    production_requested: bool = False
    optimization_requested: bool = False
    ml_requested: bool = False


@dataclass(frozen=True)
class ValidationReadinessIdentity:
    validation_readiness_id: str
    scientific_execution_id: str
    implementation_id: str
    implementation_version: str
    design_id: str
    validation_protocol_version: str
    evaluation_identity: str
    evaluation_version: str
    readiness_state: ValidationReadinessState


@dataclass(frozen=True)
class ValidationReadinessDiagnostics:
    codes: tuple[ValidationReadinessDiagnosticCode, ...]
    entries: tuple[dict[str, str], ...]


@dataclass(frozen=True)
class ValidationReadinessLimitations:
    codes: tuple[str, ...]


@dataclass(frozen=True)
class ValidationReadinessLineage:
    lineage_chain: tuple[str, ...]
    upstream_artifacts: dict[str, Any]
    scientific_execution_artifact: str
    validation_readiness_artifact: str
    empirical_evaluation_artifact: str = ""
    validation_artifact: str = ""
    candidate_artifact: str = ""
    panel_artifact: str = ""
    production_artifact: str = ""
    ml_artifact: str = ""


@dataclass(frozen=True)
class ValidationReadinessReproducibility:
    validation_protocol_version: str
    execution_version: str
    scientific_specification_version: str
    formula_specification_version: str
    frozen_activation_specification_version: str
    frozen_horizon_version: str
    reproducibility_version: str
    serialization_version: str
    deterministic_readiness_identity: str


@dataclass(frozen=True)
class ValidationReadinessInformationContract:
    exposes_readiness_state: bool = True
    exposes_diagnostics: bool = True
    exposes_limitations: bool = True
    exposes_evaluation_metadata: bool = True
    exposes_lineage: bool = True
    exposes_reproducibility: bool = True
    exposes_sharpe: bool = False
    exposes_ic: bool = False
    exposes_alpha: bool = False
    exposes_prediction: bool = False
    exposes_ranking: bool = False
    exposes_portfolio: bool = False
    exposes_validation_statistics: bool = False
    makes_production_decisions: bool = False
    performs_optimization: bool = False
    exposes_ml_outputs: bool = False


@dataclass(frozen=True)
class ValidationReadinessResult:
    validation_readiness_id: str
    readiness_state: ValidationReadinessState
    diagnostics: ValidationReadinessDiagnostics
    limitations: ValidationReadinessLimitations
    identity: ValidationReadinessIdentity
    lineage: ValidationReadinessLineage
    reproducibility: ValidationReadinessReproducibility
    information_contract: ValidationReadinessInformationContract
    evaluation_metadata: EvaluationGovernanceMetadata
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
    validation_logic_executed: bool = False
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
class ValidationReadinessFixture:
    fixture_id: str
    description: str
    request: ValidationReadinessRequest
    expected_state: ValidationReadinessState
    expected_diagnostic_codes: tuple[ValidationReadinessDiagnosticCode, ...] = ()
    expected_limitations: tuple[str, ...] = ()


def _registration_authoritative(registration: ValidationReadinessRegistration) -> bool:
    return (
        registration.implementation_id == MODULE_ID
        and registration.implementation_version == MODULE_VERSION
        and registration.design_id == DESIGN_ID
        and registration.selected_module_id == SELECTED_MODULE_ID
        and registration.validation_protocol_version == VALIDATION_PROTOCOL_VERSION
        and registration.validation_readiness_schema_version == VALIDATION_READINESS_SCHEMA_VERSION
        and registration.reproducibility_schema_version == REPRODUCIBILITY_SCHEMA_VERSION
        and registration.stable_serialization_version == STABLE_SERIALIZATION_VERSION
        and registration.performs_empirical_evaluation is False
        and registration.performs_statistical_testing is False
        and registration.calculates_validation_metrics is False
        and registration.evaluates_alpha_quality is False
        and registration.supports_production is False
        and registration.supports_optimization is False
        and registration.supports_ml is False
    )


def _diagnostic(code: ValidationReadinessDiagnosticCode, stage: str, message: str) -> dict[str, str]:
    return {"code": code.value, "message": message, "stage": stage}


def _append_diagnostic(
    diagnostics: list[dict[str, str]],
    code: ValidationReadinessDiagnosticCode,
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


def _lineage_complete(result: scientific_execution.ScientificExecutionResult | None) -> bool:
    if result is None:
        return False
    return bool(result.lineage.scientific_execution_artifact) and result.lineage.upstream_lineage_preserved


def _reproducibility_complete(result: scientific_execution.ScientificExecutionResult | None) -> bool:
    if result is None:
        return False
    repro = result.reproducibility
    return _metadata_complete(
        repro.execution_version,
        repro.formula_version,
        repro.scientific_specification_version,
        repro.frozen_activation_specification_version,
        repro.frozen_horizon_version,
        repro.reproducibility_schema_version,
        repro.serialization_version,
        repro.deterministic_execution_identity,
        repro.controlled_reference,
    )


def _scientific_spec_compatible(result: scientific_execution.ScientificExecutionResult | None) -> bool:
    if result is None:
        return False
    return (
        result.identity.scientific_specification_id == SCIENTIFIC_SPECIFICATION_ID
        and result.identity.scientific_specification_version == SCIENTIFIC_SPECIFICATION_VERSION
        and result.reproducibility.scientific_specification_version == SCIENTIFIC_SPECIFICATION_VERSION
    )


def _formula_spec_compatible(result: scientific_execution.ScientificExecutionResult | None) -> bool:
    if result is None:
        return False
    return result.reproducibility.formula_version == FORMULA_VERSION and result.identity.formula_version == FORMULA_VERSION


def _activation_spec_compatible(result: scientific_execution.ScientificExecutionResult | None) -> bool:
    if result is None:
        return False
    return result.reproducibility.frozen_activation_specification_version == ACTIVATION_SPECIFICATION_VERSION


def _horizon_compatible(result: scientific_execution.ScientificExecutionResult | None) -> bool:
    if result is None:
        return False
    return (
        result.identity.frozen_horizon_specification_id == FROZEN_HORIZON_SPECIFICATION_ID
        and result.identity.frozen_horizon_specification_version == FROZEN_HORIZON_SPECIFICATION_VERSION
        and result.reproducibility.frozen_horizon_version == FROZEN_HORIZON_SPECIFICATION_VERSION
    )


def _governance_complete(governance: EvaluationGovernanceMetadata) -> tuple[ValidationReadinessDiagnosticCode, ...]:
    failures: list[ValidationReadinessDiagnosticCode] = []
    if not governance.protocol_version:
        failures.append(ValidationReadinessDiagnosticCode.MISSING_PROTOCOL)
    if not governance.benchmark_protocol:
        failures.append(ValidationReadinessDiagnosticCode.MISSING_BENCHMARK_DEFINITION)
    if not governance.contamination_protocol:
        failures.append(ValidationReadinessDiagnosticCode.MISSING_CONTAMINATION_POLICY)
    if not governance.falsification_protocol:
        failures.append(ValidationReadinessDiagnosticCode.MISSING_FALSIFICATION_POLICY)
    if not governance.reporting_protocol:
        failures.append(ValidationReadinessDiagnosticCode.MISSING_REPORTING_PROTOCOL)
    return tuple(failures)


def _contamination_complete(contamination: ContaminationReadinessMetadata) -> bool:
    return all(
        (
            contamination.future_leakage_controls,
            contamination.lookahead_controls,
            contamination.benchmark_contamination_controls,
            contamination.comparator_contamination_controls,
            contamination.role_contamination_controls,
            contamination.horizon_contamination_controls,
            contamination.specification_contamination_controls,
        )
    )


def _falsification_complete(falsification: FalsificationReadinessMetadata) -> bool:
    return all(
        (
            falsification.negative_controls,
            falsification.placebo_tests,
            falsification.ablations,
            falsification.mechanism_challenges,
            falsification.competing_explanations,
        )
    )


def _negative_evidence_preserved(evidence: NegativeEvidencePreservationMetadata) -> bool:
    return all(
        (
            evidence.failures_preserved,
            evidence.unresolved_outcomes_preserved,
            evidence.insufficient_evidence_preserved,
            evidence.null_findings_preserved,
            evidence.negative_findings_preserved,
        )
    )


def _build_identity_payload(request: ValidationReadinessRequest, readiness_state: ValidationReadinessState) -> dict[str, Any]:
    result = request.scientific_execution_result
    return {
        "fixture_id": request.fixture_id,
        "scientific_execution_id": "" if result is None else result.scientific_execution_id,
        "implementation_id": request.registration.implementation_id,
        "implementation_version": request.registration.implementation_version,
        "design_id": request.registration.design_id,
        "validation_protocol_version": request.registration.validation_protocol_version,
        "evaluation_identity": request.evaluation_governance.evaluation_identity,
        "evaluation_version": request.evaluation_governance.evaluation_version,
        "readiness_state": readiness_state.value,
    }


def _lineage_payload(
    result: scientific_execution.ScientificExecutionResult | None,
    validation_readiness_id: str,
) -> ValidationReadinessLineage:
    if result is None:
        upstream = {}
        scientific_execution_artifact = ""
    else:
        upstream = dict(result.lineage.upstream_artifacts)
        upstream["frozen_module_input_artifact"] = result.lineage.frozen_module_input_id
        upstream["scientific_execution_artifact"] = result.scientific_execution_id
        upstream["scientific_result_artifact"] = result.lineage.scientific_result_artifact
        scientific_execution_artifact = result.scientific_execution_id
    return ValidationReadinessLineage(
        lineage_chain=LINEAGE_CHAIN,
        upstream_artifacts=upstream,
        scientific_execution_artifact=scientific_execution_artifact,
        validation_readiness_artifact=validation_readiness_id,
    )


def evaluate_validation_readiness(request: ValidationReadinessRequest) -> ValidationReadinessResult:
    diagnostics: list[dict[str, str]] = []
    limitations: list[str] = list(REFERENCE_LIMITATIONS)
    result = request.scientific_execution_result
    prerequisites = request.prerequisites
    governance = request.evaluation_governance

    if (
        request.excluded
        or request.empirical_evaluation_requested
        or request.statistical_testing_requested
        or request.validation_metrics_requested
        or request.alpha_evaluation_requested
        or request.production_requested
        or request.optimization_requested
        or request.ml_requested
        or not _registration_authoritative(request.registration)
    ):
        _append_diagnostic(
            diagnostics,
            ValidationReadinessDiagnosticCode.VALIDATION_READINESS_EXCLUDED,
            "scope",
            "Request is outside the validation-readiness reference implementation boundary.",
        )
    if (
        request.empirical_evaluation_requested
        or request.statistical_testing_requested
        or request.validation_metrics_requested
        or request.alpha_evaluation_requested
        or request.production_requested
        or request.optimization_requested
        or request.ml_requested
    ):
        _append_diagnostic(
            diagnostics,
            ValidationReadinessDiagnosticCode.DOWNSTREAM_SCOPE_PROHIBITED,
            "scope",
            "Empirical evaluation, statistics, production, optimization, and ML are prohibited.",
        )

    if result is None:
        _append_diagnostic(
            diagnostics,
            ValidationReadinessDiagnosticCode.SCIENTIFIC_EXECUTION_ARTIFACT_MISSING,
            "prerequisite",
            "Validation readiness requires a scientific execution result artifact.",
        )
    if not prerequisites.scientific_execution_complete:
        _append_diagnostic(
            diagnostics,
            ValidationReadinessDiagnosticCode.SCIENTIFIC_EXECUTION_NOT_COMPLETE,
            "prerequisite",
            "Scientific execution completion metadata is absent.",
        )
    if not prerequisites.frozen_scientific_specification:
        _append_diagnostic(
            diagnostics,
            ValidationReadinessDiagnosticCode.FROZEN_SCIENTIFIC_SPECIFICATION_MISSING,
            "prerequisite",
            "Frozen scientific specification metadata is absent.",
        )
    if not prerequisites.frozen_formula_specification:
        _append_diagnostic(
            diagnostics,
            ValidationReadinessDiagnosticCode.FROZEN_FORMULA_SPECIFICATION_MISSING,
            "prerequisite",
            "Frozen formula specification metadata is absent.",
        )
    if not prerequisites.frozen_activation_specification:
        _append_diagnostic(
            diagnostics,
            ValidationReadinessDiagnosticCode.FROZEN_ACTIVATION_SPECIFICATION_MISSING,
            "prerequisite",
            "Frozen activation specification metadata is absent.",
        )
    if not prerequisites.frozen_horizon:
        _append_diagnostic(
            diagnostics,
            ValidationReadinessDiagnosticCode.FROZEN_HORIZON_MISSING,
            "prerequisite",
            "Frozen horizon metadata is absent.",
        )
    if not prerequisites.diagnostics_preserved:
        _append_diagnostic(
            diagnostics,
            ValidationReadinessDiagnosticCode.SCIENTIFIC_DIAGNOSTICS_NOT_PRESERVED,
            "prerequisite",
            "Scientific execution diagnostics were not preserved.",
        )
    if not prerequisites.limitations_preserved:
        _append_diagnostic(
            diagnostics,
            ValidationReadinessDiagnosticCode.SCIENTIFIC_LIMITATIONS_NOT_PRESERVED,
            "prerequisite",
            "Scientific execution limitations were not preserved.",
        )

    for code in _governance_complete(governance):
        _append_diagnostic(diagnostics, code, "evaluation_governance", "Required evaluation-governance metadata is missing.")
    if not _contamination_complete(request.contamination_readiness):
        _append_diagnostic(
            diagnostics,
            ValidationReadinessDiagnosticCode.MISSING_CONTAMINATION_POLICY,
            "contamination_readiness",
            "Required contamination-readiness metadata is incomplete.",
        )
    if not _falsification_complete(request.falsification_readiness):
        _append_diagnostic(
            diagnostics,
            ValidationReadinessDiagnosticCode.MISSING_FALSIFICATION_POLICY,
            "falsification_readiness",
            "Required falsification-readiness metadata is incomplete.",
        )

    if result is not None and not _scientific_spec_compatible(result):
        _append_diagnostic(
            diagnostics,
            ValidationReadinessDiagnosticCode.INCOMPATIBLE_SCIENTIFIC_SPECIFICATION,
            "compatibility",
            "Scientific execution result does not match the frozen scientific specification.",
        )
    if result is not None and not _formula_spec_compatible(result):
        _append_diagnostic(
            diagnostics,
            ValidationReadinessDiagnosticCode.INCOMPATIBLE_FORMULA_SPECIFICATION,
            "compatibility",
            "Scientific execution result does not match the frozen formula specification.",
        )
    if result is not None and not _activation_spec_compatible(result):
        _append_diagnostic(
            diagnostics,
            ValidationReadinessDiagnosticCode.INCOMPATIBLE_ACTIVATION_SPECIFICATION,
            "compatibility",
            "Scientific execution result does not match the frozen activation specification.",
        )
    if result is not None and not _horizon_compatible(result):
        _append_diagnostic(
            diagnostics,
            ValidationReadinessDiagnosticCode.INCOMPATIBLE_FROZEN_HORIZON,
            "compatibility",
            "Scientific execution result does not match the frozen horizon.",
        )

    if not prerequisites.complete_lineage or not _lineage_complete(result):
        _append_diagnostic(
            diagnostics,
            ValidationReadinessDiagnosticCode.INCOMPLETE_LINEAGE,
            "lineage",
            "Required upstream-to-readiness lineage is incomplete.",
        )
    if not prerequisites.reproducibility_metadata or not _reproducibility_complete(result):
        _append_diagnostic(
            diagnostics,
            ValidationReadinessDiagnosticCode.MISSING_REPRODUCIBILITY_METADATA,
            "reproducibility",
            "Required reproducibility metadata is incomplete.",
        )

    if result is not None and (
        result.execution_state != scientific_execution.ScientificExecutionState.COMPLETE
        or result.decomposition_result == scientific_execution.DecompositionResult.UNRESOLVED
    ):
        _append_diagnostic(
            diagnostics,
            ValidationReadinessDiagnosticCode.UNRESOLVED_SCIENTIFIC_EXECUTION,
            "scientific_execution",
            "Scientific execution is not complete and resolved.",
        )
        _add_limitations(limitations, UNRESOLVED_LIMITATION)

    if not prerequisites.negative_evidence_preserved or not _negative_evidence_preserved(request.negative_evidence):
        _append_diagnostic(
            diagnostics,
            ValidationReadinessDiagnosticCode.NEGATIVE_EVIDENCE_NOT_PRESERVED,
            "negative_evidence",
            "Negative, null, unresolved, or insufficient-evidence outcomes are not fully preserved.",
        )
        _append_diagnostic(
            diagnostics,
            ValidationReadinessDiagnosticCode.INSUFFICIENT_VALIDATION_EVIDENCE,
            "negative_evidence",
            "Validation-readiness evidence is insufficient without negative-evidence preservation.",
        )
        _add_limitations(limitations, INSUFFICIENT_LIMITATION)

    if governance.conditional_governance or request.conditional_limitations:
        _append_diagnostic(
            diagnostics,
            ValidationReadinessDiagnosticCode.CONDITIONALLY_READY_LIMITATION,
            "conditional_readiness",
            "Conditional readiness metadata must be preserved before empirical evaluation.",
        )
        _add_limitations(limitations, CONDITIONAL_LIMITATION, *request.conditional_limitations)

    diagnostic_codes = tuple(ValidationReadinessDiagnosticCode(entry["code"]) for entry in _ordered_diagnostics(diagnostics))

    if ValidationReadinessDiagnosticCode.VALIDATION_READINESS_EXCLUDED in diagnostic_codes:
        readiness_state = ValidationReadinessState.EXCLUDED
    elif any(
        code
        in diagnostic_codes
        for code in (
            ValidationReadinessDiagnosticCode.SCIENTIFIC_EXECUTION_ARTIFACT_MISSING,
            ValidationReadinessDiagnosticCode.SCIENTIFIC_EXECUTION_NOT_COMPLETE,
            ValidationReadinessDiagnosticCode.FROZEN_SCIENTIFIC_SPECIFICATION_MISSING,
            ValidationReadinessDiagnosticCode.FROZEN_FORMULA_SPECIFICATION_MISSING,
            ValidationReadinessDiagnosticCode.FROZEN_ACTIVATION_SPECIFICATION_MISSING,
            ValidationReadinessDiagnosticCode.FROZEN_HORIZON_MISSING,
            ValidationReadinessDiagnosticCode.SCIENTIFIC_DIAGNOSTICS_NOT_PRESERVED,
            ValidationReadinessDiagnosticCode.SCIENTIFIC_LIMITATIONS_NOT_PRESERVED,
            ValidationReadinessDiagnosticCode.MISSING_PROTOCOL,
            ValidationReadinessDiagnosticCode.MISSING_BENCHMARK_DEFINITION,
            ValidationReadinessDiagnosticCode.MISSING_CONTAMINATION_POLICY,
            ValidationReadinessDiagnosticCode.MISSING_FALSIFICATION_POLICY,
            ValidationReadinessDiagnosticCode.MISSING_REPORTING_PROTOCOL,
        )
    ):
        readiness_state = ValidationReadinessState.NOT_READY
    elif any(
        code
        in diagnostic_codes
        for code in (
            ValidationReadinessDiagnosticCode.INCOMPATIBLE_SCIENTIFIC_SPECIFICATION,
            ValidationReadinessDiagnosticCode.INCOMPATIBLE_FORMULA_SPECIFICATION,
            ValidationReadinessDiagnosticCode.INCOMPATIBLE_ACTIVATION_SPECIFICATION,
            ValidationReadinessDiagnosticCode.INCOMPATIBLE_FROZEN_HORIZON,
        )
    ):
        readiness_state = ValidationReadinessState.NOT_READY
    elif ValidationReadinessDiagnosticCode.INCOMPLETE_LINEAGE in diagnostic_codes:
        readiness_state = ValidationReadinessState.NOT_READY
    elif ValidationReadinessDiagnosticCode.MISSING_REPRODUCIBILITY_METADATA in diagnostic_codes:
        readiness_state = ValidationReadinessState.NOT_READY
    elif ValidationReadinessDiagnosticCode.UNRESOLVED_SCIENTIFIC_EXECUTION in diagnostic_codes:
        readiness_state = ValidationReadinessState.UNRESOLVED
    elif ValidationReadinessDiagnosticCode.INSUFFICIENT_VALIDATION_EVIDENCE in diagnostic_codes:
        readiness_state = ValidationReadinessState.INSUFFICIENT_EVIDENCE
    elif ValidationReadinessDiagnosticCode.CONDITIONALLY_READY_LIMITATION in diagnostic_codes:
        readiness_state = ValidationReadinessState.CONDITIONALLY_READY
    else:
        readiness_state = ValidationReadinessState.READY

    validation_readiness_id = _stable_digest(_build_identity_payload(request, readiness_state), "validation_readiness")
    scientific_execution_id = "" if result is None else result.scientific_execution_id
    identity = ValidationReadinessIdentity(
        validation_readiness_id=validation_readiness_id,
        scientific_execution_id=scientific_execution_id,
        implementation_id=request.registration.implementation_id,
        implementation_version=request.registration.implementation_version,
        design_id=request.registration.design_id,
        validation_protocol_version=request.registration.validation_protocol_version,
        evaluation_identity=governance.evaluation_identity,
        evaluation_version=governance.evaluation_version,
        readiness_state=readiness_state,
    )
    lineage = _lineage_payload(result, validation_readiness_id)
    if result is None:
        execution_version = ""
        scientific_spec_version = ""
        formula_version = ""
        activation_version = ""
        horizon_version = ""
    else:
        execution_version = result.reproducibility.execution_version
        scientific_spec_version = result.reproducibility.scientific_specification_version
        formula_version = result.reproducibility.formula_version
        activation_version = result.reproducibility.frozen_activation_specification_version
        horizon_version = result.reproducibility.frozen_horizon_version
    reproducibility = ValidationReadinessReproducibility(
        validation_protocol_version=request.registration.validation_protocol_version,
        execution_version=execution_version,
        scientific_specification_version=scientific_spec_version,
        formula_specification_version=formula_version,
        frozen_activation_specification_version=activation_version,
        frozen_horizon_version=horizon_version,
        reproducibility_version=REPRODUCIBILITY_SCHEMA_VERSION,
        serialization_version=request.registration.stable_serialization_version,
        deterministic_readiness_identity=validation_readiness_id,
    )

    return ValidationReadinessResult(
        validation_readiness_id=validation_readiness_id,
        readiness_state=readiness_state,
        diagnostics=ValidationReadinessDiagnostics(codes=diagnostic_codes, entries=_ordered_diagnostics(diagnostics)),
        limitations=ValidationReadinessLimitations(codes=tuple(limitations)),
        identity=identity,
        lineage=lineage,
        reproducibility=reproducibility,
        information_contract=ValidationReadinessInformationContract(),
        evaluation_metadata=governance,
    )


def _scientific_execution_result(fixture_id: str) -> scientific_execution.ScientificExecutionResult:
    fixtures = {fixture.fixture_id: fixture for fixture in scientific_execution.canonical_scientific_execution_fixtures()}
    return scientific_execution.execute_selected_scientific_module(fixtures[fixture_id].request)


def _ready_result() -> scientific_execution.ScientificExecutionResult:
    return _scientific_execution_result("SE01_common")


def _fixture(
    fixture_id: str,
    description: str,
    expected_state: ValidationReadinessState,
    expected_diagnostic_codes: tuple[ValidationReadinessDiagnosticCode, ...] = (),
    expected_limitations: tuple[str, ...] = (),
    scientific_result: scientific_execution.ScientificExecutionResult | None | str = "ready",
    **request_overrides: Any,
) -> ValidationReadinessFixture:
    if scientific_result == "ready":
        execution_result = _ready_result()
    elif isinstance(scientific_result, str):
        execution_result = _scientific_execution_result(scientific_result)
    else:
        execution_result = scientific_result
    request = ValidationReadinessRequest(
        scientific_execution_result=execution_result,
        fixture_id=fixture_id,
        **request_overrides,
    )
    return ValidationReadinessFixture(
        fixture_id=fixture_id,
        description=description,
        request=request,
        expected_state=expected_state,
        expected_diagnostic_codes=expected_diagnostic_codes,
        expected_limitations=expected_limitations,
    )


def canonical_validation_readiness_fixtures() -> tuple[ValidationReadinessFixture, ...]:
    ready = _ready_result()
    incompatible_spec = replace(
        ready,
        identity=replace(ready.identity, scientific_specification_version="v2"),
        reproducibility=replace(ready.reproducibility, scientific_specification_version="v2"),
    )
    incompatible_formula = replace(ready, reproducibility=replace(ready.reproducibility, formula_version="formula_v2"))
    incompatible_activation = replace(ready, reproducibility=replace(ready.reproducibility, frozen_activation_specification_version="v2"))
    incompatible_horizon = replace(
        ready,
        identity=replace(ready.identity, frozen_horizon_specification_version="v2"),
        reproducibility=replace(ready.reproducibility, frozen_horizon_version="v2"),
    )
    missing_lineage = replace(ready, lineage=replace(ready.lineage, upstream_lineage_preserved=False))
    missing_repro = replace(ready, reproducibility=replace(ready.reproducibility, controlled_reference=""))

    fixtures = [
        _fixture("VR01_ready", "Fully ready metadata.", ValidationReadinessState.READY),
        _fixture(
            "VR02_conditionally_ready",
            "Conditional metadata is preserved after all fatal gates pass.",
            ValidationReadinessState.CONDITIONALLY_READY,
            (ValidationReadinessDiagnosticCode.CONDITIONALLY_READY_LIMITATION,),
            (CONDITIONAL_LIMITATION, "bounded_population_review_required"),
            evaluation_governance=EvaluationGovernanceMetadata(conditional_governance=True),
            conditional_limitations=("bounded_population_review_required",),
        ),
        _fixture(
            "VR03_unresolved_execution",
            "Unresolved scientific execution remains unresolved.",
            ValidationReadinessState.UNRESOLVED,
            (ValidationReadinessDiagnosticCode.UNRESOLVED_SCIENTIFIC_EXECUTION,),
            (UNRESOLVED_LIMITATION,),
            scientific_result="SE04_unresolved",
        ),
        _fixture(
            "VR04_excluded_request",
            "Excluded request refuses readiness.",
            ValidationReadinessState.EXCLUDED,
            (ValidationReadinessDiagnosticCode.VALIDATION_READINESS_EXCLUDED,),
            excluded=True,
        ),
        _fixture(
            "VR05_missing_execution_artifact",
            "Missing scientific execution artifact fails closed.",
            ValidationReadinessState.NOT_READY,
            (ValidationReadinessDiagnosticCode.SCIENTIFIC_EXECUTION_ARTIFACT_MISSING,),
            scientific_result=None,
        ),
        _fixture(
            "VR06_missing_protocol",
            "Missing protocol fails closed.",
            ValidationReadinessState.NOT_READY,
            (ValidationReadinessDiagnosticCode.MISSING_PROTOCOL,),
            evaluation_governance=EvaluationGovernanceMetadata(protocol_version=""),
        ),
        _fixture(
            "VR07_missing_benchmark",
            "Missing benchmark protocol fails closed.",
            ValidationReadinessState.NOT_READY,
            (ValidationReadinessDiagnosticCode.MISSING_BENCHMARK_DEFINITION,),
            evaluation_governance=EvaluationGovernanceMetadata(benchmark_protocol=""),
        ),
        _fixture(
            "VR08_missing_contamination_policy",
            "Missing contamination policy fails closed.",
            ValidationReadinessState.NOT_READY,
            (ValidationReadinessDiagnosticCode.MISSING_CONTAMINATION_POLICY,),
            evaluation_governance=EvaluationGovernanceMetadata(contamination_protocol=""),
        ),
        _fixture(
            "VR09_missing_falsification_policy",
            "Missing falsification policy fails closed.",
            ValidationReadinessState.NOT_READY,
            (ValidationReadinessDiagnosticCode.MISSING_FALSIFICATION_POLICY,),
            evaluation_governance=EvaluationGovernanceMetadata(falsification_protocol=""),
        ),
        _fixture(
            "VR10_missing_reporting_protocol",
            "Missing reporting policy fails closed.",
            ValidationReadinessState.NOT_READY,
            (ValidationReadinessDiagnosticCode.MISSING_REPORTING_PROTOCOL,),
            evaluation_governance=EvaluationGovernanceMetadata(reporting_protocol=""),
        ),
        _fixture(
            "VR11_missing_scientific_spec_prerequisite",
            "Missing frozen scientific specification metadata fails closed.",
            ValidationReadinessState.NOT_READY,
            (ValidationReadinessDiagnosticCode.FROZEN_SCIENTIFIC_SPECIFICATION_MISSING,),
            prerequisites=ValidationPrerequisiteMetadata(frozen_scientific_specification=False),
        ),
        _fixture(
            "VR12_missing_formula_spec_prerequisite",
            "Missing frozen formula specification metadata fails closed.",
            ValidationReadinessState.NOT_READY,
            (ValidationReadinessDiagnosticCode.FROZEN_FORMULA_SPECIFICATION_MISSING,),
            prerequisites=ValidationPrerequisiteMetadata(frozen_formula_specification=False),
        ),
        _fixture(
            "VR13_missing_activation_spec_prerequisite",
            "Missing frozen activation specification metadata fails closed.",
            ValidationReadinessState.NOT_READY,
            (ValidationReadinessDiagnosticCode.FROZEN_ACTIVATION_SPECIFICATION_MISSING,),
            prerequisites=ValidationPrerequisiteMetadata(frozen_activation_specification=False),
        ),
        _fixture(
            "VR14_missing_horizon_prerequisite",
            "Missing frozen horizon metadata fails closed.",
            ValidationReadinessState.NOT_READY,
            (ValidationReadinessDiagnosticCode.FROZEN_HORIZON_MISSING,),
            prerequisites=ValidationPrerequisiteMetadata(frozen_horizon=False),
        ),
        _fixture(
            "VR15_incompatible_scientific_spec",
            "Incompatible scientific specification fails closed.",
            ValidationReadinessState.NOT_READY,
            (ValidationReadinessDiagnosticCode.INCOMPATIBLE_SCIENTIFIC_SPECIFICATION,),
            scientific_result=incompatible_spec,
        ),
        _fixture(
            "VR16_incompatible_formula_spec",
            "Incompatible formula metadata fails closed.",
            ValidationReadinessState.NOT_READY,
            (ValidationReadinessDiagnosticCode.INCOMPATIBLE_FORMULA_SPECIFICATION,),
            scientific_result=incompatible_formula,
        ),
        _fixture(
            "VR17_incompatible_activation_spec",
            "Incompatible activation metadata fails closed.",
            ValidationReadinessState.NOT_READY,
            (ValidationReadinessDiagnosticCode.INCOMPATIBLE_ACTIVATION_SPECIFICATION,),
            scientific_result=incompatible_activation,
        ),
        _fixture(
            "VR18_incompatible_horizon",
            "Incompatible horizon metadata fails closed.",
            ValidationReadinessState.NOT_READY,
            (ValidationReadinessDiagnosticCode.INCOMPATIBLE_FROZEN_HORIZON,),
            scientific_result=incompatible_horizon,
        ),
        _fixture(
            "VR19_missing_lineage",
            "Missing lineage fails closed.",
            ValidationReadinessState.NOT_READY,
            (ValidationReadinessDiagnosticCode.INCOMPLETE_LINEAGE,),
            scientific_result=missing_lineage,
        ),
        _fixture(
            "VR20_missing_reproducibility",
            "Missing reproducibility metadata fails closed.",
            ValidationReadinessState.NOT_READY,
            (ValidationReadinessDiagnosticCode.MISSING_REPRODUCIBILITY_METADATA,),
            scientific_result=missing_repro,
        ),
        _fixture(
            "VR21_negative_evidence_not_preserved",
            "Negative evidence preservation is mandatory.",
            ValidationReadinessState.INSUFFICIENT_EVIDENCE,
            (
                ValidationReadinessDiagnosticCode.NEGATIVE_EVIDENCE_NOT_PRESERVED,
                ValidationReadinessDiagnosticCode.INSUFFICIENT_VALIDATION_EVIDENCE,
            ),
            (INSUFFICIENT_LIMITATION,),
            negative_evidence=NegativeEvidencePreservationMetadata(null_findings_preserved=False),
        ),
        _fixture(
            "VR22_incomplete_contamination_controls",
            "Incomplete contamination controls fail closed.",
            ValidationReadinessState.NOT_READY,
            (ValidationReadinessDiagnosticCode.MISSING_CONTAMINATION_POLICY,),
            contamination_readiness=ContaminationReadinessMetadata(role_contamination_controls=False),
        ),
        _fixture(
            "VR23_incomplete_falsification_metadata",
            "Incomplete falsification metadata fails closed.",
            ValidationReadinessState.NOT_READY,
            (ValidationReadinessDiagnosticCode.MISSING_FALSIFICATION_POLICY,),
            falsification_readiness=FalsificationReadinessMetadata(placebo_tests=False),
        ),
        _fixture(
            "VR24_downstream_request_excluded",
            "Empirical evaluation request is excluded.",
            ValidationReadinessState.EXCLUDED,
            (
                ValidationReadinessDiagnosticCode.VALIDATION_READINESS_EXCLUDED,
                ValidationReadinessDiagnosticCode.DOWNSTREAM_SCOPE_PROHIBITED,
            ),
            empirical_evaluation_requested=True,
        ),
        _fixture(
            "VR25_combined_failures",
            "Combined failures accumulate but precedence fails closed.",
            ValidationReadinessState.NOT_READY,
            (
                ValidationReadinessDiagnosticCode.MISSING_PROTOCOL,
                ValidationReadinessDiagnosticCode.MISSING_CONTAMINATION_POLICY,
                ValidationReadinessDiagnosticCode.INCOMPLETE_LINEAGE,
                ValidationReadinessDiagnosticCode.MISSING_REPRODUCIBILITY_METADATA,
                ValidationReadinessDiagnosticCode.NEGATIVE_EVIDENCE_NOT_PRESERVED,
            ),
            (INSUFFICIENT_LIMITATION,),
            scientific_result=missing_lineage,
            prerequisites=ValidationPrerequisiteMetadata(reproducibility_metadata=False, negative_evidence_preserved=False),
            evaluation_governance=EvaluationGovernanceMetadata(protocol_version="", contamination_protocol=""),
            negative_evidence=NegativeEvidencePreservationMetadata(failures_preserved=False),
        ),
        _fixture(
            "VR26_deterministic_repeat",
            "Repeat fixture for deterministic identity and serialization.",
            ValidationReadinessState.READY,
        ),
    ]
    return tuple(fixtures)


def validation_readiness_guardrail_manifest() -> dict[str, bool]:
    return {
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

