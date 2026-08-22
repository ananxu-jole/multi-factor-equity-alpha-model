from __future__ import annotations

from dataclasses import dataclass, field, is_dataclass
from enum import Enum
import hashlib
import json
from typing import Any

from pipelines import project_underdog_phase5_prepared_observations_reference_implementation_v1 as po
from pipelines import project_underdog_phase5_scientific_module_activation_registry_and_execution_authorization_reference_implementation_v1 as ar
from pipelines import project_underdog_phase5_scientific_module_intake_reference_implementation_v1 as smi


MODULE_ID = "project_underdog_phase5_selected_scientific_module_adapter_reference_implementation_v1"
MODULE_VERSION = "v1"
DESIGN_ID = "project_underdog_phase5_selected_scientific_module_adapter_and_frozen_activation_specification_design_v1"
STABLE_SERIALIZATION_VERSION = "stable_json_v1"

SELECTED_RESEARCH_PROGRAM_ID = "Peer-Relative Post-Stress Repair And Stabilization Asymmetry"
SELECTED_RESEARCH_PROGRAM_VERSION = ar.SELECTED_RESEARCH_PROGRAM_VERSION
NARROW_ACTIVATION_SPECIFICATION_ID = "Common-Versus-Idiosyncratic Post-Stress Repair Decomposition"
NARROW_ACTIVATION_SPECIFICATION_VERSION = ar.NARROW_ACTIVATION_SPECIFICATION_VERSION

DEFAULT_ADAPTER_REGISTRATION_ID = "selected_module_adapter_registration_v1"
DEFAULT_ADAPTER_ID = ar.DEFAULT_ADAPTER_ID
DEFAULT_ADAPTER_VERSION = ar.DEFAULT_ADAPTER_VERSION
DEFAULT_MODULE_ID = ar.DEFAULT_MODULE_ID
DEFAULT_MODULE_VERSION = ar.DEFAULT_MODULE_VERSION
DEFAULT_INTAKE_CONTRACT_ID = ar.DEFAULT_INTAKE_CONTRACT_ID
DEFAULT_INTAKE_CONTRACT_VERSION = ar.DEFAULT_INTAKE_CONTRACT_VERSION
DEFAULT_HANDOFF_CONTRACT_ID = ar.DEFAULT_HANDOFF_CONTRACT_ID
DEFAULT_HANDOFF_CONTRACT_VERSION = "v1"
DEFAULT_MODULE_INPUT_CONTRACT_ID = ar.DEFAULT_INPUT_CONTRACT_ID
DEFAULT_MODULE_INPUT_CONTRACT_VERSION = ar.DEFAULT_INPUT_CONTRACT_VERSION
DEFAULT_SCIENTIFIC_SPECIFICATION_ID = ar.DEFAULT_SCIENTIFIC_SPECIFICATION_ID
DEFAULT_SCIENTIFIC_SPECIFICATION_VERSION = ar.DEFAULT_SCIENTIFIC_SPECIFICATION_VERSION
DEFAULT_FROZEN_HORIZON_SPECIFICATION_ID = ar.DEFAULT_FROZEN_HORIZON_SPECIFICATION_ID
DEFAULT_FROZEN_HORIZON_SPECIFICATION_VERSION = ar.DEFAULT_FROZEN_HORIZON_SPECIFICATION_VERSION
DEFAULT_INFORMATION_ROLE_SCHEMA_VERSION = ar.DEFAULT_INFORMATION_ROLE_SCHEMA_VERSION
DEFAULT_DIAGNOSTIC_SCHEMA_VERSION = "selected_module_adapter_diagnostic_schema_v1"
DEFAULT_ARTIFACT_LINEAGE_SCHEMA_VERSION = "selected_module_adapter_artifact_lineage_schema_v1"
DEFAULT_REPRODUCIBILITY_SCHEMA_VERSION = "selected_module_adapter_reproducibility_schema_v1"
DEFAULT_REQUIRED_ROLE = po.InformationRole.COMMON_IDIOSYNCRATIC_DECOMPOSITION_INFORMATION.value


class SelectedModuleAdapterState(str, Enum):
    COMPATIBLE = "SELECTED_MODULE_ADAPTER_COMPATIBLE"
    CONDITIONALLY_COMPATIBLE = "SELECTED_MODULE_ADAPTER_CONDITIONALLY_COMPATIBLE"
    UNRESOLVED = "SELECTED_MODULE_ADAPTER_UNRESOLVED"
    INCOMPATIBLE = "SELECTED_MODULE_ADAPTER_INCOMPATIBLE"
    EXCLUDED = "SELECTED_MODULE_ADAPTER_EXCLUDED"
    INSUFFICIENT_EVIDENCE = "INSUFFICIENT_SELECTED_MODULE_ADAPTER_EVIDENCE"


class FrozenModuleInputState(str, Enum):
    READY = "FROZEN_MODULE_INPUT_READY"
    CONDITIONALLY_READY = "FROZEN_MODULE_INPUT_CONDITIONALLY_READY"
    UNRESOLVED = "FROZEN_MODULE_INPUT_UNRESOLVED"
    INCOMPLETE = "FROZEN_MODULE_INPUT_INCOMPLETE"
    EXCLUDED = "FROZEN_MODULE_INPUT_EXCLUDED"
    INSUFFICIENT_EVIDENCE = "INSUFFICIENT_FROZEN_MODULE_INPUT_EVIDENCE"


class AdapterDiagnosticCode(str, Enum):
    EXECUTION_NOT_AUTHORIZED = "EXECUTION_NOT_AUTHORIZED"
    ACTIVATION_REFERENCE_MISMATCH = "ACTIVATION_REFERENCE_MISMATCH"
    INTAKE_EVALUATION_REFERENCE_MISMATCH = "INTAKE_EVALUATION_REFERENCE_MISMATCH"
    PREPARED_OBSERVATION_REFERENCE_MISMATCH = "PREPARED_OBSERVATION_REFERENCE_MISMATCH"
    HANDOFF_REFERENCE_MISMATCH = "HANDOFF_REFERENCE_MISMATCH"
    ADAPTER_REFERENCE_MISMATCH = "ADAPTER_REFERENCE_MISMATCH"
    MODULE_REFERENCE_MISMATCH = "MODULE_REFERENCE_MISMATCH"
    RESEARCH_PROGRAM_REFERENCE_MISMATCH = "RESEARCH_PROGRAM_REFERENCE_MISMATCH"
    ACTIVATION_SPECIFICATION_REFERENCE_MISMATCH = "ACTIVATION_SPECIFICATION_REFERENCE_MISMATCH"
    MODULE_INPUT_CONTRACT_REFERENCE_MISMATCH = "MODULE_INPUT_CONTRACT_REFERENCE_MISMATCH"
    SCIENTIFIC_SPECIFICATION_REFERENCE_MISMATCH = "SCIENTIFIC_SPECIFICATION_REFERENCE_MISMATCH"
    FROZEN_HORIZON_REFERENCE_MISMATCH = "FROZEN_HORIZON_REFERENCE_MISMATCH"
    SCIENTIFIC_TRANSFORMATION_PROHIBITED = "SCIENTIFIC_TRANSFORMATION_PROHIBITED"
    ADAPTER_VERSION_INCOMPATIBLE = "ADAPTER_VERSION_INCOMPATIBLE"
    HANDOFF_CONTRACT_VERSION_INCOMPATIBLE = "HANDOFF_CONTRACT_VERSION_INCOMPATIBLE"
    MODULE_INPUT_CONTRACT_VERSION_INCOMPATIBLE = "MODULE_INPUT_CONTRACT_VERSION_INCOMPATIBLE"
    SCIENTIFIC_SPECIFICATION_VERSION_INCOMPATIBLE = "SCIENTIFIC_SPECIFICATION_VERSION_INCOMPATIBLE"
    FROZEN_ACTIVATION_SPECIFICATION_VERSION_INCOMPATIBLE = "FROZEN_ACTIVATION_SPECIFICATION_VERSION_INCOMPATIBLE"
    FROZEN_HORIZON_VERSION_INCOMPATIBLE = "FROZEN_HORIZON_VERSION_INCOMPATIBLE"
    INFORMATION_ROLE_SCHEMA_VERSION_INCOMPATIBLE = "INFORMATION_ROLE_SCHEMA_VERSION_INCOMPATIBLE"
    DIAGNOSTIC_SCHEMA_VERSION_INCOMPATIBLE = "DIAGNOSTIC_SCHEMA_VERSION_INCOMPATIBLE"
    LINEAGE_SCHEMA_VERSION_INCOMPATIBLE = "LINEAGE_SCHEMA_VERSION_INCOMPATIBLE"
    REPRODUCIBILITY_SCHEMA_VERSION_INCOMPATIBLE = "REPRODUCIBILITY_SCHEMA_VERSION_INCOMPATIBLE"
    ADAPTER_LINEAGE_INCOMPLETE = "ADAPTER_LINEAGE_INCOMPLETE"
    ADAPTER_REPRODUCIBILITY_INCOMPLETE = "ADAPTER_REPRODUCIBILITY_INCOMPLETE"
    PROHIBITED_INFORMATION_ROLE = "PROHIBITED_INFORMATION_ROLE"
    REQUIRED_INFORMATION_ROLE_MISSING = "REQUIRED_INFORMATION_ROLE_MISSING"
    TARGET_MAPPING_INCOMPLETE = "TARGET_MAPPING_INCOMPLETE"
    CONTEXT_MAPPING_INCOMPLETE = "CONTEXT_MAPPING_INCOMPLETE"
    COMPARATOR_MAPPING_INCOMPLETE = "COMPARATOR_MAPPING_INCOMPLETE"
    TEMPORAL_METADATA_INCOMPATIBLE = "TEMPORAL_METADATA_INCOMPATIBLE"
    INSUFFICIENT_MAPPING_COVERAGE = "INSUFFICIENT_MAPPING_COVERAGE"
    UNACCEPTABLE_MAPPING_MISSINGNESS = "UNACCEPTABLE_MAPPING_MISSINGNESS"
    DIRECT_UPSTREAM_BYPASS = "DIRECT_UPSTREAM_BYPASS"
    RAW_PREPARED_OBSERVATION_BYPASS = "RAW_PREPARED_OBSERVATION_BYPASS"


