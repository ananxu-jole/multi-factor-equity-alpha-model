from __future__ import annotations

from dataclasses import dataclass, field, is_dataclass
from enum import Enum
import hashlib
import json
import math
from typing import Any

from pipelines import project_underdog_phase5_selected_scientific_module_adapter_reference_implementation_v1 as adapter


MODULE_ID = "project_underdog_phase5_selected_scientific_module_scientific_execution_reference_implementation_v1"
MODULE_VERSION = "v1"
DESIGN_ID = "project_underdog_phase5_selected_scientific_module_scientific_execution_design_v1"
FINAL_CLASSIFICATION = "SELECTED_MODULE_SCIENTIFIC_EXECUTION_REFERENCE_IMPLEMENTATION_COMPLETE"
SELECTED_MODULE_ID = adapter.SELECTED_RESEARCH_PROGRAM_ID
SELECTED_NARROW_MODULE = adapter.NARROW_ACTIVATION_SPECIFICATION_ID
FORMULA_SPECIFICATION_ID = "project_underdog_first_module_formula_specification_v1"
FORMULA_VERSION = "first_module_formula_specification_v1"
SCIENTIFIC_EXECUTION_SCHEMA_VERSION = "selected_module_scientific_execution_schema_v1"
REPRODUCIBILITY_SCHEMA_VERSION = "selected_module_scientific_execution_reproducibility_schema_v1"
STABLE_SERIALIZATION_VERSION = "stable_json_v1"


class ScientificExecutionState(str, Enum):
    COMPLETE = "SCIENTIFIC_EXECUTION_COMPLETE"
    UNRESOLVED = "SCIENTIFIC_EXECUTION_UNRESOLVED"
    INCOMPLETE = "SCIENTIFIC_EXECUTION_INCOMPLETE"
    INSUFFICIENT_EVIDENCE = "INSUFFICIENT_SCIENTIFIC_EXECUTION_EVIDENCE"


class DecompositionResult(str, Enum):
    COMMON = "common"
    IDIOSYNCRATIC = "idiosyncratic"
    MIXED = "mixed"
    UNRESOLVED = "unresolved"


class ScientificExecutionDiagnosticCode(str, Enum):
    FROZEN_INPUT_MISSING = "FROZEN_INPUT_MISSING"
    FROZEN_INPUT_NOT_READY = "FROZEN_INPUT_NOT_READY"
    FROZEN_ACTIVATION_SPECIFICATION_MISMATCH = "FROZEN_ACTIVATION_SPECIFICATION_MISMATCH"
    FROZEN_ACTIVATION_SPECIFICATION_VERSION_MISMATCH = "FROZEN_ACTIVATION_SPECIFICATION_VERSION_MISMATCH"
    FROZEN_HORIZON_MISMATCH = "FROZEN_HORIZON_MISMATCH"
    SCIENTIFIC_SPECIFICATION_MISMATCH = "SCIENTIFIC_SPECIFICATION_MISMATCH"
    FORMULA_VERSION_MISMATCH = "FORMULA_VERSION_MISMATCH"
    LINEAGE_INCOMPLETE = "LINEAGE_INCOMPLETE"
    REPRODUCIBILITY_INCOMPLETE = "REPRODUCIBILITY_INCOMPLETE"
    PROHIBITED_UPSTREAM_OUTPUT = "PROHIBITED_UPSTREAM_OUTPUT"
    POST_STRESS_CONTEXT_UNRESOLVED = "POST_STRESS_CONTEXT_UNRESOLVED"
    POST_STRESS_CONTEXT_NOT_ELIGIBLE = "POST_STRESS_CONTEXT_NOT_ELIGIBLE"
    TARGET_REPAIR_UNAVAILABLE = "TARGET_REPAIR_UNAVAILABLE"
    COMPARATOR_REPAIR_UNAVAILABLE = "COMPARATOR_REPAIR_UNAVAILABLE"
    INSUFFICIENT_COMPARATOR_EVIDENCE = "INSUFFICIENT_COMPARATOR_EVIDENCE"
    DECOMPOSITION_RELATION_UNAVAILABLE = "DECOMPOSITION_RELATION_UNAVAILABLE"
    DECOMPOSITION_UNRESOLVED = "DECOMPOSITION_UNRESOLVED"
    INSUFFICIENT_SCIENTIFIC_EVIDENCE = "INSUFFICIENT_SCIENTIFIC_EVIDENCE"
    UPSTREAM_MUTATION_PROHIBITED = "UPSTREAM_MUTATION_PROHIBITED"
    DOWNSTREAM_SCOPE_PROHIBITED = "DOWNSTREAM_SCOPE_PROHIBITED"
    SCIENTIFIC_EXECUTION_FORMULA_BINDING_MISMATCH = "SCIENTIFIC_EXECUTION_FORMULA_BINDING_MISMATCH"
    SCIENTIFIC_EXECUTION_PROHIBITED_ROLE = "SCIENTIFIC_EXECUTION_PROHIBITED_ROLE"
    SCIENTIFIC_EXECUTION_ROLE_BINDING_MISMATCH = "SCIENTIFIC_EXECUTION_ROLE_BINDING_MISMATCH"


REFERENCE_LIMITATIONS = (
    "REFERENCE_IMPLEMENTATION_ONLY",
    "SYNTHETIC_EXECUTION_ONLY",
    "NOT_VALIDATED",
    "NOT_PRODUCTION_READY",
)

UNRESOLVED_LIMITATIONS = (
    "INSUFFICIENT_SCIENTIFIC_EVIDENCE",
    "UNRESOLVED_DECOMPOSITION",
)

LINEAGE_CHAIN = (
    "Source Authority",
    "PIT",
    "Comparator",
    "Prepared Observations",
    "Scientific Module Intake",
    "Activation",
    "Execution Authorization",
    "Selected Module Adapter",
    "Frozen Module Input",
    "Scientific Execution",
    "Scientific Result",
)

UPSTREAM_LINEAGE_KEYS = (
    "source_authority_artifact",
    "pit_artifact",
    "comparator_artifact",
    "prepared_observation_artifact",
    "intake_evaluation_artifact",
    "activation_declaration_artifact",
    "execution_authorization_artifact",
    "adapter_registration_artifact",
    "frozen_module_input_artifact",
)

UPSTREAM_REPRODUCIBILITY_KEYS = (
    "controlled_reference",
    "deterministic_serialization",
    "stable_serialization_version",
)

FORMULA_METADATA_KEYS = (
    "formula_specification_id",
    "formula_id",
    "formula_version",
)

