from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
import json
from typing import Any

from pipelines import project_underdog_phase5_prepared_observations_reference_implementation_v1 as po


MODULE_ID = "project_underdog_phase5_scientific_module_intake_reference_implementation_v1"
MODULE_VERSION = "v1"
FROZEN_DESIGN_ID = "project_underdog_phase5_prepared_observations_platform_integration_and_scientific_module_intake_design_v1"
LAYER_NAME = "Project Underdog Phase 5 Scientific Module Intake"
INTAKE_CONTRACT_ID = "synthetic_scientific_module_intake_contract_v1"
INTAKE_CONTRACT_VERSION = "v1"
MODULE_SPECIFICATION_VERSION = "synthetic_scientific_module_specification_v1"
ROLE_SCHEMA_VERSION = "project_underdog_phase5_integrated_scientific_information_inventory_v1"
DIAGNOSTIC_SCHEMA_VERSION = "scientific_module_intake_diagnostic_schema_v1"
ARTIFACT_LINEAGE_SCHEMA_VERSION = "scientific_module_intake_artifact_lineage_schema_v1"
REPRODUCIBILITY_SCHEMA_VERSION = "scientific_module_intake_reproducibility_schema_v1"
STABLE_SERIALIZATION_VERSION = "stable_json_v1"


class IntakeCompatibilityState(str, Enum):
    COMPATIBLE = "INTAKE_COMPATIBLE"
    CONDITIONALLY_COMPATIBLE = "INTAKE_CONDITIONALLY_COMPATIBLE"
    UNRESOLVED = "INTAKE_UNRESOLVED"
    INCOMPATIBLE = "INTAKE_INCOMPATIBLE"
    EXCLUDED = "INTAKE_EXCLUDED"
    INSUFFICIENT_EVIDENCE = "INSUFFICIENT_INTAKE_EVIDENCE"


class IntakeDiagnosticCode(str, Enum):
    PREPARED_OBSERVATION_EXCLUDED = "PREPARED_OBSERVATION_EXCLUDED"
    PREPARED_OBSERVATION_STRUCTURALLY_INCOMPLETE = "PREPARED_OBSERVATION_STRUCTURALLY_INCOMPLETE"
    PREPARED_OBSERVATION_UNRESOLVED = "PREPARED_OBSERVATION_UNRESOLVED"
    PREPARED_OBSERVATION_INSUFFICIENT = "PREPARED_OBSERVATION_INSUFFICIENT"
    CONDITIONAL_READINESS_NOT_ACCEPTED = "CONDITIONAL_READINESS_NOT_ACCEPTED"
    MISSING_INTAKE_CONTRACT = "MISSING_INTAKE_CONTRACT"
    INTAKE_CONTRACT_VERSION_MISMATCH = "INTAKE_CONTRACT_VERSION_MISMATCH"
    UNKNOWN_SCIENTIFIC_MODULE = "UNKNOWN_SCIENTIFIC_MODULE"
    UNKNOWN_MODULE_VERSION = "UNKNOWN_MODULE_VERSION"
    MODULE_SPECIFICATION_VERSION_MISMATCH = "MODULE_SPECIFICATION_VERSION_MISMATCH"
    PREPARED_OBSERVATION_CONTRACT_VERSION_MISMATCH = "PREPARED_OBSERVATION_CONTRACT_VERSION_MISMATCH"
    PREPARED_OBSERVATION_IMPLEMENTATION_VERSION_MISMATCH = "PREPARED_OBSERVATION_IMPLEMENTATION_VERSION_MISMATCH"
    INFORMATION_ROLE_SCHEMA_VERSION_MISMATCH = "INFORMATION_ROLE_SCHEMA_VERSION_MISMATCH"
    DIAGNOSTIC_SCHEMA_VERSION_MISMATCH = "DIAGNOSTIC_SCHEMA_VERSION_MISMATCH"
    ARTIFACT_LINEAGE_SCHEMA_VERSION_MISMATCH = "ARTIFACT_LINEAGE_SCHEMA_VERSION_MISMATCH"
    REPRODUCIBILITY_SCHEMA_VERSION_MISMATCH = "REPRODUCIBILITY_SCHEMA_VERSION_MISMATCH"
    MISSING_PREPARED_OBSERVATION_LINEAGE = "MISSING_PREPARED_OBSERVATION_LINEAGE"
    MISSING_MODULE_LINEAGE = "MISSING_MODULE_LINEAGE"
    INCOMPLETE_REPRODUCIBILITY_METADATA = "INCOMPLETE_REPRODUCIBILITY_METADATA"
    MISSING_REQUIRED_ROLE = "MISSING_REQUIRED_ROLE"
    PROHIBITED_ROLE_PRESENT = "PROHIBITED_ROLE_PRESENT"
    UNSUPPORTED_ROLE = "UNSUPPORTED_ROLE"
    ROLE_CARDINALITY_MISMATCH = "ROLE_CARDINALITY_MISMATCH"
    ROLE_ATTACHMENT_MISMATCH = "ROLE_ATTACHMENT_MISMATCH"
    MISSING_TARGET_OBSERVATION = "MISSING_TARGET_OBSERVATION"
    UNSUPPORTED_TARGET_OBSERVATION_TYPE = "UNSUPPORTED_TARGET_OBSERVATION_TYPE"
    UNSUPPORTED_OBSERVATION_TIME_FORM = "UNSUPPORTED_OBSERVATION_TIME_FORM"
    MISSING_REQUIRED_CONTEXT = "MISSING_REQUIRED_CONTEXT"
    PROHIBITED_CONTEXT_PRESENT = "PROHIBITED_CONTEXT_PRESENT"
    CONTEXT_CARDINALITY_MISMATCH = "CONTEXT_CARDINALITY_MISMATCH"
    CONTEXT_BINDING_CONFLICT = "CONTEXT_BINDING_CONFLICT"
    MISSING_REQUIRED_COMPARATOR = "MISSING_REQUIRED_COMPARATOR"
    PROHIBITED_COMPARATOR_PRESENT = "PROHIBITED_COMPARATOR_PRESENT"
    COMPARATOR_CARDINALITY_MISMATCH = "COMPARATOR_CARDINALITY_MISMATCH"
    COMPARATOR_BINDING_CONFLICT = "COMPARATOR_BINDING_CONFLICT"
    TEMPORAL_INCOMPATIBILITY = "TEMPORAL_INCOMPATIBILITY"
    TEMPORAL_NON_OVERLAP = "TEMPORAL_NON_OVERLAP"
    UNSUPPORTED_OPEN_INTERVAL = "UNSUPPORTED_OPEN_INTERVAL"
    UNSUPPORTED_MIXED_FREQUENCY = "UNSUPPORTED_MIXED_FREQUENCY"
    INCOMPLETE_TEMPORAL_TRACEABILITY = "INCOMPLETE_TEMPORAL_TRACEABILITY"
    INSUFFICIENT_REQUIRED_COVERAGE = "INSUFFICIENT_REQUIRED_COVERAGE"
    UNACCEPTABLE_REQUIRED_MISSINGNESS = "UNACCEPTABLE_REQUIRED_MISSINGNESS"
    INHERITED_FATAL_DIAGNOSTIC = "INHERITED_FATAL_DIAGNOSTIC"
    INHERITED_UNRESOLVED_DIAGNOSTIC = "INHERITED_UNRESOLVED_DIAGNOSTIC"
    DUPLICATE_INTAKE_EXPOSURE = "DUPLICATE_INTAKE_EXPOSURE"
    CONFLICTING_INTAKE_BINDING = "CONFLICTING_INTAKE_BINDING"
    SUPERSEDED_PREPARED_OBSERVATION = "SUPERSEDED_PREPARED_OBSERVATION"
    INCOMPLETE_INTAKE_TRACEABILITY = "INCOMPLETE_INTAKE_TRACEABILITY"
    RAW_PREPARED_OBSERVATION_BYPASS = "RAW_PREPARED_OBSERVATION_BYPASS"
    DIRECT_UPSTREAM_COMPONENT_BYPASS = "DIRECT_UPSTREAM_COMPONENT_BYPASS"


APPROVED_INFORMATION_ROLES = tuple(role.value for role in po.InformationRole)
CORE_INFORMATION_ROLES = tuple(
    role.value
    for role in (
        po.InformationRole.VALIDATED_ALPHA_INFORMATION,
        po.InformationRole.SUPPORTED_ALPHA_INFORMATION,
        po.InformationRole.CONTEXTUAL_CONTROL_INFORMATION,
        po.InformationRole.CONDITIONING_INFORMATION,
        po.InformationRole.COMPARATOR_OR_BENCHMARK_INFORMATION,
        po.InformationRole.COMMON_IDIOSYNCRATIC_DECOMPOSITION_INFORMATION,
        po.InformationRole.EXPLANATORY_ONLY_INFORMATION,
        po.InformationRole.FAMILY_REFINEMENT_INFORMATION,
        po.InformationRole.DIAGNOSTIC_INFORMATION,
        po.InformationRole.NEGATIVE_INFORMATION,
    )
)


@dataclass(frozen=True)
class IntakeDiagnostic:
    code: IntakeDiagnosticCode
    component: str
    message: str
    inherited: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "code": self.code.value,
            "component": self.component,
            "inherited": self.inherited,
            "message": self.message,
        }


@dataclass(frozen=True)
class RoleCardinalityRule:
    role: str
    minimum_count: int = 0
    maximum_count: int | None = None
    allowed_attachment_types: tuple[str, ...] = ("target", "context", "comparator")

    def to_dict(self) -> dict[str, Any]:
        return {
            "allowed_attachment_types": list(self.allowed_attachment_types),
            "maximum_count": self.maximum_count,
            "minimum_count": self.minimum_count,
            "role": self.role,
        }


@dataclass(frozen=True)
class AttachmentRequirement:
    requirement_id: str
    required_or_optional: str
    allowed_roles: tuple[str, ...]
    minimum_count: int = 1
    maximum_count: int | None = None
    accepted_statuses: tuple[str, ...] = ("present", "COMPARATOR_ELIGIBLE")
    accepted_temporal_states: tuple[str, ...] = ("valid_overlap",)
    required_trace: bool = True
    required_lineage: bool = True
    minimum_coverage: bool = True
    accepted_missingness: tuple[str, ...] = ()
    allow_superseded: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "accepted_missingness": list(self.accepted_missingness),
            "accepted_statuses": list(self.accepted_statuses),
            "accepted_temporal_states": list(self.accepted_temporal_states),
            "allowed_roles": list(self.allowed_roles),
            "allow_superseded": self.allow_superseded,
            "maximum_count": self.maximum_count,
            "minimum_count": self.minimum_count,
            "minimum_coverage": self.minimum_coverage,
            "required_lineage": self.required_lineage,
            "required_or_optional": self.required_or_optional,
            "required_trace": self.required_trace,
            "requirement_id": self.requirement_id,
        }


@dataclass(frozen=True)
class ScientificModuleRegistration:
    module_id: str
    module_version: str
    module_specification_version: str
    intake_contract_id: str
    intake_contract_version: str
    module_status: str = "SYNTHETIC_REFERENCE_MODULE"
    governing_versions: dict[str, str] = field(default_factory=dict)
    artifact_reference: str = "synthetic_scientific_module_specification_artifact"

    def to_dict(self) -> dict[str, Any]:
        return {
            "artifact_reference": self.artifact_reference,
            "governing_versions": dict(sorted(self.governing_versions.items())),
            "intake_contract_id": self.intake_contract_id,
            "intake_contract_version": self.intake_contract_version,
            "module_id": self.module_id,
            "module_specification_version": self.module_specification_version,
            "module_status": self.module_status,
            "module_version": self.module_version,
        }


