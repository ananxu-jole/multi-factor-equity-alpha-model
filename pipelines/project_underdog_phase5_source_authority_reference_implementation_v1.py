from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import json
from typing import Any


MODULE_ID = "project_underdog_phase5_source_authority_reference_implementation_v1"
MODULE_VERSION = "v1"
FROZEN_DESIGN_ID = "project_underdog_phase5_source_authority_implementation_design_v1"
LAYER_NAME = "Project Underdog Phase 5 Source Authority"


class AuthorityState(str, Enum):
    AUTHORITATIVE = "AUTHORITATIVE_FOR_DEFINED_ROLE"
    CONDITIONAL = "CONDITIONALLY_ACCEPTABLE_FOR_DEFINED_ROLE"
    DIAGNOSTIC_ONLY = "DIAGNOSTIC_ONLY"
    INSUFFICIENT = "INSUFFICIENT_EVIDENCE"
    REJECTED = "REJECTED_FOR_DEFINED_ROLE"


class DiagnosticCode(str, Enum):
    UNAUTHORIZED_SOURCE = "UNAUTHORIZED_SOURCE"
    INSUFFICIENT_AUTHORITY = "INSUFFICIENT_AUTHORITY"
    CONFLICTING_AUTHORITY = "CONFLICTING_AUTHORITY"
    MISSING_PROVENANCE = "MISSING_PROVENANCE"
    MISSING_TEMPORAL_GUARANTEE = "MISSING_TEMPORAL_GUARANTEE"
    UNSUPPORTED_EVIDENCE = "UNSUPPORTED_EVIDENCE"
    UNRESOLVED_AUTHORITY = "UNRESOLVED_AUTHORITY"
    ROLE_SCOPE_VIOLATION = "ROLE_SCOPE_VIOLATION"
    COVERAGE_INSUFFICIENT = "COVERAGE_INSUFFICIENT"
    REVISION_UNRECONSTRUCTABLE = "REVISION_UNRECONSTRUCTABLE"
    REPRODUCIBILITY_INSUFFICIENT = "REPRODUCIBILITY_INSUFFICIENT"
    TRACEABILITY_INCOMPLETE = "TRACEABILITY_INCOMPLETE"
    CONTRACT_MISMATCH = "CONTRACT_MISMATCH"


class GateStatus(str, Enum):
    PASS = "pass"
    WARNING = "warning"
    INSUFFICIENT = "insufficient"
    REJECTED = "rejected"


@dataclass(frozen=True)
class Diagnostic:
    code: DiagnosticCode
    gate: str
    message: str

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
class SourceRegistration:
    source_id: str
    source_name: str
    requested_role: str
    registered_roles: tuple[str, ...]
    source_registered: bool = True
    synthetic_record: bool = True

    def to_dict(self) -> dict[str, Any]:
        return {
            "source_id": self.source_id,
            "source_name": self.source_name,
            "requested_role": self.requested_role,
            "registered_roles": list(self.registered_roles),
            "source_registered": self.source_registered,
            "synthetic_record": self.synthetic_record,
        }


@dataclass(frozen=True)
class ProvenanceMetadata:
    origin: str
    source_version: str
    publication_identity: str
    evidence_references: tuple[str, ...]
    lineage_reference: str
    acquisition_identity: str = "synthetic_controlled_reference"
    retention_status: str = "controlled_reference"

    def is_complete(self) -> bool:
        return bool(
            self.origin
            and self.source_version
            and self.publication_identity
            and self.evidence_references
            and self.lineage_reference
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "acquisition_identity": self.acquisition_identity,
            "evidence_references": list(self.evidence_references),
            "lineage_reference": self.lineage_reference,
            "origin": self.origin,
            "publication_identity": self.publication_identity,
            "retention_status": self.retention_status,
            "source_version": self.source_version,
        }


