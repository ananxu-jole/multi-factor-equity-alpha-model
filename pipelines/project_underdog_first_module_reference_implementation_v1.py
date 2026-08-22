from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
import json
import math
from typing import Any


MODULE_ID = "project_underdog_first_module_reference_implementation_v1"
MODULE_VERSION = "v1"
FROZEN_CONTRACT_ID = "project_underdog_first_module_implementation_readiness_freeze_v1"
SCIENTIFIC_MODULE_NAME = "Common-Versus-Idiosyncratic Post-Stress Repair Decomposition"


class DecompositionStatus(str, Enum):
    COMMON = "common"
    IDIOSYNCRATIC = "idiosyncratic"
    MIXED = "mixed"
    UNRESOLVED = "unresolved"


class ValidityState(str, Enum):
    VALID = "valid"
    UNRESOLVED = "unresolved"
    FAIL_CLOSED = "fail_closed"
    REJECTED = "rejected"


class GateStatus(str, Enum):
    PASS = "pass"
    FAIL_CLOSED = "fail_closed"
    UNRESOLVED = "unresolved"
    REJECTED = "rejected"
    WARNING = "warning"


class DiagnosticCode(str, Enum):
    SPECIFICATION_MISMATCH = "SPECIFICATION_MISMATCH"
    SOURCE_SPECIFIC_INPUT = "SOURCE_SPECIFIC_INPUT"
    INVALID_IDENTITY = "INVALID_IDENTITY"
    INVALID_PIT_STATE = "INVALID_PIT_STATE"
    FUTURE_LEAKAGE = "FUTURE_LEAKAGE"
    TEMPORAL_OVERLAP_OR_REVERSAL = "TEMPORAL_OVERLAP_OR_REVERSAL"
    ABSENT_POST_STRESS_CONTEXT = "ABSENT_POST_STRESS_CONTEXT"
    UNRESOLVED_POST_STRESS_CONTEXT = "UNRESOLVED_POST_STRESS_CONTEXT"
    MISSING_TARGET_OBSERVATION = "MISSING_TARGET_OBSERVATION"
    MISSING_COMPARATOR_OBSERVATION = "MISSING_COMPARATOR_OBSERVATION"
    INSUFFICIENT_COMPARATOR_COVERAGE = "INSUFFICIENT_COMPARATOR_COVERAGE"
    INVALID_COMPARATOR_MEMBERSHIP = "INVALID_COMPARATOR_MEMBERSHIP"
    COMPARATOR_CONTEXT_UNAVAILABLE = "COMPARATOR_CONTEXT_UNAVAILABLE"
    COMPARATOR_CONTEXT_AMBIGUOUS = "COMPARATOR_CONTEXT_AMBIGUOUS"
    UNSUPPORTED_SOURCE_CONFLICT = "UNSUPPORTED_SOURCE_CONFLICT"
    COVERAGE_INVALID = "COVERAGE_INVALID"
    TERMINAL_STATE_UNRESOLVED = "TERMINAL_STATE_UNRESOLVED"
    AMBIGUOUS_DECOMPOSITION = "AMBIGUOUS_DECOMPOSITION"
    UNSTABLE_INPUT = "UNSTABLE_INPUT"
    UNAVAILABLE_FORMULA_QUANTITY = "UNAVAILABLE_FORMULA_QUANTITY"
    TRACEABILITY_FAILURE = "TRACEABILITY_FAILURE"
    MARKET_WIDE_REPAIR_VISIBLE = "MARKET_WIDE_REPAIR_VISIBLE"


class QualitativeRelation(str, Enum):
    COMMON = "common"
    IDIOSYNCRATIC = "idiosyncratic"
    MIXED = "mixed"
    AMBIGUOUS = "ambiguous"


class PostStressState(str, Enum):
    ELIGIBLE = "eligible"
    NOT_ELIGIBLE = "not_eligible"
    UNRESOLVED = "unresolved"


@dataclass(frozen=True)
class Diagnostic:
    code: DiagnosticCode
    message: str
    gate: str

    def to_dict(self) -> dict[str, str]:
        return {"code": self.code.value, "gate": self.gate, "message": self.message}


@dataclass(frozen=True)
class GateOutcome:
    gate: str
    status: GateStatus
    diagnostics: tuple[Diagnostic, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "gate": self.gate,
            "status": self.status.value,
            "diagnostics": [diag.to_dict() for diag in self.diagnostics],
        }