PROHIBITED_INFORMATION_CONTRACT_FLAGS = (
    "exposes_formulas",
    "exposes_repair_outputs",
    "exposes_peer_common_repair",
    "exposes_idiosyncratic_repair",
    "exposes_decomposition_output",
    "exposes_stabilization_outputs",
    "exposes_asymmetry_outputs",
    "exposes_signals",
    "exposes_factors",
    "exposes_ranks",
    "exposes_scores",
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
)


@dataclass(frozen=True)
class AdapterDiagnostic:
    code: AdapterDiagnosticCode
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
class AdapterRegistrationMetadata:
    adapter_registration_id: str = DEFAULT_ADAPTER_REGISTRATION_ID
    adapter_id: str = DEFAULT_ADAPTER_ID
    adapter_version: str = DEFAULT_ADAPTER_VERSION
    module_id: str = DEFAULT_MODULE_ID
    module_version: str = DEFAULT_MODULE_VERSION
    research_program_id: str = SELECTED_RESEARCH_PROGRAM_ID
    research_program_version: str = SELECTED_RESEARCH_PROGRAM_VERSION
    activation_specification_id: str = NARROW_ACTIVATION_SPECIFICATION_ID
    activation_specification_version: str = NARROW_ACTIVATION_SPECIFICATION_VERSION
    intake_contract_id: str = DEFAULT_INTAKE_CONTRACT_ID
    intake_contract_version: str = DEFAULT_INTAKE_CONTRACT_VERSION
    handoff_contract_id: str = DEFAULT_HANDOFF_CONTRACT_ID
    handoff_contract_version: str = DEFAULT_HANDOFF_CONTRACT_VERSION
    module_input_contract_id: str = DEFAULT_MODULE_INPUT_CONTRACT_ID
    module_input_contract_version: str = DEFAULT_MODULE_INPUT_CONTRACT_VERSION
    scientific_specification_id: str = DEFAULT_SCIENTIFIC_SPECIFICATION_ID
    scientific_specification_version: str = DEFAULT_SCIENTIFIC_SPECIFICATION_VERSION
    frozen_horizon_specification_id: str = DEFAULT_FROZEN_HORIZON_SPECIFICATION_ID
    frozen_horizon_specification_version: str = DEFAULT_FROZEN_HORIZON_SPECIFICATION_VERSION
    information_role_schema_version: str = DEFAULT_INFORMATION_ROLE_SCHEMA_VERSION
    diagnostic_schema_version: str = DEFAULT_DIAGNOSTIC_SCHEMA_VERSION
    artifact_lineage_schema_version: str = DEFAULT_ARTIFACT_LINEAGE_SCHEMA_VERSION
    reproducibility_schema_version: str = DEFAULT_REPRODUCIBILITY_SCHEMA_VERSION
    adapter_status: SelectedModuleAdapterState = SelectedModuleAdapterState.COMPATIBLE
    scientific_transformation_permitted: bool = False
    artifact_reference: str = "synthetic_selected_module_adapter_artifact_v1"
    governing_versions: dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return _to_jsonable(self)


@dataclass(frozen=True)
class FrozenActivationSpecification:
    frozen_activation_specification_id: str = NARROW_ACTIVATION_SPECIFICATION_ID
    frozen_activation_specification_version: str = NARROW_ACTIVATION_SPECIFICATION_VERSION
    research_program_id: str = SELECTED_RESEARCH_PROGRAM_ID
    research_program_version: str = SELECTED_RESEARCH_PROGRAM_VERSION
    narrow_activation_specification_id: str = NARROW_ACTIVATION_SPECIFICATION_ID
    narrow_activation_specification_version: str = NARROW_ACTIVATION_SPECIFICATION_VERSION
    permitted_information_roles: tuple[str, ...] = (DEFAULT_REQUIRED_ROLE,)
    prohibited_information_roles: tuple[str, ...] = (
        po.InformationRole.DIAGNOSTIC_INFORMATION.value,
        po.InformationRole.EXPLANATORY_ONLY_INFORMATION.value,
        po.InformationRole.NEGATIVE_INFORMATION.value,
        po.InformationRole.VALIDATED_ALPHA_INFORMATION.value,
    )
    required_target_contract: str = "synthetic_target_observation_metadata_contract_v1"
    required_context_contract: str = "synthetic_context_metadata_contract_v1"
    required_comparator_contract: str = "synthetic_comparator_metadata_contract_v1"
    observation_time_policy: str = "preserve_existing_observation_time"
    temporal_alignment_policy: str = "preserve_existing_temporal_metadata"
    coverage_policy: str = "require_mapping_coverage"
    missingness_policy: str = "fail_required_missingness"
    frozen_horizon_specification_id: str = DEFAULT_FROZEN_HORIZON_SPECIFICATION_ID
    frozen_horizon_specification_version: str = DEFAULT_FROZEN_HORIZON_SPECIFICATION_VERSION
    negative_evidence_policy_reference: str = "project_underdog_phase5_negative_evidence_and_falsification_science_v1"
    falsification_policy_reference: str = "project_underdog_phase5_negative_evidence_and_falsification_science_v1"
    contamination_control_policy_reference: str = "project_underdog_phase5_external_information_contamination_and_orthogonality_science_v1"
    module_input_contract_id: str = DEFAULT_MODULE_INPUT_CONTRACT_ID
    module_input_contract_version: str = DEFAULT_MODULE_INPUT_CONTRACT_VERSION
    diagnostic_schema_version: str = DEFAULT_DIAGNOSTIC_SCHEMA_VERSION
    lineage_schema_version: str = DEFAULT_ARTIFACT_LINEAGE_SCHEMA_VERSION
    reproducibility_schema_version: str = DEFAULT_REPRODUCIBILITY_SCHEMA_VERSION
    governing_versions: dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return _to_jsonable(self)


@dataclass(frozen=True)
class AdapterReproducibilityMetadata:
    governing_design_version: str = DESIGN_ID
    adapter_implementation_version: str = MODULE_VERSION
    fixture_identifier: str = "synthetic_adapter_fixture"
    module_version: str = DEFAULT_MODULE_VERSION
    intake_contract_version: str = DEFAULT_INTAKE_CONTRACT_VERSION
    handoff_contract_version: str = DEFAULT_HANDOFF_CONTRACT_VERSION
    activation_specification_version: str = NARROW_ACTIVATION_SPECIFICATION_VERSION
    adapter_version: str = DEFAULT_ADAPTER_VERSION
    module_input_contract_version: str = DEFAULT_MODULE_INPUT_CONTRACT_VERSION
    scientific_specification_version: str = DEFAULT_SCIENTIFIC_SPECIFICATION_VERSION
    frozen_activation_specification_version: str = NARROW_ACTIVATION_SPECIFICATION_VERSION
    frozen_horizon_version: str = DEFAULT_FROZEN_HORIZON_SPECIFICATION_VERSION
    prepared_observation_version: str = po.MODULE_VERSION
    information_role_schema_version: str = DEFAULT_INFORMATION_ROLE_SCHEMA_VERSION
    diagnostic_schema_version: str = DEFAULT_DIAGNOSTIC_SCHEMA_VERSION
    lineage_schema_version: str = DEFAULT_ARTIFACT_LINEAGE_SCHEMA_VERSION
    reproducibility_schema_version: str = DEFAULT_REPRODUCIBILITY_SCHEMA_VERSION
    stable_serialization_version: str = STABLE_SERIALIZATION_VERSION
    deterministic_serialization: bool = True
    controlled_reference: bool = True

    def complete(self) -> bool:
        return all(self.to_dict().values())

    def to_dict(self) -> dict[str, Any]:
        return _to_jsonable(self)


@dataclass(frozen=True)
class AdapterEvaluationRequest:
    execution_authorization: ar.ExecutionAuthorization
    intake_handoff: smi.ScientificModuleIntakeResult
    activation_declaration: ar.ActivationDeclaration
    adapter_registration: AdapterRegistrationMetadata = field(default_factory=AdapterRegistrationMetadata)
    frozen_activation_specification: FrozenActivationSpecification = field(default_factory=FrozenActivationSpecification)
    reproducibility_metadata: AdapterReproducibilityMetadata = field(default_factory=AdapterReproducibilityMetadata)
    fixture_id: str = "synthetic_adapter_request"
    target_mapping_complete: bool = True
    context_mapping_complete: bool = True
    comparator_mapping_complete: bool = True
    direct_upstream_bypass: bool = False
    raw_prepared_observation_bypass: bool = False
    requester_metadata: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class FrozenModuleInputContract:
    frozen_module_input_id: str
    adapter_evaluation_id: str
    adapter_state: SelectedModuleAdapterState
    frozen_module_input_state: FrozenModuleInputState
    execution_authorization_id: str
    execution_authorization_state: str
    activation_id: str
    module_id: str
    module_version: str
    research_program_id: str
    activation_specification_id: str
    activation_specification_version: str
    intake_evaluation_id: str
    prepared_observation_package_id: str
    handoff_contract_id: str
    adapter_id: str
    adapter_version: str
    module_input_contract_id: str
    module_input_contract_version: str
    scientific_specification_id: str
    scientific_specification_version: str
    frozen_horizon_specification_id: str
    frozen_horizon_specification_version: str
    target_observation_metadata: dict[str, Any]
    context_attachments: tuple[dict[str, Any], ...]
    comparator_attachments: tuple[dict[str, Any], ...]
    information_role_bindings: tuple[dict[str, Any], ...]
    observation_time_metadata: dict[str, Any]
    temporal_metadata: dict[str, Any]
    coverage_metadata: dict[str, Any]
    missingness_metadata: dict[str, Any]
    inherited_diagnostics: tuple[dict[str, Any], ...]
    inherited_limitations: tuple[str, ...]
    adapter_diagnostics: tuple[AdapterDiagnostic, ...]
    adapter_limitations: tuple[str, ...]
    artifact_lineage: dict[str, Any]
    reproducibility_metadata: dict[str, Any]
    governing_versions: dict[str, str]
    information_contract: dict[str, Any]
    exposes_scientific_execution_artifact: bool = False
    exposes_scientific_result_artifact: bool = False
    exposes_measurement_artifact: bool = False
    exposes_validation_artifact: bool = False
    source_retrieval_performed: bool = False
    authority_evaluation_performed: bool = False
    pit_construction_performed: bool = False
    identity_construction_performed: bool = False
    comparator_construction_performed: bool = False
    prepared_observation_construction_performed: bool = False
    intake_recomputation_performed: bool = False
    activation_recomputation_performed: bool = False
    execution_authorization_recomputation_performed: bool = False
    scientific_transformation_performed: bool = False
    repair_calculation_performed: bool = False
    decomposition_calculation_performed: bool = False
    stabilization_calculation_performed: bool = False
    asymmetry_calculation_performed: bool = False
    formula_execution_performed: bool = False
    signal_generation_performed: bool = False
    factor_generation_performed: bool = False
    candidate_generation_performed: bool = False
    panel_generation_performed: bool = False
    ic_calculation_performed: bool = False
    validation_performed: bool = False
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
class SelectedModuleAdapterFixture:
    fixture_id: str
    description: str
    request: AdapterEvaluationRequest
    expected_adapter_state: SelectedModuleAdapterState
    expected_frozen_input_state: FrozenModuleInputState
    expected_diagnostic_codes: tuple[AdapterDiagnosticCode, ...] = ()
    expected_limitations: tuple[str, ...] = ()