@dataclass(frozen=True)
class TemporalGuaranteeMetadata:
    effective_date_supported: bool
    publication_or_availability_supported: bool
    revision_date_supported: bool
    snapshot_or_project_known_supported: bool
    historical_reconstruction_supported: bool
    temporal_scope: str
    uncertainty_interval: str = ""
    conservative_delay_rule: str = ""

    def is_sufficient(self) -> bool:
        return (
            self.effective_date_supported
            and self.publication_or_availability_supported
            and self.revision_date_supported
            and self.snapshot_or_project_known_supported
            and self.historical_reconstruction_supported
            and bool(self.temporal_scope)
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "conservative_delay_rule": self.conservative_delay_rule,
            "effective_date_supported": self.effective_date_supported,
            "historical_reconstruction_supported": self.historical_reconstruction_supported,
            "publication_or_availability_supported": self.publication_or_availability_supported,
            "revision_date_supported": self.revision_date_supported,
            "snapshot_or_project_known_supported": self.snapshot_or_project_known_supported,
            "temporal_scope": self.temporal_scope,
            "uncertainty_interval": self.uncertainty_interval,
        }


@dataclass(frozen=True)
class AuthorityEvidenceMetadata:
    official_definitions: bool
    data_dictionary: bool
    historical_methodology: bool
    date_semantics: bool
    revision_policy: bool
    coverage_evidence: bool
    reproducibility_evidence: bool
    unsupported_evidence: bool = False

    def is_sufficient(self) -> bool:
        return (
            self.official_definitions
            and self.data_dictionary
            and self.historical_methodology
            and self.date_semantics
            and self.revision_policy
            and self.coverage_evidence
            and self.reproducibility_evidence
            and not self.unsupported_evidence
        )

    def to_dict(self) -> dict[str, bool]:
        return {
            "coverage_evidence": self.coverage_evidence,
            "data_dictionary": self.data_dictionary,
            "date_semantics": self.date_semantics,
            "historical_methodology": self.historical_methodology,
            "official_definitions": self.official_definitions,
            "reproducibility_evidence": self.reproducibility_evidence,
            "revision_policy": self.revision_policy,
            "unsupported_evidence": self.unsupported_evidence,
        }


@dataclass(frozen=True)
class SourceAuthorityRecord:
    registration: SourceRegistration
    provenance: ProvenanceMetadata
    temporal_guarantees: TemporalGuaranteeMetadata
    evidence: AuthorityEvidenceMetadata
    fixture_id: str = ""
    module_id: str = MODULE_ID
    frozen_design_id: str = FROZEN_DESIGN_ID
    conflict_present: bool = False
    unresolved_authority: bool = False
    coverage_sufficient: bool = True
    coverage_conditionally_governed: bool = False
    revision_reconstructable: bool = True
    reproducibility_sufficient: bool = True
    diagnostic_only_requested: bool = False
    conditional_limitations: tuple[str, ...] = ()
    traceability_complete: bool = True


@dataclass(frozen=True)
class InformationContract:
    authority_state: AuthorityState
    supported_roles: tuple[str, ...]
    unsupported_roles: tuple[str, ...]
    provenance: ProvenanceMetadata
    temporal_guarantees: TemporalGuaranteeMetadata
    limitations: tuple[str, ...]
    diagnostics: tuple[Diagnostic, ...]
    traceability: dict[str, Any]
    exposes_raw_values: bool = False
    exposes_retrieval: bool = False
    exposes_queries: bool = False
    constructs_identity: bool = False
    constructs_peers: bool = False
    exposes_formulas: bool = False
    creates_candidates: bool = False
    creates_panels: bool = False
    computes_ic: bool = False
    runs_validation: bool = False
    makes_production_decisions: bool = False
    exposes_ml_inputs: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "authority_state": self.authority_state.value,
            "computes_ic": self.computes_ic,
            "constructs_identity": self.constructs_identity,
            "constructs_peers": self.constructs_peers,
            "creates_candidates": self.creates_candidates,
            "creates_panels": self.creates_panels,
            "diagnostics": [diag.to_dict() for diag in self.diagnostics],
            "exposes_formulas": self.exposes_formulas,
            "exposes_ml_inputs": self.exposes_ml_inputs,
            "exposes_queries": self.exposes_queries,
            "exposes_raw_values": self.exposes_raw_values,
            "exposes_retrieval": self.exposes_retrieval,
            "limitations": list(self.limitations),
            "makes_production_decisions": self.makes_production_decisions,
            "provenance": self.provenance.to_dict(),
            "runs_validation": self.runs_validation,
            "supported_roles": list(self.supported_roles),
            "temporal_guarantees": self.temporal_guarantees.to_dict(),
            "traceability": self.traceability,
            "unsupported_roles": list(self.unsupported_roles),
        }


