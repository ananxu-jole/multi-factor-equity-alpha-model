from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from pipelines.project_underdog_first_module_reference_implementation_v1 import (  # noqa: E402
    canonical_fixtures as first_module_fixtures,
    run_first_module_reference,
)
from pipelines.project_underdog_phase5_comparator_construction_reference_implementation_v1 import (  # noqa: E402
    canonical_comparator_construction_fixtures,
    evaluate_comparator_construction,
)
from pipelines.project_underdog_phase5_pit_identity_and_context_evidence_reference_implementation_v1 import (  # noqa: E402
    canonical_pit_identity_context_fixtures,
    evaluate_pit_identity_context,
)
from pipelines.project_underdog_phase5_prepared_observations_reference_implementation_v1 import (  # noqa: E402
    ComparatorAttachment,
    ContextEvidenceAttachment,
    CoverageMetadata,
    InformationRole,
    MissingnessMetadata,
    ObservationInterval,
    PreparedObservationDiagnosticCode,
    PreparedObservationReadinessState,
    PreparedObservationRecord,
    TargetObservationMetadata,
    TemporalAlignmentState,
    _base_record,
    _comparator,
    _context,
    _replace,
    _target,
    _time,
    canonical_prepared_observation_fixtures,
    evaluate_prepared_observation,
    prepared_observations_guardrail_manifest,
)
from pipelines.project_underdog_phase5_source_authority_reference_implementation_v1 import (  # noqa: E402
    canonical_source_authority_fixtures,
    evaluate_source_authority,
)


def _fixture_by_id(fixture_id: str):
    return {fixture.fixture_id: fixture for fixture in canonical_prepared_observation_fixtures()}[fixture_id]


def _diagnostic_codes(result):
    return tuple(diag.code for diag in result.diagnostics)


def test_all_canonical_prepared_observation_fixtures_match_expected_contracts():
    fixtures = canonical_prepared_observation_fixtures()

    assert len(fixtures) == 35
    assert len({fixture.fixture_id for fixture in fixtures}) == 35

    for fixture in fixtures:
        result = evaluate_prepared_observation(fixture.record)
        assert result.readiness_state == fixture.expected_readiness_state
        assert result.temporal_alignment_state == fixture.expected_temporal_alignment_state
        for expected_code in fixture.expected_diagnostic_codes:
            assert expected_code in _diagnostic_codes(result)
        for expected_limitation in fixture.expected_limitations:
            assert expected_limitation in result.limitations


def test_only_approved_readiness_states_are_present():
    assert {state.value for state in PreparedObservationReadinessState} == {
        "PREPARED_OBSERVATION_STRUCTURALLY_READY",
        "PREPARED_OBSERVATION_CONDITIONALLY_READY",
        "PREPARED_OBSERVATION_UNRESOLVED",
        "PREPARED_OBSERVATION_STRUCTURALLY_INCOMPLETE",
        "PREPARED_OBSERVATION_EXCLUDED",
        "INSUFFICIENT_PREPARED_OBSERVATION_EVIDENCE",
    }


def test_package_registration_preserves_target_context_and_comparator_metadata():
    result = evaluate_prepared_observation(_fixture_by_id("PO1_ready").record)

    assert result.package_id == "prepared_package_PO1_ready"
    assert result.target_observation.target_identity_id == "synthetic_target"
    assert result.context_attachments[0].context_id == "context_PO1_ready"
    assert result.comparator_attachments[0].relationship_id == "relationship_PO1_ready"
    assert result.readiness_state == PreparedObservationReadinessState.STRUCTURALLY_READY


def test_prepared_observation_invariant_requires_exactly_one_target_interval():
    missing = evaluate_prepared_observation(_fixture_by_id("PO7_missing_target").record)
    multiple_target = evaluate_prepared_observation(
        _replace(
            _base_record("PO_multiple_target"),
            target_observation=_target(
                "PO_multiple_target",
                interval_ids=("target_interval_PO_multiple_target", "extra_target_interval"),
            ),
        )
    )

    assert PreparedObservationDiagnosticCode.MISSING_TARGET_APPLICABILITY in _diagnostic_codes(missing)
    assert PreparedObservationDiagnosticCode.MISSING_TARGET_APPLICABILITY in _diagnostic_codes(multiple_target)
    assert missing.readiness_state == PreparedObservationReadinessState.STRUCTURALLY_INCOMPLETE
    assert multiple_target.readiness_state == PreparedObservationReadinessState.STRUCTURALLY_INCOMPLETE


