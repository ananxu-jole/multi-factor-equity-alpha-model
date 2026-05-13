"""Shared orchestration helpers for modular research pipelines."""

from __future__ import annotations

import time
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

import pandas as pd

from src.alpha.construction import run_04a_alpha_construction
from src.alpha.constructed_wfv import run_04b_alpha_wfv
from src.alpha.stress import run_07_alpha_stress
from src.alpha.survivor_registry import run_08_survivor_freeze
from src.pipeline.registry import get_stage
from src.portfolio.construction import run_09_portfolio_construction
from src.portfolio.dashboard import run_09b_dashboard
from src.scoring.decay import run_03c_signal_decay
from src.scoring.diversity import run_03g_signal_diversity
from src.scoring.health import run_03e_signal_health
from src.scoring.regime_ic import run_03d_regime_ic
from src.scoring.reproducibility import run_03f_signal_reproducibility
from src.scoring.signal_scoring import run_03_signal_scoring


@dataclass(frozen=True)
class StageSpec:
    stage_id: str
    runner: Callable[..., dict[str, object]]


SCORING_STAGE_SPECS = [
    StageSpec("03_signal_scoring", run_03_signal_scoring),
    StageSpec("03c_signal_decay", run_03c_signal_decay),
    StageSpec("03d_regime_ic", run_03d_regime_ic),
    StageSpec("03e_signal_health", run_03e_signal_health),
    StageSpec("03f_signal_reproducibility", run_03f_signal_reproducibility),
    StageSpec("03g_signal_diversity", run_03g_signal_diversity),
]

ALPHA_STAGE_SPECS = [
    StageSpec("04a_alpha_construction", run_04a_alpha_construction),
    StageSpec("04b_alpha_wfv", run_04b_alpha_wfv),
    StageSpec("07_alpha_stress", run_07_alpha_stress),
    StageSpec("08_survivor_freeze", run_08_survivor_freeze),
    StageSpec("09_portfolio_construction", run_09_portfolio_construction),
    StageSpec("09b_dashboard", run_09b_dashboard),
]

FULL_STAGE_SPECS = SCORING_STAGE_SPECS + ALPHA_STAGE_SPECS


def metric_value(summary: pd.DataFrame | object, metric: str) -> object | None:
    if not isinstance(summary, pd.DataFrame) or summary.empty:
        return None
    if not {"metric", "value"}.issubset(summary.columns):
        return None
    matched = summary.loc[summary["metric"].eq(metric), "value"]
    return matched.iloc[0] if not matched.empty else None


def _is_frame(value: object) -> bool:
    return isinstance(value, pd.DataFrame)


def _row_counts(result: dict[str, object]) -> dict[str, int]:
    preferred = [
        "scores",
        "score_summary",
        "scoring_gate",
        "best_horizon_summary",
        "decay_summary",
        "regime_summary",
        "regime_opportunity_summary",
        "signal_health_score",
        "reproducibility_gate",
        "signal_diversity_selection",
        "alpha_construction_quality",
        "alpha_wfv_gate",
        "stress_gate",
        "survivor_registry",
        "pre_ml_alpha_inputs",
        "portfolio_alpha_pool",
        "portfolio_performance_summary",
        "validation_report",
        "dashboard_summary",
    ]
    counts: dict[str, int] = {}
    for key in preferred:
        value = result.get(key)
        if _is_frame(value):
            counts[key] = len(value)
    if not counts:
        for key, value in result.items():
            if _is_frame(value) and key != "summary":
                counts[key] = len(value)
            if len(counts) >= 5:
                break
    return counts


def _status_counts(result: dict[str, object]) -> dict[str, dict[object, int]]:
    counts: dict[str, dict[object, int]] = {}
    for key, value in result.items():
        if not _is_frame(value) or value.empty:
            continue
        for column in ("status", "health_status", "decay_status", "decay_risk_flag", "promotion_decision_final"):
            if column in value.columns:
                counts[f"{key}.{column}"] = (
                    value[column].value_counts(dropna=False).sort_index().astype(int).to_dict()
                )
                break
        if len(counts) >= 3:
            break
    return counts