@dataclass(frozen=True)
class TimeBounds:
    stress_start: int
    stress_end: int
    repair_start: int
    repair_end: int
    observation_time: int
    future_start: int

    def is_valid(self) -> bool:
        # Frozen formula spec section 4: B_t precedes H_t, H_t is at or before t, and F_t is later.
        return (
            self.stress_start <= self.stress_end
            and self.stress_end < self.repair_start
            and self.repair_start <= self.repair_end
            and self.repair_end <= self.observation_time
            and self.observation_time < self.future_start
        )

    def to_dict(self) -> dict[str, int]:
        return {
            "stress_start": self.stress_start,
            "stress_end": self.stress_end,
            "repair_start": self.repair_start,
            "repair_end": self.repair_end,
            "observation_time": self.observation_time,
            "future_start": self.future_start,
        }


@dataclass(frozen=True)
class RepairObservation:
    entity_id: str
    repair_value: float | None
    identity_valid: bool = True
    pit_valid: bool = True
    observation_valid: bool = True
    coverage_valid: bool = True
    terminal_state_valid: bool = True
    missing_governed: bool = False
    unstable_input: bool = False
    trace_id: str = ""

    def has_observable_repair(self) -> bool:
        return self.repair_value is not None and math.isfinite(self.repair_value)

    def to_trace(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "has_repair_value": self.repair_value is not None,
            "identity_valid": self.identity_valid,
            "pit_valid": self.pit_valid,
            "observation_valid": self.observation_valid,
            "coverage_valid": self.coverage_valid,
            "terminal_state_valid": self.terminal_state_valid,
            "missing_governed": self.missing_governed,
            "unstable_input": self.unstable_input,
            "trace_id": self.trace_id,
        }


@dataclass(frozen=True)
class ComparatorObservation:
    observation: RepairObservation
    membership_valid: bool = True
    context_valid: bool = True

    def to_trace(self) -> dict[str, Any]:
        trace = self.observation.to_trace()
        trace.update({"membership_valid": self.membership_valid, "context_valid": self.context_valid})
        return trace


@dataclass(frozen=True)
class FirstModuleInput:
    target_id: str
    time_bounds: TimeBounds
    post_stress_state: PostStressState
    target_observation: RepairObservation
    comparator_observations: tuple[ComparatorObservation, ...]
    qualitative_relation: QualitativeRelation
    fixture_id: str = ""
    module_id: str = MODULE_ID
    frozen_contract_id: str = FROZEN_CONTRACT_ID
    source_independent: bool = True
    comparator_context_available: bool = True
    comparator_context_valid: bool = True
    comparator_context_ambiguous: bool = False
    comparator_membership_pit_valid: bool = True
    source_conflict: bool = False
    future_leakage: bool = False
    market_wide_repair_visible: bool = False
    traceability_complete: bool = True
    requested_output_roles: tuple[str, ...] = ("scientific_interpretation",)


@dataclass(frozen=True)
class FirstModuleResult:
    module_id: str
    module_version: str
    frozen_contract_id: str
    fixture_id: str
    target_id: str
    validity_state: ValidityState
    decomposition_status: DecompositionStatus
    diagnostics: tuple[Diagnostic, ...]
    gate_outcomes: tuple[GateOutcome, ...]
    target_repair: float | None
    peer_common_repair: float | None
    idiosyncratic_repair: float | None
    comparator_ids: tuple[str, ...]
    traceability: dict[str, Any]
    output_roles: tuple[str, ...] = ("scientific_interpretation",)
    alpha_claim: bool = False
    candidate_record: bool = False
    panel_record: bool = False
    discovery_output: bool = False
    validation_input: bool = False
    production_output: bool = False
    ranking_output: bool = False
    predictive_output: bool = False

    def to_ordered_dict(self) -> dict[str, Any]:
        return {
            "alpha_claim": self.alpha_claim,
            "candidate_record": self.candidate_record,
            "comparator_ids": list(self.comparator_ids),
            "decomposition_status": self.decomposition_status.value,
            "diagnostics": [diag.to_dict() for diag in self.diagnostics],
            "discovery_output": self.discovery_output,
            "fixture_id": self.fixture_id,
            "frozen_contract_id": self.frozen_contract_id,
            "gate_outcomes": [gate.to_dict() for gate in self.gate_outcomes],
            "idiosyncratic_repair": self.idiosyncratic_repair,
            "module_id": self.module_id,
            "module_version": self.module_version,
            "output_roles": list(self.output_roles),
            "panel_record": self.panel_record,
            "peer_common_repair": self.peer_common_repair,
            "predictive_output": self.predictive_output,
            "production_output": self.production_output,
            "ranking_output": self.ranking_output,
            "target_id": self.target_id,
            "target_repair": self.target_repair,
            "traceability": self.traceability,
            "validation_input": self.validation_input,
            "validity_state": self.validity_state.value,
        }

    def stable_json(self) -> str:
        return json.dumps(self.to_ordered_dict(), sort_keys=True, separators=(",", ":"))