def test_observation_time_and_interval_validation_never_uses_package_construction_time_as_fallback():
    missing_time = evaluate_prepared_observation(_fixture_by_id("PO8_missing_time").record)
    invalid_interval = evaluate_prepared_observation(_fixture_by_id("PO9_invalid_interval").record)
    open_interval = evaluate_prepared_observation(
        _replace(
            _base_record("PO_open_interval"),
            observation_time=_time(interval=ObservationInterval("open_observation_interval", 5, None, open_interval=True)),
        )
    )

    assert PreparedObservationDiagnosticCode.MISSING_OBSERVATION_TIME in _diagnostic_codes(missing_time)
    assert missing_time.observation_time.package_construction_time == "synthetic_package_construction_v1"
    assert missing_time.readiness_state == PreparedObservationReadinessState.STRUCTURALLY_INCOMPLETE
    assert PreparedObservationDiagnosticCode.INVALID_OBSERVATION_INTERVAL in _diagnostic_codes(invalid_interval)
    assert open_interval.readiness_state == PreparedObservationReadinessState.CONDITIONALLY_READY
    assert "open observation interval" in open_interval.limitations


def test_required_traces_and_inherited_fatal_diagnostics_fail_closed():
    missing_source = evaluate_prepared_observation(_fixture_by_id("PO10_missing_source_trace").record)
    missing_pit = evaluate_prepared_observation(_fixture_by_id("PO11_missing_pit_trace").record)
    missing_comparator = evaluate_prepared_observation(_fixture_by_id("PO12_missing_comparator_trace").record)
    inherited_source = evaluate_prepared_observation(_fixture_by_id("PO13_inherited_source_fatal").record)
    inherited_pit = evaluate_prepared_observation(_fixture_by_id("PO14_inherited_pit_fatal").record)
    inherited_comparator = evaluate_prepared_observation(_fixture_by_id("PO15_inherited_comparator_fatal").record)

    assert PreparedObservationDiagnosticCode.MISSING_SOURCE_AUTHORITY_TRACE in _diagnostic_codes(missing_source)
    assert PreparedObservationDiagnosticCode.MISSING_PIT_TRACE in _diagnostic_codes(missing_pit)
    assert PreparedObservationDiagnosticCode.MISSING_COMPARATOR_TRACE in _diagnostic_codes(missing_comparator)
    for result in (inherited_source, inherited_pit, inherited_comparator):
        assert PreparedObservationDiagnosticCode.INHERITED_FATAL_UPSTREAM_DIAGNOSTIC in _diagnostic_codes(result)
        assert result.readiness_state == PreparedObservationReadinessState.STRUCTURALLY_INCOMPLETE


def test_temporal_alignment_states_are_metadata_only_and_fail_closed_when_required():
    partial = evaluate_prepared_observation(_fixture_by_id("PO17_partial_alignment").record)
    non_overlap = evaluate_prepared_observation(_fixture_by_id("PO18_temporal_non_overlap").record)
    unknown = evaluate_prepared_observation(_fixture_by_id("PO19_unknown_alignment").record)
    mixed = evaluate_prepared_observation(
        _replace(_base_record("PO_mixed_frequency"), temporal_alignment_state=TemporalAlignmentState.MIXED_FREQUENCY)
    )

    assert partial.temporal_alignment_state == TemporalAlignmentState.PARTIALLY_ALIGNED
    assert "partial temporal alignment" in partial.limitations
    assert non_overlap.readiness_state == PreparedObservationReadinessState.STRUCTURALLY_INCOMPLETE
    assert PreparedObservationDiagnosticCode.NON_OVERLAPPING_TEMPORAL_APPLICABILITY in _diagnostic_codes(non_overlap)
    assert unknown.readiness_state == PreparedObservationReadinessState.UNRESOLVED
    assert PreparedObservationDiagnosticCode.UNRESOLVED_TEMPORAL_ALIGNMENT in _diagnostic_codes(unknown)
    assert mixed.readiness_state == PreparedObservationReadinessState.CONDITIONALLY_READY
    assert "mixed observation frequency" in mixed.limitations


