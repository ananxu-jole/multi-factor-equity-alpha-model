from __future__ import annotations

import json
from dataclasses import dataclass
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd

from run_participation_liquidity_state_shift_refinement import (
    SIGNAL_NAME as LIQUIDITY_SIGNAL_NAME,
    V4_DIR,
    _build_states as build_liquidity_states,
    _variant_panels as build_liquidity_variants,
)
from run_track_b_robustness_discovery_v3 import (
    baseline_panels,
    build_stress_states,
    daily_ic,
    load_inputs,
    score_signals,
    wfv_diagnostics,
)


RUN_ID = "conditional_alpha_inventory_monitoring_v1"
OUT_DIR = Path("artifacts/research") / RUN_ID
NOTE_PATH = Path("docs/research_notes/conditional_alpha_inventory_monitoring_v1.md")

BREADTH_PANEL_PATH = Path(
    "artifacts/research/participation_breadth_repair_refinement_v1/"
    "strict_weak_breadth_rebalance_10_signal_panel.parquet"
)
VOLATILITY_PANEL_PATH = Path(
    "artifacts/research/volatility_compression_stress_stabilization_conditional_validation_v1/"
    "rebalance_5_signal_panel.parquet"
)

HORIZON = 20
ROLLING_WINDOW = 63


@dataclass(frozen=True)
class InventoryCandidate:
    signal_name: str
    primary_variant: str
    family: str
    inventory_status: str
    activation_semantics: str
    expected_horizon: str
    turnover_ceiling: float
    active_coverage_min: float
    active_coverage_max: float
    inventory_similarity_ceiling: float
    reversal_similarity_ceiling: float
    momentum_similarity_ceiling: float
    one_window_dominance_ceiling: float
    recent_positive_rate_min: float
    recent_mean_ic_min: float


CANDIDATES = [
    InventoryCandidate(
        signal_name="participation_liquidity_state_shift_20_60",
        primary_variant="rank_persist_10_state_TREND_HOSTILE_zero",
        family="participation_liquidity_repair",
        inventory_status="INVENTORY_ACTIVE_RESEARCH",
        activation_semantics="TREND_HOSTILE primary; WEAK_BREADTH and STRESS_OR_WEAK_BREADTH confirmation",
        expected_horizon="h20 primary; h10 review flag",
        turnover_ceiling=0.12,
        active_coverage_min=0.25,
        active_coverage_max=0.65,
        inventory_similarity_ceiling=0.35,
        reversal_similarity_ceiling=0.35,
        momentum_similarity_ceiling=0.35,
        one_window_dominance_ceiling=0.70,
        recent_positive_rate_min=0.45,
        recent_mean_ic_min=0.0,
    ),
    InventoryCandidate(
        signal_name="participation_breadth_repair_under_hostile_trend",
        primary_variant="strict_weak_breadth_rebalance_10",
        family="breadth_repair_under_hostile_trend",
        inventory_status="CONDITIONAL_ALPHA_INTEGRATION_REVIEW_CANDIDATE",
        activation_semantics="strict weak breadth under hostile trend",
        expected_horizon="h20",
        turnover_ceiling=0.05,
        active_coverage_min=0.10,
        active_coverage_max=0.40,
        inventory_similarity_ceiling=0.15,
        reversal_similarity_ceiling=0.15,
        momentum_similarity_ceiling=0.20,
        one_window_dominance_ceiling=0.65,
        recent_positive_rate_min=0.45,
        recent_mean_ic_min=0.0,
    ),
    InventoryCandidate(
        signal_name="volatility_compression_after_stress_stabilization",
        primary_variant="rebalance_5",
        family="volatility_stress_transition",
        inventory_status="INVENTORY_ACTIVE_RESEARCH_WITH_GUARDRAILS",
        activation_semantics="recent volatility or panic stress followed by range/volatility stabilization",
        expected_horizon="h20",
        turnover_ceiling=0.05,
        active_coverage_min=0.15,
        active_coverage_max=0.45,
        inventory_similarity_ceiling=0.15,
        reversal_similarity_ceiling=0.15,
        momentum_similarity_ceiling=0.15,
        one_window_dominance_ceiling=0.65,
        recent_positive_rate_min=0.45,
        recent_mean_ic_min=0.0,
    ),
]


def _ensure_dirs() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    NOTE_PATH.parent.mkdir(parents=True, exist_ok=True)


def _forward_returns(close: pd.DataFrame, horizon: int) -> pd.DataFrame:
    return close.shift(-horizon) / close - 1.0


