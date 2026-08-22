from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import json
from typing import Any


MODULE_ID = "project_underdog_phase5_comparator_construction_reference_implementation_v1"
MODULE_VERSION = "v1"
FROZEN_DESIGN_ID = "project_underdog_phase5_comparator_construction_implementation_design_v1"
LAYER_NAME = "Project Underdog Phase 5 Comparator Construction"


class ComparatorEligibilityState(str, Enum):
    COMPARATOR_ELIGIBLE = "COMPARATOR_ELIGIBLE"
    COMPARATOR_CONDITIONALLY_ELIGIBLE = "COMPARATOR_CONDITIONALLY_ELIGIBLE"
    COMPARATOR_UNRESOLVED = "COMPARATOR_UNRESOLVED"
    COMPARATOR_INELIGIBLE = "COMPARATOR_INELIGIBLE"
    COMPARATOR_EXCLUDED = "COMPARATOR_EXCLUDED"
    INSUFFICIENT_COMPARATOR_EVIDENCE = "INSUFFICIENT_COMPARATOR_EVIDENCE"


class TemporalApplicabilityState(str, Enum):
    VALID_OVERLAP = "valid_overlap"
    PARTIAL_OVERLAP = "partial_overlap"
    NO_OVERLAP = "no_overlap"
    UNRESOLVED = "unresolved"


class ComparatorDiagnosticCode(str, Enum):
    UNRESOLVED_COMPARATOR = "UNRESOLVED_COMPARATOR"
    CONFLICTING_COMPARATOR = "CONFLICTING_COMPARATOR"
    MISSING_COMPARATOR_APPLICABILITY = "MISSING_COMPARATOR_APPLICABILITY"
    INVALID_TEMPORAL_OVERLAP = "INVALID_TEMPORAL_OVERLAP"
    INSUFFICIENT_COMPARATOR_COVERAGE = "INSUFFICIENT_COMPARATOR_COVERAGE"
    UNSUPPORTED_COMPARATOR_RELATIONSHIP = "UNSUPPORTED_COMPARATOR_RELATIONSHIP"
    EXCLUDED_COMPARATOR = "EXCLUDED_COMPARATOR"
    INCOMPLETE_COMPARATOR_TRACEABILITY = "INCOMPLETE_COMPARATOR_TRACEABILITY"
    UNRESOLVED_COMPARATOR_LINEAGE = "UNRESOLVED_COMPARATOR_LINEAGE"
    DUPLICATE_EXPOSURE_UNRESOLVED = "DUPLICATE_EXPOSURE_UNRESOLVED"
    COMPARATOR_CONTEXT_INSUFFICIENT = "COMPARATOR_CONTEXT_INSUFFICIENT"


@dataclass(frozen=True)
class ComparatorDiagnostic:
    code: ComparatorDiagnosticCode
    component: str
    message: str

    def to_dict(self) -> dict[str, str]:
        return {"code": self.code.value, "component": self.component, "message": self.message}


@dataclass(frozen=True)
class ComparatorIntervalMetadata:
    interval_id: str
    identity_id: str
    effective_start: int | None
    effective_end: int | None
    open_interval: bool = False
    unknown_interval: bool = False
    superseded_interval: bool = False
    expired_interval: bool = False
    discontinuity: bool = False

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
            "expired_interval": self.expired_interval,
            "identity_id": self.identity_id,
            "interval_id": self.interval_id,
            "open_interval": self.open_interval,
            "superseded_interval": self.superseded_interval,
            "unknown_interval": self.unknown_interval,
        }


@dataclass(frozen=True)
class IdentityApplicabilityReference:
    identity_id: str
    applicability_interval_ids: tuple[str, ...]
    interval: ComparatorIntervalMetadata
    pit_identity_trace: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "applicability_interval_ids": list(self.applicability_interval_ids),
            "identity_id": self.identity_id,
            "interval": self.interval.to_dict(),
            "pit_identity_trace": self.pit_identity_trace,
        }


@dataclass(frozen=True)
class ComparatorRelationshipMetadata:
    relationship_id: str
    relationship_type: str
    target_identity_id: str
    comparator_identity_id: str
    target_interval_id: str
    comparator_interval_id: str
    supported_relationship: bool = True
    unresolved_relationship: bool = False
    conflicting_relationship: bool = False
    excluded_relationship: bool = False
    self_comparison_prohibited: bool = True
    lineage_unresolved: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "comparator_identity_id": self.comparator_identity_id,
            "comparator_interval_id": self.comparator_interval_id,
            "conflicting_relationship": self.conflicting_relationship,
            "excluded_relationship": self.excluded_relationship,
            "lineage_unresolved": self.lineage_unresolved,
            "relationship_id": self.relationship_id,
            "relationship_type": self.relationship_type,
            "self_comparison_prohibited": self.self_comparison_prohibited,
            "supported_relationship": self.supported_relationship,
            "target_identity_id": self.target_identity_id,
            "target_interval_id": self.target_interval_id,
            "unresolved_relationship": self.unresolved_relationship,
        }