@dataclass(frozen=True)
class FixtureCase:
    fixture_id: str
    description: str
    module_input: FirstModuleInput
    expected_validity_state: ValidityState
    expected_decomposition_status: DecompositionStatus
    expected_diagnostic_codes: tuple[DiagnosticCode, ...] = ()


def _diag(code: DiagnosticCode, gate: str, message: str) -> Diagnostic:
    return Diagnostic(code=code, gate=gate, message=message)


def _gate(gate: str, status: GateStatus, diagnostics: tuple[Diagnostic, ...] = ()) -> GateOutcome:
    return GateOutcome(gate=gate, status=status, diagnostics=diagnostics)


def _trace(inp: FirstModuleInput, gate_outcomes: tuple[GateOutcome, ...]) -> dict[str, Any]:
    return {
        "accepted_formula_components": ["R_i(t)", "C_i(t)", "D_i(t)", "Z_i(t)"],
        "accepted_measurement_concepts": [
            "post_stress_context",
            "own_security_repair",
            "peer_common_repair",
            "security_specific_repair",
            "comparator_context",
            "decomposition_outcome",
        ],
        "fixture_id": inp.fixture_id,
        "frozen_specifications": [
            "project_underdog_phase5_first_module_scientific_boundary_definition_v1",
            "project_underdog_first_module_source_independent_measurement_specification_v1",
            "project_underdog_first_module_formula_specification_v1",
            "project_underdog_first_module_synthetic_fixture_and_acceptance_test_specification_v1",
            "project_underdog_first_module_implementation_architecture_specification_v1",
            "project_underdog_first_module_detailed_implementation_design_v1",
            "project_underdog_first_module_implementation_readiness_freeze_v1",
        ],
        "gate_sequence": [gate.gate for gate in gate_outcomes],
        "module_name": SCIENTIFIC_MODULE_NAME,
        "target_observation": inp.target_observation.to_trace(),
        "time_bounds": inp.time_bounds.to_dict(),
        "comparator_observations": [comp.to_trace() for comp in inp.comparator_observations],
    }


def _final_result(
    inp: FirstModuleInput,
    validity_state: ValidityState,
    status: DecompositionStatus,
    gate_outcomes: list[GateOutcome],
    *,
    target_repair: float | None = None,
    peer_common_repair: float | None = None,
    idiosyncratic_repair: float | None = None,
    comparator_ids: tuple[str, ...] = (),
) -> FirstModuleResult:
    diagnostics = tuple(diag for gate in gate_outcomes for diag in gate.diagnostics)
    gate_tuple = tuple(gate_outcomes)
    return FirstModuleResult(
        module_id=MODULE_ID,
        module_version=MODULE_VERSION,
        frozen_contract_id=FROZEN_CONTRACT_ID,
        fixture_id=inp.fixture_id,
        target_id=inp.target_id,
        validity_state=validity_state,
        decomposition_status=status,
        diagnostics=diagnostics,
        gate_outcomes=gate_tuple,
        target_repair=target_repair,
        peer_common_repair=peer_common_repair,
        idiosyncratic_repair=idiosyncratic_repair,
        comparator_ids=comparator_ids,
        traceability=_trace(inp, gate_tuple),
    )