def _panel_corr(left: pd.DataFrame, right: pd.DataFrame) -> float:
    left, right = left.align(right, join="inner", axis=0)
    left, right = left.align(right, join="inner", axis=1)
    a = left.to_numpy(dtype=float, copy=False).ravel()
    b = right.to_numpy(dtype=float, copy=False).ravel()
    mask = np.isfinite(a) & np.isfinite(b)
    if int(mask.sum()) < 100:
        return np.nan
    a = a[mask]
    b = b[mask]
    a_std = a.std()
    b_std = b.std()
    if a_std == 0 or b_std == 0:
        return np.nan
    return float(np.mean((a - a.mean()) * (b - b.mean())) / (a_std * b_std))


def _active_dates(panel: pd.DataFrame) -> pd.Series:
    valid_count = panel.notna().sum(axis=1)
    mean_abs = panel.abs().mean(axis=1, skipna=True)
    return (valid_count >= 25) & (mean_abs > 0.02)


def _turnover_series(panel: pd.DataFrame) -> pd.Series:
    return panel.diff().abs().mean(axis=1, skipna=True)


def _load_inventory_panels(panels: dict[str, pd.DataFrame], benchmark: pd.Series) -> tuple[dict[str, pd.DataFrame], list[dict[str, str]]]:
    loaded: dict[str, pd.DataFrame] = {}
    missing: list[dict[str, str]] = []
    close = panels["close"]

    try:
        base = pd.read_parquet(V4_DIR / f"{LIQUIDITY_SIGNAL_NAME}_signal_panel.parquet")
        states = build_liquidity_states(close, panels["volume"], benchmark)
        variants = build_liquidity_variants(base.reindex(index=close.index, columns=close.columns), states)
        loaded["participation_liquidity_state_shift_20_60"] = variants[
            "rank_persist_10_state_TREND_HOSTILE_zero"
        ].reindex(index=close.index, columns=close.columns)
    except Exception as exc:  # noqa: BLE001 - research runner records missing/unavailable inputs.
        missing.append(
            {
                "signal_name": "participation_liquidity_state_shift_20_60",
                "expected_artifact": str(V4_DIR / f"{LIQUIDITY_SIGNAL_NAME}_signal_panel.parquet"),
                "reason": str(exc),
            }
        )

    if BREADTH_PANEL_PATH.exists():
        loaded["participation_breadth_repair_under_hostile_trend"] = pd.read_parquet(BREADTH_PANEL_PATH).reindex(
            index=close.index,
            columns=close.columns,
        )
    else:
        missing.append(
            {
                "signal_name": "participation_breadth_repair_under_hostile_trend",
                "expected_artifact": str(BREADTH_PANEL_PATH),
                "reason": "primary panel not found",
            }
        )

    if VOLATILITY_PANEL_PATH.exists():
        loaded["volatility_compression_after_stress_stabilization"] = pd.read_parquet(VOLATILITY_PANEL_PATH).reindex(
            index=close.index,
            columns=close.columns,
        )
    else:
        missing.append(
            {
                "signal_name": "volatility_compression_after_stress_stabilization",
                "expected_artifact": str(VOLATILITY_PANEL_PATH),
                "reason": "primary panel not found",
            }
        )
    return loaded, missing


def _rolling_health(daily_ics: pd.DataFrame) -> pd.DataFrame:
    rows = []
    focus = daily_ics[daily_ics["horizon"].eq(HORIZON)].copy()
    for signal_name, group in focus.groupby("signal_name"):
        series = group.sort_values("Date").set_index("Date")["ic"].astype(float)
        rolling_mean = series.rolling(ROLLING_WINDOW, min_periods=30).mean()
        rolling_pos = series.gt(0).rolling(ROLLING_WINDOW, min_periods=30).mean()
        rows.append(
            {
                "signal_name": signal_name,
                "rolling_window": ROLLING_WINDOW,
                "rolling_h20_ic_latest": float(rolling_mean.dropna().iloc[-1]) if not rolling_mean.dropna().empty else np.nan,
                "rolling_h20_ic_min": float(rolling_mean.min(skipna=True)),
                "rolling_h20_ic_median": float(rolling_mean.median(skipna=True)),
                "rolling_positive_rate_latest": float(rolling_pos.dropna().iloc[-1]) if not rolling_pos.dropna().empty else np.nan,
                "rolling_positive_rate_min": float(rolling_pos.min(skipna=True)),
                "recent_valid_ic_dates": int(series.tail(ROLLING_WINDOW).dropna().shape[0]),
            }
        )
    return pd.DataFrame(rows)