@dataclass(frozen=True)
class ModuleIntakeContract:
    intake_contract_id: str = INTAKE_CONTRACT_ID
    intake_contract_version: str = INTAKE_CONTRACT_VERSION
    module_id: str = "synthetic_target_context_comparator_module"
    module_version: str = "v1"
    module_specification_version: str = MODULE_SPECIFICATION_VERSION
    accepted_prepared_observation_contract_versions: tuple[str, ...] = ("v1",)
    accepted_prepared_observation_implementation_versions: tuple[str, ...] = (po.MODULE_VERSION,)
    accepted_information_role_schema_versions: tuple[str, ...] = (ROLE_SCHEMA_VERSION,)
    accepted_diagnostic_schema_versions: tuple[str, ...] = (DIAGNOSTIC_SCHEMA_VERSION,)
    accepted_artifact_lineage_schema_versions: tuple[str, ...] = (ARTIFACT_LINEAGE_SCHEMA_VERSION,)
    accepted_reproducibility_schema_versions: tuple[str, ...] = (REPRODUCIBILITY_SCHEMA_VERSION,)
    accepted_prepared_observation_readiness_states: tuple[po.PreparedObservationReadinessState, ...] = (
        po.PreparedObservationReadinessState.STRUCTURALLY_READY,
    )
    conditional_readiness_policy: str = "reject"
    required_target_observation_types: tuple[str, ...] = ("synthetic_target_observation",)
    accepted_observation_time_forms: tuple[str, ...] = ("point",)
    accepted_temporal_alignment_states: tuple[po.TemporalAlignmentState, ...] = (po.TemporalAlignmentState.FULLY_ALIGNED,)
    required_roles: tuple[str, ...] = (
        po.InformationRole.CONTEXTUAL_CONTROL_INFORMATION.value,
        po.InformationRole.COMPARATOR_OR_BENCHMARK_INFORMATION.value,
    )
    optional_roles: tuple[str, ...] = ()
    prohibited_roles: tuple[str, ...] = ()
    role_cardinality_rules: tuple[RoleCardinalityRule, ...] = ()
    required_context_requirements: tuple[AttachmentRequirement, ...] = (
        AttachmentRequirement(
            "required_context",
            "required",
            (po.InformationRole.CONTEXTUAL_CONTROL_INFORMATION.value,),
            accepted_statuses=("present",),
        ),
    )
    optional_context_requirements: tuple[AttachmentRequirement, ...] = ()
    prohibited_context_requirements: tuple[AttachmentRequirement, ...] = ()
    required_comparator_requirements: tuple[AttachmentRequirement, ...] = (
        AttachmentRequirement(
            "required_comparator",
            "required",
            (po.InformationRole.COMPARATOR_OR_BENCHMARK_INFORMATION.value,),
            accepted_statuses=("COMPARATOR_ELIGIBLE",),
            accepted_temporal_states=("valid_overlap",),
        ),
    )
    optional_comparator_requirements: tuple[AttachmentRequirement, ...] = ()
    prohibited_comparator_requirements: tuple[AttachmentRequirement, ...] = ()
    required_coverage_dimensions: tuple[str, ...] = (
        "target_coverage",
        "context_coverage",
        "comparator_coverage",
        "temporal_coverage",
        "information_role_coverage",
        "traceability_coverage",
    )
    minimum_coverage_rules: dict[str, bool] = field(default_factory=dict)
    accepted_missingness_conditions: tuple[str, ...] = ()
    prohibited_inherited_diagnostics: tuple[str, ...] = (po.PreparedObservationDiagnosticCode.INHERITED_FATAL_UPSTREAM_DIAGNOSTIC.value,)
    required_trace_dimensions: tuple[str, ...] = ("source_authority_trace", "pit_trace", "comparator_traces")
    required_reproducibility_fields: tuple[str, ...] = ("deterministic_serialization", "controlled_reference")
    required_lineage_fields: tuple[str, ...] = (
        "source_authority_artifacts",
        "pit_identity_context_artifacts",
        "prepared_observation_artifact",
    )
    output_contract_id: str = "synthetic_scientific_module_handoff_contract_v1"
    governing_design_version: str = FROZEN_DESIGN_ID
    information_role_schema_version: str = ROLE_SCHEMA_VERSION
    diagnostic_schema_version: str = DIAGNOSTIC_SCHEMA_VERSION
    artifact_lineage_schema_version: str = ARTIFACT_LINEAGE_SCHEMA_VERSION
    reproducibility_schema_version: str = REPRODUCIBILITY_SCHEMA_VERSION

    def to_dict(self) -> dict[str, Any]:
        return {
            "accepted_artifact_lineage_schema_versions": list(self.accepted_artifact_lineage_schema_versions),
            "accepted_diagnostic_schema_versions": list(self.accepted_diagnostic_schema_versions),
            "accepted_information_role_schema_versions": list(self.accepted_information_role_schema_versions),
            "accepted_missingness_conditions": list(self.accepted_missingness_conditions),
            "accepted_observation_time_forms": list(self.accepted_observation_time_forms),
            "accepted_prepared_observation_contract_versions": list(self.accepted_prepared_observation_contract_versions),
            "accepted_prepared_observation_implementation_versions": list(self.accepted_prepared_observation_implementation_versions),
            "accepted_prepared_observation_readiness_states": [state.value for state in self.accepted_prepared_observation_readiness_states],
            "accepted_reproducibility_schema_versions": list(self.accepted_reproducibility_schema_versions),
            "accepted_temporal_alignment_states": [state.value for state in self.accepted_temporal_alignment_states],
            "artifact_lineage_schema_version": self.artifact_lineage_schema_version,
            "conditional_readiness_policy": self.conditional_readiness_policy,
            "diagnostic_schema_version": self.diagnostic_schema_version,
            "governing_design_version": self.governing_design_version,
            "information_role_schema_version": self.information_role_schema_version,
            "intake_contract_id": self.intake_contract_id,
            "intake_contract_version": self.intake_contract_version,
            "minimum_coverage_rules": dict(sorted(self.minimum_coverage_rules.items())),
            "module_id": self.module_id,
            "module_specification_version": self.module_specification_version,
            "module_version": self.module_version,
            "optional_context_requirements": [req.to_dict() for req in self.optional_context_requirements],
            "optional_comparator_requirements": [req.to_dict() for req in self.optional_comparator_requirements],
            "optional_roles": list(self.optional_roles),
            "output_contract_id": self.output_contract_id,
            "prohibited_context_requirements": [req.to_dict() for req in self.prohibited_context_requirements],
            "prohibited_comparator_requirements": [req.to_dict() for req in self.prohibited_comparator_requirements],
            "prohibited_inherited_diagnostics": list(self.prohibited_inherited_diagnostics),
            "prohibited_roles": list(self.prohibited_roles),
            "required_context_requirements": [req.to_dict() for req in self.required_context_requirements],
            "required_comparator_requirements": [req.to_dict() for req in self.required_comparator_requirements],
            "required_coverage_dimensions": list(self.required_coverage_dimensions),
            "required_lineage_fields": list(self.required_lineage_fields),
            "required_reproducibility_fields": list(self.required_reproducibility_fields),
            "required_roles": list(self.required_roles),
            "required_target_observation_types": list(self.required_target_observation_types),
            "required_trace_dimensions": list(self.required_trace_dimensions),
            "reproducibility_schema_version": self.reproducibility_schema_version,
            "role_cardinality_rules": [rule.to_dict() for rule in self.role_cardinality_rules],
        }


@dataclass(frozen=True)
class IntakeEvaluationRequest:
    prepared_observation: po.PreparedObservationResult
    intake_contract: ModuleIntakeContract | None
    scientific_module: ScientificModuleRegistration | None
    prepared_observation_contract_version: str = "v1"
    information_role_schema_version: str = ROLE_SCHEMA_VERSION
    diagnostic_schema_version: str = DIAGNOSTIC_SCHEMA_VERSION
    artifact_lineage_schema_version: str = ARTIFACT_LINEAGE_SCHEMA_VERSION
    reproducibility_schema_version: str = REPRODUCIBILITY_SCHEMA_VERSION
    duplicate_intake_exposure: bool = False
    conflicting_intake_binding: bool = False
    raw_prepared_observation_bypass: bool = False
    direct_upstream_component_bypass: bool = False
    missing_module_lineage: bool = False
    fixture_id: str = ""


@dataclass(frozen=True)
class IntakeInformationContract:
    prepared_observation_package_id: str
    immutable_package_metadata: dict[str, Any]
    accepted_target_observation_metadata: dict[str, Any]
    accepted_context_attachments: tuple[dict[str, Any], ...]
    accepted_comparator_attachments: tuple[dict[str, Any], ...]
    information_role_bindings: tuple[dict[str, Any], ...]
    observation_time_metadata: dict[str, Any]
    temporal_compatibility_metadata: dict[str, Any]
    coverage_metadata: dict[str, Any]
    missingness_metadata: dict[str, Any]
    inherited_diagnostics: tuple[dict[str, Any], ...]
    inherited_limitations: tuple[str, ...]
    intake_diagnostics: tuple[IntakeDiagnostic, ...]
    intake_limitations: tuple[str, ...]
    compatibility_state: IntakeCompatibilityState
    reproducibility_metadata: dict[str, Any]
    artifact_lineage: dict[str, Any]
    governing_versions: dict[str, str]
    exposes_scientific_result: bool = False
    exposes_formula_output: bool = False
    creates_signal: bool = False
    creates_factor: bool = False
    creates_rank: bool = False
    creates_score: bool = False
    computes_ic: bool = False
    computes_sharpe: bool = False
    creates_prediction: bool = False
    creates_model_feature: bool = False
    creates_model_label: bool = False
    creates_validation_result: bool = False
    makes_production_decision: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "accepted_comparator_attachments": list(self.accepted_comparator_attachments),
            "accepted_context_attachments": list(self.accepted_context_attachments),
            "accepted_target_observation_metadata": self.accepted_target_observation_metadata,
            "artifact_lineage": self.artifact_lineage,
            "compatibility_state": self.compatibility_state.value,
            "computes_ic": self.computes_ic,
            "computes_sharpe": self.computes_sharpe,
            "coverage_metadata": self.coverage_metadata,
            "creates_factor": self.creates_factor,
            "creates_model_feature": self.creates_model_feature,
            "creates_model_label": self.creates_model_label,
            "creates_prediction": self.creates_prediction,
            "creates_rank": self.creates_rank,
            "creates_score": self.creates_score,
            "creates_signal": self.creates_signal,
            "creates_validation_result": self.creates_validation_result,
            "exposes_formula_output": self.exposes_formula_output,
            "exposes_scientific_result": self.exposes_scientific_result,
            "governing_versions": self.governing_versions,
            "immutable_package_metadata": self.immutable_package_metadata,
            "information_role_bindings": list(self.information_role_bindings),
            "inherited_diagnostics": list(self.inherited_diagnostics),
            "inherited_limitations": list(self.inherited_limitations),
            "intake_diagnostics": [diag.to_dict() for diag in self.intake_diagnostics],
            "intake_limitations": list(self.intake_limitations),
            "makes_production_decision": self.makes_production_decision,
            "missingness_metadata": self.missingness_metadata,
            "observation_time_metadata": self.observation_time_metadata,
            "prepared_observation_package_id": self.prepared_observation_package_id,
            "reproducibility_metadata": self.reproducibility_metadata,
            "temporal_compatibility_metadata": self.temporal_compatibility_metadata,
        }


