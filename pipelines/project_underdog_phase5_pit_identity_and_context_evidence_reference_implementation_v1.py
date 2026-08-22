from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import json
from typing import Any

from pipelines.project_underdog_phase5_source_authority_reference_implementation_v1 import AuthorityState


MODULE_ID = "project_underdog_phase5_pit_identity_and_context_evidence_reference_implementation_v1"
MODULE_VERSION = "v1"
FROZEN_DESIGN_ID = "project_underdog_phase5_pit_identity_and_context_evidence_implementation_design_v1"
LAYER_NAME = "Project Underdog Phase 5 PIT Identity And Context Evidence"


class ApplicabilityState(str, Enum):
    APPLICABLE = "applicable"
    CONDITIONALLY_APPLICABLE = "conditionally_applicable"
    UNRESOLVED = "unresolved"
    REJECTED = "rejected"


class IdentityStatus(str, Enum):
    VALID = "valid"
    CONDITIONALLY_VALID = "conditionally_valid"
    UNRESOLVED = "unresolved"
    AMBIGUOUS = "ambiguous"
    RETIRED = "retired"
    REJECTED = "rejected"


class ContextEvidenceStatus(str, Enum):
    PRESENT = "present"
    INCOMPLETE = "incomplete"
    MISSING = "missing"
    OVERLAPPING = "overlapping"
    CONFLICTING = "conflicting"


class DiagnosticCode(str, Enum):
    UNRESOLVED_IDENTITY = "UNRESOLVED_IDENTITY"
    AMBIGUOUS_IDENTITY = "AMBIGUOUS_IDENTITY"
    MISSING_CONTEXTUAL_EVIDENCE = "MISSING_CONTEXTUAL_EVIDENCE"
    OVERLAPPING_CONTEXT_INTERVALS = "OVERLAPPING_CONTEXT_INTERVALS"
    INVALID_TEMPORAL_ORDERING = "INVALID_TEMPORAL_ORDERING"
    NON_RECONSTRUCTABLE_LINEAGE = "NON_RECONSTRUCTABLE_LINEAGE"
    UNSUPPORTED_CONTINUITY = "UNSUPPORTED_CONTINUITY"
    INCOMPLETE_APPLICABILITY = "INCOMPLETE_APPLICABILITY"
    COVERAGE_GAP = "COVERAGE_GAP"
    CONFLICTING_IDENTITY_ASSOCIATION = "CONFLICTING_IDENTITY_ASSOCIATION"
    SOURCE_AUTHORITY_NOT_ACCEPTED = "SOURCE_AUTHORITY_NOT_ACCEPTED"
    TRACEABILITY_INCOMPLETE = "TRACEABILITY_INCOMPLETE"


@dataclass(frozen=True)
class Diagnostic:
    code: DiagnosticCode
    message: str
    component: str

    def to_dict(self) -> dict[str, str]:
        return {"code": self.code.value, "component": self.component, "message": self.message}


@dataclass(frozen=True)
class TimeIntervalMetadata:
    interval_id: str
    effective_start: int | None
    effective_end: int | None
    open_interval: bool = False
    unknown_interval: bool = False
    superseded_interval: bool = False
    discontinuity: bool = False
    non_reconstructable: bool = False

    def has_invalid_ordering(self) -> bool:
        return (
            self.effective_start is not None
            and self.effective_end is not None
            and self.effective_end < self.effective_start
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "discontinuity": self.discontinuity,
            "effective_end": self.effective_end,
            "effective_start": self.effective_start,
            "interval_id": self.interval_id,
            "non_reconstructable": self.non_reconstructable,
            "open_interval": self.open_interval,
            "superseded_interval": self.superseded_interval,
            "unknown_interval": self.unknown_interval,
        }


@dataclass(frozen=True)
class IdentityLineageMetadata:
    lineage_id: str
    predecessor_identity: str = ""
    successor_identity: str = ""
    continuity_supported: bool = True
    non_reconstructable: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "continuity_supported": self.continuity_supported,
            "lineage_id": self.lineage_id,
            "non_reconstructable": self.non_reconstructable,
            "predecessor_identity": self.predecessor_identity,
            "successor_identity": self.successor_identity,
        }