@dataclass(frozen=True)
class ComparatorCoverageMetadata:
    sufficient: bool = True
    conditionally_governed: bool = False
    coverage_gap: bool = False

    def to_dict(self) -> dict[str, bool]:
        return {
            "conditionally_governed": self.conditionally_governed,
            "coverage_gap": self.coverage_gap,
            "sufficient": self.sufficient,
        }


@dataclass(frozen=True)
class ComparatorContextSupportMetadata:
    sufficient: bool = True
    conditionally_governed: bool = False
    context_missing: bool = False

    def to_dict(self) -> dict[str, bool]:
        return {
            "conditionally_governed": self.conditionally_governed,
            "context_missing": self.context_missing,
            "sufficient": self.sufficient,
        }


@dataclass(frozen=True)
class ComparatorConstructionRecord:
    target: IdentityApplicabilityReference
    comparator: IdentityApplicabilityReference
    relationship: ComparatorRelationshipMetadata
    coverage: ComparatorCoverageMetadata
    context_support: ComparatorContextSupportMetadata
    source_authority_trace: dict[str, Any]
    pit_identity_trace: dict[str, Any]
    duplicate_exposure: bool = False
    traceability_complete: bool = True
    limitations: tuple[str, ...] = ()
    fixture_id: str = ""
    module_id: str = MODULE_ID
    frozen_design_id: str = FROZEN_DESIGN_ID


@dataclass(frozen=True)
class ComparatorInformationContract:
    relationship_metadata: dict[str, Any]
    target_applicability_metadata: dict[str, Any]
    comparator_applicability_metadata: dict[str, Any]
    eligibility_state: ComparatorEligibilityState
    temporal_applicability_metadata: dict[str, Any]
    coverage_metadata: dict[str, Any]
    context_support_metadata: dict[str, Any]
    limitations: tuple[str, ...]
    diagnostics: tuple[ComparatorDiagnostic, ...]
    source_authority_trace: dict[str, Any]
    pit_identity_trace: dict[str, Any]
    traceability: dict[str, Any]
    exposes_raw_source_values: bool = False
    exposes_retrieval_instructions: bool = False
    performs_authority_evaluation: bool = False
    performs_identity_construction: bool = False
    performs_identity_resolution: bool = False
    ranks_comparators: bool = False
    exposes_similarity_scores: bool = False
    performs_peer_discovery: bool = False
    exposes_contextual_measurements: bool = False
    exposes_formulas: bool = False
    performs_scientific_interpretation: bool = False
    creates_candidates: bool = False
    constructs_panels: bool = False
    computes_ic: bool = False
    runs_validation: bool = False
    makes_production_decisions: bool = False
    exposes_ml_features: bool = False
    exposes_ml_labels: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "comparator_applicability_metadata": self.comparator_applicability_metadata,
            "computes_ic": self.computes_ic,
            "constructs_panels": self.constructs_panels,
            "context_support_metadata": self.context_support_metadata,
            "coverage_metadata": self.coverage_metadata,
            "creates_candidates": self.creates_candidates,
            "diagnostics": [diag.to_dict() for diag in self.diagnostics],
            "eligibility_state": self.eligibility_state.value,
            "exposes_contextual_measurements": self.exposes_contextual_measurements,
            "exposes_formulas": self.exposes_formulas,
            "exposes_ml_features": self.exposes_ml_features,
            "exposes_ml_labels": self.exposes_ml_labels,
            "exposes_raw_source_values": self.exposes_raw_source_values,
            "exposes_retrieval_instructions": self.exposes_retrieval_instructions,
            "exposes_similarity_scores": self.exposes_similarity_scores,
            "limitations": list(self.limitations),
            "makes_production_decisions": self.makes_production_decisions,
            "performs_authority_evaluation": self.performs_authority_evaluation,
            "performs_identity_construction": self.performs_identity_construction,
            "performs_identity_resolution": self.performs_identity_resolution,
            "performs_peer_discovery": self.performs_peer_discovery,
            "performs_scientific_interpretation": self.performs_scientific_interpretation,
            "pit_identity_trace": self.pit_identity_trace,
            "ranks_comparators": self.ranks_comparators,
            "relationship_metadata": self.relationship_metadata,
            "runs_validation": self.runs_validation,
            "source_authority_trace": self.source_authority_trace,
            "target_applicability_metadata": self.target_applicability_metadata,
            "temporal_applicability_metadata": self.temporal_applicability_metadata,
            "traceability": self.traceability,
        }


