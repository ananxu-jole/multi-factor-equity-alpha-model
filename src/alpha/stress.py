"""Engine entrypoint for 07 Alpha Stress Testing."""

from __future__ import annotations

import time
import sqlite3
from contextlib import contextmanager
from pathlib import Path

import pandas as pd

import src.alpha_stress as alpha_stress_core
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
from src.forward_returns import make_forward_returns
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


def _memory_usage_mb() -> float | None:
    try:
        import psutil  # type: ignore[import-not-found]
    except ImportError:
        return None
    try:
        return psutil.Process().memory_info().rss / (1024 * 1024)
    except Exception:
        return None


@contextmanager
def _profile_block(profile_records: list[dict[str, object]], block_name: str):
    memory_before = _memory_usage_mb()
    started = time.perf_counter()
    yield
    elapsed = time.perf_counter() - started
    memory_after = _memory_usage_mb()
    profile_records.append(
        {
            "block": block_name,
            "elapsed_seconds": elapsed,
            "memory_before_mb": memory_before,
            "memory_after_mb": memory_after,
            "memory_delta_mb": (
                memory_after - memory_before
                if memory_before is not None and memory_after is not None
                else None
            ),
        }
    )


def _require_input_tables(db_path: Path) -> None:
    missing_tables = [
        table_name
        for table_name in REQUIRED_INPUT_TABLES
        if not table_exists(table_name, db_path=db_path)
    ]
    if missing_tables:
        raise ValueError(f"Required alpha stress input tables are missing from {db_path}: {missing_tables}")


def _quote_identifier(identifier: str) -> str:
    return '"' + identifier.replace('"', '""') + '"'


def _load_constructed_alpha_stress_metadata_inputs(db_path: Path) -> dict[str, pd.DataFrame]:
    return {
        "quality": load_table("alpha_construction_quality_current", db_path=db_path),
        "diagnostics": load_table("alpha_construction_diagnostics_current", db_path=db_path),
        "wfv_gate": load_table("constructed_alpha_wfv_gate_current", db_path=db_path),
        "wfv_winner_summary": load_table("constructed_alpha_wfv_winner_summary_current", db_path=db_path),
        "regime_overlay_decision": load_table("regime_overlay_diagnostic_decision_current", db_path=db_path),
    }


def _load_constructed_alpha_rows_for_names(alpha_names: list[str], db_path: Path) -> pd.DataFrame:
    if not alpha_names:
        return load_table("alpha_constructed_candidates_current", db_path=db_path).iloc[0:0].copy()
    placeholders = ",".join("?" for _ in alpha_names)
    query = f"""
        SELECT *
        FROM {_quote_identifier("alpha_constructed_candidates_current")}
        WHERE alpha_name IN ({placeholders})
    """
    with sqlite3.connect(db_path) as conn:
        return pd.read_sql_query(query, conn, params=alpha_names)


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
    stress_names = stress_candidates["alpha_name"].dropna().astype(str).drop_duplicates().tolist()
    overlay_names: set[str] = set()
    for table_name in [
        "regime_context_alpha_metadata_current",
        "regime_context_alpha_candidates_current",
    ]:
        if table_exists(table_name, db_path=db_path):
            placeholders = ",".join("?" for _ in stress_names)
            query = f"""
                SELECT DISTINCT alpha_name
                FROM {_quote_identifier(table_name)}
                WHERE alpha_name IN ({placeholders})
            """
            with sqlite3.connect(db_path) as conn:
                rows = conn.execute(query, stress_names).fetchall()
            overlay_names.update(str(row[0]) for row in rows if row[0] is not None)
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
    grouped_alpha_rows = {
        str(alpha_name): group
        for alpha_name, group in alpha_long.groupby("alpha_name", sort=False)
    }
    for _, candidate in stress_candidates.iterrows():
        alpha_name = candidate["alpha_name"]
        panel = build_alpha_panel(grouped_alpha_rows.get(str(alpha_name), alpha_long.iloc[0:0]), alpha_name)
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
    if stress_candidates.empty:
        return pd.DataFrame()

    horizons = sorted(stress_candidates["horizon"].dropna().astype(int).unique().tolist())
    forward_returns = make_forward_returns(close_prices, horizons)
    base_scores: dict[tuple[str, int], dict[str, object]] = {}
    turnover_context: dict[str, tuple[float, object]] = {}
    for _, candidate in stress_candidates.iterrows():
        alpha_name = candidate["alpha_name"]
        horizon = int(candidate["horizon"])
        panel = alpha_panels[alpha_name]
        base_scores[(alpha_name, horizon)] = _score_alpha_panel_against_forward(
            panel,
            forward_returns[horizon],
        )
        turnover_context[alpha_name] = alpha_stress_core._panel_turnover_context(panel)

    stress_frames = []
    for _, candidate in stress_candidates.iterrows():
        alpha_name = candidate["alpha_name"]
        horizon = int(candidate["horizon"])
        panel = alpha_panels[alpha_name]
        base = base_scores[(alpha_name, horizon)]
        turnover = turnover_context[alpha_name]
        fwd = forward_returns[horizon]
        stress_frames.extend(
            [
                _stress_alpha_costs_cached(panel, horizon, base, turnover, cost_bps_list=COST_BPS_LIST),
                _stress_alpha_execution_delay_cached(panel, horizon, base, turnover, fwd, delays=EXECUTION_DELAYS),
                _stress_alpha_turnover_cached(panel, horizon, base, turnover),
                _stress_alpha_subperiods_cached(panel, close_prices, horizon, base, turnover),
                _stress_alpha_universe_subsamples_cached(panel, horizon, base, turnover, fwd),
                _stress_alpha_degradation_cached(panel, horizon, base, turnover, fwd, multipliers=DEGRADATION_MULTIPLIERS),
            ]
        )
    return pd.concat(stress_frames, ignore_index=True) if stress_frames else pd.DataFrame()


