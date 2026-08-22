from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
import json
from typing import Any


MODULE_ID = "project_underdog_phase5_prepared_observations_reference_implementation_v1"
MODULE_VERSION = "v1"
FROZEN_DESIGN_ID = "project_underdog_phase5_prepared_observations_implementation_design_v1"
LAYER_NAME = "Project Underdog Phase 5 Prepared Observations"


class PreparedObservationReadinessState(str, Enum):
    STRUCTURALLY_READY = "PREPARED_OBSERVATION_STRUCTURALLY_READY"
    CONDITIONALLY_READY = "PREPARED_OBSERVATION_CONDITIONALLY_READY"
    UNRESOLVED = "PREPARED_OBSERVATION_UNRESOLVED"
    STRUCTURALLY_INCOMPLETE = "PREPARED_OBSERVATION_STRUCTURALLY_INCOMPLETE"
    EXCLUDED = "PREPARED_OBSERVATION_EXCLUDED"
    INSUFFICIENT_EVIDENCE = "INSUFFICIENT_PREPARED_OBSERVATION_EVIDENCE"


class TemporalAlignmentState(str, Enum):
    FULLY_ALIGNED = "fully_aligned"
    PARTIALLY_ALIGNED = "partially_aligned"
    NON_OVERLAPPING = "non_overlapping"
    UNKNOWN_ALIGNMENT = "unknown_alignment"
    STALE_CONTEXTUAL_EVIDENCE = "stale_contextual_evidence"
    SUPERSEDED_CONTEXTUAL_EVIDENCE = "superseded_contextual_evidence"
    EXPIRED_COMPARATOR_APPLICABILITY = "expired_comparator_applicability"
    DISCONTINUOUS_IDENTITY_APPLICABILITY = "discontinuous_identity_applicability"
    MIXED_FREQUENCY = "mixed_frequency"
    INCOMPLETE_TEMPORAL_TRACEABILITY = "incomplete_temporal_traceability"


class InformationRole(str, Enum):
    VALIDATED_ALPHA_INFORMATION = "VALIDATED_ALPHA_INFORMATION"
    SUPPORTED_ALPHA_INFORMATION = "SUPPORTED_ALPHA_INFORMATION"
    CONTEXTUAL_CONTROL_INFORMATION = "CONTEXTUAL_CONTROL_INFORMATION"
    CONDITIONING_INFORMATION = "CONDITIONING_INFORMATION"
    COMPARATOR_OR_BENCHMARK_INFORMATION = "COMPARATOR_OR_BENCHMARK_INFORMATION"
    COMMON_IDIOSYNCRATIC_DECOMPOSITION_INFORMATION = "COMMON_IDIOSYNCRATIC_DECOMPOSITION_INFORMATION"
    EXPLANATORY_ONLY_INFORMATION = "EXPLANATORY_ONLY_INFORMATION"
    FAMILY_REFINEMENT_INFORMATION = "FAMILY_REFINEMENT_INFORMATION"
    DIAGNOSTIC_INFORMATION = "DIAGNOSTIC_INFORMATION"
    NEGATIVE_INFORMATION = "NEGATIVE_INFORMATION"
    REJECTED_OR_RETIRED_INFORMATION = "REJECTED_OR_RETIRED_INFORMATION"
    HYPOTHETICAL_INFORMATION = "HYPOTHETICAL_INFORMATION"
    MISSING_REQUIRED_INFORMATION = "MISSING_REQUIRED_INFORMATION"
    INSUFFICIENT_EVIDENCE = "INSUFFICIENT_EVIDENCE"


class PreparedObservationDiagnosticCode(str, Enum):
    MISSING_TARGET_APPLICABILITY = "MISSING_TARGET_APPLICABILITY"
    MISSING_OBSERVATION_TIME = "MISSING_OBSERVATION_TIME"
    INVALID_OBSERVATION_INTERVAL = "INVALID_OBSERVATION_INTERVAL"
    UNRESOLVED_TEMPORAL_ALIGNMENT = "UNRESOLVED_TEMPORAL_ALIGNMENT"
    NON_OVERLAPPING_TEMPORAL_APPLICABILITY = "NON_OVERLAPPING_TEMPORAL_APPLICABILITY"
    CONFLICTING_EVIDENCE_ATTACHMENT = "CONFLICTING_EVIDENCE_ATTACHMENT"
    MISSING_SOURCE_AUTHORITY_TRACE = "MISSING_SOURCE_AUTHORITY_TRACE"
    MISSING_PIT_TRACE = "MISSING_PIT_TRACE"
    MISSING_COMPARATOR_TRACE = "MISSING_COMPARATOR_TRACE"
    INHERITED_FATAL_UPSTREAM_DIAGNOSTIC = "INHERITED_FATAL_UPSTREAM_DIAGNOSTIC"
    INSUFFICIENT_OBSERVATION_COVERAGE = "INSUFFICIENT_OBSERVATION_COVERAGE"
    MISSING_REQUIRED_CONTEXT = "MISSING_REQUIRED_CONTEXT"
    MISSING_REQUIRED_COMPARATOR = "MISSING_REQUIRED_COMPARATOR"
    UNDECLARED_INFORMATION_ROLE = "UNDECLARED_INFORMATION_ROLE"
    UNSUPPORTED_INFORMATION_ROLE = "UNSUPPORTED_INFORMATION_ROLE"
    PROHIBITED_INFORMATION_ROLE_USE = "PROHIBITED_INFORMATION_ROLE_USE"
    DUPLICATE_OBSERVATION_EXPOSURE = "DUPLICATE_OBSERVATION_EXPOSURE"
    SUPERSEDED_OBSERVATION_PACKAGE = "SUPERSEDED_OBSERVATION_PACKAGE"
    INCOMPLETE_OBSERVATION_TRACEABILITY = "INCOMPLETE_OBSERVATION_TRACEABILITY"
    STRUCTURALLY_INCOMPLETE_PACKAGE = "STRUCTURALLY_INCOMPLETE_PACKAGE"
    RAW_EVIDENCE_ATTACHMENT_PROHIBITED = "RAW_EVIDENCE_ATTACHMENT_PROHIBITED"


@dataclass(frozen=True)
class PreparedObservationDiagnostic:
    code: PreparedObservationDiagnosticCode
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
class ObservationInterval:
    interval_id: str
    start: int | None
    end: int | None
    open_interval: bool = False
    unknown_interval: bool = False
    unavailable: bool = False

    def has_invalid_ordering(self) -> bool:
        return self.start is not None and self.end is not None and self.end < self.start

    def has_time(self) -> bool:
        if self.unavailable or self.unknown_interval:
            return False
        if self.open_interval:
            return self.start is not None
        return self.start is not None and self.end is not None

    def to_dict(self) -> dict[str, Any]:
        return {
            "end": self.end,
            "interval_id": self.interval_id,
            "open_interval": self.open_interval,
            "start": self.start,
            "unknown_interval": self.unknown_interval,
            "unavailable": self.unavailable,
        }


@dataclass(frozen=True)
class ObservationTimeMetadata:
    observation_time: int | None = None
    observation_interval: ObservationInterval | None = None
    source_effective_time: int | None = None
    identity_applicability_time: str = ""
    context_applicability_time: str = ""
    comparator_applicability_time: str = ""
    package_construction_time: str = "synthetic_package_construction_v1"
    unknown_observation_time: bool = False
    unavailable_observation_time: bool = False

    def has_valid_observation_time(self) -> bool:
        point_present = self.observation_time is not None
        interval_present = self.observation_interval is not None
        if self.unknown_observation_time or self.unavailable_observation_time:
            return False
        if point_present and interval_present:
            return False
        if point_present:
            return True
        if interval_present:
            return bool(self.observation_interval and self.observation_interval.has_time())
        return False

    def has_invalid_interval(self) -> bool:
        return bool(self.observation_interval and self.observation_interval.has_invalid_ordering())

    def is_open_interval(self) -> bool:
        return bool(self.observation_interval and self.observation_interval.open_interval)

    def to_dict(self) -> dict[str, Any]:
        return {
            "comparator_applicability_time": self.comparator_applicability_time,
            "context_applicability_time": self.context_applicability_time,
            "identity_applicability_time": self.identity_applicability_time,
            "observation_interval": self.observation_interval.to_dict() if self.observation_interval else None,
            "observation_time": self.observation_time,
            "package_construction_time": self.package_construction_time,
            "source_effective_time": self.source_effective_time,
            "unknown_observation_time": self.unknown_observation_time,
            "unavailable_observation_time": self.unavailable_observation_time,
        }