@dataclass(frozen=True)
class ComparatorConstructionResult:
    module_id: str
    module_version: str
    frozen_design_id: str
    fixture_id: str
    eligibility_state: ComparatorEligibilityState
    temporal_applicability_state: TemporalApplicabilityState
    relationship: ComparatorRelationshipMetadata
    target: IdentityApplicabilityReference
    comparator: IdentityApplicabilityReference
    coverage: ComparatorCoverageMetadata
    context_support: ComparatorContextSupportMetadata
    limitations: tuple[str, ...]
    diagnostics: tuple[ComparatorDiagnostic, ...]
    source_authority_trace: dict[str, Any]
    pit_identity_trace: dict[str, Any]
    traceability: dict[str, Any]
    information_contract: ComparatorInformationContract
    acquisition_performed: bool = False
    retrieval_performed: bool = False
    vendor_integration: bool = False
    authority_evaluation_performed: bool = False
    identity_construction: bool = False
    identity_resolution: bool = False
    scientific_similarity: bool = False
    comparator_ranking: bool = False
    peer_discovery: bool = False
    contextual_measurement: bool = False
    formula_execution: bool = False
    candidate_generation: bool = False
    panel_generation: bool = False
    discovery_execution: bool = False
    validation_execution: bool = False
    ic_computation: bool = False
    production_logic: bool = False
    optimization_performed: bool = False
    ml_integration: bool = False

    def to_ordered_dict(self) -> dict[str, Any]:
        return {
            "acquisition_performed": self.acquisition_performed,
            "authority_evaluation_performed": self.authority_evaluation_performed,
            "candidate_generation": self.candidate_generation,
            "comparator": self.comparator.to_dict(),
            "comparator_ranking": self.comparator_ranking,
            "context_support": self.context_support.to_dict(),
            "contextual_measurement": self.contextual_measurement,
            "coverage": self.coverage.to_dict(),
            "diagnostics": [diag.to_dict() for diag in self.diagnostics],
            "discovery_execution": self.discovery_execution,
            "eligibility_state": self.eligibility_state.value,
            "fixture_id": self.fixture_id,
            "formula_execution": self.formula_execution,
            "frozen_design_id": self.frozen_design_id,
            "ic_computation": self.ic_computation,
            "identity_construction": self.identity_construction,
            "identity_resolution": self.identity_resolution,
            "information_contract": self.information_contract.to_dict(),
            "limitations": list(self.limitations),
            "ml_integration": self.ml_integration,
            "module_id": self.module_id,
            "module_version": self.module_version,
            "optimization_performed": self.optimization_performed,
            "panel_generation": self.panel_generation,
            "peer_discovery": self.peer_discovery,
            "pit_identity_trace": self.pit_identity_trace,
            "production_logic": self.production_logic,
            "relationship": self.relationship.to_dict(),
            "retrieval_performed": self.retrieval_performed,
            "scientific_similarity": self.scientific_similarity,
            "source_authority_trace": self.source_authority_trace,
            "target": self.target.to_dict(),
            "temporal_applicability_state": self.temporal_applicability_state.value,
            "traceability": self.traceability,
            "validation_execution": self.validation_execution,
            "vendor_integration": self.vendor_integration,
        }

    def stable_json(self) -> str:
        return json.dumps(self.to_ordered_dict(), sort_keys=True, separators=(",", ":"))


@dataclass(frozen=True)
class ComparatorConstructionFixture:
    fixture_id: str
    description: str
    record: ComparatorConstructionRecord
    expected_eligibility_state: ComparatorEligibilityState
    expected_temporal_state: TemporalApplicabilityState
    expected_diagnostic_codes: tuple[ComparatorDiagnosticCode, ...] = ()
    expected_limitations: tuple[str, ...] = ()


def _diag(code: ComparatorDiagnosticCode, component: str, message: str) -> ComparatorDiagnostic:
    return ComparatorDiagnostic(code=code, component=component, message=message)


def _interval(
    identity_id: str,
    interval_id: str,
    start: int | None = 1,
    end: int | None = 10,
    **kwargs: Any,
) -> ComparatorIntervalMetadata:
    return ComparatorIntervalMetadata(interval_id, identity_id, start, end, **kwargs)


def _ref(identity_id: str, interval: ComparatorIntervalMetadata, interval_ids: tuple[str, ...] | None = None) -> IdentityApplicabilityReference:
    return IdentityApplicabilityReference(
        identity_id=identity_id,
        applicability_interval_ids=interval_ids if interval_ids is not None else (interval.interval_id,),
        interval=interval,
        pit_identity_trace={"pit_identity_fixture": identity_id, "identity_interval_id": interval.interval_id},
    )