def _to_jsonable(value: Any) -> Any:
    if isinstance(value, Enum):
        return value.value
    if is_dataclass(value):
        return {key: _to_jsonable(val) for key, val in sorted(value.__dict__.items())}
    if isinstance(value, dict):
        return {str(key): _to_jsonable(val) for key, val in sorted(value.items())}
    if isinstance(value, (tuple, list)):
        return [_to_jsonable(item) for item in value]
    return value


def _stable_json(payload: Any) -> str:
    return json.dumps(_to_jsonable(payload), sort_keys=True, separators=(",", ":"))


def _stable_hash(payload: Any) -> str:
    return hashlib.sha256(_stable_json(payload).encode("utf-8")).hexdigest()[:24]


def _diag(code: AdapterDiagnosticCode, component: str, message: str, *, inherited: bool = False) -> AdapterDiagnostic:
    return AdapterDiagnostic(code, component, message, inherited)


def _dedupe_diagnostics(diagnostics: list[AdapterDiagnostic]) -> tuple[AdapterDiagnostic, ...]:
    seen: set[tuple[str, str, str, bool]] = set()
    out: list[AdapterDiagnostic] = []
    for diag in diagnostics:
        key = (diag.code.value, diag.component, diag.message, diag.inherited)
        if key not in seen:
            seen.add(key)
            out.append(diag)
    return tuple(out)


def _dedupe_strings(values: list[str]) -> tuple[str, ...]:
    return tuple(dict.fromkeys(values))


def _adapter_registration(**overrides: Any) -> AdapterRegistrationMetadata:
    values = {**AdapterRegistrationMetadata().__dict__}
    values["governing_versions"] = _base_governing_versions()
    values.update(overrides)
    return AdapterRegistrationMetadata(**values)


def _frozen_specification(**overrides: Any) -> FrozenActivationSpecification:
    values = {**FrozenActivationSpecification().__dict__}
    values["governing_versions"] = _base_governing_versions()
    values.update(overrides)
    return FrozenActivationSpecification(**values)


def _repro(**overrides: Any) -> AdapterReproducibilityMetadata:
    values = {**AdapterReproducibilityMetadata().__dict__}
    values.update(overrides)
    return AdapterReproducibilityMetadata(**values)


def _base_governing_versions() -> dict[str, str]:
    return {
        "activation_registry": ar.MODULE_VERSION,
        "adapter_design": DESIGN_ID,
        "adapter_implementation": MODULE_VERSION,
        "intake": smi.MODULE_VERSION,
        "prepared_observations": po.MODULE_VERSION,
        "stable_serialization": STABLE_SERIALIZATION_VERSION,
    }


def _selected_contract(
    *,
    required_context: bool = True,
    required_comparator: bool = True,
    conditional: bool = False,
    target_only: bool = False,
) -> smi.ModuleIntakeContract:
    required_roles = () if target_only else (DEFAULT_REQUIRED_ROLE,)
    context_requirements: tuple[smi.AttachmentRequirement, ...] = ()
    comparator_requirements: tuple[smi.AttachmentRequirement, ...] = ()
    accepted_states = (po.PreparedObservationReadinessState.STRUCTURALLY_READY,)
    temporal_states = (po.TemporalAlignmentState.FULLY_ALIGNED,)
    missingness = ()
    conditional_policy = "reject"
    if conditional:
        accepted_states = (
            po.PreparedObservationReadinessState.STRUCTURALLY_READY,
            po.PreparedObservationReadinessState.CONDITIONALLY_READY,
        )
        temporal_states = (po.TemporalAlignmentState.FULLY_ALIGNED, po.TemporalAlignmentState.PARTIALLY_ALIGNED)
        missingness = ("optional_field_missing",)
        conditional_policy = "accept"
    if not target_only and required_context:
        context_requirements = (
            smi.AttachmentRequirement(
                "required_context",
                "required",
                (DEFAULT_REQUIRED_ROLE,),
                accepted_statuses=("present",),
            ),
        )
    if not target_only and required_comparator:
        comparator_requirements = (
            smi.AttachmentRequirement(
                "required_comparator",
                "required",
                (DEFAULT_REQUIRED_ROLE,),
                accepted_statuses=("COMPARATOR_ELIGIBLE",),
                accepted_temporal_states=("valid_overlap",),
            ),
        )
    return smi._contract(
        module_id=DEFAULT_MODULE_ID,
        module_version=DEFAULT_MODULE_VERSION,
        module_specification_version=ar.DEFAULT_MODULE_SPECIFICATION_VERSION,
        intake_contract_id=DEFAULT_INTAKE_CONTRACT_ID,
        intake_contract_version=DEFAULT_INTAKE_CONTRACT_VERSION,
        required_roles=required_roles,
        required_context_requirements=context_requirements,
        required_comparator_requirements=comparator_requirements,
        accepted_prepared_observation_readiness_states=accepted_states,
        accepted_temporal_alignment_states=temporal_states,
        accepted_missingness_conditions=missingness,
        conditional_readiness_policy=conditional_policy,
        output_contract_id=DEFAULT_HANDOFF_CONTRACT_ID,
    )


def _selected_package(
    fixture_id: str,
    *,
    include_context: bool = True,
    include_comparator: bool = True,
    conditional: bool = False,
    **overrides: Any,
) -> po.PreparedObservationResult:
    context = po._context(fixture_id, information_role=DEFAULT_REQUIRED_ROLE, required=True)
    comparator = po._comparator(fixture_id, information_role=DEFAULT_REQUIRED_ROLE, required=True)
    package_overrides: dict[str, Any] = {
        "context_attachments": (context,) if include_context else (),
        "comparator_attachments": (comparator,) if include_comparator else (),
        "required_context_ids": (context.context_id,) if include_context else (),
        "required_comparator_relationship_ids": (comparator.relationship_id,) if include_comparator else (),
    }
    if conditional:
        package_overrides["limitations"] = ("relationship conditionally governed",)
    package_overrides.update(overrides)
    return smi._po_result(fixture_id, **package_overrides)


def _selected_intake(
    fixture_id: str,
    *,
    include_context: bool = True,
    include_comparator: bool = True,
    conditional: bool = False,
    contract: smi.ModuleIntakeContract | None = None,
    package: po.PreparedObservationResult | None = None,
    **request_overrides: Any,
) -> smi.ScientificModuleIntakeResult:
    contract = contract or _selected_contract(
        required_context=include_context,
        required_comparator=include_comparator,
        conditional=conditional,
        target_only=not include_context and not include_comparator,
    )
    package = package or _selected_package(
        fixture_id,
        include_context=include_context,
        include_comparator=include_comparator,
        conditional=conditional,
    )
    request = smi._request(
        fixture_id,
        package=package,
        contract=contract,
        module=smi._module(contract),
        **request_overrides,
    )
    return smi.evaluate_scientific_module_intake(request)


def _authorized_execution_for_intake(
    intake: smi.ScientificModuleIntakeResult,
    *,
    execution_overrides: dict[str, Any] | None = None,
    declaration_overrides: dict[str, Any] | None = None,
    lineage_overrides: dict[str, Any] | None = None,
    adapter: ar.AdapterRegistration | None = None,
) -> tuple[ar.ActivationDeclaration, ar.ExecutionAuthorization]:
    declaration_values = {
        "requested_activation_state": ar.ModuleActivationState.MODULE_ACTIVE,
        "explicit_activation_authorized": True,
    }
    if declaration_overrides:
        declaration_values.update(declaration_overrides)
    declaration = ar.selected_activation_declaration(**declaration_values)
    registry = ar.registry_snapshot(declaration=declaration, adapter=adapter or ar.selected_adapter_registration())
    lineage_values = {
        "intake_evaluation_artifact": intake.intake_evaluation_id,
        "prepared_observation_artifact": intake.prepared_observation_package_id,
        "handoff_artifact": DEFAULT_HANDOFF_CONTRACT_ID,
    }
    if lineage_overrides:
        lineage_values.update(lineage_overrides)
    lineage = ar.ArtifactLineage(**lineage_values)
    reproducibility = ar.ReproducibilityMetadata(fixture_identifier=f"adapter_upstream_{intake.intake_evaluation_id}")
    activation = ar.evaluate_activation_readiness(declaration, registry, lineage=lineage, reproducibility=reproducibility)
    execution_values = {
        "explicit_execution_authorized": True,
        "intake_evaluation_id": intake.intake_evaluation_id,
        "prepared_observation_package_id": intake.prepared_observation_package_id,
        "handoff_contract_id": DEFAULT_HANDOFF_CONTRACT_ID,
        "intake_state": intake.compatibility_state.value,
    }
    if execution_overrides:
        execution_values.update(execution_overrides)
    execution = ar.evaluate_execution_authorization(
        activation,
        ar.execution_request(**execution_values),
        registry,
        lineage=lineage,
        reproducibility=reproducibility,
    )
    return declaration, execution