@dataclass(frozen=True)
class SourceAuthorityResult:
    module_id: str
    module_version: str
    frozen_design_id: str
    fixture_id: str
    source_id: str
    requested_role: str
    authority_state: AuthorityState
    supported_roles: tuple[str, ...]
    unsupported_roles: tuple[str, ...]
    limitations: tuple[str, ...]
    diagnostics: tuple[Diagnostic, ...]
    gate_outcomes: tuple[GateOutcome, ...]
    provenance: ProvenanceMetadata
    temporal_guarantees: TemporalGuaranteeMetadata
    traceability: dict[str, Any]
    information_contract: InformationContract
    external_retrieval_performed: bool = False
    vendor_integration: bool = False
    acquisition_performed: bool = False
    identity_construction: bool = False
    comparator_construction: bool = False
    contextual_measurement: bool = False
    formula_execution: bool = False
    discovery_execution: bool = False
    validation_execution: bool = False
    production_logic: bool = False
    optimization_performed: bool = False
    ml_integration: bool = False

    def to_ordered_dict(self) -> dict[str, Any]:
        return {
            "acquisition_performed": self.acquisition_performed,
            "authority_state": self.authority_state.value,
            "comparator_construction": self.comparator_construction,
            "contextual_measurement": self.contextual_measurement,
            "diagnostics": [diag.to_dict() for diag in self.diagnostics],
            "discovery_execution": self.discovery_execution,
            "external_retrieval_performed": self.external_retrieval_performed,
            "fixture_id": self.fixture_id,
            "formula_execution": self.formula_execution,
            "frozen_design_id": self.frozen_design_id,
            "gate_outcomes": [gate.to_dict() for gate in self.gate_outcomes],
            "identity_construction": self.identity_construction,
            "information_contract": self.information_contract.to_dict(),
            "limitations": list(self.limitations),
            "ml_integration": self.ml_integration,
            "module_id": self.module_id,
            "module_version": self.module_version,
            "optimization_performed": self.optimization_performed,
            "production_logic": self.production_logic,
            "provenance": self.provenance.to_dict(),
            "requested_role": self.requested_role,
            "source_id": self.source_id,
            "supported_roles": list(self.supported_roles),
            "temporal_guarantees": self.temporal_guarantees.to_dict(),
            "traceability": self.traceability,
            "unsupported_roles": list(self.unsupported_roles),
            "validation_execution": self.validation_execution,
            "vendor_integration": self.vendor_integration,
        }

    def stable_json(self) -> str:
        return json.dumps(self.to_ordered_dict(), sort_keys=True, separators=(",", ":"))


@dataclass(frozen=True)
class SourceAuthorityFixture:
    fixture_id: str
    description: str
    record: SourceAuthorityRecord
    expected_authority_state: AuthorityState
    expected_diagnostic_codes: tuple[DiagnosticCode, ...] = ()


def _diag(code: DiagnosticCode, gate: str, message: str) -> Diagnostic:
    return Diagnostic(code=code, gate=gate, message=message)


def _gate(gate: str, status: GateStatus, diagnostics: tuple[Diagnostic, ...] = ()) -> GateOutcome:
    return GateOutcome(gate=gate, status=status, diagnostics=diagnostics)


def _trace(record: SourceAuthorityRecord, gate_outcomes: tuple[GateOutcome, ...]) -> dict[str, Any]:
    return {
        "authority_evidence_metadata": record.evidence.to_dict(),
        "coverage_conditionally_governed": record.coverage_conditionally_governed,
        "coverage_sufficient": record.coverage_sufficient,
        "fixture_id": record.fixture_id,
        "frozen_specifications": [
            "project_underdog_phase5_source_authority_implementation_design_v1",
            "project_underdog_phase5_external_information_authority_science_v1",
            "project_underdog_phase5_integrated_scientific_information_inventory_v1",
            "project_underdog_platform_v2_scientific_research_standard_v1",
        ],
        "gate_sequence": [gate.gate for gate in gate_outcomes],
        "layer_name": LAYER_NAME,
        "reproducibility_sufficient": record.reproducibility_sufficient,
        "requested_role": record.registration.requested_role,
        "revision_reconstructable": record.revision_reconstructable,
        "source_id": record.registration.source_id,
        "synthetic_record": record.registration.synthetic_record,
    }