def _overlap_state(target: ComparatorIntervalMetadata, comparator: ComparatorIntervalMetadata) -> TemporalApplicabilityState:
    if target.unknown_interval or comparator.unknown_interval:
        return TemporalApplicabilityState.UNRESOLVED
    if target.has_invalid_ordering() or comparator.has_invalid_ordering():
        return TemporalApplicabilityState.NO_OVERLAP
    if target.effective_start is None or comparator.effective_start is None:
        return TemporalApplicabilityState.UNRESOLVED
    target_end = target.effective_end
    comparator_end = comparator.effective_end
    if target_end is None or comparator_end is None:
        return TemporalApplicabilityState.PARTIAL_OVERLAP
    if target_end < comparator.effective_start or comparator_end < target.effective_start:
        return TemporalApplicabilityState.NO_OVERLAP
    if target.effective_start == comparator.effective_start and target_end == comparator_end:
        return TemporalApplicabilityState.VALID_OVERLAP
    return TemporalApplicabilityState.PARTIAL_OVERLAP


def _trace(record: ComparatorConstructionRecord, temporal_state: TemporalApplicabilityState) -> dict[str, Any]:
    return {
        "comparator_identity_id": record.comparator.identity_id,
        "comparator_interval_id": record.comparator.interval.interval_id,
        "fixture_id": record.fixture_id,
        "frozen_design_id": record.frozen_design_id,
        "governing_design": FROZEN_DESIGN_ID,
        "layer_name": LAYER_NAME,
        "pit_identity_trace": record.pit_identity_trace,
        "relationship_id": record.relationship.relationship_id,
        "relationship_type": record.relationship.relationship_type,
        "source_authority_trace": record.source_authority_trace,
        "target_identity_id": record.target.identity_id,
        "target_interval_id": record.target.interval.interval_id,
        "temporal_applicability_state": temporal_state.value,
    }


def _final_result(
    record: ComparatorConstructionRecord,
    eligibility_state: ComparatorEligibilityState,
    temporal_state: TemporalApplicabilityState,
    diagnostics: tuple[ComparatorDiagnostic, ...],
    limitations: tuple[str, ...],
) -> ComparatorConstructionResult:
    traceability = _trace(record, temporal_state)
    contract = ComparatorInformationContract(
        relationship_metadata=record.relationship.to_dict(),
        target_applicability_metadata=record.target.to_dict(),
        comparator_applicability_metadata=record.comparator.to_dict(),
        eligibility_state=eligibility_state,
        temporal_applicability_metadata={
            "comparator_interval": record.comparator.interval.to_dict(),
            "target_interval": record.target.interval.to_dict(),
            "temporal_applicability_state": temporal_state.value,
        },
        coverage_metadata=record.coverage.to_dict(),
        context_support_metadata=record.context_support.to_dict(),
        limitations=limitations,
        diagnostics=diagnostics,
        source_authority_trace=record.source_authority_trace,
        pit_identity_trace=record.pit_identity_trace,
        traceability=traceability,
    )
    return ComparatorConstructionResult(
        module_id=MODULE_ID,
        module_version=MODULE_VERSION,
        frozen_design_id=FROZEN_DESIGN_ID,
        fixture_id=record.fixture_id,
        eligibility_state=eligibility_state,
        temporal_applicability_state=temporal_state,
        relationship=record.relationship,
        target=record.target,
        comparator=record.comparator,
        coverage=record.coverage,
        context_support=record.context_support,
        limitations=limitations,
        diagnostics=diagnostics,
        source_authority_trace=record.source_authority_trace,
        pit_identity_trace=record.pit_identity_trace,
        traceability=traceability,
        information_contract=contract,
    )


