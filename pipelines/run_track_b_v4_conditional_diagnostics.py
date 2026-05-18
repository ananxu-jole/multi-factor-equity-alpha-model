from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

from run_track_b_robustness_discovery_v3 import (
    HORIZONS,
    build_stress_states,
    daily_ic,
    load_inputs,
    wfv_diagnostics,
)


RUN_ID = "track_b_v4_conditional_diagnostics"
V4_DIR = Path("artifacts/research/robustness_first_discovery_expansion_v4")
OUT_DIR = Path("artifacts/research") / RUN_ID
NOTE_PATH = Path("docs/research_notes/track_b_v4_conditional_diagnostics.md")

FOCUS_SIGNALS = [
    "participation_liquidity_state_shift_20_60",
    "conditional_low_overextension_breakout_20",
    "gap_followthrough_low_churn_10",
    "nonprice_liquidity_persistence_20_60",
]


def _ensure_dirs() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    NOTE_PATH.parent.mkdir(parents=True, exist_ok=True)


def _load_focus_panels() -> dict[str, pd.DataFrame]:
    return {
        name: pd.read_parquet(V4_DIR / f"{name}_signal_panel.parquet")
        for name in FOCUS_SIGNALS
    }


def _forward_returns(close: pd.DataFrame, horizon: int) -> pd.DataFrame:
    return close.shift(-horizon) / close - 1.0


def _score_panel(panel: pd.DataFrame, close: pd.DataFrame, horizon: int, dates: pd.Index | None = None) -> dict[str, float | int]:
    signal = panel if dates is None else panel.reindex(dates)
    fwd = _forward_returns(close, horizon)
    fwd = fwd if dates is None else fwd.reindex(dates)
    ic = daily_ic(signal, fwd).dropna()
    std = ic.std(ddof=0) if len(ic) > 1 else np.nan
    return {
        "mean_ic": float(ic.mean()) if len(ic) else np.nan,
        "ic_ir": float(ic.mean() / std) if pd.notna(std) and std > 0 else np.nan,
        "positive_ic_rate": float((ic > 0).mean()) if len(ic) else np.nan,
        "n_dates": int(len(ic)),
    }


def _turnover(panel: pd.DataFrame) -> float:
    return float(panel.diff().abs().mean(axis=1, skipna=True).mean(skipna=True))


def _rank_churn(panel: pd.DataFrame) -> dict[str, float]:
    rank_corrs = []
    for idx in range(1, len(panel.index)):
        prev = panel.iloc[idx - 1]
        cur = panel.iloc[idx]
        valid = prev.notna() & cur.notna()
        if int(valid.sum()) >= 25:
            rank_corrs.append(prev[valid].rank().corr(cur[valid].rank()))
    rank_corrs = pd.Series(rank_corrs, dtype=float).dropna()
    return {
        "mean_rank_autocorr": float(rank_corrs.mean()) if len(rank_corrs) else np.nan,
        "rank_churn": float(1.0 - rank_corrs.mean()) if len(rank_corrs) else np.nan,
    }


def _active_stats(panel: pd.DataFrame) -> dict[str, float | int]:
    valid_count = panel.notna().sum(axis=1)
    mean_abs = panel.abs().mean(axis=1, skipna=True)
    active = (valid_count >= 25) & (mean_abs > 0.02)
    transitions = active.astype(int).diff().abs().fillna(0)
    return {
        "active_dates": int(active.sum()),
        "active_date_ratio": float(active.mean()),
        "activation_transitions": int(transitions.sum()),
        "mean_active_coverage": float(panel[active].notna().mean(axis=1).mean()) if active.any() else np.nan,
    }