def _final_result(
    record: SourceAuthorityRecord,
    state: AuthorityState,
    gates: list[GateOutcome],
    limitations: tuple[str, ...] = (),
) -> SourceAuthorityResult:
    diagnostics = tuple(diag for gate in gates for diag in gate.diagnostics)
    supported_roles = (
        (record.registration.requested_role,)
        if state in (AuthorityState.AUTHORITATIVE, AuthorityState.CONDITIONAL)
        else ()
    )
    unsupported_roles = (
        ()
        if state in (AuthorityState.AUTHORITATIVE, AuthorityState.CONDITIONAL)
        else (record.registration.requested_role,)
    )
    gate_tuple = tuple(gates)
    traceability = _trace(record, gate_tuple)
    contract = InformationContract(
        authority_state=state,
        supported_roles=supported_roles,
        unsupported_roles=unsupported_roles,
        provenance=record.provenance,
        temporal_guarantees=record.temporal_guarantees,
        limitations=limitations,
        diagnostics=diagnostics,
        traceability=traceability,
    )
    return SourceAuthorityResult(
        module_id=MODULE_ID,
        module_version=MODULE_VERSION,
        frozen_design_id=FROZEN_DESIGN_ID,
        fixture_id=record.fixture_id,
        source_id=record.registration.source_id,
        requested_role=record.registration.requested_role,
        authority_state=state,
        supported_roles=supported_roles,
        unsupported_roles=unsupported_roles,
        limitations=limitations,
        diagnostics=diagnostics,
        gate_outcomes=gate_tuple,
        provenance=record.provenance,
        temporal_guarantees=record.temporal_guarantees,
        traceability=traceability,
        information_contract=contract,
    )