def test_information_roles_are_preserved_and_prohibited_conversion_fails_closed():
    ready = evaluate_prepared_observation(_fixture_by_id("PO1_ready").record)
    undeclared = evaluate_prepared_observation(_fixture_by_id("PO25_undeclared_role").record)
    unsupported = evaluate_prepared_observation(_fixture_by_id("PO26_unsupported_role").record)
    prohibited = evaluate_prepared_observation(_fixture_by_id("PO27_prohibited_role_conversion").record)

    roles = {entry["information_role"] for entry in ready.information_contract.information_role_metadata}
    assert InformationRole.CONTEXTUAL_CONTROL_INFORMATION.value in roles
    assert InformationRole.COMPARATOR_OR_BENCHMARK_INFORMATION.value in roles
    assert PreparedObservationDiagnosticCode.UNDECLARED_INFORMATION_ROLE in _diagnostic_codes(undeclared)
    assert PreparedObservationDiagnosticCode.UNSUPPORTED_INFORMATION_ROLE in _diagnostic_codes(unsupported)
    assert PreparedObservationDiagnosticCode.PROHIBITED_INFORMATION_ROLE_USE in _diagnostic_codes(prohibited)
    assert prohibited.readiness_state == PreparedObservationReadinessState.EXCLUDED


def test_context_and_comparator_attachment_conflicts_are_visible():
    context_conflict = evaluate_prepared_observation(
        _replace(
            _base_record("PO_context_conflict"),
            context_attachments=(
                ContextEvidenceAttachment(
                    context_id="context_conflict",
                    identity_applicability_interval_id="different_interval",
                    context_applicability_interval_id="context_interval_conflict",
                    information_role=InformationRole.CONTEXTUAL_CONTROL_INFORMATION.value,
                    trace={"fixture_id": "PIC_context_conflict"},
                ),
            ),
        )
    )
    comparator_conflict = evaluate_prepared_observation(
        _replace(_base_record("PO_comparator_conflict"), comparator_attachments=(_comparator("PO_comparator_conflict", conflicting=True),))
    )

    assert PreparedObservationDiagnosticCode.CONFLICTING_EVIDENCE_ATTACHMENT in _diagnostic_codes(context_conflict)
    assert PreparedObservationDiagnosticCode.CONFLICTING_EVIDENCE_ATTACHMENT in _diagnostic_codes(comparator_conflict)
    assert context_conflict.readiness_state == PreparedObservationReadinessState.STRUCTURALLY_INCOMPLETE
    assert comparator_conflict.readiness_state == PreparedObservationReadinessState.STRUCTURALLY_INCOMPLETE


def test_required_and_optional_missingness_and_coverage_behavior():
    insufficient = evaluate_prepared_observation(_fixture_by_id("PO22_insufficient_coverage").record)
    required_missing = evaluate_prepared_observation(_fixture_by_id("PO23_required_missingness").record)
    optional_missing = evaluate_prepared_observation(_fixture_by_id("PO24_optional_missingness").record)
    unavailable = evaluate_prepared_observation(
        _replace(_base_record("PO_unavailable"), missingness=MissingnessMetadata(unavailable_evidence=True))
    )
    conditional_coverage = evaluate_prepared_observation(
        _replace(_base_record("PO_conditional_coverage"), coverage=CoverageMetadata(conditionally_governed=True))
    )

    assert insufficient.readiness_state == PreparedObservationReadinessState.INSUFFICIENT_EVIDENCE
    assert required_missing.readiness_state == PreparedObservationReadinessState.STRUCTURALLY_INCOMPLETE
    assert optional_missing.readiness_state == PreparedObservationReadinessState.CONDITIONALLY_READY
    assert unavailable.readiness_state == PreparedObservationReadinessState.INSUFFICIENT_EVIDENCE
    assert conditional_coverage.readiness_state == PreparedObservationReadinessState.CONDITIONALLY_READY
    assert "coverage conditionally governed" in conditional_coverage.limitations