@dataclass(frozen=True)
class ScientificModuleIntakeResult:
    intake_evaluation_id: str
    prepared_observation_package_id: str
    prepared_observation_contract_version: str
    prepared_observation_implementation_version: str
    intake_contract_id: str
    intake_contract_version: str
    module_id: str
    module_version: str
    module_specification_version: str
    inherited_prepared_observation_readiness: po.PreparedObservationReadinessState
    compatibility_state: IntakeCompatibilityState
    target_compatibility: dict[str, Any]
    role_compatibility: dict[str, Any]
    context_compatibility: dict[str, Any]
    comparator_compatibility: dict[str, Any]
    temporal_compatibility: dict[str, Any]
    coverage_compatibility: dict[str, Any]
    missingness_compatibility: dict[str, Any]
    traceability_sufficiency: dict[str, Any]
    reproducibility_sufficiency: dict[str, Any]
    version_compatibility: dict[str, Any]
    inherited_diagnostics: tuple[po.PreparedObservationDiagnostic, ...]
    inherited_limitations: tuple[str, ...]
    intake_diagnostics: tuple[IntakeDiagnostic, ...]
    intake_limitations: tuple[str, ...]
    role_bindings: tuple[dict[str, Any], ...]
    context_bindings: tuple[dict[str, Any], ...]
    comparator_bindings: tuple[dict[str, Any], ...]
    artifact_lineage: dict[str, Any]
    governing_versions: dict[str, str]
    information_contract: IntakeInformationContract
    acquisition_performed: bool = False
    retrieval_performed: bool = False
    vendor_access_performed: bool = False
    api_access_performed: bool = False
    database_access_performed: bool = False
    authority_evaluation_performed: bool = False
    identity_construction_performed: bool = False
    identity_resolution_performed: bool = False
    context_construction_performed: bool = False
    context_interpretation_performed: bool = False
    comparator_construction_performed: bool = False
    peer_discovery_performed: bool = False
    scientific_similarity_performed: bool = False
    value_transformation_performed: bool = False
    normalization_performed: bool = False
    winsorization_performed: bool = False
    imputation_performed: bool = False
    interpolation_performed: bool = False
    filling_performed: bool = False
    resampling_performed: bool = False
    ranking_performed: bool = False
    scoring_performed: bool = False
    formula_execution_performed: bool = False
    return_calculation_performed: bool = False
    lag_construction_performed: bool = False
    signal_calculation_performed: bool = False
    factor_construction_performed: bool = False
    candidate_generation_performed: bool = False
    panel_construction_performed: bool = False
    ic_calculation_performed: bool = False
    statistical_testing_performed: bool = False
    hypothesis_evaluation_performed: bool = False
    validation_performed: bool = False
    portfolio_construction_performed: bool = False
    optimization_performed: bool = False
    production_decision_performed: bool = False
    ml_feature_created: bool = False
    ml_label_created: bool = False
    model_fit_performed: bool = False
    model_prediction_performed: bool = False
    model_training_performed: bool = False

    def to_ordered_dict(self) -> dict[str, Any]:
        return {
            "acquisition_performed": self.acquisition_performed,
            "api_access_performed": self.api_access_performed,
            "artifact_lineage": self.artifact_lineage,
            "authority_evaluation_performed": self.authority_evaluation_performed,
            "candidate_generation_performed": self.candidate_generation_performed,
            "comparator_bindings": list(self.comparator_bindings),
            "comparator_compatibility": self.comparator_compatibility,
            "comparator_construction_performed": self.comparator_construction_performed,
            "compatibility_state": self.compatibility_state.value,
            "context_bindings": list(self.context_bindings),
            "context_compatibility": self.context_compatibility,
            "context_construction_performed": self.context_construction_performed,
            "context_interpretation_performed": self.context_interpretation_performed,
            "coverage_compatibility": self.coverage_compatibility,
            "database_access_performed": self.database_access_performed,
            "factor_construction_performed": self.factor_construction_performed,
            "filling_performed": self.filling_performed,
            "formula_execution_performed": self.formula_execution_performed,
            "governing_versions": self.governing_versions,
            "hypothesis_evaluation_performed": self.hypothesis_evaluation_performed,
            "ic_calculation_performed": self.ic_calculation_performed,
            "identity_construction_performed": self.identity_construction_performed,
            "identity_resolution_performed": self.identity_resolution_performed,
            "imputation_performed": self.imputation_performed,
            "information_contract": self.information_contract.to_dict(),
            "inherited_diagnostics": [diag.to_dict() for diag in self.inherited_diagnostics],
            "inherited_limitations": list(self.inherited_limitations),
            "inherited_prepared_observation_readiness": self.inherited_prepared_observation_readiness.value,
            "intake_contract_id": self.intake_contract_id,
            "intake_contract_version": self.intake_contract_version,
            "intake_diagnostics": [diag.to_dict() for diag in self.intake_diagnostics],
            "intake_evaluation_id": self.intake_evaluation_id,
            "intake_limitations": list(self.intake_limitations),
            "interpolation_performed": self.interpolation_performed,
            "lag_construction_performed": self.lag_construction_performed,
            "missingness_compatibility": self.missingness_compatibility,
            "ml_feature_created": self.ml_feature_created,
            "ml_label_created": self.ml_label_created,
            "model_fit_performed": self.model_fit_performed,
            "model_prediction_performed": self.model_prediction_performed,
            "model_training_performed": self.model_training_performed,
            "module_id": self.module_id,
            "module_specification_version": self.module_specification_version,
            "module_version": self.module_version,
            "normalization_performed": self.normalization_performed,
            "optimization_performed": self.optimization_performed,
            "panel_construction_performed": self.panel_construction_performed,
            "peer_discovery_performed": self.peer_discovery_performed,
            "portfolio_construction_performed": self.portfolio_construction_performed,
            "prepared_observation_contract_version": self.prepared_observation_contract_version,
            "prepared_observation_implementation_version": self.prepared_observation_implementation_version,
            "prepared_observation_package_id": self.prepared_observation_package_id,
            "production_decision_performed": self.production_decision_performed,
            "ranking_performed": self.ranking_performed,
            "reproducibility_sufficiency": self.reproducibility_sufficiency,
            "resampling_performed": self.resampling_performed,
            "retrieval_performed": self.retrieval_performed,
            "return_calculation_performed": self.return_calculation_performed,
            "role_bindings": list(self.role_bindings),
            "role_compatibility": self.role_compatibility,
            "scientific_similarity_performed": self.scientific_similarity_performed,
            "scoring_performed": self.scoring_performed,
            "signal_calculation_performed": self.signal_calculation_performed,
            "statistical_testing_performed": self.statistical_testing_performed,
            "target_compatibility": self.target_compatibility,
            "temporal_compatibility": self.temporal_compatibility,
            "traceability_sufficiency": self.traceability_sufficiency,
            "validation_performed": self.validation_performed,
            "value_transformation_performed": self.value_transformation_performed,
            "vendor_access_performed": self.vendor_access_performed,
            "version_compatibility": self.version_compatibility,
            "winsorization_performed": self.winsorization_performed,
        }

    def stable_json(self) -> str:
        return json.dumps(self.to_ordered_dict(), sort_keys=True, separators=(",", ":"))


@dataclass(frozen=True)
class ScientificModuleIntakeFixture:
    fixture_id: str
    description: str
    request: IntakeEvaluationRequest
    expected_state: IntakeCompatibilityState
    expected_diagnostic_codes: tuple[IntakeDiagnosticCode, ...] = ()
    expected_limitations: tuple[str, ...] = ()


def _diag(code: IntakeDiagnosticCode, component: str, message: str, *, inherited: bool = False) -> IntakeDiagnostic:
    return IntakeDiagnostic(code=code, component=component, message=message, inherited=inherited)


def _dedupe(values: list[str]) -> tuple[str, ...]:
    return tuple(dict.fromkeys(values))


def _observation_time_form(obs_time: po.ObservationTimeMetadata) -> str:
    if obs_time.observation_time is not None:
        return "point"
    if obs_time.observation_interval is not None and obs_time.observation_interval.open_interval:
        return "open_interval"
    if obs_time.observation_interval is not None:
        return "interval"
    if obs_time.unknown_observation_time:
        return "unknown"
    if obs_time.unavailable_observation_time:
        return "unavailable"
    return "missing"


def _actual_role_entries(package: po.PreparedObservationResult) -> tuple[dict[str, Any], ...]:
    entries: list[dict[str, Any]] = []
    for context in package.context_attachments:
        entries.append({"attachment_type": "context", "element_id": context.context_id, "information_role": context.information_role})
    for comparator in package.comparator_attachments:
        entries.append({"attachment_type": "comparator", "element_id": comparator.relationship_id, "information_role": comparator.information_role})
    return tuple(entries)


def _lineage_has_required_fields(lineage: dict[str, Any], fields: tuple[str, ...]) -> bool:
    for field_name in fields:
        value = lineage.get(field_name)
        if value in (None, "", (), [], {}):
            return False
    return True


def _matches_context_requirement(context: po.ContextEvidenceAttachment, req: AttachmentRequirement) -> bool:
    return (
        context.information_role in req.allowed_roles
        and context.context_status in req.accepted_statuses
        and (not req.required_trace or bool(context.trace))
        and (req.allow_superseded or not context.superseded)
        and not context.conflicting
        and not context.duplicate
    )


def _matches_comparator_requirement(comparator: po.ComparatorAttachment, req: AttachmentRequirement) -> bool:
    return (
        comparator.information_role in req.allowed_roles
        and comparator.eligibility_state in req.accepted_statuses
        and comparator.temporal_applicability_state in req.accepted_temporal_states
        and (not req.required_trace or bool(comparator.trace))
        and (req.allow_superseded or not comparator.superseded)
        and not comparator.conflicting
        and not comparator.duplicate
    )


def _check_requirement_count(count: int, req: AttachmentRequirement) -> bool:
    if count < req.minimum_count:
        return False
    if req.maximum_count is not None and count > req.maximum_count:
        return False
    return True


def _version_dict(request: IntakeEvaluationRequest) -> dict[str, Any]:
    contract = request.intake_contract
    module = request.scientific_module
    package = request.prepared_observation
    return {
        "artifact_lineage_schema_version": request.artifact_lineage_schema_version,
        "diagnostic_schema_version": request.diagnostic_schema_version,
        "information_role_schema_version": request.information_role_schema_version,
        "intake_contract_version": contract.intake_contract_version if contract else "",
        "module_specification_version": module.module_specification_version if module else "",
        "module_version": module.module_version if module else "",
        "prepared_observation_contract_version": request.prepared_observation_contract_version,
        "prepared_observation_implementation_version": package.module_version,
        "reproducibility_schema_version": request.reproducibility_schema_version,
    }