def run_first_module_reference(inp: FirstModuleInput) -> FirstModuleResult:
    """Reference implementation authorized by the frozen first-module implementation stack.

    The function accepts only prepared source-independent observations, implements the
    formula-specification v1 direct decomposition, and fails closed for invalid gates.
    """

    gates: list[GateOutcome] = []

    if inp.module_id != MODULE_ID or inp.frozen_contract_id != FROZEN_CONTRACT_ID:
        diagnostics = (
            _diag(
                DiagnosticCode.SPECIFICATION_MISMATCH,
                "specification_conformance",
                "Input module or frozen contract identity does not match the approved reference implementation.",
            ),
        )
        gates.append(_gate("specification_conformance", GateStatus.REJECTED, diagnostics))
        return _final_result(inp, ValidityState.REJECTED, DecompositionStatus.UNRESOLVED, gates)
    gates.append(_gate("specification_conformance", GateStatus.PASS))

    if not inp.source_independent or inp.requested_output_roles != ("scientific_interpretation",):
        diagnostics = (
            _diag(
                DiagnosticCode.SOURCE_SPECIFIC_INPUT,
                "observation_intake",
                "Observation intake accepts only source-independent roles and scientific interpretation output.",
            ),
        )
        gates.append(_gate("observation_intake", GateStatus.REJECTED, diagnostics))
        return _final_result(inp, ValidityState.REJECTED, DecompositionStatus.UNRESOLVED, gates)
    gates.append(_gate("observation_intake", GateStatus.PASS))
    gates.append(_gate("measurement_mapping", GateStatus.PASS))

    all_observations = (inp.target_observation,) + tuple(comp.observation for comp in inp.comparator_observations)
    if not inp.target_observation.identity_valid or any(not obs.identity_valid for obs in all_observations):
        diagnostics = (
            _diag(DiagnosticCode.INVALID_IDENTITY, "identity_validity", "Target or comparator identity is invalid."),
        )
        gates.append(_gate("identity_validity", GateStatus.UNRESOLVED, diagnostics))
        return _final_result(inp, ValidityState.UNRESOLVED, DecompositionStatus.UNRESOLVED, gates)
    gates.append(_gate("identity_validity", GateStatus.PASS))

    if (
        not inp.target_observation.pit_valid
        or any(not obs.pit_valid for obs in all_observations)
        or not inp.comparator_membership_pit_valid
    ):
        diagnostics = (
            _diag(DiagnosticCode.INVALID_PIT_STATE, "pit_validity", "PIT validity failed for target, comparator, or membership."),
        )
        gates.append(_gate("pit_validity", GateStatus.FAIL_CLOSED, diagnostics))
        return _final_result(inp, ValidityState.FAIL_CLOSED, DecompositionStatus.UNRESOLVED, gates)
    if inp.future_leakage:
        diagnostics = (
            _diag(DiagnosticCode.FUTURE_LEAKAGE, "pit_validity", "Future-known information entered the explanatory relationship."),
        )
        gates.append(_gate("pit_validity", GateStatus.FAIL_CLOSED, diagnostics))
        return _final_result(inp, ValidityState.FAIL_CLOSED, DecompositionStatus.UNRESOLVED, gates)
    gates.append(_gate("pit_validity", GateStatus.PASS))

    if not inp.time_bounds.is_valid():
        diagnostics = (
            _diag(
                DiagnosticCode.TEMPORAL_OVERLAP_OR_REVERSAL,
                "temporal_validity",
                "Temporal ordering must preserve B_t before H_t at or before t before F_t.",
            ),
        )
        gates.append(_gate("temporal_validity", GateStatus.FAIL_CLOSED, diagnostics))
        return _final_result(inp, ValidityState.FAIL_CLOSED, DecompositionStatus.UNRESOLVED, gates)
    gates.append(_gate("temporal_validity", GateStatus.PASS))

    if inp.post_stress_state == PostStressState.NOT_ELIGIBLE:
        diagnostics = (
            _diag(
                DiagnosticCode.ABSENT_POST_STRESS_CONTEXT,
                "post_stress_context_validity",
                "The first module is not applicable without eligible post-stress context.",
            ),
        )
        gates.append(_gate("post_stress_context_validity", GateStatus.UNRESOLVED, diagnostics))
        return _final_result(inp, ValidityState.UNRESOLVED, DecompositionStatus.UNRESOLVED, gates)
    if inp.post_stress_state == PostStressState.UNRESOLVED:
        diagnostics = (
            _diag(
                DiagnosticCode.UNRESOLVED_POST_STRESS_CONTEXT,
                "post_stress_context_validity",
                "Unresolved stress context must preserve unresolved decomposition.",
            ),
        )
        gates.append(_gate("post_stress_context_validity", GateStatus.UNRESOLVED, diagnostics))
        return _final_result(inp, ValidityState.UNRESOLVED, DecompositionStatus.UNRESOLVED, gates)
    gates.append(_gate("post_stress_context_validity", GateStatus.PASS))

    comparator_diags: list[Diagnostic] = []
    if not inp.comparator_context_available:
        comparator_diags.append(
            _diag(DiagnosticCode.COMPARATOR_CONTEXT_UNAVAILABLE, "comparator_validity", "Comparator context is unavailable.")
        )
    if not inp.comparator_context_valid:
        comparator_diags.append(
            _diag(DiagnosticCode.INVALID_COMPARATOR_MEMBERSHIP, "comparator_validity", "Comparator context is invalid.")
        )
    if inp.comparator_context_ambiguous:
        comparator_diags.append(
            _diag(DiagnosticCode.COMPARATOR_CONTEXT_AMBIGUOUS, "comparator_validity", "Comparator context is ambiguous.")
        )
    if inp.source_conflict:
        comparator_diags.append(
            _diag(DiagnosticCode.UNSUPPORTED_SOURCE_CONFLICT, "comparator_validity", "Unsupported source conflict affects comparator use.")
        )
    if any((not comp.membership_valid or not comp.context_valid) for comp in inp.comparator_observations):
        comparator_diags.append(
            _diag(DiagnosticCode.INVALID_COMPARATOR_MEMBERSHIP, "comparator_validity", "Comparator membership or context validity failed.")
        )
    if comparator_diags:
        gates.append(_gate("comparator_validity", GateStatus.UNRESOLVED, tuple(comparator_diags)))
        return _final_result(inp, ValidityState.UNRESOLVED, DecompositionStatus.UNRESOLVED, gates)
    gates.append(_gate("comparator_validity", GateStatus.PASS))

    if not inp.target_observation.observation_valid or not inp.target_observation.has_observable_repair():
        diagnostics = (
            _diag(
                DiagnosticCode.MISSING_TARGET_OBSERVATION,
                "observation_validity",
                "Target repair observation is missing or invalid.",
            ),
        )
        gates.append(_gate("observation_validity", GateStatus.UNRESOLVED, diagnostics))
        return _final_result(inp, ValidityState.UNRESOLVED, DecompositionStatus.UNRESOLVED, gates)

    valid_comparators: list[ComparatorObservation] = []
    missing_comparator_diags: list[Diagnostic] = []
    for comp in inp.comparator_observations:
        obs = comp.observation
        if not obs.observation_valid or not obs.has_observable_repair():
            if obs.missing_governed:
                missing_comparator_diags.append(
                    _diag(
                        DiagnosticCode.MISSING_COMPARATOR_OBSERVATION,
                        "observation_validity",
                        f"Comparator {obs.entity_id} has governed missing repair observation and is excluded.",
                    )
                )
                continue
            diagnostics = (
                _diag(
                    DiagnosticCode.MISSING_COMPARATOR_OBSERVATION,
                    "observation_validity",
                    f"Comparator {obs.entity_id} repair observation is missing or invalid.",
                ),
            )
            gates.append(_gate("observation_validity", GateStatus.UNRESOLVED, diagnostics))
            return _final_result(inp, ValidityState.UNRESOLVED, DecompositionStatus.UNRESOLVED, gates)
        valid_comparators.append(comp)

    if not valid_comparators:
        diagnostics = (
            _diag(
                DiagnosticCode.INSUFFICIENT_COMPARATOR_COVERAGE,
                "observation_validity",
                "No valid observable comparators remain after gates.",
            ),
        )
        gates.append(_gate("observation_validity", GateStatus.UNRESOLVED, diagnostics))
        return _final_result(inp, ValidityState.UNRESOLVED, DecompositionStatus.UNRESOLVED, gates)

    gates.append(
        _gate(
            "observation_validity",
            GateStatus.PASS if not missing_comparator_diags else GateStatus.WARNING,
            tuple(missing_comparator_diags),
        )
    )

    coverage_diags: list[Diagnostic] = []
    if not inp.target_observation.coverage_valid:
        coverage_diags.append(_diag(DiagnosticCode.COVERAGE_INVALID, "coverage_validity", "Target coverage is invalid."))
    if not inp.target_observation.terminal_state_valid:
        coverage_diags.append(
            _diag(DiagnosticCode.TERMINAL_STATE_UNRESOLVED, "coverage_validity", "Target terminal state is unresolved.")
        )
    for comp in valid_comparators:
        if not comp.observation.coverage_valid:
            coverage_diags.append(
                _diag(DiagnosticCode.COVERAGE_INVALID, "coverage_validity", f"Comparator {comp.observation.entity_id} coverage is invalid.")
            )
        if not comp.observation.terminal_state_valid:
            coverage_diags.append(
                _diag(
                    DiagnosticCode.TERMINAL_STATE_UNRESOLVED,
                    "coverage_validity",
                    f"Comparator {comp.observation.entity_id} terminal state is unresolved.",
                )
            )
    if coverage_diags:
        gates.append(_gate("coverage_validity", GateStatus.UNRESOLVED, tuple(coverage_diags)))
        return _final_result(inp, ValidityState.UNRESOLVED, DecompositionStatus.UNRESOLVED, gates)
    gates.append(_gate("coverage_validity", GateStatus.PASS))

    if inp.target_observation.unstable_input or any(comp.observation.unstable_input for comp in valid_comparators):
        diagnostics = (
            _diag(DiagnosticCode.UNSTABLE_INPUT, "formula_availability", "Unstable input must not be silently clipped or normalized."),
        )
        gates.append(_gate("formula_availability", GateStatus.UNRESOLVED, diagnostics))
        return _final_result(inp, ValidityState.UNRESOLVED, DecompositionStatus.UNRESOLVED, gates)

    target_repair = float(inp.target_observation.repair_value)  # type: ignore[arg-type]
    comparator_repairs = tuple(float(comp.observation.repair_value) for comp in valid_comparators)  # type: ignore[arg-type]
    if not comparator_repairs:
        diagnostics = (
            _diag(
                DiagnosticCode.UNAVAILABLE_FORMULA_QUANTITY,
                "formula_availability",
                "Peer-common repair cannot be derived without comparator observations.",
            ),
        )
        gates.append(_gate("formula_availability", GateStatus.UNRESOLVED, diagnostics))
        return _final_result(inp, ValidityState.UNRESOLVED, DecompositionStatus.UNRESOLVED, gates)

    peer_common_repair = sum(comparator_repairs) / len(comparator_repairs)
    idiosyncratic_repair = target_repair - peer_common_repair
    gates.append(_gate("formula_availability", GateStatus.PASS))
    if inp.market_wide_repair_visible:
        gates.append(
            _gate(
                "contamination_visibility",
                GateStatus.WARNING,
                (
                    _diag(
                        DiagnosticCode.MARKET_WIDE_REPAIR_VISIBLE,
                        "contamination_visibility",
                        "Market-wide repair is visible and must remain a contextual control, not alpha.",
                    ),
                ),
            )
        )

    relation_to_status = {
        QualitativeRelation.COMMON: DecompositionStatus.COMMON,
        QualitativeRelation.IDIOSYNCRATIC: DecompositionStatus.IDIOSYNCRATIC,
        QualitativeRelation.MIXED: DecompositionStatus.MIXED,
    }
    if inp.qualitative_relation == QualitativeRelation.AMBIGUOUS:
        diagnostics = (
            _diag(DiagnosticCode.AMBIGUOUS_DECOMPOSITION, "decomposition_validity", "Qualitative relation is ambiguous."),
        )
        gates.append(_gate("decomposition_validity", GateStatus.UNRESOLVED, diagnostics))
        return _final_result(
            inp,
            ValidityState.UNRESOLVED,
            DecompositionStatus.UNRESOLVED,
            gates,
            target_repair=target_repair,
            peer_common_repair=peer_common_repair,
            idiosyncratic_repair=idiosyncratic_repair,
            comparator_ids=tuple(comp.observation.entity_id for comp in valid_comparators),
        )

    gates.append(_gate("decomposition_validity", GateStatus.PASS))

    if not inp.traceability_complete:
        diagnostics = (
            _diag(DiagnosticCode.TRACEABILITY_FAILURE, "traceability_validity", "Traceability is incomplete."),
        )
        gates.append(_gate("traceability_validity", GateStatus.REJECTED, diagnostics))
        return _final_result(
            inp,
            ValidityState.REJECTED,
            DecompositionStatus.UNRESOLVED,
            gates,
            target_repair=target_repair,
            peer_common_repair=peer_common_repair,
            idiosyncratic_repair=idiosyncratic_repair,
            comparator_ids=tuple(comp.observation.entity_id for comp in valid_comparators),
        )

    gates.append(_gate("traceability_validity", GateStatus.PASS))
    return _final_result(
        inp,
        ValidityState.VALID,
        relation_to_status[inp.qualitative_relation],
        gates,
        target_repair=target_repair,
        peer_common_repair=peer_common_repair,
        idiosyncratic_repair=idiosyncratic_repair,
        comparator_ids=tuple(comp.observation.entity_id for comp in valid_comparators),
    )