def test_duplicate_and_supersession_handling_preserves_diagnostics_and_limitations():
    duplicate_package = evaluate_prepared_observation(_fixture_by_id("PO28_duplicate_package").record)
    duplicate_context = evaluate_prepared_observation(_fixture_by_id("PO29_duplicate_context").record)
    duplicate_comparator = evaluate_prepared_observation(_fixture_by_id("PO30_duplicate_comparator").record)
    superseded_context = evaluate_prepared_observation(_fixture_by_id("PO31_superseded_context").record)
    superseded_comparator = evaluate_prepared_observation(_fixture_by_id("PO32_superseded_comparator").record)
    superseded_package = evaluate_prepared_observation(_fixture_by_id("PO33_superseded_package").record)

    assert duplicate_package.readiness_state == PreparedObservationReadinessState.EXCLUDED
    assert PreparedObservationDiagnosticCode.DUPLICATE_OBSERVATION_EXPOSURE in _diagnostic_codes(duplicate_context)
    assert PreparedObservationDiagnosticCode.DUPLICATE_OBSERVATION_EXPOSURE in _diagnostic_codes(duplicate_comparator)
    assert "superseded context evidence" in superseded_context.limitations
    assert "superseded comparator relationship" in superseded_comparator.limitations
    assert superseded_package.readiness_state == PreparedObservationReadinessState.EXCLUDED
    assert PreparedObservationDiagnosticCode.SUPERSEDED_OBSERVATION_PACKAGE in _diagnostic_codes(superseded_package)


def test_decision_precedence_preserves_later_diagnostics_without_conditional_masking():
    source_fatal = _replace(
        _base_record("PO_fatal_plus_complete"),
        source_authority_trace={"fixture_id": "SA_fatal", "fatal_diagnostics": ["TRACEABILITY_INCOMPLETE"]},
    )
    prohibited_full = _replace(
        _base_record("PO_prohibited_full_coverage"),
        prohibited_role_conversion=True,
        coverage=CoverageMetadata(),
    )
    missing_time_duplicate = _replace(_base_record("PO_missing_time_duplicate"), observation_time=_time(None), duplicate_package=True)
    non_overlap_conditional = _replace(
        _base_record("PO_non_overlap_conditional"),
        temporal_alignment_state=TemporalAlignmentState.NON_OVERLAPPING,
        coverage=CoverageMetadata(conditionally_governed=True),
    )
    missing_pit_and_comparator = _replace(
        _base_record("PO_missing_pit_and_comparator"),
        pit_trace={},
        comparator_attachments=(_comparator("PO_missing_pit_and_comparator", required=True, trace=None),),
    )
    conflicting_incomplete = _replace(_base_record("PO_conflicting_incomplete"), conflicting_attachment=True, incomplete_traceability=True)
    superseded_otherwise_ready = _replace(
        _base_record("PO_superseded_otherwise_ready"),
        comparator_attachments=(_comparator("PO_superseded_otherwise_ready", superseded=True),),
    )
    optional_context_fatal = _replace(
        _base_record("PO_optional_context_fatal"),
        missingness=MissingnessMetadata(optional_field_missing=True),
        pit_trace={"fixture_id": "PIC_fatal", "fatal_diagnostics": ["TRACEABILITY_INCOMPLETE"]},
    )
    raw_undeclared = _replace(
        _base_record("PO_raw_undeclared"),
        raw_evidence_bypass=True,
        context_attachments=(_context("PO_raw_undeclared", information_role=""),),
    )
    duplicate_non_overlap = _replace(
        _base_record("PO_duplicate_non_overlap"),
        temporal_alignment_state=TemporalAlignmentState.NON_OVERLAPPING,
        comparator_attachments=(_comparator("PO_duplicate_non_overlap", duplicate=True),),
    )

    cases = (
        (source_fatal, PreparedObservationReadinessState.STRUCTURALLY_INCOMPLETE, (PreparedObservationDiagnosticCode.INHERITED_FATAL_UPSTREAM_DIAGNOSTIC,)),
        (prohibited_full, PreparedObservationReadinessState.EXCLUDED, (PreparedObservationDiagnosticCode.PROHIBITED_INFORMATION_ROLE_USE,)),
        (missing_time_duplicate, PreparedObservationReadinessState.EXCLUDED, (PreparedObservationDiagnosticCode.MISSING_OBSERVATION_TIME, PreparedObservationDiagnosticCode.DUPLICATE_OBSERVATION_EXPOSURE)),
        (non_overlap_conditional, PreparedObservationReadinessState.STRUCTURALLY_INCOMPLETE, (PreparedObservationDiagnosticCode.NON_OVERLAPPING_TEMPORAL_APPLICABILITY,)),
        (missing_pit_and_comparator, PreparedObservationReadinessState.STRUCTURALLY_INCOMPLETE, (PreparedObservationDiagnosticCode.MISSING_PIT_TRACE, PreparedObservationDiagnosticCode.MISSING_COMPARATOR_TRACE)),
        (conflicting_incomplete, PreparedObservationReadinessState.STRUCTURALLY_INCOMPLETE, (PreparedObservationDiagnosticCode.CONFLICTING_EVIDENCE_ATTACHMENT, PreparedObservationDiagnosticCode.INCOMPLETE_OBSERVATION_TRACEABILITY)),
        (superseded_otherwise_ready, PreparedObservationReadinessState.CONDITIONALLY_READY, ()),
        (optional_context_fatal, PreparedObservationReadinessState.STRUCTURALLY_INCOMPLETE, (PreparedObservationDiagnosticCode.INHERITED_FATAL_UPSTREAM_DIAGNOSTIC,)),
        (raw_undeclared, PreparedObservationReadinessState.STRUCTURALLY_INCOMPLETE, (PreparedObservationDiagnosticCode.RAW_EVIDENCE_ATTACHMENT_PROHIBITED, PreparedObservationDiagnosticCode.UNDECLARED_INFORMATION_ROLE)),
        (duplicate_non_overlap, PreparedObservationReadinessState.STRUCTURALLY_INCOMPLETE, (PreparedObservationDiagnosticCode.DUPLICATE_OBSERVATION_EXPOSURE, PreparedObservationDiagnosticCode.NON_OVERLAPPING_TEMPORAL_APPLICABILITY)),
    )

    for record, expected_state, expected_codes in cases:
        result = evaluate_prepared_observation(record)
        assert result.readiness_state == expected_state
        for expected_code in expected_codes:
            assert expected_code in _diagnostic_codes(result)