def evaluate_scientific_module_intake(request: IntakeEvaluationRequest) -> ScientificModuleIntakeResult:
    package = request.prepared_observation
    contract = request.intake_contract
    module = request.scientific_module
    diagnostics: list[IntakeDiagnostic] = []
    limitations: list[str] = []
    role_entries = _actual_role_entries(package)
    role_counts = {role: sum(1 for entry in role_entries if entry["information_role"] == role) for role in APPROVED_INFORMATION_ROLES}
    inherited_codes = tuple(diag.code.value for diag in package.diagnostics)
    lineage = package.artifact_lineage.to_dict()
    version_compatibility = {"checked": True, "versions": _version_dict(request)}

    if package.readiness_state == po.PreparedObservationReadinessState.EXCLUDED:
        diagnostics.append(_diag(IntakeDiagnosticCode.PREPARED_OBSERVATION_EXCLUDED, "admission", "Prepared Observation package is excluded."))
    if request.raw_prepared_observation_bypass:
        diagnostics.append(_diag(IntakeDiagnosticCode.RAW_PREPARED_OBSERVATION_BYPASS, "admission", "Raw Prepared Observation bypass requested."))
    if request.direct_upstream_component_bypass:
        diagnostics.append(_diag(IntakeDiagnosticCode.DIRECT_UPSTREAM_COMPONENT_BYPASS, "admission", "Direct upstream component bypass requested."))
    if not package.package_id or not lineage or not request.prepared_observation_contract_version or not package.module_version:
        diagnostics.append(_diag(IntakeDiagnosticCode.INCOMPLETE_INTAKE_TRACEABILITY, "invariant", "Required intake invariant fields are missing."))
    if package.readiness_state == po.PreparedObservationReadinessState.STRUCTURALLY_INCOMPLETE:
        diagnostics.append(_diag(IntakeDiagnosticCode.PREPARED_OBSERVATION_STRUCTURALLY_INCOMPLETE, "admission", "Prepared Observation is structurally incomplete."))
    if package.readiness_state == po.PreparedObservationReadinessState.UNRESOLVED:
        diagnostics.append(_diag(IntakeDiagnosticCode.PREPARED_OBSERVATION_UNRESOLVED, "admission", "Prepared Observation is unresolved."))
    if package.readiness_state == po.PreparedObservationReadinessState.INSUFFICIENT_EVIDENCE:
        diagnostics.append(_diag(IntakeDiagnosticCode.PREPARED_OBSERVATION_INSUFFICIENT, "admission", "Prepared Observation evidence is insufficient."))
    if package.readiness_state == po.PreparedObservationReadinessState.CONDITIONALLY_READY:
        if not contract or contract.conditional_readiness_policy != "accept":
            diagnostics.append(_diag(IntakeDiagnosticCode.CONDITIONAL_READINESS_NOT_ACCEPTED, "admission", "Conditional Prepared Observation is not accepted by contract."))
        else:
            limitations.append("accepted conditional Prepared Observation")

    if contract is None:
        diagnostics.append(_diag(IntakeDiagnosticCode.MISSING_INTAKE_CONTRACT, "contract", "Intake contract is missing."))
    if module is None:
        diagnostics.append(_diag(IntakeDiagnosticCode.UNKNOWN_SCIENTIFIC_MODULE, "module", "Scientific module registration is missing."))

    if contract and module:
        if contract.intake_contract_version != module.intake_contract_version or contract.intake_contract_id != module.intake_contract_id:
            diagnostics.append(_diag(IntakeDiagnosticCode.INTAKE_CONTRACT_VERSION_MISMATCH, "version", "Module registration and intake contract do not match."))
        if contract.module_id != module.module_id:
            diagnostics.append(_diag(IntakeDiagnosticCode.UNKNOWN_SCIENTIFIC_MODULE, "module", "Module id is not accepted by the contract."))
        if contract.module_version != module.module_version:
            diagnostics.append(_diag(IntakeDiagnosticCode.UNKNOWN_MODULE_VERSION, "version", "Module version is not accepted by the contract."))
        if contract.module_specification_version != module.module_specification_version:
            diagnostics.append(_diag(IntakeDiagnosticCode.MODULE_SPECIFICATION_VERSION_MISMATCH, "version", "Module specification version mismatch."))
        if request.prepared_observation_contract_version not in contract.accepted_prepared_observation_contract_versions:
            diagnostics.append(_diag(IntakeDiagnosticCode.PREPARED_OBSERVATION_CONTRACT_VERSION_MISMATCH, "version", "Prepared Observation contract version is not accepted."))
        if package.module_version not in contract.accepted_prepared_observation_implementation_versions:
            diagnostics.append(_diag(IntakeDiagnosticCode.PREPARED_OBSERVATION_IMPLEMENTATION_VERSION_MISMATCH, "version", "Prepared Observation implementation version is not accepted."))
        if request.information_role_schema_version not in contract.accepted_information_role_schema_versions:
            diagnostics.append(_diag(IntakeDiagnosticCode.INFORMATION_ROLE_SCHEMA_VERSION_MISMATCH, "version", "Information Role schema version is not accepted."))
        if request.diagnostic_schema_version not in contract.accepted_diagnostic_schema_versions:
            diagnostics.append(_diag(IntakeDiagnosticCode.DIAGNOSTIC_SCHEMA_VERSION_MISMATCH, "version", "Diagnostic schema version is not accepted."))
        if request.artifact_lineage_schema_version not in contract.accepted_artifact_lineage_schema_versions:
            diagnostics.append(_diag(IntakeDiagnosticCode.ARTIFACT_LINEAGE_SCHEMA_VERSION_MISMATCH, "version", "Artifact lineage schema version is not accepted."))
        if request.reproducibility_schema_version not in contract.accepted_reproducibility_schema_versions:
            diagnostics.append(_diag(IntakeDiagnosticCode.REPRODUCIBILITY_SCHEMA_VERSION_MISMATCH, "version", "Reproducibility schema version is not accepted."))

        if package.readiness_state not in contract.accepted_prepared_observation_readiness_states and package.readiness_state not in (
            po.PreparedObservationReadinessState.EXCLUDED,
            po.PreparedObservationReadinessState.STRUCTURALLY_INCOMPLETE,
            po.PreparedObservationReadinessState.UNRESOLVED,
            po.PreparedObservationReadinessState.INSUFFICIENT_EVIDENCE,
            po.PreparedObservationReadinessState.CONDITIONALLY_READY,
        ):
            diagnostics.append(_diag(IntakeDiagnosticCode.PREPARED_OBSERVATION_STRUCTURALLY_INCOMPLETE, "admission", "Prepared Observation readiness is not accepted."))

        for inherited_code in inherited_codes:
            if inherited_code in contract.prohibited_inherited_diagnostics:
                diagnostics.append(_diag(IntakeDiagnosticCode.INHERITED_FATAL_DIAGNOSTIC, "inherited_diagnostic", f"Inherited diagnostic {inherited_code} is prohibited.", inherited=True))
        if po.PreparedObservationDiagnosticCode.UNRESOLVED_TEMPORAL_ALIGNMENT.value in inherited_codes:
            diagnostics.append(_diag(IntakeDiagnosticCode.INHERITED_UNRESOLVED_DIAGNOSTIC, "inherited_diagnostic", "Inherited unresolved temporal diagnostic is visible.", inherited=True))

        if not _lineage_has_required_fields(lineage, contract.required_lineage_fields):
            diagnostics.append(_diag(IntakeDiagnosticCode.MISSING_PREPARED_OBSERVATION_LINEAGE, "lineage", "Prepared Observation lineage is incomplete."))
        if request.missing_module_lineage or not module.artifact_reference:
            diagnostics.append(_diag(IntakeDiagnosticCode.MISSING_MODULE_LINEAGE, "lineage", "Scientific module lineage is incomplete."))

        repro = package.reproducibility.to_dict()
        if any(field_name not in repro or repro[field_name] in (None, "", False) for field_name in contract.required_reproducibility_fields):
            diagnostics.append(_diag(IntakeDiagnosticCode.INCOMPLETE_REPRODUCIBILITY_METADATA, "reproducibility", "Required reproducibility metadata is incomplete."))
        if not package.reproducibility.deterministic_serialization or package.reproducibility.environment_dependent_output or package.reproducibility.runtime_timestamp_used:
            diagnostics.append(_diag(IntakeDiagnosticCode.INCOMPLETE_REPRODUCIBILITY_METADATA, "reproducibility", "Reproducibility metadata is not deterministic."))

        actual_roles = tuple(entry["information_role"] for entry in role_entries)
        for role in actual_roles:
            if role not in APPROVED_INFORMATION_ROLES:
                diagnostics.append(_diag(IntakeDiagnosticCode.UNSUPPORTED_ROLE, "role", f"Unsupported role {role}."))
        for role in contract.prohibited_roles:
            if role in actual_roles:
                diagnostics.append(_diag(IntakeDiagnosticCode.PROHIBITED_ROLE_PRESENT, "role", f"Prohibited role {role} is present."))
        for role in contract.required_roles:
            if role_counts.get(role, 0) == 0:
                diagnostics.append(_diag(IntakeDiagnosticCode.MISSING_REQUIRED_ROLE, "role", f"Required role {role} is missing."))
        for rule in contract.role_cardinality_rules:
            count = role_counts.get(rule.role, 0)
            if count < rule.minimum_count or (rule.maximum_count is not None and count > rule.maximum_count):
                diagnostics.append(_diag(IntakeDiagnosticCode.ROLE_CARDINALITY_MISMATCH, "role", f"Role {rule.role} cardinality is incompatible."))
            for entry in role_entries:
                if entry["information_role"] == rule.role and entry["attachment_type"] not in rule.allowed_attachment_types:
                    diagnostics.append(_diag(IntakeDiagnosticCode.ROLE_ATTACHMENT_MISMATCH, "role", f"Role {rule.role} is bound to an unsupported attachment type."))

        if not package.target_observation or not package.target_observation.observation_available:
            diagnostics.append(_diag(IntakeDiagnosticCode.MISSING_TARGET_OBSERVATION, "target", "Target observation metadata is missing."))
        elif package.target_observation.observation_role not in contract.required_target_observation_types:
            diagnostics.append(_diag(IntakeDiagnosticCode.UNSUPPORTED_TARGET_OBSERVATION_TYPE, "target", "Target observation type is unsupported."))

        time_form = _observation_time_form(package.observation_time)
        if time_form not in contract.accepted_observation_time_forms:
            if time_form == "open_interval":
                diagnostics.append(_diag(IntakeDiagnosticCode.UNSUPPORTED_OPEN_INTERVAL, "temporal", "Open observation interval is unsupported."))
            else:
                diagnostics.append(_diag(IntakeDiagnosticCode.UNSUPPORTED_OBSERVATION_TIME_FORM, "temporal", f"Observation time form {time_form} is unsupported."))

        for req in contract.required_context_requirements:
            matches = tuple(context for context in package.context_attachments if _matches_context_requirement(context, req))
            if not _check_requirement_count(len(matches), req):
                diagnostics.append(_diag(IntakeDiagnosticCode.MISSING_REQUIRED_CONTEXT if len(matches) < req.minimum_count else IntakeDiagnosticCode.CONTEXT_CARDINALITY_MISMATCH, "context", f"Context requirement {req.requirement_id} is not satisfied."))
        for req in contract.optional_context_requirements:
            matches = tuple(context for context in package.context_attachments if _matches_context_requirement(context, req))
            if not matches:
                limitations.append("accepted optional attachment absence")
            elif any(context.superseded for context in matches):
                limitations.append("accepted superseded nonrequired attachment")
        for req in contract.prohibited_context_requirements:
            if any(context.information_role in req.allowed_roles for context in package.context_attachments):
                diagnostics.append(_diag(IntakeDiagnosticCode.PROHIBITED_CONTEXT_PRESENT, "context", f"Prohibited context requirement {req.requirement_id} is present."))
        if any(context.conflicting or context.duplicate for context in package.context_attachments):
            diagnostics.append(_diag(IntakeDiagnosticCode.CONTEXT_BINDING_CONFLICT, "context", "Context binding is conflicting or duplicate."))

        for req in contract.required_comparator_requirements:
            matches = tuple(comp for comp in package.comparator_attachments if _matches_comparator_requirement(comp, req))
            if not _check_requirement_count(len(matches), req):
                diagnostics.append(_diag(IntakeDiagnosticCode.MISSING_REQUIRED_COMPARATOR if len(matches) < req.minimum_count else IntakeDiagnosticCode.COMPARATOR_CARDINALITY_MISMATCH, "comparator", f"Comparator requirement {req.requirement_id} is not satisfied."))
        for req in contract.optional_comparator_requirements:
            matches = tuple(comp for comp in package.comparator_attachments if _matches_comparator_requirement(comp, req))
            if not matches:
                limitations.append("accepted optional attachment absence")
            elif any(comp.superseded for comp in matches):
                limitations.append("accepted superseded nonrequired attachment")
        for req in contract.prohibited_comparator_requirements:
            if any(comp.information_role in req.allowed_roles for comp in package.comparator_attachments):
                diagnostics.append(_diag(IntakeDiagnosticCode.PROHIBITED_COMPARATOR_PRESENT, "comparator", f"Prohibited comparator requirement {req.requirement_id} is present."))
        if any(comp.conflicting or comp.duplicate for comp in package.comparator_attachments):
            diagnostics.append(_diag(IntakeDiagnosticCode.COMPARATOR_BINDING_CONFLICT, "comparator", "Comparator binding is conflicting or duplicate."))
        if any(comp.temporal_applicability_state == "expired" or comp.eligibility_state in {"COMPARATOR_INELIGIBLE", "COMPARATOR_EXCLUDED"} for comp in package.comparator_attachments):
            diagnostics.append(_diag(IntakeDiagnosticCode.COMPARATOR_BINDING_CONFLICT, "comparator", "Comparator eligibility or applicability is incompatible."))

        if package.temporal_alignment_state not in contract.accepted_temporal_alignment_states:
            if package.temporal_alignment_state == po.TemporalAlignmentState.NON_OVERLAPPING:
                diagnostics.append(_diag(IntakeDiagnosticCode.TEMPORAL_NON_OVERLAP, "temporal", "Temporal alignment does not overlap."))
            elif package.temporal_alignment_state == po.TemporalAlignmentState.MIXED_FREQUENCY:
                diagnostics.append(_diag(IntakeDiagnosticCode.UNSUPPORTED_MIXED_FREQUENCY, "temporal", "Mixed observation frequency is unsupported."))
            elif package.temporal_alignment_state == po.TemporalAlignmentState.INCOMPLETE_TEMPORAL_TRACEABILITY:
                diagnostics.append(_diag(IntakeDiagnosticCode.INCOMPLETE_TEMPORAL_TRACEABILITY, "temporal", "Temporal traceability is incomplete."))
            else:
                diagnostics.append(_diag(IntakeDiagnosticCode.TEMPORAL_INCOMPATIBILITY, "temporal", "Temporal alignment is incompatible."))
        elif package.temporal_alignment_state == po.TemporalAlignmentState.PARTIALLY_ALIGNED:
            limitations.append("accepted partial temporal alignment")
        elif package.temporal_alignment_state == po.TemporalAlignmentState.STALE_CONTEXTUAL_EVIDENCE:
            limitations.append("accepted stale context")

        coverage = package.coverage.to_dict()
        for dim in contract.required_coverage_dimensions:
            expected = contract.minimum_coverage_rules.get(dim, True)
            if coverage.get(dim) is not expected:
                diagnostics.append(_diag(IntakeDiagnosticCode.INSUFFICIENT_REQUIRED_COVERAGE, "coverage", f"Coverage dimension {dim} is insufficient."))
        if coverage.get("conditionally_governed"):
            limitations.append("accepted conditional coverage")

        missing = package.missingness.to_dict()
        for name, value in missing.items():
            if value and name not in contract.accepted_missingness_conditions:
                diagnostics.append(_diag(IntakeDiagnosticCode.UNACCEPTABLE_REQUIRED_MISSINGNESS, "missingness", f"Missingness condition {name} is not accepted."))
            elif value and name in contract.accepted_missingness_conditions:
                limitations.append("accepted optional missingness" if name == "optional_field_missing" else f"accepted missingness {name}")

    if request.duplicate_intake_exposure:
        diagnostics.append(_diag(IntakeDiagnosticCode.DUPLICATE_INTAKE_EXPOSURE, "intake", "Duplicate intake exposure is unresolved."))
    if request.conflicting_intake_binding:
        diagnostics.append(_diag(IntakeDiagnosticCode.CONFLICTING_INTAKE_BINDING, "intake", "Intake binding is conflicting."))
    if package.readiness_state == po.PreparedObservationReadinessState.EXCLUDED and any(diag.code == po.PreparedObservationDiagnosticCode.SUPERSEDED_OBSERVATION_PACKAGE for diag in package.diagnostics):
        diagnostics.append(_diag(IntakeDiagnosticCode.SUPERSEDED_PREPARED_OBSERVATION, "admission", "Prepared Observation package is superseded."))

    diagnostic_tuple = tuple(diagnostics)
    limitation_tuple = _dedupe(limitations + list(package.limitations))
    codes = tuple(diag.code for diag in diagnostic_tuple)

    state = _classify_state(codes, limitation_tuple)
    if state == IntakeCompatibilityState.COMPATIBLE and package.readiness_state == po.PreparedObservationReadinessState.CONDITIONALLY_READY:
        state = IntakeCompatibilityState.CONDITIONALLY_COMPATIBLE
    if state == IntakeCompatibilityState.COMPATIBLE and limitation_tuple:
        state = IntakeCompatibilityState.CONDITIONALLY_COMPATIBLE

    contract_id = contract.intake_contract_id if contract else ""
    contract_version = contract.intake_contract_version if contract else ""
    module_id = module.module_id if module else ""
    module_version = module.module_version if module else ""
    module_spec_version = module.module_specification_version if module else ""
    intake_evaluation_id = f"intake_eval_{package.package_id}_{contract_id or 'missing_contract'}_{module_id or 'missing_module'}"
    artifact_lineage = _artifact_lineage(request, intake_evaluation_id)
    governing_versions = {
        "design": FROZEN_DESIGN_ID,
        "implementation": MODULE_ID,
        "implementation_version": MODULE_VERSION,
        "prepared_observations_implementation": po.MODULE_ID,
        "prepared_observations_version": package.module_version,
        "stable_serialization": STABLE_SERIALIZATION_VERSION,
    }
    role_bindings = tuple(
        {"attachment_type": entry["attachment_type"], "element_id": entry["element_id"], "information_role": entry["information_role"]}
        for entry in role_entries
    )
    context_bindings = tuple(context.to_dict() for context in package.context_attachments)
    comparator_bindings = tuple(comp.to_dict() for comp in package.comparator_attachments)
    target_compatibility = {
        "observation_role": package.target_observation.observation_role,
        "target_present": bool(package.target_observation and package.target_observation.observation_available),
    }
    role_compatibility = {
        "actual_roles": list(role_bindings),
        "required_roles": list(contract.required_roles if contract else ()),
    }
    context_compatibility = {"context_count": len(package.context_attachments)}
    comparator_compatibility = {"comparator_count": len(package.comparator_attachments)}
    temporal_compatibility = {
        "observation_time_form": _observation_time_form(package.observation_time),
        "temporal_alignment_state": package.temporal_alignment_state.value,
    }
    coverage_compatibility = package.coverage.to_dict()
    missingness_compatibility = package.missingness.to_dict()
    traceability_sufficiency = {
        "comparator_traces_present": all(bool(trace) for trace in package.comparator_traces) if package.comparator_traces else True,
        "lineage_complete": _lineage_has_required_fields(lineage, contract.required_lineage_fields if contract else ()),
        "pit_trace_present": bool(package.pit_trace),
        "source_authority_trace_present": bool(package.source_authority_trace),
    }
    reproducibility_sufficiency = package.reproducibility.to_dict()
    information_contract = IntakeInformationContract(
        prepared_observation_package_id=package.package_id,
        immutable_package_metadata=package.information_contract.package_metadata,
        accepted_target_observation_metadata=package.target_observation.to_dict(),
        accepted_context_attachments=context_bindings,
        accepted_comparator_attachments=comparator_bindings,
        information_role_bindings=role_bindings,
        observation_time_metadata=package.observation_time.to_dict(),
        temporal_compatibility_metadata=temporal_compatibility,
        coverage_metadata=coverage_compatibility,
        missingness_metadata=missingness_compatibility,
        inherited_diagnostics=tuple(diag.to_dict() for diag in package.diagnostics),
        inherited_limitations=package.limitations,
        intake_diagnostics=diagnostic_tuple,
        intake_limitations=limitation_tuple,
        compatibility_state=state,
        reproducibility_metadata=reproducibility_sufficiency,
        artifact_lineage=artifact_lineage,
        governing_versions=governing_versions,
    )
    return ScientificModuleIntakeResult(
        intake_evaluation_id=intake_evaluation_id,
        prepared_observation_package_id=package.package_id,
        prepared_observation_contract_version=request.prepared_observation_contract_version,
        prepared_observation_implementation_version=package.module_version,
        intake_contract_id=contract_id,
        intake_contract_version=contract_version,
        module_id=module_id,
        module_version=module_version,
        module_specification_version=module_spec_version,
        inherited_prepared_observation_readiness=package.readiness_state,
        compatibility_state=state,
        target_compatibility=target_compatibility,
        role_compatibility=role_compatibility,
        context_compatibility=context_compatibility,
        comparator_compatibility=comparator_compatibility,
        temporal_compatibility=temporal_compatibility,
        coverage_compatibility=coverage_compatibility,
        missingness_compatibility=missingness_compatibility,
        traceability_sufficiency=traceability_sufficiency,
        reproducibility_sufficiency=reproducibility_sufficiency,
        version_compatibility=version_compatibility,
        inherited_diagnostics=package.diagnostics,
        inherited_limitations=package.limitations,
        intake_diagnostics=diagnostic_tuple,
        intake_limitations=limitation_tuple,
        role_bindings=role_bindings,
        context_bindings=context_bindings,
        comparator_bindings=comparator_bindings,
        artifact_lineage=artifact_lineage,
        governing_versions=governing_versions,
        information_contract=information_contract,
    )