def _request(fixture_id: str, **overrides: Any) -> AdapterEvaluationRequest:
    intake = overrides.pop("intake_handoff", None) or _selected_intake(fixture_id)
    declaration, execution = _authorized_execution_for_intake(
        intake,
        execution_overrides=overrides.pop("execution_overrides", None),
        declaration_overrides=overrides.pop("declaration_overrides", None),
        lineage_overrides=overrides.pop("lineage_overrides", None),
        adapter=overrides.pop("activation_adapter", None),
    )
    values = {
        "execution_authorization": execution,
        "intake_handoff": intake,
        "activation_declaration": declaration,
        "adapter_registration": _adapter_registration(),
        "frozen_activation_specification": _frozen_specification(),
        "reproducibility_metadata": _repro(fixture_identifier=fixture_id),
        "fixture_id": fixture_id,
    }
    values.update(overrides)
    return AdapterEvaluationRequest(**values)


def _artifact_lineage(request: AdapterEvaluationRequest, frozen_input_id: str) -> dict[str, Any]:
    execution_lineage = request.execution_authorization.lineage_metadata.to_dict()
    intake_lineage = request.intake_handoff.artifact_lineage
    return {
        "activation_declaration_artifact": execution_lineage.get("activation_declaration_artifact", ""),
        "adapter_registration_artifact": request.adapter_registration.artifact_reference,
        "comparator_artifact": execution_lineage.get("comparator_artifact", ""),
        "comparator_construction_artifacts": list(intake_lineage.get("comparator_construction_artifacts", [])),
        "execution_authorization_artifact": execution_lineage.get("execution_authorization_artifact", ""),
        "frozen_activation_specification_artifact": request.frozen_activation_specification.frozen_activation_specification_id,
        "frozen_horizon_artifact": execution_lineage.get("frozen_horizon_artifact", ""),
        "frozen_module_input_artifact": frozen_input_id,
        "intake_contract_artifact": execution_lineage.get("intake_contract_artifact", ""),
        "intake_evaluation_artifact": intake_lineage.get("intake_evaluation_artifact", ""),
        "module_input_contract_artifact": execution_lineage.get("module_input_contract_artifact", ""),
        "module_registration_artifact": execution_lineage.get("module_registration_artifact", ""),
        "pit_artifact": execution_lineage.get("pit_artifact", ""),
        "pit_identity_context_artifacts": list(intake_lineage.get("pit_identity_context_artifacts", [])),
        "prepared_observation_artifact": intake_lineage.get("prepared_observation_artifact", ""),
        "scientific_execution_artifact": "",
        "scientific_output_artifact": "",
        "scientific_specification_artifact": execution_lineage.get("scientific_specification_artifact", ""),
        "source_authority_artifact": execution_lineage.get("source_authority_artifact", ""),
        "source_authority_artifacts": list(intake_lineage.get("source_authority_artifacts", [])),
    }


def _lineage_complete(lineage: dict[str, Any]) -> bool:
    required = (
        "source_authority_artifact",
        "pit_artifact",
        "comparator_artifact",
        "prepared_observation_artifact",
        "intake_contract_artifact",
        "intake_evaluation_artifact",
        "module_registration_artifact",
        "activation_declaration_artifact",
        "execution_authorization_artifact",
        "adapter_registration_artifact",
        "frozen_activation_specification_artifact",
        "module_input_contract_artifact",
        "scientific_specification_artifact",
        "frozen_horizon_artifact",
        "frozen_module_input_artifact",
    )
    return all(lineage.get(name) not in (None, "", (), [], {}) for name in required) and not lineage.get("scientific_execution_artifact") and not lineage.get("scientific_output_artifact")


def _identity_payload(request: AdapterEvaluationRequest) -> dict[str, str]:
    execution = request.execution_authorization
    return {
        "activation_id": execution.activation_reference,
        "adapter_id": request.adapter_registration.adapter_id,
        "adapter_version": request.adapter_registration.adapter_version,
        "execution_authorization_id": execution.execution_authorization_id,
        "frozen_activation_specification_version": request.frozen_activation_specification.frozen_activation_specification_version,
        "frozen_horizon_specification_version": request.frozen_activation_specification.frozen_horizon_specification_version,
        "handoff_contract_id": execution.handoff_reference,
        "intake_evaluation_id": request.intake_handoff.intake_evaluation_id,
        "module_input_contract_version": request.adapter_registration.module_input_contract_version,
        "prepared_observation_package_id": request.intake_handoff.prepared_observation_package_id,
        "scientific_specification_version": request.adapter_registration.scientific_specification_version,
    }


def deterministic_frozen_input_identity(request: AdapterEvaluationRequest) -> str:
    return "frozen_module_input_" + _stable_hash(_identity_payload(request))


