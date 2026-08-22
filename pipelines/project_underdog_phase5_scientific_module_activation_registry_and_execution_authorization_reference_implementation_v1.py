from __future__ import annotations

from dataclasses import dataclass, field, is_dataclass
from enum import Enum
import hashlib
import json
from typing import Any


MODULE_ID = "project_underdog_phase5_scientific_module_activation_registry_and_execution_authorization_reference_implementation_v1"
MODULE_VERSION = "v1"
FROZEN_DESIGN_ID = "project_underdog_phase5_scientific_module_intake_platform_integration_readiness_and_first_scientific_module_activation_design_v1"
LAYER_NAME = "Project Underdog Phase 5 Scientific Module Activation Registry And Execution Authorization"
STABLE_SERIALIZATION_VERSION = "stable_json_v1"

SELECTED_RESEARCH_PROGRAM_ID = "Peer-Relative Post-Stress Repair And Stabilization Asymmetry"
SELECTED_RESEARCH_PROGRAM_VERSION = "phase5_selected_program_v1"
NARROW_ACTIVATION_SPECIFICATION_ID = "Common-Versus-Idiosyncratic Post-Stress Repair Decomposition"
NARROW_ACTIVATION_SPECIFICATION_VERSION = "phase5_first_activation_boundary_v1"

DEFAULT_MODULE_ID = "project_underdog_phase5_first_scientific_module_common_idiosyncratic_repair_decomposition_v1"
DEFAULT_MODULE_VERSION = "v1"
DEFAULT_MODULE_SPECIFICATION_VERSION = "module_specification_v1"
DEFAULT_INTAKE_CONTRACT_ID = "synthetic_scientific_module_intake_contract_v1"
DEFAULT_INTAKE_CONTRACT_VERSION = "v1"
DEFAULT_ADAPTER_ID = "synthetic_activation_registry_adapter_v1"
DEFAULT_ADAPTER_VERSION = "v1"
DEFAULT_INPUT_CONTRACT_ID = "synthetic_module_input_contract_v1"
DEFAULT_INPUT_CONTRACT_VERSION = "v1"
DEFAULT_OUTPUT_CONTRACT_ID = "synthetic_module_output_contract_v1"
DEFAULT_OUTPUT_CONTRACT_VERSION = "v1"
DEFAULT_SCIENTIFIC_SPECIFICATION_ID = "synthetic_common_idiosyncratic_repair_scientific_specification_v1"
DEFAULT_SCIENTIFIC_SPECIFICATION_VERSION = "v1"
DEFAULT_FROZEN_HORIZON_SPECIFICATION_ID = "synthetic_frozen_horizon_specification_v1"
DEFAULT_FROZEN_HORIZON_SPECIFICATION_VERSION = "v1"
DEFAULT_INFORMATION_ROLE_SCHEMA_VERSION = "project_underdog_phase5_integrated_scientific_information_inventory_v1"
DEFAULT_DIAGNOSTIC_SCHEMA_VERSION = "scientific_module_activation_diagnostic_schema_v1"
DEFAULT_LINEAGE_SCHEMA_VERSION = "scientific_module_activation_artifact_lineage_schema_v1"
DEFAULT_REPRODUCIBILITY_SCHEMA_VERSION = "scientific_module_activation_reproducibility_schema_v1"
DEFAULT_INTAKE_EVALUATION_ID = "synthetic_intake_eval_v1"
DEFAULT_PREPARED_OBSERVATION_PACKAGE_ID = "synthetic_prepared_observation_package_v1"
DEFAULT_HANDOFF_CONTRACT_ID = "synthetic_handoff_contract_v1"


class ModuleActivationState(str, Enum):
    MODULE_REGISTERED = "MODULE_REGISTERED"
    MODULE_ACTIVATION_READY = "MODULE_ACTIVATION_READY"
    MODULE_ACTIVATION_CONDITIONALLY_READY = "MODULE_ACTIVATION_CONDITIONALLY_READY"
    MODULE_ACTIVATION_UNRESOLVED = "MODULE_ACTIVATION_UNRESOLVED"
    MODULE_ACTIVATION_BLOCKED = "MODULE_ACTIVATION_BLOCKED"
    MODULE_ACTIVE = "MODULE_ACTIVE"
    MODULE_SUSPENDED = "MODULE_SUSPENDED"
    MODULE_DEACTIVATED = "MODULE_DEACTIVATED"
    MODULE_RETIRED = "MODULE_RETIRED"


class AdapterCompatibilityState(str, Enum):
    ADAPTER_COMPATIBLE = "ADAPTER_COMPATIBLE"
    ADAPTER_CONDITIONALLY_COMPATIBLE = "ADAPTER_CONDITIONALLY_COMPATIBLE"
    ADAPTER_UNRESOLVED = "ADAPTER_UNRESOLVED"
    ADAPTER_INCOMPATIBLE = "ADAPTER_INCOMPATIBLE"
    ADAPTER_EXCLUDED = "ADAPTER_EXCLUDED"
    INSUFFICIENT_ADAPTER_EVIDENCE = "INSUFFICIENT_ADAPTER_EVIDENCE"


class ExecutionAuthorizationState(str, Enum):
    EXECUTION_AUTHORIZED = "EXECUTION_AUTHORIZED"
    EXECUTION_CONDITIONALLY_AUTHORIZED = "EXECUTION_CONDITIONALLY_AUTHORIZED"
    EXECUTION_UNRESOLVED = "EXECUTION_UNRESOLVED"
    EXECUTION_BLOCKED = "EXECUTION_BLOCKED"
    EXECUTION_EXCLUDED = "EXECUTION_EXCLUDED"
    INSUFFICIENT_EXECUTION_AUTHORIZATION_EVIDENCE = "INSUFFICIENT_EXECUTION_AUTHORIZATION_EVIDENCE"


class DuplicateExecutionState(str, Enum):
    NO_DUPLICATE = "NO_DUPLICATE"
    EXACT_RERUN = "EXACT_RERUN"
    AUTHORIZED_RERUN = "AUTHORIZED_RERUN"
    ACCIDENTAL_DUPLICATE = "ACCIDENTAL_DUPLICATE"
    CONFLICTING_DUPLICATE = "CONFLICTING_DUPLICATE"
    SUPERSEDING_EXECUTION = "SUPERSEDING_EXECUTION"
    CORRECTED_RERUN = "CORRECTED_RERUN"
    SPECIFICATION_CHANGED_RERUN = "SPECIFICATION_CHANGED_RERUN"
    HORIZON_CHANGED_RERUN = "HORIZON_CHANGED_RERUN"


class RerunClassification(str, Enum):
    IDENTICAL_DETERMINISTIC_RERUN = "IDENTICAL_DETERMINISTIC_RERUN"
    ENVIRONMENT_ONLY_RERUN = "ENVIRONMENT_ONLY_RERUN"
    CODE_VERSION_RERUN = "CODE_VERSION_RERUN"
    ADAPTER_VERSION_RERUN = "ADAPTER_VERSION_RERUN"
    INPUT_CONTRACT_RERUN = "INPUT_CONTRACT_RERUN"
    OUTPUT_CONTRACT_RERUN = "OUTPUT_CONTRACT_RERUN"
    SCIENTIFIC_SPECIFICATION_RERUN = "SCIENTIFIC_SPECIFICATION_RERUN"
    HORIZON_VERSION_RERUN = "HORIZON_VERSION_RERUN"
    CORRECTED_UPSTREAM_DATA_RERUN = "CORRECTED_UPSTREAM_DATA_RERUN"
    DIAGNOSTIC_SCHEMA_RERUN = "DIAGNOSTIC_SCHEMA_RERUN"
    REPRODUCIBILITY_SCHEMA_RERUN = "REPRODUCIBILITY_SCHEMA_RERUN"


class ActivationDiagnosticCode(str, Enum):
    MODULE_REGISTRATION_MISSING = "MODULE_REGISTRATION_MISSING"
    RESEARCH_PROGRAM_ID_MISSING = "RESEARCH_PROGRAM_ID_MISSING"
    ACTIVATION_SPECIFICATION_MISSING = "ACTIVATION_SPECIFICATION_MISSING"
    RESEARCH_PROGRAM_ACTIVATION_SPECIFICATION_MISMATCH = "RESEARCH_PROGRAM_ACTIVATION_SPECIFICATION_MISMATCH"
    INTAKE_CONTRACT_MISSING = "INTAKE_CONTRACT_MISSING"
    ADAPTER_MISSING = "ADAPTER_MISSING"
    MODULE_INPUT_CONTRACT_MISSING = "MODULE_INPUT_CONTRACT_MISSING"
    MODULE_OUTPUT_CONTRACT_MISSING = "MODULE_OUTPUT_CONTRACT_MISSING"
    SCIENTIFIC_SPECIFICATION_MISSING = "SCIENTIFIC_SPECIFICATION_MISSING"
    FROZEN_HORIZON_SPECIFICATION_MISSING = "FROZEN_HORIZON_SPECIFICATION_MISSING"
    ACTIVATION_INVARIANT_INCOMPLETE = "ACTIVATION_INVARIANT_INCOMPLETE"
    ACTIVATION_VERSION_INCOMPATIBILITY = "ACTIVATION_VERSION_INCOMPATIBILITY"
    ADAPTER_VERSION_INCOMPATIBILITY = "ADAPTER_VERSION_INCOMPATIBILITY"
    INPUT_CONTRACT_VERSION_INCOMPATIBILITY = "INPUT_CONTRACT_VERSION_INCOMPATIBILITY"
    OUTPUT_CONTRACT_VERSION_INCOMPATIBILITY = "OUTPUT_CONTRACT_VERSION_INCOMPATIBILITY"
    SCIENTIFIC_SPECIFICATION_VERSION_INCOMPATIBILITY = "SCIENTIFIC_SPECIFICATION_VERSION_INCOMPATIBILITY"
    FROZEN_HORIZON_VERSION_INCOMPATIBILITY = "FROZEN_HORIZON_VERSION_INCOMPATIBILITY"
    ACTIVATION_LINEAGE_INCOMPLETE = "ACTIVATION_LINEAGE_INCOMPLETE"
    ACTIVATION_REPRODUCIBILITY_INCOMPLETE = "ACTIVATION_REPRODUCIBILITY_INCOMPLETE"
    SOURCE_AUTHORITY_EVIDENCE_ABSENT = "SOURCE_AUTHORITY_EVIDENCE_ABSENT"
    PIT_IDENTITY_CONTEXT_EVIDENCE_ABSENT = "PIT_IDENTITY_CONTEXT_EVIDENCE_ABSENT"
    COMPARATOR_EVIDENCE_ABSENT = "COMPARATOR_EVIDENCE_ABSENT"
    PREPARED_OBSERVATIONS_UNAVAILABLE = "PREPARED_OBSERVATIONS_UNAVAILABLE"
    INTAKE_PLATFORM_UNAVAILABLE = "INTAKE_PLATFORM_UNAVAILABLE"
    CONTAMINATION_CONTROL_UNRESOLVED = "CONTAMINATION_CONTROL_UNRESOLVED"
    NEGATIVE_EVIDENCE_POLICY_UNRESOLVED = "NEGATIVE_EVIDENCE_POLICY_UNRESOLVED"
    FALSIFICATION_POLICY_UNRESOLVED = "FALSIFICATION_POLICY_UNRESOLVED"
    MODULE_ALREADY_ACTIVE = "MODULE_ALREADY_ACTIVE"
    MODULE_SUSPENDED = "MODULE_SUSPENDED"
    MODULE_DEACTIVATED = "MODULE_DEACTIVATED"
    MODULE_RETIRED = "MODULE_RETIRED"
    ACTIVATION_EFFECTIVE_INTERVAL_INVALID = "ACTIVATION_EFFECTIVE_INTERVAL_INVALID"
    ACTIVATION_NOT_EXPLICITLY_AUTHORIZED = "ACTIVATION_NOT_EXPLICITLY_AUTHORIZED"


class ExecutionDiagnosticCode(str, Enum):
    MODULE_NOT_ACTIVE = "MODULE_NOT_ACTIVE"
    ACTIVATION_EXPIRED = "ACTIVATION_EXPIRED"
    ACTIVATION_SUPERSEDED = "ACTIVATION_SUPERSEDED"
    INTAKE_STATE_NOT_ACCEPTED = "INTAKE_STATE_NOT_ACCEPTED"
    HANDOFF_INCOMPLETE = "HANDOFF_INCOMPLETE"
    ADAPTER_INCOMPATIBLE = "ADAPTER_INCOMPATIBLE"
    SCIENTIFIC_TRANSFORMATION_IN_ADAPTER = "SCIENTIFIC_TRANSFORMATION_IN_ADAPTER"
    EXECUTION_INPUT_CONTRACT_MISSING = "EXECUTION_INPUT_CONTRACT_MISSING"
    EXECUTION_OUTPUT_CONTRACT_MISSING = "EXECUTION_OUTPUT_CONTRACT_MISSING"
    EXECUTION_SCIENTIFIC_SPECIFICATION_MISSING = "EXECUTION_SCIENTIFIC_SPECIFICATION_MISSING"
    EXECUTION_FROZEN_HORIZON_MISSING = "EXECUTION_FROZEN_HORIZON_MISSING"
    EXECUTION_VERSION_INCOMPATIBILITY = "EXECUTION_VERSION_INCOMPATIBILITY"
    EXECUTION_LINEAGE_INCOMPLETE = "EXECUTION_LINEAGE_INCOMPLETE"
    EXECUTION_REPRODUCIBILITY_INCOMPLETE = "EXECUTION_REPRODUCIBILITY_INCOMPLETE"
    BLOCKING_INHERITED_DIAGNOSTIC = "BLOCKING_INHERITED_DIAGNOSTIC"
    BLOCKING_INTAKE_DIAGNOSTIC = "BLOCKING_INTAKE_DIAGNOSTIC"
    DUPLICATE_EXECUTION = "DUPLICATE_EXECUTION"
    CONFLICTING_EXECUTION = "CONFLICTING_EXECUTION"
    DIRECT_UPSTREAM_BYPASS = "DIRECT_UPSTREAM_BYPASS"
    RAW_PREPARED_OBSERVATION_BYPASS = "RAW_PREPARED_OBSERVATION_BYPASS"
    INSUFFICIENT_EXECUTION_EVIDENCE = "INSUFFICIENT_EXECUTION_EVIDENCE"
    EXECUTION_NOT_EXPLICITLY_AUTHORIZED = "EXECUTION_NOT_EXPLICITLY_AUTHORIZED"