def _base_input(
    *,
    fixture_id: str,
    target_repair: float | None,
    comparator_repairs: tuple[float | None, ...],
    qualitative_relation: QualitativeRelation,
    post_stress_state: PostStressState = PostStressState.ELIGIBLE,
    market_wide_repair_visible: bool = False,
) -> FirstModuleInput:
    comparators = tuple(
        ComparatorObservation(
            RepairObservation(
                entity_id=f"peer_{idx + 1}",
                repair_value=value,
                trace_id=f"{fixture_id}_peer_{idx + 1}",
            )
        )
        for idx, value in enumerate(comparator_repairs)
    )
    return FirstModuleInput(
        target_id="target_security",
        fixture_id=fixture_id,
        time_bounds=TimeBounds(0, 1, 2, 3, 3, 4),
        post_stress_state=post_stress_state,
        target_observation=RepairObservation(
            entity_id="target_security",
            repair_value=target_repair,
            trace_id=f"{fixture_id}_target",
        ),
        comparator_observations=comparators,
        qualitative_relation=qualitative_relation,
        market_wide_repair_visible=market_wide_repair_visible,
    )


def canonical_fixtures() -> tuple[FixtureCase, ...]:
    """Executable versions of the 15 canonical synthetic fixtures from the frozen fixture spec."""

    fixtures: list[FixtureCase] = [
        FixtureCase(
            "F1_common_repair",
            "Target and peers repair together.",
            _base_input(fixture_id="F1_common_repair", target_repair=1.0, comparator_repairs=(1.0, 1.0), qualitative_relation=QualitativeRelation.COMMON),
            ValidityState.VALID,
            DecompositionStatus.COMMON,
        ),
        FixtureCase(
            "F2_idiosyncratic_repair",
            "Target repairs while peers do not.",
            _base_input(
                fixture_id="F2_idiosyncratic_repair",
                target_repair=2.0,
                comparator_repairs=(0.0, 0.0),
                qualitative_relation=QualitativeRelation.IDIOSYNCRATIC,
            ),
            ValidityState.VALID,
            DecompositionStatus.IDIOSYNCRATIC,
        ),
        FixtureCase(
            "F3_mixed_repair",
            "Target and peers both repair, with material target-specific component.",
            _base_input(fixture_id="F3_mixed_repair", target_repair=2.0, comparator_repairs=(1.0, 1.0), qualitative_relation=QualitativeRelation.MIXED),
            ValidityState.VALID,
            DecompositionStatus.MIXED,
        ),
        FixtureCase(
            "F4_unresolved_repair",
            "Materiality relation is ambiguous.",
            _base_input(
                fixture_id="F4_unresolved_repair",
                target_repair=1.0,
                comparator_repairs=(0.8, 1.2),
                qualitative_relation=QualitativeRelation.AMBIGUOUS,
            ),
            ValidityState.UNRESOLVED,
            DecompositionStatus.UNRESOLVED,
            (DiagnosticCode.AMBIGUOUS_DECOMPOSITION,),
        ),
        FixtureCase(
            "F5_comparator_unavailable",
            "Comparator context is unavailable.",
            FirstModuleInput(
                **{
                    **_base_input(
                        fixture_id="F5_comparator_unavailable",
                        target_repair=1.0,
                        comparator_repairs=(1.0,),
                        qualitative_relation=QualitativeRelation.COMMON,
                    ).__dict__,
                    "comparator_context_available": False,
                }
            ),
            ValidityState.UNRESOLVED,
            DecompositionStatus.UNRESOLVED,
            (DiagnosticCode.COMPARATOR_CONTEXT_UNAVAILABLE,),
        ),
        FixtureCase(
            "F6_invalid_identity",
            "Target identity is invalid.",
            FirstModuleInput(
                **{
                    **_base_input(
                        fixture_id="F6_invalid_identity",
                        target_repair=1.0,
                        comparator_repairs=(1.0,),
                        qualitative_relation=QualitativeRelation.COMMON,
                    ).__dict__,
                    "target_observation": RepairObservation("target_security", 1.0, identity_valid=False, trace_id="F6_target"),
                }
            ),
            ValidityState.UNRESOLVED,
            DecompositionStatus.UNRESOLVED,
            (DiagnosticCode.INVALID_IDENTITY,),
        ),
        FixtureCase(
            "F7_pit_violation",
            "Comparator membership uses future/current evidence.",
            FirstModuleInput(
                **{
                    **_base_input(
                        fixture_id="F7_pit_violation",
                        target_repair=1.0,
                        comparator_repairs=(1.0,),
                        qualitative_relation=QualitativeRelation.COMMON,
                    ).__dict__,
                    "comparator_membership_pit_valid": False,
                }
            ),
            ValidityState.FAIL_CLOSED,
            DecompositionStatus.UNRESOLVED,
            (DiagnosticCode.INVALID_PIT_STATE,),
        ),
        FixtureCase(
            "F8_timing_violation",
            "Repair period overlaps stress period.",
            FirstModuleInput(
                **{
                    **_base_input(
                        fixture_id="F8_timing_violation",
                        target_repair=1.0,
                        comparator_repairs=(1.0,),
                        qualitative_relation=QualitativeRelation.COMMON,
                    ).__dict__,
                    "time_bounds": TimeBounds(0, 2, 2, 3, 3, 4),
                }
            ),
            ValidityState.FAIL_CLOSED,
            DecompositionStatus.UNRESOLVED,
            (DiagnosticCode.TEMPORAL_OVERLAP_OR_REVERSAL,),
        ),
        FixtureCase(
            "F9_market_wide_repair",
            "Market-wide repair is visible and must remain contextual.",
            _base_input(
                fixture_id="F9_market_wide_repair",
                target_repair=1.0,
                comparator_repairs=(1.0, 1.0),
                qualitative_relation=QualitativeRelation.COMMON,
                market_wide_repair_visible=True,
            ),
            ValidityState.VALID,
            DecompositionStatus.COMMON,
            (DiagnosticCode.MARKET_WIDE_REPAIR_VISIBLE,),
        ),
        FixtureCase(
            "F10_target_only_repair",
            "Target-only repair remains interpretive, not alpha.",
            _base_input(
                fixture_id="F10_target_only_repair",
                target_repair=3.0,
                comparator_repairs=(0.0, 0.0),
                qualitative_relation=QualitativeRelation.IDIOSYNCRATIC,
            ),
            ValidityState.VALID,
            DecompositionStatus.IDIOSYNCRATIC,
        ),
        FixtureCase(
            "F11_peer_only_repair",
            "Peers repair while target does not.",
            _base_input(fixture_id="F11_peer_only_repair", target_repair=0.0, comparator_repairs=(1.0, 1.0), qualitative_relation=QualitativeRelation.MIXED),
            ValidityState.VALID,
            DecompositionStatus.MIXED,
        ),
        FixtureCase(
            "F12_partial_repair",
            "Target and peer repair partially diverge.",
            _base_input(fixture_id="F12_partial_repair", target_repair=1.5, comparator_repairs=(1.0, 1.0), qualitative_relation=QualitativeRelation.MIXED),
            ValidityState.VALID,
            DecompositionStatus.MIXED,
        ),
        FixtureCase(
            "F13_missing_observations",
            "Target observation is missing.",
            _base_input(
                fixture_id="F13_missing_observations",
                target_repair=None,
                comparator_repairs=(1.0, 1.0),
                qualitative_relation=QualitativeRelation.COMMON,
            ),
            ValidityState.UNRESOLVED,
            DecompositionStatus.UNRESOLVED,
            (DiagnosticCode.MISSING_TARGET_OBSERVATION,),
        ),
        FixtureCase(
            "F14_ambiguous_decomposition",
            "Formula quantities exist but interpretation is ambiguous.",
            _base_input(
                fixture_id="F14_ambiguous_decomposition",
                target_repair=-0.1,
                comparator_repairs=(0.1, -0.1),
                qualitative_relation=QualitativeRelation.AMBIGUOUS,
            ),
            ValidityState.UNRESOLVED,
            DecompositionStatus.UNRESOLVED,
            (DiagnosticCode.AMBIGUOUS_DECOMPOSITION,),
        ),
        FixtureCase(
            "F15_unstable_input",
            "Unstable input must not be clipped or normalized.",
            FirstModuleInput(
                **{
                    **_base_input(
                        fixture_id="F15_unstable_input",
                        target_repair=1.0,
                        comparator_repairs=(1.0,),
                        qualitative_relation=QualitativeRelation.COMMON,
                    ).__dict__,
                    "target_observation": RepairObservation("target_security", 1.0, unstable_input=True, trace_id="F15_target"),
                }
            ),
            ValidityState.UNRESOLVED,
            DecompositionStatus.UNRESOLVED,
            (DiagnosticCode.UNSTABLE_INPUT,),
        ),
    ]
    return tuple(fixtures)


def fixture_results() -> tuple[FirstModuleResult, ...]:
    return tuple(run_first_module_reference(fixture.module_input) for fixture in canonical_fixtures())


def module_guardrail_manifest() -> dict[str, bool | str]:
    return {
        "module_id": MODULE_ID,
        "frozen_contract_id": FROZEN_CONTRACT_ID,
        "source_independent": True,
        "external_data_retrieval": False,
        "real_peer_construction": False,
        "candidate_generation": False,
        "panel_generation": False,
        "ic_computation": False,
        "discovery_executed": False,
        "validation_executed": False,
        "production_logic": False,
        "survivor_status_changed": False,
        "formula_optimization": False,
        "ml_integration": False,
    }