def evaluate_source_authority(record: SourceAuthorityRecord) -> SourceAuthorityResult:
    """Evaluate synthetic source-role authority using metadata only."""

    gates: list[GateOutcome] = []
    if record.module_id != MODULE_ID or record.frozen_design_id != FROZEN_DESIGN_ID:
        diagnostics = (
            _diag(
                DiagnosticCode.CONTRACT_MISMATCH,
                "contract_conformance",
                "Record does not match the approved Source Authority reference implementation contract.",
            ),
        )
        gates.append(_gate("contract_conformance", GateStatus.REJECTED, diagnostics))
        return _final_result(record, AuthorityState.REJECTED, gates)
    gates.append(_gate("contract_conformance", GateStatus.PASS))

    if not record.registration.synthetic_record or not record.registration.source_registered:
        diagnostics = (
            _diag(
                DiagnosticCode.UNAUTHORIZED_SOURCE,
                "source_registration",
                "Source Authority accepts only registered synthetic source authority records.",
            ),
        )
        gates.append(_gate("source_registration", GateStatus.REJECTED, diagnostics))
        return _final_result(record, AuthorityState.REJECTED, gates)
    if record.registration.requested_role not in record.registration.registered_roles:
        diagnostics = (
            _diag(
                DiagnosticCode.ROLE_SCOPE_VIOLATION,
                "source_registration",
                "Requested role is outside the registered role scope.",
            ),
        )
        gates.append(_gate("source_registration", GateStatus.REJECTED, diagnostics))
        return _final_result(record, AuthorityState.REJECTED, gates)
    gates.append(_gate("source_registration", GateStatus.PASS))

    if not record.provenance.is_complete():
        diagnostics = (
            _diag(
                DiagnosticCode.MISSING_PROVENANCE,
                "provenance",
                "Origin, version, publication identity, evidence references, and lineage are required.",
            ),
        )
        gates.append(_gate("provenance", GateStatus.INSUFFICIENT, diagnostics))
        fatal_insufficient = True
    else:
        gates.append(_gate("provenance", GateStatus.PASS))
        fatal_insufficient = False

    if not record.temporal_guarantees.is_sufficient():
        diagnostics = (
            _diag(
                DiagnosticCode.MISSING_TEMPORAL_GUARANTEE,
                "temporal_guarantees",
                "Effective, availability, revision, snapshot, reconstruction, and scope semantics are required.",
            ),
        )
        gates.append(_gate("temporal_guarantees", GateStatus.INSUFFICIENT, diagnostics))
        fatal_insufficient = True
    else:
        gates.append(_gate("temporal_guarantees", GateStatus.PASS))

    if record.conflict_present:
        diagnostics = (
            _diag(
                DiagnosticCode.CONFLICTING_AUTHORITY,
                "authority_conflict",
                "Material source-role authority conflict is unresolved.",
            ),
        )
        gates.append(_gate("authority_conflict", GateStatus.INSUFFICIENT, diagnostics))
        fatal_insufficient = True
    else:
        gates.append(_gate("authority_conflict", GateStatus.PASS))

    diagnostic_only = False
    final_limitations: tuple[str, ...] = ()
    if record.evidence.unsupported_evidence:
        diagnostics = (
            _diag(
                DiagnosticCode.UNSUPPORTED_EVIDENCE,
                "evidence_strength",
                "Unsupported evidence cannot establish authoritative source-role status.",
            ),
        )
        gates.append(_gate("evidence_strength", GateStatus.WARNING, diagnostics))
        diagnostic_only = True
        final_limitations = final_limitations + ("unsupported evidence limits use to diagnostics",)
    elif not record.evidence.is_sufficient():
        diagnostics = (
            _diag(
                DiagnosticCode.INSUFFICIENT_AUTHORITY,
                "evidence_strength",
                "Required official definitions, dictionaries, methodology, dates, revisions, coverage, or reproducibility evidence is missing.",
            ),
        )
        gates.append(_gate("evidence_strength", GateStatus.INSUFFICIENT, diagnostics))
        fatal_insufficient = True
    else:
        gates.append(_gate("evidence_strength", GateStatus.PASS))

    if record.unresolved_authority:
        diagnostics = (
            _diag(
                DiagnosticCode.UNRESOLVED_AUTHORITY,
                "authority_resolution",
                "A required authority question remains unresolved.",
            ),
        )
        gates.append(_gate("authority_resolution", GateStatus.INSUFFICIENT, diagnostics))
        fatal_insufficient = True
    else:
        gates.append(_gate("authority_resolution", GateStatus.PASS))

    if not record.coverage_sufficient:
        diagnostics = (
            _diag(
                DiagnosticCode.COVERAGE_INSUFFICIENT,
                "coverage",
                "Coverage is insufficient for unconditional authority.",
            ),
        )
        if record.coverage_conditionally_governed and record.conditional_limitations:
            gates.append(_gate("coverage", GateStatus.WARNING, diagnostics))
            final_limitations = final_limitations + record.conditional_limitations
        else:
            gates.append(_gate("coverage", GateStatus.INSUFFICIENT, diagnostics))
            fatal_insufficient = True
    else:
        gates.append(_gate("coverage", GateStatus.PASS))

    fatal_rejected = False
    if not record.revision_reconstructable:
        diagnostics = (
            _diag(
                DiagnosticCode.REVISION_UNRECONSTRUCTABLE,
                "revision_reconstruction",
                "Historical source revisions cannot be reconstructed as knowable at the relevant time.",
            ),
        )
        gates.append(_gate("revision_reconstruction", GateStatus.REJECTED, diagnostics))
        fatal_rejected = True
    else:
        gates.append(_gate("revision_reconstruction", GateStatus.PASS))

    if not record.reproducibility_sufficient:
        diagnostics = (
            _diag(
                DiagnosticCode.REPRODUCIBILITY_INSUFFICIENT,
                "reproducibility",
                "Evidence cannot be retained, reconstructed, or controlled-referenced sufficiently.",
            ),
        )
        gates.append(_gate("reproducibility", GateStatus.INSUFFICIENT, diagnostics))
        fatal_insufficient = True
    else:
        gates.append(_gate("reproducibility", GateStatus.PASS))

    if record.diagnostic_only_requested:
        diagnostics = (
            _diag(
                DiagnosticCode.UNSUPPORTED_EVIDENCE,
                "authority_scope",
                "Record is explicitly scoped to diagnostic-only use.",
            ),
        )
        gates.append(_gate("authority_scope", GateStatus.WARNING, diagnostics))
        diagnostic_only = True
        final_limitations = final_limitations + ("diagnostic-only scope",)
    else:
        gates.append(_gate("authority_scope", GateStatus.PASS))

    if not record.traceability_complete:
        diagnostics = (
            _diag(
                DiagnosticCode.TRACEABILITY_INCOMPLETE,
                "traceability",
                "Authority decision lineage is incomplete.",
            ),
        )
        gates.append(_gate("traceability", GateStatus.REJECTED, diagnostics))
        fatal_rejected = True
    else:
        gates.append(_gate("traceability", GateStatus.PASS))

    if fatal_rejected:
        return _final_result(record, AuthorityState.REJECTED, gates, final_limitations)
    if fatal_insufficient:
        return _final_result(record, AuthorityState.INSUFFICIENT, gates, final_limitations)
    if diagnostic_only:
        return _final_result(record, AuthorityState.DIAGNOSTIC_ONLY, gates, final_limitations)
    if final_limitations:
        return _final_result(record, AuthorityState.CONDITIONAL, gates, final_limitations)
    if record.conditional_limitations:
        return _final_result(record, AuthorityState.CONDITIONAL, gates, record.conditional_limitations)

    return _final_result(record, AuthorityState.AUTHORITATIVE, gates)