class RegistryDiagnosticCode(str, Enum):
    MISSING_REGISTRY_SNAPSHOT = "MISSING_REGISTRY_SNAPSHOT"
    DUPLICATE_REGISTRY_KEY = "DUPLICATE_REGISTRY_KEY"
    CONFLICTING_REGISTRY_VERSION = "CONFLICTING_REGISTRY_VERSION"
    MISSING_AUTHORITATIVE_RECORD = "MISSING_AUTHORITATIVE_RECORD"
    AMBIGUOUS_AUTHORITATIVE_RECORD = "AMBIGUOUS_AUTHORITATIVE_RECORD"
    SUPERSEDED_RECORD_SELECTED = "SUPERSEDED_RECORD_SELECTED"
    INACTIVE_RECORD_SELECTED = "INACTIVE_RECORD_SELECTED"


@dataclass(frozen=True)
class Diagnostic:
    code: str
    component: str
    message: str

    def to_dict(self) -> dict[str, str]:
        return {"code": self.code, "component": self.component, "message": self.message}


@dataclass(frozen=True)
class VersionCompatibility:
    module_version_compatible: bool = True
    module_specification_version_compatible: bool = True
    intake_contract_version_compatible: bool = True
    activation_declaration_version_compatible: bool = True
    adapter_version_compatible: bool = True
    input_contract_version_compatible: bool = True
    output_contract_version_compatible: bool = True
    scientific_specification_version_compatible: bool = True
    frozen_horizon_specification_version_compatible: bool = True
    information_role_schema_version_compatible: bool = True
    diagnostic_schema_version_compatible: bool = True
    artifact_lineage_schema_version_compatible: bool = True
    reproducibility_schema_version_compatible: bool = True

    def all_compatible(self) -> bool:
        return all(self.to_dict().values())

    def to_dict(self) -> dict[str, bool]:
        return {
            "activation_declaration_version_compatible": self.activation_declaration_version_compatible,
            "adapter_version_compatible": self.adapter_version_compatible,
            "artifact_lineage_schema_version_compatible": self.artifact_lineage_schema_version_compatible,
            "diagnostic_schema_version_compatible": self.diagnostic_schema_version_compatible,
            "frozen_horizon_specification_version_compatible": self.frozen_horizon_specification_version_compatible,
            "information_role_schema_version_compatible": self.information_role_schema_version_compatible,
            "input_contract_version_compatible": self.input_contract_version_compatible,
            "intake_contract_version_compatible": self.intake_contract_version_compatible,
            "module_specification_version_compatible": self.module_specification_version_compatible,
            "module_version_compatible": self.module_version_compatible,
            "output_contract_version_compatible": self.output_contract_version_compatible,
            "reproducibility_schema_version_compatible": self.reproducibility_schema_version_compatible,
            "scientific_specification_version_compatible": self.scientific_specification_version_compatible,
        }


@dataclass(frozen=True)
class ActivationPrerequisiteState:
    source_authority_evidence_ready: bool = True
    pit_identity_context_evidence_ready: bool = True
    comparator_evidence_ready: bool = True
    prepared_observations_ready: bool = True
    intake_platform_ready: bool = True
    adapter_ready: bool = True
    module_input_contract_ready: bool = True
    module_output_contract_ready: bool = True
    scientific_specification_frozen: bool = True
    frozen_horizon_specification_ready: bool = True
    negative_evidence_policy_ready: bool = True
    falsification_policy_ready: bool = True
    contamination_controls_ready: bool = True
    artifact_lineage_ready: bool = True
    reproducibility_ready: bool = True
    version_compatibility_ready: bool = True
    unresolved_readiness: bool = False
    conditional_readiness: bool = False

    def to_dict(self) -> dict[str, bool]:
        return {
            "adapter_ready": self.adapter_ready,
            "artifact_lineage_ready": self.artifact_lineage_ready,
            "comparator_evidence_ready": self.comparator_evidence_ready,
            "conditional_readiness": self.conditional_readiness,
            "contamination_controls_ready": self.contamination_controls_ready,
            "falsification_policy_ready": self.falsification_policy_ready,
            "frozen_horizon_specification_ready": self.frozen_horizon_specification_ready,
            "intake_platform_ready": self.intake_platform_ready,
            "module_input_contract_ready": self.module_input_contract_ready,
            "module_output_contract_ready": self.module_output_contract_ready,
            "negative_evidence_policy_ready": self.negative_evidence_policy_ready,
            "pit_identity_context_evidence_ready": self.pit_identity_context_evidence_ready,
            "prepared_observations_ready": self.prepared_observations_ready,
            "reproducibility_ready": self.reproducibility_ready,
            "scientific_specification_frozen": self.scientific_specification_frozen,
            "source_authority_evidence_ready": self.source_authority_evidence_ready,
            "unresolved_readiness": self.unresolved_readiness,
            "version_compatibility_ready": self.version_compatibility_ready,
        }


@dataclass(frozen=True)
class ArtifactLineage:
    source_authority_artifact: str = "synthetic_source_authority_artifact"
    pit_artifact: str = "synthetic_pit_identity_context_artifact"
    comparator_artifact: str = "synthetic_comparator_artifact"
    prepared_observation_artifact: str = "synthetic_prepared_observation_artifact"
    intake_contract_artifact: str = "synthetic_intake_contract_artifact"
    module_registration_artifact: str = "synthetic_module_registration_artifact"
    intake_evaluation_artifact: str = "synthetic_intake_evaluation_artifact"
    handoff_artifact: str = "synthetic_handoff_artifact"
    activation_declaration_artifact: str = "synthetic_activation_declaration_artifact"
    adapter_artifact: str = "synthetic_adapter_artifact"
    module_input_contract_artifact: str = "synthetic_module_input_contract_artifact"
    module_output_contract_artifact: str = "synthetic_module_output_contract_artifact"
    scientific_specification_artifact: str = "synthetic_scientific_specification_artifact"
    frozen_horizon_artifact: str = "synthetic_frozen_horizon_artifact"
    execution_authorization_artifact: str = "synthetic_execution_authorization_artifact"
    deterministic_execution_identity_artifact: str = "synthetic_execution_identity_artifact"
    scientific_execution_artifact: str = ""
    scientific_output_artifact: str = ""
    negative_evidence_artifacts_preserved: bool = True

    def complete(self) -> bool:
        required = (
            self.source_authority_artifact,
            self.pit_artifact,
            self.comparator_artifact,
            self.prepared_observation_artifact,
            self.intake_contract_artifact,
            self.module_registration_artifact,
            self.intake_evaluation_artifact,
            self.handoff_artifact,
            self.activation_declaration_artifact,
            self.adapter_artifact,
            self.module_input_contract_artifact,
            self.module_output_contract_artifact,
            self.scientific_specification_artifact,
            self.frozen_horizon_artifact,
        )
        return all(required) and self.scientific_execution_artifact == "" and self.scientific_output_artifact == ""

    def to_dict(self) -> dict[str, Any]:
        return _to_jsonable(self)


@dataclass(frozen=True)
class ReproducibilityMetadata:
    governing_design_version: str = FROZEN_DESIGN_ID
    implementation_version: str = MODULE_VERSION
    fixture_identifier: str = "synthetic_fixture"
    module_version: str = DEFAULT_MODULE_VERSION
    intake_contract_version: str = DEFAULT_INTAKE_CONTRACT_VERSION
    activation_declaration_version: str = "v1"
    adapter_version: str = DEFAULT_ADAPTER_VERSION
    input_contract_version: str = DEFAULT_INPUT_CONTRACT_VERSION
    output_contract_version: str = DEFAULT_OUTPUT_CONTRACT_VERSION
    scientific_specification_version: str = DEFAULT_SCIENTIFIC_SPECIFICATION_VERSION
    frozen_horizon_version: str = DEFAULT_FROZEN_HORIZON_SPECIFICATION_VERSION
    prepared_observation_version: str = "v1"
    information_role_schema_version: str = DEFAULT_INFORMATION_ROLE_SCHEMA_VERSION
    diagnostic_schema_version: str = DEFAULT_DIAGNOSTIC_SCHEMA_VERSION
    lineage_schema_version: str = DEFAULT_LINEAGE_SCHEMA_VERSION
    reproducibility_schema_version: str = DEFAULT_REPRODUCIBILITY_SCHEMA_VERSION
    stable_serialization_format_version: str = STABLE_SERIALIZATION_VERSION
    deterministic_serialization: bool = True
    controlled_reference: bool = True

    def complete(self) -> bool:
        values = self.to_dict()
        return all(values.values())

    def to_dict(self) -> dict[str, Any]:
        return _to_jsonable(self)


@dataclass(frozen=True)
class ScientificModuleRegistration:
    module_registration_id: str
    module_id: str
    module_version: str
    module_specification_version: str
    research_program_id: str
    research_program_version: str
    activation_specification_id: str
    activation_specification_version: str
    intake_contract_id: str
    intake_contract_version: str
    adapter_id: str
    adapter_version: str
    module_input_contract_id: str
    module_input_contract_version: str
    module_output_contract_id: str
    module_output_contract_version: str
    module_status: str = "REGISTERED"
    artifact_reference: str = "synthetic_module_registration_artifact"
    governing_versions: dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return _to_jsonable(self)


@dataclass(frozen=True)
class AdapterRegistration:
    adapter_id: str
    adapter_version: str
    module_id: str
    module_version: str
    intake_contract_id: str
    intake_contract_version: str
    input_contract_id: str
    input_contract_version: str
    mapping_specification_id: str
    mapping_specification_version: str
    adapter_status: AdapterCompatibilityState
    scientific_transformation_permitted: bool
    artifact_reference: str = "synthetic_adapter_artifact"
    governing_versions: dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return _to_jsonable(self)


@dataclass(frozen=True)
class ActivationDeclaration:
    activation_declaration_id: str
    activation_declaration_version: str
    module_registration_id: str
    module_id: str
    module_version: str
    module_specification_version: str
    research_program_id: str
    research_program_version: str
    activation_specification_id: str
    activation_specification_version: str
    intake_contract_id: str
    intake_contract_version: str
    adapter_id: str
    adapter_version: str
    module_input_contract_id: str
    module_input_contract_version: str
    module_output_contract_id: str
    module_output_contract_version: str
    scientific_specification_id: str
    scientific_specification_version: str
    frozen_horizon_specification_id: str
    frozen_horizon_specification_version: str
    accepted_intake_states: tuple[str, ...]
    conditional_intake_policy: str
    execution_policy: str
    duplicate_execution_policy: str
    rerun_policy: str
    supersession_policy: str
    failure_policy: str
    negative_evidence_policy: str
    falsification_policy: str
    contamination_control_policy: str
    artifact_lineage_requirements: tuple[str, ...]
    reproducibility_requirements: tuple[str, ...]
    activation_effective_start: int | None
    activation_effective_end: int | None
    requested_activation_state: ModuleActivationState
    governing_design_versions: tuple[str, ...]
    explicit_activation_authorized: bool = False
    prohibited_activation: bool = False
    superseded: bool = False

    def effective_interval_valid(self) -> bool:
        if self.activation_effective_start is None or self.activation_effective_end is None:
            return False
        return self.activation_effective_start <= self.activation_effective_end

    def to_dict(self) -> dict[str, Any]:
        return _to_jsonable(self)


@dataclass(frozen=True)
class ExecutionAuthorizationRequest:
    execution_authorization_request_id: str
    activation_id: str
    module_id: str
    module_version: str
    module_specification_version: str
    activation_specification_id: str
    activation_specification_version: str
    intake_evaluation_id: str
    prepared_observation_package_id: str
    handoff_contract_id: str
    adapter_id: str
    adapter_version: str
    module_input_contract_id: str
    module_input_contract_version: str
    module_output_contract_id: str
    module_output_contract_version: str
    scientific_specification_id: str
    scientific_specification_version: str
    frozen_horizon_specification_id: str
    frozen_horizon_specification_version: str
    requested_execution_interval: tuple[int | None, int | None]
    requesting_execution_identity: str
    duplicate_policy: str
    rerun_reason: RerunClassification | str
    governing_versions: dict[str, str]
    explicit_execution_authorized: bool = False
    intake_state: str = "INTAKE_COMPATIBLE"
    handoff_complete: bool = True
    lineage_complete: bool = True
    reproducibility_complete: bool = True
    blocking_inherited_diagnostic: bool = False
    blocking_intake_diagnostic: bool = False
    direct_upstream_bypass: bool = False
    raw_prepared_observation_bypass: bool = False
    unresolved_authorization: bool = False
    insufficient_authorization_evidence: bool = False
    conditional_authorization: bool = False

    def to_dict(self) -> dict[str, Any]:
        return _to_jsonable(self)


@dataclass(frozen=True)
class LifecycleRecord:
    record_id: str
    module_registration_id: str
    reason: str
    artifact_reference: str
    preserves_historical_artifacts: bool = True
    preserves_negative_evidence: bool = True

    def to_dict(self) -> dict[str, Any]:
        return _to_jsonable(self)


@dataclass(frozen=True)
class SupersessionRecord:
    record_id: str
    superseded_id: str
    superseding_id: str
    reason: str
    preserves_negative_evidence: bool = True

    def to_dict(self) -> dict[str, Any]:
        return _to_jsonable(self)


