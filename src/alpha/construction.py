"""Engine entrypoint for 04A Alpha Construction."""

from __future__ import annotations

import time
from pathlib import Path

import numpy as np
import pandas as pd

from src.alpha_construction import *  # noqa: F401,F403
from src.alpha_construction import (
    build_alpha_candidates,
    build_alpha_construction_diagnostics,
    build_alpha_construction_metadata,
    build_alpha_construction_quality,
    build_alpha_correlation_matrix,
    build_alpha_signal_pool,
    build_dynamic_universe_eligibility_mask,
    build_normalized_signal_panels,
    get_approved_alpha_research_signals,
    get_watchlist_diversifier_signals,
    load_alpha_construction_inputs,
    load_candidate_signals_for_names,
)
from src.alpha_construction_storage import alpha_candidates_to_long, save_alpha_construction_outputs
from src.db import get_db_path, load_table, table_exists
from src.run_config import make_run_id, make_run_timestamp


SMOOTHING_WINDOW = 10
REBALANCE_FREQUENCY = 5
TURNOVER_CONTROL_ENABLED = True
TURNOVER_CONTROL_UPDATE_RATE = 0.10
WARMUP_TRADING_DAYS = 60

ORTHOGONAL_V2_CANDIDATE_SPECS = [
    ("vol_surprise_20_60", 20),
    ("price_impact_proxy_20", 20),
    ("range_expansion_failure_5", 20),
    ("liquidity_adjusted_reversal_5", 5),
]