def evaluate_selected_module_adapter(request: AdapterEvaluationRequest) -> FrozenModuleInputContract:
    diagnostics: list[AdapterDiagnostic] = []
    limitations = [
        "REFERENCE_IMPLEMENTATION_ONLY",
        "SYNTHETIC_ADAPTER_ONLY",
        "SYNTHETIC_AUTHORIZED_EXECUTION_ONLY",
        "REAL_ADAPTER_NOT_PLATFORM_INTEGRATED",
        "REAL_MODULE_EXECUTION_NOT_IMPLEMENTED",
    ]
    execution = request.execution_authorization
    intake = request.intake_handoff
    declaration = request.activation_declaration
    registration = request.adapter_registration
    spec = request.frozen_activation_specification
    repro = request.reproducibility_metadata

    if request.fixture_id.startswith("REAL"):
        limitations.append("REAL_SELECTED_MODULE_EXECUTION_BLOCKED_UPSTREAM")

    if execution.execution_authorization_state != ar.ExecutionAuthorizationState.EXECUTION_AUTHORIZED:
        diagnostics.append(_diag(AdapterDiagnosticCode.EXECUTION_NOT_AUTHORIZED, "execution", "Execution authorization is not EXECUTION_AUTHORIZED."))
    if request.direct_upstream_bypass:
        diagnostics.append(_diag(AdapterDiagnosticCode.DIRECT_UPSTREAM_BYPASS, "admission", "Direct upstream bypass is prohibited."))
    if request.raw_prepared_observation_bypass:
        diagnostics.append(_diag(AdapterDiagnosticCode.RAW_PREPARED_OBSERVATION_BYPASS, "admission", "Raw Prepared Observation bypass is prohibited."))

    if execution.activation_reference != declaration.activation_declaration_id:
        diagnostics.append(_diag(AdapterDiagnosticCode.ACTIVATION_REFERENCE_MISMATCH, "chain", "Execution activation reference does not match activation declaration."))
    if execution.intake_reference != intake.intake_evaluation_id:
        diagnostics.append(_diag(AdapterDiagnosticCode.INTAKE_EVALUATION_REFERENCE_MISMATCH, "chain", "Execution intake reference does not match intake handoff."))
    if execution.handoff_reference != registration.handoff_contract_id:
        diagnostics.append(_diag(AdapterDiagnosticCode.HANDOFF_REFERENCE_MISMATCH, "chain", "Execution handoff reference does not match adapter registration."))
    if intake.prepared_observation_package_id != _identity_payload(request)["prepared_observation_package_id"]:
        diagnostics.append(_diag(AdapterDiagnosticCode.PREPARED_OBSERVATION_REFERENCE_MISMATCH, "chain", "Prepared Observation reference is inconsistent."))
    if execution.input_contract_reference != registration.module_input_contract_id:
        diagnostics.append(_diag(AdapterDiagnosticCode.MODULE_INPUT_CONTRACT_REFERENCE_MISMATCH, "chain", "Execution input contract reference does not match adapter registration."))
    if execution.adapter_reference != registration.adapter_id:
        diagnostics.append(_diag(AdapterDiagnosticCode.ADAPTER_REFERENCE_MISMATCH, "chain", "Execution adapter reference does not match adapter registration."))

    if declaration.module_id != registration.module_id or intake.module_id != registration.module_id:
        diagnostics.append(_diag(AdapterDiagnosticCode.MODULE_REFERENCE_MISMATCH, "boundary", "Module reference mismatch."))
    if declaration.module_version != registration.module_version or intake.module_version != registration.module_version:
        diagnostics.append(_diag(AdapterDiagnosticCode.MODULE_REFERENCE_MISMATCH, "boundary", "Module version mismatch."))
    if registration.research_program_id != SELECTED_RESEARCH_PROGRAM_ID or declaration.research_program_id != SELECTED_RESEARCH_PROGRAM_ID or spec.research_program_id != SELECTED_RESEARCH_PROGRAM_ID:
        diagnostics.append(_diag(AdapterDiagnosticCode.RESEARCH_PROGRAM_REFERENCE_MISMATCH, "boundary", "Research program reference mismatch."))
    if (
        registration.activation_specification_id != NARROW_ACTIVATION_SPECIFICATION_ID
        or declaration.activation_specification_id != NARROW_ACTIVATION_SPECIFICATION_ID
        or spec.narrow_activation_specification_id != NARROW_ACTIVATION_SPECIFICATION_ID
        or spec.frozen_activation_specification_id != NARROW_ACTIVATION_SPECIFICATION_ID
    ):
        diagnostics.append(_diag(AdapterDiagnosticCode.ACTIVATION_SPECIFICATION_REFERENCE_MISMATCH, "boundary", "Narrow activation specification mismatch."))
    if execution.scientific_specification_reference != registration.scientific_specification_id or registration.scientific_specification_id != DEFAULT_SCIENTIFIC_SPECIFICATION_ID:
        diagnostics.append(_diag(AdapterDiagnosticCode.SCIENTIFIC_SPECIFICATION_REFERENCE_MISMATCH, "specification", "Scientific specification reference mismatch."))
    if execution.frozen_horizon_reference != registration.frozen_horizon_specification_id or spec.frozen_horizon_specification_id != registration.frozen_horizon_specification_id:
        diagnostics.append(_diag(AdapterDiagnosticCode.FROZEN_HORIZON_REFERENCE_MISMATCH, "horizon", "Frozen horizon reference mismatch."))

    if registration.scientific_transformation_permitted:
        diagnostics.append(_diag(AdapterDiagnosticCode.SCIENTIFIC_TRANSFORMATION_PROHIBITED, "adapter", "Adapter scientific transformation is prohibited."))
    if registration.adapter_version != DEFAULT_ADAPTER_VERSION:
        diagnostics.append(_diag(AdapterDiagnosticCode.ADAPTER_VERSION_INCOMPATIBLE, "version", "Adapter version is incompatible."))
    if registration.handoff_contract_version != DEFAULT_HANDOFF_CONTRACT_VERSION:
        diagnostics.append(_diag(AdapterDiagnosticCode.HANDOFF_CONTRACT_VERSION_INCOMPATIBLE, "version", "Handoff contract version is incompatible."))
    if registration.module_input_contract_version != DEFAULT_MODULE_INPUT_CONTRACT_VERSION or spec.module_input_contract_version != DEFAULT_MODULE_INPUT_CONTRACT_VERSION:
        diagnostics.append(_diag(AdapterDiagnosticCode.MODULE_INPUT_CONTRACT_VERSION_INCOMPATIBLE, "version", "Module input contract version is incompatible."))
    if registration.scientific_specification_version != DEFAULT_SCIENTIFIC_SPECIFICATION_VERSION:
        diagnostics.append(_diag(AdapterDiagnosticCode.SCIENTIFIC_SPECIFICATION_VERSION_INCOMPATIBLE, "version", "Scientific specification version is incompatible."))
    if spec.frozen_activation_specification_version != NARROW_ACTIVATION_SPECIFICATION_VERSION:
        diagnostics.append(_diag(AdapterDiagnosticCode.FROZEN_ACTIVATION_SPECIFICATION_VERSION_INCOMPATIBLE, "version", "Frozen activation specification version is incompatible."))
    if registration.frozen_horizon_specification_version != DEFAULT_FROZEN_HORIZON_SPECIFICATION_VERSION or spec.frozen_horizon_specification_version != DEFAULT_FROZEN_HORIZON_SPECIFICATION_VERSION:
        diagnostics.append(_diag(AdapterDiagnosticCode.FROZEN_HORIZON_VERSION_INCOMPATIBLE, "version", "Frozen horizon version is incompatible."))
    if registration.information_role_schema_version != DEFAULT_INFORMATION_ROLE_SCHEMA_VERSION or repro.information_role_schema_version != DEFAULT_INFORMATION_ROLE_SCHEMA_VERSION:
        diagnostics.append(_diag(AdapterDiagnosticCode.INFORMATION_ROLE_SCHEMA_VERSION_INCOMPATIBLE, "version", "Information-role schema version is incompatible."))
    if registration.diagnostic_schema_version != DEFAULT_DIAGNOSTIC_SCHEMA_VERSION or spec.diagnostic_schema_version != DEFAULT_DIAGNOSTIC_SCHEMA_VERSION or repro.diagnostic_schema_version != DEFAULT_DIAGNOSTIC_SCHEMA_VERSION:
        diagnostics.append(_diag(AdapterDiagnosticCode.DIAGNOSTIC_SCHEMA_VERSION_INCOMPATIBLE, "version", "Diagnostic schema version is incompatible."))
    if registration.artifact_lineage_schema_version != DEFAULT_ARTIFACT_LINEAGE_SCHEMA_VERSION or spec.lineage_schema_version != DEFAULT_ARTIFACT_LINEAGE_SCHEMA_VERSION or repro.lineage_schema_version != DEFAULT_ARTIFACT_LINEAGE_SCHEMA_VERSION:
        diagnostics.append(_diag(AdapterDiagnosticCode.LINEAGE_SCHEMA_VERSION_INCOMPATIBLE, "version", "Lineage schema version is incompatible."))
    if registration.reproducibility_schema_version != DEFAULT_REPRODUCIBILITY_SCHEMA_VERSION or spec.reproducibility_schema_version != DEFAULT_REPRODUCIBILITY_SCHEMA_VERSION or repro.reproducibility_schema_version != DEFAULT_REPRODUCIBILITY_SCHEMA_VERSION:
        diagnostics.append(_diag(AdapterDiagnosticCode.REPRODUCIBILITY_SCHEMA_VERSION_INCOMPATIBLE, "version", "Reproducibility schema version is incompatible."))

    role_values = tuple(binding.get("information_role", "") for binding in intake.role_bindings) + (
        intake.information_contract.accepted_target_observation_metadata.get("observation_role", ""),
    )
    if DEFAULT_REQUIRED_ROLE not in role_values:
        diagnostics.append(_diag(AdapterDiagnosticCode.REQUIRED_INFORMATION_ROLE_MISSING, "role", "Required decomposition information role is missing."))
    if any(role in spec.prohibited_information_roles for role in role_values):
        diagnostics.append(_diag(AdapterDiagnosticCode.PROHIBITED_INFORMATION_ROLE, "role", "Prohibited information role is present."))
    if not request.target_mapping_complete or not intake.information_contract.accepted_target_observation_metadata:
        diagnostics.append(_diag(AdapterDiagnosticCode.TARGET_MAPPING_INCOMPLETE, "mapping", "Target mapping is incomplete."))
    if not request.context_mapping_complete:
        diagnostics.append(_diag(AdapterDiagnosticCode.CONTEXT_MAPPING_INCOMPLETE, "mapping", "Context mapping is incomplete."))
    if not request.comparator_mapping_complete:
        diagnostics.append(_diag(AdapterDiagnosticCode.COMPARATOR_MAPPING_INCOMPLETE, "mapping", "Comparator mapping is incomplete."))
    if intake.temporal_compatibility.get("temporal_alignment_state") not in {
        po.TemporalAlignmentState.FULLY_ALIGNED.value,
        po.TemporalAlignmentState.PARTIALLY_ALIGNED.value,
    }:
        diagnostics.append(_diag(AdapterDiagnosticCode.TEMPORAL_METADATA_INCOMPATIBLE, "temporal", "Temporal metadata is incompatible."))
    required_coverage_values = (
        value
        for name, value in intake.coverage_compatibility.items()
        if isinstance(value, bool) and name != "conditionally_governed"
    )
    if not all(bool(value) for value in required_coverage_values):
        diagnostics.append(_diag(AdapterDiagnosticCode.INSUFFICIENT_MAPPING_COVERAGE, "coverage", "Mapping coverage is insufficient."))
    if any(value for name, value in intake.missingness_compatibility.items() if name != "optional_field_missing"):
        diagnostics.append(_diag(AdapterDiagnosticCode.UNACCEPTABLE_MAPPING_MISSINGNESS, "missingness", "Required mapping missingness is unacceptable."))

    frozen_input_id = deterministic_frozen_input_identity(request)
    lineage = _artifact_lineage(request, frozen_input_id)
    if not _lineage_complete(lineage):
        diagnostics.append(_diag(AdapterDiagnosticCode.ADAPTER_LINEAGE_INCOMPLETE, "lineage", "Adapter artifact lineage is incomplete."))
    if not repro.complete():
        diagnostics.append(_diag(AdapterDiagnosticCode.ADAPTER_REPRODUCIBILITY_INCOMPLETE, "reproducibility", "Adapter reproducibility metadata is incomplete."))

    diagnostics_tuple = _dedupe_diagnostics(diagnostics)
    limitations_tuple = _dedupe_strings(limitations + list(execution.authorization_limitations) + list(intake.intake_limitations))
    adapter_state = _classify_adapter_state(diagnostics_tuple, limitations_tuple, execution.execution_authorization_state, intake.compatibility_state)
    frozen_state = _classify_frozen_state(adapter_state)
    adapter_evaluation_id = "selected_module_adapter_eval_" + _stable_hash(
        {
            "diagnostics": [diag.to_dict() for diag in diagnostics_tuple],
            "frozen_input_id": frozen_input_id,
            "state": adapter_state.value,
        }
    )
    information_contract = _information_contract(request, adapter_state, frozen_state)
    return FrozenModuleInputContract(
        frozen_module_input_id=frozen_input_id,
        adapter_evaluation_id=adapter_evaluation_id,
        adapter_state=adapter_state,
        frozen_module_input_state=frozen_state,
        execution_authorization_id=execution.execution_authorization_id,
        execution_authorization_state=execution.execution_authorization_state.value,
        activation_id=execution.activation_reference,
        module_id=registration.module_id,
        module_version=registration.module_version,
        research_program_id=registration.research_program_id,
        activation_specification_id=registration.activation_specification_id,
        activation_specification_version=registration.activation_specification_version,
        intake_evaluation_id=intake.intake_evaluation_id,
        prepared_observation_package_id=intake.prepared_observation_package_id,
        handoff_contract_id=registration.handoff_contract_id,
        adapter_id=registration.adapter_id,
        adapter_version=registration.adapter_version,
        module_input_contract_id=registration.module_input_contract_id,
        module_input_contract_version=registration.module_input_contract_version,
        scientific_specification_id=registration.scientific_specification_id,
        scientific_specification_version=registration.scientific_specification_version,
        frozen_horizon_specification_id=registration.frozen_horizon_specification_id,
        frozen_horizon_specification_version=registration.frozen_horizon_specification_version,
        target_observation_metadata=intake.information_contract.accepted_target_observation_metadata,
        context_attachments=tuple(intake.context_bindings),
        comparator_attachments=tuple(intake.comparator_bindings),
        information_role_bindings=tuple(intake.role_bindings),
        observation_time_metadata=intake.information_contract.observation_time_metadata,
        temporal_metadata=intake.temporal_compatibility,
        coverage_metadata=intake.coverage_compatibility,
        missingness_metadata=intake.missingness_compatibility,
        inherited_diagnostics=tuple(diag.to_dict() for diag in intake.inherited_diagnostics) + tuple(diag.to_dict() for diag in intake.intake_diagnostics),
        inherited_limitations=tuple(intake.inherited_limitations) + tuple(intake.intake_limitations),
        adapter_diagnostics=diagnostics_tuple,
        adapter_limitations=limitations_tuple,
        artifact_lineage=lineage,
        reproducibility_metadata=repro.to_dict(),
        governing_versions={**_base_governing_versions(), **registration.governing_versions, **spec.governing_versions},
        information_contract=information_contract,
    )