@dataclass(frozen=True)
class RegistrySnapshot:
    registry_snapshot_id: str
    module_registrations: tuple[ScientificModuleRegistration, ...] = ()
    activation_declarations: tuple[ActivationDeclaration, ...] = ()
    adapters: tuple[AdapterRegistration, ...] = ()
    intake_contracts: tuple[str, ...] = (DEFAULT_INTAKE_CONTRACT_ID,)
    module_input_contracts: tuple[str, ...] = (DEFAULT_INPUT_CONTRACT_ID,)
    module_output_contracts: tuple[str, ...] = (DEFAULT_OUTPUT_CONTRACT_ID,)
    scientific_specifications: tuple[str, ...] = (DEFAULT_SCIENTIFIC_SPECIFICATION_ID,)
    frozen_horizon_specifications: tuple[str, ...] = (DEFAULT_FROZEN_HORIZON_SPECIFICATION_ID,)
    execution_authorizations: tuple[str, ...] = ()
    execution_identities: tuple[str, ...] = ()
    suspension_records: tuple[LifecycleRecord, ...] = ()
    deactivation_records: tuple[LifecycleRecord, ...] = ()
    retirement_records: tuple[LifecycleRecord, ...] = ()
    supersession_records: tuple[SupersessionRecord, ...] = ()
    inactive_records: tuple[str, ...] = ()

    def stable_json(self) -> str:
        return _stable_json(self.to_dict())

    def to_dict(self) -> dict[str, Any]:
        return _to_jsonable(self)


@dataclass(frozen=True)
class DuplicateExecutionMetadata:
    duplicate_state: DuplicateExecutionState = DuplicateExecutionState.NO_DUPLICATE
    prior_execution_identity: str = ""
    rerun_classification: RerunClassification | str = ""
    supersedes_execution_identity: str = ""

    def to_dict(self) -> dict[str, Any]:
        return _to_jsonable(self)


@dataclass(frozen=True)
class ActivationEvaluation:
    activation_evaluation_id: str
    module_registration: ScientificModuleRegistration | None
    activation_declaration: ActivationDeclaration
    activation_state: ModuleActivationState
    activation_diagnostics: tuple[Diagnostic, ...]
    activation_limitations: tuple[str, ...]
    prerequisite_states: ActivationPrerequisiteState
    adapter_metadata: AdapterRegistration | None
    adapter_compatibility_state: AdapterCompatibilityState
    version_compatibility: VersionCompatibility
    lineage_metadata: ArtifactLineage
    reproducibility_metadata: ReproducibilityMetadata
    registry_references: dict[str, str]
    registry_diagnostics: tuple[Diagnostic, ...]
    governing_versions: dict[str, str]
    exposes_scientific_measurements: bool = False
    exposes_formulas: bool = False
    exposes_signals: bool = False
    exposes_factors: bool = False
    exposes_candidates: bool = False
    exposes_panels: bool = False
    computes_ic: bool = False
    computes_sharpe: bool = False
    exposes_predictions: bool = False
    exposes_validation_results: bool = False
    makes_portfolio_decisions: bool = False
    makes_production_decisions: bool = False
    exposes_ml_features: bool = False
    exposes_ml_labels: bool = False
    trains_models: bool = False

    def stable_json(self) -> str:
        return _stable_json(self.to_dict())

    def to_dict(self) -> dict[str, Any]:
        return _to_jsonable(self)


@dataclass(frozen=True)
class ExecutionAuthorization:
    execution_authorization_id: str
    execution_authorization_state: ExecutionAuthorizationState
    deterministic_execution_identity: str
    authorization_diagnostics: tuple[Diagnostic, ...]
    authorization_limitations: tuple[str, ...]
    activation_reference: str
    intake_reference: str
    handoff_reference: str
    adapter_reference: str
    input_contract_reference: str
    output_contract_reference: str
    scientific_specification_reference: str
    frozen_horizon_reference: str
    duplicate_rerun_metadata: DuplicateExecutionMetadata
    lineage_metadata: ArtifactLineage
    reproducibility_metadata: ReproducibilityMetadata
    governing_versions: dict[str, str]
    exposes_scientific_execution_artifact: bool = False
    exposes_scientific_output: bool = False
    exposes_scientific_measurements: bool = False
    exposes_formulas: bool = False
    exposes_signals: bool = False
    exposes_factors: bool = False
    exposes_candidates: bool = False
    exposes_panels: bool = False
    computes_ic: bool = False
    computes_sharpe: bool = False
    exposes_predictions: bool = False
    exposes_validation_results: bool = False
    makes_portfolio_decisions: bool = False
    makes_production_decisions: bool = False
    exposes_ml_features: bool = False
    exposes_ml_labels: bool = False
    trains_models: bool = False

    def stable_json(self) -> str:
        return _stable_json(self.to_dict())

    def to_dict(self) -> dict[str, Any]:
        return _to_jsonable(self)


@dataclass(frozen=True)
class CanonicalActivationFixture:
    fixture_id: str
    registry_snapshot: RegistrySnapshot
    activation_declaration: ActivationDeclaration
    prerequisites: ActivationPrerequisiteState
    version_compatibility: VersionCompatibility
    lineage: ArtifactLineage
    reproducibility: ReproducibilityMetadata
    expected_activation_state: ModuleActivationState
    expected_activation_diagnostics: tuple[ActivationDiagnosticCode, ...] = ()
    execution_request: ExecutionAuthorizationRequest | None = None
    duplicate_metadata: DuplicateExecutionMetadata = field(default_factory=DuplicateExecutionMetadata)
    expected_execution_state: ExecutionAuthorizationState | None = None
    expected_execution_diagnostics: tuple[ExecutionDiagnosticCode, ...] = ()


def _to_jsonable(value: Any) -> Any:
    if isinstance(value, Enum):
        return value.value
    if is_dataclass(value):
        return {key: _to_jsonable(val) for key, val in sorted(value.__dict__.items())}
    if isinstance(value, dict):
        return {str(key): _to_jsonable(value[key]) for key in sorted(value)}
    if isinstance(value, tuple):
        return [_to_jsonable(item) for item in value]
    if isinstance(value, list):
        return [_to_jsonable(item) for item in value]
    return value


def _stable_json(payload: Any) -> str:
    return json.dumps(_to_jsonable(payload), sort_keys=True, separators=(",", ":"))


def _stable_hash(payload: Any) -> str:
    return hashlib.sha256(_stable_json(payload).encode("utf-8")).hexdigest()[:24]


def _is_blank(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, str):
        return value.strip() == ""
    if isinstance(value, tuple):
        return len(value) == 0 or any(_is_blank(item) for item in value)
    if isinstance(value, dict):
        return len(value) == 0 or any(_is_blank(key) or _is_blank(val) for key, val in value.items())
    return False


def _diag(code: Enum, component: str, message: str) -> Diagnostic:
    return Diagnostic(code.value, component, message)


def _dedupe_diagnostics(diagnostics: list[Diagnostic]) -> tuple[Diagnostic, ...]:
    seen: set[tuple[str, str, str]] = set()
    result: list[Diagnostic] = []
    for diagnostic in diagnostics:
        key = (diagnostic.code, diagnostic.component, diagnostic.message)
        if key not in seen:
            seen.add(key)
            result.append(diagnostic)
    return tuple(result)


def _limitations(*items: str) -> tuple[str, ...]:
    return tuple(sorted(item for item in items if item))


def _base_governing_versions() -> dict[str, str]:
    return {
        "activation_design": FROZEN_DESIGN_ID,
        "artifact_lineage_schema": DEFAULT_LINEAGE_SCHEMA_VERSION,
        "diagnostic_schema": DEFAULT_DIAGNOSTIC_SCHEMA_VERSION,
        "information_role_schema": DEFAULT_INFORMATION_ROLE_SCHEMA_VERSION,
        "implementation": MODULE_VERSION,
        "module": DEFAULT_MODULE_VERSION,
        "reproducibility_schema": DEFAULT_REPRODUCIBILITY_SCHEMA_VERSION,
        "stable_serialization": STABLE_SERIALIZATION_VERSION,
    }


def selected_module_registration(**overrides: Any) -> ScientificModuleRegistration:
    values = {
        "module_registration_id": "registration_selected_first_phase5_module_v1",
        "module_id": DEFAULT_MODULE_ID,
        "module_version": DEFAULT_MODULE_VERSION,
        "module_specification_version": DEFAULT_MODULE_SPECIFICATION_VERSION,
        "research_program_id": SELECTED_RESEARCH_PROGRAM_ID,
        "research_program_version": SELECTED_RESEARCH_PROGRAM_VERSION,
        "activation_specification_id": NARROW_ACTIVATION_SPECIFICATION_ID,
        "activation_specification_version": NARROW_ACTIVATION_SPECIFICATION_VERSION,
        "intake_contract_id": DEFAULT_INTAKE_CONTRACT_ID,
        "intake_contract_version": DEFAULT_INTAKE_CONTRACT_VERSION,
        "adapter_id": DEFAULT_ADAPTER_ID,
        "adapter_version": DEFAULT_ADAPTER_VERSION,
        "module_input_contract_id": DEFAULT_INPUT_CONTRACT_ID,
        "module_input_contract_version": DEFAULT_INPUT_CONTRACT_VERSION,
        "module_output_contract_id": DEFAULT_OUTPUT_CONTRACT_ID,
        "module_output_contract_version": DEFAULT_OUTPUT_CONTRACT_VERSION,
        "governing_versions": _base_governing_versions(),
    }
    values.update(overrides)
    return ScientificModuleRegistration(**values)


def selected_adapter_registration(**overrides: Any) -> AdapterRegistration:
    values = {
        "adapter_id": DEFAULT_ADAPTER_ID,
        "adapter_version": DEFAULT_ADAPTER_VERSION,
        "module_id": DEFAULT_MODULE_ID,
        "module_version": DEFAULT_MODULE_VERSION,
        "intake_contract_id": DEFAULT_INTAKE_CONTRACT_ID,
        "intake_contract_version": DEFAULT_INTAKE_CONTRACT_VERSION,
        "input_contract_id": DEFAULT_INPUT_CONTRACT_ID,
        "input_contract_version": DEFAULT_INPUT_CONTRACT_VERSION,
        "mapping_specification_id": "synthetic_activation_to_module_input_mapping_v1",
        "mapping_specification_version": "v1",
        "adapter_status": AdapterCompatibilityState.ADAPTER_COMPATIBLE,
        "scientific_transformation_permitted": False,
        "governing_versions": _base_governing_versions(),
    }
    values.update(overrides)
    return AdapterRegistration(**values)


def selected_activation_declaration(**overrides: Any) -> ActivationDeclaration:
    values = {
        "activation_declaration_id": "activation_declaration_selected_first_phase5_module_v1",
        "activation_declaration_version": "v1",
        "module_registration_id": "registration_selected_first_phase5_module_v1",
        "module_id": DEFAULT_MODULE_ID,
        "module_version": DEFAULT_MODULE_VERSION,
        "module_specification_version": DEFAULT_MODULE_SPECIFICATION_VERSION,
        "research_program_id": SELECTED_RESEARCH_PROGRAM_ID,
        "research_program_version": SELECTED_RESEARCH_PROGRAM_VERSION,
        "activation_specification_id": NARROW_ACTIVATION_SPECIFICATION_ID,
        "activation_specification_version": NARROW_ACTIVATION_SPECIFICATION_VERSION,
        "intake_contract_id": DEFAULT_INTAKE_CONTRACT_ID,
        "intake_contract_version": DEFAULT_INTAKE_CONTRACT_VERSION,
        "adapter_id": DEFAULT_ADAPTER_ID,
        "adapter_version": DEFAULT_ADAPTER_VERSION,
        "module_input_contract_id": DEFAULT_INPUT_CONTRACT_ID,
        "module_input_contract_version": DEFAULT_INPUT_CONTRACT_VERSION,
        "module_output_contract_id": DEFAULT_OUTPUT_CONTRACT_ID,
        "module_output_contract_version": DEFAULT_OUTPUT_CONTRACT_VERSION,
        "scientific_specification_id": DEFAULT_SCIENTIFIC_SPECIFICATION_ID,
        "scientific_specification_version": DEFAULT_SCIENTIFIC_SPECIFICATION_VERSION,
        "frozen_horizon_specification_id": DEFAULT_FROZEN_HORIZON_SPECIFICATION_ID,
        "frozen_horizon_specification_version": DEFAULT_FROZEN_HORIZON_SPECIFICATION_VERSION,
        "accepted_intake_states": ("INTAKE_COMPATIBLE", "INTAKE_CONDITIONALLY_COMPATIBLE"),
        "conditional_intake_policy": "carry_limitations",
        "execution_policy": "explicit_authorization_required",
        "duplicate_execution_policy": "no_silent_overwrite",
        "rerun_policy": "metadata_only_governed_reruns",
        "supersession_policy": "append_only_supersession",
        "failure_policy": "fail_closed",
        "negative_evidence_policy": "negative_evidence_preserved_v1",
        "falsification_policy": "falsification_policy_bound_v1",
        "contamination_control_policy": "contamination_controls_bound_v1",
        "artifact_lineage_requirements": (
            "activation_declaration_artifact",
            "module_registration_artifact",
            "intake_evaluation_artifact",
            "handoff_artifact",
        ),
        "reproducibility_requirements": (
            "deterministic_serialization",
            "controlled_reference",
            "stable_versions",
        ),
        "activation_effective_start": 1,
        "activation_effective_end": 10,
        "requested_activation_state": ModuleActivationState.MODULE_ACTIVATION_READY,
        "governing_design_versions": (FROZEN_DESIGN_ID,),
    }
    values.update(overrides)
    return ActivationDeclaration(**values)


_DEFAULT = object()


def registry_snapshot(
    registration: ScientificModuleRegistration | None | object = _DEFAULT,
    declaration: ActivationDeclaration | None | object = _DEFAULT,
    adapter: AdapterRegistration | None | object = _DEFAULT,
    **overrides: Any,
) -> RegistrySnapshot:
    registration = selected_module_registration() if registration is _DEFAULT else registration
    declaration = selected_activation_declaration() if declaration is _DEFAULT else declaration
    adapter = selected_adapter_registration() if adapter is _DEFAULT else adapter
    values = {
        "registry_snapshot_id": "synthetic_activation_registry_snapshot_v1",
        "module_registrations": (registration,) if registration else (),
        "activation_declarations": (declaration,) if declaration else (),
        "adapters": (adapter,) if adapter else (),
    }
    values.update(overrides)
    return RegistrySnapshot(**values)


