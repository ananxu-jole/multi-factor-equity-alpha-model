from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from pipelines.project_underdog_first_module_reference_implementation_v1 import (
    canonical_fixtures as first_module_fixtures,
    run_first_module_reference,
)
from pipelines.project_underdog_phase5_pit_identity_and_context_evidence_reference_implementation_v1 import (
    ApplicabilityState,
    ContextEvidenceMetadata,
    ContextEvidenceStatus,
    DiagnosticCode,
    IdentityApplicabilityMetadata,
    IdentityLineageMetadata,
    IdentityMetadata,
    IdentityStatus,
    PitIdentityContextRecord,
    TimeIntervalMetadata,
    canonical_pit_identity_context_fixtures,
    evaluate_pit_identity_context,
    pit_identity_context_guardrail_manifest,
)
from pipelines.project_underdog_phase5_source_authority_reference_implementation_v1 import (
    AuthorityState,
    canonical_source_authority_fixtures,
    evaluate_source_authority,
)


def _diagnostic_codes(result):
    return tuple(diag.code for diag in result.diagnostics)


def _fixture_by_id(fixture_id: str):
    return {fixture.fixture_id: fixture for fixture in canonical_pit_identity_context_fixtures()}[fixture_id]


def _base_record(**overrides):
    fixture = _fixture_by_id("PIC1_normal_identity")
    values = {**fixture.record.__dict__}
    values.update(overrides)
    return PitIdentityContextRecord(**values)


def _interval(interval_id: str, start: int | None = 1, end: int | None = 10, **kwargs):
    return TimeIntervalMetadata(interval_id=interval_id, effective_start=start, effective_end=end, **kwargs)


def test_all_canonical_pit_identity_context_fixtures_match_expected_states_and_diagnostics():
    fixtures = canonical_pit_identity_context_fixtures()
    assert len(fixtures) == 14
    assert len({fixture.fixture_id for fixture in fixtures}) == 14

    for fixture in fixtures:
        result = evaluate_pit_identity_context(fixture.record)
        assert result.applicability_state == fixture.expected_applicability_state
        assert result.fixture_id == fixture.fixture_id
        for expected_code in fixture.expected_diagnostic_codes:
            assert expected_code in _diagnostic_codes(result)
        for expected_limitation in fixture.expected_limitations:
            assert expected_limitation in result.limitations


def test_identity_registration_preserves_canonical_identity_metadata_without_construction():
    result = evaluate_pit_identity_context(_fixture_by_id("PIC1_normal_identity").record)

    assert result.applicability_state == ApplicabilityState.APPLICABLE
    identity = result.identity_applicability.identity
    assert identity.canonical_identity == "synthetic_identity_PIC1_normal_identity"
    assert identity.identity_level == "security"
    assert identity.synthetic_identity is True
    assert result.identity_construction is False


def test_alias_identity_registration_preserves_alias_metadata():
    result = evaluate_pit_identity_context(_fixture_by_id("PIC2_alias_identity").record)

    assert result.applicability_state == ApplicabilityState.APPLICABLE
    assert result.identity_applicability.identity.aliases == ("SYN.A", "SYN-A")
    assert result.information_contract.canonical_identity_metadata["aliases"] == ["SYN.A", "SYN-A"]


def test_lineage_registration_preserves_predecessor_and_successor_metadata():
    result = evaluate_pit_identity_context(_fixture_by_id("PIC3_successor_predecessor").record)

    lineage = result.identity_applicability.lineage
    assert lineage.predecessor_identity == "synthetic_predecessor"
    assert lineage.successor_identity == "synthetic_successor"
    assert lineage.continuity_supported is True


def test_context_evidence_must_reference_exactly_one_identity_applicability_interval():
    result = evaluate_pit_identity_context(_fixture_by_id("PIC13_conflicting_association").record)

    assert result.applicability_state == ApplicabilityState.UNRESOLVED
    assert DiagnosticCode.CONFLICTING_IDENTITY_ASSOCIATION in _diagnostic_codes(result)

    valid = evaluate_pit_identity_context(_fixture_by_id("PIC1_normal_identity").record)
    interval_id = valid.identity_applicability.interval.interval_id
    assert all(context.identity_applicability_interval_id == interval_id for context in valid.context_evidence)