def _classify_adapter_state(
    diagnostics: tuple[AdapterDiagnostic, ...],
    limitations: tuple[str, ...],
    execution_state: ar.ExecutionAuthorizationState,
    intake_state: smi.IntakeCompatibilityState,
) -> SelectedModuleAdapterState:
    codes = {diag.code for diag in diagnostics}
    if codes & {
        AdapterDiagnosticCode.DIRECT_UPSTREAM_BYPASS,
        AdapterDiagnosticCode.RAW_PREPARED_OBSERVATION_BYPASS,
        AdapterDiagnosticCode.RESEARCH_PROGRAM_REFERENCE_MISMATCH,
        AdapterDiagnosticCode.ACTIVATION_SPECIFICATION_REFERENCE_MISMATCH,
    }:
        return SelectedModuleAdapterState.EXCLUDED
    if execution_state == ar.ExecutionAuthorizationState.EXECUTION_EXCLUDED or intake_state == smi.IntakeCompatibilityState.EXCLUDED:
        return SelectedModuleAdapterState.EXCLUDED
    if execution_state == ar.ExecutionAuthorizationState.EXECUTION_UNRESOLVED or intake_state == smi.IntakeCompatibilityState.UNRESOLVED:
        return SelectedModuleAdapterState.UNRESOLVED
    if execution_state == ar.ExecutionAuthorizationState.INSUFFICIENT_EXECUTION_AUTHORIZATION_EVIDENCE or intake_state == smi.IntakeCompatibilityState.INSUFFICIENT_EVIDENCE:
        return SelectedModuleAdapterState.INSUFFICIENT_EVIDENCE
    if codes & {
        AdapterDiagnosticCode.EXECUTION_NOT_AUTHORIZED,
        AdapterDiagnosticCode.ACTIVATION_REFERENCE_MISMATCH,
        AdapterDiagnosticCode.INTAKE_EVALUATION_REFERENCE_MISMATCH,
        AdapterDiagnosticCode.PREPARED_OBSERVATION_REFERENCE_MISMATCH,
        AdapterDiagnosticCode.HANDOFF_REFERENCE_MISMATCH,
        AdapterDiagnosticCode.ADAPTER_REFERENCE_MISMATCH,
        AdapterDiagnosticCode.MODULE_REFERENCE_MISMATCH,
        AdapterDiagnosticCode.MODULE_INPUT_CONTRACT_REFERENCE_MISMATCH,
        AdapterDiagnosticCode.SCIENTIFIC_SPECIFICATION_REFERENCE_MISMATCH,
        AdapterDiagnosticCode.FROZEN_HORIZON_REFERENCE_MISMATCH,
        AdapterDiagnosticCode.SCIENTIFIC_TRANSFORMATION_PROHIBITED,
        AdapterDiagnosticCode.ADAPTER_VERSION_INCOMPATIBLE,
        AdapterDiagnosticCode.HANDOFF_CONTRACT_VERSION_INCOMPATIBLE,
        AdapterDiagnosticCode.MODULE_INPUT_CONTRACT_VERSION_INCOMPATIBLE,
        AdapterDiagnosticCode.SCIENTIFIC_SPECIFICATION_VERSION_INCOMPATIBLE,
        AdapterDiagnosticCode.FROZEN_ACTIVATION_SPECIFICATION_VERSION_INCOMPATIBLE,
        AdapterDiagnosticCode.FROZEN_HORIZON_VERSION_INCOMPATIBLE,
        AdapterDiagnosticCode.INFORMATION_ROLE_SCHEMA_VERSION_INCOMPATIBLE,
        AdapterDiagnosticCode.DIAGNOSTIC_SCHEMA_VERSION_INCOMPATIBLE,
        AdapterDiagnosticCode.LINEAGE_SCHEMA_VERSION_INCOMPATIBLE,
        AdapterDiagnosticCode.REPRODUCIBILITY_SCHEMA_VERSION_INCOMPATIBLE,
        AdapterDiagnosticCode.ADAPTER_LINEAGE_INCOMPLETE,
        AdapterDiagnosticCode.ADAPTER_REPRODUCIBILITY_INCOMPLETE,
        AdapterDiagnosticCode.PROHIBITED_INFORMATION_ROLE,
        AdapterDiagnosticCode.REQUIRED_INFORMATION_ROLE_MISSING,
        AdapterDiagnosticCode.TARGET_MAPPING_INCOMPLETE,
        AdapterDiagnosticCode.CONTEXT_MAPPING_INCOMPLETE,
        AdapterDiagnosticCode.COMPARATOR_MAPPING_INCOMPLETE,
        AdapterDiagnosticCode.TEMPORAL_METADATA_INCOMPATIBLE,
        AdapterDiagnosticCode.UNACCEPTABLE_MAPPING_MISSINGNESS,
    }:
        return SelectedModuleAdapterState.INCOMPATIBLE
    if AdapterDiagnosticCode.INSUFFICIENT_MAPPING_COVERAGE in codes:
        return SelectedModuleAdapterState.INSUFFICIENT_EVIDENCE
    if execution_state == ar.ExecutionAuthorizationState.EXECUTION_CONDITIONALLY_AUTHORIZED or intake_state == smi.IntakeCompatibilityState.CONDITIONALLY_COMPATIBLE:
        return SelectedModuleAdapterState.CONDITIONALLY_COMPATIBLE
    return SelectedModuleAdapterState.COMPATIBLE


def _classify_frozen_state(adapter_state: SelectedModuleAdapterState) -> FrozenModuleInputState:
    return {
        SelectedModuleAdapterState.COMPATIBLE: FrozenModuleInputState.READY,
        SelectedModuleAdapterState.CONDITIONALLY_COMPATIBLE: FrozenModuleInputState.CONDITIONALLY_READY,
        SelectedModuleAdapterState.UNRESOLVED: FrozenModuleInputState.UNRESOLVED,
        SelectedModuleAdapterState.INCOMPATIBLE: FrozenModuleInputState.INCOMPLETE,
        SelectedModuleAdapterState.EXCLUDED: FrozenModuleInputState.EXCLUDED,
        SelectedModuleAdapterState.INSUFFICIENT_EVIDENCE: FrozenModuleInputState.INSUFFICIENT_EVIDENCE,
    }[adapter_state]


def _information_contract(
    request: AdapterEvaluationRequest,
    adapter_state: SelectedModuleAdapterState,
    frozen_state: FrozenModuleInputState,
) -> dict[str, Any]:
    contract = {
        "adapter_state": adapter_state.value,
        "frozen_module_input_state": frozen_state.value,
        "metadata_only": True,
        "structural_mapping_only": True,
        "scientific_transformation_permitted": False,
        "target_observation_metadata_preserved": True,
        "context_metadata_preserved": True,
        "comparator_metadata_preserved": True,
        "role_bindings_preserved": True,
        "temporal_metadata_preserved": True,
        "diagnostics_preserved": True,
        "limitations_preserved": True,
        "lineage_preserved": True,
        "reproducibility_preserved": True,
        "requester_metadata_ignored_for_identity": bool(request.requester_metadata),
    }
    for flag in PROHIBITED_INFORMATION_CONTRACT_FLAGS:
        contract[flag] = False
    return contract