def _classify_state(codes: tuple[IntakeDiagnosticCode, ...], limitations: tuple[str, ...]) -> IntakeCompatibilityState:
    code_set = set(codes)
    if (
        IntakeDiagnosticCode.PREPARED_OBSERVATION_EXCLUDED in code_set
        or IntakeDiagnosticCode.RAW_PREPARED_OBSERVATION_BYPASS in code_set
        or IntakeDiagnosticCode.DIRECT_UPSTREAM_COMPONENT_BYPASS in code_set
        or IntakeDiagnosticCode.PROHIBITED_ROLE_PRESENT in code_set
        or IntakeDiagnosticCode.PROHIBITED_CONTEXT_PRESENT in code_set
        or IntakeDiagnosticCode.PROHIBITED_COMPARATOR_PRESENT in code_set
        or IntakeDiagnosticCode.SUPERSEDED_PREPARED_OBSERVATION in code_set
    ):
        return IntakeCompatibilityState.EXCLUDED
    if (
        IntakeDiagnosticCode.PREPARED_OBSERVATION_STRUCTURALLY_INCOMPLETE in code_set
        or IntakeDiagnosticCode.INCOMPLETE_INTAKE_TRACEABILITY in code_set
        or IntakeDiagnosticCode.INHERITED_FATAL_DIAGNOSTIC in code_set
    ):
        return IntakeCompatibilityState.INCOMPATIBLE
    if (
        IntakeDiagnosticCode.PREPARED_OBSERVATION_UNRESOLVED in code_set
        or IntakeDiagnosticCode.INHERITED_UNRESOLVED_DIAGNOSTIC in code_set
    ):
        return IntakeCompatibilityState.UNRESOLVED
    if (
        IntakeDiagnosticCode.PREPARED_OBSERVATION_INSUFFICIENT in code_set
        or IntakeDiagnosticCode.MISSING_INTAKE_CONTRACT in code_set
    ):
        return IntakeCompatibilityState.INSUFFICIENT_EVIDENCE
    if (
        IntakeDiagnosticCode.INTAKE_CONTRACT_VERSION_MISMATCH in code_set
        or IntakeDiagnosticCode.UNKNOWN_SCIENTIFIC_MODULE in code_set
        or IntakeDiagnosticCode.UNKNOWN_MODULE_VERSION in code_set
        or IntakeDiagnosticCode.MODULE_SPECIFICATION_VERSION_MISMATCH in code_set
        or IntakeDiagnosticCode.PREPARED_OBSERVATION_CONTRACT_VERSION_MISMATCH in code_set
        or IntakeDiagnosticCode.PREPARED_OBSERVATION_IMPLEMENTATION_VERSION_MISMATCH in code_set
        or IntakeDiagnosticCode.INFORMATION_ROLE_SCHEMA_VERSION_MISMATCH in code_set
        or IntakeDiagnosticCode.DIAGNOSTIC_SCHEMA_VERSION_MISMATCH in code_set
        or IntakeDiagnosticCode.ARTIFACT_LINEAGE_SCHEMA_VERSION_MISMATCH in code_set
        or IntakeDiagnosticCode.REPRODUCIBILITY_SCHEMA_VERSION_MISMATCH in code_set
        or IntakeDiagnosticCode.MISSING_PREPARED_OBSERVATION_LINEAGE in code_set
        or IntakeDiagnosticCode.MISSING_MODULE_LINEAGE in code_set
        or IntakeDiagnosticCode.INCOMPLETE_REPRODUCIBILITY_METADATA in code_set
        or IntakeDiagnosticCode.MISSING_REQUIRED_ROLE in code_set
        or IntakeDiagnosticCode.UNSUPPORTED_ROLE in code_set
        or IntakeDiagnosticCode.ROLE_CARDINALITY_MISMATCH in code_set
        or IntakeDiagnosticCode.ROLE_ATTACHMENT_MISMATCH in code_set
        or IntakeDiagnosticCode.MISSING_TARGET_OBSERVATION in code_set
        or IntakeDiagnosticCode.UNSUPPORTED_TARGET_OBSERVATION_TYPE in code_set
        or IntakeDiagnosticCode.UNSUPPORTED_OBSERVATION_TIME_FORM in code_set
        or IntakeDiagnosticCode.MISSING_REQUIRED_CONTEXT in code_set
        or IntakeDiagnosticCode.CONTEXT_CARDINALITY_MISMATCH in code_set
        or IntakeDiagnosticCode.CONTEXT_BINDING_CONFLICT in code_set
        or IntakeDiagnosticCode.MISSING_REQUIRED_COMPARATOR in code_set
        or IntakeDiagnosticCode.COMPARATOR_CARDINALITY_MISMATCH in code_set
        or IntakeDiagnosticCode.COMPARATOR_BINDING_CONFLICT in code_set
        or IntakeDiagnosticCode.TEMPORAL_INCOMPATIBILITY in code_set
        or IntakeDiagnosticCode.TEMPORAL_NON_OVERLAP in code_set
        or IntakeDiagnosticCode.UNSUPPORTED_OPEN_INTERVAL in code_set
        or IntakeDiagnosticCode.UNSUPPORTED_MIXED_FREQUENCY in code_set
        or IntakeDiagnosticCode.INCOMPLETE_TEMPORAL_TRACEABILITY in code_set
        or IntakeDiagnosticCode.UNACCEPTABLE_REQUIRED_MISSINGNESS in code_set
        or IntakeDiagnosticCode.INSUFFICIENT_REQUIRED_COVERAGE in code_set
        or IntakeDiagnosticCode.DUPLICATE_INTAKE_EXPOSURE in code_set
        or IntakeDiagnosticCode.CONFLICTING_INTAKE_BINDING in code_set
    ):
        return IntakeCompatibilityState.INCOMPATIBLE
    if IntakeDiagnosticCode.CONDITIONAL_READINESS_NOT_ACCEPTED in code_set:
        return IntakeCompatibilityState.INCOMPATIBLE
    if limitations:
        return IntakeCompatibilityState.CONDITIONALLY_COMPATIBLE
    return IntakeCompatibilityState.COMPATIBLE