def evaluate_comparator_construction(record: ComparatorConstructionRecord) -> ComparatorConstructionResult:
    diagnostics: list[ComparatorDiagnostic] = []
    limitations: list[str] = list(record.limitations)

    target = record.target
    comparator = record.comparator
    relationship = record.relationship
    temporal_state = _overlap_state(target.interval, comparator.interval)

    if len(target.applicability_interval_ids) != 1:
        diagnostics.append(_diag(ComparatorDiagnosticCode.MISSING_COMPARATOR_APPLICABILITY, "target", "Target must reference exactly one applicability interval."))
    if len(comparator.applicability_interval_ids) != 1:
        diagnostics.append(_diag(ComparatorDiagnosticCode.MISSING_COMPARATOR_APPLICABILITY, "comparator", "Comparator must reference exactly one applicability interval."))
    if target.applicability_interval_ids and target.applicability_interval_ids[0] != target.interval.interval_id:
        diagnostics.append(_diag(ComparatorDiagnosticCode.MISSING_COMPARATOR_APPLICABILITY, "target", "Target interval reference does not match target interval metadata."))
    if comparator.applicability_interval_ids and comparator.applicability_interval_ids[0] != comparator.interval.interval_id:
        diagnostics.append(_diag(ComparatorDiagnosticCode.MISSING_COMPARATOR_APPLICABILITY, "comparator", "Comparator interval reference does not match comparator interval metadata."))
    if target.identity_id != target.interval.identity_id or relationship.target_identity_id != target.identity_id:
        diagnostics.append(_diag(ComparatorDiagnosticCode.CONFLICTING_COMPARATOR, "target", "Target identity and interval metadata conflict."))
    if comparator.identity_id != comparator.interval.identity_id or relationship.comparator_identity_id != comparator.identity_id:
        diagnostics.append(_diag(ComparatorDiagnosticCode.CONFLICTING_COMPARATOR, "comparator", "Comparator identity and interval metadata conflict."))
    if relationship.target_interval_id != target.interval.interval_id or relationship.comparator_interval_id != comparator.interval.interval_id:
        diagnostics.append(_diag(ComparatorDiagnosticCode.MISSING_COMPARATOR_APPLICABILITY, "relationship", "Relationship interval references do not match declared applicability intervals."))
    if relationship.self_comparison_prohibited and target.interval.interval_id == comparator.interval.interval_id:
        diagnostics.append(_diag(ComparatorDiagnosticCode.DUPLICATE_EXPOSURE_UNRESOLVED, "relationship", "Self-comparison or duplicate interval exposure is prohibited."))

    if target.interval.unknown_interval or comparator.interval.unknown_interval:
        diagnostics.append(_diag(ComparatorDiagnosticCode.MISSING_COMPARATOR_APPLICABILITY, "temporal", "Required interval applicability is unknown."))
    if target.interval.has_invalid_ordering() or comparator.interval.has_invalid_ordering() or temporal_state == TemporalApplicabilityState.NO_OVERLAP:
        diagnostics.append(_diag(ComparatorDiagnosticCode.INVALID_TEMPORAL_OVERLAP, "temporal", "Target and comparator intervals do not have a valid required overlap."))
    if temporal_state == TemporalApplicabilityState.PARTIAL_OVERLAP:
        limitations.append("partial temporal overlap")
    if target.interval.open_interval or comparator.interval.open_interval:
        limitations.append("open interval")
    if target.interval.superseded_interval or comparator.interval.superseded_interval:
        limitations.append("superseded interval")
    if target.interval.expired_interval or comparator.interval.expired_interval:
        limitations.append("expired interval")
    if target.interval.discontinuity or comparator.interval.discontinuity:
        limitations.append("discontinuous interval")

    if relationship.excluded_relationship:
        diagnostics.append(_diag(ComparatorDiagnosticCode.EXCLUDED_COMPARATOR, "relationship", "Comparator relationship is explicitly excluded."))
    if relationship.conflicting_relationship:
        diagnostics.append(_diag(ComparatorDiagnosticCode.CONFLICTING_COMPARATOR, "relationship", "Comparator relationship is conflicting."))
    if relationship.unresolved_relationship:
        diagnostics.append(_diag(ComparatorDiagnosticCode.UNRESOLVED_COMPARATOR, "relationship", "Comparator relationship is unresolved."))
    if not relationship.supported_relationship:
        diagnostics.append(_diag(ComparatorDiagnosticCode.UNSUPPORTED_COMPARATOR_RELATIONSHIP, "relationship", "Comparator relationship is unsupported."))
    if relationship.lineage_unresolved:
        diagnostics.append(_diag(ComparatorDiagnosticCode.UNRESOLVED_COMPARATOR_LINEAGE, "lineage", "Comparator relationship lineage is unresolved."))
    if record.duplicate_exposure:
        diagnostics.append(_diag(ComparatorDiagnosticCode.DUPLICATE_EXPOSURE_UNRESOLVED, "coverage", "Duplicate comparator exposure is unresolved."))

    if not record.coverage.sufficient:
        diagnostics.append(_diag(ComparatorDiagnosticCode.INSUFFICIENT_COMPARATOR_COVERAGE, "coverage", "Comparator coverage is insufficient."))
    if record.coverage.conditionally_governed:
        limitations.append("coverage conditionally governed")
    if record.coverage.coverage_gap:
        limitations.append("coverage gap")
    if not record.context_support.sufficient or record.context_support.context_missing:
        diagnostics.append(_diag(ComparatorDiagnosticCode.COMPARATOR_CONTEXT_INSUFFICIENT, "context", "Comparator context support is insufficient."))
    if record.context_support.conditionally_governed:
        limitations.append("context support conditionally governed")

    if not record.traceability_complete:
        diagnostics.append(_diag(ComparatorDiagnosticCode.INCOMPLETE_COMPARATOR_TRACEABILITY, "traceability", "Comparator traceability is incomplete."))

    diagnostic_tuple = tuple(diagnostics)
    limitation_tuple = tuple(dict.fromkeys(limitations))
    codes = {diag.code for diag in diagnostic_tuple}

    if ComparatorDiagnosticCode.EXCLUDED_COMPARATOR in codes:
        state = ComparatorEligibilityState.COMPARATOR_EXCLUDED
    elif (
        ComparatorDiagnosticCode.INCOMPLETE_COMPARATOR_TRACEABILITY in codes
        or ComparatorDiagnosticCode.CONFLICTING_COMPARATOR in codes
        or ComparatorDiagnosticCode.INVALID_TEMPORAL_OVERLAP in codes
        or ComparatorDiagnosticCode.UNSUPPORTED_COMPARATOR_RELATIONSHIP in codes
        or ComparatorDiagnosticCode.DUPLICATE_EXPOSURE_UNRESOLVED in codes
    ):
        state = ComparatorEligibilityState.COMPARATOR_INELIGIBLE
    elif (
        ComparatorDiagnosticCode.MISSING_COMPARATOR_APPLICABILITY in codes
        or ComparatorDiagnosticCode.UNRESOLVED_COMPARATOR_LINEAGE in codes
        or ComparatorDiagnosticCode.INSUFFICIENT_COMPARATOR_COVERAGE in codes
        or ComparatorDiagnosticCode.COMPARATOR_CONTEXT_INSUFFICIENT in codes
    ):
        state = ComparatorEligibilityState.INSUFFICIENT_COMPARATOR_EVIDENCE
    elif ComparatorDiagnosticCode.UNRESOLVED_COMPARATOR in codes:
        state = ComparatorEligibilityState.COMPARATOR_UNRESOLVED
    elif limitation_tuple:
        state = ComparatorEligibilityState.COMPARATOR_CONDITIONALLY_ELIGIBLE
    else:
        state = ComparatorEligibilityState.COMPARATOR_ELIGIBLE

    return _final_result(record, state, temporal_state, diagnostic_tuple, limitation_tuple)