def test_missing_context_and_missing_applicability_remain_distinct_diagnostics():
    missing_context = evaluate_pit_identity_context(_fixture_by_id("PIC12_missing_context").record)
    missing_applicability = evaluate_pit_identity_context(_fixture_by_id("PIC8_missing_applicability").record)

    assert DiagnosticCode.MISSING_CONTEXTUAL_EVIDENCE in _diagnostic_codes(missing_context)
    assert DiagnosticCode.INCOMPLETE_APPLICABILITY in _diagnostic_codes(missing_applicability)
    assert DiagnosticCode.CONFLICTING_IDENTITY_ASSOCIATION not in _diagnostic_codes(missing_applicability)


def test_invalid_temporal_ordering_fails_closed_without_pit_construction():
    bad_interval = _interval("identity_interval_bad_ordering", start=10, end=1)
    base = _fixture_by_id("PIC1_normal_identity").record
    record = PitIdentityContextRecord(
        **{
            **base.__dict__,
            "identity_applicability": IdentityApplicabilityMetadata(
                identity=IdentityMetadata("synthetic_bad_ordering", "security", (), IdentityStatus.VALID),
                interval=bad_interval,
                lineage=IdentityLineageMetadata("lineage_bad_ordering"),
            ),
            "context_evidence": (
                ContextEvidenceMetadata(
                    "context_bad_ordering",
                    "historical_classification_context",
                    bad_interval.interval_id,
                    _interval("context_interval_bad_ordering"),
                ),
            ),
        }
    )

    result = evaluate_pit_identity_context(record)
    assert result.applicability_state == ApplicabilityState.REJECTED
    assert DiagnosticCode.INVALID_TEMPORAL_ORDERING in _diagnostic_codes(result)
    assert result.contextual_measurement is False


def test_unsupported_continuity_and_non_reconstructable_lineage_are_separate_failures():
    base = _fixture_by_id("PIC1_normal_identity").record
    unsupported = _base_record(
        identity_applicability=IdentityApplicabilityMetadata(
            identity=base.identity_applicability.identity,
            interval=base.identity_applicability.interval,
            lineage=IdentityLineageMetadata("lineage_unsupported", continuity_supported=False),
        )
    )
    non_reconstructable = _fixture_by_id("PIC11_non_reconstructable_interval").record

    unsupported_result = evaluate_pit_identity_context(unsupported)
    non_reconstructable_result = evaluate_pit_identity_context(non_reconstructable)
    assert unsupported_result.applicability_state == ApplicabilityState.UNRESOLVED
    assert DiagnosticCode.UNSUPPORTED_CONTINUITY in _diagnostic_codes(unsupported_result)
    assert non_reconstructable_result.applicability_state == ApplicabilityState.REJECTED
    assert DiagnosticCode.NON_RECONSTRUCTABLE_LINEAGE in _diagnostic_codes(non_reconstructable_result)


def test_source_authority_state_must_be_accepted_before_applicability_can_pass():
    record = _base_record(source_authority_state=AuthorityState.INSUFFICIENT)
    result = evaluate_pit_identity_context(record)

    assert result.applicability_state == ApplicabilityState.REJECTED
    assert DiagnosticCode.SOURCE_AUTHORITY_NOT_ACCEPTED in _diagnostic_codes(result)
    assert result.authority_evaluation_performed is False


def test_context_statuses_emit_expected_diagnostics():
    base = _fixture_by_id("PIC1_normal_identity").record
    interval_id = base.identity_applicability.interval.interval_id
    cases = (
        (ContextEvidenceStatus.MISSING, DiagnosticCode.MISSING_CONTEXTUAL_EVIDENCE),
        (ContextEvidenceStatus.INCOMPLETE, DiagnosticCode.INCOMPLETE_APPLICABILITY),
        (ContextEvidenceStatus.OVERLAPPING, DiagnosticCode.OVERLAPPING_CONTEXT_INTERVALS),
        (ContextEvidenceStatus.CONFLICTING, DiagnosticCode.CONFLICTING_IDENTITY_ASSOCIATION),
    )

    for status, expected in cases:
        record = _base_record(
            context_evidence=(
                ContextEvidenceMetadata(
                    f"context_{status.value}",
                    "historical_classification_context",
                    interval_id,
                    _interval(f"context_interval_{status.value}"),
                    status=status,
                ),
            )
        )
        result = evaluate_pit_identity_context(record)
        assert expected in _diagnostic_codes(result)