def selected_real_module_prerequisites() -> ActivationPrerequisiteState:
    return ActivationPrerequisiteState(
        source_authority_evidence_ready=False,
        pit_identity_context_evidence_ready=False,
        comparator_evidence_ready=False,
        prepared_observations_ready=False,
    )


def _selected_real_prerequisites() -> ActivationPrerequisiteState:
    return ActivationPrerequisiteState(
        source_authority_evidence_ready=False,
        pit_identity_context_evidence_ready=False,
        comparator_evidence_ready=False,
        prepared_observations_ready=False,
    )


def _lookup_unique(records: tuple[Any, ...], key_name: str, key_value: str, component: str) -> tuple[Any | None, tuple[Diagnostic, ...]]:
    diagnostics: list[Diagnostic] = []
    if not key_value:
        return None, tuple()
    matches = tuple(record for record in records if getattr(record, key_name) == key_value)
    if not matches:
        diagnostics.append(_diag(RegistryDiagnosticCode.MISSING_AUTHORITATIVE_RECORD, component, f"Missing record for {key_name}={key_value}"))
        return None, tuple(diagnostics)
    versions = {getattr(record, "module_version", getattr(record, "adapter_version", "")) for record in matches}
    if len(matches) > 1 and len(versions) > 1:
        diagnostics.append(_diag(RegistryDiagnosticCode.CONFLICTING_REGISTRY_VERSION, component, f"Conflicting versions for {key_name}={key_value}"))
    elif len(matches) > 1:
        diagnostics.append(_diag(RegistryDiagnosticCode.DUPLICATE_REGISTRY_KEY, component, f"Duplicate records for {key_name}={key_value}"))
        diagnostics.append(_diag(RegistryDiagnosticCode.AMBIGUOUS_AUTHORITATIVE_RECORD, component, f"Ambiguous authoritative record for {key_name}={key_value}"))
    return matches[0], tuple(diagnostics)


def _registry_diagnostics(snapshot: RegistrySnapshot | None) -> tuple[Diagnostic, ...]:
    if snapshot is None:
        return (_diag(RegistryDiagnosticCode.MISSING_REGISTRY_SNAPSHOT, "registry", "Missing registry snapshot"),)
    diagnostics: list[Diagnostic] = []
    for records, key_name, component in (
        (snapshot.module_registrations, "module_registration_id", "module_registry"),
        (snapshot.activation_declarations, "activation_declaration_id", "activation_registry"),
        (snapshot.adapters, "adapter_id", "adapter_registry"),
    ):
        seen: dict[str, str] = {}
        for record in records:
            key = getattr(record, key_name)
            version = getattr(record, "module_version", getattr(record, "activation_declaration_version", getattr(record, "adapter_version", "")))
            if key in seen and seen[key] == version:
                diagnostics.append(_diag(RegistryDiagnosticCode.DUPLICATE_REGISTRY_KEY, component, f"Duplicate registry key {key}"))
            elif key in seen:
                diagnostics.append(_diag(RegistryDiagnosticCode.CONFLICTING_REGISTRY_VERSION, component, f"Conflicting registry version for {key}"))
            seen[key] = version
    for record_id in snapshot.inactive_records:
        diagnostics.append(_diag(RegistryDiagnosticCode.INACTIVE_RECORD_SELECTED, "registry", f"Inactive record selected: {record_id}"))
    for record in snapshot.supersession_records:
        diagnostics.append(_diag(RegistryDiagnosticCode.SUPERSEDED_RECORD_SELECTED, "registry", f"Superseded record selected: {record.superseded_id}"))
    return _dedupe_diagnostics(diagnostics)


def _has_fatal_registry_diagnostic(diagnostics: tuple[Diagnostic, ...] | list[Diagnostic]) -> bool:
    fatal_codes = {
        RegistryDiagnosticCode.MISSING_REGISTRY_SNAPSHOT.value,
        RegistryDiagnosticCode.DUPLICATE_REGISTRY_KEY.value,
        RegistryDiagnosticCode.CONFLICTING_REGISTRY_VERSION.value,
        RegistryDiagnosticCode.MISSING_AUTHORITATIVE_RECORD.value,
        RegistryDiagnosticCode.AMBIGUOUS_AUTHORITATIVE_RECORD.value,
        RegistryDiagnosticCode.SUPERSEDED_RECORD_SELECTED.value,
        RegistryDiagnosticCode.INACTIVE_RECORD_SELECTED.value,
    }
    return any(diagnostic.code in fatal_codes for diagnostic in diagnostics)


def _authoritative_handoff_chain(lineage: ArtifactLineage) -> dict[str, str]:
    intake_evaluation_id = (
        DEFAULT_INTAKE_EVALUATION_ID
        if lineage.intake_evaluation_artifact == "synthetic_intake_evaluation_artifact"
        else lineage.intake_evaluation_artifact
    )
    prepared_observation_package_id = (
        DEFAULT_PREPARED_OBSERVATION_PACKAGE_ID
        if lineage.prepared_observation_artifact == "synthetic_prepared_observation_artifact"
        else lineage.prepared_observation_artifact
    )
    handoff_contract_id = (
        DEFAULT_HANDOFF_CONTRACT_ID
        if lineage.handoff_artifact == "synthetic_handoff_artifact"
        else lineage.handoff_artifact
    )
    return {
        "intake_evaluation_id": intake_evaluation_id,
        "prepared_observation_package_id": prepared_observation_package_id,
        "handoff_contract_id": handoff_contract_id,
    }