def compact_stage_summary(stage_id: str, result: dict[str, object], elapsed_seconds: float) -> dict[str, object]:
    validation = result.get("validation_report")
    validation_passed = bool(validation["passed"].all()) if _is_frame(validation) and "passed" in validation.columns else True
    return {
        "stage_id": stage_id,
        "elapsed_seconds": round(elapsed_seconds, 3),
        "row_counts": _row_counts(result),
        "status_counts": _status_counts(result),
        "validation_passed": validation_passed,
    }


def print_stage_summary(summary: dict[str, object]) -> None:
    print(f"stage_id: {summary['stage_id']}")
    print(f"  elapsed_seconds: {summary['elapsed_seconds']}")
    print(f"  row_counts: {summary['row_counts']}")
    print(f"  status_counts: {summary['status_counts']}")
    print(f"  validation_passed: {summary['validation_passed']}")


def describe_pipeline(name: str, stages: list[StageSpec]) -> None:
    print(f"pipeline: {name}")
    print("stages:")
    for spec in stages:
        stage = get_stage(spec.stage_id)
        print(f"  - {stage.stage_id}: {stage.current_module}.{stage.current_function}")


def run_stage_specs(
    stages: list[StageSpec],
    *,
    db_path: str | Path | None,
    write: bool,
    verbose: bool,
) -> dict[str, object]:
    results: dict[str, dict[str, object]] = {}
    stage_summaries: list[dict[str, object]] = []
    started = time.perf_counter()

    for spec in stages:
        stage_start = time.perf_counter()
        try:
            result = spec.runner(db_path=db_path, write=write, verbose=verbose)
        except Exception as exc:
            elapsed = time.perf_counter() - stage_start
            print(f"stage_failed: {spec.stage_id}")
            print(f"  elapsed_seconds: {elapsed:.3f}")
            print(f"  error: {type(exc).__name__}: {exc}")
            raise
        elapsed = time.perf_counter() - stage_start
        results[spec.stage_id] = result
        summary = compact_stage_summary(spec.stage_id, result, elapsed)
        stage_summaries.append(summary)
        print_stage_summary(summary)

    validation = validate_stage_results(results)
    total_elapsed = time.perf_counter() - started
    dominant = max(stage_summaries, key=lambda item: float(item["elapsed_seconds"])) if stage_summaries else None
    output = {
        "results": results,
        "stage_summaries": stage_summaries,
        "validation": validation,
        "validation_passed": bool(validation["passed"].all()) if not validation.empty else True,
        "total_elapsed_seconds": total_elapsed,
        "dominant_stage": dominant,
    }
    print("pipeline_validation:")
    print(validation.to_string(index=False))
    print(f"final_validation_status: {output['validation_passed']}")
    print(f"total_elapsed_seconds: {total_elapsed:.3f}")
    if dominant is not None:
        print(f"dominant_stage: {dominant['stage_id']} ({dominant['elapsed_seconds']}s)")
    return output


def _non_empty(result: dict[str, object], key: str) -> bool:
    value = result.get(key)
    return _is_frame(value) and not value.empty


def _validation_record(check_name: str, passed: bool, details: str = "") -> dict[str, object]:
    return {"check_name": check_name, "passed": bool(passed), "details": details}


def validate_scoring_stack_results(results: dict[str, dict[str, object]]) -> pd.DataFrame:
    scoring = results.get("03_signal_scoring", {})
    decay = results.get("03c_signal_decay", {})
    regime = results.get("03d_regime_ic", {})
    health = results.get("03e_signal_health", {})
    reproducibility = results.get("03f_signal_reproducibility", {})
    diversity = results.get("03g_signal_diversity", {})
    records = [
        _validation_record("signal_scores_non_empty", _non_empty(scoring, "scores"), f"rows={len(scoring.get('scores', []))}"),
        _validation_record(
            "signal_best_horizon_count_gt_0",
            _non_empty(scoring, "best_horizon_summary"),
            f"rows={len(scoring.get('best_horizon_summary', []))}",
        ),
        _validation_record("decay_summary_non_empty", _non_empty(decay, "decay_summary"), f"rows={len(decay.get('decay_summary', []))}"),
        _validation_record("regime_ic_summary_non_empty", _non_empty(regime, "regime_summary"), f"rows={len(regime.get('regime_summary', []))}"),
        _validation_record("health_score_non_empty", _non_empty(health, "signal_health_score"), f"rows={len(health.get('signal_health_score', []))}"),
        _validation_record("reproducibility_gate_non_empty", _non_empty(reproducibility, "reproducibility_gate"), f"rows={len(reproducibility.get('reproducibility_gate', []))}"),
        _validation_record("diversity_selection_non_empty", _non_empty(diversity, "signal_diversity_selection"), f"rows={len(diversity.get('signal_diversity_selection', []))}"),
    ]
    return pd.DataFrame(records)