def test_diagnostic_ordering_is_stable_for_combined_failure_case():
    result = evaluate_prepared_observation(
        _replace(_base_record("PO_order"), observation_time=_time(None), duplicate_package=True)
    )

    assert _diagnostic_codes(result) == (
        PreparedObservationDiagnosticCode.MISSING_OBSERVATION_TIME,
        PreparedObservationDiagnosticCode.DUPLICATE_OBSERVATION_EXPOSURE,
    )


def test_information_contract_refuses_prohibited_outputs():
    contract = evaluate_prepared_observation(_fixture_by_id("PO1_ready").record).information_contract

    assert contract.exposes_retrieval is False
    assert contract.exposes_raw_vendor_access is False
    assert contract.performs_authority_evaluation is False
    assert contract.performs_identity_construction is False
    assert contract.performs_identity_resolution is False
    assert contract.performs_comparator_construction is False
    assert contract.performs_peer_discovery is False
    assert contract.exposes_scientific_similarity is False
    assert contract.performs_value_transformation is False
    assert contract.performs_normalization is False
    assert contract.performs_ranking is False
    assert contract.performs_winsorization is False
    assert contract.performs_imputation is False
    assert contract.performs_resampling is False
    assert contract.exposes_formulas is False
    assert contract.creates_signals is False
    assert contract.creates_factors is False
    assert contract.creates_candidates is False
    assert contract.constructs_panels is False
    assert contract.computes_ic is False
    assert contract.runs_statistical_testing is False
    assert contract.runs_validation is False
    assert contract.constructs_portfolios is False
    assert contract.performs_optimization is False
    assert contract.makes_production_decisions is False
    assert contract.exposes_ml_features is False
    assert contract.exposes_ml_labels is False
    assert contract.trains_models is False


def test_result_boundary_flags_remain_false_for_all_fixtures():
    for fixture in canonical_prepared_observation_fixtures():
        result = evaluate_prepared_observation(fixture.record)
        assert result.acquisition_performed is False
        assert result.retrieval_performed is False
        assert result.vendor_integration is False
        assert result.authority_evaluation_performed is False
        assert result.identity_construction is False
        assert result.identity_resolution is False
        assert result.comparator_construction is False
        assert result.peer_discovery is False
        assert result.scientific_similarity is False
        assert result.contextual_interpretation is False
        assert result.value_transformation is False
        assert result.normalization is False
        assert result.ranking is False
        assert result.winsorization is False
        assert result.imputation is False
        assert result.resampling is False
        assert result.formula_execution is False
        assert result.signal_construction is False
        assert result.factor_construction is False
        assert result.candidate_generation is False
        assert result.panel_generation is False
        assert result.discovery_execution is False
        assert result.ic_computation is False
        assert result.validation_execution is False
        assert result.portfolio_construction is False
        assert result.optimization_performed is False
        assert result.production_logic is False
        assert result.ml_integration is False