def _artifact_lineage(request: IntakeEvaluationRequest, intake_evaluation_id: str) -> dict[str, Any]:
    package = request.prepared_observation
    lineage = package.artifact_lineage.to_dict()
    module = request.scientific_module
    contract = request.intake_contract
    return {
        "handoff_contract_artifact": f"handoff_contract_{intake_evaluation_id}",
        "intake_declaration_artifact": f"intake_declaration_{contract.intake_contract_id}" if contract else "",
        "intake_evaluation_artifact": f"intake_artifact_{intake_evaluation_id}",
        "prepared_observation_artifact": lineage.get("prepared_observation_artifact", ""),
        "scientific_execution_artifact": "",
        "scientific_module_specification_artifact": module.artifact_reference if module else "",
        "source_authority_artifacts": list(lineage.get("source_authority_artifacts", [])),
        "pit_identity_context_artifacts": list(lineage.get("pit_identity_context_artifacts", [])),
        "comparator_construction_artifacts": list(lineage.get("comparator_construction_artifacts", [])),
    }


def _po_result(fixture_id: str, **overrides: Any) -> po.PreparedObservationResult:
    record = po._base_record(fixture_id)
    if overrides:
        record = po._replace(record, **overrides)
    return po.evaluate_prepared_observation(record)


def _module(contract: ModuleIntakeContract | None = None, **overrides: Any) -> ScientificModuleRegistration:
    contract = contract or ModuleIntakeContract()
    values = {
        "module_id": contract.module_id,
        "module_version": contract.module_version,
        "module_specification_version": contract.module_specification_version,
        "intake_contract_id": contract.intake_contract_id,
        "intake_contract_version": contract.intake_contract_version,
        "governing_versions": {"design": FROZEN_DESIGN_ID, "implementation": MODULE_ID},
        "artifact_reference": f"module_spec_artifact_{contract.module_id}",
    }
    values.update(overrides)
    return ScientificModuleRegistration(**values)


def _request(
    fixture_id: str,
    *,
    package: po.PreparedObservationResult | None = None,
    contract: ModuleIntakeContract | None | str = None,
    module: ScientificModuleRegistration | None | str = "default",
    **overrides: Any,
) -> IntakeEvaluationRequest:
    contract_obj = None if contract == "missing" else contract if contract is not None else ModuleIntakeContract()
    module_obj = _module(contract_obj) if module == "default" else module
    values = {
        "prepared_observation": package or _po_result(fixture_id),
        "intake_contract": contract_obj,
        "scientific_module": module_obj,
        "fixture_id": fixture_id,
    }
    values.update(overrides)
    return IntakeEvaluationRequest(**values)


def _contract(**overrides: Any) -> ModuleIntakeContract:
    values = {**ModuleIntakeContract().__dict__}
    values.update(overrides)
    return ModuleIntakeContract(**values)


