"""Engine entrypoint for 07 Alpha Stress Testing."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.alpha_stress import *  # noqa: F401,F403
from src.alpha_stress import (
    apply_alpha_stress_gate,
    build_alpha_panel,
    build_alpha_stress_audit_summary,
    build_alpha_stress_case_matrix,
    build_alpha_stress_degradation_matrix,
    select_constructed_alpha_stress_candidates,
    stress_alpha_costs,
    stress_alpha_degradation,
    stress_alpha_execution_delay,
    stress_alpha_subperiods,
    stress_alpha_turnover,
    stress_alpha_universe_subsamples,
    summarize_alpha_stress_results,
)
from src.alpha_stress_storage import save_alpha_stress_outputs
from src.db import load_ohlcv_panels, load_table, table_exists
from src.run_config import get_sqlite_db_path, make_run_id, make_run_timestamp


V3_DYNAMIC_ALPHAS = [
    "alpha_hybrid_adaptive_v3",
    "alpha_rolling_ic_dynamic_v3",
    "alpha_regime_blend_dynamic_v3",
    "alpha_decay_aware_dynamic_v3",
]

PRIORITY_ALPHAS = V3_DYNAMIC_ALPHAS + [
    "alpha_persistence_blend_v2",
    "alpha_diversified_research_v2",
    "alpha_health_weighted_research_v1",
    "alpha_equal_weight_research_v1",
    "alpha_smooth_regime_weighted_v2",
]

COST_BPS_LIST = [0, 5, 10, 25]
EXECUTION_DELAYS = [0, 1, 2, 5]
DEGRADATION_MULTIPLIERS = [0.75, 0.50]

REQUIRED_INPUT_TABLES = [
    "alpha_constructed_candidates_current",
    "alpha_construction_quality_current",
    "alpha_construction_diagnostics_current",
    "constructed_alpha_wfv_gate_current",
    "constructed_alpha_wfv_winner_summary_current",
    "regime_overlay_diagnostic_decision_current",
    "clean_close_prices_current",
]


def _log(verbose: bool, message: str) -> None:
    if verbose:
        print(message)


def _require_input_tables(db_path: Path) -> None:
    missing_tables = [
        table_name
        for table_name in REQUIRED_INPUT_TABLES
        if not table_exists(table_name, db_path=db_path)
    ]
    if missing_tables:
        raise ValueError(f"Required alpha stress input tables are missing from {db_path}: {missing_tables}")


def _load_constructed_alpha_stress_inputs(db_path: Path) -> dict[str, pd.DataFrame]:
    return {
        "alpha_long": load_table("alpha_constructed_candidates_current", db_path=db_path),
        "quality": load_table("alpha_construction_quality_current", db_path=db_path),
        "diagnostics": load_table("alpha_construction_diagnostics_current", db_path=db_path),
        "wfv_gate": load_table("constructed_alpha_wfv_gate_current", db_path=db_path),
        "wfv_winner_summary": load_table("constructed_alpha_wfv_winner_summary_current", db_path=db_path),
        "regime_overlay_decision": load_table("regime_overlay_diagnostic_decision_current", db_path=db_path),
    }


def _regime_overlay_current_decision(regime_overlay_decision: pd.DataFrame) -> str:
    if not regime_overlay_decision.empty and "diagnostic_decision" in regime_overlay_decision.columns:
        return regime_overlay_decision["diagnostic_decision"].dropna().astype(str).iloc[-1]
    return "UNKNOWN"


def _validate_regime_overlay_exclusion(
    stress_candidates: pd.DataFrame,
    regime_overlay_current_decision: str,
    db_path: Path,
) -> list[str]:
    if regime_overlay_current_decision != "PARK_OVERLAYS":
        return []
    if stress_candidates.empty or "alpha_name" not in stress_candidates.columns:
        return []
    overlay_names: set[str] = set()
    for table_name in [
        "regime_context_alpha_metadata_current",
        "regime_context_alpha_candidates_current",
    ]:
        if table_exists(table_name, db_path=db_path):
            overlay_table = load_table(table_name, db_path=db_path)
            if "alpha_name" in overlay_table.columns:
                overlay_names.update(overlay_table["alpha_name"].dropna().astype(str))
    leaked_names = sorted(set(stress_candidates["alpha_name"].dropna().astype(str)).intersection(overlay_names))
    if leaked_names:
        raise ValueError(
            "Regime overlay candidates were included while diagnostic decision is PARK_OVERLAYS: "
            f"{leaked_names}"
        )
    return leaked_names


def _build_alpha_panels(
    alpha_long: pd.DataFrame,
    stress_candidates: pd.DataFrame,
) -> dict[str, pd.DataFrame]:
    alpha_panels: dict[str, pd.DataFrame] = {}
    for _, candidate in stress_candidates.iterrows():
        alpha_name = candidate["alpha_name"]
        panel = build_alpha_panel(alpha_long, alpha_name)
        panel.attrs["alpha_name"] = alpha_name
        panel.attrs["avg_turnover_proxy"] = candidate.get("avg_turnover_proxy")
        panel.attrs["turnover_risk_flag"] = candidate.get("turnover_risk_flag")
        alpha_panels[alpha_name] = panel
    return alpha_panels


def _run_stress_scenarios(
    stress_candidates: pd.DataFrame,
    alpha_panels: dict[str, pd.DataFrame],
    close_prices: pd.DataFrame,
) -> pd.DataFrame:
    stress_frames = []
    for _, candidate in stress_candidates.iterrows():
        alpha_name = candidate["alpha_name"]
        horizon = int(candidate["horizon"])
        panel = alpha_panels[alpha_name]
        stress_frames.extend(
            [
                stress_alpha_costs(panel, close_prices, horizon, cost_bps_list=COST_BPS_LIST),
                stress_alpha_execution_delay(panel, close_prices, horizon, delays=EXECUTION_DELAYS),
                stress_alpha_turnover(panel, close_prices, horizon),
                stress_alpha_subperiods(panel, close_prices, horizon),
                stress_alpha_universe_subsamples(panel, close_prices, horizon),
                stress_alpha_degradation(panel, close_prices, horizon, multipliers=DEGRADATION_MULTIPLIERS),
            ]
        )
    return pd.concat(stress_frames, ignore_index=True) if stress_frames else pd.DataFrame()


def _value_counts(df: pd.DataFrame, column: str, output_name: str = "n_alpha_horizons") -> pd.DataFrame:
    if df.empty or column not in df.columns:
        return pd.DataFrame(columns=[column, output_name])
    return df[column].value_counts(dropna=False).rename_axis(column).reset_index(name=output_name)


def _build_validation_report(
    *,
    stress_candidates: pd.DataFrame,
    stress_gate: pd.DataFrame,
    regime_overlay_current_decision: str,
    overlay_leaked_names: list[str],
) -> pd.DataFrame:
    checks = [
        {
            "check_name": "stress_candidate_set_non_empty",
            "passed": not stress_candidates.empty,
            "details": f"Stress candidate rows: {len(stress_candidates)}",
        },
        {
            "check_name": "parked_regime_overlays_excluded",
            "passed": regime_overlay_current_decision != "PARK_OVERLAYS" or not overlay_leaked_names,
            "details": (
                f"decision={regime_overlay_current_decision}; "
                f"overlay_leaked_names={overlay_leaked_names}"
            ),
        },
        {
            "check_name": "stress_gate_non_empty",
            "passed": not stress_gate.empty,
            "details": f"Stress gate rows: {len(stress_gate)}",
        },
        {
            "check_name": "stress_gate_has_decision_columns",
            "passed": {
                "status",
                "survivor_tier",
                "promotion_decision",
                "alpha_role",
            }.issubset(stress_gate.columns),
            "details": f"Columns: {list(stress_gate.columns)}",
        },
    ]
    return pd.DataFrame(checks, columns=["check_name", "passed", "details"])


def _build_summary(
    *,
    run_id: str,
    run_timestamp: str,
    stress_version: str,
    stress_candidates: pd.DataFrame,
    stress_results: pd.DataFrame,
    stress_gate: pd.DataFrame,
    regime_overlay_current_decision: str,
) -> pd.DataFrame:
    candidate_names = (
        sorted(stress_candidates["alpha_name"].dropna().astype(str).unique().tolist())
        if "alpha_name" in stress_candidates.columns
        else []
    )
    approved_count = int(stress_gate["status"].eq("APPROVED_STRESS").sum()) if "status" in stress_gate else 0
    watch_count = int(stress_gate["status"].eq("WATCHLIST_STRESS").sum()) if "status" in stress_gate else 0
    rejected_count = int(stress_gate["status"].eq("REJECTED_STRESS").sum()) if "status" in stress_gate else 0
    return pd.DataFrame(
        [
            {"metric": "run_id", "value": run_id},
            {"metric": "run_timestamp", "value": run_timestamp},
            {"metric": "alpha_stress_version", "value": stress_version},
            {"metric": "stress_candidate_count", "value": len(candidate_names)},
            {"metric": "stress_candidate_names", "value": ", ".join(candidate_names)},
            {"metric": "stress_result_rows", "value": len(stress_results)},
            {"metric": "stress_gate_rows", "value": len(stress_gate)},
            {"metric": "approved_stress_count", "value": approved_count},
            {"metric": "watchlist_stress_count", "value": watch_count},
            {"metric": "rejected_stress_count", "value": rejected_count},
            {"metric": "regime_overlay_diagnostic_decision", "value": regime_overlay_current_decision},
            {"metric": "regime_overlay_candidates_excluded", "value": True},
        ]
    )


def run_07_alpha_stress(
    db_path=None,
    stress_version: str = "phase7_alpha_stress_v1",
    run_id: str | None = None,
    write: bool = True,
    verbose: bool = True,
) -> dict[str, object]:
    """Run the 07 alpha stress notebook core logic as a callable engine."""
    resolved_db_path = Path(db_path) if db_path is not None else get_sqlite_db_path()
    resolved_run_id = run_id or make_run_id(prefix="phase7_constructed_alpha_stress")
    run_timestamp = make_run_timestamp()

    _require_input_tables(resolved_db_path)
    inputs = _load_constructed_alpha_stress_inputs(resolved_db_path)

    stress_candidates = select_constructed_alpha_stress_candidates(
        alpha_quality=inputs["quality"],
        alpha_diagnostics=inputs["diagnostics"],
        constructed_alpha_wfv_gate=inputs["wfv_gate"],
        constructed_alpha_wfv_winner_summary=inputs["wfv_winner_summary"],
        priority_alphas=PRIORITY_ALPHAS,
    )
    regime_overlay_current_decision = _regime_overlay_current_decision(inputs["regime_overlay_decision"])
    overlay_leaked_names = _validate_regime_overlay_exclusion(
        stress_candidates,
        regime_overlay_current_decision,
        resolved_db_path,
    )
    if stress_candidates.empty:
        raise ValueError("No constructed alpha candidates met construction-quality and WFV-status filters.")

    alpha_panels = _build_alpha_panels(inputs["alpha_long"], stress_candidates)
    ohlcv = load_ohlcv_panels(current=True, db_path=resolved_db_path)
    close_prices = ohlcv["close"]

    stress_results = _run_stress_scenarios(stress_candidates, alpha_panels, close_prices)
    stress_summary = summarize_alpha_stress_results(stress_results)
    stress_gate = apply_alpha_stress_gate(stress_summary)
    stress_case_matrix = build_alpha_stress_case_matrix(stress_results)
    stress_degradation_matrix = build_alpha_stress_degradation_matrix(stress_results)
    stress_audit_summary = build_alpha_stress_audit_summary(stress_results, stress_gate)
    validation_report = _build_validation_report(
        stress_candidates=stress_candidates,
        stress_gate=stress_gate,
        regime_overlay_current_decision=regime_overlay_current_decision,
        overlay_leaked_names=overlay_leaked_names,
    )
    if not validation_report["passed"].all():
        failed = validation_report.loc[
            ~validation_report["passed"],
            ["check_name", "details"],
        ].to_dict("records")
        raise ValueError(f"Alpha stress validation failed: {failed}")

    summary = _build_summary(
        run_id=resolved_run_id,
        run_timestamp=run_timestamp,
        stress_version=stress_version,
        stress_candidates=stress_candidates,
        stress_results=stress_results,
        stress_gate=stress_gate,
        regime_overlay_current_decision=regime_overlay_current_decision,
    )

    saved_paths = None
    if write:
        saved_paths = save_alpha_stress_outputs(
            stress_results=stress_results,
            stress_summary=stress_summary,
            stress_gate=stress_gate,
            stress_case_matrix=stress_case_matrix,
            stress_degradation_matrix=stress_degradation_matrix,
            stress_audit_summary=stress_audit_summary,
            db_path=resolved_db_path,
            run_id=resolved_run_id,
            stress_version=stress_version,
        )

    _log(verbose, f"Loaded 07 alpha stress inputs from {resolved_db_path}")
    for input_name, df in inputs.items():
        _log(verbose, f"  {input_name}: {len(df):,} rows x {len(df.columns):,} columns")
    _log(verbose, f"Regime overlay diagnostic decision: {regime_overlay_current_decision}")
    _log(verbose, "07 alpha stress output rows")
    for artifact_name, artifact in [
        ("stress_candidates", stress_candidates),
        ("stress_results", stress_results),
        ("stress_summary", stress_summary),
        ("stress_gate", stress_gate),
        ("stress_case_matrix", stress_case_matrix),
        ("stress_degradation_matrix", stress_degradation_matrix),
        ("stress_audit_summary", stress_audit_summary),
        ("validation_report", validation_report),
    ]:
        _log(verbose, f"  {artifact_name}: {len(artifact):,}")
    for _, row in _value_counts(stress_gate, "status").iterrows():
        _log(verbose, f"  status[{row['status']}]: {row['n_alpha_horizons']}")
    for _, row in _value_counts(stress_gate, "promotion_decision").iterrows():
        _log(verbose, f"  promotion_decision[{row['promotion_decision']}]: {row['n_alpha_horizons']}")
    _log(verbose, f"SQLite write: {'yes' if write else 'no'}")

    return {
        "stress_results": stress_results,
        "stress_gate": stress_gate,
        "stress_summary": stress_summary,
        "stress_scenario_results": stress_results,
        "stress_case_matrix": stress_case_matrix,
        "stress_degradation_matrix": stress_degradation_matrix,
        "stress_audit_summary": stress_audit_summary,
        "validation_report": validation_report,
        "summary": summary,
        "stress_candidates": stress_candidates,
        "alpha_panels": alpha_panels,
        "saved_paths": saved_paths,
        "db_path": resolved_db_path,
        "run_id": resolved_run_id,
        "run_timestamp": run_timestamp,
        "write": write,
    }


__all__ = [name for name in globals() if not name.startswith("_")]