REQUIRED_INPUT_TABLES = [
    "signal_reproducibility_gate_current",
    "signal_health_score_current",
    "signal_decay_summary_current",
    "signal_diversity_selection_current",
    "signal_regime_opportunity_summary_current",
    "regime_features_ic_current",
    "candidate_signals_current",
    "clean_close_prices_current",
    "universe_membership_dynamic_top300_current",
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
        raise ValueError(f"Required 04A input tables are missing from {db_path}: {missing_tables}")


def _load_core_inputs(db_path: Path) -> dict[str, pd.DataFrame]:
    return load_alpha_construction_inputs(db_path=db_path, include_candidate_signals=False)


def _needed_signal_names(
    approved_input_signals: pd.DataFrame,
    watchlist_diversifier_signals: pd.DataFrame,
    alpha_signal_pool: pd.DataFrame,
) -> list[str]:
    orthogonal_v2_signal_names = [signal_name for signal_name, _ in ORTHOGONAL_V2_CANDIDATE_SPECS]
    return sorted(
        set(approved_input_signals["signal_name"].dropna().unique().tolist())
        | set(watchlist_diversifier_signals["signal_name"].dropna().unique().tolist())
        | set(alpha_signal_pool["signal_name"].dropna().unique().tolist())
        | set(orthogonal_v2_signal_names)
    )


def _orthogonal_v2_component_metrics(db_path: Path) -> pd.DataFrame:
    orthogonal_v2_daily_ic = (
        load_table("signal_regime_ic_daily_current", db_path=db_path)
        if table_exists("signal_regime_ic_daily_current", db_path=db_path)
        else pd.DataFrame()
    )
    orthogonal_v2_health = (
        load_table("signal_health_score_current", db_path=db_path)
        if table_exists("signal_health_score_current", db_path=db_path)
        else pd.DataFrame()
    )
    component_metrics = pd.DataFrame(
        ORTHOGONAL_V2_CANDIDATE_SPECS,
        columns=["signal_name", "horizon"],
    )
    if not orthogonal_v2_health.empty:
        health_columns = [
            "signal_name",
            "horizon",
            "signal_family",
            "signal_direction",
            "signal_health_score",
            "signal_health_gate",
        ]
        component_metrics = component_metrics.merge(
            orthogonal_v2_health[
                [column for column in health_columns if column in orthogonal_v2_health.columns]
            ],
            on=["signal_name", "horizon"],
            how="left",
        )
    if not orthogonal_v2_daily_ic.empty:
        ic = orthogonal_v2_daily_ic.loc[
            orthogonal_v2_daily_ic.get("regime_column", pd.Series(dtype=object))
            .astype(str)
            .eq("benchmark_vol_regime")
        ].copy()
        ic["Date"] = pd.to_datetime(ic["Date"], errors="coerce")
        ic["horizon"] = pd.to_numeric(ic["horizon"], errors="coerce")
        ic["daily_ic"] = pd.to_numeric(ic["daily_ic"], errors="coerce")
        unique_dates = np.array(sorted(ic["Date"].dropna().unique()))
        date_windows = {
            date: idx + 1
            for idx, dates in enumerate(np.array_split(unique_dates, 4))
            for date in dates
        }
        ic["window_id"] = ic["Date"].map(date_windows)
        ic_summary = (
            ic.groupby(["signal_name", "horizon"])
            .agg(
                mean_ic=("daily_ic", "mean"),
                ic_std=("daily_ic", "std"),
                sign_consistency=("daily_ic", lambda values: float((values > 0).mean())),
            )
            .reset_index()
        )
        ic_summary["ic_ir"] = ic_summary["mean_ic"] / ic_summary["ic_std"].replace(0.0, np.nan)
        ic_windows = (
            ic.groupby(["signal_name", "horizon", "window_id"])
            .agg(window_mean_ic=("daily_ic", "mean"))
            .reset_index()
        )
        ic_windows["positive_window"] = ic_windows["window_mean_ic"].gt(0)
        persistence = (
            ic_windows.groupby(["signal_name", "horizon"])
            .agg(persistence_ratio=("positive_window", "mean"))
            .reset_index()
        )
        component_metrics = (
            component_metrics.merge(ic_summary, on=["signal_name", "horizon"], how="left")
            .merge(persistence, on=["signal_name", "horizon"], how="left")
        )

    component_metrics[["mean_ic", "persistence_ratio", "sign_consistency"]] = component_metrics[
        ["mean_ic", "persistence_ratio", "sign_consistency"]
    ].fillna({"mean_ic": 0.0, "persistence_ratio": 0.50, "sign_consistency": 0.50})
    component_metrics["signal_direction"] = component_metrics.get(
        "signal_direction",
        pd.Series("POSITIVE_EDGE", index=component_metrics.index),
    ).fillna("POSITIVE_EDGE")
    return component_metrics


def _family_summary(alpha_signal_pool: pd.DataFrame, alpha_construction_quality: pd.DataFrame) -> pd.DataFrame:
    pool_summary = (
        alpha_signal_pool.groupby(["source_role", "signal_family"], dropna=False)
        .agg(n_components=("component_id", "nunique"), avg_pool_weight=("pool_weight_base", "mean"))
        .reset_index()
        if not alpha_signal_pool.empty
        else pd.DataFrame(columns=["source_role", "signal_family", "n_components", "avg_pool_weight"])
    )
    status_summary = (
        alpha_construction_quality["status"]
        .value_counts(dropna=False)
        .rename_axis("status")
        .reset_index(name="n_alphas")
        if "status" in alpha_construction_quality.columns
        else pd.DataFrame(columns=["status", "n_alphas"])
    )
    pool_summary["summary_type"] = "signal_pool_family"
    status_summary["summary_type"] = "alpha_construction_status"
    return pd.concat([pool_summary, status_summary], ignore_index=True, sort=False)


def _validation_report(
    *,
    approved_input_signals: pd.DataFrame,
    alpha_signal_pool: pd.DataFrame,
    alpha_candidates: dict[str, pd.DataFrame],
    alpha_construction_quality: pd.DataFrame,
) -> pd.DataFrame:
    approved_count = (
        int(alpha_construction_quality["status"].eq("APPROVED_FOR_ALPHA_VALIDATION").sum())
        if "status" in alpha_construction_quality.columns
        else 0
    )
    checks = [
        {
            "check_name": "eligible_input_signals_non_empty",
            "passed": not approved_input_signals.empty or not alpha_signal_pool.empty,
            "details": f"approved_input_signals={len(approved_input_signals)}, alpha_signal_pool={len(alpha_signal_pool)}",
        },
        {
            "check_name": "constructed_alpha_candidates_non_empty",
            "passed": len(alpha_candidates) > 0,
            "details": f"Constructed alpha panels: {len(alpha_candidates)}",
        },
        {
            "check_name": "gate_table_non_empty",
            "passed": not alpha_construction_quality.empty,
            "details": f"Gate/quality rows: {len(alpha_construction_quality)}",
        },
        {
            "check_name": "approved_for_alpha_validation_exists",
            "passed": approved_count > 0,
            "details": f"APPROVED_FOR_ALPHA_VALIDATION rows: {approved_count}",
        },
    ]
    return pd.DataFrame(checks, columns=["check_name", "passed", "details"])


def _summary(
    *,
    run_id: str,
    run_timestamp: str,
    construction_version: str,
    approved_input_signals: pd.DataFrame,
    watchlist_diversifier_signals: pd.DataFrame,
    alpha_signal_pool: pd.DataFrame,
    candidate_signals_filtered: pd.DataFrame,
    alpha_candidates: dict[str, pd.DataFrame],
    constructed_alpha_candidates: pd.DataFrame,
    alpha_construction_quality: pd.DataFrame,
) -> pd.DataFrame:
    alpha_names = sorted(alpha_candidates.keys())
    approved_count = (
        int(alpha_construction_quality["status"].eq("APPROVED_FOR_ALPHA_VALIDATION").sum())
        if "status" in alpha_construction_quality.columns
        else 0
    )
    rejected_count = (
        int(alpha_construction_quality["status"].eq("REJECTED_ALPHA_CONSTRUCTION").sum())
        if "status" in alpha_construction_quality.columns
        else 0
    )
    return pd.DataFrame(
        [
            {"metric": "run_id", "value": run_id},
            {"metric": "run_timestamp", "value": run_timestamp},
            {"metric": "alpha_construction_version", "value": construction_version},
            {"metric": "approved_input_signal_rows", "value": len(approved_input_signals)},
            {"metric": "watchlist_diversifier_rows", "value": len(watchlist_diversifier_signals)},
            {"metric": "alpha_signal_pool_rows", "value": len(alpha_signal_pool)},
            {"metric": "candidate_signal_rows_loaded", "value": len(candidate_signals_filtered)},
            {"metric": "constructed_alpha_count", "value": len(alpha_names)},
            {"metric": "constructed_alpha_names", "value": ", ".join(alpha_names)},
            {"metric": "constructed_alpha_candidate_rows", "value": len(constructed_alpha_candidates)},
            {"metric": "alpha_construction_quality_rows", "value": len(alpha_construction_quality)},
            {"metric": "approved_for_alpha_validation_count", "value": approved_count},
            {"metric": "rejected_alpha_construction_count", "value": rejected_count},
            {"metric": "smoothing_window", "value": SMOOTHING_WINDOW},
            {"metric": "rebalance_frequency", "value": REBALANCE_FREQUENCY},
            {"metric": "turnover_control_enabled", "value": TURNOVER_CONTROL_ENABLED},
            {"metric": "turnover_control_update_rate", "value": TURNOVER_CONTROL_UPDATE_RATE},
            {"metric": "warmup_trading_days", "value": WARMUP_TRADING_DAYS},
        ]
    )


def run_04a_alpha_construction(
    db_path=None,
    construction_version: str = "phase4a_alpha_construction_v1",
    run_id: str | None = None,
    write: bool = True,
    verbose: bool = True,
) -> dict[str, object]:
    """Run the 04A alpha construction notebook core logic as a callable engine."""
    resolved_db_path = Path(db_path) if db_path is not None else get_db_path()
    resolved_run_id = run_id or make_run_id("phase4a_alpha_construction")
    run_timestamp = make_run_timestamp()

    _require_input_tables(resolved_db_path)
    inputs = _load_core_inputs(resolved_db_path)
    approved_input_signals = get_approved_alpha_research_signals(
        reproducibility_gate=inputs["reproducibility_gate"],
        signal_health=inputs["signal_health"],
        regime_opportunity=inputs["regime_opportunity"],
    )
    watchlist_diversifier_signals = get_watchlist_diversifier_signals(inputs["signal_health"])
    alpha_signal_pool = build_alpha_signal_pool(
        reproducibility_gate=inputs["reproducibility_gate"],
        signal_health=inputs["signal_health"],
        signal_decay=inputs["signal_decay"],
        regime_opportunity=inputs["regime_opportunity"],
        diversity_selection=inputs["diversity_selection"],
        diversity_similarity=inputs["diversity_similarity"],
    )
    if approved_input_signals.empty and alpha_signal_pool.empty:
        raise ValueError("No eligible 04A input signals found.")

    needed_signals = _needed_signal_names(
        approved_input_signals,
        watchlist_diversifier_signals,
        alpha_signal_pool,
    )
    load_started = time.perf_counter()
    candidate_signals_filtered = load_candidate_signals_for_names(needed_signals, db_path=resolved_db_path)
    candidate_signal_load_seconds = time.perf_counter() - load_started
    inputs["candidate_signals"] = candidate_signals_filtered

    build_normalized_signal_panels(
        approved_signals=approved_input_signals,
        candidate_signals=candidate_signals_filtered,
    )

    eligibility_membership = load_table("universe_membership_dynamic_top300_current", db_path=resolved_db_path)
    eligible_mask, warmup_cutoff = build_dynamic_universe_eligibility_mask(
        membership=eligibility_membership,
        close_prices=inputs["close_prices"],
        warmup_trading_days=WARMUP_TRADING_DAYS,
    )
    eligible_mask_for_construction = eligible_mask.reindex(
        index=inputs["close_prices"].index,
        columns=inputs["close_prices"].columns,
        fill_value=False,
    ).astype(bool)

    alpha_candidates, _, alpha_dynamic_weight_audit, dynamic_component_stats = build_alpha_candidates(
        approved_signals=approved_input_signals,
        candidate_signals=candidate_signals_filtered,
        regime_features=inputs["regime_features"],
        watchlist_diversifiers=watchlist_diversifier_signals,
        signal_pool=alpha_signal_pool,
        close_prices=inputs["close_prices"],
        eligible_mask=eligible_mask_for_construction,
        orthogonal_v2_component_metrics=_orthogonal_v2_component_metrics(resolved_db_path),
        smoothing_window=SMOOTHING_WINDOW,
        rebalance_frequency=REBALANCE_FREQUENCY,
        update_rate=TURNOVER_CONTROL_UPDATE_RATE,
        turnover_control_enabled=TURNOVER_CONTROL_ENABLED,
    )
    if not alpha_candidates:
        raise ValueError("No alpha candidates were constructed.")

    reference_panel = next(iter(alpha_candidates.values())) if alpha_candidates else pd.DataFrame()
    eligible_mask_for_alphas = (
        eligible_mask.reindex(
            index=reference_panel.index,
            columns=reference_panel.columns,
            fill_value=False,
        ).astype(bool)
        if not reference_panel.empty
        else eligible_mask
    )

    alpha_construction_metadata = build_alpha_construction_metadata(
        alpha_candidates=alpha_candidates,
        approved_signals=approved_input_signals,
        run_id=resolved_run_id,
        alpha_construction_version=construction_version,
        watchlist_diversifiers=watchlist_diversifier_signals,
        signal_pool=alpha_signal_pool,
        smoothing_window=SMOOTHING_WINDOW,
        rebalance_frequency=REBALANCE_FREQUENCY,
        update_rate=TURNOVER_CONTROL_UPDATE_RATE,
        turnover_control_enabled=TURNOVER_CONTROL_ENABLED,
        dynamic_component_stats=dynamic_component_stats,
    )
    alpha_construction_quality = build_alpha_construction_quality(
        alpha_candidates=alpha_candidates,
        run_id=resolved_run_id,
        alpha_construction_version=construction_version,
        eligible_mask=eligible_mask_for_alphas,
    )
    alpha_construction_diagnostics = build_alpha_construction_diagnostics(
        alpha_panels=alpha_candidates,
        run_id=resolved_run_id,
        alpha_construction_version=construction_version,
        dynamic_component_stats=dynamic_component_stats,
        eligible_mask=eligible_mask_for_alphas,
    )
    alpha_construction_correlation = build_alpha_correlation_matrix(
        alpha_panels=alpha_candidates,
        run_id=resolved_run_id,
        alpha_construction_version=construction_version,
    )
    constructed_alpha_candidates = alpha_candidates_to_long(
        alpha_candidates,
        run_id=resolved_run_id,
        alpha_construction_version=construction_version,
    )
    alpha_family_summary = _family_summary(alpha_signal_pool, alpha_construction_quality)
    validation_report = _validation_report(
        approved_input_signals=approved_input_signals,
        alpha_signal_pool=alpha_signal_pool,
        alpha_candidates=alpha_candidates,
        alpha_construction_quality=alpha_construction_quality,
    )
    if not validation_report["passed"].all():
        failed = validation_report.loc[
            ~validation_report["passed"],
            ["check_name", "details"],
        ].to_dict("records")
        raise ValueError(f"Alpha construction validation failed: {failed}")

    summary = _summary(
        run_id=resolved_run_id,
        run_timestamp=run_timestamp,
        construction_version=construction_version,
        approved_input_signals=approved_input_signals,
        watchlist_diversifier_signals=watchlist_diversifier_signals,
        alpha_signal_pool=alpha_signal_pool,
        candidate_signals_filtered=candidate_signals_filtered,
        alpha_candidates=alpha_candidates,
        constructed_alpha_candidates=constructed_alpha_candidates,
        alpha_construction_quality=alpha_construction_quality,
    )

    saved_paths = None
    if write:
        saved_paths = save_alpha_construction_outputs(
            alpha_candidates=alpha_candidates,
            metadata=alpha_construction_metadata,
            quality=alpha_construction_quality,
            diagnostics=alpha_construction_diagnostics,
            correlation=alpha_construction_correlation,
            signal_pool=alpha_signal_pool,
            dynamic_weight_audit=alpha_dynamic_weight_audit,
            db_path=resolved_db_path,
            run_id=resolved_run_id,
            alpha_construction_version=construction_version,
        )

    _log(verbose, f"Loaded 04A alpha construction inputs from {resolved_db_path}")
    _log(verbose, f"  approved_input_signals: {len(approved_input_signals):,}")
    _log(verbose, f"  watchlist_diversifier_signals: {len(watchlist_diversifier_signals):,}")
    _log(verbose, f"  alpha_signal_pool: {len(alpha_signal_pool):,}")
    _log(verbose, f"  candidate_signals_filtered: {len(candidate_signals_filtered):,} loaded in {candidate_signal_load_seconds:.2f}s")
    _log(verbose, f"  close_prices shape: {inputs['close_prices'].shape}")
    _log(verbose, f"  warmup_cutoff: {warmup_cutoff}")
    _log(verbose, "04A alpha construction output rows")
    for artifact_name, artifact in [
        ("constructed_alpha_candidates", constructed_alpha_candidates),
        ("alpha_construction_metadata", alpha_construction_metadata),
        ("alpha_construction_quality", alpha_construction_quality),
        ("alpha_construction_diagnostics", alpha_construction_diagnostics),
        ("alpha_construction_correlation", alpha_construction_correlation),
        ("alpha_signal_pool", alpha_signal_pool),
        ("alpha_dynamic_weight_audit", alpha_dynamic_weight_audit),
        ("alpha_family_summary", alpha_family_summary),
        ("validation_report", validation_report),
    ]:
        _log(verbose, f"  {artifact_name}: {len(artifact):,}")
    if "status" in alpha_construction_quality.columns:
        for status, count in alpha_construction_quality["status"].value_counts(dropna=False).items():
            _log(verbose, f"  status[{status}]: {count}")
    _log(verbose, f"SQLite write: {'yes' if write else 'no'}")

    return {
        "constructed_alpha_candidates": constructed_alpha_candidates,
        "alpha_candidates": alpha_candidates,
        "alpha_construction_metadata": alpha_construction_metadata,
        "alpha_construction_quality": alpha_construction_quality,
        "alpha_construction_gate": alpha_construction_quality,
        "alpha_construction_diagnostics": alpha_construction_diagnostics,
        "alpha_construction_correlation": alpha_construction_correlation,
        "alpha_signal_pool": alpha_signal_pool,
        "alpha_dynamic_weight_audit": alpha_dynamic_weight_audit,
        "alpha_family_summary": alpha_family_summary,
        "validation_report": validation_report,
        "summary": summary,
        "approved_input_signals": approved_input_signals,
        "watchlist_diversifier_signals": watchlist_diversifier_signals,
        "saved_paths": saved_paths,
        "db_path": resolved_db_path,
        "run_id": resolved_run_id,
        "run_timestamp": run_timestamp,
        "write": write,
    }


__all__ = [name for name in globals() if not name.startswith("_")]