def canonical_scientific_module_intake_fixtures() -> tuple[ScientificModuleIntakeFixture, ...]:
    fixtures: list[ScientificModuleIntakeFixture] = []

    def add(
        fixture_id: str,
        description: str,
        request: IntakeEvaluationRequest,
        state: IntakeCompatibilityState,
        codes: tuple[IntakeDiagnosticCode, ...] = (),
        limitations: tuple[str, ...] = (),
    ) -> None:
        fixtures.append(ScientificModuleIntakeFixture(fixture_id, description, request, state, codes, limitations))

    target_only = _contract(required_roles=(), required_context_requirements=(), required_comparator_requirements=())
    optional_context = _contract(required_roles=(), required_context_requirements=(), required_comparator_requirements=(), optional_context_requirements=(AttachmentRequirement("optional_context", "optional", (po.InformationRole.CONTEXTUAL_CONTROL_INFORMATION.value,)),))
    required_context = _contract(required_roles=(po.InformationRole.CONTEXTUAL_CONTROL_INFORMATION.value,), required_comparator_requirements=())
    required_comparator = _contract(required_roles=(po.InformationRole.COMPARATOR_OR_BENCHMARK_INFORMATION.value,), required_context_requirements=())
    cond_contract = _contract(accepted_prepared_observation_readiness_states=(po.PreparedObservationReadinessState.STRUCTURALLY_READY, po.PreparedObservationReadinessState.CONDITIONALLY_READY), conditional_readiness_policy="accept", accepted_temporal_alignment_states=(po.TemporalAlignmentState.FULLY_ALIGNED, po.TemporalAlignmentState.PARTIALLY_ALIGNED), accepted_missingness_conditions=("optional_field_missing",))
    negative_contract = _contract(required_roles=(po.InformationRole.NEGATIVE_INFORMATION.value,), required_context_requirements=(AttachmentRequirement("negative_context", "required", (po.InformationRole.NEGATIVE_INFORMATION.value,), accepted_statuses=("present",)),), required_comparator_requirements=())

    add("SMI01_target_only", "Structurally ready target-only module.", _request("SMI01_target_only", contract=target_only), IntakeCompatibilityState.COMPATIBLE)
    add("SMI02_optional_context", "Target plus optional context.", _request("SMI02_optional_context", contract=optional_context), IntakeCompatibilityState.COMPATIBLE)
    add("SMI03_required_context", "Target plus required context.", _request("SMI03_required_context", contract=required_context), IntakeCompatibilityState.COMPATIBLE)
    add("SMI04_required_comparator", "Target plus required comparator.", _request("SMI04_required_comparator", contract=required_comparator), IntakeCompatibilityState.COMPATIBLE)
    add("SMI05_context_and_comparator", "Target plus context and comparator.", _request("SMI05_context_and_comparator"), IntakeCompatibilityState.COMPATIBLE)
    add("SMI06_accepted_conditional", "Accepted conditional Prepared Observation.", _request("SMI06_accepted_conditional", package=_po_result("SMI06_accepted_conditional", limitations=("relationship conditionally governed",)), contract=cond_contract), IntakeCompatibilityState.CONDITIONALLY_COMPATIBLE, limitations=("accepted conditional Prepared Observation",))
    add("SMI07_accepted_partial_temporal", "Accepted partial temporal alignment.", _request("SMI07_accepted_partial_temporal", package=_po_result("SMI07_accepted_partial_temporal", temporal_alignment_state=po.TemporalAlignmentState.PARTIALLY_ALIGNED), contract=cond_contract), IntakeCompatibilityState.CONDITIONALLY_COMPATIBLE, limitations=("accepted partial temporal alignment",))
    add("SMI08_accepted_optional_missingness", "Accepted optional missingness.", _request("SMI08_accepted_optional_missingness", package=_po_result("SMI08_accepted_optional_missingness", missingness=po.MissingnessMetadata(optional_field_missing=True)), contract=cond_contract), IntakeCompatibilityState.CONDITIONALLY_COMPATIBLE, limitations=("accepted optional missingness",))
    add("SMI09_optional_attachment_absence", "Accepted optional attachment absence.", _request("SMI09_optional_attachment_absence", package=_po_result("SMI09_optional_attachment_absence", context_attachments=(), required_context_ids=()), contract=optional_context), IntakeCompatibilityState.CONDITIONALLY_COMPATIBLE, limitations=("accepted optional attachment absence",))
    neg_context = po._context("SMI10_negative_role", information_role=po.InformationRole.NEGATIVE_INFORMATION.value)
    add("SMI10_negative_role", "Accepted negative-evidence role without promotion.", _request("SMI10_negative_role", package=_po_result("SMI10_negative_role", context_attachments=(neg_context,), comparator_attachments=(), required_context_ids=("context_SMI10_negative_role",), required_comparator_relationship_ids=()), contract=negative_contract), IntakeCompatibilityState.COMPATIBLE)

    add("SMI11_excluded_po", "Excluded Prepared Observation.", _request("SMI11_excluded_po", package=_po_result("SMI11_excluded_po", explicit_exclusion=True)), IntakeCompatibilityState.EXCLUDED, (IntakeDiagnosticCode.PREPARED_OBSERVATION_EXCLUDED,))
    add("SMI12_structurally_incomplete_po", "Structurally incomplete Prepared Observation.", _request("SMI12_structurally_incomplete_po", package=_po_result("SMI12_structurally_incomplete_po", incomplete_traceability=True)), IntakeCompatibilityState.INCOMPATIBLE, (IntakeDiagnosticCode.PREPARED_OBSERVATION_STRUCTURALLY_INCOMPLETE,))
    add("SMI13_unresolved_po", "Unresolved Prepared Observation.", _request("SMI13_unresolved_po", package=_po_result("SMI13_unresolved_po", temporal_alignment_state=po.TemporalAlignmentState.UNKNOWN_ALIGNMENT)), IntakeCompatibilityState.UNRESOLVED, (IntakeDiagnosticCode.PREPARED_OBSERVATION_UNRESOLVED,))
    add("SMI14_insufficient_po", "Insufficient Prepared Observation.", _request("SMI14_insufficient_po", package=_po_result("SMI14_insufficient_po", coverage=po.CoverageMetadata(context_coverage=False))), IntakeCompatibilityState.INSUFFICIENT_EVIDENCE, (IntakeDiagnosticCode.PREPARED_OBSERVATION_INSUFFICIENT,))
    add("SMI15_conditional_rejected", "Conditional Prepared Observation rejected.", _request("SMI15_conditional_rejected", package=_po_result("SMI15_conditional_rejected", limitations=("relationship conditionally governed",))), IntakeCompatibilityState.INCOMPATIBLE, (IntakeDiagnosticCode.CONDITIONAL_READINESS_NOT_ACCEPTED,))
    add("SMI16_missing_contract", "Missing intake contract.", _request("SMI16_missing_contract", contract="missing", module=None), IntakeCompatibilityState.INSUFFICIENT_EVIDENCE, (IntakeDiagnosticCode.MISSING_INTAKE_CONTRACT,))
    add("SMI17_unknown_module", "Unknown module.", _request("SMI17_unknown_module", module=None), IntakeCompatibilityState.INCOMPATIBLE, (IntakeDiagnosticCode.UNKNOWN_SCIENTIFIC_MODULE,))
    add("SMI18_contract_version_mismatch", "Intake contract version mismatch.", _request("SMI18_contract_version_mismatch", module=_module(ModuleIntakeContract(), intake_contract_version="v2")), IntakeCompatibilityState.INCOMPATIBLE, (IntakeDiagnosticCode.INTAKE_CONTRACT_VERSION_MISMATCH,))
    add("SMI19_module_version_mismatch", "Module version mismatch.", _request("SMI19_module_version_mismatch", module=_module(ModuleIntakeContract(), module_version="v2")), IntakeCompatibilityState.INCOMPATIBLE, (IntakeDiagnosticCode.UNKNOWN_MODULE_VERSION,))
    add("SMI20_po_contract_version_mismatch", "Prepared Observation contract version mismatch.", _request("SMI20_po_contract_version_mismatch", prepared_observation_contract_version="v2"), IntakeCompatibilityState.INCOMPATIBLE, (IntakeDiagnosticCode.PREPARED_OBSERVATION_CONTRACT_VERSION_MISMATCH,))
    add("SMI21_role_schema_mismatch", "Role schema mismatch.", _request("SMI21_role_schema_mismatch", information_role_schema_version="other"), IntakeCompatibilityState.INCOMPATIBLE, (IntakeDiagnosticCode.INFORMATION_ROLE_SCHEMA_VERSION_MISMATCH,))
    add("SMI22_diagnostic_schema_mismatch", "Diagnostic schema mismatch.", _request("SMI22_diagnostic_schema_mismatch", diagnostic_schema_version="other"), IntakeCompatibilityState.INCOMPATIBLE, (IntakeDiagnosticCode.DIAGNOSTIC_SCHEMA_VERSION_MISMATCH,))
    add("SMI23_lineage_schema_mismatch", "Lineage schema mismatch.", _request("SMI23_lineage_schema_mismatch", artifact_lineage_schema_version="other"), IntakeCompatibilityState.INCOMPATIBLE, (IntakeDiagnosticCode.ARTIFACT_LINEAGE_SCHEMA_VERSION_MISMATCH,))
    add("SMI24_repro_schema_mismatch", "Reproducibility schema mismatch.", _request("SMI24_repro_schema_mismatch", reproducibility_schema_version="other"), IntakeCompatibilityState.INCOMPATIBLE, (IntakeDiagnosticCode.REPRODUCIBILITY_SCHEMA_VERSION_MISMATCH,))

    add("SMI25_missing_required_role", "Missing required role.", _request("SMI25_missing_required_role", contract=_contract(required_roles=(po.InformationRole.VALIDATED_ALPHA_INFORMATION.value,))), IntakeCompatibilityState.INCOMPATIBLE, (IntakeDiagnosticCode.MISSING_REQUIRED_ROLE,))
    add("SMI26_prohibited_role", "Prohibited role present.", _request("SMI26_prohibited_role", contract=_contract(prohibited_roles=(po.InformationRole.CONTEXTUAL_CONTROL_INFORMATION.value,))), IntakeCompatibilityState.EXCLUDED, (IntakeDiagnosticCode.PROHIBITED_ROLE_PRESENT,))
    bad_context = po._context("SMI27_unsupported_role", information_role="UNSUPPORTED_ROLE")
    add("SMI27_unsupported_role", "Unsupported role.", _request("SMI27_unsupported_role", package=_po_result("SMI27_unsupported_role", context_attachments=(bad_context,))), IntakeCompatibilityState.INSUFFICIENT_EVIDENCE, (IntakeDiagnosticCode.UNSUPPORTED_ROLE,))
    add("SMI28_role_cardinality", "Role cardinality mismatch.", _request("SMI28_role_cardinality", contract=_contract(role_cardinality_rules=(RoleCardinalityRule(po.InformationRole.CONTEXTUAL_CONTROL_INFORMATION.value, minimum_count=2),))), IntakeCompatibilityState.INCOMPATIBLE, (IntakeDiagnosticCode.ROLE_CARDINALITY_MISMATCH,))
    add("SMI29_role_attachment", "Role-to-attachment mismatch.", _request("SMI29_role_attachment", contract=_contract(role_cardinality_rules=(RoleCardinalityRule(po.InformationRole.COMPARATOR_OR_BENCHMARK_INFORMATION.value, minimum_count=1, allowed_attachment_types=("context",)),))), IntakeCompatibilityState.INCOMPATIBLE, (IntakeDiagnosticCode.ROLE_ATTACHMENT_MISMATCH,))
    diag_alpha_contract = _contract(required_roles=(po.InformationRole.VALIDATED_ALPHA_INFORMATION.value,), required_context_requirements=(AttachmentRequirement("alpha_context", "required", (po.InformationRole.VALIDATED_ALPHA_INFORMATION.value,), accepted_statuses=("present",)),), required_comparator_requirements=())
    for idx, role, desc in (
        ("SMI30_diag_alpha_substitution", po.InformationRole.DIAGNOSTIC_INFORMATION.value, "Diagnostic evidence attempting alpha substitution."),
        ("SMI31_explain_supported_substitution", po.InformationRole.EXPLANATORY_ONLY_INFORMATION.value, "Explanatory evidence attempting supported-alpha substitution."),
        ("SMI32_negative_alpha_substitution", po.InformationRole.NEGATIVE_INFORMATION.value, "Negative evidence attempting alpha substitution."),
        ("SMI33_comparator_target_alpha_substitution", po.InformationRole.COMPARATOR_OR_BENCHMARK_INFORMATION.value, "Comparator role attempting target-alpha substitution."),
    ):
        pkg = _po_result(idx, context_attachments=(po._context(idx, information_role=role),), comparator_attachments=(), required_comparator_relationship_ids=())
        add(idx, desc, _request(idx, package=pkg, contract=diag_alpha_contract), IntakeCompatibilityState.INCOMPATIBLE, (IntakeDiagnosticCode.MISSING_REQUIRED_ROLE, IntakeDiagnosticCode.MISSING_REQUIRED_CONTEXT))

    add("SMI34_missing_target", "Missing target observation.", _request("SMI34_missing_target", package=_po_result("SMI34_missing_target", target_observation=po.TargetObservationMetadata("synthetic_target", ("target_interval_SMI34_missing_target",), "target_interval_SMI34_missing_target", observation_available=False))), IntakeCompatibilityState.INCOMPATIBLE, (IntakeDiagnosticCode.MISSING_TARGET_OBSERVATION,))
    add("SMI35_unsupported_target_type", "Unsupported target type.", _request("SMI35_unsupported_target_type", package=_po_result("SMI35_unsupported_target_type", target_observation=po.TargetObservationMetadata("synthetic_target", ("target_interval_SMI35_unsupported_target_type",), "target_interval_SMI35_unsupported_target_type", observation_role="unsupported_target"))), IntakeCompatibilityState.INCOMPATIBLE, (IntakeDiagnosticCode.UNSUPPORTED_TARGET_OBSERVATION_TYPE,))
    add("SMI36_missing_context", "Missing required context.", _request("SMI36_missing_context", package=_po_result("SMI36_missing_context", context_attachments=(), required_context_ids=())), IntakeCompatibilityState.INCOMPATIBLE, (IntakeDiagnosticCode.MISSING_REQUIRED_CONTEXT,))
    add("SMI37_prohibited_context", "Prohibited context.", _request("SMI37_prohibited_context", contract=_contract(prohibited_context_requirements=(AttachmentRequirement("prohibit_context", "prohibited", (po.InformationRole.CONTEXTUAL_CONTROL_INFORMATION.value,)),))), IntakeCompatibilityState.EXCLUDED, (IntakeDiagnosticCode.PROHIBITED_CONTEXT_PRESENT,))
    add("SMI38_context_cardinality", "Context cardinality mismatch.", _request("SMI38_context_cardinality", contract=_contract(required_context_requirements=(AttachmentRequirement("two_contexts", "required", (po.InformationRole.CONTEXTUAL_CONTROL_INFORMATION.value,), minimum_count=2, accepted_statuses=("present",)),))), IntakeCompatibilityState.INCOMPATIBLE, (IntakeDiagnosticCode.MISSING_REQUIRED_CONTEXT,))
    add("SMI39_context_conflict", "Context conflict.", _request("SMI39_context_conflict", package=_po_result("SMI39_context_conflict", context_attachments=(po._context("SMI39_context_conflict", conflicting=True),))), IntakeCompatibilityState.INCOMPATIBLE, (IntakeDiagnosticCode.CONTEXT_BINDING_CONFLICT,))
    add("SMI40_missing_comparator", "Missing required comparator.", _request("SMI40_missing_comparator", package=_po_result("SMI40_missing_comparator", comparator_attachments=(), required_comparator_relationship_ids=())), IntakeCompatibilityState.INCOMPATIBLE, (IntakeDiagnosticCode.MISSING_REQUIRED_COMPARATOR,))
    add("SMI41_prohibited_comparator", "Prohibited comparator.", _request("SMI41_prohibited_comparator", contract=_contract(prohibited_comparator_requirements=(AttachmentRequirement("prohibit_comparator", "prohibited", (po.InformationRole.COMPARATOR_OR_BENCHMARK_INFORMATION.value,)),))), IntakeCompatibilityState.EXCLUDED, (IntakeDiagnosticCode.PROHIBITED_COMPARATOR_PRESENT,))
    add("SMI42_comparator_cardinality", "Comparator cardinality mismatch.", _request("SMI42_comparator_cardinality", contract=_contract(required_comparator_requirements=(AttachmentRequirement("two_comparators", "required", (po.InformationRole.COMPARATOR_OR_BENCHMARK_INFORMATION.value,), minimum_count=2, accepted_statuses=("COMPARATOR_ELIGIBLE",)),))), IntakeCompatibilityState.INCOMPATIBLE, (IntakeDiagnosticCode.MISSING_REQUIRED_COMPARATOR,))
    add("SMI43_comparator_conflict", "Comparator conflict.", _request("SMI43_comparator_conflict", package=_po_result("SMI43_comparator_conflict", comparator_attachments=(po._comparator("SMI43_comparator_conflict", conflicting=True),))), IntakeCompatibilityState.INCOMPATIBLE, (IntakeDiagnosticCode.COMPARATOR_BINDING_CONFLICT,))
    add("SMI44_expired_comparator", "Expired comparator.", _request("SMI44_expired_comparator", package=_po_result("SMI44_expired_comparator", comparator_attachments=(po._comparator("SMI44_expired_comparator", temporal_applicability_state="expired"),))), IntakeCompatibilityState.INCOMPATIBLE, (IntakeDiagnosticCode.COMPARATOR_BINDING_CONFLICT,))

    add("SMI45_temporal_non_overlap", "Temporal non-overlap.", _request("SMI45_temporal_non_overlap", package=_po_result("SMI45_temporal_non_overlap", temporal_alignment_state=po.TemporalAlignmentState.NON_OVERLAPPING)), IntakeCompatibilityState.INCOMPATIBLE, (IntakeDiagnosticCode.PREPARED_OBSERVATION_STRUCTURALLY_INCOMPLETE, IntakeDiagnosticCode.TEMPORAL_NON_OVERLAP))
    add("SMI46_unknown_temporal", "Unknown temporal alignment.", _request("SMI46_unknown_temporal", package=_po_result("SMI46_unknown_temporal", temporal_alignment_state=po.TemporalAlignmentState.UNKNOWN_ALIGNMENT)), IntakeCompatibilityState.UNRESOLVED, (IntakeDiagnosticCode.PREPARED_OBSERVATION_UNRESOLVED,))
    add(
        "SMI47_open_interval",
        "Unsupported open interval.",
        _request(
            "SMI47_open_interval",
            package=_po_result(
                "SMI47_open_interval",
                observation_time=po._time(interval=po.ObservationInterval("open", 1, None, open_interval=True)),
            ),
        ),
        IntakeCompatibilityState.INCOMPATIBLE,
        (IntakeDiagnosticCode.CONDITIONAL_READINESS_NOT_ACCEPTED, IntakeDiagnosticCode.UNSUPPORTED_OPEN_INTERVAL),
    )
    add(
        "SMI48_mixed_frequency",
        "Unsupported mixed frequency.",
        _request("SMI48_mixed_frequency", package=_po_result("SMI48_mixed_frequency", temporal_alignment_state=po.TemporalAlignmentState.MIXED_FREQUENCY)),
        IntakeCompatibilityState.INCOMPATIBLE,
        (IntakeDiagnosticCode.CONDITIONAL_READINESS_NOT_ACCEPTED, IntakeDiagnosticCode.UNSUPPORTED_MIXED_FREQUENCY),
    )
    add(
        "SMI49_discontinuous_identity",
        "Discontinuous identity applicability.",
        _request("SMI49_discontinuous_identity", package=_po_result("SMI49_discontinuous_identity", temporal_alignment_state=po.TemporalAlignmentState.DISCONTINUOUS_IDENTITY_APPLICABILITY)),
        IntakeCompatibilityState.INCOMPATIBLE,
        (IntakeDiagnosticCode.CONDITIONAL_READINESS_NOT_ACCEPTED, IntakeDiagnosticCode.TEMPORAL_INCOMPATIBILITY),
    )
    add("SMI50_incomplete_temporal_trace", "Incomplete temporal traceability.", _request("SMI50_incomplete_temporal_trace", package=_po_result("SMI50_incomplete_temporal_trace", temporal_alignment_state=po.TemporalAlignmentState.INCOMPLETE_TEMPORAL_TRACEABILITY)), IntakeCompatibilityState.UNRESOLVED, (IntakeDiagnosticCode.PREPARED_OBSERVATION_UNRESOLVED, IntakeDiagnosticCode.INCOMPLETE_TEMPORAL_TRACEABILITY))

    add("SMI51_insufficient_target_coverage", "Insufficient target coverage.", _request("SMI51_insufficient_target_coverage", package=_po_result("SMI51_insufficient_target_coverage", coverage=po.CoverageMetadata(target_coverage=False))), IntakeCompatibilityState.INSUFFICIENT_EVIDENCE, (IntakeDiagnosticCode.PREPARED_OBSERVATION_INSUFFICIENT, IntakeDiagnosticCode.INSUFFICIENT_REQUIRED_COVERAGE))
    add("SMI52_insufficient_comparator_coverage", "Insufficient comparator coverage.", _request("SMI52_insufficient_comparator_coverage", package=_po_result("SMI52_insufficient_comparator_coverage", coverage=po.CoverageMetadata(comparator_coverage=False))), IntakeCompatibilityState.INSUFFICIENT_EVIDENCE, (IntakeDiagnosticCode.PREPARED_OBSERVATION_INSUFFICIENT, IntakeDiagnosticCode.INSUFFICIENT_REQUIRED_COVERAGE))
    add("SMI53_insufficient_context_coverage", "Insufficient context coverage.", _request("SMI53_insufficient_context_coverage", package=_po_result("SMI53_insufficient_context_coverage", coverage=po.CoverageMetadata(context_coverage=False))), IntakeCompatibilityState.INSUFFICIENT_EVIDENCE, (IntakeDiagnosticCode.PREPARED_OBSERVATION_INSUFFICIENT, IntakeDiagnosticCode.INSUFFICIENT_REQUIRED_COVERAGE))
    add("SMI54_required_missingness", "Unacceptable required missingness.", _request("SMI54_required_missingness", package=_po_result("SMI54_required_missingness", missingness=po.MissingnessMetadata(required_field_missing=True))), IntakeCompatibilityState.INCOMPATIBLE, (IntakeDiagnosticCode.PREPARED_OBSERVATION_STRUCTURALLY_INCOMPLETE, IntakeDiagnosticCode.UNACCEPTABLE_REQUIRED_MISSINGNESS))
    add("SMI55_missing_po_lineage", "Missing Prepared Observation lineage.", _request("SMI55_missing_po_lineage", package=_po_result("SMI55_missing_po_lineage", artifact_lineage=po.ArtifactLineageMetadata((), (), (), ""))), IntakeCompatibilityState.INCOMPATIBLE, (IntakeDiagnosticCode.MISSING_PREPARED_OBSERVATION_LINEAGE,))
    add("SMI56_missing_module_lineage", "Missing module lineage.", _request("SMI56_missing_module_lineage", missing_module_lineage=True), IntakeCompatibilityState.INCOMPATIBLE, (IntakeDiagnosticCode.MISSING_MODULE_LINEAGE,))
    add("SMI57_incomplete_repro", "Incomplete reproducibility metadata.", _request("SMI57_incomplete_repro", package=_po_result("SMI57_incomplete_repro", reproducibility=po.ReproducibilityMetadata(deterministic_serialization=False))), IntakeCompatibilityState.INCOMPATIBLE, (IntakeDiagnosticCode.PREPARED_OBSERVATION_STRUCTURALLY_INCOMPLETE, IntakeDiagnosticCode.INCOMPLETE_REPRODUCIBILITY_METADATA))
    add("SMI58_prohibited_inherited_fatal", "Prohibited inherited fatal diagnostic.", _request("SMI58_prohibited_inherited_fatal", package=_po_result("SMI58_prohibited_inherited_fatal", source_authority_trace={"fixture_id": "SA_fatal", "fatal_diagnostics": ["fatal"]})), IntakeCompatibilityState.INCOMPATIBLE, (IntakeDiagnosticCode.PREPARED_OBSERVATION_STRUCTURALLY_INCOMPLETE, IntakeDiagnosticCode.INHERITED_FATAL_DIAGNOSTIC))
    add("SMI59_inherited_unresolved", "Inherited unresolved diagnostic.", _request("SMI59_inherited_unresolved", package=_po_result("SMI59_inherited_unresolved", temporal_alignment_state=po.TemporalAlignmentState.UNKNOWN_ALIGNMENT)), IntakeCompatibilityState.UNRESOLVED, (IntakeDiagnosticCode.INHERITED_UNRESOLVED_DIAGNOSTIC,))
    add("SMI60_raw_bypass", "Raw Prepared Observation bypass.", _request("SMI60_raw_bypass", raw_prepared_observation_bypass=True), IntakeCompatibilityState.EXCLUDED, (IntakeDiagnosticCode.RAW_PREPARED_OBSERVATION_BYPASS,))
    add("SMI61_direct_upstream_bypass", "Direct upstream component bypass.", _request("SMI61_direct_upstream_bypass", direct_upstream_component_bypass=True), IntakeCompatibilityState.EXCLUDED, (IntakeDiagnosticCode.DIRECT_UPSTREAM_COMPONENT_BYPASS,))
    add("SMI62_duplicate_intake", "Duplicate intake exposure.", _request("SMI62_duplicate_intake", duplicate_intake_exposure=True), IntakeCompatibilityState.INCOMPATIBLE, (IntakeDiagnosticCode.DUPLICATE_INTAKE_EXPOSURE,))
    add("SMI63_conflicting_intake", "Conflicting intake binding.", _request("SMI63_conflicting_intake", conflicting_intake_binding=True), IntakeCompatibilityState.INCOMPATIBLE, (IntakeDiagnosticCode.CONFLICTING_INTAKE_BINDING,))
    add("SMI64_superseded_po", "Superseded Prepared Observation.", _request("SMI64_superseded_po", package=_po_result("SMI64_superseded_po", superseded_package=True)), IntakeCompatibilityState.EXCLUDED, (IntakeDiagnosticCode.SUPERSEDED_PREPARED_OBSERVATION,))
    opt_sup_context = po._context("SMI65_superseded_optional_context", superseded=True)
    add(
        "SMI65_superseded_optional_context",
        "Superseded optional context accepted conditionally.",
        _request(
            "SMI65_superseded_optional_context",
            package=_po_result("SMI65_superseded_optional_context", context_attachments=(opt_sup_context,), required_context_ids=()),
            contract=_contract(
                required_roles=(po.InformationRole.COMPARATOR_OR_BENCHMARK_INFORMATION.value,),
                required_context_requirements=(),
                optional_context_requirements=(
                    AttachmentRequirement(
                        "optional_sup_context",
                        "optional",
                        (po.InformationRole.CONTEXTUAL_CONTROL_INFORMATION.value,),
                        allow_superseded=True,
                        accepted_statuses=("present",),
                    ),
                ),
                accepted_prepared_observation_readiness_states=(
                    po.PreparedObservationReadinessState.STRUCTURALLY_READY,
                    po.PreparedObservationReadinessState.CONDITIONALLY_READY,
                ),
                conditional_readiness_policy="accept",
            ),
        ),
        IntakeCompatibilityState.CONDITIONALLY_COMPATIBLE,
        limitations=("accepted superseded nonrequired attachment",),
    )
    add("SMI66_duplicate_comparator", "Duplicate comparator exposure.", _request("SMI66_duplicate_comparator", package=_po_result("SMI66_duplicate_comparator", comparator_attachments=(po._comparator("SMI66_duplicate_comparator", duplicate=True),))), IntakeCompatibilityState.INCOMPATIBLE, (IntakeDiagnosticCode.COMPARATOR_BINDING_CONFLICT,))

    return tuple(fixtures)