def _score_alpha_panel_against_forward(
    alpha_panel: pd.DataFrame,
    fwd_return_panel: pd.DataFrame,
) -> dict[str, object]:
    if alpha_panel.empty or fwd_return_panel.empty:
        return {"mean_ic": alpha_stress_core.np.nan, "effective_mean_ic": alpha_stress_core.np.nan, "effective_ic_ir": alpha_stress_core.np.nan, "n_obs": 0}

    alpha, fwd = alpha_stress_core._align_panels(alpha_panel, fwd_return_panel)
    paired = pd.concat(
        [
            alpha.stack(future_stack=True).rename("alpha"),
            fwd.stack(future_stack=True).rename("fwd_return"),
        ],
        axis=1,
    ).dropna()

    if paired.empty:
        return {"mean_ic": alpha_stress_core.np.nan, "effective_mean_ic": alpha_stress_core.np.nan, "effective_ic_ir": alpha_stress_core.np.nan, "n_obs": 0}

    ic_by_date = paired.groupby(level=0, sort=True).apply(alpha_stress_core._safe_corr).dropna()
    if ic_by_date.empty:
        return {
            "mean_ic": alpha_stress_core.np.nan,
            "effective_mean_ic": alpha_stress_core.np.nan,
            "effective_ic_ir": alpha_stress_core.np.nan,
            "n_obs": int(len(paired)),
        }

    mean_ic = float(ic_by_date.mean())
    ic_std = float(ic_by_date.std(ddof=1)) if len(ic_by_date) > 1 else alpha_stress_core.np.nan
    ic_ir = float(mean_ic / ic_std) if ic_std and not pd.isna(ic_std) else alpha_stress_core.np.nan
    return {
        "mean_ic": mean_ic,
        "effective_mean_ic": abs(mean_ic),
        "effective_ic_ir": abs(ic_ir) if not pd.isna(ic_ir) else alpha_stress_core.np.nan,
        "n_obs": int(len(paired)),
    }