def evaluate_activation_readiness(
    activation_declaration: ActivationDeclaration,
    registry: RegistrySnapshot | None,
    prerequisites: ActivationPrerequisiteState | None = None,
    version_compatibility: VersionCompatibility | None = None,
    lineage: ArtifactLineage | None = None,
    reproducibility: ReproducibilityMetadata | None = None,
) -> ActivationEvaluation:
    prerequisites = prerequisites or ActivationPrerequisiteState()
    version_compatibility = version_compatibility or VersionCompatibility()
    lineage = lineage or ArtifactLineage()
    reproducibility = reproducibility or ReproducibilityMetadata(fixture_identifier=activation_declaration.activation_declaration_id)

    registry_diags = list(_registry_diagnostics(registry))
    diagnostics: list[Diagnostic] = []
    limitations = [
        "REFERENCE_IMPLEMENTATION_ONLY",
        "SYNTHETIC_REGISTRY_ONLY",
        "SYNTHETIC_PREREQUISITE_STATE",
    ]
    activation_binding_failure = False

    registration: ScientificModuleRegistration | None = None
    adapter: AdapterRegistration | None = None

    if registry is None:
        diagnostics.append(_diag(ActivationDiagnosticCode.MODULE_REGISTRATION_MISSING, "activation", "Registry snapshot is missing"))
    else:
        registration, reg_diags = _lookup_unique(
            registry.module_registrations,
            "module_registration_id",
            activation_declaration.module_registration_id,
            "module_registry",
        )
        registry_diags.extend(reg_diags)
        adapter, adapter_diags = _lookup_unique(
            registry.adapters,
            "adapter_id",
            activation_declaration.adapter_id,
            "adapter_registry",
        )
        registry_diags.extend(adapter_diags)

    if registration is None:
        diagnostics.append(_diag(ActivationDiagnosticCode.MODULE_REGISTRATION_MISSING, "activation", "Module registration is missing"))
    if not activation_declaration.research_program_id:
        diagnostics.append(_diag(ActivationDiagnosticCode.RESEARCH_PROGRAM_ID_MISSING, "activation", "Research-program identity is missing"))
    if not activation_declaration.activation_specification_id:
        diagnostics.append(_diag(ActivationDiagnosticCode.ACTIVATION_SPECIFICATION_MISSING, "activation", "Activation specification is missing"))
    if activation_declaration.activation_specification_id == activation_declaration.research_program_id:
        diagnostics.append(_diag(ActivationDiagnosticCode.RESEARCH_PROGRAM_ACTIVATION_SPECIFICATION_MISMATCH, "activation", "Broad program label cannot substitute for narrow activation specification"))
    if registration and (
        registration.research_program_id != activation_declaration.research_program_id
        or registration.activation_specification_id != activation_declaration.activation_specification_id
    ):
        diagnostics.append(_diag(ActivationDiagnosticCode.RESEARCH_PROGRAM_ACTIVATION_SPECIFICATION_MISMATCH, "activation", "Registration and declaration identity binding mismatch"))
    if registration and (
        registration.module_id != activation_declaration.module_id
        or registration.module_version != activation_declaration.module_version
        or registration.module_specification_version != activation_declaration.module_specification_version
        or registration.intake_contract_id != activation_declaration.intake_contract_id
        or registration.adapter_id != activation_declaration.adapter_id
        or registration.module_input_contract_id != activation_declaration.module_input_contract_id
        or registration.module_output_contract_id != activation_declaration.module_output_contract_id
    ):
        diagnostics.append(_diag(ActivationDiagnosticCode.ACTIVATION_VERSION_INCOMPATIBILITY, "activation", "Registration and declaration contract binding mismatch"))

    missing_fields = (
        (activation_declaration.activation_declaration_id, ActivationDiagnosticCode.ACTIVATION_INVARIANT_INCOMPLETE, "activation declaration id"),
        (activation_declaration.activation_declaration_version, ActivationDiagnosticCode.ACTIVATION_VERSION_INCOMPATIBILITY, "activation declaration version"),
        (activation_declaration.module_registration_id, ActivationDiagnosticCode.MODULE_REGISTRATION_MISSING, "module registration id"),
        (activation_declaration.module_id, ActivationDiagnosticCode.ACTIVATION_INVARIANT_INCOMPLETE, "module id"),
        (activation_declaration.module_version, ActivationDiagnosticCode.ACTIVATION_VERSION_INCOMPATIBILITY, "module version"),
        (activation_declaration.module_specification_version, ActivationDiagnosticCode.ACTIVATION_VERSION_INCOMPATIBILITY, "module specification version"),
        (activation_declaration.research_program_id, ActivationDiagnosticCode.RESEARCH_PROGRAM_ID_MISSING, "research program id"),
        (activation_declaration.research_program_version, ActivationDiagnosticCode.ACTIVATION_VERSION_INCOMPATIBILITY, "research program version"),
        (activation_declaration.activation_specification_id, ActivationDiagnosticCode.ACTIVATION_SPECIFICATION_MISSING, "activation specification id"),
        (activation_declaration.activation_specification_version, ActivationDiagnosticCode.ACTIVATION_VERSION_INCOMPATIBILITY, "activation specification version"),
        (activation_declaration.intake_contract_id, ActivationDiagnosticCode.INTAKE_CONTRACT_MISSING, "intake contract"),
        (activation_declaration.intake_contract_version, ActivationDiagnosticCode.ACTIVATION_VERSION_INCOMPATIBILITY, "intake contract version"),
        (activation_declaration.adapter_id, ActivationDiagnosticCode.ADAPTER_MISSING, "adapter"),
        (activation_declaration.adapter_version, ActivationDiagnosticCode.ADAPTER_VERSION_INCOMPATIBILITY, "adapter version"),
        (activation_declaration.module_input_contract_id, ActivationDiagnosticCode.MODULE_INPUT_CONTRACT_MISSING, "module input contract"),
        (activation_declaration.module_input_contract_version, ActivationDiagnosticCode.INPUT_CONTRACT_VERSION_INCOMPATIBILITY, "module input contract version"),
        (activation_declaration.module_output_contract_id, ActivationDiagnosticCode.MODULE_OUTPUT_CONTRACT_MISSING, "module output contract"),
        (activation_declaration.module_output_contract_version, ActivationDiagnosticCode.OUTPUT_CONTRACT_VERSION_INCOMPATIBILITY, "module output contract version"),
        (activation_declaration.scientific_specification_id, ActivationDiagnosticCode.SCIENTIFIC_SPECIFICATION_MISSING, "scientific specification"),
        (activation_declaration.scientific_specification_version, ActivationDiagnosticCode.SCIENTIFIC_SPECIFICATION_VERSION_INCOMPATIBILITY, "scientific specification version"),
        (activation_declaration.frozen_horizon_specification_id, ActivationDiagnosticCode.FROZEN_HORIZON_SPECIFICATION_MISSING, "frozen horizon specification"),
        (activation_declaration.frozen_horizon_specification_version, ActivationDiagnosticCode.FROZEN_HORIZON_VERSION_INCOMPATIBILITY, "frozen horizon specification version"),
        (activation_declaration.requested_activation_state, ActivationDiagnosticCode.ACTIVATION_INVARIANT_INCOMPLETE, "requested activation state"),
        (activation_declaration.governing_design_versions, ActivationDiagnosticCode.ACTIVATION_INVARIANT_INCOMPLETE, "governing design versions"),
        (activation_declaration.artifact_lineage_requirements, ActivationDiagnosticCode.ACTIVATION_LINEAGE_INCOMPLETE, "artifact lineage requirements"),
        (activation_declaration.reproducibility_requirements, ActivationDiagnosticCode.ACTIVATION_REPRODUCIBILITY_INCOMPLETE, "reproducibility requirements"),
    )
    for value, code, label in missing_fields:
        if _is_blank(value):
            diagnostics.append(_diag(code, "activation", f"Missing {label}"))
            activation_binding_failure = True

    policy_fields = (
        (activation_declaration.negative_evidence_policy, ActivationDiagnosticCode.NEGATIVE_EVIDENCE_POLICY_UNRESOLVED, "negative-evidence policy"),
        (activation_declaration.falsification_policy, ActivationDiagnosticCode.FALSIFICATION_POLICY_UNRESOLVED, "falsification policy"),
        (activation_declaration.contamination_control_policy, ActivationDiagnosticCode.CONTAMINATION_CONTROL_UNRESOLVED, "contamination-control policy"),
    )
    for value, code, label in policy_fields:
        if _is_blank(value):
            diagnostics.append(_diag(code, "activation", f"Missing {label} binding"))
            activation_binding_failure = True

    if adapter is None or not prerequisites.adapter_ready:
        diagnostics.append(_diag(ActivationDiagnosticCode.ADAPTER_MISSING, "activation", "Adapter evidence is missing"))
    if not prerequisites.module_input_contract_ready:
        diagnostics.append(_diag(ActivationDiagnosticCode.MODULE_INPUT_CONTRACT_MISSING, "activation", "Module input contract is not ready"))
    if not prerequisites.module_output_contract_ready:
        diagnostics.append(_diag(ActivationDiagnosticCode.MODULE_OUTPUT_CONTRACT_MISSING, "activation", "Module output contract is not ready"))
    if not prerequisites.scientific_specification_frozen:
        diagnostics.append(_diag(ActivationDiagnosticCode.SCIENTIFIC_SPECIFICATION_MISSING, "activation", "Scientific specification is not frozen"))
    if not prerequisites.frozen_horizon_specification_ready:
        diagnostics.append(_diag(ActivationDiagnosticCode.FROZEN_HORIZON_SPECIFICATION_MISSING, "activation", "Frozen horizon specification is not ready"))

    if not activation_declaration.effective_interval_valid():
        diagnostics.append(_diag(ActivationDiagnosticCode.ACTIVATION_EFFECTIVE_INTERVAL_INVALID, "activation", "Activation effective interval is invalid"))
    if not version_compatibility.all_compatible() or not prerequisites.version_compatibility_ready:
        diagnostics.append(_diag(ActivationDiagnosticCode.ACTIVATION_VERSION_INCOMPATIBILITY, "activation", "Activation version compatibility is incomplete"))
        if not version_compatibility.adapter_version_compatible:
            diagnostics.append(_diag(ActivationDiagnosticCode.ADAPTER_VERSION_INCOMPATIBILITY, "activation", "Adapter version is incompatible"))
        if not version_compatibility.input_contract_version_compatible:
            diagnostics.append(_diag(ActivationDiagnosticCode.INPUT_CONTRACT_VERSION_INCOMPATIBILITY, "activation", "Input contract version is incompatible"))
        if not version_compatibility.output_contract_version_compatible:
            diagnostics.append(_diag(ActivationDiagnosticCode.OUTPUT_CONTRACT_VERSION_INCOMPATIBILITY, "activation", "Output contract version is incompatible"))
        if not version_compatibility.scientific_specification_version_compatible:
            diagnostics.append(_diag(ActivationDiagnosticCode.SCIENTIFIC_SPECIFICATION_VERSION_INCOMPATIBILITY, "activation", "Scientific specification version is incompatible"))
        if not version_compatibility.frozen_horizon_specification_version_compatible:
            diagnostics.append(_diag(ActivationDiagnosticCode.FROZEN_HORIZON_VERSION_INCOMPATIBILITY, "activation", "Frozen horizon version is incompatible"))

    if not prerequisites.artifact_lineage_ready or not lineage.complete():
        diagnostics.append(_diag(ActivationDiagnosticCode.ACTIVATION_LINEAGE_INCOMPLETE, "activation", "Activation lineage is incomplete"))
    if not prerequisites.reproducibility_ready or not reproducibility.complete():
        diagnostics.append(_diag(ActivationDiagnosticCode.ACTIVATION_REPRODUCIBILITY_INCOMPLETE, "activation", "Activation reproducibility is incomplete"))
    if not prerequisites.source_authority_evidence_ready:
        diagnostics.append(_diag(ActivationDiagnosticCode.SOURCE_AUTHORITY_EVIDENCE_ABSENT, "activation", "Source authority evidence is absent"))
        limitations.append("REAL_EXTERNAL_EVIDENCE_UNAVAILABLE")
    if not prerequisites.pit_identity_context_evidence_ready:
        diagnostics.append(_diag(ActivationDiagnosticCode.PIT_IDENTITY_CONTEXT_EVIDENCE_ABSENT, "activation", "PIT identity/context evidence is absent"))
    if not prerequisites.comparator_evidence_ready:
        diagnostics.append(_diag(ActivationDiagnosticCode.COMPARATOR_EVIDENCE_ABSENT, "activation", "Comparator evidence is absent"))
    if not prerequisites.prepared_observations_ready:
        diagnostics.append(_diag(ActivationDiagnosticCode.PREPARED_OBSERVATIONS_UNAVAILABLE, "activation", "Prepared Observations are unavailable"))
        limitations.append("REAL_PREPARED_OBSERVATIONS_UNAVAILABLE")
    if not prerequisites.intake_platform_ready:
        diagnostics.append(_diag(ActivationDiagnosticCode.INTAKE_PLATFORM_UNAVAILABLE, "activation", "Intake platform is unavailable"))
    if not prerequisites.contamination_controls_ready:
        diagnostics.append(_diag(ActivationDiagnosticCode.CONTAMINATION_CONTROL_UNRESOLVED, "activation", "Contamination controls are unresolved"))
    if not prerequisites.negative_evidence_policy_ready:
        diagnostics.append(_diag(ActivationDiagnosticCode.NEGATIVE_EVIDENCE_POLICY_UNRESOLVED, "activation", "Negative-evidence policy is unresolved"))
    if not prerequisites.falsification_policy_ready:
        diagnostics.append(_diag(ActivationDiagnosticCode.FALSIFICATION_POLICY_UNRESOLVED, "activation", "Falsification policy is unresolved"))

    if registry:
        if registry.retirement_records:
            diagnostics.append(_diag(ActivationDiagnosticCode.MODULE_RETIRED, "activation", "Module has a retirement record"))
        if registry.suspension_records:
            diagnostics.append(_diag(ActivationDiagnosticCode.MODULE_SUSPENDED, "activation", "Module has a suspension record"))
        if registry.deactivation_records:
            diagnostics.append(_diag(ActivationDiagnosticCode.MODULE_DEACTIVATED, "activation", "Module has a deactivation record"))

    invariant_missing = any(
        code in {diag.code for diag in diagnostics}
        for code in (
            ActivationDiagnosticCode.MODULE_REGISTRATION_MISSING.value,
            ActivationDiagnosticCode.RESEARCH_PROGRAM_ID_MISSING.value,
            ActivationDiagnosticCode.ACTIVATION_SPECIFICATION_MISSING.value,
            ActivationDiagnosticCode.INTAKE_CONTRACT_MISSING.value,
            ActivationDiagnosticCode.ADAPTER_MISSING.value,
            ActivationDiagnosticCode.MODULE_INPUT_CONTRACT_MISSING.value,
            ActivationDiagnosticCode.MODULE_OUTPUT_CONTRACT_MISSING.value,
            ActivationDiagnosticCode.SCIENTIFIC_SPECIFICATION_MISSING.value,
            ActivationDiagnosticCode.FROZEN_HORIZON_SPECIFICATION_MISSING.value,
        )
    )
    if invariant_missing:
        diagnostics.append(_diag(ActivationDiagnosticCode.ACTIVATION_INVARIANT_INCOMPLETE, "activation", "Activation invariant is incomplete"))

    if activation_declaration.requested_activation_state == ModuleActivationState.MODULE_ACTIVE and not activation_declaration.explicit_activation_authorized:
        diagnostics.append(_diag(ActivationDiagnosticCode.ACTIVATION_NOT_EXPLICITLY_AUTHORIZED, "activation", "Explicit activation authorization is absent"))
    if activation_declaration.prohibited_activation:
        diagnostics.append(_diag(ActivationDiagnosticCode.ACTIVATION_NOT_EXPLICITLY_AUTHORIZED, "activation", "Requested activation is prohibited"))

    diagnostic_codes = {diag.code for diag in diagnostics}
    registry_fatal = _has_fatal_registry_diagnostic(registry_diags)
    if ActivationDiagnosticCode.MODULE_RETIRED.value in diagnostic_codes:
        state = ModuleActivationState.MODULE_RETIRED
    elif ActivationDiagnosticCode.MODULE_SUSPENDED.value in diagnostic_codes:
        state = ModuleActivationState.MODULE_SUSPENDED
    elif ActivationDiagnosticCode.MODULE_DEACTIVATED.value in diagnostic_codes:
        state = ModuleActivationState.MODULE_DEACTIVATED
    elif any(
        code in diagnostic_codes
        for code in (
            ActivationDiagnosticCode.MODULE_REGISTRATION_MISSING.value,
            ActivationDiagnosticCode.RESEARCH_PROGRAM_ACTIVATION_SPECIFICATION_MISMATCH.value,
            ActivationDiagnosticCode.ACTIVATION_INVARIANT_INCOMPLETE.value,
            ActivationDiagnosticCode.ACTIVATION_VERSION_INCOMPATIBILITY.value,
            ActivationDiagnosticCode.ACTIVATION_LINEAGE_INCOMPLETE.value,
            ActivationDiagnosticCode.ACTIVATION_REPRODUCIBILITY_INCOMPLETE.value,
            ActivationDiagnosticCode.SOURCE_AUTHORITY_EVIDENCE_ABSENT.value,
            ActivationDiagnosticCode.PIT_IDENTITY_CONTEXT_EVIDENCE_ABSENT.value,
            ActivationDiagnosticCode.COMPARATOR_EVIDENCE_ABSENT.value,
            ActivationDiagnosticCode.PREPARED_OBSERVATIONS_UNAVAILABLE.value,
            ActivationDiagnosticCode.INTAKE_PLATFORM_UNAVAILABLE.value,
            ActivationDiagnosticCode.ACTIVATION_EFFECTIVE_INTERVAL_INVALID.value,
            ActivationDiagnosticCode.ACTIVATION_NOT_EXPLICITLY_AUTHORIZED.value,
        )
    ) or registry_fatal or activation_binding_failure:
        state = ModuleActivationState.MODULE_ACTIVATION_BLOCKED
    elif any(
        code in diagnostic_codes
        for code in (
            ActivationDiagnosticCode.CONTAMINATION_CONTROL_UNRESOLVED.value,
            ActivationDiagnosticCode.NEGATIVE_EVIDENCE_POLICY_UNRESOLVED.value,
            ActivationDiagnosticCode.FALSIFICATION_POLICY_UNRESOLVED.value,
        )
    ) or prerequisites.unresolved_readiness:
        state = ModuleActivationState.MODULE_ACTIVATION_UNRESOLVED
    elif prerequisites.conditional_readiness:
        state = ModuleActivationState.MODULE_ACTIVATION_CONDITIONALLY_READY
        limitations.append("CONDITIONAL_ACTIVATION_READINESS")
    elif activation_declaration.requested_activation_state == ModuleActivationState.MODULE_ACTIVE and activation_declaration.explicit_activation_authorized:
        state = ModuleActivationState.MODULE_ACTIVE
    else:
        state = ModuleActivationState.MODULE_ACTIVATION_READY

    if adapter and adapter.scientific_transformation_permitted:
        limitations.append("SCIENTIFIC_TRANSFORMATION_PROHIBITED_IN_ADAPTER")
    if activation_declaration.module_registration_id.endswith("historical_first_module"):
        limitations.append("HISTORICAL_FIRST_MODULE_ADAPTER_DEFERRED")

    activation_evaluation_id = "activation_eval_" + _stable_hash(
        {
            "activation_declaration": activation_declaration.activation_declaration_id,
            "diagnostics": [diag.to_dict() for diag in diagnostics],
            "state": state.value,
        }
    )
    return ActivationEvaluation(
        activation_evaluation_id=activation_evaluation_id,
        module_registration=registration,
        activation_declaration=activation_declaration,
        activation_state=state,
        activation_diagnostics=_dedupe_diagnostics(diagnostics),
        activation_limitations=_limitations(*limitations),
        prerequisite_states=prerequisites,
        adapter_metadata=adapter,
        adapter_compatibility_state=adapter.adapter_status if adapter else AdapterCompatibilityState.INSUFFICIENT_ADAPTER_EVIDENCE,
        version_compatibility=version_compatibility,
        lineage_metadata=lineage,
        reproducibility_metadata=reproducibility,
        registry_references={
            "activation_declaration_id": activation_declaration.activation_declaration_id,
            "module_registration_id": activation_declaration.module_registration_id,
            "registry_snapshot_id": registry.registry_snapshot_id if registry else "",
        },
        registry_diagnostics=_dedupe_diagnostics(registry_diags),
        governing_versions=_base_governing_versions(),
    )


def deterministic_execution_identity(request: ExecutionAuthorizationRequest) -> str:
    payload = {
        "activation_id": request.activation_id,
        "activation_specification_version": request.activation_specification_version,
        "adapter_version": request.adapter_version,
        "frozen_horizon_specification_version": request.frozen_horizon_specification_version,
        "handoff_contract_id": request.handoff_contract_id,
        "input_contract_version": request.module_input_contract_version,
        "intake_evaluation_id": request.intake_evaluation_id,
        "module_id": request.module_id,
        "module_version": request.module_version,
        "output_contract_version": request.module_output_contract_version,
        "prepared_observation_package_id": request.prepared_observation_package_id,
        "scientific_specification_version": request.scientific_specification_version,
    }
    return "scientific_execution_identity_" + _stable_hash(payload)