def _active_coverage_summary(signals: dict[str, pd.DataFrame]) -> pd.DataFrame:
    rows = []
    for signal_name, panel in signals.items():
        active = _active_dates(panel)
        transitions = active.astype(int).diff().abs().fillna(0)
        active_window_counts = []
        for dates in np.array_split(active.index, 4):
            active_window_counts.append(int(active.reindex(dates).fillna(False).sum()))
        rows.append(
            {
                "signal_name": signal_name,
                "active_dates": int(active.sum()),
                "active_coverage": float(active.mean()),
                "activation_transitions": int(transitions.sum()),
                "min_active_window_dates": int(min(active_window_counts)) if active_window_counts else 0,
                "active_window_coverage_ratio": float(np.mean([count >= 25 for count in active_window_counts]))
                if active_window_counts
                else np.nan,
                "mean_active_ticker_coverage": float(panel[active].notna().mean(axis=1).mean()) if active.any() else np.nan,
            }
        )
    return pd.DataFrame(rows)


def _turnover_summary(signals: dict[str, pd.DataFrame]) -> pd.DataFrame:
    rows = []
    for signal_name, panel in signals.items():
        turnover = _turnover_series(panel)
        rows.append(
            {
                "signal_name": signal_name,
                "turnover_proxy": float(turnover.mean(skipna=True)),
                "rolling_turnover_latest": float(turnover.rolling(ROLLING_WINDOW, min_periods=30).mean().dropna().iloc[-1])
                if not turnover.rolling(ROLLING_WINDOW, min_periods=30).mean().dropna().empty
                else np.nan,
                "turnover_p95": float(turnover.quantile(0.95)),
                "turnover_max": float(turnover.max(skipna=True)),
            }
        )
    return pd.DataFrame(rows)


def _coactivation_matrix(signals: dict[str, pd.DataFrame]) -> pd.DataFrame:
    active = {name: _active_dates(panel) for name, panel in signals.items()}
    names = list(active)
    matrix = pd.DataFrame(index=names, columns=names, dtype=float)
    for left in names:
        for right in names:
            denom = int(active[left].sum())
            matrix.loc[left, right] = float((active[left] & active[right]).sum() / denom) if denom else np.nan
    return matrix


def _correlation_matrix(signals: dict[str, pd.DataFrame]) -> pd.DataFrame:
    names = list(signals)
    matrix = pd.DataFrame(index=names, columns=names, dtype=float)
    for left in names:
        for right in names:
            matrix.loc[left, right] = 1.0 if left == right else _panel_corr(signals[left], signals[right])
    return matrix


def _similarity_summary(signals: dict[str, pd.DataFrame], panels: dict[str, pd.DataFrame], benchmark: pd.Series) -> pd.DataFrame:
    refs = baseline_panels(signals, panels, benchmark)
    for name, panel in signals.items():
        refs[f"inventory_{name}"] = panel
    rows = []
    for signal_name, panel in signals.items():
        for comparison, ref in refs.items():
            if comparison == f"inventory_{signal_name}":
                continue
            corr = _panel_corr(panel, ref)
            rows.append(
                {
                    "signal_name": signal_name,
                    "comparison": comparison,
                    "value_corr": corr,
                    "abs_value_corr": abs(corr) if pd.notna(corr) else np.nan,
                    "comparison_type": _comparison_type(comparison),
                }
            )
    detail = pd.DataFrame(rows)
    summary_rows = []
    for signal_name, group in detail.groupby("signal_name"):
        summary_rows.append(
            {
                "signal_name": signal_name,
                "max_inventory_corr": _max_by_type(group, "inventory"),
                "max_reversal_corr": _max_by_type(group, "reversal"),
                "max_momentum_corr": _max_by_type(group, "momentum"),
                "max_baseline_corr": float(group["abs_value_corr"].max(skipna=True)),
                "top_similarity": str(group.loc[group["abs_value_corr"].idxmax(), "comparison"])
                if group["abs_value_corr"].notna().any()
                else "unavailable",
            }
        )
    return detail, pd.DataFrame(summary_rows)


def _comparison_type(comparison: str) -> str:
    if comparison.startswith("inventory_"):
        return "inventory"
    if "reversal" in comparison:
        return "reversal"
    if "momentum" in comparison:
        return "momentum"
    return "baseline"


def _max_by_type(group: pd.DataFrame, comparison_type: str) -> float:
    values = group.loc[group["comparison_type"].eq(comparison_type), "abs_value_corr"].dropna()
    return float(values.max()) if not values.empty else np.nan


