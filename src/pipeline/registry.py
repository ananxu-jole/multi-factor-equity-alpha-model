"""Static pipeline stage metadata for Project Underdog.

This registry is intentionally data-only. It does not execute notebooks,
mutate SQLite state, or import engine modules.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class StageMetadata:
    stage_id: str
    notebook_path: str
    current_module: str | None
    current_function: str | None
    expected_input_tables: tuple[str, ...]
    expected_output_tables: tuple[str, ...]
    required: bool = True
    diagnostic: bool = False


PIPELINE_STAGES: tuple[StageMetadata, ...] = (
    StageMetadata(
        stage_id="01_data_foundation",
        notebook_path="notebooks/2-Phase 2_Signal Expansion/01_Data Foundation.ipynb",
        current_module="src.db",
        current_function="load_ohlcv_panels",
        expected_input_tables=(),
        expected_output_tables=(
            "clean_open_prices_current",
            "clean_high_prices_current",
            "clean_low_prices_current",
            "clean_close_prices_current",
            "clean_volume_current",
            "benchmark_prices_current",
            "universe_membership_dynamic_top300_current",
            "universe_metadata_current",
        ),
    ),
    StageMetadata(
        stage_id="02_signal_factory",
        notebook_path="notebooks/2-Phase 2_Signal Expansion/02_Signal Factory.ipynb",
        current_module="src.signals",
        current_function="generate_signal_library",
        expected_input_tables=(
            "clean_open_prices_current",
            "clean_high_prices_current",
            "clean_low_prices_current",
            "clean_close_prices_current",
            "clean_volume_current",
        ),
        expected_output_tables=(
            "candidate_signals_current",
            "candidate_signal_metadata_current",
            "candidate_signal_quality_current",
            "candidate_signal_quality_gate_current",
            "candidate_signal_family_summary_current",
        ),
    ),
    StageMetadata(
        stage_id="02c_orthogonal_signal_factory",
        notebook_path="notebooks/2-Phase 2_Signal Expansion/02C_Orthogonal_Signal_Factory.ipynb",
        current_module="src.orthogonal_signals",
        current_function="build_orthogonal_signal_candidates",
        expected_input_tables=(
            "clean_open_prices_current",
            "clean_high_prices_current",
            "clean_low_prices_current",
            "clean_close_prices_current",
            "clean_volume_current",
            "benchmark_prices_current",
        ),
        expected_output_tables=(
            "orthogonal_candidate_signals_current",
            "orthogonal_candidate_metadata_current",
            "orthogonal_candidate_quality_current",
            "orthogonal_signal_integration_report_current",
        ),
    ),
    StageMetadata(
        stage_id="02d_expanded_discovery",
        notebook_path="notebooks/2-Phase 2_Signal Expansion/02D_Expanded_Orthogonal_Discovery.ipynb",
        current_module="src.expanded_discovery",
        current_function="build_expanded_discovery_candidates",
        expected_input_tables=(
            "candidate_signals_current",
            "clean_close_prices_current",
            "clean_volume_current",
            "alpha_candidates_current",
        ),
        expected_output_tables=(
            "expanded_discovery_candidate_signals_current",
            "expanded_discovery_metadata_current",
            "expanded_discovery_quality_current",
            "expanded_discovery_core_corr_current",
            "expanded_discovery_selection_current",
            "expanded_discovery_integration_report_current",
        ),
    ),
    StageMetadata(
        stage_id="03_signal_scoring",
        notebook_path="notebooks/2-Phase 2_Signal Expansion/03_Multi Horizon Signal Scoring.ipynb",
        current_module="src.scoring.signal_scoring",
        current_function="run_03_signal_scoring",
        expected_input_tables=(
            "candidate_signals_current",
            "candidate_signal_quality_gate_current",
            "clean_close_prices_current",
        ),
        expected_output_tables=(
            "signal_scores_current",
            "signal_score_summary_current",
            "signal_scoring_gate_current",
            "signal_best_horizon_current",
            "signal_scoring_family_summary_current",
        ),
    ),
    StageMetadata(
        stage_id="03c_signal_decay",
        notebook_path="notebooks/2-Phase 2_Signal Expansion/03C_Signal Decay Engine.ipynb",
        current_module="src.scoring.decay",
        current_function="run_03c_signal_decay",
        expected_input_tables=(
            "candidate_signals_current",
            "signal_scores_current",
            "signal_best_horizon_current",
            "clean_close_prices_current",
        ),
        expected_output_tables=(
            "signal_decay_curve_current",
            "signal_decay_summary_current",
        ),
    ),
    StageMetadata(
        stage_id="03d_regime_ic",
        notebook_path="notebooks/2-Phase 2_Signal Expansion/03D_Regime Conditioned IC Engine.ipynb",
        current_module="src.scoring.regime_ic",
        current_function="run_03d_regime_ic",
        expected_input_tables=(
            "candidate_signals_current",
            "signal_scores_current",
            "signal_best_horizon_current",
            "clean_close_prices_current",
        ),
        expected_output_tables=(
            "regime_features_ic_current",
            "signal_regime_ic_daily_current",
            "signal_regime_ic_summary_current",
            "signal_regime_fragility_current",
            "signal_regime_opportunity_summary_current",
        ),
    ),
    StageMetadata(
        stage_id="03e_signal_health",
        notebook_path="notebooks/2-Phase 2_Signal Expansion/03E_Signal Health Score.ipynb",
        current_module="src.scoring.health",
        current_function="run_03e_signal_health",
        expected_input_tables=(
            "signal_best_horizon_current",
            "signal_scoring_gate_current",
            "signal_decay_summary_current",
            "signal_regime_opportunity_summary_current",
        ),
        expected_output_tables=(
            "signal_health_score_current",
            "signal_health_summary_current",
            "signal_health_attribution_current",
        ),
    ),
    StageMetadata(
        stage_id="03f_signal_reproducibility",
        notebook_path="notebooks/2-Phase 2_Signal Expansion/03F_Signal Reproducibility Engine.ipynb",
        current_module="src.scoring.reproducibility",
        current_function="run_03f_signal_reproducibility",
        expected_input_tables=(
            "signal_health_score_current",
            "candidate_signals_current",
            "clean_close_prices_current",
        ),
        expected_output_tables=(
            "signal_reproducibility_results_current",
            "signal_reproducibility_summary_current",
            "signal_reproducibility_gate_current",
        ),
    ),
    StageMetadata(
        stage_id="03g_signal_diversity",
        notebook_path="notebooks/2-Phase 2_Signal Expansion/03G_Signal_Diversity_Engine.ipynb",
        current_module="src.scoring.diversity",
        current_function="run_03g_signal_diversity",
        expected_input_tables=(
            "signal_health_score_current",
            "signal_reproducibility_gate_current",
            "candidate_signals_current",
        ),
        expected_output_tables=(
            "signal_diversity_similarity_current",
            "signal_diversity_diagnostics_current",
            "signal_diversity_selection_current",
            "signal_diversity_family_report_current",
            "signal_diversity_cluster_report_current",
        ),
    ),
    StageMetadata(
        stage_id="04a_alpha_construction",
        notebook_path="notebooks/2-Phase 2_Signal Expansion/04A_Alpha_Construction_Engine.ipynb",
        current_module="src.alpha.construction",
        current_function="run_04a_alpha_construction",
        expected_input_tables=(
            "signal_reproducibility_gate_current",
            "signal_health_score_current",
            "signal_decay_summary_current",
            "signal_regime_opportunity_summary_current",
            "signal_diversity_selection_current",
            "candidate_signals_current",
            "clean_close_prices_current",
        ),
        expected_output_tables=(
            "alpha_constructed_candidates_current",
            "alpha_construction_metadata_current",
            "alpha_construction_quality_current",
            "alpha_construction_diagnostics_current",
            "alpha_construction_correlation_current",
            "alpha_signal_pool_current",
            "alpha_dynamic_weight_audit_current",
        ),
    ),
    StageMetadata(
        stage_id="04b_alpha_wfv",
        notebook_path="notebooks/2-Phase 2_Signal Expansion/04B_Alpha_WalkForward_Validation_Engine.ipynb",
        current_module="src.alpha.constructed_wfv",
        current_function="run_04b_alpha_wfv",
        expected_input_tables=(
            "alpha_constructed_candidates_current",
            "alpha_construction_quality_current",
            "clean_close_prices_current",
        ),
        expected_output_tables=(
            "constructed_alpha_wfv_windows_current",
            "constructed_alpha_wfv_window_results_current",
            "constructed_alpha_wfv_summary_current",
            "constructed_alpha_wfv_gate_current",
            "constructed_alpha_wfv_failure_breakdown_current",
            "constructed_alpha_wfv_winner_summary_current",
        ),
    ),
    StageMetadata(
        stage_id="05_regime_overlay_experiment",
        notebook_path="notebooks/2-Phase 2_Signal Expansion/05_DIAG_Regime_Overlay_Experiment.ipynb",
        current_module="src.regime_context_alpha",
        current_function="build_regime_context_alpha_candidates",
        expected_input_tables=(
            "alpha_constructed_candidates_current",
            "alpha_construction_quality_current",
            "regime_features_current",
        ),
        expected_output_tables=(
            "regime_context_alpha_candidates_current",
            "regime_context_alpha_metadata_current",
            "regime_context_alpha_quality_current",
            "regime_context_alpha_diagnostics_current",
            "regime_context_alpha_activation_current",
        ),
        required=False,
        diagnostic=True,
    ),
    StageMetadata(
        stage_id="06_regime_overlay_validation",
        notebook_path="notebooks/2-Phase 2_Signal Expansion/06_DIAG_Regime_Overlay_Validation.ipynb",
        current_module="src.regime_context_alpha_validation",
        current_function="score_regime_context_alpha_library",
        expected_input_tables=(
            "regime_context_alpha_candidates_current",
            "regime_context_alpha_metadata_current",
            "clean_close_prices_current",
        ),
        expected_output_tables=(
            "regime_context_alpha_scores_current",
            "regime_context_alpha_best_horizon_current",
            "regime_context_alpha_wfv_gate_current",
            "regime_overlay_diagnostic_decision_current",
        ),
        required=False,
        diagnostic=True,
    ),
    StageMetadata(
        stage_id="07_alpha_stress",
        notebook_path="notebooks/2-Phase 2_Signal Expansion/07_Alpha Stress Testing.ipynb",
        current_module="src.alpha.stress",
        current_function="run_07_alpha_stress",
        expected_input_tables=(
            "alpha_constructed_candidates_current",
            "alpha_construction_quality_current",
            "alpha_construction_diagnostics_current",
            "constructed_alpha_wfv_gate_current",
            "constructed_alpha_wfv_winner_summary_current",
            "clean_close_prices_current",
            "regime_overlay_diagnostic_decision_current",
        ),
        expected_output_tables=(
            "alpha_stress_results_current",
            "alpha_stress_summary_current",
            "alpha_stress_gate_current",
            "alpha_stress_case_matrix_current",
            "alpha_stress_degradation_matrix_current",
            "alpha_stress_audit_summary_current",
        ),
    ),
    StageMetadata(
        stage_id="08_survivor_freeze",
        notebook_path="notebooks/2-Phase 2_Signal Expansion/08_Survivor Freeze Pre-ML Alpha Library.ipynb",
        current_module="src.alpha.survivor_registry",
        current_function="run_08_survivor_freeze",
        expected_input_tables=(
            "alpha_stress_gate_current",
            "alpha_stress_audit_summary_current",
            "alpha_constructed_candidates_current",
            "alpha_construction_metadata_current",
            "alpha_construction_diagnostics_current",
            "constructed_alpha_wfv_gate_current",
            "constructed_alpha_wfv_winner_summary_current",
        ),
        expected_output_tables=(
            "survivor_alpha_registry_current",
            "pre_ml_alpha_inputs_current",
            "survivor_freeze_report_current",
            "survivor_validation_report_current",
            "survivor_lineage_report_current",
            "survivor_alpha_correlation_current",
            "survivor_cluster_summary_current",
        ),
    ),
    StageMetadata(
        stage_id="09_portfolio_construction",
        notebook_path="notebooks/3-Phase 3_Portfolio Construction/09_Portfolio_Construction_Execution_Layer.ipynb",
        current_module="src.portfolio.construction",
        current_function="run_09_portfolio_construction",
        expected_input_tables=(
            "survivor_alpha_registry_current",
            "pre_ml_alpha_inputs_current",
            "clean_close_prices_current",
            "benchmark_prices_current",
        ),
        expected_output_tables=(
            "portfolio_alpha_pool_current",
            "portfolio_weights_current",
            "portfolio_backtest_results_current",
            "portfolio_performance_summary_current",
        ),
    ),
    StageMetadata(
        stage_id="09b_dashboard",
        notebook_path="notebooks/3-Phase 3_Portfolio Construction/09B_Alpha_System_Dashboard.ipynb",
        current_module="src.portfolio.dashboard",
        current_function="run_09b_dashboard",
        expected_input_tables=(
            "survivor_alpha_registry_current",
            "pre_ml_alpha_inputs_current",
            "portfolio_alpha_pool_current",
            "portfolio_weights_current",
            "portfolio_backtest_results_current",
            "portfolio_performance_summary_current",
        ),
        expected_output_tables=(
            "dashboard_summary_current",
            "dashboard_survivor_summary_current",
            "dashboard_portfolio_summary_current",
            "dashboard_benchmark_summary_current",
            "dashboard_method_comparison_current",
            "dashboard_validation_report_current",
        ),
    ),
)


STAGES_BY_ID: dict[str, StageMetadata] = {stage.stage_id: stage for stage in PIPELINE_STAGES}


def get_stage(stage_id: str) -> StageMetadata:
    """Return metadata for a stage id."""
    try:
        return STAGES_BY_ID[stage_id]
    except KeyError as exc:
        raise KeyError(f"Unknown pipeline stage_id: {stage_id}") from exc


def required_stages() -> tuple[StageMetadata, ...]:
    """Return required core stages, excluding optional diagnostics."""
    return tuple(stage for stage in PIPELINE_STAGES if stage.required)


def diagnostic_stages() -> tuple[StageMetadata, ...]:
    """Return optional diagnostic stages."""
    return tuple(stage for stage in PIPELINE_STAGES if stage.diagnostic)


__all__ = [
    "PIPELINE_STAGES",
    "STAGES_BY_ID",
    "StageMetadata",
    "diagnostic_stages",
    "get_stage",
    "required_stages",
]