@dataclass(frozen=True)
class IdentityMetadata:
    canonical_identity: str
    identity_level: str
    aliases: tuple[str, ...]
    status: IdentityStatus
    synthetic_identity: bool = True

    def to_dict(self) -> dict[str, Any]:
        return {
            "aliases": list(self.aliases),
            "canonical_identity": self.canonical_identity,
            "identity_level": self.identity_level,
            "status": self.status.value,
            "synthetic_identity": self.synthetic_identity,
        }


@dataclass(frozen=True)
class IdentityApplicabilityMetadata:
    identity: IdentityMetadata
    interval: TimeIntervalMetadata
    lineage: IdentityLineageMetadata

    def to_dict(self) -> dict[str, Any]:
        return {
            "identity": self.identity.to_dict(),
            "interval": self.interval.to_dict(),
            "lineage": self.lineage.to_dict(),
        }


@dataclass(frozen=True)
class ContextEvidenceMetadata:
    context_id: str
    context_role: str
    identity_applicability_interval_id: str
    interval: TimeIntervalMetadata
    status: ContextEvidenceStatus = ContextEvidenceStatus.PRESENT
    revision: str = ""
    replacement: str = ""
    limitations: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "context_id": self.context_id,
            "context_role": self.context_role,
            "identity_applicability_interval_id": self.identity_applicability_interval_id,
            "interval": self.interval.to_dict(),
            "limitations": list(self.limitations),
            "replacement": self.replacement,
            "revision": self.revision,
            "status": self.status.value,
        }


@dataclass(frozen=True)
class PitIdentityContextRecord:
    identity_applicability: IdentityApplicabilityMetadata
    context_evidence: tuple[ContextEvidenceMetadata, ...]
    source_authority_state: AuthorityState
    source_authority_trace: dict[str, Any]
    coverage_gap: bool = False
    traceability_complete: bool = True
    fixture_id: str = ""
    module_id: str = MODULE_ID
    frozen_design_id: str = FROZEN_DESIGN_ID


@dataclass(frozen=True)
class InformationContract:
    canonical_identity_metadata: dict[str, Any]
    identity_applicability_metadata: dict[str, Any]
    lineage_metadata: dict[str, Any]
    contextual_evidence_metadata: tuple[dict[str, Any], ...]
    temporal_applicability_metadata: dict[str, Any]
    coverage_metadata: dict[str, Any]
    limitations: tuple[str, ...]
    diagnostics: tuple[Diagnostic, ...]
    source_authority_trace: dict[str, Any]
    traceability: dict[str, Any]
    exposes_raw_source_values: bool = False
    exposes_retrieval: bool = False
    performs_authority_evaluation: bool = False
    constructs_comparators: bool = False
    constructs_peer_groups: bool = False
    exposes_contextual_measurements: bool = False
    exposes_formulas: bool = False
    performs_scientific_interpretation: bool = False
    creates_candidates: bool = False
    runs_validation: bool = False
    makes_production_decisions: bool = False
    exposes_ml_inputs: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "canonical_identity_metadata": self.canonical_identity_metadata,
            "constructs_comparators": self.constructs_comparators,
            "constructs_peer_groups": self.constructs_peer_groups,
            "contextual_evidence_metadata": list(self.contextual_evidence_metadata),
            "coverage_metadata": self.coverage_metadata,
            "creates_candidates": self.creates_candidates,
            "diagnostics": [diag.to_dict() for diag in self.diagnostics],
            "exposes_contextual_measurements": self.exposes_contextual_measurements,
            "exposes_formulas": self.exposes_formulas,
            "exposes_ml_inputs": self.exposes_ml_inputs,
            "exposes_raw_source_values": self.exposes_raw_source_values,
            "exposes_retrieval": self.exposes_retrieval,
            "identity_applicability_metadata": self.identity_applicability_metadata,
            "limitations": list(self.limitations),
            "lineage_metadata": self.lineage_metadata,
            "makes_production_decisions": self.makes_production_decisions,
            "performs_authority_evaluation": self.performs_authority_evaluation,
            "performs_scientific_interpretation": self.performs_scientific_interpretation,
            "runs_validation": self.runs_validation,
            "source_authority_trace": self.source_authority_trace,
            "temporal_applicability_metadata": self.temporal_applicability_metadata,
            "traceability": self.traceability,
        }