def test_upstream_source_pit_and_comparator_traces_are_propagated_without_recomputation():
    source_result = evaluate_source_authority(
        {fixture.fixture_id: fixture for fixture in canonical_source_authority_fixtures()}["SA1_authoritative"].record
    )
    pit_result = evaluate_pit_identity_context(
        {fixture.fixture_id: fixture for fixture in canonical_pit_identity_context_fixtures()}["PIC1_normal_identity"].record
    )
    comparator_result = evaluate_comparator_construction(
        {fixture.fixture_id: fixture for fixture in canonical_comparator_construction_fixtures()}["CC1_eligible"].record
    )
    record = _replace(
        _base_record("PO_upstream_trace"),
        source_authority_trace=source_result.traceability,
        pit_trace=pit_result.traceability,
        comparator_attachments=(
            ComparatorAttachment(
                relationship_id="relationship_PO_upstream_trace",
                comparator_identity_id="synthetic_comparator",
                comparator_applicability_interval_id="comparator_interval_PO_upstream_trace",
                information_role=InformationRole.COMPARATOR_OR_BENCHMARK_INFORMATION.value,
                required=True,
                trace=comparator_result.traceability,
            ),
        ),
        required_comparator_relationship_ids=("relationship_PO_upstream_trace",),
    )
    result = evaluate_prepared_observation(record)

    assert result.source_authority_trace["source_id"] == "synthetic_source_SA1_authoritative"
    assert result.pit_trace["identity_interval_id"] == "identity_interval_PIC1_normal_identity"
    assert result.comparator_traces[0]["relationship_id"] == "relationship_CC1_eligible"
    assert result.authority_evaluation_performed is False
    assert result.identity_construction is False
    assert result.comparator_construction is False


def test_artifact_lineage_reconstructs_upstream_and_package_metadata():
    result = evaluate_prepared_observation(_fixture_by_id("PO1_ready").record)
    lineage = result.artifact_lineage.to_dict()

    assert lineage["prepared_observation_artifact"] == "prepared_observation_artifact_prepared_package_PO1_ready"
    assert lineage["source_authority_artifacts"]
    assert lineage["pit_identity_context_artifacts"]
    assert lineage["comparator_construction_artifacts"]
    assert result.information_contract.artifact_lineage_metadata == lineage


def test_deterministic_repeated_execution_and_serialization():
    record = _replace(_base_record("PO_deterministic"), temporal_alignment_state=TemporalAlignmentState.NON_OVERLAPPING)
    first = evaluate_prepared_observation(record)
    second = evaluate_prepared_observation(record)

    assert first == second
    assert first.stable_json() == second.stable_json()
    assert json.loads(first.stable_json()) == first.to_ordered_dict()


def test_guardrail_manifest_is_synthetic_only_and_disables_prohibited_operations():
    manifest = prepared_observations_guardrail_manifest()

    assert manifest["synthetic_metadata_only"] is True
    for key, value in manifest.items():
        if key != "synthetic_metadata_only":
            assert value is False


def test_source_pit_comparator_and_first_module_compatibility_without_retrofit():
    source_result = evaluate_source_authority(
        {fixture.fixture_id: fixture for fixture in canonical_source_authority_fixtures()}["SA1_authoritative"].record
    )
    pit_result = evaluate_pit_identity_context(
        {fixture.fixture_id: fixture for fixture in canonical_pit_identity_context_fixtures()}["PIC1_normal_identity"].record
    )
    comparator_result = evaluate_comparator_construction(
        {fixture.fixture_id: fixture for fixture in canonical_comparator_construction_fixtures()}["CC1_eligible"].record
    )
    prepared_result = evaluate_prepared_observation(
        _replace(
            _base_record("PO_compatibility"),
            source_authority_trace=source_result.traceability,
            pit_trace=pit_result.traceability,
            comparator_attachments=(_comparator("PO_compatibility", trace=comparator_result.traceability),),
        )
    )
    first_result = run_first_module_reference(
        {fixture.fixture_id: fixture for fixture in first_module_fixtures()}["F1_common_repair"].module_input
    )

    assert prepared_result.readiness_state == PreparedObservationReadinessState.STRUCTURALLY_READY
    assert prepared_result.formula_execution is False
    assert first_result.target_repair is not None
    assert first_result.candidate_record is False
    assert first_result.panel_record is False
    assert first_result.validation_input is False