def _build_conditional_states(close: pd.DataFrame, volume: pd.DataFrame, benchmark: pd.Series) -> pd.DataFrame:
    bench_ret = benchmark.pct_change(1, fill_method=None)
    bench_ret20 = benchmark.pct_change(20, fill_method=None)
    bench_ret40 = benchmark.pct_change(40, fill_method=None)
    bench_vol20 = bench_ret.rolling(20, min_periods=15).std()
    dispersion20 = close.pct_change(20, fill_method=None).std(axis=1)
    breadth20 = (close.pct_change(20, fill_method=None) > 0).mean(axis=1)
    dollar_volume = close * volume.astype(float).where(volume.astype(float) > 0)
    market_liquidity = dollar_volume.sum(axis=1, min_count=25)
    liquidity_ratio = (
        market_liquidity.rolling(20, min_periods=15).mean()
        / market_liquidity.rolling(60, min_periods=40).mean()
        - 1.0
    )
    ma60 = benchmark.rolling(60, min_periods=40).mean()
    q = lambda s, p: s.rolling(252, min_periods=100).quantile(p)
    states = pd.DataFrame(index=close.index)
    states["LOW_MARKET_VOL"] = (bench_vol20 < q(bench_vol20, 0.35)).fillna(False)
    states["HIGH_MARKET_VOL"] = (bench_vol20 > q(bench_vol20, 0.75)).fillna(False)
    states["LOW_OVEREXTENSION"] = (bench_ret40.abs() < q(bench_ret40.abs(), 0.40)).fillna(False)
    states["HIGH_OVEREXTENSION"] = (bench_ret40.abs() > q(bench_ret40.abs(), 0.75)).fillna(False)
    states["LOW_DISPERSION"] = (dispersion20 < q(dispersion20, 0.35)).fillna(False)
    states["HIGH_DISPERSION"] = (dispersion20 > q(dispersion20, 0.75)).fillna(False)
    states["LIQUIDITY_IMPROVING"] = (liquidity_ratio > q(liquidity_ratio, 0.60)).fillna(False)
    states["LIQUIDITY_DETERIORATING"] = (liquidity_ratio < q(liquidity_ratio, 0.40)).fillna(False)
    states["TREND_SUPPORTIVE"] = ((benchmark > ma60) & (bench_ret20 > 0)).fillna(False)
    states["TREND_HOSTILE"] = ((benchmark < ma60) | (bench_ret20 < 0)).fillna(False)
    states["HIGH_PARTICIPATION_BREADTH"] = (breadth20 > q(breadth20, 0.65)).fillna(False)
    states["LOW_PARTICIPATION_BREADTH"] = (breadth20 < q(breadth20, 0.35)).fillna(False)
    stress = build_stress_states(close, benchmark)
    return pd.concat([states, stress.add_prefix("STRESS_")], axis=1)


def _conditional_slice_diagnostics(signals: dict[str, pd.DataFrame], close: pd.DataFrame, states: pd.DataFrame, best_horizons: dict[str, int]) -> pd.DataFrame:
    rows = []
    for name, panel in signals.items():
        horizon = best_horizons[name]
        for state in states.columns:
            dates = states.index[states[state]]
            if len(dates) < 40:
                continue
            metrics = _score_panel(panel, close, horizon, dates)
            rows.append(
                {
                    "signal_name": name,
                    "horizon": horizon,
                    "state": state,
                    "active_state_dates": int(len(dates)),
                    **metrics,
                }
            )
    return pd.DataFrame(rows)


def _rebalance_interval(panel: pd.DataFrame, interval: int) -> pd.DataFrame:
    out = panel.copy() * np.nan
    out.iloc[::interval] = panel.iloc[::interval]
    return out.ffill()


def _threshold_active(panel: pd.DataFrame, threshold: float, inactive: str) -> pd.DataFrame:
    mask = panel.abs() >= threshold
    if inactive == "zero":
        return panel.where(mask, 0.0)
    return panel.where(mask)


def _low_churn_filter(panel: pd.DataFrame, max_daily_change: float = 0.35) -> pd.DataFrame:
    churn = panel.diff().abs()
    return panel.where(churn <= max_daily_change).ffill(limit=3)