@dataclass(frozen=True)
class PitIdentityContextResult:
    module_id: str
    module_version: str
    frozen_design_id: str
    fixture_id: str
    applicability_state: ApplicabilityState
    identity_applicability: IdentityApplicabilityMetadata
    context_evidence: tuple[ContextEvidenceMetadata, ...]
    limitations: tuple[str, ...]
    diagnostics: tuple[Diagnostic, ...]
    source_authority_trace: dict[str, Any]
    traceability: dict[str, Any]
    information_contract: InformationContract
    acquisition_performed: bool = False
    retrieval_performed: bool = False
    vendor_integration: bool = False
    authority_evaluation_performed: bool = False
    identity_construction: bool = False
    comparator_construction: bool = False
    peer_construction: bool = False
    contextual_measurement: bool = False
    formula_execution: bool = False
    scientific_interpretation: bool = False
    discovery_execution: bool = False
    validation_execution: bool = False
    production_logic: bool = False
    optimization_performed: bool = False
    ml_integration: bool = False

    def to_ordered_dict(self) -> dict[str, Any]:
        return {
            "acquisition_performed": self.acquisition_performed,
            "applicability_state": self.applicability_state.value,
            "authority_evaluation_performed": self.authority_evaluation_performed,
            "comparator_construction": self.comparator_construction,
            "context_evidence": [context.to_dict() for context in self.context_evidence],
            "contextual_measurement": self.contextual_measurement,
            "diagnostics": [diag.to_dict() for diag in self.diagnostics],
            "discovery_execution": self.discovery_execution,
            "fixture_id": self.fixture_id,
            "formula_execution": self.formula_execution,
            "frozen_design_id": self.frozen_design_id,
            "identity_applicability": self.identity_applicability.to_dict(),
            "identity_construction": self.identity_construction,
            "information_contract": self.information_contract.to_dict(),
            "limitations": list(self.limitations),
            "ml_integration": self.ml_integration,
            "module_id": self.module_id,
            "module_version": self.module_version,
            "optimization_performed": self.optimization_performed,
            "peer_construction": self.peer_construction,
            "production_logic": self.production_logic,
            "retrieval_performed": self.retrieval_performed,
            "scientific_interpretation": self.scientific_interpretation,
            "source_authority_trace": self.source_authority_trace,
            "traceability": self.traceability,
            "validation_execution": self.validation_execution,
            "vendor_integration": self.vendor_integration,
        }

    def stable_json(self) -> str:
        return json.dumps(self.to_ordered_dict(), sort_keys=True, separators=(",", ":"))


@dataclass(frozen=True)
class PitIdentityContextFixture:
    fixture_id: str
    description: str
    record: PitIdentityContextRecord
    expected_applicability_state: ApplicabilityState
    expected_diagnostic_codes: tuple[DiagnosticCode, ...] = ()
    expected_limitations: tuple[str, ...] = ()


def _diag(code: DiagnosticCode, component: str, message: str) -> Diagnostic:
    return Diagnostic(code=code, component=component, message=message)


def _trace(record: PitIdentityContextRecord) -> dict[str, Any]:
    return {
        "context_ids": [context.context_id for context in record.context_evidence],
        "fixture_id": record.fixture_id,
        "frozen_design_id": record.frozen_design_id,
        "governing_design": "project_underdog_phase5_pit_identity_and_context_evidence_implementation_design_v1",
        "identity_interval_id": record.identity_applicability.interval.interval_id,
        "identity_level": record.identity_applicability.identity.identity_level,
        "layer_name": LAYER_NAME,
        "lineage_id": record.identity_applicability.lineage.lineage_id,
        "source_authority_state": record.source_authority_state.value,
        "source_authority_trace": record.source_authority_trace,
    }