def _stress_alpha_costs_cached(
    alpha_panel: pd.DataFrame,
    horizon: int,
    base: dict[str, object],
    turnover_context: tuple[float, object],
    cost_bps_list: list[int] | tuple[int, ...] = (0, 5, 10, 25),
) -> pd.DataFrame:
    base_ic = base["effective_mean_ic"]
    turnover, turnover_risk_flag = turnover_context
    rows: list[dict[str, object]] = []

    for cost_bps in cost_bps_list:
        cost_drag = 0.0 if pd.isna(turnover) else float(turnover * (float(cost_bps) / 10000.0))
        stressed_ic = base_ic - cost_drag if not pd.isna(base_ic) else alpha_stress_core.np.nan
        degradation = alpha_stress_core._degradation(base_ic, stressed_ic)
        pass_flag = (
            not pd.isna(stressed_ic)
            and stressed_ic >= 0.008
            and (pd.isna(degradation) or degradation <= (0.50 if cost_bps <= 10 else 0.80))
        )
        rows.append(
            alpha_stress_core._result_row(
                alpha_panel=alpha_panel,
                horizon=horizon,
                stress_type="cost",
                stress_case=f"{int(cost_bps)}bps",
                effective_mean_ic=stressed_ic,
                effective_ic_ir=base["effective_ic_ir"],
                degradation_from_base=degradation,
                pass_flag=pass_flag,
                avg_turnover_proxy=turnover,
                turnover_risk_flag=turnover_risk_flag,
                notes=f"turnover_proxy={turnover:.4f}" if not pd.isna(turnover) else "turnover proxy unavailable",
            )
        )

    return pd.DataFrame(rows, columns=alpha_stress_core.ALPHA_STRESS_RESULT_COLUMNS)


def _stress_alpha_execution_delay_cached(
    alpha_panel: pd.DataFrame,
    horizon: int,
    base: dict[str, object],
    turnover_context: tuple[float, object],
    fwd_return_panel: pd.DataFrame,
    delays: list[int] | tuple[int, ...] = (0, 1, 2, 5),
) -> pd.DataFrame:
    base_ic = base["effective_mean_ic"]
    avg_turnover_proxy, turnover_risk_flag = turnover_context
    rows: list[dict[str, object]] = []

    for delay in delays:
        if int(delay) == 0:
            score = base
        else:
            delayed_alpha = alpha_panel.shift(int(delay))
            delayed_alpha.attrs["alpha_name"] = alpha_stress_core._alpha_name(alpha_panel)
            score = _score_alpha_panel_against_forward(delayed_alpha, fwd_return_panel)
        degradation = alpha_stress_core._degradation(base_ic, score["effective_mean_ic"])
        if int(delay) == 0:
            pass_flag = not pd.isna(score["effective_mean_ic"]) and score["effective_mean_ic"] >= 0.015
        else:
            pass_flag = (
                not pd.isna(score["effective_mean_ic"])
                and score["effective_mean_ic"] >= 0.008
                and (pd.isna(degradation) or degradation <= (0.60 if int(delay) <= 2 else 0.90))
            )
        rows.append(
            alpha_stress_core._result_row(
                alpha_panel=alpha_panel,
                horizon=horizon,
                stress_type="execution_delay",
                stress_case=f"{int(delay)}d_delay",
                effective_mean_ic=score["effective_mean_ic"],
                effective_ic_ir=score["effective_ic_ir"],
                degradation_from_base=degradation,
                pass_flag=pass_flag,
                avg_turnover_proxy=avg_turnover_proxy,
                turnover_risk_flag=turnover_risk_flag,
                notes=f"n_obs={score['n_obs']}",
            )
        )

    return pd.DataFrame(rows, columns=alpha_stress_core.ALPHA_STRESS_RESULT_COLUMNS)


def _stress_alpha_turnover_cached(
    alpha_panel: pd.DataFrame,
    horizon: int,
    base: dict[str, object],
    turnover_context: tuple[float, object],
) -> pd.DataFrame:
    avg_turnover_proxy, turnover_risk_flag = turnover_context
    pass_flag = turnover_risk_flag != "HIGH_TURNOVER_RISK"
    return pd.DataFrame(
        [
            alpha_stress_core._result_row(
                alpha_panel=alpha_panel,
                horizon=horizon,
                stress_type="turnover",
                stress_case=str(turnover_risk_flag) if not pd.isna(turnover_risk_flag) else "UNKNOWN_TURNOVER_RISK",
                effective_mean_ic=base["effective_mean_ic"],
                effective_ic_ir=base["effective_ic_ir"],
                degradation_from_base=0.0,
                pass_flag=pass_flag,
                avg_turnover_proxy=avg_turnover_proxy,
                turnover_risk_flag=turnover_risk_flag,
                notes=f"avg_turnover_proxy={avg_turnover_proxy:.4f}"
                if not pd.isna(avg_turnover_proxy)
                else "turnover proxy unavailable",
            )
        ],
        columns=alpha_stress_core.ALPHA_STRESS_RESULT_COLUMNS,
    )