def _base_record(fixture_id: str) -> ComparatorConstructionRecord:
    target_interval = _interval("synthetic_target", f"target_interval_{fixture_id}")
    comparator_interval = _interval("synthetic_comparator", f"comparator_interval_{fixture_id}")
    return ComparatorConstructionRecord(
        fixture_id=fixture_id,
        target=_ref("synthetic_target", target_interval),
        comparator=_ref("synthetic_comparator", comparator_interval),
        relationship=ComparatorRelationshipMetadata(
            relationship_id=f"relationship_{fixture_id}",
            relationship_type="synthetic_economic_comparator",
            target_identity_id="synthetic_target",
            comparator_identity_id="synthetic_comparator",
            target_interval_id=target_interval.interval_id,
            comparator_interval_id=comparator_interval.interval_id,
        ),
        coverage=ComparatorCoverageMetadata(),
        context_support=ComparatorContextSupportMetadata(),
        source_authority_trace={"source_authority_fixture": "synthetic_authoritative"},
        pit_identity_trace={"pit_identity_fixture": fixture_id},
    )


def _replace(record: ComparatorConstructionRecord, **overrides: Any) -> ComparatorConstructionRecord:
    values = {**record.__dict__}
    values.update(overrides)
    return ComparatorConstructionRecord(**values)