def _window_concentration(wfv_windows: pd.DataFrame) -> pd.DataFrame:
    rows = []
    h20 = wfv_windows[wfv_windows["horizon"].eq(HORIZON)].copy()
    for signal_name, group in h20.groupby("signal_name"):
        group = group.sort_values("window")
        values = group["mean_test_ic"].astype(float)
        denom = float(values.abs().sum())
        positive = values[values > 0]
        rows.append(
            {
                "signal_name": signal_name,
                "window_count": int(len(values)),
                "positive_window_count": int((values > 0).sum()),
                "negative_window_count": int((values <= 0).sum()),
                "one_window_dominance_recomputed": float(values.abs().max() / denom) if denom else np.nan,
                "largest_positive_window_share": float(positive.max() / positive.sum()) if positive.sum() > 0 else np.nan,
                "recent_window_ic": float(values.iloc[-1]) if len(values) else np.nan,
                "recent_window_positive_rate": float(group.iloc[-1]["positive_ic_rate"]) if len(group) else np.nan,
                "min_valid_ic_dates": int(group["valid_ic_dates"].min()) if len(group) else 0,
            }
        )
    return pd.DataFrame(rows)


def _fixed_horizon_wfv_monitor(daily_ics: pd.DataFrame, horizon: int = HORIZON) -> tuple[pd.DataFrame, pd.DataFrame]:
    summary_rows = []
    window_rows = []
    focus = daily_ics[daily_ics["horizon"].eq(horizon)].copy()
    for signal_name, group in focus.groupby("signal_name"):
        series = group.sort_values("Date").set_index("Date")["ic"].dropna().astype(float)
        if series.empty:
            continue
        means = []
        for window, positions in enumerate(np.array_split(np.arange(len(series)), 4), start=1):
            sample = series.iloc[positions]
            mean_ic = float(sample.mean()) if len(sample) else np.nan
            std_ic = sample.std(ddof=0) if len(sample) > 1 else np.nan
            means.append(mean_ic)
            window_rows.append(
                {
                    "signal_name": signal_name,
                    "horizon": horizon,
                    "window": window,
                    "start_date": sample.index.min().date().isoformat() if len(sample) else "",
                    "end_date": sample.index.max().date().isoformat() if len(sample) else "",
                    "mean_test_ic": mean_ic,
                    "test_ic_ir": float(mean_ic / std_ic) if pd.notna(std_ic) and std_ic > 0 else np.nan,
                    "positive_ic_rate": float((sample > 0).mean()) if len(sample) else np.nan,
                    "valid_ic_dates": int(len(sample)),
                }
            )
        values = pd.Series(means, dtype=float).dropna()
        denom = float(values.abs().sum())
        summary_rows.append(
            {
                "signal_name": signal_name,
                "horizon": horizon,
                "n_windows": int(len(values)),
                "effective_mean_test_ic": float(values.mean()) if len(values) else np.nan,
                "effective_test_ic_ir": float(values.mean() / values.std(ddof=0))
                if len(values) > 1 and values.std(ddof=0) > 0
                else np.nan,
                "persistence": float((values > 0).mean()) if len(values) else np.nan,
                "sign_consistency": float((values > 0).mean()) if len(values) else np.nan,
                "one_window_dominance": float(values.abs().max() / denom) if denom else np.nan,
            }
        )
    return pd.DataFrame(summary_rows), pd.DataFrame(window_rows)


def _regime_overlap_summary(
    daily_ics: pd.DataFrame,
    scores: pd.DataFrame,
    close: pd.DataFrame,
    benchmark: pd.Series,
) -> pd.DataFrame:
    stress = build_stress_states(close, benchmark)
    bench_ret20 = benchmark.pct_change(20, fill_method=None)
    ma60 = benchmark.rolling(60, min_periods=40).mean()
    breadth20 = (close.pct_change(20, fill_method=None) > 0).mean(axis=1)
    dispersion20 = close.pct_change(20, fill_method=None).std(axis=1)
    states = stress.copy()
    states["trend_hostile"] = ((benchmark < ma60) | (bench_ret20 < 0)).fillna(False)
    states["weak_breadth"] = (breadth20 < breadth20.rolling(252, min_periods=100).quantile(0.35)).fillna(False)
    states["low_dispersion"] = (dispersion20 < dispersion20.rolling(252, min_periods=100).quantile(0.35)).fillna(False)
    states["stress_or_weak_breadth"] = (
        states["drawdown_acceleration"] | states["panic_liquidity_stress"] | states["weak_breadth"]
    ).fillna(False)

    rows = []
    focus = daily_ics[daily_ics["horizon"].eq(HORIZON)].copy()
    for signal_name in scores["signal_name"].unique():
        series = focus[focus["signal_name"].eq(signal_name)].set_index("Date")["ic"]
        for state_name, mask in states.items():
            sample = series.reindex(states.index[mask.astype(bool)]).dropna()
            rows.append(
                {
                    "signal_name": signal_name,
                    "state": state_name,
                    "state_dates": int(mask.astype(bool).sum()),
                    "valid_ic_dates": int(len(sample)),
                    "mean_ic": float(sample.mean()) if len(sample) else np.nan,
                    "positive_ic_rate": float((sample > 0).mean()) if len(sample) else np.nan,
                }
            )
    return pd.DataFrame(rows)