def _final_result(
    record: PitIdentityContextRecord,
    state: ApplicabilityState,
    diagnostics: tuple[Diagnostic, ...],
    limitations: tuple[str, ...],
) -> PitIdentityContextResult:
    traceability = _trace(record)
    contract = InformationContract(
        canonical_identity_metadata=record.identity_applicability.identity.to_dict(),
        identity_applicability_metadata=record.identity_applicability.to_dict(),
        lineage_metadata=record.identity_applicability.lineage.to_dict(),
        contextual_evidence_metadata=tuple(context.to_dict() for context in record.context_evidence),
        temporal_applicability_metadata=record.identity_applicability.interval.to_dict(),
        coverage_metadata={"coverage_gap": record.coverage_gap},
        limitations=limitations,
        diagnostics=diagnostics,
        source_authority_trace=record.source_authority_trace,
        traceability=traceability,
    )
    return PitIdentityContextResult(
        module_id=MODULE_ID,
        module_version=MODULE_VERSION,
        frozen_design_id=FROZEN_DESIGN_ID,
        fixture_id=record.fixture_id,
        applicability_state=state,
        identity_applicability=record.identity_applicability,
        context_evidence=record.context_evidence,
        limitations=limitations,
        diagnostics=diagnostics,
        source_authority_trace=record.source_authority_trace,
        traceability=traceability,
        information_contract=contract,
    )