def scientific_module_intake_guardrail_manifest() -> dict[str, bool]:
    return {
        "synthetic_metadata_only": True,
        "acquisition_performed": False,
        "retrieval_performed": False,
        "vendor_access_performed": False,
        "api_access_performed": False,
        "database_access_performed": False,
        "authority_evaluation_performed": False,
        "identity_construction_performed": False,
        "identity_resolution_performed": False,
        "context_construction_performed": False,
        "context_interpretation_performed": False,
        "comparator_construction_performed": False,
        "peer_discovery_performed": False,
        "scientific_similarity_performed": False,
        "value_transformation_performed": False,
        "normalization_performed": False,
        "winsorization_performed": False,
        "imputation_performed": False,
        "interpolation_performed": False,
        "filling_performed": False,
        "resampling_performed": False,
        "ranking_performed": False,
        "scoring_performed": False,
        "formula_execution_performed": False,
        "return_calculation_performed": False,
        "lag_construction_performed": False,
        "signal_calculation_performed": False,
        "factor_construction_performed": False,
        "candidate_generation_performed": False,
        "panel_construction_performed": False,
        "ic_calculation_performed": False,
        "statistical_testing_performed": False,
        "hypothesis_evaluation_performed": False,
        "validation_performed": False,
        "portfolio_construction_performed": False,
        "optimization_performed": False,
        "production_decision_performed": False,
        "ml_feature_created": False,
        "ml_label_created": False,
        "model_fit_performed": False,
        "model_prediction_performed": False,
        "model_training_performed": False,
    }