@dataclass(frozen=True)
class TargetObservationMetadata:
    target_identity_id: str
    target_applicability_interval_ids: tuple[str, ...]
    target_applicability_interval_id: str
    observation_role: str = "synthetic_target_observation"
    observation_available: bool = True

    def to_dict(self) -> dict[str, Any]:
        return {
            "observation_available": self.observation_available,
            "observation_role": self.observation_role,
            "target_applicability_interval_id": self.target_applicability_interval_id,
            "target_applicability_interval_ids": list(self.target_applicability_interval_ids),
            "target_identity_id": self.target_identity_id,
        }


@dataclass(frozen=True)
class ContextEvidenceAttachment:
    context_id: str
    identity_applicability_interval_id: str
    context_applicability_interval_id: str
    information_role: str
    context_status: str = "present"
    required: bool = False
    trace: dict[str, Any] | None = None
    limitations: tuple[str, ...] = ()
    diagnostics: tuple[str, ...] = ()
    duplicate: bool = False
    superseded: bool = False
    conflicting: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "conflicting": self.conflicting,
            "context_applicability_interval_id": self.context_applicability_interval_id,
            "context_id": self.context_id,
            "context_status": self.context_status,
            "diagnostics": list(self.diagnostics),
            "duplicate": self.duplicate,
            "identity_applicability_interval_id": self.identity_applicability_interval_id,
            "information_role": self.information_role,
            "limitations": list(self.limitations),
            "required": self.required,
            "superseded": self.superseded,
            "trace": self.trace or {},
        }


@dataclass(frozen=True)
class ComparatorAttachment:
    relationship_id: str
    comparator_identity_id: str
    comparator_applicability_interval_id: str
    information_role: str
    eligibility_state: str = "COMPARATOR_ELIGIBLE"
    temporal_applicability_state: str = "valid_overlap"
    required: bool = False
    trace: dict[str, Any] | None = None
    limitations: tuple[str, ...] = ()
    diagnostics: tuple[str, ...] = ()
    duplicate: bool = False
    superseded: bool = False
    conflicting: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "comparator_applicability_interval_id": self.comparator_applicability_interval_id,
            "comparator_identity_id": self.comparator_identity_id,
            "conflicting": self.conflicting,
            "diagnostics": list(self.diagnostics),
            "duplicate": self.duplicate,
            "eligibility_state": self.eligibility_state,
            "information_role": self.information_role,
            "limitations": list(self.limitations),
            "relationship_id": self.relationship_id,
            "required": self.required,
            "superseded": self.superseded,
            "temporal_applicability_state": self.temporal_applicability_state,
            "trace": self.trace or {},
        }


@dataclass(frozen=True)
class CoverageMetadata:
    target_coverage: bool = True
    comparator_coverage: bool = True
    context_coverage: bool = True
    temporal_coverage: bool = True
    information_role_coverage: bool = True
    traceability_coverage: bool = True
    conditionally_governed: bool = False

    def is_sufficient(self) -> bool:
        return (
            self.target_coverage
            and self.comparator_coverage
            and self.context_coverage
            and self.temporal_coverage
            and self.information_role_coverage
            and self.traceability_coverage
        )

    def to_dict(self) -> dict[str, bool]:
        return {
            "comparator_coverage": self.comparator_coverage,
            "conditionally_governed": self.conditionally_governed,
            "context_coverage": self.context_coverage,
            "information_role_coverage": self.information_role_coverage,
            "target_coverage": self.target_coverage,
            "temporal_coverage": self.temporal_coverage,
            "traceability_coverage": self.traceability_coverage,
        }


@dataclass(frozen=True)
class MissingnessMetadata:
    required_field_missing: bool = False
    optional_field_missing: bool = False
    unavailable_evidence: bool = False
    intentionally_excluded_evidence: bool = False

    def to_dict(self) -> dict[str, bool]:
        return {
            "intentionally_excluded_evidence": self.intentionally_excluded_evidence,
            "optional_field_missing": self.optional_field_missing,
            "required_field_missing": self.required_field_missing,
            "unavailable_evidence": self.unavailable_evidence,
        }


@dataclass(frozen=True)
class ReproducibilityMetadata:
    deterministic_serialization: bool = True
    controlled_reference: str = "synthetic_prepared_observation_controlled_reference"
    environment_dependent_output: bool = False
    runtime_timestamp_used: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "controlled_reference": self.controlled_reference,
            "deterministic_serialization": self.deterministic_serialization,
            "environment_dependent_output": self.environment_dependent_output,
            "runtime_timestamp_used": self.runtime_timestamp_used,
        }


@dataclass(frozen=True)
class ArtifactLineageMetadata:
    source_authority_artifacts: tuple[str, ...]
    pit_identity_context_artifacts: tuple[str, ...]
    comparator_construction_artifacts: tuple[str, ...]
    prepared_observation_artifact: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "comparator_construction_artifacts": list(self.comparator_construction_artifacts),
            "pit_identity_context_artifacts": list(self.pit_identity_context_artifacts),
            "prepared_observation_artifact": self.prepared_observation_artifact,
            "source_authority_artifacts": list(self.source_authority_artifacts),
        }


@dataclass(frozen=True)
class PreparedObservationRecord:
    package_id: str
    target_observation: TargetObservationMetadata
    observation_time: ObservationTimeMetadata
    source_authority_trace: dict[str, Any]
    pit_trace: dict[str, Any]
    comparator_attachments: tuple[ComparatorAttachment, ...] = ()
    context_attachments: tuple[ContextEvidenceAttachment, ...] = ()
    temporal_alignment_state: TemporalAlignmentState = TemporalAlignmentState.FULLY_ALIGNED
    coverage: CoverageMetadata = field(default_factory=CoverageMetadata)
    missingness: MissingnessMetadata = field(default_factory=MissingnessMetadata)
    reproducibility: ReproducibilityMetadata = field(default_factory=ReproducibilityMetadata)
    artifact_lineage: ArtifactLineageMetadata | None = None
    required_context_ids: tuple[str, ...] = ()
    required_comparator_relationship_ids: tuple[str, ...] = ()
    explicit_exclusion: bool = False
    duplicate_package: bool = False
    superseded_package: bool = False
    conflicting_attachment: bool = False
    incomplete_traceability: bool = False
    raw_evidence_bypass: bool = False
    prohibited_role_conversion: bool = False
    limitations: tuple[str, ...] = ()
    fixture_id: str = ""
    module_id: str = MODULE_ID
    frozen_design_id: str = FROZEN_DESIGN_ID