def _base_record(fixture_id: str) -> SourceAuthorityRecord:
    return SourceAuthorityRecord(
        fixture_id=fixture_id,
        registration=SourceRegistration(
            source_id=f"synthetic_source_{fixture_id}",
            source_name=f"Synthetic Source {fixture_id}",
            requested_role="historical_classification_authority",
            registered_roles=("historical_classification_authority", "ticker_lineage_authority"),
        ),
        provenance=ProvenanceMetadata(
            origin="synthetic_authority_fixture",
            source_version="synthetic_v1",
            publication_identity="synthetic_publication_reference_v1",
            evidence_references=("synthetic_evidence_matrix_v1",),
            lineage_reference=f"authority_lineage_{fixture_id}",
        ),
        temporal_guarantees=TemporalGuaranteeMetadata(
            effective_date_supported=True,
            publication_or_availability_supported=True,
            revision_date_supported=True,
            snapshot_or_project_known_supported=True,
            historical_reconstruction_supported=True,
            temporal_scope="synthetic historical authority interval",
        ),
        evidence=AuthorityEvidenceMetadata(
            official_definitions=True,
            data_dictionary=True,
            historical_methodology=True,
            date_semantics=True,
            revision_policy=True,
            coverage_evidence=True,
            reproducibility_evidence=True,
        ),
    )