def validate_alpha_pipeline_results(results: dict[str, dict[str, object]]) -> pd.DataFrame:
    construction = results.get("04a_alpha_construction", {})
    wfv = results.get("04b_alpha_wfv", {})
    stress = results.get("07_alpha_stress", {})
    survivor = results.get("08_survivor_freeze", {})
    portfolio = results.get("09_portfolio_construction", {})
    dashboard = results.get("09b_dashboard", {})

    construction_quality = construction.get("alpha_construction_quality")
    approved_alpha_count = 0
    if _is_frame(construction_quality) and "status" in construction_quality.columns:
        approved_alpha_count = int(construction_quality["status"].astype(str).str.contains("APPROVED", na=False).sum())

    wfv_gate = wfv.get("alpha_wfv_gate")
    approved_watchlist_count = 0
    if _is_frame(wfv_gate) and "status" in wfv_gate.columns:
        approved_watchlist_count = int(wfv_gate["status"].isin(["APPROVED_FOR_STRESS", "WATCHLIST"]).sum())
        if approved_watchlist_count == 0:
            approved_watchlist_count = int(wfv_gate["status"].astype(str).str.contains("APPROVED|WATCHLIST", na=False).sum())

    final_core = survivor.get("final_core_registry")
    final_core_names = (
        set(final_core["alpha_name"].dropna())
        if _is_frame(final_core) and "alpha_name" in final_core.columns
        else set()
    )
    portfolio_pool = portfolio.get("portfolio_alpha_pool")
    portfolio_names = (
        set(portfolio_pool["alpha_name"].dropna())
        if _is_frame(portfolio_pool) and "alpha_name" in portfolio_pool.columns
        else set()
    )
    dashboard_validation = dashboard.get("validation_report")
    dashboard_passed = bool(dashboard_validation["passed"].all()) if _is_frame(dashboard_validation) and "passed" in dashboard_validation.columns else False

    records = [
        _validation_record("04a_approved_alpha_validation_count_gt_0", approved_alpha_count > 0, f"count={approved_alpha_count}"),
        _validation_record("04b_approved_or_watchlist_count_gt_0", approved_watchlist_count > 0, f"count={approved_watchlist_count}"),
        _validation_record("07_stress_gate_non_empty", _non_empty(stress, "stress_gate"), f"rows={len(stress.get('stress_gate', []))}"),
        _validation_record("08_final_core_survivor_exists", len(final_core_names) > 0, f"names={sorted(final_core_names)}"),
        _validation_record("09_uses_only_final_core_survivors", portfolio_names == final_core_names and len(portfolio_names) > 0, f"portfolio={sorted(portfolio_names)}; final_core={sorted(final_core_names)}"),
        _validation_record("09b_validation_passed", dashboard_passed, ""),
    ]
    return pd.DataFrame(records)


def validate_stage_results(results: dict[str, dict[str, object]]) -> pd.DataFrame:
    has_scoring = any(stage.stage_id in results for stage in SCORING_STAGE_SPECS)
    has_alpha = any(stage.stage_id in results for stage in ALPHA_STAGE_SPECS)
    frames: list[pd.DataFrame] = []
    if has_scoring:
        frames.append(validate_scoring_stack_results(results))
    if has_alpha:
        frames.append(validate_alpha_pipeline_results(results))
    validation = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame(columns=["check_name", "passed", "details"])
    if has_scoring and has_alpha:
        dashboard = results.get("09b_dashboard", {})
        summary = dashboard.get("summary")
        downstream_alpha_name = metric_value(summary, "final_survivor_alpha_names")
        validation = pd.concat(
            [
                validation,
                pd.DataFrame(
                    [
                        _validation_record(
                            "final_downstream_alpha_name_reported",
                            bool(downstream_alpha_name),
                            str(downstream_alpha_name or ""),
                        )
                    ]
                ),
            ],
            ignore_index=True,
        )
    return validation