def canonical_selected_module_adapter_fixtures() -> tuple[SelectedModuleAdapterFixture, ...]:
    fixtures: list[SelectedModuleAdapterFixture] = []

    def add(
        fixture_id: str,
        description: str,
        request: AdapterEvaluationRequest,
        adapter_state: SelectedModuleAdapterState,
        frozen_state: FrozenModuleInputState,
        codes: tuple[AdapterDiagnosticCode, ...] = (),
        limitations: tuple[str, ...] = (),
    ) -> None:
        fixtures.append(SelectedModuleAdapterFixture(fixture_id, description, request, adapter_state, frozen_state, codes, limitations))

    target_only_pkg = _selected_package(
        "AD01_valid_target_only",
        include_context=False,
        include_comparator=False,
        target_observation=po.TargetObservationMetadata(
            "synthetic_target",
            ("target_interval_AD01_valid_target_only",),
            "target_interval_AD01_valid_target_only",
            observation_role=DEFAULT_REQUIRED_ROLE,
        ),
    )
    target_only_contract = _selected_contract(required_context=False, required_comparator=False, target_only=True)
    target_only_contract = smi._contract(**{**target_only_contract.__dict__, "required_target_observation_types": (DEFAULT_REQUIRED_ROLE,)})
    add("AD01_valid_target_only", "Valid target-only synthetic mapping.", _request("AD01_valid_target_only", intake_handoff=_selected_intake("AD01_valid_target_only", include_context=False, include_comparator=False, package=target_only_pkg, contract=target_only_contract)), SelectedModuleAdapterState.COMPATIBLE, FrozenModuleInputState.READY)
    add("AD02_valid_target_comparator", "Valid target plus comparator.", _request("AD02_valid_target_comparator", intake_handoff=_selected_intake("AD02_valid_target_comparator", include_context=False, include_comparator=True)), SelectedModuleAdapterState.COMPATIBLE, FrozenModuleInputState.READY)
    add("AD03_valid_target_context", "Valid target plus context.", _request("AD03_valid_target_context", intake_handoff=_selected_intake("AD03_valid_target_context", include_context=True, include_comparator=False)), SelectedModuleAdapterState.COMPATIBLE, FrozenModuleInputState.READY)
    add("AD04_valid_target_context_comparator", "Valid target plus context and comparator.", _request("AD04_valid_target_context_comparator"), SelectedModuleAdapterState.COMPATIBLE, FrozenModuleInputState.READY)
    add("AD05_alternate_valid_handoff", "Alternate valid synthetic handoff.", _request("AD05_alternate_valid_handoff"), SelectedModuleAdapterState.COMPATIBLE, FrozenModuleInputState.READY)
    add("AD06_deterministic_repeat", "Deterministic repeat.", _request("AD06_deterministic_repeat"), SelectedModuleAdapterState.COMPATIBLE, FrozenModuleInputState.READY)
    add("AD07_accepted_conditional", "Accepted conditional mapping.", _request("AD07_accepted_conditional", intake_handoff=_selected_intake("AD07_accepted_conditional", conditional=True)), SelectedModuleAdapterState.CONDITIONALLY_COMPATIBLE, FrozenModuleInputState.CONDITIONALLY_READY)

    real_activation, real_execution = ar.real_selected_module_blocked_result()
    real_intake = _selected_intake("REAL_selected_module_blocked")
    add("AD08_real_selected_module_blocked", "Real selected module remains blocked upstream.", AdapterEvaluationRequest(real_execution, real_intake, real_activation.activation_declaration, fixture_id="REAL_selected_module_blocked"), SelectedModuleAdapterState.INCOMPATIBLE, FrozenModuleInputState.INCOMPLETE, (AdapterDiagnosticCode.EXECUTION_NOT_AUTHORIZED,), ("REAL_SELECTED_MODULE_EXECUTION_BLOCKED_UPSTREAM",))
    add("AD09_execution_blocked", "Execution blocked.", _request("AD09_execution_blocked", execution_overrides={"explicit_execution_authorized": False}), SelectedModuleAdapterState.INCOMPATIBLE, FrozenModuleInputState.INCOMPLETE, (AdapterDiagnosticCode.EXECUTION_NOT_AUTHORIZED,))
    add("AD10_execution_unresolved", "Execution unresolved.", _request("AD10_execution_unresolved", execution_overrides={"unresolved_authorization": True}), SelectedModuleAdapterState.UNRESOLVED, FrozenModuleInputState.UNRESOLVED, (AdapterDiagnosticCode.EXECUTION_NOT_AUTHORIZED,))
    retired_decl = ar.selected_activation_declaration(requested_activation_state=ar.ModuleActivationState.MODULE_ACTIVE, explicit_activation_authorized=True)
    add("AD11_execution_excluded", "Execution excluded.", _request("AD11_execution_excluded", declaration_overrides={"requested_activation_state": ar.ModuleActivationState.MODULE_RETIRED}), SelectedModuleAdapterState.INCOMPATIBLE, FrozenModuleInputState.INCOMPLETE, (AdapterDiagnosticCode.EXECUTION_NOT_AUTHORIZED,))
    add("AD12_execution_insufficient", "Execution insufficient evidence.", _request("AD12_execution_insufficient", execution_overrides={"insufficient_authorization_evidence": True}), SelectedModuleAdapterState.INSUFFICIENT_EVIDENCE, FrozenModuleInputState.INSUFFICIENT_EVIDENCE, (AdapterDiagnosticCode.EXECUTION_NOT_AUTHORIZED,))

    add("AD13_wrong_activation_id", "Wrong activation id.", _request("AD13_wrong_activation_id", execution_overrides={"activation_id": "wrong_activation"}), SelectedModuleAdapterState.INCOMPATIBLE, FrozenModuleInputState.INCOMPLETE, (AdapterDiagnosticCode.EXECUTION_NOT_AUTHORIZED, AdapterDiagnosticCode.ACTIVATION_REFERENCE_MISMATCH))
    add("AD14_wrong_intake_id", "Wrong intake id.", _request("AD14_wrong_intake_id", execution_overrides={"intake_evaluation_id": "wrong_intake"}), SelectedModuleAdapterState.INCOMPATIBLE, FrozenModuleInputState.INCOMPLETE, (AdapterDiagnosticCode.EXECUTION_NOT_AUTHORIZED, AdapterDiagnosticCode.INTAKE_EVALUATION_REFERENCE_MISMATCH))
    add("AD15_wrong_package_id", "Wrong Prepared Observation id.", _request("AD15_wrong_package_id", execution_overrides={"prepared_observation_package_id": "wrong_package"}), SelectedModuleAdapterState.INCOMPATIBLE, FrozenModuleInputState.INCOMPLETE, (AdapterDiagnosticCode.EXECUTION_NOT_AUTHORIZED,))
    add("AD16_wrong_handoff_id", "Wrong handoff id.", _request("AD16_wrong_handoff_id", execution_overrides={"handoff_contract_id": "wrong_handoff"}), SelectedModuleAdapterState.INCOMPATIBLE, FrozenModuleInputState.INCOMPLETE, (AdapterDiagnosticCode.EXECUTION_NOT_AUTHORIZED, AdapterDiagnosticCode.HANDOFF_REFERENCE_MISMATCH))
    add("AD17_wrong_adapter_id", "Wrong adapter id.", _request("AD17_wrong_adapter_id", adapter_registration=_adapter_registration(adapter_id="wrong_adapter")), SelectedModuleAdapterState.INCOMPATIBLE, FrozenModuleInputState.INCOMPLETE, (AdapterDiagnosticCode.ADAPTER_REFERENCE_MISMATCH,))
    add("AD18_wrong_module_id", "Wrong module id.", _request("AD18_wrong_module_id", adapter_registration=_adapter_registration(module_id="wrong_module")), SelectedModuleAdapterState.INCOMPATIBLE, FrozenModuleInputState.INCOMPLETE, (AdapterDiagnosticCode.MODULE_REFERENCE_MISMATCH,))
    add("AD19_wrong_module_version", "Wrong module version.", _request("AD19_wrong_module_version", adapter_registration=_adapter_registration(module_version="v2")), SelectedModuleAdapterState.INCOMPATIBLE, FrozenModuleInputState.INCOMPLETE, (AdapterDiagnosticCode.MODULE_REFERENCE_MISMATCH,))
    add("AD20_wrong_activation_spec", "Wrong activation specification.", _request("AD20_wrong_activation_spec", adapter_registration=_adapter_registration(activation_specification_id=SELECTED_RESEARCH_PROGRAM_ID)), SelectedModuleAdapterState.EXCLUDED, FrozenModuleInputState.EXCLUDED, (AdapterDiagnosticCode.ACTIVATION_SPECIFICATION_REFERENCE_MISMATCH,))
    add("AD21_wrong_scientific_spec", "Wrong scientific specification.", _request("AD21_wrong_scientific_spec", adapter_registration=_adapter_registration(scientific_specification_id="wrong_spec")), SelectedModuleAdapterState.INCOMPATIBLE, FrozenModuleInputState.INCOMPLETE, (AdapterDiagnosticCode.SCIENTIFIC_SPECIFICATION_REFERENCE_MISMATCH,))
    add("AD22_wrong_frozen_horizon", "Wrong frozen horizon.", _request("AD22_wrong_frozen_horizon", adapter_registration=_adapter_registration(frozen_horizon_specification_id="wrong_horizon")), SelectedModuleAdapterState.INCOMPATIBLE, FrozenModuleInputState.INCOMPLETE, (AdapterDiagnosticCode.FROZEN_HORIZON_REFERENCE_MISMATCH,))
    add("AD23_wrong_input_contract", "Wrong module input contract.", _request("AD23_wrong_input_contract", adapter_registration=_adapter_registration(module_input_contract_id="wrong_input_contract")), SelectedModuleAdapterState.INCOMPATIBLE, FrozenModuleInputState.INCOMPLETE, (AdapterDiagnosticCode.MODULE_INPUT_CONTRACT_REFERENCE_MISMATCH,))

    add("AD24_adapter_version_mismatch", "Adapter version mismatch.", _request("AD24_adapter_version_mismatch", adapter_registration=_adapter_registration(adapter_version="v2")), SelectedModuleAdapterState.INCOMPATIBLE, FrozenModuleInputState.INCOMPLETE, (AdapterDiagnosticCode.ADAPTER_VERSION_INCOMPATIBLE,))
    add("AD25_handoff_version_mismatch", "Handoff version mismatch.", _request("AD25_handoff_version_mismatch", adapter_registration=_adapter_registration(handoff_contract_version="v2")), SelectedModuleAdapterState.INCOMPATIBLE, FrozenModuleInputState.INCOMPLETE, (AdapterDiagnosticCode.HANDOFF_CONTRACT_VERSION_INCOMPATIBLE,))
    add("AD26_input_contract_version_mismatch", "Input contract version mismatch.", _request("AD26_input_contract_version_mismatch", adapter_registration=_adapter_registration(module_input_contract_version="v2")), SelectedModuleAdapterState.INCOMPATIBLE, FrozenModuleInputState.INCOMPLETE, (AdapterDiagnosticCode.MODULE_INPUT_CONTRACT_VERSION_INCOMPATIBLE,))
    add("AD27_scientific_spec_version_mismatch", "Scientific spec version mismatch.", _request("AD27_scientific_spec_version_mismatch", adapter_registration=_adapter_registration(scientific_specification_version="v2")), SelectedModuleAdapterState.INCOMPATIBLE, FrozenModuleInputState.INCOMPLETE, (AdapterDiagnosticCode.SCIENTIFIC_SPECIFICATION_VERSION_INCOMPATIBLE,))
    add("AD28_frozen_activation_version_mismatch", "Frozen activation spec version mismatch.", _request("AD28_frozen_activation_version_mismatch", frozen_activation_specification=_frozen_specification(frozen_activation_specification_version="v2")), SelectedModuleAdapterState.INCOMPATIBLE, FrozenModuleInputState.INCOMPLETE, (AdapterDiagnosticCode.FROZEN_ACTIVATION_SPECIFICATION_VERSION_INCOMPATIBLE,))
    add("AD29_frozen_horizon_version_mismatch", "Frozen horizon version mismatch.", _request("AD29_frozen_horizon_version_mismatch", adapter_registration=_adapter_registration(frozen_horizon_specification_version="v2")), SelectedModuleAdapterState.INCOMPATIBLE, FrozenModuleInputState.INCOMPLETE, (AdapterDiagnosticCode.FROZEN_HORIZON_VERSION_INCOMPATIBLE,))
    add("AD30_role_schema_mismatch", "Role schema mismatch.", _request("AD30_role_schema_mismatch", adapter_registration=_adapter_registration(information_role_schema_version="other")), SelectedModuleAdapterState.INCOMPATIBLE, FrozenModuleInputState.INCOMPLETE, (AdapterDiagnosticCode.INFORMATION_ROLE_SCHEMA_VERSION_INCOMPATIBLE,))
    add("AD31_diagnostic_schema_mismatch", "Diagnostic schema mismatch.", _request("AD31_diagnostic_schema_mismatch", adapter_registration=_adapter_registration(diagnostic_schema_version="other")), SelectedModuleAdapterState.INCOMPATIBLE, FrozenModuleInputState.INCOMPLETE, (AdapterDiagnosticCode.DIAGNOSTIC_SCHEMA_VERSION_INCOMPATIBLE,))
    add("AD32_lineage_schema_mismatch", "Lineage schema mismatch.", _request("AD32_lineage_schema_mismatch", adapter_registration=_adapter_registration(artifact_lineage_schema_version="other")), SelectedModuleAdapterState.INCOMPATIBLE, FrozenModuleInputState.INCOMPLETE, (AdapterDiagnosticCode.LINEAGE_SCHEMA_VERSION_INCOMPATIBLE,))
    add("AD33_repro_schema_mismatch", "Repro schema mismatch.", _request("AD33_repro_schema_mismatch", adapter_registration=_adapter_registration(reproducibility_schema_version="other")), SelectedModuleAdapterState.INCOMPATIBLE, FrozenModuleInputState.INCOMPLETE, (AdapterDiagnosticCode.REPRODUCIBILITY_SCHEMA_VERSION_INCOMPATIBLE,))

    prohibited_pkg = _selected_package("AD34_prohibited_role", context_attachments=(po._context("AD34_prohibited_role", information_role=po.InformationRole.DIAGNOSTIC_INFORMATION.value),), comparator_attachments=(), required_comparator_relationship_ids=())
    add("AD34_prohibited_role", "Prohibited role.", _request("AD34_prohibited_role", intake_handoff=_selected_intake("AD34_prohibited_role", package=prohibited_pkg, contract=_selected_contract(required_comparator=False))), SelectedModuleAdapterState.INCOMPATIBLE, FrozenModuleInputState.INCOMPLETE, (AdapterDiagnosticCode.PROHIBITED_INFORMATION_ROLE, AdapterDiagnosticCode.REQUIRED_INFORMATION_ROLE_MISSING))
    missing_role_pkg = _selected_package("AD35_missing_required_role", context_attachments=(), comparator_attachments=(), required_context_ids=(), required_comparator_relationship_ids=())
    add("AD35_missing_required_role", "Missing required role.", _request("AD35_missing_required_role", intake_handoff=_selected_intake("AD35_missing_required_role", package=missing_role_pkg, contract=_selected_contract(target_only=True, required_context=False, required_comparator=False))), SelectedModuleAdapterState.INCOMPATIBLE, FrozenModuleInputState.INCOMPLETE, (AdapterDiagnosticCode.REQUIRED_INFORMATION_ROLE_MISSING,))
    add("AD36_target_mapping_incomplete", "Target mapping incomplete.", _request("AD36_target_mapping_incomplete", target_mapping_complete=False), SelectedModuleAdapterState.INCOMPATIBLE, FrozenModuleInputState.INCOMPLETE, (AdapterDiagnosticCode.TARGET_MAPPING_INCOMPLETE,))
    add("AD37_context_mapping_incomplete", "Context mapping incomplete.", _request("AD37_context_mapping_incomplete", context_mapping_complete=False), SelectedModuleAdapterState.INCOMPATIBLE, FrozenModuleInputState.INCOMPLETE, (AdapterDiagnosticCode.CONTEXT_MAPPING_INCOMPLETE,))
    add("AD38_comparator_mapping_incomplete", "Comparator mapping incomplete.", _request("AD38_comparator_mapping_incomplete", comparator_mapping_complete=False), SelectedModuleAdapterState.INCOMPATIBLE, FrozenModuleInputState.INCOMPLETE, (AdapterDiagnosticCode.COMPARATOR_MAPPING_INCOMPLETE,))
    add("AD39_role_binding_mismatch", "Role binding mismatch.", _request("AD39_role_binding_mismatch", adapter_registration=_adapter_registration()), SelectedModuleAdapterState.COMPATIBLE, FrozenModuleInputState.READY)

    add("AD40_lineage_incomplete", "Lineage incomplete.", _request("AD40_lineage_incomplete", lineage_overrides={"source_authority_artifact": ""}), SelectedModuleAdapterState.INCOMPATIBLE, FrozenModuleInputState.INCOMPLETE, (AdapterDiagnosticCode.EXECUTION_NOT_AUTHORIZED, AdapterDiagnosticCode.ADAPTER_LINEAGE_INCOMPLETE))
    add("AD41_reproducibility_incomplete", "Reproducibility incomplete.", _request("AD41_reproducibility_incomplete", reproducibility_metadata=_repro(controlled_reference=False)), SelectedModuleAdapterState.INCOMPATIBLE, FrozenModuleInputState.INCOMPLETE, (AdapterDiagnosticCode.ADAPTER_REPRODUCIBILITY_INCOMPLETE,))
    add("AD42_scientific_transformation_enabled", "Scientific transformation enabled.", _request("AD42_scientific_transformation_enabled", adapter_registration=_adapter_registration(scientific_transformation_permitted=True)), SelectedModuleAdapterState.INCOMPATIBLE, FrozenModuleInputState.INCOMPLETE, (AdapterDiagnosticCode.SCIENTIFIC_TRANSFORMATION_PROHIBITED,))
    add("AD43_direct_upstream_bypass", "Direct upstream bypass.", _request("AD43_direct_upstream_bypass", direct_upstream_bypass=True), SelectedModuleAdapterState.EXCLUDED, FrozenModuleInputState.EXCLUDED, (AdapterDiagnosticCode.DIRECT_UPSTREAM_BYPASS,))
    add("AD44_raw_prepared_observation_bypass", "Raw Prepared Observation bypass.", _request("AD44_raw_prepared_observation_bypass", raw_prepared_observation_bypass=True), SelectedModuleAdapterState.EXCLUDED, FrozenModuleInputState.EXCLUDED, (AdapterDiagnosticCode.RAW_PREPARED_OBSERVATION_BYPASS,))
    temporal_pkg = _selected_package("AD45_temporal_incompatible", temporal_alignment_state=po.TemporalAlignmentState.UNKNOWN_ALIGNMENT)
    add("AD45_temporal_incompatible", "Temporal metadata incompatible.", _request("AD45_temporal_incompatible", intake_handoff=_selected_intake("AD45_temporal_incompatible", package=temporal_pkg, contract=_selected_contract(conditional=True))), SelectedModuleAdapterState.UNRESOLVED, FrozenModuleInputState.UNRESOLVED, (AdapterDiagnosticCode.EXECUTION_NOT_AUTHORIZED, AdapterDiagnosticCode.TEMPORAL_METADATA_INCOMPATIBLE))
    coverage_pkg = _selected_package("AD46_insufficient_coverage", coverage=po.CoverageMetadata(target_coverage=False))
    add("AD46_insufficient_coverage", "Insufficient mapping coverage.", _request("AD46_insufficient_coverage", intake_handoff=_selected_intake("AD46_insufficient_coverage", package=coverage_pkg)), SelectedModuleAdapterState.INSUFFICIENT_EVIDENCE, FrozenModuleInputState.INSUFFICIENT_EVIDENCE, (AdapterDiagnosticCode.EXECUTION_NOT_AUTHORIZED, AdapterDiagnosticCode.INSUFFICIENT_MAPPING_COVERAGE))
    missing_pkg = _selected_package("AD47_unacceptable_missingness", missingness=po.MissingnessMetadata(required_field_missing=True))
    add("AD47_unacceptable_missingness", "Unacceptable missingness.", _request("AD47_unacceptable_missingness", intake_handoff=_selected_intake("AD47_unacceptable_missingness", package=missing_pkg, contract=_selected_contract(conditional=True))), SelectedModuleAdapterState.INCOMPATIBLE, FrozenModuleInputState.INCOMPLETE, (AdapterDiagnosticCode.EXECUTION_NOT_AUTHORIZED, AdapterDiagnosticCode.UNACCEPTABLE_MAPPING_MISSINGNESS))

    return tuple(fixtures)


def selected_module_adapter_guardrail_manifest() -> dict[str, bool]:
    return {
        "retrieves_sources": False,
        "evaluates_authority": False,
        "constructs_pit": False,
        "constructs_identity": False,
        "constructs_comparators": False,
        "constructs_prepared_observations": False,
        "recomputes_intake": False,
        "recomputes_activation": False,
        "recomputes_execution_authorization": False,
        "executes_science": False,
        "calculates_repair": False,
        "calculates_decomposition": False,
        "calculates_stabilization": False,
        "calculates_asymmetry": False,
        "defines_formulas": False,
        "generates_signals": False,
        "generates_factors": False,
        "creates_candidates": False,
        "creates_panels": False,
        "calculates_ic": False,
        "runs_validation": False,
        "runs_production": False,
        "optimizes": False,
        "introduces_ml": False,
    }


def real_selected_module_adapter_result() -> FrozenModuleInputContract:
    fixture = {item.fixture_id: item for item in canonical_selected_module_adapter_fixtures()}["AD08_real_selected_module_blocked"]
    return evaluate_selected_module_adapter(fixture.request)