def evaluate_pit_identity_context(record: PitIdentityContextRecord) -> PitIdentityContextResult:
    diagnostics: list[Diagnostic] = []
    limitations: list[str] = []

    if record.source_authority_state not in (AuthorityState.AUTHORITATIVE, AuthorityState.CONDITIONAL):
        diagnostics.append(
            _diag(
                DiagnosticCode.SOURCE_AUTHORITY_NOT_ACCEPTED,
                "source_authority",
                "Source Authority state is not accepted for authoritative PIT identity/context applicability.",
            )
        )

    identity = record.identity_applicability.identity
    interval = record.identity_applicability.interval
    lineage = record.identity_applicability.lineage

    if identity.status == IdentityStatus.UNRESOLVED:
        diagnostics.append(_diag(DiagnosticCode.UNRESOLVED_IDENTITY, "identity", "Identity is unresolved."))
    if identity.status == IdentityStatus.AMBIGUOUS:
        diagnostics.append(_diag(DiagnosticCode.AMBIGUOUS_IDENTITY, "identity", "Identity is ambiguous."))
    if identity.status == IdentityStatus.REJECTED:
        diagnostics.append(_diag(DiagnosticCode.UNRESOLVED_IDENTITY, "identity", "Identity is rejected."))
    if identity.status == IdentityStatus.CONDITIONALLY_VALID:
        limitations.append("identity conditionally valid")
    if identity.status == IdentityStatus.RETIRED:
        limitations.append("identity retired after applicability interval")

    if interval.has_invalid_ordering() or any(context.interval.has_invalid_ordering() for context in record.context_evidence):
        diagnostics.append(
            _diag(DiagnosticCode.INVALID_TEMPORAL_ORDERING, "temporal", "Identity or context interval has invalid temporal ordering.")
        )
    if interval.unknown_interval or any(context.interval.unknown_interval for context in record.context_evidence):
        diagnostics.append(_diag(DiagnosticCode.INCOMPLETE_APPLICABILITY, "temporal", "Identity or context interval is unknown."))
    if interval.non_reconstructable or lineage.non_reconstructable or any(context.interval.non_reconstructable for context in record.context_evidence):
        diagnostics.append(
            _diag(
                DiagnosticCode.NON_RECONSTRUCTABLE_LINEAGE,
                "lineage",
                "Identity or context applicability history is non-reconstructable.",
            )
        )
    if interval.discontinuity or any(context.interval.discontinuity for context in record.context_evidence):
        limitations.append("discontinuous applicability interval")
    if interval.superseded_interval or any(context.interval.superseded_interval for context in record.context_evidence):
        limitations.append("superseded interval")
    if interval.open_interval or any(context.interval.open_interval for context in record.context_evidence):
        limitations.append("open interval")

    if not lineage.continuity_supported:
        diagnostics.append(
            _diag(DiagnosticCode.UNSUPPORTED_CONTINUITY, "lineage", "Identity continuity is not supported by lineage metadata.")
        )

    if not record.context_evidence:
        diagnostics.append(
            _diag(DiagnosticCode.MISSING_CONTEXTUAL_EVIDENCE, "context", "No contextual evidence is registered.")
        )

    for context in record.context_evidence:
        if not context.identity_applicability_interval_id or context.identity_applicability_interval_id != interval.interval_id:
            diagnostics.append(
                _diag(
                    DiagnosticCode.CONFLICTING_IDENTITY_ASSOCIATION,
                    "association",
                    "Context evidence does not reference exactly the evaluated identity applicability interval.",
                )
            )
        if context.status == ContextEvidenceStatus.MISSING:
            diagnostics.append(
                _diag(DiagnosticCode.MISSING_CONTEXTUAL_EVIDENCE, "context", "Contextual evidence is missing.")
            )
        if context.status == ContextEvidenceStatus.OVERLAPPING:
            diagnostics.append(
                _diag(DiagnosticCode.OVERLAPPING_CONTEXT_INTERVALS, "context", "Context intervals overlap without governed replacement.")
            )
        if context.status == ContextEvidenceStatus.CONFLICTING:
            diagnostics.append(
                _diag(DiagnosticCode.CONFLICTING_IDENTITY_ASSOCIATION, "association", "Context association is conflicting.")
            )
        if context.status == ContextEvidenceStatus.INCOMPLETE:
            diagnostics.append(
                _diag(DiagnosticCode.INCOMPLETE_APPLICABILITY, "context", "Context applicability metadata is incomplete.")
            )
        limitations.extend(context.limitations)

    if record.coverage_gap:
        diagnostics.append(_diag(DiagnosticCode.COVERAGE_GAP, "coverage", "Context coverage gap is present."))

    if not record.traceability_complete:
        diagnostics.append(_diag(DiagnosticCode.TRACEABILITY_INCOMPLETE, "traceability", "Traceability is incomplete."))

    diagnostic_tuple = tuple(diagnostics)
    limitation_tuple = tuple(dict.fromkeys(limitations))
    diagnostic_codes = {diag.code for diag in diagnostic_tuple}

    if (
        DiagnosticCode.TRACEABILITY_INCOMPLETE in diagnostic_codes
        or DiagnosticCode.SOURCE_AUTHORITY_NOT_ACCEPTED in diagnostic_codes
        or DiagnosticCode.INVALID_TEMPORAL_ORDERING in diagnostic_codes
        or DiagnosticCode.NON_RECONSTRUCTABLE_LINEAGE in diagnostic_codes
    ):
        state = ApplicabilityState.REJECTED
    elif diagnostic_tuple:
        state = ApplicabilityState.UNRESOLVED
    elif limitation_tuple:
        state = ApplicabilityState.CONDITIONALLY_APPLICABLE
    else:
        state = ApplicabilityState.APPLICABLE

    return _final_result(record, state, diagnostic_tuple, limitation_tuple)


def _interval(interval_id: str, start: int | None = 1, end: int | None = 10, **kwargs: Any) -> TimeIntervalMetadata:
    return TimeIntervalMetadata(interval_id=interval_id, effective_start=start, effective_end=end, **kwargs)