def _stress_alpha_subperiods_cached(
    alpha_panel: pd.DataFrame,
    close_prices: pd.DataFrame,
    horizon: int,
    base: dict[str, object],
    turnover_context: tuple[float, object],
) -> pd.DataFrame:
    base_ic = base["effective_mean_ic"]
    avg_turnover_proxy, turnover_risk_flag = turnover_context
    rows: list[dict[str, object]] = []

    for stress_case, (start_date, end_date) in alpha_stress_core._subperiods_from_dates(alpha_panel.index).items():
        sub_alpha = alpha_panel.loc[start_date:end_date]
        sub_alpha.attrs.update(alpha_panel.attrs)
        sub_close = close_prices.loc[start_date:end_date]
        score = alpha_stress_core._score_alpha_panel(sub_alpha, sub_close, horizon)
        degradation = alpha_stress_core._degradation(base_ic, score["effective_mean_ic"])
        pass_flag = (
            not pd.isna(score["effective_mean_ic"])
            and score["effective_mean_ic"] >= 0.008
            and (pd.isna(degradation) or degradation <= 0.75)
        )
        rows.append(
            alpha_stress_core._result_row(
                alpha_panel=alpha_panel,
                horizon=horizon,
                stress_type="subperiod",
                stress_case=stress_case,
                effective_mean_ic=score["effective_mean_ic"],
                effective_ic_ir=score["effective_ic_ir"],
                degradation_from_base=degradation,
                pass_flag=pass_flag,
                avg_turnover_proxy=avg_turnover_proxy,
                turnover_risk_flag=turnover_risk_flag,
                notes=f"{start_date.date()} to {end_date.date()}; n_obs={score['n_obs']}",
            )
        )

    return pd.DataFrame(rows, columns=alpha_stress_core.ALPHA_STRESS_RESULT_COLUMNS)