@dataclass(frozen=True)
class PreparedObservationInformationContract:
    package_metadata: dict[str, Any]
    target_observation_metadata: dict[str, Any]
    comparator_attachment_metadata: tuple[dict[str, Any], ...]
    context_attachment_metadata: tuple[dict[str, Any], ...]
    observation_time_metadata: dict[str, Any]
    temporal_alignment_metadata: dict[str, Any]
    information_role_metadata: tuple[dict[str, Any], ...]
    inherited_eligibility_metadata: dict[str, Any]
    structural_readiness_state: PreparedObservationReadinessState
    coverage_metadata: dict[str, Any]
    missingness_metadata: dict[str, Any]
    limitations: tuple[str, ...]
    diagnostics: tuple[PreparedObservationDiagnostic, ...]
    source_authority_trace: dict[str, Any]
    pit_trace: dict[str, Any]
    comparator_traces: tuple[dict[str, Any], ...]
    reproducibility_metadata: dict[str, Any]
    artifact_lineage_metadata: dict[str, Any]
    governing_versions: dict[str, str]
    exposes_retrieval: bool = False
    exposes_raw_vendor_access: bool = False
    performs_authority_evaluation: bool = False
    performs_identity_construction: bool = False
    performs_identity_resolution: bool = False
    performs_comparator_construction: bool = False
    performs_peer_discovery: bool = False
    exposes_scientific_similarity: bool = False
    performs_value_transformation: bool = False
    performs_normalization: bool = False
    performs_ranking: bool = False
    performs_winsorization: bool = False
    performs_imputation: bool = False
    performs_resampling: bool = False
    exposes_formulas: bool = False
    creates_signals: bool = False
    creates_factors: bool = False
    creates_candidates: bool = False
    constructs_panels: bool = False
    computes_ic: bool = False
    runs_statistical_testing: bool = False
    runs_validation: bool = False
    constructs_portfolios: bool = False
    performs_optimization: bool = False
    makes_production_decisions: bool = False
    exposes_ml_features: bool = False
    exposes_ml_labels: bool = False
    trains_models: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "artifact_lineage_metadata": self.artifact_lineage_metadata,
            "comparator_attachment_metadata": list(self.comparator_attachment_metadata),
            "comparator_traces": list(self.comparator_traces),
            "computes_ic": self.computes_ic,
            "constructs_panels": self.constructs_panels,
            "constructs_portfolios": self.constructs_portfolios,
            "context_attachment_metadata": list(self.context_attachment_metadata),
            "coverage_metadata": self.coverage_metadata,
            "creates_candidates": self.creates_candidates,
            "creates_factors": self.creates_factors,
            "creates_signals": self.creates_signals,
            "diagnostics": [diag.to_dict() for diag in self.diagnostics],
            "exposes_formulas": self.exposes_formulas,
            "exposes_ml_features": self.exposes_ml_features,
            "exposes_ml_labels": self.exposes_ml_labels,
            "exposes_raw_vendor_access": self.exposes_raw_vendor_access,
            "exposes_retrieval": self.exposes_retrieval,
            "exposes_scientific_similarity": self.exposes_scientific_similarity,
            "governing_versions": self.governing_versions,
            "information_role_metadata": list(self.information_role_metadata),
            "inherited_eligibility_metadata": self.inherited_eligibility_metadata,
            "limitations": list(self.limitations),
            "makes_production_decisions": self.makes_production_decisions,
            "missingness_metadata": self.missingness_metadata,
            "observation_time_metadata": self.observation_time_metadata,
            "package_metadata": self.package_metadata,
            "performs_authority_evaluation": self.performs_authority_evaluation,
            "performs_comparator_construction": self.performs_comparator_construction,
            "performs_identity_construction": self.performs_identity_construction,
            "performs_identity_resolution": self.performs_identity_resolution,
            "performs_imputation": self.performs_imputation,
            "performs_normalization": self.performs_normalization,
            "performs_optimization": self.performs_optimization,
            "performs_peer_discovery": self.performs_peer_discovery,
            "performs_ranking": self.performs_ranking,
            "performs_resampling": self.performs_resampling,
            "performs_value_transformation": self.performs_value_transformation,
            "performs_winsorization": self.performs_winsorization,
            "pit_trace": self.pit_trace,
            "reproducibility_metadata": self.reproducibility_metadata,
            "runs_statistical_testing": self.runs_statistical_testing,
            "runs_validation": self.runs_validation,
            "source_authority_trace": self.source_authority_trace,
            "structural_readiness_state": self.structural_readiness_state.value,
            "target_observation_metadata": self.target_observation_metadata,
            "temporal_alignment_metadata": self.temporal_alignment_metadata,
            "trains_models": self.trains_models,
        }


@dataclass(frozen=True)
class PreparedObservationResult:
    module_id: str
    module_version: str
    frozen_design_id: str
    fixture_id: str
    package_id: str
    readiness_state: PreparedObservationReadinessState
    temporal_alignment_state: TemporalAlignmentState
    target_observation: TargetObservationMetadata
    observation_time: ObservationTimeMetadata
    comparator_attachments: tuple[ComparatorAttachment, ...]
    context_attachments: tuple[ContextEvidenceAttachment, ...]
    coverage: CoverageMetadata
    missingness: MissingnessMetadata
    limitations: tuple[str, ...]
    diagnostics: tuple[PreparedObservationDiagnostic, ...]
    source_authority_trace: dict[str, Any]
    pit_trace: dict[str, Any]
    comparator_traces: tuple[dict[str, Any], ...]
    reproducibility: ReproducibilityMetadata
    artifact_lineage: ArtifactLineageMetadata
    traceability: dict[str, Any]
    information_contract: PreparedObservationInformationContract
    acquisition_performed: bool = False
    retrieval_performed: bool = False
    vendor_integration: bool = False
    authority_evaluation_performed: bool = False
    identity_construction: bool = False
    identity_resolution: bool = False
    comparator_construction: bool = False
    peer_discovery: bool = False
    scientific_similarity: bool = False
    contextual_interpretation: bool = False
    value_transformation: bool = False
    normalization: bool = False
    ranking: bool = False
    winsorization: bool = False
    imputation: bool = False
    resampling: bool = False
    formula_execution: bool = False
    signal_construction: bool = False
    factor_construction: bool = False
    candidate_generation: bool = False
    panel_generation: bool = False
    discovery_execution: bool = False
    ic_computation: bool = False
    validation_execution: bool = False
    portfolio_construction: bool = False
    optimization_performed: bool = False
    production_logic: bool = False
    ml_integration: bool = False

    def to_ordered_dict(self) -> dict[str, Any]:
        return {
            "acquisition_performed": self.acquisition_performed,
            "artifact_lineage": self.artifact_lineage.to_dict(),
            "authority_evaluation_performed": self.authority_evaluation_performed,
            "candidate_generation": self.candidate_generation,
            "comparator_attachments": [attachment.to_dict() for attachment in self.comparator_attachments],
            "comparator_construction": self.comparator_construction,
            "comparator_traces": list(self.comparator_traces),
            "context_attachments": [attachment.to_dict() for attachment in self.context_attachments],
            "contextual_interpretation": self.contextual_interpretation,
            "coverage": self.coverage.to_dict(),
            "diagnostics": [diag.to_dict() for diag in self.diagnostics],
            "discovery_execution": self.discovery_execution,
            "factor_construction": self.factor_construction,
            "fixture_id": self.fixture_id,
            "formula_execution": self.formula_execution,
            "frozen_design_id": self.frozen_design_id,
            "ic_computation": self.ic_computation,
            "identity_construction": self.identity_construction,
            "identity_resolution": self.identity_resolution,
            "imputation": self.imputation,
            "information_contract": self.information_contract.to_dict(),
            "limitations": list(self.limitations),
            "missingness": self.missingness.to_dict(),
            "ml_integration": self.ml_integration,
            "module_id": self.module_id,
            "module_version": self.module_version,
            "normalization": self.normalization,
            "observation_time": self.observation_time.to_dict(),
            "optimization_performed": self.optimization_performed,
            "package_id": self.package_id,
            "panel_generation": self.panel_generation,
            "peer_discovery": self.peer_discovery,
            "pit_trace": self.pit_trace,
            "portfolio_construction": self.portfolio_construction,
            "production_logic": self.production_logic,
            "ranking": self.ranking,
            "readiness_state": self.readiness_state.value,
            "reproducibility": self.reproducibility.to_dict(),
            "resampling": self.resampling,
            "retrieval_performed": self.retrieval_performed,
            "scientific_similarity": self.scientific_similarity,
            "signal_construction": self.signal_construction,
            "source_authority_trace": self.source_authority_trace,
            "target_observation": self.target_observation.to_dict(),
            "temporal_alignment_state": self.temporal_alignment_state.value,
            "traceability": self.traceability,
            "validation_execution": self.validation_execution,
            "value_transformation": self.value_transformation,
            "vendor_integration": self.vendor_integration,
            "winsorization": self.winsorization,
        }

    def stable_json(self) -> str:
        return json.dumps(self.to_ordered_dict(), sort_keys=True, separators=(",", ":"))