def canonical_comparator_construction_fixtures() -> tuple[ComparatorConstructionFixture, ...]:
    f1 = _base_record("CC1_eligible")
    f2 = _replace(_base_record("CC2_conditionally_eligible"), limitations=("relationship conditionally governed",))
    f3 = _replace(
        _base_record("CC3_unresolved"),
        relationship=ComparatorRelationshipMetadata(**{**_base_record("CC3_unresolved").relationship.__dict__, "unresolved_relationship": True}),
    )
    f4 = _replace(
        _base_record("CC4_ineligible"),
        relationship=ComparatorRelationshipMetadata(**{**_base_record("CC4_ineligible").relationship.__dict__, "supported_relationship": False}),
    )
    f5 = _replace(
        _base_record("CC5_excluded"),
        relationship=ComparatorRelationshipMetadata(**{**_base_record("CC5_excluded").relationship.__dict__, "excluded_relationship": True}),
    )
    f6 = _replace(_base_record("CC6_insufficient_evidence"), coverage=ComparatorCoverageMetadata(sufficient=False))
    f7 = _replace(_base_record("CC7_missing_target_interval"), target=_ref("synthetic_target", _interval("synthetic_target", "target_interval_CC7_missing_target_interval"), ()))
    f8 = _replace(_base_record("CC8_missing_comparator_interval"), comparator=_ref("synthetic_comparator", _interval("synthetic_comparator", "comparator_interval_CC8_missing_comparator_interval"), ()))
    bad_target_interval = _interval("different_target", "target_interval_CC9_identity_interval_mismatch")
    f9 = _replace(_base_record("CC9_identity_interval_mismatch"), target=_ref("synthetic_target", bad_target_interval))
    f10 = _base_record("CC10_valid_temporal_overlap")
    no_overlap_comparator = _interval("synthetic_comparator", "comparator_interval_CC11_invalid_temporal_overlap", 20, 30)
    f11 = _replace(
        _base_record("CC11_invalid_temporal_overlap"),
        comparator=_ref("synthetic_comparator", no_overlap_comparator),
        relationship=ComparatorRelationshipMetadata(**{**_base_record("CC11_invalid_temporal_overlap").relationship.__dict__, "comparator_interval_id": no_overlap_comparator.interval_id}),
    )
    partial_comparator = _interval("synthetic_comparator", "comparator_interval_CC12_partial_overlap", 5, 15)
    f12 = _replace(
        _base_record("CC12_partial_overlap"),
        comparator=_ref("synthetic_comparator", partial_comparator),
        relationship=ComparatorRelationshipMetadata(**{**_base_record("CC12_partial_overlap").relationship.__dict__, "comparator_interval_id": partial_comparator.interval_id}),
    )
    superseded = _interval("synthetic_comparator", "comparator_interval_CC13_superseded", superseded_interval=True)
    f13 = _replace(
        _base_record("CC13_superseded_interval"),
        comparator=_ref("synthetic_comparator", superseded),
        relationship=ComparatorRelationshipMetadata(**{**_base_record("CC13_superseded_interval").relationship.__dict__, "comparator_interval_id": superseded.interval_id}),
    )
    expired = _interval("synthetic_comparator", "comparator_interval_CC14_expired", expired_interval=True)
    f14 = _replace(
        _base_record("CC14_expired_interval"),
        comparator=_ref("synthetic_comparator", expired),
        relationship=ComparatorRelationshipMetadata(**{**_base_record("CC14_expired_interval").relationship.__dict__, "comparator_interval_id": expired.interval_id}),
    )
    f15 = _replace(
        _base_record("CC15_unresolved_lineage"),
        relationship=ComparatorRelationshipMetadata(**{**_base_record("CC15_unresolved_lineage").relationship.__dict__, "lineage_unresolved": True}),
    )
    f16 = _replace(_base_record("CC16_insufficient_coverage"), coverage=ComparatorCoverageMetadata(sufficient=False))
    f17 = _replace(_base_record("CC17_insufficient_context"), context_support=ComparatorContextSupportMetadata(sufficient=False))
    f18 = _replace(_base_record("CC18_duplicate_exposure"), duplicate_exposure=True)
    f19 = _replace(
        _base_record("CC19_conflicting_relationship"),
        relationship=ComparatorRelationshipMetadata(**{**_base_record("CC19_conflicting_relationship").relationship.__dict__, "conflicting_relationship": True}),
    )
    f20 = _replace(_base_record("CC20_incomplete_traceability"), traceability_complete=False)

    return (
        ComparatorConstructionFixture("CC1_eligible", "Fully eligible comparator.", f1, ComparatorEligibilityState.COMPARATOR_ELIGIBLE, TemporalApplicabilityState.VALID_OVERLAP),
        ComparatorConstructionFixture("CC2_conditionally_eligible", "Conditionally eligible comparator.", f2, ComparatorEligibilityState.COMPARATOR_CONDITIONALLY_ELIGIBLE, TemporalApplicabilityState.VALID_OVERLAP, expected_limitations=("relationship conditionally governed",)),
        ComparatorConstructionFixture("CC3_unresolved", "Unresolved comparator.", f3, ComparatorEligibilityState.COMPARATOR_UNRESOLVED, TemporalApplicabilityState.VALID_OVERLAP, (ComparatorDiagnosticCode.UNRESOLVED_COMPARATOR,)),
        ComparatorConstructionFixture("CC4_ineligible", "Ineligible comparator.", f4, ComparatorEligibilityState.COMPARATOR_INELIGIBLE, TemporalApplicabilityState.VALID_OVERLAP, (ComparatorDiagnosticCode.UNSUPPORTED_COMPARATOR_RELATIONSHIP,)),
        ComparatorConstructionFixture("CC5_excluded", "Explicitly excluded comparator.", f5, ComparatorEligibilityState.COMPARATOR_EXCLUDED, TemporalApplicabilityState.VALID_OVERLAP, (ComparatorDiagnosticCode.EXCLUDED_COMPARATOR,)),
        ComparatorConstructionFixture("CC6_insufficient_evidence", "Insufficient comparator evidence.", f6, ComparatorEligibilityState.INSUFFICIENT_COMPARATOR_EVIDENCE, TemporalApplicabilityState.VALID_OVERLAP, (ComparatorDiagnosticCode.INSUFFICIENT_COMPARATOR_COVERAGE,)),
        ComparatorConstructionFixture("CC7_missing_target_interval", "Missing target applicability interval.", f7, ComparatorEligibilityState.INSUFFICIENT_COMPARATOR_EVIDENCE, TemporalApplicabilityState.VALID_OVERLAP, (ComparatorDiagnosticCode.MISSING_COMPARATOR_APPLICABILITY,)),
        ComparatorConstructionFixture("CC8_missing_comparator_interval", "Missing comparator applicability interval.", f8, ComparatorEligibilityState.INSUFFICIENT_COMPARATOR_EVIDENCE, TemporalApplicabilityState.VALID_OVERLAP, (ComparatorDiagnosticCode.MISSING_COMPARATOR_APPLICABILITY,)),
        ComparatorConstructionFixture("CC9_identity_interval_mismatch", "Identity-to-interval mismatch.", f9, ComparatorEligibilityState.COMPARATOR_INELIGIBLE, TemporalApplicabilityState.VALID_OVERLAP, (ComparatorDiagnosticCode.CONFLICTING_COMPARATOR,)),
        ComparatorConstructionFixture("CC10_valid_temporal_overlap", "Valid temporal overlap.", f10, ComparatorEligibilityState.COMPARATOR_ELIGIBLE, TemporalApplicabilityState.VALID_OVERLAP),
        ComparatorConstructionFixture("CC11_invalid_temporal_overlap", "Invalid temporal overlap.", f11, ComparatorEligibilityState.COMPARATOR_INELIGIBLE, TemporalApplicabilityState.NO_OVERLAP, (ComparatorDiagnosticCode.INVALID_TEMPORAL_OVERLAP,)),
        ComparatorConstructionFixture("CC12_partial_overlap", "Partial overlap with limitation.", f12, ComparatorEligibilityState.COMPARATOR_CONDITIONALLY_ELIGIBLE, TemporalApplicabilityState.PARTIAL_OVERLAP, expected_limitations=("partial temporal overlap",)),
        ComparatorConstructionFixture("CC13_superseded_interval", "Superseded comparator interval.", f13, ComparatorEligibilityState.COMPARATOR_CONDITIONALLY_ELIGIBLE, TemporalApplicabilityState.VALID_OVERLAP, expected_limitations=("superseded interval",)),
        ComparatorConstructionFixture("CC14_expired_interval", "Expired comparator interval.", f14, ComparatorEligibilityState.COMPARATOR_CONDITIONALLY_ELIGIBLE, TemporalApplicabilityState.VALID_OVERLAP, expected_limitations=("expired interval",)),
        ComparatorConstructionFixture("CC15_unresolved_lineage", "Unresolved comparator lineage.", f15, ComparatorEligibilityState.INSUFFICIENT_COMPARATOR_EVIDENCE, TemporalApplicabilityState.VALID_OVERLAP, (ComparatorDiagnosticCode.UNRESOLVED_COMPARATOR_LINEAGE,)),
        ComparatorConstructionFixture("CC16_insufficient_coverage", "Insufficient comparator coverage.", f16, ComparatorEligibilityState.INSUFFICIENT_COMPARATOR_EVIDENCE, TemporalApplicabilityState.VALID_OVERLAP, (ComparatorDiagnosticCode.INSUFFICIENT_COMPARATOR_COVERAGE,)),
        ComparatorConstructionFixture("CC17_insufficient_context", "Insufficient comparator context.", f17, ComparatorEligibilityState.INSUFFICIENT_COMPARATOR_EVIDENCE, TemporalApplicabilityState.VALID_OVERLAP, (ComparatorDiagnosticCode.COMPARATOR_CONTEXT_INSUFFICIENT,)),
        ComparatorConstructionFixture("CC18_duplicate_exposure", "Duplicate comparator exposure.", f18, ComparatorEligibilityState.COMPARATOR_INELIGIBLE, TemporalApplicabilityState.VALID_OVERLAP, (ComparatorDiagnosticCode.DUPLICATE_EXPOSURE_UNRESOLVED,)),
        ComparatorConstructionFixture("CC19_conflicting_relationship", "Conflicting comparator relationship.", f19, ComparatorEligibilityState.COMPARATOR_INELIGIBLE, TemporalApplicabilityState.VALID_OVERLAP, (ComparatorDiagnosticCode.CONFLICTING_COMPARATOR,)),
        ComparatorConstructionFixture("CC20_incomplete_traceability", "Incomplete comparator traceability.", f20, ComparatorEligibilityState.COMPARATOR_INELIGIBLE, TemporalApplicabilityState.VALID_OVERLAP, (ComparatorDiagnosticCode.INCOMPLETE_COMPARATOR_TRACEABILITY,)),
    )


def comparator_construction_guardrail_manifest() -> dict[str, bool]:
    return {
        "synthetic_metadata_only": True,
        "acquisition_performed": False,
        "retrieval_performed": False,
        "vendor_integration": False,
        "authority_evaluation": False,
        "identity_construction": False,
        "identity_resolution": False,
        "scientific_similarity": False,
        "comparator_ranking": False,
        "peer_discovery": False,
        "contextual_measurement": False,
        "formula_execution": False,
        "candidate_generation": False,
        "panel_generation": False,
        "discovery_execution": False,
        "validation_execution": False,
        "ic_computation": False,
        "production_logic": False,
        "optimization_performed": False,
        "ml_integration": False,
    }