def canonical_source_authority_fixtures() -> tuple[SourceAuthorityFixture, ...]:
    authoritative = _base_record("SA1_authoritative")
    conditional = SourceAuthorityRecord(
        **{
            **_base_record("SA2_conditional").__dict__,
            "conditional_limitations": ("role limited to synthetic 2000-2010 interval",),
        }
    )
    diagnostic = SourceAuthorityRecord(
        **{
            **_base_record("SA3_diagnostic_only").__dict__,
            "diagnostic_only_requested": True,
        }
    )
    rejected = SourceAuthorityRecord(
        **{
            **_base_record("SA4_rejected").__dict__,
            "revision_reconstructable": False,
        }
    )
    insufficient = SourceAuthorityRecord(
        **{
            **_base_record("SA5_insufficient_evidence").__dict__,
            "evidence": AuthorityEvidenceMetadata(
                official_definitions=True,
                data_dictionary=False,
                historical_methodology=True,
                date_semantics=True,
                revision_policy=True,
                coverage_evidence=True,
                reproducibility_evidence=True,
            ),
        }
    )
    conflict = SourceAuthorityRecord(**{**_base_record("SA6_conflict").__dict__, "conflict_present": True})
    missing_provenance = SourceAuthorityRecord(
        **{
            **_base_record("SA7_missing_provenance").__dict__,
            "provenance": ProvenanceMetadata(
                origin="",
                source_version="synthetic_v1",
                publication_identity="synthetic_publication_reference_v1",
                evidence_references=("synthetic_evidence_matrix_v1",),
                lineage_reference="authority_lineage_missing_provenance",
            ),
        }
    )
    missing_temporal = SourceAuthorityRecord(
        **{
            **_base_record("SA8_missing_temporal").__dict__,
            "temporal_guarantees": TemporalGuaranteeMetadata(
                effective_date_supported=True,
                publication_or_availability_supported=False,
                revision_date_supported=True,
                snapshot_or_project_known_supported=True,
                historical_reconstruction_supported=True,
                temporal_scope="synthetic historical authority interval",
            ),
        }
    )
    role_scope = SourceAuthorityRecord(
        **{
            **_base_record("SA9_role_scope_violation").__dict__,
            "registration": SourceRegistration(
                source_id="synthetic_source_SA9_role_scope_violation",
                source_name="Synthetic Source SA9 Role Scope",
                requested_role="shares_outstanding_authority",
                registered_roles=("historical_classification_authority",),
            ),
        }
    )
    unreconstructable = SourceAuthorityRecord(
        **{
            **_base_record("SA10_unreconstructable_revision").__dict__,
            "revision_reconstructable": False,
        }
    )
    insufficient_repro = SourceAuthorityRecord(
        **{
            **_base_record("SA11_insufficient_reproducibility").__dict__,
            "reproducibility_sufficient": False,
        }
    )

    return (
        SourceAuthorityFixture("SA1_authoritative", "Fully authoritative source-role.", authoritative, AuthorityState.AUTHORITATIVE),
        SourceAuthorityFixture("SA2_conditional", "Conditionally acceptable source-role.", conditional, AuthorityState.CONDITIONAL),
        SourceAuthorityFixture(
            "SA3_diagnostic_only",
            "Diagnostic-only source-role.",
            diagnostic,
            AuthorityState.DIAGNOSTIC_ONLY,
            (DiagnosticCode.UNSUPPORTED_EVIDENCE,),
        ),
        SourceAuthorityFixture(
            "SA4_rejected",
            "Rejected source-role.",
            rejected,
            AuthorityState.REJECTED,
            (DiagnosticCode.REVISION_UNRECONSTRUCTABLE,),
        ),
        SourceAuthorityFixture(
            "SA5_insufficient_evidence",
            "Insufficient evidence.",
            insufficient,
            AuthorityState.INSUFFICIENT,
            (DiagnosticCode.INSUFFICIENT_AUTHORITY,),
        ),
        SourceAuthorityFixture(
            "SA6_conflict",
            "Conflicting authority.",
            conflict,
            AuthorityState.INSUFFICIENT,
            (DiagnosticCode.CONFLICTING_AUTHORITY,),
        ),
        SourceAuthorityFixture(
            "SA7_missing_provenance",
            "Missing provenance.",
            missing_provenance,
            AuthorityState.INSUFFICIENT,
            (DiagnosticCode.MISSING_PROVENANCE,),
        ),
        SourceAuthorityFixture(
            "SA8_missing_temporal",
            "Missing temporal guarantee.",
            missing_temporal,
            AuthorityState.INSUFFICIENT,
            (DiagnosticCode.MISSING_TEMPORAL_GUARANTEE,),
        ),
        SourceAuthorityFixture(
            "SA9_role_scope_violation",
            "Role scope violation.",
            role_scope,
            AuthorityState.REJECTED,
            (DiagnosticCode.ROLE_SCOPE_VIOLATION,),
        ),
        SourceAuthorityFixture(
            "SA10_unreconstructable_revision",
            "Unreconstructable revision history.",
            unreconstructable,
            AuthorityState.REJECTED,
            (DiagnosticCode.REVISION_UNRECONSTRUCTABLE,),
        ),
        SourceAuthorityFixture(
            "SA11_insufficient_reproducibility",
            "Insufficient reproducibility.",
            insufficient_repro,
            AuthorityState.INSUFFICIENT,
            (DiagnosticCode.REPRODUCIBILITY_INSUFFICIENT,),
        ),
    )


def source_authority_guardrail_manifest() -> dict[str, bool]:
    return {
        "source_independent": True,
        "synthetic_records_only": True,
        "external_data_retrieval": False,
        "vendor_integration": False,
        "acquisition_performed": False,
        "identity_construction": False,
        "comparator_construction": False,
        "contextual_measurement": False,
        "formula_execution": False,
        "candidate_generation": False,
        "panel_generation": False,
        "ic_computation": False,
        "discovery_executed": False,
        "validation_executed": False,
        "production_logic": False,
        "optimization_performed": False,
        "ml_integration": False,
    }