@dataclass(frozen=True)
class PreparedObservationFixture:
    fixture_id: str
    description: str
    record: PreparedObservationRecord
    expected_readiness_state: PreparedObservationReadinessState
    expected_temporal_alignment_state: TemporalAlignmentState
    expected_diagnostic_codes: tuple[PreparedObservationDiagnosticCode, ...] = ()
    expected_limitations: tuple[str, ...] = ()


def _diag(
    code: PreparedObservationDiagnosticCode,
    component: str,
    message: str,
    *,
    inherited: bool = False,
) -> PreparedObservationDiagnostic:
    return PreparedObservationDiagnostic(code=code, component=component, message=message, inherited=inherited)


def _valid_role(role: str) -> bool:
    return role in {item.value for item in InformationRole}


def _role_entries(record: PreparedObservationRecord) -> tuple[dict[str, str], ...]:
    entries: list[dict[str, str]] = []
    for context in record.context_attachments:
        entries.append({"element_id": context.context_id, "information_role": context.information_role})
    for comparator in record.comparator_attachments:
        entries.append({"element_id": comparator.relationship_id, "information_role": comparator.information_role})
    return tuple(entries)


def _trace(record: PreparedObservationRecord, diagnostics: tuple[PreparedObservationDiagnostic, ...]) -> dict[str, Any]:
    return {
        "context_ids": [context.context_id for context in record.context_attachments],
        "diagnostic_codes": [diag.code.value for diag in diagnostics],
        "fixture_id": record.fixture_id,
        "frozen_design_id": record.frozen_design_id,
        "governing_design": FROZEN_DESIGN_ID,
        "layer_name": LAYER_NAME,
        "package_id": record.package_id,
        "pit_trace": record.pit_trace,
        "relationship_ids": [comparator.relationship_id for comparator in record.comparator_attachments],
        "source_authority_trace": record.source_authority_trace,
        "target_identity_id": record.target_observation.target_identity_id,
        "target_interval_id": record.target_observation.target_applicability_interval_id,
        "temporal_alignment_state": record.temporal_alignment_state.value,
    }


def _artifact_lineage(record: PreparedObservationRecord) -> ArtifactLineageMetadata:
    if record.artifact_lineage is not None:
        return record.artifact_lineage
    return ArtifactLineageMetadata(
        source_authority_artifacts=(record.source_authority_trace.get("fixture_id", "synthetic_source_authority_trace"),),
        pit_identity_context_artifacts=(record.pit_trace.get("fixture_id", "synthetic_pit_trace"),),
        comparator_construction_artifacts=tuple(
            attachment.trace.get("fixture_id", attachment.relationship_id) for attachment in record.comparator_attachments if attachment.trace
        ),
        prepared_observation_artifact=f"prepared_observation_artifact_{record.package_id}",
    )


def _contract(
    record: PreparedObservationRecord,
    state: PreparedObservationReadinessState,
    diagnostics: tuple[PreparedObservationDiagnostic, ...],
    limitations: tuple[str, ...],
    traceability: dict[str, Any],
    artifact_lineage: ArtifactLineageMetadata,
) -> PreparedObservationInformationContract:
    comparator_traces = tuple(attachment.trace or {} for attachment in record.comparator_attachments)
    return PreparedObservationInformationContract(
        package_metadata={"package_id": record.package_id, "fixture_id": record.fixture_id},
        target_observation_metadata=record.target_observation.to_dict(),
        comparator_attachment_metadata=tuple(attachment.to_dict() for attachment in record.comparator_attachments),
        context_attachment_metadata=tuple(attachment.to_dict() for attachment in record.context_attachments),
        observation_time_metadata=record.observation_time.to_dict(),
        temporal_alignment_metadata={"temporal_alignment_state": record.temporal_alignment_state.value},
        information_role_metadata=_role_entries(record),
        inherited_eligibility_metadata={
            "comparator_eligibility_states": [attachment.eligibility_state for attachment in record.comparator_attachments],
            "context_statuses": [attachment.context_status for attachment in record.context_attachments],
            "source_authority_trace_present": bool(record.source_authority_trace),
            "pit_trace_present": bool(record.pit_trace),
        },
        structural_readiness_state=state,
        coverage_metadata=record.coverage.to_dict(),
        missingness_metadata=record.missingness.to_dict(),
        limitations=limitations,
        diagnostics=diagnostics,
        source_authority_trace=record.source_authority_trace,
        pit_trace=record.pit_trace,
        comparator_traces=comparator_traces,
        reproducibility_metadata=record.reproducibility.to_dict(),
        artifact_lineage_metadata=artifact_lineage.to_dict(),
        governing_versions={
            "design": FROZEN_DESIGN_ID,
            "implementation": MODULE_ID,
            "implementation_version": MODULE_VERSION,
        },
    )


def _final_result(
    record: PreparedObservationRecord,
    state: PreparedObservationReadinessState,
    diagnostics: tuple[PreparedObservationDiagnostic, ...],
    limitations: tuple[str, ...],
) -> PreparedObservationResult:
    traceability = _trace(record, diagnostics)
    artifact_lineage = _artifact_lineage(record)
    contract = _contract(record, state, diagnostics, limitations, traceability, artifact_lineage)
    return PreparedObservationResult(
        module_id=MODULE_ID,
        module_version=MODULE_VERSION,
        frozen_design_id=FROZEN_DESIGN_ID,
        fixture_id=record.fixture_id,
        package_id=record.package_id,
        readiness_state=state,
        temporal_alignment_state=record.temporal_alignment_state,
        target_observation=record.target_observation,
        observation_time=record.observation_time,
        comparator_attachments=record.comparator_attachments,
        context_attachments=record.context_attachments,
        coverage=record.coverage,
        missingness=record.missingness,
        limitations=limitations,
        diagnostics=diagnostics,
        source_authority_trace=record.source_authority_trace,
        pit_trace=record.pit_trace,
        comparator_traces=tuple(attachment.trace or {} for attachment in record.comparator_attachments),
        reproducibility=record.reproducibility,
        artifact_lineage=artifact_lineage,
        traceability=traceability,
        information_contract=contract,
    )