def evaluate_execution_authorization(
    activation_evaluation: ActivationEvaluation,
    request: ExecutionAuthorizationRequest,
    registry: RegistrySnapshot | None = None,
    duplicate_metadata: DuplicateExecutionMetadata | None = None,
    lineage: ArtifactLineage | None = None,
    reproducibility: ReproducibilityMetadata | None = None,
) -> ExecutionAuthorization:
    duplicate_metadata = duplicate_metadata or DuplicateExecutionMetadata()
    lineage = lineage or activation_evaluation.lineage_metadata
    reproducibility = reproducibility or activation_evaluation.reproducibility_metadata
    diagnostics: list[Diagnostic] = []
    limitations = ["REFERENCE_IMPLEMENTATION_ONLY", "SYNTHETIC_REGISTRY_ONLY"]
    execution_binding_failure = False

    if activation_evaluation.activation_state == ModuleActivationState.MODULE_RETIRED:
        state = ExecutionAuthorizationState.EXECUTION_EXCLUDED
        diagnostics.append(_diag(ExecutionDiagnosticCode.MODULE_NOT_ACTIVE, "execution", "Module is retired and not active"))
    elif activation_evaluation.activation_state != ModuleActivationState.MODULE_ACTIVE:
        state = ExecutionAuthorizationState.EXECUTION_BLOCKED
        diagnostics.append(_diag(ExecutionDiagnosticCode.MODULE_NOT_ACTIVE, "execution", "Module is not active"))
    else:
        state = ExecutionAuthorizationState.EXECUTION_AUTHORIZED

    registry_diags = _registry_diagnostics(registry) if registry is not None else ()
    if _has_fatal_registry_diagnostic(registry_diags):
        diagnostics.append(_diag(ExecutionDiagnosticCode.INSUFFICIENT_EXECUTION_EVIDENCE, "execution", "Registry authority evidence is not executable"))
        execution_binding_failure = True
    if activation_evaluation.activation_declaration.superseded or (registry and registry.supersession_records):
        diagnostics.append(_diag(ExecutionDiagnosticCode.ACTIVATION_SUPERSEDED, "execution", "Activation is superseded"))
    decl = activation_evaluation.activation_declaration
    if _is_blank(request.requested_execution_interval) or len(request.requested_execution_interval) != 2:
        start, end = None, None
    else:
        start, end = request.requested_execution_interval
    if (
        start is None
        or end is None
        or decl.activation_effective_start is None
        or decl.activation_effective_end is None
        or start < decl.activation_effective_start
        or end > decl.activation_effective_end
        or end < start
    ):
        diagnostics.append(_diag(ExecutionDiagnosticCode.ACTIVATION_EXPIRED, "execution", "Execution interval is outside activation interval"))
    required_execution_fields = (
        (request.execution_authorization_request_id, ExecutionDiagnosticCode.INSUFFICIENT_EXECUTION_EVIDENCE, "execution authorization request id"),
        (request.activation_id, ExecutionDiagnosticCode.INSUFFICIENT_EXECUTION_EVIDENCE, "activation id"),
        (request.module_id, ExecutionDiagnosticCode.EXECUTION_VERSION_INCOMPATIBILITY, "module id"),
        (request.module_version, ExecutionDiagnosticCode.EXECUTION_VERSION_INCOMPATIBILITY, "module version"),
        (request.module_specification_version, ExecutionDiagnosticCode.EXECUTION_VERSION_INCOMPATIBILITY, "module specification version"),
        (request.activation_specification_id, ExecutionDiagnosticCode.EXECUTION_VERSION_INCOMPATIBILITY, "activation specification id"),
        (request.activation_specification_version, ExecutionDiagnosticCode.EXECUTION_VERSION_INCOMPATIBILITY, "activation specification version"),
        (request.intake_evaluation_id, ExecutionDiagnosticCode.HANDOFF_INCOMPLETE, "intake evaluation id"),
        (request.prepared_observation_package_id, ExecutionDiagnosticCode.HANDOFF_INCOMPLETE, "Prepared Observation package id"),
        (request.handoff_contract_id, ExecutionDiagnosticCode.HANDOFF_INCOMPLETE, "handoff contract id"),
        (request.adapter_id, ExecutionDiagnosticCode.ADAPTER_INCOMPATIBLE, "adapter id"),
        (request.adapter_version, ExecutionDiagnosticCode.EXECUTION_VERSION_INCOMPATIBILITY, "adapter version"),
        (request.module_input_contract_id, ExecutionDiagnosticCode.EXECUTION_INPUT_CONTRACT_MISSING, "module input contract id"),
        (request.module_input_contract_version, ExecutionDiagnosticCode.EXECUTION_VERSION_INCOMPATIBILITY, "module input contract version"),
        (request.module_output_contract_id, ExecutionDiagnosticCode.EXECUTION_OUTPUT_CONTRACT_MISSING, "module output contract id"),
        (request.module_output_contract_version, ExecutionDiagnosticCode.EXECUTION_VERSION_INCOMPATIBILITY, "module output contract version"),
        (request.scientific_specification_id, ExecutionDiagnosticCode.EXECUTION_SCIENTIFIC_SPECIFICATION_MISSING, "scientific specification id"),
        (request.scientific_specification_version, ExecutionDiagnosticCode.EXECUTION_VERSION_INCOMPATIBILITY, "scientific specification version"),
        (request.frozen_horizon_specification_id, ExecutionDiagnosticCode.EXECUTION_FROZEN_HORIZON_MISSING, "frozen horizon specification id"),
        (request.frozen_horizon_specification_version, ExecutionDiagnosticCode.EXECUTION_VERSION_INCOMPATIBILITY, "frozen horizon specification version"),
        (request.requesting_execution_identity, ExecutionDiagnosticCode.INSUFFICIENT_EXECUTION_EVIDENCE, "requesting execution identity"),
        (request.duplicate_policy, ExecutionDiagnosticCode.INSUFFICIENT_EXECUTION_EVIDENCE, "duplicate policy"),
        (request.governing_versions, ExecutionDiagnosticCode.INSUFFICIENT_EXECUTION_EVIDENCE, "governing versions"),
    )
    for value, code, label in required_execution_fields:
        if _is_blank(value):
            diagnostics.append(_diag(code, "execution", f"Missing {label}"))
            execution_binding_failure = True
    authoritative_handoff_chain = _authoritative_handoff_chain(lineage)
    handoff_chain_fields = (
        (request.intake_evaluation_id, authoritative_handoff_chain["intake_evaluation_id"], "intake evaluation id"),
        (
            request.prepared_observation_package_id,
            authoritative_handoff_chain["prepared_observation_package_id"],
            "Prepared Observation package id",
        ),
        (request.handoff_contract_id, authoritative_handoff_chain["handoff_contract_id"], "handoff contract id"),
    )
    for request_value, authoritative_value, label in handoff_chain_fields:
        if _is_blank(authoritative_value):
            diagnostics.append(_diag(ExecutionDiagnosticCode.HANDOFF_INCOMPLETE, "execution", f"Authoritative {label} is missing"))
            execution_binding_failure = True
        elif not _is_blank(request_value) and request_value != authoritative_value:
            diagnostics.append(
                _diag(
                    ExecutionDiagnosticCode.HANDOFF_INCOMPLETE,
                    "execution",
                    f"Execution {label} does not match authoritative handoff chain",
                )
            )
            execution_binding_failure = True
    if request.activation_id != decl.activation_declaration_id:
        diagnostics.append(_diag(ExecutionDiagnosticCode.INSUFFICIENT_EXECUTION_EVIDENCE, "execution", "Execution activation id does not match evaluated activation"))
        execution_binding_failure = True
    if (
        request.module_id != decl.module_id
        or request.module_version != decl.module_version
        or request.module_specification_version != decl.module_specification_version
        or request.activation_specification_id != decl.activation_specification_id
        or request.activation_specification_version != decl.activation_specification_version
        or request.adapter_id != decl.adapter_id
        or request.adapter_version != decl.adapter_version
        or request.module_input_contract_id != decl.module_input_contract_id
        or request.module_input_contract_version != decl.module_input_contract_version
        or request.module_output_contract_id != decl.module_output_contract_id
        or request.module_output_contract_version != decl.module_output_contract_version
        or request.scientific_specification_id != decl.scientific_specification_id
        or request.scientific_specification_version != decl.scientific_specification_version
        or request.frozen_horizon_specification_id != decl.frozen_horizon_specification_id
        or request.frozen_horizon_specification_version != decl.frozen_horizon_specification_version
    ):
        diagnostics.append(_diag(ExecutionDiagnosticCode.EXECUTION_VERSION_INCOMPATIBILITY, "execution", "Execution request bindings do not match activation declaration"))
        execution_binding_failure = True
    if request.direct_upstream_bypass:
        diagnostics.append(_diag(ExecutionDiagnosticCode.DIRECT_UPSTREAM_BYPASS, "execution", "Direct upstream bypass is prohibited"))
    if request.raw_prepared_observation_bypass:
        diagnostics.append(_diag(ExecutionDiagnosticCode.RAW_PREPARED_OBSERVATION_BYPASS, "execution", "Raw Prepared Observation bypass is prohibited"))
    if request.intake_state not in decl.accepted_intake_states:
        diagnostics.append(_diag(ExecutionDiagnosticCode.INTAKE_STATE_NOT_ACCEPTED, "execution", "Intake state is not accepted"))
    if not request.handoff_complete:
        diagnostics.append(_diag(ExecutionDiagnosticCode.HANDOFF_INCOMPLETE, "execution", "Handoff is incomplete"))
    adapter = activation_evaluation.adapter_metadata
    if adapter is None or adapter.adapter_status not in (
        AdapterCompatibilityState.ADAPTER_COMPATIBLE,
        AdapterCompatibilityState.ADAPTER_CONDITIONALLY_COMPATIBLE,
    ):
        diagnostics.append(_diag(ExecutionDiagnosticCode.ADAPTER_INCOMPATIBLE, "execution", "Adapter is incompatible"))
    if adapter and adapter.scientific_transformation_permitted:
        diagnostics.append(_diag(ExecutionDiagnosticCode.SCIENTIFIC_TRANSFORMATION_IN_ADAPTER, "execution", "Adapter scientific transformation is prohibited"))
    if not request.module_input_contract_id:
        diagnostics.append(_diag(ExecutionDiagnosticCode.EXECUTION_INPUT_CONTRACT_MISSING, "execution", "Execution input contract is missing"))
    if not request.module_output_contract_id:
        diagnostics.append(_diag(ExecutionDiagnosticCode.EXECUTION_OUTPUT_CONTRACT_MISSING, "execution", "Execution output contract is missing"))
    if not request.scientific_specification_id:
        diagnostics.append(_diag(ExecutionDiagnosticCode.EXECUTION_SCIENTIFIC_SPECIFICATION_MISSING, "execution", "Execution scientific specification is missing"))
    if not request.frozen_horizon_specification_id:
        diagnostics.append(_diag(ExecutionDiagnosticCode.EXECUTION_FROZEN_HORIZON_MISSING, "execution", "Execution frozen horizon is missing"))
    if (
        request.module_version != decl.module_version
        or request.module_input_contract_version != decl.module_input_contract_version
        or request.module_output_contract_version != decl.module_output_contract_version
        or request.scientific_specification_version != decl.scientific_specification_version
        or request.frozen_horizon_specification_version != decl.frozen_horizon_specification_version
    ):
        diagnostics.append(_diag(ExecutionDiagnosticCode.EXECUTION_VERSION_INCOMPATIBILITY, "execution", "Execution versions are incompatible"))
    if not request.lineage_complete or not lineage.complete():
        diagnostics.append(_diag(ExecutionDiagnosticCode.EXECUTION_LINEAGE_INCOMPLETE, "execution", "Execution lineage is incomplete"))
    if not request.reproducibility_complete or not reproducibility.complete():
        diagnostics.append(_diag(ExecutionDiagnosticCode.EXECUTION_REPRODUCIBILITY_INCOMPLETE, "execution", "Execution reproducibility is incomplete"))
    if request.blocking_inherited_diagnostic:
        diagnostics.append(_diag(ExecutionDiagnosticCode.BLOCKING_INHERITED_DIAGNOSTIC, "execution", "Blocking inherited diagnostic is present"))
    if request.blocking_intake_diagnostic:
        diagnostics.append(_diag(ExecutionDiagnosticCode.BLOCKING_INTAKE_DIAGNOSTIC, "execution", "Blocking intake diagnostic is present"))
    if duplicate_metadata.duplicate_state in (
        DuplicateExecutionState.EXACT_RERUN,
        DuplicateExecutionState.ACCIDENTAL_DUPLICATE,
    ):
        diagnostics.append(_diag(ExecutionDiagnosticCode.DUPLICATE_EXECUTION, "execution", "Duplicate execution requires governance"))
    if duplicate_metadata.duplicate_state == DuplicateExecutionState.CONFLICTING_DUPLICATE:
        diagnostics.append(_diag(ExecutionDiagnosticCode.CONFLICTING_EXECUTION, "execution", "Conflicting duplicate execution is prohibited"))
    if request.unresolved_authorization:
        diagnostics.append(_diag(ExecutionDiagnosticCode.INSUFFICIENT_EXECUTION_EVIDENCE, "execution", "Execution authorization is unresolved"))
    if request.insufficient_authorization_evidence:
        diagnostics.append(_diag(ExecutionDiagnosticCode.INSUFFICIENT_EXECUTION_EVIDENCE, "execution", "Execution authorization evidence is insufficient"))
    if not request.explicit_execution_authorized:
        diagnostics.append(_diag(ExecutionDiagnosticCode.EXECUTION_NOT_EXPLICITLY_AUTHORIZED, "execution", "Explicit execution authorization is absent"))

    diagnostic_codes = {diag.code for diag in diagnostics}
    if state != ExecutionAuthorizationState.EXECUTION_EXCLUDED:
        if ExecutionDiagnosticCode.MODULE_NOT_ACTIVE.value in diagnostic_codes:
            state = ExecutionAuthorizationState.EXECUTION_BLOCKED
        elif any(
            code in diagnostic_codes
            for code in (
                ExecutionDiagnosticCode.ACTIVATION_EXPIRED.value,
                ExecutionDiagnosticCode.ACTIVATION_SUPERSEDED.value,
                ExecutionDiagnosticCode.DIRECT_UPSTREAM_BYPASS.value,
                ExecutionDiagnosticCode.RAW_PREPARED_OBSERVATION_BYPASS.value,
                ExecutionDiagnosticCode.INTAKE_STATE_NOT_ACCEPTED.value,
                ExecutionDiagnosticCode.HANDOFF_INCOMPLETE.value,
                ExecutionDiagnosticCode.ADAPTER_INCOMPATIBLE.value,
                ExecutionDiagnosticCode.SCIENTIFIC_TRANSFORMATION_IN_ADAPTER.value,
                ExecutionDiagnosticCode.EXECUTION_INPUT_CONTRACT_MISSING.value,
                ExecutionDiagnosticCode.EXECUTION_OUTPUT_CONTRACT_MISSING.value,
                ExecutionDiagnosticCode.EXECUTION_SCIENTIFIC_SPECIFICATION_MISSING.value,
                ExecutionDiagnosticCode.EXECUTION_FROZEN_HORIZON_MISSING.value,
                ExecutionDiagnosticCode.EXECUTION_VERSION_INCOMPATIBILITY.value,
                ExecutionDiagnosticCode.EXECUTION_LINEAGE_INCOMPLETE.value,
                ExecutionDiagnosticCode.EXECUTION_REPRODUCIBILITY_INCOMPLETE.value,
                ExecutionDiagnosticCode.BLOCKING_INHERITED_DIAGNOSTIC.value,
                ExecutionDiagnosticCode.BLOCKING_INTAKE_DIAGNOSTIC.value,
                ExecutionDiagnosticCode.DUPLICATE_EXECUTION.value,
                ExecutionDiagnosticCode.CONFLICTING_EXECUTION.value,
                ExecutionDiagnosticCode.EXECUTION_NOT_EXPLICITLY_AUTHORIZED.value,
            )
        ) or execution_binding_failure:
            state = ExecutionAuthorizationState.EXECUTION_BLOCKED
        elif request.unresolved_authorization:
            state = ExecutionAuthorizationState.EXECUTION_UNRESOLVED
        elif request.insufficient_authorization_evidence:
            state = ExecutionAuthorizationState.INSUFFICIENT_EXECUTION_AUTHORIZATION_EVIDENCE
        elif request.conditional_authorization or duplicate_metadata.duplicate_state in (
            DuplicateExecutionState.AUTHORIZED_RERUN,
            DuplicateExecutionState.CORRECTED_RERUN,
            DuplicateExecutionState.SUPERSEDING_EXECUTION,
            DuplicateExecutionState.SPECIFICATION_CHANGED_RERUN,
            DuplicateExecutionState.HORIZON_CHANGED_RERUN,
        ):
            state = ExecutionAuthorizationState.EXECUTION_CONDITIONALLY_AUTHORIZED
            limitations.append("CONDITIONAL_EXECUTION_AUTHORIZATION")
        else:
            state = ExecutionAuthorizationState.EXECUTION_AUTHORIZED

    identity = deterministic_execution_identity(request)
    authorization_id = "execution_auth_" + _stable_hash(
        {"identity": identity, "state": state.value, "diagnostics": [diag.to_dict() for diag in diagnostics]}
    )
    return ExecutionAuthorization(
        execution_authorization_id=authorization_id,
        execution_authorization_state=state,
        deterministic_execution_identity=identity,
        authorization_diagnostics=_dedupe_diagnostics(diagnostics),
        authorization_limitations=_limitations(*limitations),
        activation_reference=request.activation_id,
        intake_reference=request.intake_evaluation_id,
        handoff_reference=request.handoff_contract_id,
        adapter_reference=request.adapter_id,
        input_contract_reference=request.module_input_contract_id,
        output_contract_reference=request.module_output_contract_id,
        scientific_specification_reference=request.scientific_specification_id,
        frozen_horizon_reference=request.frozen_horizon_specification_id,
        duplicate_rerun_metadata=duplicate_metadata,
        lineage_metadata=lineage,
        reproducibility_metadata=reproducibility,
        governing_versions=_base_governing_versions(),
    )