def _guardrail_status(
    candidate_summary: pd.DataFrame,
    specs: list[InventoryCandidate],
) -> pd.DataFrame:
    spec_by_name = {spec.signal_name: spec for spec in specs}
    rows = []
    for _, row in candidate_summary.iterrows():
        spec = spec_by_name[row["signal_name"]]
        checks = {
            "active_coverage_min": row["active_coverage"] >= spec.active_coverage_min,
            "active_coverage_max": row["active_coverage"] <= spec.active_coverage_max,
            "turnover_ceiling": row["turnover_proxy"] <= spec.turnover_ceiling,
            "inventory_similarity_ceiling": row["max_inventory_corr"] <= spec.inventory_similarity_ceiling
            if pd.notna(row["max_inventory_corr"])
            else False,
            "reversal_similarity_ceiling": row["max_reversal_corr"] <= spec.reversal_similarity_ceiling
            if pd.notna(row["max_reversal_corr"])
            else False,
            "momentum_similarity_ceiling": row["max_momentum_corr"] <= spec.momentum_similarity_ceiling
            if pd.notna(row["max_momentum_corr"])
            else False,
            "one_window_dominance_ceiling": row["one_window_dominance_recomputed"] <= spec.one_window_dominance_ceiling,
            "recent_positive_rate_min": row["recent_window_positive_rate"] >= spec.recent_positive_rate_min,
            "recent_mean_ic_min": row["recent_window_ic"] >= spec.recent_mean_ic_min,
            "semantic_rebuild_equivalence_ready": row["panel_source_status"] == "available",
        }
        failed = [name for name, ok in checks.items() if not bool(ok)]
        caution = []
        if row["rolling_h20_ic_latest"] < row["h20_mean_ic"] * 0.50:
            caution.append("rolling_ic_below_half_full_sample")
        if row["active_window_coverage_ratio"] < 1.0:
            caution.append("active_window_coverage_incomplete")
        if row["largest_positive_window_share"] > 0.60:
            caution.append("positive_ic_window_concentration")

        if failed and ("recent_mean_ic_min" in failed or "recent_positive_rate_min" in failed):
            classification = "WATCH_MONITOR"
        elif len(failed) >= 3:
            classification = "REVIEW_FOR_DOWNGRADE"
        elif failed:
            classification = "DEGRADED_RESEARCH"
        elif caution:
            classification = "WATCH_MONITOR"
        else:
            classification = "HEALTHY_ACTIVE_RESEARCH"

        rows.append(
            {
                "signal_name": row["signal_name"],
                "monitoring_classification": classification,
                "failed_guardrails": "; ".join(failed) if failed else "none",
                "caution_flags": "; ".join(caution) if caution else "none",
                **{f"pass_{name}": bool(ok) for name, ok in checks.items()},
            }
        )
    return pd.DataFrame(rows)


def _inventory_level_summary(
    coactivation: pd.DataFrame,
    corr: pd.DataFrame,
    candidate_summary: pd.DataFrame,
    regime_overlap: pd.DataFrame,
) -> pd.DataFrame:
    off_diag_corr = []
    off_diag_coactivation = []
    for left, right in combinations(corr.index, 2):
        off_diag_corr.append(abs(float(corr.loc[left, right])))
        off_diag_coactivation.append(float(max(coactivation.loc[left, right], coactivation.loc[right, left])))

    hostile_states = {"trend_hostile", "weak_breadth", "stress_or_weak_breadth", "panic_liquidity_stress", "drawdown_acceleration"}
    state_hits = regime_overlap[
        regime_overlap["state"].isin(hostile_states) & regime_overlap["mean_ic"].gt(0)
    ].groupby("signal_name")["state"].nunique()

    return pd.DataFrame(
        [
            {
                "inventory_candidate_count": int(candidate_summary.shape[0]),
                "max_pairwise_abs_corr": float(np.nanmax(off_diag_corr)) if off_diag_corr else np.nan,
                "max_pairwise_coactivation": float(np.nanmax(off_diag_coactivation)) if off_diag_coactivation else np.nan,
                "h20_concentration": "all_inventory_candidates_primary_h20",
                "hostile_or_stress_positive_state_candidate_count": int((state_hits >= 2).sum()),
                "turnover_concentration_max": float(candidate_summary["turnover_proxy"].max(skipna=True)),
                "active_coverage_min": float(candidate_summary["active_coverage"].min(skipna=True)),
                "recent_window_negative_count": int((candidate_summary["recent_window_ic"] < 0).sum()),
            }
        ]
    )