def evaluate_prepared_observation(record: PreparedObservationRecord) -> PreparedObservationResult:
    diagnostics: list[PreparedObservationDiagnostic] = []
    limitations: list[str] = list(record.limitations)
    target = record.target_observation

    if len(target.target_applicability_interval_ids) != 1 or not target.target_applicability_interval_id:
        diagnostics.append(_diag(PreparedObservationDiagnosticCode.MISSING_TARGET_APPLICABILITY, "target", "Target must reference exactly one identity applicability interval."))
    elif target.target_applicability_interval_ids[0] != target.target_applicability_interval_id:
        diagnostics.append(_diag(PreparedObservationDiagnosticCode.MISSING_TARGET_APPLICABILITY, "target", "Target applicability interval reference does not match target metadata."))

    if not record.observation_time.has_valid_observation_time():
        diagnostics.append(_diag(PreparedObservationDiagnosticCode.MISSING_OBSERVATION_TIME, "observation_time", "Observation time or approved observation interval is required."))
    if record.observation_time.has_invalid_interval():
        diagnostics.append(_diag(PreparedObservationDiagnosticCode.INVALID_OBSERVATION_INTERVAL, "observation_time", "Observation interval ordering is invalid."))
    if record.observation_time.is_open_interval():
        limitations.append("open observation interval")

    if not record.source_authority_trace:
        diagnostics.append(_diag(PreparedObservationDiagnosticCode.MISSING_SOURCE_AUTHORITY_TRACE, "trace", "Source Authority trace is required."))
    if not record.pit_trace:
        diagnostics.append(_diag(PreparedObservationDiagnosticCode.MISSING_PIT_TRACE, "trace", "PIT Identity and Context trace is required."))

    for context in record.context_attachments:
        if not context.information_role:
            diagnostics.append(_diag(PreparedObservationDiagnosticCode.UNDECLARED_INFORMATION_ROLE, "information_role", f"Context {context.context_id} lacks an information role."))
        elif not _valid_role(context.information_role):
            diagnostics.append(_diag(PreparedObservationDiagnosticCode.UNSUPPORTED_INFORMATION_ROLE, "information_role", f"Context {context.context_id} has unsupported role."))
        if context.identity_applicability_interval_id != target.target_applicability_interval_id:
            diagnostics.append(_diag(PreparedObservationDiagnosticCode.CONFLICTING_EVIDENCE_ATTACHMENT, "context", f"Context {context.context_id} references a different identity interval."))
        if context.required and context.context_id not in record.required_context_ids:
            limitations.append("required context attachment declared by attachment")
        if context.duplicate:
            diagnostics.append(_diag(PreparedObservationDiagnosticCode.DUPLICATE_OBSERVATION_EXPOSURE, "context", f"Duplicate context attachment {context.context_id}."))
        if context.superseded:
            limitations.append("superseded context evidence")
        if context.conflicting:
            diagnostics.append(_diag(PreparedObservationDiagnosticCode.CONFLICTING_EVIDENCE_ATTACHMENT, "context", f"Context {context.context_id} is conflicting."))
        limitations.extend(context.limitations)

    for comparator in record.comparator_attachments:
        if not comparator.information_role:
            diagnostics.append(_diag(PreparedObservationDiagnosticCode.UNDECLARED_INFORMATION_ROLE, "information_role", f"Comparator {comparator.relationship_id} lacks an information role."))
        elif not _valid_role(comparator.information_role):
            diagnostics.append(_diag(PreparedObservationDiagnosticCode.UNSUPPORTED_INFORMATION_ROLE, "information_role", f"Comparator {comparator.relationship_id} has unsupported role."))
        if comparator.required and not comparator.trace:
            diagnostics.append(_diag(PreparedObservationDiagnosticCode.MISSING_COMPARATOR_TRACE, "trace", f"Required comparator {comparator.relationship_id} lacks traceability."))
        if comparator.duplicate:
            diagnostics.append(_diag(PreparedObservationDiagnosticCode.DUPLICATE_OBSERVATION_EXPOSURE, "comparator", f"Duplicate comparator attachment {comparator.relationship_id}."))
        if comparator.superseded:
            limitations.append("superseded comparator relationship")
        if comparator.conflicting:
            diagnostics.append(_diag(PreparedObservationDiagnosticCode.CONFLICTING_EVIDENCE_ATTACHMENT, "comparator", f"Comparator {comparator.relationship_id} is conflicting."))
        if comparator.eligibility_state in {"COMPARATOR_INELIGIBLE", "COMPARATOR_EXCLUDED"}:
            diagnostics.append(_diag(PreparedObservationDiagnosticCode.INHERITED_FATAL_UPSTREAM_DIAGNOSTIC, "comparator", f"Comparator {comparator.relationship_id} inherited fatal eligibility."))
        limitations.extend(comparator.limitations)

    context_ids = {context.context_id for context in record.context_attachments}
    for required_context in record.required_context_ids:
        if required_context not in context_ids:
            diagnostics.append(_diag(PreparedObservationDiagnosticCode.MISSING_REQUIRED_CONTEXT, "context", f"Required context {required_context} is missing."))

    comparator_ids = {comparator.relationship_id for comparator in record.comparator_attachments}
    for required_comparator in record.required_comparator_relationship_ids:
        if required_comparator not in comparator_ids:
            diagnostics.append(_diag(PreparedObservationDiagnosticCode.MISSING_REQUIRED_COMPARATOR, "comparator", f"Required comparator {required_comparator} is missing."))

    if record.explicit_exclusion or record.missingness.intentionally_excluded_evidence:
        diagnostics.append(_diag(PreparedObservationDiagnosticCode.SUPERSEDED_OBSERVATION_PACKAGE if record.superseded_package else PreparedObservationDiagnosticCode.DUPLICATE_OBSERVATION_EXPOSURE, "exclusion", "Prepared package or evidence is explicitly excluded."))
    if record.duplicate_package:
        diagnostics.append(_diag(PreparedObservationDiagnosticCode.DUPLICATE_OBSERVATION_EXPOSURE, "package", "Duplicate prepared-observation package exposure is unresolved."))
    if record.superseded_package:
        diagnostics.append(_diag(PreparedObservationDiagnosticCode.SUPERSEDED_OBSERVATION_PACKAGE, "package", "Prepared-observation package is superseded."))
    if record.conflicting_attachment:
        diagnostics.append(_diag(PreparedObservationDiagnosticCode.CONFLICTING_EVIDENCE_ATTACHMENT, "attachment", "Evidence attachment conflict is unresolved."))
    if record.incomplete_traceability:
        diagnostics.append(_diag(PreparedObservationDiagnosticCode.INCOMPLETE_OBSERVATION_TRACEABILITY, "traceability", "Prepared observation traceability is incomplete."))
    if record.raw_evidence_bypass:
        diagnostics.append(_diag(PreparedObservationDiagnosticCode.RAW_EVIDENCE_ATTACHMENT_PROHIBITED, "contract", "Raw evidence bypasses upstream metadata contracts."))
    if record.prohibited_role_conversion:
        diagnostics.append(_diag(PreparedObservationDiagnosticCode.PROHIBITED_INFORMATION_ROLE_USE, "information_role", "Prohibited information-role conversion requested."))

    if record.source_authority_trace.get("fatal_diagnostics"):
        diagnostics.append(_diag(PreparedObservationDiagnosticCode.INHERITED_FATAL_UPSTREAM_DIAGNOSTIC, "source_authority", "Source Authority trace contains fatal diagnostics.", inherited=True))
    if record.pit_trace.get("fatal_diagnostics"):
        diagnostics.append(_diag(PreparedObservationDiagnosticCode.INHERITED_FATAL_UPSTREAM_DIAGNOSTIC, "pit", "PIT trace contains fatal diagnostics.", inherited=True))
    for comparator in record.comparator_attachments:
        trace = comparator.trace or {}
        if trace.get("fatal_diagnostics"):
            diagnostics.append(_diag(PreparedObservationDiagnosticCode.INHERITED_FATAL_UPSTREAM_DIAGNOSTIC, "comparator", f"Comparator {comparator.relationship_id} trace contains fatal diagnostics.", inherited=True))

    if record.temporal_alignment_state == TemporalAlignmentState.PARTIALLY_ALIGNED:
        limitations.append("partial temporal alignment")
    elif record.temporal_alignment_state == TemporalAlignmentState.NON_OVERLAPPING:
        diagnostics.append(_diag(PreparedObservationDiagnosticCode.NON_OVERLAPPING_TEMPORAL_APPLICABILITY, "temporal_alignment", "Required temporal applicability does not overlap."))
    elif record.temporal_alignment_state == TemporalAlignmentState.UNKNOWN_ALIGNMENT:
        diagnostics.append(_diag(PreparedObservationDiagnosticCode.UNRESOLVED_TEMPORAL_ALIGNMENT, "temporal_alignment", "Temporal alignment is unknown."))
    elif record.temporal_alignment_state == TemporalAlignmentState.STALE_CONTEXTUAL_EVIDENCE:
        limitations.append("stale contextual evidence")
    elif record.temporal_alignment_state == TemporalAlignmentState.SUPERSEDED_CONTEXTUAL_EVIDENCE:
        limitations.append("superseded contextual evidence")
    elif record.temporal_alignment_state == TemporalAlignmentState.EXPIRED_COMPARATOR_APPLICABILITY:
        diagnostics.append(_diag(PreparedObservationDiagnosticCode.NON_OVERLAPPING_TEMPORAL_APPLICABILITY, "temporal_alignment", "Comparator applicability is expired."))
    elif record.temporal_alignment_state == TemporalAlignmentState.DISCONTINUOUS_IDENTITY_APPLICABILITY:
        limitations.append("discontinuous identity applicability")
    elif record.temporal_alignment_state == TemporalAlignmentState.MIXED_FREQUENCY:
        limitations.append("mixed observation frequency")
    elif record.temporal_alignment_state == TemporalAlignmentState.INCOMPLETE_TEMPORAL_TRACEABILITY:
        diagnostics.append(_diag(PreparedObservationDiagnosticCode.UNRESOLVED_TEMPORAL_ALIGNMENT, "temporal_alignment", "Temporal traceability is incomplete."))

    if not record.coverage.is_sufficient():
        diagnostics.append(_diag(PreparedObservationDiagnosticCode.INSUFFICIENT_OBSERVATION_COVERAGE, "coverage", "Required observation coverage is insufficient."))
    if record.coverage.conditionally_governed:
        limitations.append("coverage conditionally governed")
    if record.missingness.required_field_missing:
        diagnostics.append(_diag(PreparedObservationDiagnosticCode.STRUCTURALLY_INCOMPLETE_PACKAGE, "missingness", "Required field missingness blocks structural readiness."))
    if record.missingness.optional_field_missing:
        limitations.append("optional field missing")
    if record.missingness.unavailable_evidence:
        diagnostics.append(_diag(PreparedObservationDiagnosticCode.INSUFFICIENT_OBSERVATION_COVERAGE, "missingness", "Required evidence is unavailable."))
    if not record.reproducibility.deterministic_serialization or record.reproducibility.environment_dependent_output or record.reproducibility.runtime_timestamp_used:
        diagnostics.append(_diag(PreparedObservationDiagnosticCode.INCOMPLETE_OBSERVATION_TRACEABILITY, "reproducibility", "Reproducibility metadata is insufficient."))

    diagnostic_tuple = tuple(diagnostics)
    limitation_tuple = tuple(dict.fromkeys(limitations))
    codes = {diag.code for diag in diagnostic_tuple}

    if (
        record.explicit_exclusion
        or record.missingness.intentionally_excluded_evidence
        or PreparedObservationDiagnosticCode.PROHIBITED_INFORMATION_ROLE_USE in codes
        or record.duplicate_package
        or record.superseded_package
    ):
        state = PreparedObservationReadinessState.EXCLUDED
    elif (
        PreparedObservationDiagnosticCode.MISSING_TARGET_APPLICABILITY in codes
        or PreparedObservationDiagnosticCode.MISSING_OBSERVATION_TIME in codes
        or PreparedObservationDiagnosticCode.INVALID_OBSERVATION_INTERVAL in codes
        or PreparedObservationDiagnosticCode.MISSING_SOURCE_AUTHORITY_TRACE in codes
        or PreparedObservationDiagnosticCode.MISSING_PIT_TRACE in codes
        or PreparedObservationDiagnosticCode.MISSING_COMPARATOR_TRACE in codes
        or PreparedObservationDiagnosticCode.INHERITED_FATAL_UPSTREAM_DIAGNOSTIC in codes
        or PreparedObservationDiagnosticCode.NON_OVERLAPPING_TEMPORAL_APPLICABILITY in codes
        or PreparedObservationDiagnosticCode.CONFLICTING_EVIDENCE_ATTACHMENT in codes
        or PreparedObservationDiagnosticCode.UNDECLARED_INFORMATION_ROLE in codes
        or PreparedObservationDiagnosticCode.DUPLICATE_OBSERVATION_EXPOSURE in codes
        or PreparedObservationDiagnosticCode.INCOMPLETE_OBSERVATION_TRACEABILITY in codes
        or PreparedObservationDiagnosticCode.STRUCTURALLY_INCOMPLETE_PACKAGE in codes
        or PreparedObservationDiagnosticCode.RAW_EVIDENCE_ATTACHMENT_PROHIBITED in codes
    ):
        state = PreparedObservationReadinessState.STRUCTURALLY_INCOMPLETE
    elif PreparedObservationDiagnosticCode.UNRESOLVED_TEMPORAL_ALIGNMENT in codes:
        state = PreparedObservationReadinessState.UNRESOLVED
    elif (
        PreparedObservationDiagnosticCode.INSUFFICIENT_OBSERVATION_COVERAGE in codes
        or PreparedObservationDiagnosticCode.MISSING_REQUIRED_CONTEXT in codes
        or PreparedObservationDiagnosticCode.MISSING_REQUIRED_COMPARATOR in codes
        or PreparedObservationDiagnosticCode.UNSUPPORTED_INFORMATION_ROLE in codes
    ):
        state = PreparedObservationReadinessState.INSUFFICIENT_EVIDENCE
    elif limitation_tuple:
        state = PreparedObservationReadinessState.CONDITIONALLY_READY
    else:
        state = PreparedObservationReadinessState.STRUCTURALLY_READY

    return _final_result(record, state, diagnostic_tuple, limitation_tuple)