def _stress_alpha_universe_subsamples_cached(
    alpha_panel: pd.DataFrame,
    horizon: int,
    base: dict[str, object],
    turnover_context: tuple[float, object],
    fwd_return_panel: pd.DataFrame,
) -> pd.DataFrame:
    tickers = list(alpha_panel.columns)
    midpoint = max(1, len(tickers) // 2)
    rng_42 = alpha_stress_core.np.random.default_rng(42)
    rng_99 = alpha_stress_core.np.random.default_rng(99)
    half_size = max(1, len(tickers) // 2)
    subsets = {
        "first_half_tickers": tickers[:midpoint],
        "second_half_tickers": tickers[midpoint:] or tickers[:midpoint],
        "random_half_seed_42": sorted(rng_42.choice(tickers, size=half_size, replace=False).tolist()),
        "random_half_seed_99": sorted(rng_99.choice(tickers, size=half_size, replace=False).tolist()),
    }

    base_ic = base["effective_mean_ic"]
    avg_turnover_proxy, turnover_risk_flag = turnover_context
    rows: list[dict[str, object]] = []
    for stress_case, subset in subsets.items():
        subset_alpha = alpha_panel.reindex(columns=subset)
        subset_alpha.attrs["alpha_name"] = alpha_stress_core._alpha_name(alpha_panel)
        subset_fwd = fwd_return_panel.reindex(columns=subset)
        score = _score_alpha_panel_against_forward(subset_alpha, subset_fwd)
        degradation = alpha_stress_core._degradation(base_ic, score["effective_mean_ic"])
        pass_flag = (
            not pd.isna(score["effective_mean_ic"])
            and score["effective_mean_ic"] >= 0.008
            and (pd.isna(degradation) or degradation <= 0.75)
        )
        rows.append(
            alpha_stress_core._result_row(
                alpha_panel=alpha_panel,
                horizon=horizon,
                stress_type="universe_subsample",
                stress_case=stress_case,
                effective_mean_ic=score["effective_mean_ic"],
                effective_ic_ir=score["effective_ic_ir"],
                degradation_from_base=degradation,
                pass_flag=pass_flag,
                avg_turnover_proxy=avg_turnover_proxy,
                turnover_risk_flag=turnover_risk_flag,
                notes=f"n_tickers={len(subset)}; n_obs={score['n_obs']}",
            )
        )

    return pd.DataFrame(rows, columns=alpha_stress_core.ALPHA_STRESS_RESULT_COLUMNS)


def _stress_alpha_degradation_cached(
    alpha_panel: pd.DataFrame,
    horizon: int,
    base: dict[str, object],
    turnover_context: tuple[float, object],
    fwd_return_panel: pd.DataFrame,
    multipliers: list[float] | tuple[float, ...] = (0.75, 0.50),
) -> pd.DataFrame:
    base_ic = base["effective_mean_ic"]
    avg_turnover_proxy, turnover_risk_flag = turnover_context
    rows: list[dict[str, object]] = []

    for multiplier in multipliers:
        degraded_alpha = alpha_panel * float(multiplier)
        degraded_alpha.attrs.update(alpha_panel.attrs)
        score = _score_alpha_panel_against_forward(degraded_alpha, fwd_return_panel)
        degradation = alpha_stress_core._degradation(base_ic, score["effective_mean_ic"])
        pass_flag = (
            not pd.isna(score["effective_mean_ic"])
            and score["effective_mean_ic"] >= 0.008
            and (pd.isna(degradation) or degradation <= 0.75)
        )
        rows.append(
            alpha_stress_core._result_row(
                alpha_panel=alpha_panel,
                horizon=horizon,
                stress_type="alpha_degradation",
                stress_case=f"alpha_x_{float(multiplier):.2f}",
                effective_mean_ic=score["effective_mean_ic"],
                effective_ic_ir=score["effective_ic_ir"],
                degradation_from_base=degradation,
                pass_flag=pass_flag,
                avg_turnover_proxy=avg_turnover_proxy,
                turnover_risk_flag=turnover_risk_flag,
                notes=f"alpha_multiplier={float(multiplier):.2f}; n_obs={score['n_obs']}",
            )
        )

    return pd.DataFrame(rows, columns=alpha_stress_core.ALPHA_STRESS_RESULT_COLUMNS)


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
    profile_records: list[dict[str, object]] = []

    _require_input_tables(resolved_db_path)
    with _profile_block(profile_records, "loading 04B WFV outputs"):
        inputs = _load_constructed_alpha_stress_metadata_inputs(resolved_db_path)

    with _profile_block(profile_records, "loading constructed alpha candidates"):
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

    with _profile_block(profile_records, "stress scenario generation"):
        alpha_names = stress_candidates["alpha_name"].dropna().astype(str).drop_duplicates().tolist()
        inputs["alpha_long"] = _load_constructed_alpha_rows_for_names(alpha_names, resolved_db_path)
        alpha_panels = _build_alpha_panels(inputs["alpha_long"], stress_candidates)
        ohlcv = load_ohlcv_panels(current=True, db_path=resolved_db_path)
        close_prices = ohlcv["close"]

    with _profile_block(profile_records, "stress scenario evaluation"):
        stress_results = _run_stress_scenarios(stress_candidates, alpha_panels, close_prices)

    with _profile_block(profile_records, "gate/status assignment"):
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
        with _profile_block(profile_records, "SQLite writes"):
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
    else:
        profile_records.append(
            {
                "block": "SQLite writes",
                "elapsed_seconds": 0.0,
                "memory_before_mb": _memory_usage_mb(),
                "memory_after_mb": _memory_usage_mb(),
                "memory_delta_mb": 0.0,
            }
        )
    profile = pd.DataFrame(profile_records)

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
        "profile": profile,
        "saved_paths": saved_paths,
        "db_path": resolved_db_path,
        "run_id": resolved_run_id,
        "run_timestamp": run_timestamp,
        "write": write,
    }


__all__ = [name for name in globals() if not name.startswith("_")]