def execution_request(**overrides: Any) -> ExecutionAuthorizationRequest:
    values = {
        "execution_authorization_request_id": "execution_request_selected_first_phase5_module_v1",
        "activation_id": "activation_declaration_selected_first_phase5_module_v1",
        "module_id": DEFAULT_MODULE_ID,
        "module_version": DEFAULT_MODULE_VERSION,
        "module_specification_version": DEFAULT_MODULE_SPECIFICATION_VERSION,
        "activation_specification_id": NARROW_ACTIVATION_SPECIFICATION_ID,
        "activation_specification_version": NARROW_ACTIVATION_SPECIFICATION_VERSION,
        "intake_evaluation_id": DEFAULT_INTAKE_EVALUATION_ID,
        "prepared_observation_package_id": DEFAULT_PREPARED_OBSERVATION_PACKAGE_ID,
        "handoff_contract_id": DEFAULT_HANDOFF_CONTRACT_ID,
        "adapter_id": DEFAULT_ADAPTER_ID,
        "adapter_version": DEFAULT_ADAPTER_VERSION,
        "module_input_contract_id": DEFAULT_INPUT_CONTRACT_ID,
        "module_input_contract_version": DEFAULT_INPUT_CONTRACT_VERSION,
        "module_output_contract_id": DEFAULT_OUTPUT_CONTRACT_ID,
        "module_output_contract_version": DEFAULT_OUTPUT_CONTRACT_VERSION,
        "scientific_specification_id": DEFAULT_SCIENTIFIC_SPECIFICATION_ID,
        "scientific_specification_version": DEFAULT_SCIENTIFIC_SPECIFICATION_VERSION,
        "frozen_horizon_specification_id": DEFAULT_FROZEN_HORIZON_SPECIFICATION_ID,
        "frozen_horizon_specification_version": DEFAULT_FROZEN_HORIZON_SPECIFICATION_VERSION,
        "requested_execution_interval": (2, 3),
        "requesting_execution_identity": "synthetic_requesting_execution_identity",
        "duplicate_policy": "no_silent_overwrite",
        "rerun_reason": "",
        "governing_versions": _base_governing_versions(),
    }
    values.update(overrides)
    return ExecutionAuthorizationRequest(**values)


def _fixture(
    fixture_id: str,
    declaration: ActivationDeclaration | None = None,
    registration: ScientificModuleRegistration | None = None,
    adapter: AdapterRegistration | None = None,
    registry: RegistrySnapshot | None = None,
    prerequisites: ActivationPrerequisiteState | None = None,
    version_compatibility: VersionCompatibility | None = None,
    lineage: ArtifactLineage | None = None,
    reproducibility: ReproducibilityMetadata | None = None,
    execution: ExecutionAuthorizationRequest | None = None,
    duplicate: DuplicateExecutionMetadata | None = None,
    expected_activation_state: ModuleActivationState | None = None,
    expected_activation_diagnostics: tuple[ActivationDiagnosticCode, ...] = (),
    expected_execution_state: ExecutionAuthorizationState | None = None,
    expected_execution_diagnostics: tuple[ExecutionDiagnosticCode, ...] = (),
) -> CanonicalActivationFixture:
    declaration = declaration or selected_activation_declaration()
    registration = registration if registration is not None else selected_module_registration()
    adapter = adapter if adapter is not None else selected_adapter_registration()
    registry = registry if registry is not None else registry_snapshot(registration=registration, declaration=declaration, adapter=adapter)
    prerequisites = prerequisites or ActivationPrerequisiteState()
    version_compatibility = version_compatibility or VersionCompatibility()
    lineage = lineage or ArtifactLineage()
    reproducibility = reproducibility or ReproducibilityMetadata(fixture_identifier=fixture_id)
    activation = evaluate_activation_readiness(declaration, registry, prerequisites, version_compatibility, lineage, reproducibility)
    execution_result = None
    duplicate = duplicate or DuplicateExecutionMetadata()
    if execution:
        execution_result = evaluate_execution_authorization(activation, execution, registry, duplicate, lineage, reproducibility)
    return CanonicalActivationFixture(
        fixture_id=fixture_id,
        registry_snapshot=registry,
        activation_declaration=declaration,
        prerequisites=prerequisites,
        version_compatibility=version_compatibility,
        lineage=lineage,
        reproducibility=reproducibility,
        expected_activation_state=expected_activation_state or activation.activation_state,
        expected_activation_diagnostics=expected_activation_diagnostics,
        execution_request=execution,
        duplicate_metadata=duplicate,
        expected_execution_state=expected_execution_state or (execution_result.execution_authorization_state if execution_result else None),
        expected_execution_diagnostics=expected_execution_diagnostics,
    )