def _target(fixture_id: str, interval_ids: tuple[str, ...] | None = None, interval_id: str | None = None) -> TargetObservationMetadata:
    resolved_interval = interval_id or f"target_interval_{fixture_id}"
    return TargetObservationMetadata(
        target_identity_id="synthetic_target",
        target_applicability_interval_ids=interval_ids if interval_ids is not None else (resolved_interval,),
        target_applicability_interval_id=resolved_interval,
    )


def _time(point: int | None = 5, *, interval: ObservationInterval | None = None, unknown: bool = False, unavailable: bool = False) -> ObservationTimeMetadata:
    return ObservationTimeMetadata(
        observation_time=point if interval is None else None,
        observation_interval=interval,
        source_effective_time=1,
        identity_applicability_time="target_interval_time",
        context_applicability_time="context_interval_time",
        comparator_applicability_time="comparator_interval_time",
        unknown_observation_time=unknown,
        unavailable_observation_time=unavailable,
    )


def _context(fixture_id: str, **kwargs: Any) -> ContextEvidenceAttachment:
    values = {
        "context_id": f"context_{fixture_id}",
        "identity_applicability_interval_id": f"target_interval_{fixture_id}",
        "context_applicability_interval_id": f"context_interval_{fixture_id}",
        "information_role": InformationRole.CONTEXTUAL_CONTROL_INFORMATION.value,
        "trace": {"fixture_id": f"PIC_{fixture_id}", "identity_interval_id": f"target_interval_{fixture_id}"},
    }
    values.update(kwargs)
    return ContextEvidenceAttachment(**values)


def _comparator(fixture_id: str, **kwargs: Any) -> ComparatorAttachment:
    values = {
        "relationship_id": f"relationship_{fixture_id}",
        "comparator_identity_id": "synthetic_comparator",
        "comparator_applicability_interval_id": f"comparator_interval_{fixture_id}",
        "information_role": InformationRole.COMPARATOR_OR_BENCHMARK_INFORMATION.value,
        "trace": {"fixture_id": f"CC_{fixture_id}", "relationship_id": f"relationship_{fixture_id}"},
    }
    values.update(kwargs)
    return ComparatorAttachment(**values)