def _build_candidate_summary(
    signals: dict[str, pd.DataFrame],
    panels: dict[str, pd.DataFrame],
    benchmark: pd.Series,
    missing: list[dict[str, str]],
) -> tuple[dict[str, pd.DataFrame], pd.DataFrame]:
    scores, daily_ics = score_signals(signals, panels["close"])
    wfv, wfv_windows = wfv_diagnostics(daily_ics, scores)
    h20_wfv, h20_wfv_windows = _fixed_horizon_wfv_monitor(daily_ics, HORIZON)
    rolling = _rolling_health(daily_ics)
    active = _active_coverage_summary(signals)
    turnover = _turnover_summary(signals)
    sim_detail, sim_summary = _similarity_summary(signals, panels, benchmark)
    concentration = _window_concentration(h20_wfv_windows)
    h20 = scores[scores["horizon"].eq(HORIZON)].rename(
        columns={
            "mean_ic": "h20_mean_ic",
            "ic_ir": "h20_ic_ir",
            "positive_ic_rate": "h20_positive_ic_rate",
            "n_dates": "h20_n_dates",
        }
    )
    source_rows = [
        {"signal_name": name, "panel_source_status": "available"}
        for name in signals
    ] + [
        {"signal_name": item["signal_name"], "panel_source_status": f"missing: {item['reason']}"}
        for item in missing
    ]
    source = pd.DataFrame(source_rows)

    spec_df = pd.DataFrame([spec.__dict__ for spec in CANDIDATES])
    summary = (
        spec_df.merge(h20[["signal_name", "h20_mean_ic", "h20_ic_ir", "h20_positive_ic_rate", "h20_n_dates"]], on="signal_name", how="left")
        .merge(h20_wfv[["signal_name", "persistence", "sign_consistency", "effective_test_ic_ir"]], on="signal_name", how="left")
        .merge(rolling, on="signal_name", how="left")
        .merge(active, on="signal_name", how="left")
        .merge(turnover, on="signal_name", how="left")
        .merge(sim_summary, on="signal_name", how="left")
        .merge(concentration, on="signal_name", how="left")
        .merge(source, on="signal_name", how="left")
    )
    artifacts = {
        "scores": scores,
        "daily_ics": daily_ics,
        "wfv": wfv,
        "wfv_windows": wfv_windows,
        "h20_wfv": h20_wfv,
        "h20_wfv_windows": h20_wfv_windows,
        "similarity_detail": sim_detail,
        "similarity_summary": sim_summary,
        "active": active,
        "turnover": turnover,
        "rolling": rolling,
        "window_concentration": concentration,
    }
    return artifacts, summary