def _base_record(fixture_id: str) -> PitIdentityContextRecord:
    interval = _interval(f"identity_interval_{fixture_id}")
    return PitIdentityContextRecord(
        fixture_id=fixture_id,
        source_authority_state=AuthorityState.AUTHORITATIVE,
        source_authority_trace={"source_authority_fixture": "synthetic_authoritative"},
        identity_applicability=IdentityApplicabilityMetadata(
            identity=IdentityMetadata(
                canonical_identity=f"synthetic_identity_{fixture_id}",
                identity_level="security",
                aliases=(),
                status=IdentityStatus.VALID,
            ),
            interval=interval,
            lineage=IdentityLineageMetadata(lineage_id=f"lineage_{fixture_id}"),
        ),
        context_evidence=(
            ContextEvidenceMetadata(
                context_id=f"context_{fixture_id}",
                context_role="historical_classification_context",
                identity_applicability_interval_id=interval.interval_id,
                interval=_interval(f"context_interval_{fixture_id}"),
            ),
        ),
    )


def canonical_pit_identity_context_fixtures() -> tuple[PitIdentityContextFixture, ...]:
    normal = _base_record("PIC1_normal_identity")
    alias = PitIdentityContextRecord(
        **{
            **_base_record("PIC2_alias_identity").__dict__,
            "identity_applicability": IdentityApplicabilityMetadata(
                identity=IdentityMetadata(
                    canonical_identity="synthetic_identity_alias",
                    identity_level="security",
                    aliases=("SYN.A", "SYN-A"),
                    status=IdentityStatus.VALID,
                ),
                interval=_interval("identity_interval_PIC2_alias_identity"),
                lineage=IdentityLineageMetadata(lineage_id="lineage_PIC2_alias_identity"),
            ),
            "context_evidence": (
                ContextEvidenceMetadata(
                    context_id="context_PIC2_alias_identity",
                    context_role="historical_classification_context",
                    identity_applicability_interval_id="identity_interval_PIC2_alias_identity",
                    interval=_interval("context_interval_PIC2_alias_identity"),
                ),
            ),
        }
    )
    predecessor = PitIdentityContextRecord(
        **{
            **_base_record("PIC3_successor_predecessor").__dict__,
            "identity_applicability": IdentityApplicabilityMetadata(
                identity=IdentityMetadata("synthetic_successor", "security", (), IdentityStatus.VALID),
                interval=_interval("identity_interval_PIC3_successor_predecessor"),
                lineage=IdentityLineageMetadata(
                    lineage_id="lineage_PIC3_successor_predecessor",
                    predecessor_identity="synthetic_predecessor",
                    successor_identity="synthetic_successor",
                ),
            ),
            "context_evidence": (
                ContextEvidenceMetadata(
                    context_id="context_PIC3_successor_predecessor",
                    context_role="event_context",
                    identity_applicability_interval_id="identity_interval_PIC3_successor_predecessor",
                    interval=_interval("context_interval_PIC3_successor_predecessor"),
                ),
            ),
        }
    )
    retired = PitIdentityContextRecord(
        **{
            **_base_record("PIC4_retired_identity").__dict__,
            "identity_applicability": IdentityApplicabilityMetadata(
                identity=IdentityMetadata("synthetic_retired", "security", (), IdentityStatus.RETIRED),
                interval=_interval("identity_interval_PIC4_retired_identity"),
                lineage=IdentityLineageMetadata("lineage_PIC4_retired_identity"),
            ),
            "context_evidence": (
                ContextEvidenceMetadata(
                    "context_PIC4_retired_identity",
                    "listing_context",
                    "identity_interval_PIC4_retired_identity",
                    _interval("context_interval_PIC4_retired_identity"),
                ),
            ),
        }
    )
    unresolved = PitIdentityContextRecord(
        **{
            **_base_record("PIC5_unresolved_identity").__dict__,
            "identity_applicability": IdentityApplicabilityMetadata(
                identity=IdentityMetadata("synthetic_unresolved", "security", (), IdentityStatus.UNRESOLVED),
                interval=_interval("identity_interval_PIC5_unresolved_identity"),
                lineage=IdentityLineageMetadata("lineage_PIC5_unresolved_identity"),
            ),
            "context_evidence": (
                ContextEvidenceMetadata(
                    "context_PIC5_unresolved_identity",
                    "historical_classification_context",
                    "identity_interval_PIC5_unresolved_identity",
                    _interval("context_interval_PIC5_unresolved_identity"),
                ),
            ),
        }
    )
    ambiguous = PitIdentityContextRecord(
        **{
            **_base_record("PIC6_ambiguous_identity").__dict__,
            "identity_applicability": IdentityApplicabilityMetadata(
                identity=IdentityMetadata("synthetic_ambiguous", "security", (), IdentityStatus.AMBIGUOUS),
                interval=_interval("identity_interval_PIC6_ambiguous_identity"),
                lineage=IdentityLineageMetadata("lineage_PIC6_ambiguous_identity"),
            ),
            "context_evidence": (
                ContextEvidenceMetadata(
                    "context_PIC6_ambiguous_identity",
                    "historical_classification_context",
                    "identity_interval_PIC6_ambiguous_identity",
                    _interval("context_interval_PIC6_ambiguous_identity"),
                ),
            ),
        }
    )
    valid_interval = _base_record("PIC7_valid_applicability_interval")
    missing_applicability = PitIdentityContextRecord(
        **{
            **_base_record("PIC8_missing_applicability").__dict__,
            "identity_applicability": IdentityApplicabilityMetadata(
                identity=IdentityMetadata("synthetic_missing_applicability", "security", (), IdentityStatus.VALID),
                interval=_interval("identity_interval_PIC8_missing_applicability", None, None, unknown_interval=True),
                lineage=IdentityLineageMetadata("lineage_PIC8_missing_applicability"),
            ),
            "context_evidence": (
                ContextEvidenceMetadata(
                    "context_PIC8_missing_applicability",
                    "historical_classification_context",
                    "identity_interval_PIC8_missing_applicability",
                    _interval("context_interval_PIC8_missing_applicability"),
                ),
            ),
        }
    )
    overlapping = PitIdentityContextRecord(
        **{
            **_base_record("PIC9_overlapping_applicability").__dict__,
            "context_evidence": (
                ContextEvidenceMetadata(
                    "context_PIC9_overlapping_applicability",
                    "historical_classification_context",
                    "identity_interval_PIC9_overlapping_applicability",
                    _interval("context_interval_PIC9_overlapping_applicability"),
                    status=ContextEvidenceStatus.OVERLAPPING,
                ),
            ),
        }
    )
    coverage_gap = PitIdentityContextRecord(**{**_base_record("PIC10_coverage_gap").__dict__, "coverage_gap": True})
    non_reconstructable = PitIdentityContextRecord(
        **{
            **_base_record("PIC11_non_reconstructable_interval").__dict__,
            "identity_applicability": IdentityApplicabilityMetadata(
                identity=IdentityMetadata("synthetic_non_reconstructable", "security", (), IdentityStatus.VALID),
                interval=_interval("identity_interval_PIC11_non_reconstructable_interval", non_reconstructable=True),
                lineage=IdentityLineageMetadata("lineage_PIC11_non_reconstructable_interval"),
            ),
            "context_evidence": (
                ContextEvidenceMetadata(
                    "context_PIC11_non_reconstructable_interval",
                    "historical_classification_context",
                    "identity_interval_PIC11_non_reconstructable_interval",
                    _interval("context_interval_PIC11_non_reconstructable_interval"),
                ),
            ),
        }
    )
    missing_context = PitIdentityContextRecord(**{**_base_record("PIC12_missing_context").__dict__, "context_evidence": ()})
    conflicting = PitIdentityContextRecord(
        **{
            **_base_record("PIC13_conflicting_association").__dict__,
            "context_evidence": (
                ContextEvidenceMetadata(
                    "context_PIC13_conflicting_association",
                    "historical_classification_context",
                    "different_identity_interval",
                    _interval("context_interval_PIC13_conflicting_association"),
                ),
            ),
        }
    )
    incomplete_trace = PitIdentityContextRecord(
        **{**_base_record("PIC14_incomplete_traceability").__dict__, "traceability_complete": False}
    )

    return (
        PitIdentityContextFixture("PIC1_normal_identity", "Normal identity.", normal, ApplicabilityState.APPLICABLE),
        PitIdentityContextFixture("PIC2_alias_identity", "Alias identity.", alias, ApplicabilityState.APPLICABLE),
        PitIdentityContextFixture("PIC3_successor_predecessor", "Successor/predecessor lineage.", predecessor, ApplicabilityState.APPLICABLE),
        PitIdentityContextFixture(
            "PIC4_retired_identity",
            "Retired identity.",
            retired,
            ApplicabilityState.CONDITIONALLY_APPLICABLE,
            expected_limitations=("identity retired after applicability interval",),
        ),
        PitIdentityContextFixture(
            "PIC5_unresolved_identity",
            "Unresolved identity.",
            unresolved,
            ApplicabilityState.UNRESOLVED,
            (DiagnosticCode.UNRESOLVED_IDENTITY,),
        ),
        PitIdentityContextFixture(
            "PIC6_ambiguous_identity",
            "Ambiguous identity.",
            ambiguous,
            ApplicabilityState.UNRESOLVED,
            (DiagnosticCode.AMBIGUOUS_IDENTITY,),
        ),
        PitIdentityContextFixture("PIC7_valid_applicability_interval", "Valid applicability interval.", valid_interval, ApplicabilityState.APPLICABLE),
        PitIdentityContextFixture(
            "PIC8_missing_applicability",
            "Missing applicability interval.",
            missing_applicability,
            ApplicabilityState.UNRESOLVED,
            (DiagnosticCode.INCOMPLETE_APPLICABILITY,),
        ),
        PitIdentityContextFixture(
            "PIC9_overlapping_applicability",
            "Overlapping applicability.",
            overlapping,
            ApplicabilityState.UNRESOLVED,
            (DiagnosticCode.OVERLAPPING_CONTEXT_INTERVALS,),
        ),
        PitIdentityContextFixture(
            "PIC10_coverage_gap",
            "Coverage gap.",
            coverage_gap,
            ApplicabilityState.UNRESOLVED,
            (DiagnosticCode.COVERAGE_GAP,),
        ),
        PitIdentityContextFixture(
            "PIC11_non_reconstructable_interval",
            "Non-reconstructable interval.",
            non_reconstructable,
            ApplicabilityState.REJECTED,
            (DiagnosticCode.NON_RECONSTRUCTABLE_LINEAGE,),
        ),
        PitIdentityContextFixture(
            "PIC12_missing_context",
            "Missing contextual evidence.",
            missing_context,
            ApplicabilityState.UNRESOLVED,
            (DiagnosticCode.MISSING_CONTEXTUAL_EVIDENCE,),
        ),
        PitIdentityContextFixture(
            "PIC13_conflicting_association",
            "Conflicting identity association.",
            conflicting,
            ApplicabilityState.UNRESOLVED,
            (DiagnosticCode.CONFLICTING_IDENTITY_ASSOCIATION,),
        ),
        PitIdentityContextFixture(
            "PIC14_incomplete_traceability",
            "Incomplete traceability.",
            incomplete_trace,
            ApplicabilityState.REJECTED,
            (DiagnosticCode.TRACEABILITY_INCOMPLETE,),
        ),
    )


def pit_identity_context_guardrail_manifest() -> dict[str, bool]:
    return {
        "synthetic_metadata_only": True,
        "acquisition_performed": False,
        "retrieval_performed": False,
        "vendor_integration": False,
        "authority_evaluation": False,
        "identity_construction": False,
        "comparator_construction": False,
        "peer_construction": False,
        "contextual_measurement": False,
        "formula_execution": False,
        "scientific_interpretation": False,
        "discovery_executed": False,
        "validation_executed": False,
        "production_logic": False,
        "optimization_performed": False,
        "ml_integration": False,
    }