def test_information_contract_refuses_prohibited_outputs():
    result = evaluate_pit_identity_context(_fixture_by_id("PIC1_normal_identity").record)
    contract = result.information_contract

    assert contract.exposes_raw_source_values is False
    assert contract.exposes_retrieval is False
    assert contract.performs_authority_evaluation is False
    assert contract.constructs_comparators is False
    assert contract.constructs_peer_groups is False
    assert contract.exposes_contextual_measurements is False
    assert contract.exposes_formulas is False
    assert contract.performs_scientific_interpretation is False
    assert contract.creates_candidates is False
    assert contract.runs_validation is False
    assert contract.makes_production_decisions is False
    assert contract.exposes_ml_inputs is False


def test_result_boundary_flags_remain_false_for_all_fixtures():
    for fixture in canonical_pit_identity_context_fixtures():
        result = evaluate_pit_identity_context(fixture.record)
        assert result.acquisition_performed is False
        assert result.retrieval_performed is False
        assert result.vendor_integration is False
        assert result.authority_evaluation_performed is False
        assert result.identity_construction is False
        assert result.comparator_construction is False
        assert result.peer_construction is False
        assert result.contextual_measurement is False
        assert result.formula_execution is False
        assert result.scientific_interpretation is False
        assert result.discovery_execution is False
        assert result.validation_execution is False
        assert result.production_logic is False
        assert result.optimization_performed is False
        assert result.ml_integration is False


def test_traceability_contains_identity_context_source_and_frozen_design_fields():
    result = evaluate_pit_identity_context(_fixture_by_id("PIC1_normal_identity").record)
    trace = result.traceability

    assert trace["layer_name"] == "Project Underdog Phase 5 PIT Identity And Context Evidence"
    assert trace["governing_design"] == "project_underdog_phase5_pit_identity_and_context_evidence_implementation_design_v1"
    assert trace["identity_interval_id"] == "identity_interval_PIC1_normal_identity"
    assert trace["context_ids"] == ["context_PIC1_normal_identity"]
    assert trace["source_authority_state"] == AuthorityState.AUTHORITATIVE.value
    assert result.information_contract.traceability == trace


def test_deterministic_repeated_execution_and_serialization():
    record = _fixture_by_id("PIC13_conflicting_association").record
    first = evaluate_pit_identity_context(record)
    second = evaluate_pit_identity_context(record)

    assert first == second
    assert first.stable_json() == second.stable_json()
    assert json.loads(first.stable_json()) == first.to_ordered_dict()


def test_guardrail_manifest_is_synthetic_only_and_disables_prohibited_operations():
    manifest = pit_identity_context_guardrail_manifest()

    assert manifest["synthetic_metadata_only"] is True
    for key, value in manifest.items():
        if key != "synthetic_metadata_only":
            assert value is False


def test_source_authority_compatibility_uses_authority_state_without_reevaluation():
    source_fixture = {fixture.fixture_id: fixture for fixture in canonical_source_authority_fixtures()}["SA1_authoritative"]
    source_result = evaluate_source_authority(source_fixture.record)
    record = _base_record(
        source_authority_state=source_result.authority_state,
        source_authority_trace=source_result.traceability,
    )

    result = evaluate_pit_identity_context(record)
    assert result.applicability_state == ApplicabilityState.APPLICABLE
    assert result.authority_evaluation_performed is False
    assert result.source_authority_trace["source_id"] == "synthetic_source_SA1_authoritative"


def test_first_module_compatibility_preserves_separate_formula_boundary():
    pit_result = evaluate_pit_identity_context(_fixture_by_id("PIC1_normal_identity").record)
    first_fixture = {fixture.fixture_id: fixture for fixture in first_module_fixtures()}["F1_common_repair"]
    first_result = run_first_module_reference(first_fixture.module_input)

    assert pit_result.applicability_state == ApplicabilityState.APPLICABLE
    assert pit_result.formula_execution is False
    assert first_result.target_repair is not None
    assert first_result.peer_common_repair is not None
    assert first_result.idiosyncratic_repair is not None
    assert first_result.candidate_record is False
    assert first_result.panel_record is False
    assert first_result.validation_input is False
    assert first_result.production_output is False