PROHIBITED_INFORMATION_ROLES = (
    "VALIDATED_ALPHA_INFORMATION",
    "SUPPORTED_ALPHA_INFORMATION",
    "CONTEXTUAL_CONTROL_INFORMATION",
    "CONDITIONING_INFORMATION",
    "COMPARATOR_OR_BENCHMARK_INFORMATION",
    "EXPLANATORY_ONLY_INFORMATION",
    "FAMILY_REFINEMENT_INFORMATION",
    "DIAGNOSTIC_INFORMATION",
    "NEGATIVE_INFORMATION",
    "REJECTED_OR_RETIRED_INFORMATION",
    "HYPOTHETICAL_INFORMATION",
    "MISSING_REQUIRED_INFORMATION",
    "INSUFFICIENT_EVIDENCE",
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
class ScientificExecutionRegistration:
    registration_id: str = "selected_scientific_module_scientific_execution_registration_v1"
    implementation_id: str = MODULE_ID
    implementation_version: str = MODULE_VERSION
    design_id: str = DESIGN_ID
    selected_module_id: str = SELECTED_MODULE_ID
    narrow_activation_specification_id: str = SELECTED_NARROW_MODULE
    formula_specification_id: str = FORMULA_SPECIFICATION_ID
    formula_version: str = FORMULA_VERSION
    scientific_execution_schema_version: str = SCIENTIFIC_EXECUTION_SCHEMA_VERSION
    reproducibility_schema_version: str = REPRODUCIBILITY_SCHEMA_VERSION
    stable_serialization_version: str = STABLE_SERIALIZATION_VERSION
    validates_outputs: bool = False
    supports_production: bool = False
    supports_optimization: bool = False
    supports_ml: bool = False


@dataclass(frozen=True)
class ScientificExecutionRequest:
    frozen_module_input: adapter.FrozenModuleInputContract | None
    registration: ScientificExecutionRegistration = field(default_factory=ScientificExecutionRegistration)
    requested_formula_version: str = FORMULA_VERSION
    fixture_id: str = "synthetic_scientific_execution_request"
    requester_metadata: dict[str, str] = field(default_factory=dict)
    validation_requested: bool = False
    production_requested: bool = False
    optimization_requested: bool = False
    ml_requested: bool = False


@dataclass(frozen=True)
class ScientificExecutionIdentity:
    scientific_execution_id: str
    frozen_module_input_id: str
    implementation_id: str
    implementation_version: str
    formula_version: str
    scientific_specification_id: str
    scientific_specification_version: str
    frozen_horizon_specification_id: str
    frozen_horizon_specification_version: str
    decomposition_result: DecompositionResult


@dataclass(frozen=True)
class ScientificExecutionDiagnostics:
    codes: tuple[ScientificExecutionDiagnosticCode, ...]
    entries: tuple[dict[str, str], ...]


@dataclass(frozen=True)
class ScientificExecutionLimitations:
    codes: tuple[str, ...]


@dataclass(frozen=True)
class ScientificExecutionLineage:
    lineage_chain: tuple[str, ...]
    upstream_artifacts: dict[str, Any]
    frozen_module_input_id: str
    scientific_execution_artifact: str
    scientific_result_artifact: str
    upstream_lineage_preserved: bool
    upstream_lineage_mutated: bool = False
    validation_artifact: str = ""
    candidate_artifact: str = ""
    panel_artifact: str = ""
    production_artifact: str = ""
    ml_artifact: str = ""


@dataclass(frozen=True)
class ScientificExecutionReproducibility:
    execution_version: str
    formula_version: str
    scientific_specification_version: str
    frozen_activation_specification_version: str
    frozen_horizon_version: str
    serialization_version: str
    reproducibility_schema_version: str
    deterministic_execution_identity: str
    controlled_reference: str
    source_authority_version: str = ""
    pit_version: str = ""
    comparator_version: str = ""
    prepared_observation_version: str = ""
    intake_version: str = ""
    activation_version: str = ""
    adapter_version: str = ""


@dataclass(frozen=True)
class ScientificExecutionInformationContract:
    exposes_decomposition_result: bool = True
    exposes_common_component: bool = True
    exposes_idiosyncratic_component: bool = True
    exposes_diagnostics: bool = True
    exposes_limitations: bool = True
    exposes_lineage: bool = True
    exposes_reproducibility: bool = True
    exposes_alpha: bool = False
    exposes_prediction: bool = False
    exposes_ranking: bool = False
    exposes_candidate: bool = False
    exposes_portfolio: bool = False
    computes_ic: bool = False
    performs_validation: bool = False
    performs_regression: bool = False
    performs_residualization: bool = False
    performs_optimization: bool = False
    supports_production: bool = False
    ml_feature_created: bool = False
    ml_label_created: bool = False
    model_training_performed: bool = False


@dataclass(frozen=True)
class ScientificExecutionResult:
    scientific_execution_id: str
    execution_state: ScientificExecutionState
    decomposition_result: DecompositionResult
    target_repair: float | None
    common_component: float | None
    idiosyncratic_component: float | None
    comparator_repairs: tuple[float, ...]
    diagnostics: ScientificExecutionDiagnostics
    limitations: ScientificExecutionLimitations
    identity: ScientificExecutionIdentity
    lineage: ScientificExecutionLineage
    reproducibility: ScientificExecutionReproducibility
    information_contract: ScientificExecutionInformationContract
    final_classification: str = FINAL_CLASSIFICATION
    alpha_claim: bool = False
    prediction_created: bool = False
    ranking_created: bool = False
    candidate_created: bool = False
    portfolio_created: bool = False
    ic_calculation_performed: bool = False
    validation_performed: bool = False
    regression_performed: bool = False
    residualization_performed: bool = False
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
class ScientificExecutionFixture:
    fixture_id: str
    description: str
    request: ScientificExecutionRequest
    expected_state: ScientificExecutionState
    expected_decomposition_result: DecompositionResult
    expected_diagnostic_codes: tuple[ScientificExecutionDiagnosticCode, ...] = ()
    expected_limitations: tuple[str, ...] = ()


def _diagnostic(code: ScientificExecutionDiagnosticCode, stage: str, message: str) -> dict[str, str]:
    return {"code": code.value, "message": message, "stage": stage}


def _append_diagnostic(
    diagnostics: list[dict[str, str]],
    code: ScientificExecutionDiagnosticCode,
    stage: str,
    message: str,
) -> None:
    diagnostics.append(_diagnostic(code, stage, message))


def _add_limitations(limitations: list[str], *codes: str) -> None:
    for code in codes:
        if code not in limitations:
            limitations.append(code)


def _is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def _ordered_diagnostics(entries: list[dict[str, str]]) -> tuple[dict[str, str], ...]:
    return tuple(sorted(entries, key=lambda item: (item["code"], item["stage"], item["message"])))


def _extract_target_repair(frozen_input: adapter.FrozenModuleInputContract | None) -> float | None:
    if frozen_input is None:
        return None
    value = frozen_input.target_observation_metadata.get("target_repair")
    return float(value) if _is_number(value) else None


def _extract_comparator_repairs(frozen_input: adapter.FrozenModuleInputContract | None) -> tuple[float, ...]:
    if frozen_input is None:
        return ()
    repairs: list[float] = []
    for attachment in frozen_input.comparator_attachments:
        value = attachment.get("comparator_repair")
        if _is_number(value):
            repairs.append(float(value))
    return tuple(repairs)


def _extract_decomposition_relation(frozen_input: adapter.FrozenModuleInputContract | None) -> DecompositionResult | None:
    if frozen_input is None:
        return None
    value = frozen_input.target_observation_metadata.get("decomposition_relation")
    try:
        return DecompositionResult(str(value))
    except ValueError:
        return None


def _upstream_output_present(frozen_input: adapter.FrozenModuleInputContract) -> bool:
    return any(
        (
            frozen_input.exposes_scientific_execution_artifact,
            frozen_input.exposes_scientific_result_artifact,
            frozen_input.exposes_measurement_artifact,
            frozen_input.exposes_validation_artifact,
            frozen_input.repair_calculation_performed,
            frozen_input.decomposition_calculation_performed,
            frozen_input.formula_execution_performed,
            frozen_input.signal_generation_performed,
            frozen_input.factor_generation_performed,
            frozen_input.candidate_generation_performed,
            frozen_input.panel_generation_performed,
            frozen_input.ic_calculation_performed,
            frozen_input.validation_performed,
            frozen_input.production_logic_performed,
            frozen_input.optimization_performed,
            frozen_input.ml_feature_created,
            frozen_input.ml_label_created,
            frozen_input.model_training_performed,
        )
    )


def _lineage_complete(frozen_input: adapter.FrozenModuleInputContract | None) -> bool:
    if frozen_input is None:
        return False
    return all(bool(frozen_input.artifact_lineage.get(key)) for key in UPSTREAM_LINEAGE_KEYS)


def _reproducibility_complete(frozen_input: adapter.FrozenModuleInputContract | None) -> bool:
    if frozen_input is None:
        return False
    return all(bool(frozen_input.reproducibility_metadata.get(key)) for key in UPSTREAM_REPRODUCIBILITY_KEYS)


def _registration_is_authoritative(registration: ScientificExecutionRegistration) -> bool:
    return (
        registration.implementation_id == MODULE_ID
        and registration.implementation_version == MODULE_VERSION
        and registration.design_id == DESIGN_ID
        and registration.selected_module_id == SELECTED_MODULE_ID
        and registration.narrow_activation_specification_id == SELECTED_NARROW_MODULE
        and registration.formula_specification_id == FORMULA_SPECIFICATION_ID
        and registration.formula_version == FORMULA_VERSION
        and registration.scientific_execution_schema_version == SCIENTIFIC_EXECUTION_SCHEMA_VERSION
        and registration.reproducibility_schema_version == REPRODUCIBILITY_SCHEMA_VERSION
        and registration.stable_serialization_version == STABLE_SERIALIZATION_VERSION
        and registration.validates_outputs is False
        and registration.supports_production is False
        and registration.supports_optimization is False
        and registration.supports_ml is False
    )


def _supplied_formula_metadata_mismatches(frozen_input: adapter.FrozenModuleInputContract | None) -> bool:
    if frozen_input is None:
        return False
    metadata_sources = (
        frozen_input.target_observation_metadata,
        frozen_input.temporal_metadata,
        frozen_input.coverage_metadata,
        frozen_input.missingness_metadata,
        frozen_input.reproducibility_metadata,
        frozen_input.governing_versions,
        frozen_input.information_contract,
    )
    for source in metadata_sources:
        for key in FORMULA_METADATA_KEYS:
            if key not in source:
                continue
            value = source.get(key)
            if key in {"formula_specification_id", "formula_id"} and value != FORMULA_SPECIFICATION_ID:
                return True
            if key == "formula_version" and value != FORMULA_VERSION:
                return True
    return False


def _role_binding_failures(frozen_input: adapter.FrozenModuleInputContract | None) -> tuple[ScientificExecutionDiagnosticCode, ...]:
    if frozen_input is None:
        return ()
    failures: list[ScientificExecutionDiagnosticCode] = []
    required_role = adapter.DEFAULT_REQUIRED_ROLE
    role_bindings = tuple(binding.get("information_role") for binding in frozen_input.information_role_bindings)

    if required_role not in role_bindings:
        failures.append(ScientificExecutionDiagnosticCode.SCIENTIFIC_EXECUTION_ROLE_BINDING_MISMATCH)
    for role in role_bindings:
        if role != required_role:
            failures.append(ScientificExecutionDiagnosticCode.SCIENTIFIC_EXECUTION_PROHIBITED_ROLE)

    target_role = frozen_input.target_observation_metadata.get("information_role")
    if target_role is not None and target_role != required_role:
        failures.append(ScientificExecutionDiagnosticCode.SCIENTIFIC_EXECUTION_ROLE_BINDING_MISMATCH)

    for attachment in frozen_input.context_attachments:
        role = attachment.get("information_role")
        if role != required_role:
            failures.append(ScientificExecutionDiagnosticCode.SCIENTIFIC_EXECUTION_ROLE_BINDING_MISMATCH)

    for attachment in frozen_input.comparator_attachments:
        role = attachment.get("information_role")
        if role != required_role:
            failures.append(ScientificExecutionDiagnosticCode.SCIENTIFIC_EXECUTION_ROLE_BINDING_MISMATCH)

    return tuple(dict.fromkeys(failures))


def _build_identity_payload(
    request: ScientificExecutionRequest,
    decomposition_result: DecompositionResult,
    target_repair: float | None,
    comparator_repairs: tuple[float, ...],
) -> dict[str, Any]:
    frozen_input = request.frozen_module_input
    return {
        "fixture_id": request.fixture_id,
        "frozen_module_input_id": "" if frozen_input is None else frozen_input.frozen_module_input_id,
        "implementation_id": request.registration.implementation_id,
        "implementation_version": request.registration.implementation_version,
        "formula_version": request.requested_formula_version,
        "module_id": "" if frozen_input is None else frozen_input.module_id,
        "module_version": "" if frozen_input is None else frozen_input.module_version,
        "activation_specification_id": "" if frozen_input is None else frozen_input.activation_specification_id,
        "activation_specification_version": "" if frozen_input is None else frozen_input.activation_specification_version,
        "scientific_specification_id": "" if frozen_input is None else frozen_input.scientific_specification_id,
        "scientific_specification_version": "" if frozen_input is None else frozen_input.scientific_specification_version,
        "frozen_horizon_specification_id": "" if frozen_input is None else frozen_input.frozen_horizon_specification_id,
        "frozen_horizon_specification_version": "" if frozen_input is None else frozen_input.frozen_horizon_specification_version,
        "target_repair": target_repair,
        "comparator_repairs": comparator_repairs,
        "decomposition_result": decomposition_result.value,
    }


def execute_selected_scientific_module(
    request: ScientificExecutionRequest,
) -> ScientificExecutionResult:
    diagnostics: list[dict[str, str]] = []
    limitations: list[str] = list(REFERENCE_LIMITATIONS)
    frozen_input = request.frozen_module_input

    if frozen_input is None:
        _append_diagnostic(
            diagnostics,
            ScientificExecutionDiagnosticCode.FROZEN_INPUT_MISSING,
            "frozen_input_verification",
            "Scientific execution requires an accepted Frozen Module Input.",
        )
    else:
        if frozen_input.frozen_module_input_state != adapter.FrozenModuleInputState.READY:
            _append_diagnostic(
                diagnostics,
                ScientificExecutionDiagnosticCode.FROZEN_INPUT_NOT_READY,
                "frozen_input_verification",
                "Frozen Module Input is not in FROZEN_MODULE_INPUT_READY state.",
            )
        if frozen_input.activation_specification_id != adapter.NARROW_ACTIVATION_SPECIFICATION_ID:
            _append_diagnostic(
                diagnostics,
                ScientificExecutionDiagnosticCode.FROZEN_ACTIVATION_SPECIFICATION_MISMATCH,
                "frozen_input_verification",
                "Frozen activation specification does not match the selected narrow module.",
            )
        if frozen_input.activation_specification_version != adapter.NARROW_ACTIVATION_SPECIFICATION_VERSION:
            _append_diagnostic(
                diagnostics,
                ScientificExecutionDiagnosticCode.FROZEN_ACTIVATION_SPECIFICATION_VERSION_MISMATCH,
                "frozen_input_verification",
                "Frozen activation specification version does not match the selected narrow module.",
            )
        if (
            frozen_input.frozen_horizon_specification_id != adapter.DEFAULT_FROZEN_HORIZON_SPECIFICATION_ID
            or frozen_input.frozen_horizon_specification_version != adapter.DEFAULT_FROZEN_HORIZON_SPECIFICATION_VERSION
        ):
            _append_diagnostic(
                diagnostics,
                ScientificExecutionDiagnosticCode.FROZEN_HORIZON_MISMATCH,
                "frozen_input_verification",
                "Frozen horizon specification is not the accepted frozen horizon.",
            )
        if (
            frozen_input.scientific_specification_id != adapter.DEFAULT_SCIENTIFIC_SPECIFICATION_ID
            or frozen_input.scientific_specification_version != adapter.DEFAULT_SCIENTIFIC_SPECIFICATION_VERSION
        ):
            _append_diagnostic(
                diagnostics,
                ScientificExecutionDiagnosticCode.SCIENTIFIC_SPECIFICATION_MISMATCH,
                "frozen_input_verification",
                "Scientific specification is not the accepted selected-module specification.",
            )
        if _upstream_output_present(frozen_input):
            _append_diagnostic(
                diagnostics,
                ScientificExecutionDiagnosticCode.PROHIBITED_UPSTREAM_OUTPUT,
                "contamination_control",
                "Frozen input already exposes downstream scientific or validation artifacts.",
            )

    if request.requested_formula_version != request.registration.formula_version:
        _append_diagnostic(
            diagnostics,
            ScientificExecutionDiagnosticCode.FORMULA_VERSION_MISMATCH,
            "formula_invocation",
            "Scientific execution may invoke only the approved frozen formula version.",
        )

    if (
        request.requested_formula_version != FORMULA_VERSION
        or not _registration_is_authoritative(request.registration)
        or _supplied_formula_metadata_mismatches(frozen_input)
    ):
        _append_diagnostic(
            diagnostics,
            ScientificExecutionDiagnosticCode.SCIENTIFIC_EXECUTION_FORMULA_BINDING_MISMATCH,
            "formula_invocation",
            "Scientific execution formula binding does not match the frozen authoritative specification.",
        )

    if request.validation_requested or request.production_requested or request.optimization_requested or request.ml_requested:
        _append_diagnostic(
            diagnostics,
            ScientificExecutionDiagnosticCode.DOWNSTREAM_SCOPE_PROHIBITED,
            "contamination_control",
            "Validation, production, optimization, and ML are outside scientific execution scope.",
        )

    if not _lineage_complete(frozen_input):
        _append_diagnostic(
            diagnostics,
            ScientificExecutionDiagnosticCode.LINEAGE_INCOMPLETE,
            "lineage_construction",
            "Required upstream lineage chain is incomplete.",
        )

    if not _reproducibility_complete(frozen_input):
        _append_diagnostic(
            diagnostics,
            ScientificExecutionDiagnosticCode.REPRODUCIBILITY_INCOMPLETE,
            "reproducibility",
            "Required frozen-input reproducibility metadata is incomplete.",
        )

    for role_failure in _role_binding_failures(frozen_input):
        _append_diagnostic(
            diagnostics,
            role_failure,
            "information_role_validation",
            "Frozen input information role binding is not execution-valid for the selected module.",
        )

    target_repair = _extract_target_repair(frozen_input)
    comparator_repairs = _extract_comparator_repairs(frozen_input)
    relation = _extract_decomposition_relation(frozen_input)
    post_stress_state = None if frozen_input is None else frozen_input.target_observation_metadata.get("post_stress_state")

    if post_stress_state == "unresolved":
        _append_diagnostic(
            diagnostics,
            ScientificExecutionDiagnosticCode.POST_STRESS_CONTEXT_UNRESOLVED,
            "scientific_precondition_verification",
            "Post-stress context is unresolved.",
        )
    elif post_stress_state != "eligible":
        _append_diagnostic(
            diagnostics,
            ScientificExecutionDiagnosticCode.POST_STRESS_CONTEXT_NOT_ELIGIBLE,
            "scientific_precondition_verification",
            "Post-stress context is not eligible for the selected formula.",
        )

    if target_repair is None:
        _append_diagnostic(
            diagnostics,
            ScientificExecutionDiagnosticCode.TARGET_REPAIR_UNAVAILABLE,
            "scientific_precondition_verification",
            "Target repair observation is unavailable.",
        )

    if frozen_input is not None and len(frozen_input.comparator_attachments) == 0:
        _append_diagnostic(
            diagnostics,
            ScientificExecutionDiagnosticCode.INSUFFICIENT_COMPARATOR_EVIDENCE,
            "scientific_precondition_verification",
            "Comparator evidence is absent.",
        )
    elif frozen_input is not None and len(comparator_repairs) != len(frozen_input.comparator_attachments):
        _append_diagnostic(
            diagnostics,
            ScientificExecutionDiagnosticCode.COMPARATOR_REPAIR_UNAVAILABLE,
            "scientific_precondition_verification",
            "At least one comparator repair observation is unavailable.",
        )

    if relation is None:
        _append_diagnostic(
            diagnostics,
            ScientificExecutionDiagnosticCode.DECOMPOSITION_RELATION_UNAVAILABLE,
            "decomposition_classification",
            "Predeclared qualitative decomposition relation is unavailable.",
        )

    precondition_failed = bool(diagnostics)
    common_component: float | None = None
    idiosyncratic_component: float | None = None
    decomposition_result = DecompositionResult.UNRESOLVED

    if not precondition_failed and target_repair is not None and comparator_repairs and relation is not None:
        common_component = sum(comparator_repairs) / len(comparator_repairs)
        idiosyncratic_component = target_repair - common_component
        decomposition_result = relation

    if decomposition_result == DecompositionResult.UNRESOLVED:
        _append_diagnostic(
            diagnostics,
            ScientificExecutionDiagnosticCode.DECOMPOSITION_UNRESOLVED,
            "decomposition_classification",
            "Scientific decomposition remains unresolved.",
        )
        _append_diagnostic(
            diagnostics,
            ScientificExecutionDiagnosticCode.INSUFFICIENT_SCIENTIFIC_EVIDENCE,
            "limitation_accumulation",
            "Execution result is insufficient as scientific evidence.",
        )
        _add_limitations(limitations, *UNRESOLVED_LIMITATIONS)

    ordered_entries = _ordered_diagnostics(diagnostics)
    diagnostic_codes = tuple(ScientificExecutionDiagnosticCode(entry["code"]) for entry in ordered_entries)

    if any(
        code
        in {
            ScientificExecutionDiagnosticCode.FROZEN_INPUT_MISSING,
            ScientificExecutionDiagnosticCode.FROZEN_INPUT_NOT_READY,
            ScientificExecutionDiagnosticCode.FROZEN_ACTIVATION_SPECIFICATION_MISMATCH,
            ScientificExecutionDiagnosticCode.FROZEN_ACTIVATION_SPECIFICATION_VERSION_MISMATCH,
            ScientificExecutionDiagnosticCode.FROZEN_HORIZON_MISMATCH,
            ScientificExecutionDiagnosticCode.SCIENTIFIC_SPECIFICATION_MISMATCH,
            ScientificExecutionDiagnosticCode.FORMULA_VERSION_MISMATCH,
            ScientificExecutionDiagnosticCode.SCIENTIFIC_EXECUTION_FORMULA_BINDING_MISMATCH,
            ScientificExecutionDiagnosticCode.SCIENTIFIC_EXECUTION_PROHIBITED_ROLE,
            ScientificExecutionDiagnosticCode.SCIENTIFIC_EXECUTION_ROLE_BINDING_MISMATCH,
            ScientificExecutionDiagnosticCode.LINEAGE_INCOMPLETE,
            ScientificExecutionDiagnosticCode.REPRODUCIBILITY_INCOMPLETE,
            ScientificExecutionDiagnosticCode.PROHIBITED_UPSTREAM_OUTPUT,
            ScientificExecutionDiagnosticCode.DOWNSTREAM_SCOPE_PROHIBITED,
        }
        for code in diagnostic_codes
    ):
        execution_state = ScientificExecutionState.INCOMPLETE
    elif decomposition_result == DecompositionResult.UNRESOLVED:
        execution_state = ScientificExecutionState.INSUFFICIENT_EVIDENCE
    else:
        execution_state = ScientificExecutionState.COMPLETE

    identity_payload = _build_identity_payload(request, decomposition_result, target_repair, comparator_repairs)
    scientific_execution_id = _stable_digest(identity_payload, "scientific_execution")
    frozen_module_input_id = "" if frozen_input is None else frozen_input.frozen_module_input_id

    identity = ScientificExecutionIdentity(
        scientific_execution_id=scientific_execution_id,
        frozen_module_input_id=frozen_module_input_id,
        implementation_id=request.registration.implementation_id,
        implementation_version=request.registration.implementation_version,
        formula_version=request.registration.formula_version,
        scientific_specification_id="" if frozen_input is None else frozen_input.scientific_specification_id,
        scientific_specification_version="" if frozen_input is None else frozen_input.scientific_specification_version,
        frozen_horizon_specification_id="" if frozen_input is None else frozen_input.frozen_horizon_specification_id,
        frozen_horizon_specification_version="" if frozen_input is None else frozen_input.frozen_horizon_specification_version,
        decomposition_result=decomposition_result,
    )

    upstream_artifacts = {} if frozen_input is None else {key: frozen_input.artifact_lineage.get(key, "") for key in UPSTREAM_LINEAGE_KEYS}
    lineage = ScientificExecutionLineage(
        lineage_chain=LINEAGE_CHAIN,
        upstream_artifacts=upstream_artifacts,
        frozen_module_input_id=frozen_module_input_id,
        scientific_execution_artifact=scientific_execution_id,
        scientific_result_artifact=_stable_digest({"scientific_execution_id": scientific_execution_id, "result": decomposition_result.value}, "scientific_result"),
        upstream_lineage_preserved=_lineage_complete(frozen_input),
    )

    repro_meta = {} if frozen_input is None else frozen_input.reproducibility_metadata
    governing_versions = {} if frozen_input is None else frozen_input.governing_versions
    reproducibility = ScientificExecutionReproducibility(
        execution_version=MODULE_VERSION,
        formula_version=FORMULA_VERSION,
        scientific_specification_version="" if frozen_input is None else frozen_input.scientific_specification_version,
        frozen_activation_specification_version="" if frozen_input is None else frozen_input.activation_specification_version,
        frozen_horizon_version="" if frozen_input is None else frozen_input.frozen_horizon_specification_version,
        serialization_version=STABLE_SERIALIZATION_VERSION,
        reproducibility_schema_version=REPRODUCIBILITY_SCHEMA_VERSION,
        deterministic_execution_identity=scientific_execution_id,
        controlled_reference=str(repro_meta.get("controlled_reference", "")),
        source_authority_version=str(governing_versions.get("source_authority_version", "")),
        pit_version=str(governing_versions.get("pit_version", "")),
        comparator_version=str(governing_versions.get("comparator_version", "")),
        prepared_observation_version=str(governing_versions.get("prepared_observation_version", "")),
        intake_version=str(governing_versions.get("intake_version", "")),
        activation_version=str(governing_versions.get("activation_version", "")),
        adapter_version="" if frozen_input is None else frozen_input.adapter_version,
    )

    return ScientificExecutionResult(
        scientific_execution_id=scientific_execution_id,
        execution_state=execution_state,
        decomposition_result=decomposition_result,
        target_repair=target_repair,
        common_component=common_component,
        idiosyncratic_component=idiosyncratic_component,
        comparator_repairs=comparator_repairs,
        diagnostics=ScientificExecutionDiagnostics(codes=diagnostic_codes, entries=ordered_entries),
        limitations=ScientificExecutionLimitations(codes=tuple(limitations)),
        identity=identity,
        lineage=lineage,
        reproducibility=reproducibility,
        information_contract=ScientificExecutionInformationContract(),
    )


def _ready_adapter_output() -> adapter.FrozenModuleInputContract:
    fixtures = {fixture.fixture_id: fixture for fixture in adapter.canonical_selected_module_adapter_fixtures()}
    return adapter.evaluate_selected_module_adapter(fixtures["AD04_valid_target_context_comparator"].request)


def _replace_frozen_input(
    base: adapter.FrozenModuleInputContract,
    fixture_id: str,
    **overrides: Any,
) -> adapter.FrozenModuleInputContract:
    payload = dict(base.__dict__)
    payload.update(overrides)
    payload.setdefault("frozen_module_input_id", f"frozen_module_input_{fixture_id}")
    lineage = dict(payload["artifact_lineage"])
    lineage["frozen_module_input_artifact"] = payload["frozen_module_input_id"]
    payload["artifact_lineage"] = lineage
    return adapter.FrozenModuleInputContract(**payload)


def _synthetic_frozen_input(
    fixture_id: str,
    target_repair: float | None,
    comparator_repairs: tuple[float | None, ...],
    relation: str | None,
    post_stress_state: str = "eligible",
    **overrides: Any,
) -> adapter.FrozenModuleInputContract:
    base = _ready_adapter_output()
    target_metadata = dict(base.target_observation_metadata)
    target_metadata.update(
        {
            "target_repair": target_repair,
            "post_stress_state": post_stress_state,
            "decomposition_relation": relation,
            "synthetic_scientific_execution_fixture_id": fixture_id,
        }
    )
    comparator_attachments = tuple(
        {
            "comparator_id": f"synthetic_comparator_{index + 1}",
            "information_role": adapter.DEFAULT_REQUIRED_ROLE,
            "comparator_repair": value,
        }
        for index, value in enumerate(comparator_repairs)
    )
    return _replace_frozen_input(
        base,
        fixture_id,
        frozen_module_input_id=f"frozen_module_input_{fixture_id}",
        target_observation_metadata=target_metadata,
        comparator_attachments=comparator_attachments,
        **overrides,
    )


def _fixture(
    fixture_id: str,
    description: str,
    frozen_input: adapter.FrozenModuleInputContract | None,
    expected_state: ScientificExecutionState,
    expected_decomposition_result: DecompositionResult,
    expected_diagnostic_codes: tuple[ScientificExecutionDiagnosticCode, ...] = (),
    expected_limitations: tuple[str, ...] = (),
    requested_formula_version: str = FORMULA_VERSION,
    registration: ScientificExecutionRegistration = ScientificExecutionRegistration(),
) -> ScientificExecutionFixture:
    return ScientificExecutionFixture(
        fixture_id=fixture_id,
        description=description,
        request=ScientificExecutionRequest(
            frozen_module_input=frozen_input,
            fixture_id=fixture_id,
            requested_formula_version=requested_formula_version,
            registration=registration,
        ),
        expected_state=expected_state,
        expected_decomposition_result=expected_decomposition_result,
        expected_diagnostic_codes=expected_diagnostic_codes,
        expected_limitations=expected_limitations,
    )


def canonical_scientific_execution_fixtures() -> tuple[ScientificExecutionFixture, ...]:
    base = _ready_adapter_output()
    bad_lineage = dict(base.artifact_lineage)
    bad_lineage["source_authority_artifact"] = ""
    bad_repro = dict(base.reproducibility_metadata)
    bad_repro["controlled_reference"] = ""
    bad_role_target = dict(base.target_observation_metadata)
    bad_role_target.update(
        {
            "target_repair": 1.0,
            "post_stress_state": "eligible",
            "decomposition_relation": "common",
            "information_role": "DIAGNOSTIC_INFORMATION",
        }
    )
    bad_role_binding = (
        {"information_role": adapter.DEFAULT_REQUIRED_ROLE},
        {"information_role": "NEGATIVE_INFORMATION"},
    )
    spoofed_registration = ScientificExecutionRegistration(formula_version="formula_v2")

    fixtures: list[ScientificExecutionFixture] = [
        _fixture(
            "SE01_common",
            "Target and comparator repairs share a predeclared common relation.",
            _synthetic_frozen_input("SE01_common", 1.0, (1.0, 1.0), "common"),
            ScientificExecutionState.COMPLETE,
            DecompositionResult.COMMON,
        ),
        _fixture(
            "SE02_idiosyncratic",
            "Target repair exceeds peer-common repair under a predeclared idiosyncratic relation.",
            _synthetic_frozen_input("SE02_idiosyncratic", 2.0, (1.0, 1.0), "idiosyncratic"),
            ScientificExecutionState.COMPLETE,
            DecompositionResult.IDIOSYNCRATIC,
        ),
        _fixture(
            "SE03_mixed",
            "Target repair and peer-common repair preserve a predeclared mixed relation.",
            _synthetic_frozen_input("SE03_mixed", 1.5, (1.0, 1.0), "mixed"),
            ScientificExecutionState.COMPLETE,
            DecompositionResult.MIXED,
        ),
        _fixture(
            "SE04_unresolved",
            "Ambiguous relation preserves unresolved decomposition.",
            _synthetic_frozen_input("SE04_unresolved", 1.2, (1.0, 1.0), "unresolved"),
            ScientificExecutionState.INSUFFICIENT_EVIDENCE,
            DecompositionResult.UNRESOLVED,
            (
                ScientificExecutionDiagnosticCode.DECOMPOSITION_UNRESOLVED,
                ScientificExecutionDiagnosticCode.INSUFFICIENT_SCIENTIFIC_EVIDENCE,
            ),
            UNRESOLVED_LIMITATIONS,
        ),
        _fixture(
            "SE05_missing_frozen_input",
            "Scientific execution refuses absent frozen input.",
            None,
            ScientificExecutionState.INCOMPLETE,
            DecompositionResult.UNRESOLVED,
            (
                ScientificExecutionDiagnosticCode.FROZEN_INPUT_MISSING,
                ScientificExecutionDiagnosticCode.LINEAGE_INCOMPLETE,
                ScientificExecutionDiagnosticCode.REPRODUCIBILITY_INCOMPLETE,
                ScientificExecutionDiagnosticCode.DECOMPOSITION_UNRESOLVED,
            ),
            UNRESOLVED_LIMITATIONS,
        ),
        _fixture(
            "SE06_frozen_spec_mismatch",
            "Wrong activation specification fails closed.",
            _synthetic_frozen_input("SE06_frozen_spec_mismatch", 1.0, (1.0, 1.0), "common", activation_specification_id="wrong_spec"),
            ScientificExecutionState.INCOMPLETE,
            DecompositionResult.UNRESOLVED,
            (ScientificExecutionDiagnosticCode.FROZEN_ACTIVATION_SPECIFICATION_MISMATCH,),
            UNRESOLVED_LIMITATIONS,
        ),
        _fixture(
            "SE07_frozen_horizon_mismatch",
            "Wrong frozen horizon fails closed.",
            _synthetic_frozen_input("SE07_frozen_horizon_mismatch", 1.0, (1.0, 1.0), "common", frozen_horizon_specification_id="wrong_horizon"),
            ScientificExecutionState.INCOMPLETE,
            DecompositionResult.UNRESOLVED,
            (ScientificExecutionDiagnosticCode.FROZEN_HORIZON_MISMATCH,),
            UNRESOLVED_LIMITATIONS,
        ),
        _fixture(
            "SE08_scientific_spec_mismatch",
            "Wrong scientific specification fails closed.",
            _synthetic_frozen_input("SE08_scientific_spec_mismatch", 1.0, (1.0, 1.0), "common", scientific_specification_id="wrong_scientific_spec"),
            ScientificExecutionState.INCOMPLETE,
            DecompositionResult.UNRESOLVED,
            (ScientificExecutionDiagnosticCode.SCIENTIFIC_SPECIFICATION_MISMATCH,),
            UNRESOLVED_LIMITATIONS,
        ),
        _fixture(
            "SE09_lineage_failure",
            "Incomplete upstream lineage blocks ready scientific output.",
            _synthetic_frozen_input("SE09_lineage_failure", 1.0, (1.0, 1.0), "common", artifact_lineage=bad_lineage),
            ScientificExecutionState.INCOMPLETE,
            DecompositionResult.UNRESOLVED,
            (ScientificExecutionDiagnosticCode.LINEAGE_INCOMPLETE,),
            UNRESOLVED_LIMITATIONS,
        ),
        _fixture(
            "SE10_reproducibility_failure",
            "Incomplete upstream reproducibility blocks ready scientific output.",
            _synthetic_frozen_input("SE10_reproducibility_failure", 1.0, (1.0, 1.0), "common", reproducibility_metadata=bad_repro),
            ScientificExecutionState.INCOMPLETE,
            DecompositionResult.UNRESOLVED,
            (ScientificExecutionDiagnosticCode.REPRODUCIBILITY_INCOMPLETE,),
            UNRESOLVED_LIMITATIONS,
        ),
        _fixture(
            "SE11_post_stress_unresolved",
            "Unresolved post-stress context forces unresolved decomposition.",
            _synthetic_frozen_input("SE11_post_stress_unresolved", 1.0, (1.0, 1.0), "common", post_stress_state="unresolved"),
            ScientificExecutionState.INSUFFICIENT_EVIDENCE,
            DecompositionResult.UNRESOLVED,
            (ScientificExecutionDiagnosticCode.POST_STRESS_CONTEXT_UNRESOLVED,),
            UNRESOLVED_LIMITATIONS,
        ),
        _fixture(
            "SE12_insufficient_comparator_evidence",
            "Absent comparators force insufficient scientific evidence.",
            _synthetic_frozen_input("SE12_insufficient_comparator_evidence", 1.0, (), "idiosyncratic"),
            ScientificExecutionState.INSUFFICIENT_EVIDENCE,
            DecompositionResult.UNRESOLVED,
            (ScientificExecutionDiagnosticCode.INSUFFICIENT_COMPARATOR_EVIDENCE,),
            UNRESOLVED_LIMITATIONS,
        ),
        _fixture(
            "SE13_missing_target_repair",
            "Missing target repair blocks formula quantities.",
            _synthetic_frozen_input("SE13_missing_target_repair", None, (1.0, 1.0), "common"),
            ScientificExecutionState.INSUFFICIENT_EVIDENCE,
            DecompositionResult.UNRESOLVED,
            (ScientificExecutionDiagnosticCode.TARGET_REPAIR_UNAVAILABLE,),
            UNRESOLVED_LIMITATIONS,
        ),
        _fixture(
            "SE14_missing_comparator_repair",
            "Missing comparator repair blocks peer-common component.",
            _synthetic_frozen_input("SE14_missing_comparator_repair", 1.0, (1.0, None), "common"),
            ScientificExecutionState.INSUFFICIENT_EVIDENCE,
            DecompositionResult.UNRESOLVED,
            (ScientificExecutionDiagnosticCode.COMPARATOR_REPAIR_UNAVAILABLE,),
            UNRESOLVED_LIMITATIONS,
        ),
        _fixture(
            "SE15_combined_failures",
            "Combined spec, horizon, target, comparator, lineage, and repro failures accumulate deterministically.",
            _synthetic_frozen_input(
                "SE15_combined_failures",
                None,
                (),
                None,
                post_stress_state="unresolved",
                activation_specification_id="wrong_spec",
                frozen_horizon_specification_id="wrong_horizon",
                scientific_specification_id="wrong_scientific_spec",
                artifact_lineage=bad_lineage,
                reproducibility_metadata=bad_repro,
            ),
            ScientificExecutionState.INCOMPLETE,
            DecompositionResult.UNRESOLVED,
            (
                ScientificExecutionDiagnosticCode.FROZEN_ACTIVATION_SPECIFICATION_MISMATCH,
                ScientificExecutionDiagnosticCode.FROZEN_HORIZON_MISMATCH,
                ScientificExecutionDiagnosticCode.SCIENTIFIC_SPECIFICATION_MISMATCH,
                ScientificExecutionDiagnosticCode.LINEAGE_INCOMPLETE,
                ScientificExecutionDiagnosticCode.REPRODUCIBILITY_INCOMPLETE,
                ScientificExecutionDiagnosticCode.POST_STRESS_CONTEXT_UNRESOLVED,
                ScientificExecutionDiagnosticCode.TARGET_REPAIR_UNAVAILABLE,
                ScientificExecutionDiagnosticCode.INSUFFICIENT_COMPARATOR_EVIDENCE,
                ScientificExecutionDiagnosticCode.DECOMPOSITION_RELATION_UNAVAILABLE,
            ),
            UNRESOLVED_LIMITATIONS,
        ),
        _fixture(
            "SE16_formula_version_mismatch",
            "Formula version substitution is prohibited.",
            _synthetic_frozen_input("SE16_formula_version_mismatch", 1.0, (1.0, 1.0), "common"),
            ScientificExecutionState.INCOMPLETE,
            DecompositionResult.UNRESOLVED,
            (ScientificExecutionDiagnosticCode.FORMULA_VERSION_MISMATCH,),
            UNRESOLVED_LIMITATIONS,
            requested_formula_version="formula_v2",
        ),
        _fixture(
            "SE17_prohibited_upstream_output",
            "Frozen input carrying prior scientific output is rejected as contaminated.",
            _synthetic_frozen_input("SE17_prohibited_upstream_output", 1.0, (1.0, 1.0), "common", formula_execution_performed=True),
            ScientificExecutionState.INCOMPLETE,
            DecompositionResult.UNRESOLVED,
            (ScientificExecutionDiagnosticCode.PROHIBITED_UPSTREAM_OUTPUT,),
            UNRESOLVED_LIMITATIONS,
        ),
        _fixture(
            "SE18_deterministic_repeat",
            "Repeat fixture for deterministic identity and serialization checks.",
            _synthetic_frozen_input("SE18_deterministic_repeat", 1.5, (1.0, 2.0), "mixed"),
            ScientificExecutionState.COMPLETE,
            DecompositionResult.MIXED,
        ),
        _fixture(
            "SE19_formula_registration_spoofing",
            "Caller-supplied formula registration cannot relabel authoritative formula metadata.",
            _synthetic_frozen_input("SE19_formula_registration_spoofing", 1.0, (1.0, 1.0), "common"),
            ScientificExecutionState.INCOMPLETE,
            DecompositionResult.UNRESOLVED,
            (ScientificExecutionDiagnosticCode.SCIENTIFIC_EXECUTION_FORMULA_BINDING_MISMATCH,),
            UNRESOLVED_LIMITATIONS,
            requested_formula_version="formula_v2",
            registration=spoofed_registration,
        ),
        _fixture(
            "SE20_blank_formula_version",
            "Blank requested formula version fails closed.",
            _synthetic_frozen_input("SE20_blank_formula_version", 1.0, (1.0, 1.0), "common"),
            ScientificExecutionState.INCOMPLETE,
            DecompositionResult.UNRESOLVED,
            (
                ScientificExecutionDiagnosticCode.FORMULA_VERSION_MISMATCH,
                ScientificExecutionDiagnosticCode.SCIENTIFIC_EXECUTION_FORMULA_BINDING_MISMATCH,
            ),
            UNRESOLVED_LIMITATIONS,
            requested_formula_version="",
        ),
        _fixture(
            "SE21_role_substitution",
            "Diagnostic role substituted into target metadata fails closed.",
            _replace_frozen_input(
                _synthetic_frozen_input("SE21_role_substitution", 1.0, (1.0, 1.0), "common"),
                "SE21_role_substitution",
                target_observation_metadata=bad_role_target,
            ),
            ScientificExecutionState.INCOMPLETE,
            DecompositionResult.UNRESOLVED,
            (ScientificExecutionDiagnosticCode.SCIENTIFIC_EXECUTION_ROLE_BINDING_MISMATCH,),
            UNRESOLVED_LIMITATIONS,
        ),
        _fixture(
            "SE22_prohibited_role_binding",
            "Unrelated prohibited role binding in otherwise ready input fails closed.",
            _synthetic_frozen_input("SE22_prohibited_role_binding", 1.0, (1.0, 1.0), "common", information_role_bindings=bad_role_binding),
            ScientificExecutionState.INCOMPLETE,
            DecompositionResult.UNRESOLVED,
            (ScientificExecutionDiagnosticCode.SCIENTIFIC_EXECUTION_PROHIBITED_ROLE,),
            UNRESOLVED_LIMITATIONS,
        ),
        _fixture(
            "SE23_combined_formula_role_failure",
            "Formula spoofing plus prohibited role preserves both diagnostics.",
            _synthetic_frozen_input("SE23_combined_formula_role_failure", 1.0, (1.0, 1.0), "common", information_role_bindings=bad_role_binding),
            ScientificExecutionState.INCOMPLETE,
            DecompositionResult.UNRESOLVED,
            (
                ScientificExecutionDiagnosticCode.SCIENTIFIC_EXECUTION_FORMULA_BINDING_MISMATCH,
                ScientificExecutionDiagnosticCode.SCIENTIFIC_EXECUTION_PROHIBITED_ROLE,
            ),
            UNRESOLVED_LIMITATIONS,
            requested_formula_version="formula_v2",
            registration=spoofed_registration,
        ),
    ]
    return tuple(fixtures)


def scientific_execution_guardrail_manifest() -> dict[str, bool]:
    return {
        "source_retrieval": False,
        "authority_evaluation": False,
        "pit_construction": False,
        "identity_construction": False,
        "comparator_construction": False,
        "prepared_observation_construction": False,
        "intake_recomputation": False,
        "activation_recomputation": False,
        "adapter_recomputation": False,
        "alternate_formula_execution": False,
        "hidden_weighting": False,
        "adaptive_thresholds": False,
        "normalization": False,
        "smoothing": False,
        "clipping": False,
        "ranking": False,
        "prediction": False,
        "candidate_generation": False,
        "panel_generation": False,
        "ic_calculation": False,
        "validation": False,
        "regression": False,
        "residualization": False,
        "optimization": False,
        "production": False,
        "ml": False,
    }