def canonical_activation_registry_fixtures() -> tuple[CanonicalActivationFixture, ...]:
    fixtures: list[CanonicalActivationFixture] = []

    def add(*args: Any, **kwargs: Any) -> None:
        fixtures.append(_fixture(*args, **kwargs))

    missing_registration_registry = registry_snapshot(registration=None)
    add("ACT01_valid_module_registration")
    add("ACT02_missing_module_registration", registry=missing_registration_registry, expected_activation_diagnostics=(ActivationDiagnosticCode.MODULE_REGISTRATION_MISSING,))
    add("ACT03_missing_research_program_identity", declaration=selected_activation_declaration(research_program_id=""), expected_activation_diagnostics=(ActivationDiagnosticCode.RESEARCH_PROGRAM_ID_MISSING,))
    add("ACT04_missing_activation_specification", declaration=selected_activation_declaration(activation_specification_id=""), expected_activation_diagnostics=(ActivationDiagnosticCode.ACTIVATION_SPECIFICATION_MISSING,))
    add("ACT05_broad_program_narrow_spec_mismatch", declaration=selected_activation_declaration(activation_specification_id=SELECTED_RESEARCH_PROGRAM_ID), expected_activation_diagnostics=(ActivationDiagnosticCode.RESEARCH_PROGRAM_ACTIVATION_SPECIFICATION_MISMATCH,))
    add("ACT06_missing_intake_contract", declaration=selected_activation_declaration(intake_contract_id=""), expected_activation_diagnostics=(ActivationDiagnosticCode.INTAKE_CONTRACT_MISSING,))
    add("ACT07_missing_adapter", registry=registry_snapshot(adapter=None), expected_activation_diagnostics=(ActivationDiagnosticCode.ADAPTER_MISSING,))
    add("ACT08_missing_input_contract", declaration=selected_activation_declaration(module_input_contract_id=""), expected_activation_diagnostics=(ActivationDiagnosticCode.MODULE_INPUT_CONTRACT_MISSING,))
    add("ACT09_missing_output_contract", declaration=selected_activation_declaration(module_output_contract_id=""), expected_activation_diagnostics=(ActivationDiagnosticCode.MODULE_OUTPUT_CONTRACT_MISSING,))
    add("ACT10_missing_scientific_specification", declaration=selected_activation_declaration(scientific_specification_id=""), expected_activation_diagnostics=(ActivationDiagnosticCode.SCIENTIFIC_SPECIFICATION_MISSING,))
    add("ACT11_missing_frozen_horizon_specification", declaration=selected_activation_declaration(frozen_horizon_specification_id=""), expected_activation_diagnostics=(ActivationDiagnosticCode.FROZEN_HORIZON_SPECIFICATION_MISSING,))

    add("ACT12_selected_authority_absent", prerequisites=ActivationPrerequisiteState(source_authority_evidence_ready=False), expected_activation_diagnostics=(ActivationDiagnosticCode.SOURCE_AUTHORITY_EVIDENCE_ABSENT,))
    add("ACT13_selected_pit_absent", prerequisites=ActivationPrerequisiteState(pit_identity_context_evidence_ready=False), expected_activation_diagnostics=(ActivationDiagnosticCode.PIT_IDENTITY_CONTEXT_EVIDENCE_ABSENT,))
    add("ACT14_selected_comparator_absent", prerequisites=ActivationPrerequisiteState(comparator_evidence_ready=False), expected_activation_diagnostics=(ActivationDiagnosticCode.COMPARATOR_EVIDENCE_ABSENT,))
    add("ACT15_selected_prepared_observations_absent", prerequisites=ActivationPrerequisiteState(prepared_observations_ready=False), expected_activation_diagnostics=(ActivationDiagnosticCode.PREPARED_OBSERVATIONS_UNAVAILABLE,))
    add("ACT16_selected_all_real_prerequisites_absent", prerequisites=_selected_real_prerequisites(), expected_activation_state=ModuleActivationState.MODULE_ACTIVATION_BLOCKED, expected_activation_diagnostics=(ActivationDiagnosticCode.SOURCE_AUTHORITY_EVIDENCE_ABSENT, ActivationDiagnosticCode.PIT_IDENTITY_CONTEXT_EVIDENCE_ABSENT, ActivationDiagnosticCode.COMPARATOR_EVIDENCE_ABSENT, ActivationDiagnosticCode.PREPARED_OBSERVATIONS_UNAVAILABLE))
    add("ACT17_selected_registry_valid_activation_blocked", prerequisites=_selected_real_prerequisites(), expected_activation_state=ModuleActivationState.MODULE_ACTIVATION_BLOCKED)
    blocked_activation = evaluate_activation_readiness(selected_activation_declaration(), registry_snapshot(), _selected_real_prerequisites())
    add("ACT18_selected_execution_while_activation_blocked", prerequisites=_selected_real_prerequisites(), execution=execution_request(), expected_execution_state=ExecutionAuthorizationState.EXECUTION_BLOCKED, expected_execution_diagnostics=(ExecutionDiagnosticCode.MODULE_NOT_ACTIVE,))

    add("ACT19_activation_ready")
    add("ACT20_activation_conditionally_ready", prerequisites=ActivationPrerequisiteState(conditional_readiness=True), expected_activation_state=ModuleActivationState.MODULE_ACTIVATION_CONDITIONALLY_READY)
    add("ACT21_activation_unresolved", prerequisites=ActivationPrerequisiteState(unresolved_readiness=True), expected_activation_state=ModuleActivationState.MODULE_ACTIVATION_UNRESOLVED)
    add("ACT22_activation_blocked", prerequisites=ActivationPrerequisiteState(source_authority_evidence_ready=False), expected_activation_state=ModuleActivationState.MODULE_ACTIVATION_BLOCKED)
    add("ACT23_explicitly_authorized_active", declaration=selected_activation_declaration(requested_activation_state=ModuleActivationState.MODULE_ACTIVE, explicit_activation_authorized=True), expected_activation_state=ModuleActivationState.MODULE_ACTIVE)
    add("ACT24_module_suspended", registry=registry_snapshot(suspension_records=(LifecycleRecord("suspension_v1", "registration_selected_first_phase5_module_v1", "schema incompatibility", "suspension_artifact"),)), expected_activation_state=ModuleActivationState.MODULE_SUSPENDED)
    add("ACT25_module_deactivated", registry=registry_snapshot(deactivation_records=(LifecycleRecord("deactivation_v1", "registration_selected_first_phase5_module_v1", "governance action", "deactivation_artifact"),)), expected_activation_state=ModuleActivationState.MODULE_DEACTIVATED)
    add("ACT26_module_retired", registry=registry_snapshot(retirement_records=(LifecycleRecord("retirement_v1", "registration_selected_first_phase5_module_v1", "scientific retirement", "retirement_artifact"),)), expected_activation_state=ModuleActivationState.MODULE_RETIRED)
    add("ACT27_activation_interval_invalid", declaration=selected_activation_declaration(activation_effective_start=10, activation_effective_end=1), expected_activation_diagnostics=(ActivationDiagnosticCode.ACTIVATION_EFFECTIVE_INTERVAL_INVALID,))
    active_decl = selected_activation_declaration(requested_activation_state=ModuleActivationState.MODULE_ACTIVE, explicit_activation_authorized=True)
    add("ACT28_activation_interval_expired", declaration=active_decl, execution=execution_request(requested_execution_interval=(11, 12), explicit_execution_authorized=True), expected_execution_diagnostics=(ExecutionDiagnosticCode.ACTIVATION_EXPIRED,))
    add("ACT29_activation_superseded", declaration=selected_activation_declaration(superseded=True, requested_activation_state=ModuleActivationState.MODULE_ACTIVE, explicit_activation_authorized=True), registry=registry_snapshot(supersession_records=(SupersessionRecord("supersession_v1", "activation_declaration_selected_first_phase5_module_v1", "activation_declaration_v2", "version change"),)), execution=execution_request(explicit_execution_authorized=True), expected_execution_diagnostics=(ExecutionDiagnosticCode.ACTIVATION_SUPERSEDED,))

    add("ACT30_negative_evidence_policy_missing", prerequisites=ActivationPrerequisiteState(negative_evidence_policy_ready=False), expected_activation_diagnostics=(ActivationDiagnosticCode.NEGATIVE_EVIDENCE_POLICY_UNRESOLVED,))
    add("ACT31_falsification_policy_missing", prerequisites=ActivationPrerequisiteState(falsification_policy_ready=False), expected_activation_diagnostics=(ActivationDiagnosticCode.FALSIFICATION_POLICY_UNRESOLVED,))
    add("ACT32_contamination_control_unresolved", prerequisites=ActivationPrerequisiteState(contamination_controls_ready=False), expected_activation_diagnostics=(ActivationDiagnosticCode.CONTAMINATION_CONTROL_UNRESOLVED,))
    add("ACT33_lineage_incomplete", lineage=ArtifactLineage(source_authority_artifact=""), expected_activation_diagnostics=(ActivationDiagnosticCode.ACTIVATION_LINEAGE_INCOMPLETE,))
    add("ACT34_reproducibility_incomplete", reproducibility=ReproducibilityMetadata(fixture_identifier="ACT34", controlled_reference=False), expected_activation_diagnostics=(ActivationDiagnosticCode.ACTIVATION_REPRODUCIBILITY_INCOMPLETE,))
    add("ACT35_version_incompatible", version_compatibility=VersionCompatibility(adapter_version_compatible=False, input_contract_version_compatible=False), expected_activation_diagnostics=(ActivationDiagnosticCode.ACTIVATION_VERSION_INCOMPATIBILITY, ActivationDiagnosticCode.ADAPTER_VERSION_INCOMPATIBILITY, ActivationDiagnosticCode.INPUT_CONTRACT_VERSION_INCOMPATIBILITY))
    add("ACT36_scientific_transformation_enabled_in_adapter", adapter=selected_adapter_registration(scientific_transformation_permitted=True), declaration=selected_activation_declaration(requested_activation_state=ModuleActivationState.MODULE_ACTIVE, explicit_activation_authorized=True), execution=execution_request(explicit_execution_authorized=True), expected_execution_diagnostics=(ExecutionDiagnosticCode.SCIENTIFIC_TRANSFORMATION_IN_ADAPTER,))
    add("ACT37_direct_upstream_bypass_permitted", declaration=selected_activation_declaration(requested_activation_state=ModuleActivationState.MODULE_ACTIVE, explicit_activation_authorized=True), execution=execution_request(direct_upstream_bypass=True, explicit_execution_authorized=True), expected_execution_diagnostics=(ExecutionDiagnosticCode.DIRECT_UPSTREAM_BYPASS,))
    add("ACT38_raw_prepared_observation_bypass_permitted", declaration=selected_activation_declaration(requested_activation_state=ModuleActivationState.MODULE_ACTIVE, explicit_activation_authorized=True), execution=execution_request(raw_prepared_observation_bypass=True, explicit_execution_authorized=True), expected_execution_diagnostics=(ExecutionDiagnosticCode.RAW_PREPARED_OBSERVATION_BYPASS,))

    active = selected_activation_declaration(requested_activation_state=ModuleActivationState.MODULE_ACTIVE, explicit_activation_authorized=True)
    add("ACT39_execution_authorized_synthetic", declaration=active, execution=execution_request(explicit_execution_authorized=True), expected_execution_state=ExecutionAuthorizationState.EXECUTION_AUTHORIZED)
    add("ACT40_execution_conditionally_authorized", declaration=active, execution=execution_request(explicit_execution_authorized=True, conditional_authorization=True), expected_execution_state=ExecutionAuthorizationState.EXECUTION_CONDITIONALLY_AUTHORIZED)
    add("ACT41_execution_unresolved", declaration=active, execution=execution_request(explicit_execution_authorized=True, unresolved_authorization=True), expected_execution_state=ExecutionAuthorizationState.EXECUTION_UNRESOLVED)
    add("ACT42_execution_blocked_module_inactive", execution=execution_request(explicit_execution_authorized=True), expected_execution_state=ExecutionAuthorizationState.EXECUTION_BLOCKED)
    add("ACT43_execution_blocked_suspended", registry=registry_snapshot(suspension_records=(LifecycleRecord("suspension_exec", "registration_selected_first_phase5_module_v1", "governance action", "suspension"),)), execution=execution_request(explicit_execution_authorized=True), expected_execution_state=ExecutionAuthorizationState.EXECUTION_BLOCKED)
    add("ACT44_execution_blocked_deactivated", registry=registry_snapshot(deactivation_records=(LifecycleRecord("deactivation_exec", "registration_selected_first_phase5_module_v1", "governance action", "deactivation"),)), execution=execution_request(explicit_execution_authorized=True), expected_execution_state=ExecutionAuthorizationState.EXECUTION_BLOCKED)
    add("ACT45_execution_excluded_retired", registry=registry_snapshot(retirement_records=(LifecycleRecord("retirement_exec", "registration_selected_first_phase5_module_v1", "scientific retirement", "retirement"),)), execution=execution_request(explicit_execution_authorized=True), expected_execution_state=ExecutionAuthorizationState.EXECUTION_EXCLUDED)
    add("ACT46_intake_state_not_accepted", declaration=active, execution=execution_request(explicit_execution_authorized=True, intake_state="INTAKE_INCOMPATIBLE"), expected_execution_diagnostics=(ExecutionDiagnosticCode.INTAKE_STATE_NOT_ACCEPTED,))
    add("ACT47_handoff_incomplete", declaration=active, execution=execution_request(explicit_execution_authorized=True, handoff_complete=False), expected_execution_diagnostics=(ExecutionDiagnosticCode.HANDOFF_INCOMPLETE,))
    add("ACT48_adapter_incompatible", declaration=active, adapter=selected_adapter_registration(adapter_status=AdapterCompatibilityState.ADAPTER_INCOMPATIBLE), execution=execution_request(explicit_execution_authorized=True), expected_execution_diagnostics=(ExecutionDiagnosticCode.ADAPTER_INCOMPATIBLE,))
    add("ACT49_blocking_inherited_diagnostic", declaration=active, execution=execution_request(explicit_execution_authorized=True, blocking_inherited_diagnostic=True), expected_execution_diagnostics=(ExecutionDiagnosticCode.BLOCKING_INHERITED_DIAGNOSTIC,))
    add("ACT50_blocking_intake_diagnostic", declaration=active, execution=execution_request(explicit_execution_authorized=True, blocking_intake_diagnostic=True), expected_execution_diagnostics=(ExecutionDiagnosticCode.BLOCKING_INTAKE_DIAGNOSTIC,))
    add("ACT51_execution_lineage_incomplete", declaration=active, execution=execution_request(explicit_execution_authorized=True, lineage_complete=False), expected_execution_diagnostics=(ExecutionDiagnosticCode.EXECUTION_LINEAGE_INCOMPLETE,))
    add("ACT52_execution_reproducibility_incomplete", declaration=active, execution=execution_request(explicit_execution_authorized=True, reproducibility_complete=False), expected_execution_diagnostics=(ExecutionDiagnosticCode.EXECUTION_REPRODUCIBILITY_INCOMPLETE,))
    add("ACT53_duplicate_execution", declaration=active, execution=execution_request(explicit_execution_authorized=True), duplicate=DuplicateExecutionMetadata(DuplicateExecutionState.EXACT_RERUN), expected_execution_diagnostics=(ExecutionDiagnosticCode.DUPLICATE_EXECUTION,))
    add("ACT54_conflicting_execution", declaration=active, execution=execution_request(explicit_execution_authorized=True), duplicate=DuplicateExecutionMetadata(DuplicateExecutionState.CONFLICTING_DUPLICATE), expected_execution_diagnostics=(ExecutionDiagnosticCode.CONFLICTING_EXECUTION,))
    add("ACT55_execution_interval_outside_activation", declaration=active, execution=execution_request(requested_execution_interval=(0, 20), explicit_execution_authorized=True), expected_execution_diagnostics=(ExecutionDiagnosticCode.ACTIVATION_EXPIRED,))
    add("ACT56_explicit_execution_authorization_absent", declaration=active, execution=execution_request(explicit_execution_authorized=False), expected_execution_diagnostics=(ExecutionDiagnosticCode.EXECUTION_NOT_EXPLICITLY_AUTHORIZED,))

    add("ACT57_exact_rerun", declaration=active, execution=execution_request(explicit_execution_authorized=True), duplicate=DuplicateExecutionMetadata(DuplicateExecutionState.EXACT_RERUN, rerun_classification=RerunClassification.IDENTICAL_DETERMINISTIC_RERUN))
    add("ACT58_authorized_rerun", declaration=active, execution=execution_request(explicit_execution_authorized=True), duplicate=DuplicateExecutionMetadata(DuplicateExecutionState.AUTHORIZED_RERUN, rerun_classification=RerunClassification.ENVIRONMENT_ONLY_RERUN), expected_execution_state=ExecutionAuthorizationState.EXECUTION_CONDITIONALLY_AUTHORIZED)
    add("ACT59_accidental_duplicate", declaration=active, execution=execution_request(explicit_execution_authorized=True), duplicate=DuplicateExecutionMetadata(DuplicateExecutionState.ACCIDENTAL_DUPLICATE))
    add("ACT60_corrected_rerun", declaration=active, execution=execution_request(explicit_execution_authorized=True), duplicate=DuplicateExecutionMetadata(DuplicateExecutionState.CORRECTED_RERUN, rerun_classification=RerunClassification.CORRECTED_UPSTREAM_DATA_RERUN), expected_execution_state=ExecutionAuthorizationState.EXECUTION_CONDITIONALLY_AUTHORIZED)
    add("ACT61_specification_changed_rerun", declaration=active, execution=execution_request(explicit_execution_authorized=True), duplicate=DuplicateExecutionMetadata(DuplicateExecutionState.SPECIFICATION_CHANGED_RERUN, rerun_classification=RerunClassification.SCIENTIFIC_SPECIFICATION_RERUN), expected_execution_state=ExecutionAuthorizationState.EXECUTION_CONDITIONALLY_AUTHORIZED)
    add("ACT62_horizon_changed_rerun", declaration=active, execution=execution_request(explicit_execution_authorized=True), duplicate=DuplicateExecutionMetadata(DuplicateExecutionState.HORIZON_CHANGED_RERUN, rerun_classification=RerunClassification.HORIZON_VERSION_RERUN), expected_execution_state=ExecutionAuthorizationState.EXECUTION_CONDITIONALLY_AUTHORIZED)
    add("ACT63_superseding_execution", declaration=active, execution=execution_request(explicit_execution_authorized=True), duplicate=DuplicateExecutionMetadata(DuplicateExecutionState.SUPERSEDING_EXECUTION, supersedes_execution_identity="prior_identity"), expected_execution_state=ExecutionAuthorizationState.EXECUTION_CONDITIONALLY_AUTHORIZED)

    duplicate_registration = selected_module_registration(module_version="v1")
    add("ACT64_duplicate_registry_key", registry=registry_snapshot(registration=duplicate_registration, module_registrations=(duplicate_registration, duplicate_registration)))
    add("ACT65_conflicting_registry_version", registry=registry_snapshot(module_registrations=(selected_module_registration(module_version="v1"), selected_module_registration(module_version="v2"))))
    add("ACT66_ambiguous_authoritative_record", registry=registry_snapshot(module_registrations=(selected_module_registration(), selected_module_registration(module_registration_id="registration_selected_first_phase5_module_v1"))))
    add("ACT67_superseded_record_selected", registry=registry_snapshot(supersession_records=(SupersessionRecord("registry_supersession", "registration_selected_first_phase5_module_v1", "registration_v2", "version change"),)))
    add("ACT68_inactive_record_selected", registry=registry_snapshot(inactive_records=("registration_selected_first_phase5_module_v1",)))

    return tuple(fixtures)


def activation_registry_guardrail_manifest() -> dict[str, bool]:
    return {
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


def real_selected_module_blocked_result() -> tuple[ActivationEvaluation, ExecutionAuthorization]:
    declaration = selected_activation_declaration()
    registry = registry_snapshot(declaration=declaration)
    activation = evaluate_activation_readiness(declaration, registry, _selected_real_prerequisites())
    execution = evaluate_execution_authorization(activation, execution_request(explicit_execution_authorized=True), registry)
    return activation, execution