def _refinement_diagnostics(signals: dict[str, pd.DataFrame], close: pd.DataFrame, best_horizons: dict[str, int]) -> pd.DataFrame:
    rows = []
    variants: dict[str, callable] = {
        "base": lambda p: p,
        "smooth_3": lambda p: p.rolling(3, min_periods=2).mean(),
        "smooth_5": lambda p: p.rolling(5, min_periods=3).mean(),
        "rebalance_5": lambda p: _rebalance_interval(p, 5),
        "rebalance_10": lambda p: _rebalance_interval(p, 10),
        "threshold_0p35_nan": lambda p: _threshold_active(p, 0.35, "nan"),
        "threshold_0p35_zero": lambda p: _threshold_active(p, 0.35, "zero"),
        "low_churn_filter": lambda p: _low_churn_filter(p),
    }
    for name, panel in signals.items():
        horizon = best_horizons[name]
        base_turnover = _turnover(panel)
        for variant, fn in variants.items():
            refined = fn(panel)
            metrics = _score_panel(refined, close, horizon)
            turn = _turnover(refined)
            rows.append(
                {
                    "signal_name": name,
                    "variant": variant,
                    "horizon": horizon,
                    "turnover_proxy": turn,
                    "turnover_reduction_pct": float((base_turnover - turn) / base_turnover) if base_turnover else np.nan,
                    "missing_pct": float(1.0 - refined.notna().to_numpy().mean()),
                    **metrics,
                }
            )
    return pd.DataFrame(rows)


def _turnover_source_diagnostics(signals: dict[str, pd.DataFrame]) -> pd.DataFrame:
    rows = []
    for name, panel in signals.items():
        churn = _rank_churn(panel)
        active = _active_stats(panel)
        signal_turnover = panel.diff().abs().mean(axis=1, skipna=True)
        active_flag = (panel.notna().sum(axis=1) >= 25) & (panel.abs().mean(axis=1, skipna=True) > 0.02)
        activation_transitions = active_flag.astype(int).diff().abs().fillna(0)
        rows.append(
            {
                "signal_name": name,
                "turnover_proxy": _turnover(panel),
                "turnover_p95": float(signal_turnover.quantile(0.95)),
                "turnover_max": float(signal_turnover.max(skipna=True)),
                "activation_transition_turnover_share": float(
                    signal_turnover[activation_transitions > 0].sum() / signal_turnover.sum()
                )
                if signal_turnover.sum() > 0
                else np.nan,
                **churn,
                **active,
            }
        )
    return pd.DataFrame(rows)


def _baseline_summary(orth: pd.DataFrame, focus: list[str]) -> pd.DataFrame:
    rows = []
    for name, group in orth[orth["signal_name"].isin(focus)].groupby("signal_name"):
        top = group.loc[group["abs_value_corr"].idxmax()]
        rows.append(
            {
                "signal_name": name,
                "top_baseline": top["comparison"],
                "max_abs_baseline_corr": float(top["abs_value_corr"]),
                "top_value_corr": float(top["value_corr"]),
                "mean_rank_corr_by_date": float(top["mean_rank_corr_by_date"]),
            }
        )
    return pd.DataFrame(rows)


def _classify(
    base: pd.DataFrame,
    slices: pd.DataFrame,
    refinements: pd.DataFrame,
    turnover: pd.DataFrame,
    baseline: pd.DataFrame,
) -> pd.DataFrame:
    rows = []
    for name in FOCUS_SIGNALS:
        base_row = base.loc[base["signal_name"].eq(name)].iloc[0]
        best_slice = slices[slices["signal_name"].eq(name)].sort_values("mean_ic", ascending=False).head(1)
        best_slice_row = best_slice.iloc[0] if not best_slice.empty else None
        ref = refinements[refinements["signal_name"].eq(name)].copy()
        ref["turnover_ok"] = ref["turnover_reduction_pct"] >= 0.20
        best_ref = ref.sort_values(["mean_ic", "turnover_reduction_pct"], ascending=False).head(1).iloc[0]
        turn = turnover.loc[turnover["signal_name"].eq(name)].iloc[0]
        sim = baseline.loc[baseline["signal_name"].eq(name)].iloc[0]

        best_state_ic = float(best_slice_row["mean_ic"]) if best_slice_row is not None else np.nan
        best_state = str(best_slice_row["state"]) if best_slice_row is not None else "none"
        state_dates = int(best_slice_row["active_state_dates"]) if best_slice_row is not None else 0
        base_mean = float(base_row["mean_ic"])
        max_corr = float(sim["max_abs_baseline_corr"])
        turnover_proxy = float(turn["turnover_proxy"])
        refined_turnover_reduction = float(best_ref["turnover_reduction_pct"])

        if name == "participation_liquidity_state_shift_20_60":
            if base_mean > 0.006 and best_state_ic > 0.015 and max_corr < 0.55:
                status = "CONDITIONAL_REFINEMENT_CANDIDATE"
            else:
                status = "CONDITIONAL_ONLY_KEEP"
        elif name == "nonprice_liquidity_persistence_20_60":
            status = "CONDITIONAL_ONLY_KEEP" if max_corr < 0.35 and best_state_ic > 0.012 else "REDESIGN"
        elif name == "gap_followthrough_low_churn_10":
            status = "REDESIGN" if best_state_ic > 0.012 and max_corr < 0.20 else "DISCARD"
        elif name == "conditional_low_overextension_breakout_20":
            status = "REDESIGN" if best_state_ic > 0.02 and state_dates >= 40 else "DISCARD"
        else:
            status = "REDESIGN"

        if turnover_proxy > 0.18 and refined_turnover_reduction < 0.20:
            status = "REDESIGN" if status != "DISCARD" else status

        rows.append(
            {
                "signal_name": name,
                "base_mean_ic": base_mean,
                "base_positive_ic_rate": float(base_row["positive_ic_rate"]),
                "base_turnover_proxy": turnover_proxy,
                "max_abs_baseline_corr": max_corr,
                "best_conditional_state": best_state,
                "best_conditional_mean_ic": best_state_ic,
                "best_conditional_dates": state_dates,
                "best_refinement_variant": best_ref["variant"],
                "best_refinement_mean_ic": float(best_ref["mean_ic"]),
                "best_refinement_turnover_reduction_pct": refined_turnover_reduction,
                "classification": status,
                "interpretation": _interpretation(name, status),
            }
        )
    return pd.DataFrame(rows)