def _write_note(
    candidate_summary: pd.DataFrame,
    guardrails: pd.DataFrame,
    coactivation: pd.DataFrame,
    corr: pd.DataFrame,
    regime_overlap: pd.DataFrame,
    inventory_summary: pd.DataFrame,
    missing: list[dict[str, str]],
) -> None:
    merged = candidate_summary.merge(
        guardrails[["signal_name", "monitoring_classification", "failed_guardrails", "caution_flags"]],
        on="signal_name",
        how="left",
    )
    class_counts = guardrails["monitoring_classification"].value_counts().to_dict()
    extra_monitor = guardrails[
        guardrails["monitoring_classification"].isin(["WATCH_MONITOR", "DEGRADED_RESEARCH", "REVIEW_FOR_DOWNGRADE"])
    ]["signal_name"].tolist()
    lines = [
        "# Conditional Alpha Inventory Monitoring v1",
        "",
        "## Executive Takeaway",
        "",
        f"This research-only monitoring pass evaluated the current three-candidate Conditional Alpha Inventory under `{RUN_ID}`.",
        "",
        f"Monitoring classifications: `{json.dumps(class_counts, sort_keys=True)}`",
        "",
        "The inventory remains research-usable, but it should be treated as a monitored ecosystem rather than a static candidate list. The main risks are h20 concentration, shared hostile/stress state dependence, active-coverage fragility, and candidate-specific recent-window or window-concentration guardrails.",
        "",
        "No new alpha candidates, discovery, validation/refinement, production registration, survivor/watchlist mutation, portfolio construction, ML integration, signal blending, weighting engine, optimization engine, gate/schema/threshold change, or production Conditional-Alpha wiring was performed.",
        "",
        "## Scope",
        "",
        "This runner uses existing research panels and artifacts where available. If a full panel is unavailable, the candidate is documented as missing rather than guessed. The `participation_liquidity_state_shift_20_60` primary representation is rebuilt from its v4 base panel and documented refinement transformation because the final primary panel was not stored as a standalone parquet artifact.",
        "",
        "## Inventory Health Summary",
        "",
        merged[
            [
                "signal_name",
                "family",
                "inventory_status",
                "primary_variant",
                "h20_mean_ic",
                "h20_positive_ic_rate",
                "turnover_proxy",
                "active_coverage",
                "persistence",
                "sign_consistency",
                "rolling_h20_ic_latest",
                "recent_window_ic",
                "recent_window_positive_rate",
                "max_inventory_corr",
                "max_reversal_corr",
                "monitoring_classification",
                "failed_guardrails",
                "caution_flags",
            ]
        ].to_markdown(index=False),
        "",
        "## Candidate-Level Monitoring Interpretation",
        "",
    ]

    for _, row in merged.iterrows():
        lines.extend(
            [
                f"### {row['signal_name']}",
                "",
                f"- Classification: `{row['monitoring_classification']}`",
                f"- Activation semantics: {row['activation_semantics']}",
                f"- h20 mean IC / positive IC rate: `{row['h20_mean_ic']:.6f}` / `{row['h20_positive_ic_rate']:.6f}`",
                f"- Turnover / active coverage: `{row['turnover_proxy']:.6f}` / `{row['active_coverage']:.6f}`",
                f"- WFV-style persistence/sign consistency: `{row['persistence']:.2f}` / `{row['sign_consistency']:.2f}`",
                f"- Latest rolling h20 IC / rolling positive rate: `{row['rolling_h20_ic_latest']:.6f}` / `{row['rolling_positive_rate_latest']:.6f}`",
                f"- Recent window IC / positive rate: `{row['recent_window_ic']:.6f}` / `{row['recent_window_positive_rate']:.6f}`",
                f"- Guardrail failures: `{row['failed_guardrails']}`",
                f"- Caution flags: `{row['caution_flags']}`",
                "",
            ]
        )

    lines.extend(
        [
            "## Inventory-Level Overlap",
            "",
            "### Co-Activation Matrix",
            "",
            coactivation.to_markdown(),
            "",
            "### Signal Correlation Matrix",
            "",
            corr.to_markdown(),
            "",
            "### Inventory-Level Summary",
            "",
            inventory_summary.to_markdown(index=False),
            "",
            "## Shared Regime / State Dependence",
            "",
            "Top positive h20 state slices by candidate:",
            "",
            regime_overlap.sort_values(["signal_name", "mean_ic"], ascending=[True, False])
            .groupby("signal_name")
            .head(5)[["signal_name", "state", "state_dates", "valid_ic_dates", "mean_ic", "positive_ic_rate"]]
            .to_markdown(index=False),
            "",
            "## Current Ecosystem Risks",
            "",
            "- h20 remains the dominant inventory horizon.",
            "- Hostile, weak-breadth, drawdown, panic/liquidity, or post-stress states explain much of the current inventory's useful behavior.",
            "- The participation and breadth candidates are intentionally distinct, but they still occupy adjacent repair semantics.",
            "- The volatility/stress candidate adds mechanism diversity, but requires recent-window and one-window-dominance monitoring.",
            "- Active coverage is adequate for research but not yet sufficient for construction-layer assumptions.",
            "- Rebuilt primary representations need semantic preservation and rebuild-equivalence checks before any future integration work.",
            "",
            "## Candidates Needing Extra Monitoring",
            "",
            ", ".join(f"`{name}`" for name in extra_monitor) if extra_monitor else "No candidates require extra monitoring under this pass.",
            "",
            "## Missing Or Partial Inputs",
            "",
            pd.DataFrame(missing).to_markdown(index=False) if missing else "All current inventory panels were available or rebuildable from existing research artifacts.",
            "",
            "## Before Expansion v3",
            "",
            "Expansion v3 should wait for at least one additional inventory monitoring pass or a formal Inventory v2 governance update. The next monitoring package should add active-window drift, co-activation drift, and rebuild-equivalence checks as first-class artifacts.",
            "",
            "If Expansion v3 proceeds later, it should remain one-by-one and inventory-aware. New concepts should be required to fill a clear inventory gap and pass overlap checks against all three current candidates.",
            "",
            "## Monitoring Framework Definition",
            "",
            "Candidate-level monitoring dimensions:",
            "",
            "- rolling h20 IC and positive IC rate",
            "- rolling turnover",
            "- rolling active coverage",
            "- recent-window health",
            "- one-window dominance",
            "- WFV-style persistence and sign consistency drift",
            "- baseline similarity drift",
            "- semantic/state activation stability",
            "- candidate-specific guardrail status",
            "",
            "Inventory-level monitoring dimensions:",
            "",
            "- co-activation matrix",
            "- signal correlation matrix",
            "- inventory overlap map",
            "- shared regime/state dependence",
            "- horizon concentration",
            "- state concentration",
            "- turnover concentration",
            "- hidden mechanism clustering",
            "- recent-window fragility across inventory",
            "",
            "Monitoring classifications:",
            "",
            "- `HEALTHY_ACTIVE_RESEARCH`",
            "- `WATCH_MONITOR`",
            "- `DEGRADED_RESEARCH`",
            "- `REVIEW_FOR_DOWNGRADE`",
            "- `RETIREMENT_CANDIDATE`",
            "",
            "No classification changes production status. They are research governance labels only.",
        ]
    )
    NOTE_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    _ensure_dirs()
    panels, benchmark = load_inputs()
    signals, missing = _load_inventory_panels(panels, benchmark)
    artifacts, candidate_summary = _build_candidate_summary(signals, panels, benchmark, missing)
    guardrails = _guardrail_status(candidate_summary, CANDIDATES)
    coactivation = _coactivation_matrix(signals)
    corr = _correlation_matrix(signals)
    regime_overlap = _regime_overlap_summary(artifacts["daily_ics"], artifacts["scores"], panels["close"], benchmark)
    inventory_summary = _inventory_level_summary(coactivation, corr, candidate_summary, regime_overlap)

    candidate_summary.merge(
        guardrails[["signal_name", "monitoring_classification", "failed_guardrails", "caution_flags"]],
        on="signal_name",
        how="left",
    ).to_csv(OUT_DIR / "candidate_health_summary.csv", index=False)
    coactivation.to_csv(OUT_DIR / "coactivation_matrix.csv")
    corr.to_csv(OUT_DIR / "inventory_correlation_matrix.csv")
    guardrails.to_csv(OUT_DIR / "guardrail_status.csv", index=False)
    regime_overlap.to_csv(OUT_DIR / "regime_overlap_summary.csv", index=False)
    inventory_summary.to_csv(OUT_DIR / "inventory_level_summary.csv", index=False)
    artifacts["scores"].to_csv(OUT_DIR / "multi_horizon_scores.csv", index=False)
    artifacts["daily_ics"].to_csv(OUT_DIR / "daily_ic_by_signal_horizon.csv", index=False)
    artifacts["wfv"].to_csv(OUT_DIR / "wfv_style_summary.csv", index=False)
    artifacts["wfv_windows"].to_csv(OUT_DIR / "wfv_window_diagnostics.csv", index=False)
    artifacts["h20_wfv"].to_csv(OUT_DIR / "h20_wfv_monitor_summary.csv", index=False)
    artifacts["h20_wfv_windows"].to_csv(OUT_DIR / "h20_wfv_monitor_windows.csv", index=False)
    artifacts["similarity_detail"].to_csv(OUT_DIR / "inventory_similarity_detail.csv", index=False)
    pd.DataFrame(missing).to_csv(OUT_DIR / "missing_artifacts.csv", index=False)
    (OUT_DIR / "manifest.json").write_text(
        json.dumps(
            {
                "run_id": RUN_ID,
                "research_only": True,
                "production_logic_modified": False,
                "candidate_implementation": False,
                "discovery_or_validation_run": False,
                "inventory_candidates": [candidate.signal_name for candidate in CANDIDATES],
                "outputs": [
                    "candidate_health_summary.csv",
                    "coactivation_matrix.csv",
                    "inventory_correlation_matrix.csv",
                    "guardrail_status.csv",
                    "regime_overlap_summary.csv",
                    "inventory_level_summary.csv",
                    "manifest.json",
                ],
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )
    _write_note(candidate_summary, guardrails, coactivation, corr, regime_overlap, inventory_summary, missing)
    print(f"WROTE {OUT_DIR}")
    print(f"WROTE {NOTE_PATH}")
    print(guardrails[["signal_name", "monitoring_classification", "failed_guardrails", "caution_flags"]].to_string(index=False))


if __name__ == "__main__":
    main()