def _base_record(fixture_id: str) -> PreparedObservationRecord:
    return PreparedObservationRecord(
        package_id=f"prepared_package_{fixture_id}",
        fixture_id=fixture_id,
        target_observation=_target(fixture_id),
        observation_time=_time(),
        source_authority_trace={"fixture_id": f"SA_{fixture_id}", "authority_state": "AUTHORITATIVE_FOR_DEFINED_ROLE"},
        pit_trace={"fixture_id": f"PIC_{fixture_id}", "identity_interval_id": f"target_interval_{fixture_id}"},
        comparator_attachments=(_comparator(fixture_id, required=True),),
        context_attachments=(_context(fixture_id, required=True),),
        required_context_ids=(f"context_{fixture_id}",),
        required_comparator_relationship_ids=(f"relationship_{fixture_id}",),
    )


def _replace(record: PreparedObservationRecord, **overrides: Any) -> PreparedObservationRecord:
    values = {**record.__dict__}
    values.update(overrides)
    return PreparedObservationRecord(**values)


def canonical_prepared_observation_fixtures() -> tuple[PreparedObservationFixture, ...]:
    fixtures: list[PreparedObservationFixture] = []

    def add(
        fixture_id: str,
        description: str,
        record: PreparedObservationRecord,
        state: PreparedObservationReadinessState,
        temporal: TemporalAlignmentState | None = None,
        codes: tuple[PreparedObservationDiagnosticCode, ...] = (),
        limitations: tuple[str, ...] = (),
    ) -> None:
        fixtures.append(
            PreparedObservationFixture(
                fixture_id,
                description,
                record,
                state,
                temporal or record.temporal_alignment_state,
                codes,
                limitations,
            )
        )

    add("PO1_ready", "Fully structurally ready package.", _base_record("PO1_ready"), PreparedObservationReadinessState.STRUCTURALLY_READY)
    add("PO2_conditional", "Conditionally ready package.", _replace(_base_record("PO2_conditional"), limitations=("relationship conditionally governed",)), PreparedObservationReadinessState.CONDITIONALLY_READY, limitations=("relationship conditionally governed",))
    add("PO3_unresolved", "Unresolved package.", _replace(_base_record("PO3_unresolved"), temporal_alignment_state=TemporalAlignmentState.UNKNOWN_ALIGNMENT), PreparedObservationReadinessState.UNRESOLVED, TemporalAlignmentState.UNKNOWN_ALIGNMENT, (PreparedObservationDiagnosticCode.UNRESOLVED_TEMPORAL_ALIGNMENT,))
    add("PO4_structurally_incomplete", "Structurally incomplete package.", _replace(_base_record("PO4_structurally_incomplete"), incomplete_traceability=True), PreparedObservationReadinessState.STRUCTURALLY_INCOMPLETE, codes=(PreparedObservationDiagnosticCode.INCOMPLETE_OBSERVATION_TRACEABILITY,))
    add("PO5_excluded", "Explicitly excluded package.", _replace(_base_record("PO5_excluded"), explicit_exclusion=True), PreparedObservationReadinessState.EXCLUDED, codes=(PreparedObservationDiagnosticCode.DUPLICATE_OBSERVATION_EXPOSURE,))
    add("PO6_insufficient", "Insufficient prepared-observation evidence.", _replace(_base_record("PO6_insufficient"), coverage=CoverageMetadata(context_coverage=False)), PreparedObservationReadinessState.INSUFFICIENT_EVIDENCE, codes=(PreparedObservationDiagnosticCode.INSUFFICIENT_OBSERVATION_COVERAGE,))
    add("PO7_missing_target", "Missing target applicability interval.", _replace(_base_record("PO7_missing_target"), target_observation=_target("PO7_missing_target", interval_ids=())), PreparedObservationReadinessState.STRUCTURALLY_INCOMPLETE, codes=(PreparedObservationDiagnosticCode.MISSING_TARGET_APPLICABILITY,))
    add("PO8_missing_time", "Missing observation time.", _replace(_base_record("PO8_missing_time"), observation_time=_time(None)), PreparedObservationReadinessState.STRUCTURALLY_INCOMPLETE, codes=(PreparedObservationDiagnosticCode.MISSING_OBSERVATION_TIME,))
    add("PO9_invalid_interval", "Invalid observation interval.", _replace(_base_record("PO9_invalid_interval"), observation_time=_time(interval=ObservationInterval("bad_interval", 10, 1))), PreparedObservationReadinessState.STRUCTURALLY_INCOMPLETE, codes=(PreparedObservationDiagnosticCode.INVALID_OBSERVATION_INTERVAL,))
    add("PO10_missing_source_trace", "Missing Source Authority trace.", _replace(_base_record("PO10_missing_source_trace"), source_authority_trace={}), PreparedObservationReadinessState.STRUCTURALLY_INCOMPLETE, codes=(PreparedObservationDiagnosticCode.MISSING_SOURCE_AUTHORITY_TRACE,))
    add("PO11_missing_pit_trace", "Missing PIT trace.", _replace(_base_record("PO11_missing_pit_trace"), pit_trace={}), PreparedObservationReadinessState.STRUCTURALLY_INCOMPLETE, codes=(PreparedObservationDiagnosticCode.MISSING_PIT_TRACE,))
    missing_comp = _comparator("PO12_missing_comparator_trace", required=True, trace=None)
    add("PO12_missing_comparator_trace", "Missing required Comparator trace.", _replace(_base_record("PO12_missing_comparator_trace"), comparator_attachments=(missing_comp,)), PreparedObservationReadinessState.STRUCTURALLY_INCOMPLETE, codes=(PreparedObservationDiagnosticCode.MISSING_COMPARATOR_TRACE,))
    add("PO13_inherited_source_fatal", "Inherited fatal Source Authority diagnostic.", _replace(_base_record("PO13_inherited_source_fatal"), source_authority_trace={"fixture_id": "SA_fatal", "fatal_diagnostics": ["TRACEABILITY_INCOMPLETE"]}), PreparedObservationReadinessState.STRUCTURALLY_INCOMPLETE, codes=(PreparedObservationDiagnosticCode.INHERITED_FATAL_UPSTREAM_DIAGNOSTIC,))
    add("PO14_inherited_pit_fatal", "Inherited fatal PIT diagnostic.", _replace(_base_record("PO14_inherited_pit_fatal"), pit_trace={"fixture_id": "PIC_fatal", "fatal_diagnostics": ["NON_RECONSTRUCTABLE_LINEAGE"]}), PreparedObservationReadinessState.STRUCTURALLY_INCOMPLETE, codes=(PreparedObservationDiagnosticCode.INHERITED_FATAL_UPSTREAM_DIAGNOSTIC,))
    fatal_comp = _comparator("PO15_inherited_comparator_fatal", trace={"fixture_id": "CC_fatal", "fatal_diagnostics": ["INCOMPLETE_COMPARATOR_TRACEABILITY"]})
    add("PO15_inherited_comparator_fatal", "Inherited fatal Comparator diagnostic.", _replace(_base_record("PO15_inherited_comparator_fatal"), comparator_attachments=(fatal_comp,)), PreparedObservationReadinessState.STRUCTURALLY_INCOMPLETE, codes=(PreparedObservationDiagnosticCode.INHERITED_FATAL_UPSTREAM_DIAGNOSTIC,))
    add("PO16_fully_aligned", "Fully aligned temporal inputs.", _base_record("PO16_fully_aligned"), PreparedObservationReadinessState.STRUCTURALLY_READY, TemporalAlignmentState.FULLY_ALIGNED)
    add("PO17_partial_alignment", "Partial temporal alignment.", _replace(_base_record("PO17_partial_alignment"), temporal_alignment_state=TemporalAlignmentState.PARTIALLY_ALIGNED), PreparedObservationReadinessState.CONDITIONALLY_READY, TemporalAlignmentState.PARTIALLY_ALIGNED, limitations=("partial temporal alignment",))
    add("PO18_temporal_non_overlap", "Temporal non-overlap.", _replace(_base_record("PO18_temporal_non_overlap"), temporal_alignment_state=TemporalAlignmentState.NON_OVERLAPPING), PreparedObservationReadinessState.STRUCTURALLY_INCOMPLETE, TemporalAlignmentState.NON_OVERLAPPING, (PreparedObservationDiagnosticCode.NON_OVERLAPPING_TEMPORAL_APPLICABILITY,))
    add("PO19_unknown_alignment", "Unknown temporal alignment.", _replace(_base_record("PO19_unknown_alignment"), temporal_alignment_state=TemporalAlignmentState.UNKNOWN_ALIGNMENT), PreparedObservationReadinessState.UNRESOLVED, TemporalAlignmentState.UNKNOWN_ALIGNMENT, (PreparedObservationDiagnosticCode.UNRESOLVED_TEMPORAL_ALIGNMENT,))
    add("PO20_missing_required_context", "Missing required context.", _replace(_base_record("PO20_missing_required_context"), context_attachments=()), PreparedObservationReadinessState.INSUFFICIENT_EVIDENCE, codes=(PreparedObservationDiagnosticCode.MISSING_REQUIRED_CONTEXT,))
    add("PO21_missing_required_comparator", "Missing required comparator.", _replace(_base_record("PO21_missing_required_comparator"), comparator_attachments=()), PreparedObservationReadinessState.INSUFFICIENT_EVIDENCE, codes=(PreparedObservationDiagnosticCode.MISSING_REQUIRED_COMPARATOR,))
    add("PO22_insufficient_coverage", "Insufficient coverage.", _replace(_base_record("PO22_insufficient_coverage"), coverage=CoverageMetadata(target_coverage=False)), PreparedObservationReadinessState.INSUFFICIENT_EVIDENCE, codes=(PreparedObservationDiagnosticCode.INSUFFICIENT_OBSERVATION_COVERAGE,))
    add("PO23_required_missingness", "Required-field missingness.", _replace(_base_record("PO23_required_missingness"), missingness=MissingnessMetadata(required_field_missing=True)), PreparedObservationReadinessState.STRUCTURALLY_INCOMPLETE, codes=(PreparedObservationDiagnosticCode.STRUCTURALLY_INCOMPLETE_PACKAGE,))
    add("PO24_optional_missingness", "Optional-field missingness.", _replace(_base_record("PO24_optional_missingness"), missingness=MissingnessMetadata(optional_field_missing=True)), PreparedObservationReadinessState.CONDITIONALLY_READY, limitations=("optional field missing",))
    bad_context = _context("PO25_undeclared_role", information_role="")
    add("PO25_undeclared_role", "Undeclared information role.", _replace(_base_record("PO25_undeclared_role"), context_attachments=(bad_context,)), PreparedObservationReadinessState.STRUCTURALLY_INCOMPLETE, codes=(PreparedObservationDiagnosticCode.UNDECLARED_INFORMATION_ROLE,))
    unsupported_context = _context("PO26_unsupported_role", information_role="UNAPPROVED_ROLE")
    add("PO26_unsupported_role", "Unsupported information role.", _replace(_base_record("PO26_unsupported_role"), context_attachments=(unsupported_context,)), PreparedObservationReadinessState.INSUFFICIENT_EVIDENCE, codes=(PreparedObservationDiagnosticCode.UNSUPPORTED_INFORMATION_ROLE,))
    add("PO27_prohibited_role_conversion", "Prohibited role conversion.", _replace(_base_record("PO27_prohibited_role_conversion"), prohibited_role_conversion=True), PreparedObservationReadinessState.EXCLUDED, codes=(PreparedObservationDiagnosticCode.PROHIBITED_INFORMATION_ROLE_USE,))
    add("PO28_duplicate_package", "Duplicate package.", _replace(_base_record("PO28_duplicate_package"), duplicate_package=True), PreparedObservationReadinessState.EXCLUDED, codes=(PreparedObservationDiagnosticCode.DUPLICATE_OBSERVATION_EXPOSURE,))
    dup_context = _context("PO29_duplicate_context", duplicate=True)
    add("PO29_duplicate_context", "Duplicate context attachment.", _replace(_base_record("PO29_duplicate_context"), context_attachments=(dup_context,)), PreparedObservationReadinessState.STRUCTURALLY_INCOMPLETE, codes=(PreparedObservationDiagnosticCode.DUPLICATE_OBSERVATION_EXPOSURE,))
    dup_comparator = _comparator("PO30_duplicate_comparator", duplicate=True)
    add("PO30_duplicate_comparator", "Duplicate comparator attachment.", _replace(_base_record("PO30_duplicate_comparator"), comparator_attachments=(dup_comparator,)), PreparedObservationReadinessState.STRUCTURALLY_INCOMPLETE, codes=(PreparedObservationDiagnosticCode.DUPLICATE_OBSERVATION_EXPOSURE,))
    superseded_context = _context("PO31_superseded_context", superseded=True)
    add("PO31_superseded_context", "Superseded context evidence.", _replace(_base_record("PO31_superseded_context"), context_attachments=(superseded_context,)), PreparedObservationReadinessState.CONDITIONALLY_READY, limitations=("superseded context evidence",))
    superseded_comparator = _comparator("PO32_superseded_comparator", superseded=True)
    add("PO32_superseded_comparator", "Superseded comparator relationship.", _replace(_base_record("PO32_superseded_comparator"), comparator_attachments=(superseded_comparator,)), PreparedObservationReadinessState.CONDITIONALLY_READY, limitations=("superseded comparator relationship",))
    add("PO33_superseded_package", "Superseded prepared package.", _replace(_base_record("PO33_superseded_package"), superseded_package=True), PreparedObservationReadinessState.EXCLUDED, codes=(PreparedObservationDiagnosticCode.SUPERSEDED_OBSERVATION_PACKAGE,))
    add("PO34_incomplete_traceability", "Incomplete traceability.", _replace(_base_record("PO34_incomplete_traceability"), incomplete_traceability=True), PreparedObservationReadinessState.STRUCTURALLY_INCOMPLETE, codes=(PreparedObservationDiagnosticCode.INCOMPLETE_OBSERVATION_TRACEABILITY,))
    add("PO35_raw_evidence_bypass", "Raw evidence bypass.", _replace(_base_record("PO35_raw_evidence_bypass"), raw_evidence_bypass=True), PreparedObservationReadinessState.STRUCTURALLY_INCOMPLETE, codes=(PreparedObservationDiagnosticCode.RAW_EVIDENCE_ATTACHMENT_PROHIBITED,))

    return tuple(fixtures)


def prepared_observations_guardrail_manifest() -> dict[str, bool]:
    return {
        "synthetic_metadata_only": True,
        "acquisition_performed": False,
        "retrieval_performed": False,
        "vendor_integration": False,
        "authority_evaluation": False,
        "identity_construction": False,
        "identity_resolution": False,
        "comparator_construction": False,
        "peer_discovery": False,
        "scientific_similarity": False,
        "contextual_interpretation": False,
        "value_transformation": False,
        "normalization": False,
        "ranking": False,
        "winsorization": False,
        "imputation": False,
        "resampling": False,
        "formula_execution": False,
        "signal_construction": False,
        "factor_construction": False,
        "candidate_generation": False,
        "panel_generation": False,
        "discovery_execution": False,
        "ic_computation": False,
        "validation_execution": False,
        "portfolio_construction": False,
        "optimization_performed": False,
        "production_logic": False,
        "ml_integration": False,
    }