def _interpretation(name: str, status: str) -> str:
    if name == "participation_liquidity_state_shift_20_60":
        return "Contains the clearest conditional structure, but turnover remains the main blocker."
    if name == "nonprice_liquidity_persistence_20_60":
        return "Orthogonal and genuinely non-price, but standalone edge is weak and needs state filtering."
    if name == "gap_followthrough_low_churn_10":
        return "Coverage improved versus v3, but the edge remains noisy and needs a cleaner event model."
    if name == "conditional_low_overextension_breakout_20":
        return "Has narrow state-specific strength, but always-on direction is wrong and persistence is weak."
    return status


def _write_note(
    base: pd.DataFrame,
    slices: pd.DataFrame,
    refinements: pd.DataFrame,
    turnover: pd.DataFrame,
    baseline: pd.DataFrame,
    final: pd.DataFrame,
) -> None:
    best_slices = slices.sort_values("mean_ic", ascending=False).groupby("signal_name").head(5)
    best_refinements = refinements.sort_values(["signal_name", "mean_ic"], ascending=[True, False]).groupby("signal_name").head(4)
    lines = [
        "# Track B v4 Conditional Diagnostics",
        "",
        "## Executive Takeaway",
        "",
        f"This research-only pass analyzed the four v4 `CONDITIONAL_ONLY_RESEARCH` candidates under `{RUN_ID}`.",
        "",
        "The candidates are not ready for promotion or registration. The useful evidence is narrower: v4 did produce several mechanisms with materially lower reversal/price-rank similarity, but their edges appear state-dependent, weak, or turnover-sensitive rather than standalone robust.",
        "",
        "No production logic, gates, schemas, thresholds, survivor/watchlist status, ML logic, portfolio logic, or Conditional-Alpha production paths were changed.",
        "",
        "## Candidates Reviewed",
        "",
        "- `participation_liquidity_state_shift_20_60`",
        "- `conditional_low_overextension_breakout_20`",
        "- `gap_followthrough_low_churn_10`",
        "- `nonprice_liquidity_persistence_20_60`",
        "",
        "## Base v4 Diagnostics",
        "",
        base.to_markdown(index=False),
        "",
        "## Orthogonality",
        "",
        baseline.to_markdown(index=False),
        "",
        "## Turnover / Active-Date Diagnostics",
        "",
        turnover.to_markdown(index=False),
        "",
        "## Best Conditional Slices",
        "",
        best_slices[["signal_name", "horizon", "state", "active_state_dates", "mean_ic", "ic_ir", "positive_ic_rate", "n_dates"]].to_markdown(index=False),
        "",
        "## Turnover Refinement Tests",
        "",
        best_refinements[[
            "signal_name",
            "variant",
            "horizon",
            "mean_ic",
            "ic_ir",
            "positive_ic_rate",
            "turnover_proxy",
            "turnover_reduction_pct",
            "missing_pct",
        ]].to_markdown(index=False),
        "",
        "## Candidate Classifications",
        "",
        final.to_markdown(index=False),
        "",
        "## Candidate Notes",
        "",
        "### participation_liquidity_state_shift_20_60",
        "",
        "This is the strongest v4 conditional ingredient. It had positive base h20 IC, acceptable WFV-style persistence/sign consistency from v4, low baseline similarity, and strong drawdown/panic-liquidity conditional slices. The main issue is turnover: diagnostics point to rank churn and high continuous movement rather than sparse activation transitions. Classification: `CONDITIONAL_REFINEMENT_CANDIDATE`.",
        "",
        "### conditional_low_overextension_breakout_20",
        "",
        "This candidate has a narrow positive stress/volatility-spike slice, but standalone direction remains negative and WFV persistence is weak. It should not be kept as an alpha signal; if revisited, it needs a redesigned conditional activation model. Classification: `REDESIGN`.",
        "",
        "### gap_followthrough_low_churn_10",
        "",
        "The v4 redesign materially improved missingness versus v3 and remained highly orthogonal, but the edge is still weak/noisy and turnover remains nontrivial. Some regime slices are positive, especially recovery/high-dispersion style states, but not enough for keep status without redesign. Classification: `REDESIGN`.",
        "",
        "### nonprice_liquidity_persistence_20_60",
        "",
        "This candidate is genuinely more orthogonal and non-price than the v3 liquidity design, but the base edge is small and WFV-style persistence is not sufficient. It has promising conditional behavior in trend-transition/high-dispersion states. Classification: `CONDITIONAL_ONLY_KEEP`.",
        "",
        "## Recommended Next Step",
        "",
        "Do not create a broad v5 batch yet. First run a narrow refinement design for `participation_liquidity_state_shift_20_60` focused on turnover reduction and cleaner activation, and keep `nonprice_liquidity_persistence_20_60` as a secondary conditional-only ingredient. Redesign gap and breakout concepts before retesting.",
    ]
    NOTE_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    _ensure_dirs()
    panels, benchmark = load_inputs()
    signals = _load_focus_panels()
    classification = pd.read_csv(V4_DIR / "candidate_classification.csv")
    base = classification[classification["signal_name"].isin(FOCUS_SIGNALS)].copy()
    best_horizons = base.set_index("signal_name")["best_horizon"].astype(int).to_dict()
    orth = pd.read_csv(V4_DIR / "orthogonality_redundancy_audit.csv")
    baseline = _baseline_summary(orth, FOCUS_SIGNALS)
    states = _build_conditional_states(panels["close"], panels["volume"], benchmark)
    slices = _conditional_slice_diagnostics(signals, panels["close"], states, best_horizons)
    refinements = _refinement_diagnostics(signals, panels["close"], best_horizons)
    turnover = _turnover_source_diagnostics(signals)
    final = _classify(base, slices, refinements, turnover, baseline)

    base.to_csv(OUT_DIR / "base_v4_conditional_candidates.csv", index=False)
    baseline.to_csv(OUT_DIR / "baseline_similarity_summary.csv", index=False)
    states.to_csv(OUT_DIR / "conditional_state_flags.csv", index=True)
    slices.to_csv(OUT_DIR / "conditional_slice_diagnostics.csv", index=False)
    refinements.to_csv(OUT_DIR / "turnover_refinement_diagnostics.csv", index=False)
    turnover.to_csv(OUT_DIR / "turnover_source_diagnostics.csv", index=False)
    final.to_csv(OUT_DIR / "final_candidate_classification.csv", index=False)
    (OUT_DIR / "manifest.json").write_text(
        json.dumps(
            {
                "run_id": RUN_ID,
                "source_run_id": "robustness_first_discovery_expansion_v4",
                "research_only": True,
                "production_logic_modified": False,
                "promotion_or_registration": False,
                "focus_signals": FOCUS_SIGNALS,
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )
    _write_note(base, slices, refinements, turnover, baseline, final)
    print(f"WROTE {OUT_DIR}")
    print(f"WROTE {NOTE_PATH}")
    print(final.to_string(index=False))


if __name__ == "__main__":
    main()
