from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

from run_track_b_robustness_discovery_v3 import (
    baseline_panels,
    build_stress_states,
    load_inputs,
    orthogonality,
    score_signals,
    stress_attribution,
    structural_summary,
    wfv_diagnostics,
    _clean_panel,
    _rank_cs,
    _winsor,
    _zscore_ts,
)
from run_track_b_robustness_discovery_v4 import _cs_neutralize


RUN_ID = "track_b_v5_focused_discovery"
OUT_DIR = Path("artifacts/research") / RUN_ID
NOTE_PATH = Path("docs/research_notes/track_b_v5_focused_discovery.md")
CONCEPT_NOTE = Path("docs/research_notes/track_b_v5_concept_screening.md")
CLOSEOUT_NOTE = Path("docs/research_notes/track_b_conditional_alpha_cycle_closeout.md")
V4_DIR = Path("artifacts/research/robustness_first_discovery_expansion_v4")
INTEGRATION_DIR = Path("artifacts/research/participation_liquidity_integration_review_v1")


CANDIDATES: list[dict[str, str]] = [
    {
        "signal_name": "participation_breadth_repair_under_hostile_trend",
        "family": "participation_breadth_transition",
        "mechanism_thesis": "Participation breadth repair during hostile trend states.",
        "state_transition_logic": "Activates when the benchmark trend is hostile and market breadth is repairing.",
        "non_reversal_rationale": "Uses participation repair under hostile state rather than fading a large prior price move.",
        "non_momentum_rationale": "Controls price extension and neutralizes 20-day return rank instead of chasing mature leaders.",
        "expected_activation_state": "TREND_HOSTILE plus breadth repair.",
        "expected_horizon": "h10-h20",
        "expected_turnover_profile": "Medium-low after rank persistence and smoothing.",
    },
    {
        "signal_name": "nonprice_liquidity_repair_without_price_extension",
        "family": "nonprice_liquidity_transition",
        "mechanism_thesis": "Non-price liquidity repair with explicit low-extension control.",
        "state_transition_logic": "Targets securities with improving liquidity while price extension remains modest.",
        "non_reversal_rationale": "Does not require prior price underperformance or abnormal price shock.",
        "non_momentum_rationale": "Liquidity repair is neutralized against recent return rank and penalizes price extension.",
        "expected_activation_state": "Improving liquidity with low-to-moderate price extension.",
        "expected_horizon": "h10-h20",
        "expected_turnover_profile": "Medium-low after smoothing.",
    },
    {
        "signal_name": "stress_to_normalization_participation_repair",
        "family": "stress_normalization_participation",
        "mechanism_thesis": "Participation and liquidity repair as stress begins to normalize.",
        "state_transition_logic": "Activates after recent stress when breadth/liquidity repair and volatility normalization appear.",
        "non_reversal_rationale": "Requires stress-state transition and participation repair rather than simply buying prior losers.",
        "non_momentum_rationale": "Avoids mature post-stress leaders by controlling price extension and neutralizing return rank.",
        "expected_activation_state": "Recent drawdown/volatility stress with improving participation or liquidity.",
        "expected_horizon": "h10-h20",
        "expected_turnover_profile": "Medium with explicit state activation.",
    },
]


def _ensure_dirs() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    NOTE_PATH.parent.mkdir(parents=True, exist_ok=True)


def _market_state_panel(series: pd.Series, columns: pd.Index) -> pd.DataFrame:
    return pd.DataFrame(
        np.repeat(series.astype(float).values[:, None], len(columns), axis=1),
        index=series.index,
        columns=columns,
    )


def _rank_series_to_01(series: pd.Series) -> pd.Series:
    return series.rank(pct=True).fillna(0.5)


def _rebalance_interval(panel: pd.DataFrame, interval: int) -> pd.DataFrame:
    out = panel.copy() * np.nan
    out.iloc[::interval] = panel.iloc[::interval]
    return out.ffill()


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


def _build_market_states(close: pd.DataFrame, volume: pd.DataFrame, benchmark: pd.Series) -> pd.DataFrame:
    bench_ret = benchmark.pct_change(1, fill_method=None)
    bench_ret20 = benchmark.pct_change(20, fill_method=None)
    bench_ret40 = benchmark.pct_change(40, fill_method=None)
    bench_ma60 = benchmark.rolling(60, min_periods=40).mean()
    bench_vol20 = bench_ret.rolling(20, min_periods=15).std()
    bench_vol60 = bench_ret.rolling(60, min_periods=40).std()
    breadth20 = (close.pct_change(20, fill_method=None) > 0).mean(axis=1)
    breadth10 = (close.pct_change(10, fill_method=None) > 0).mean(axis=1)
    breadth_repair = breadth10 - breadth20
    dollar_volume = close * volume.astype(float).where(volume.astype(float) > 0)
    market_liquidity = dollar_volume.sum(axis=1, min_count=25)
    liquidity20 = market_liquidity.rolling(20, min_periods=15).mean()
    liquidity60 = market_liquidity.rolling(60, min_periods=40).mean()
    liquidity_repair = liquidity20 / liquidity60 - 1.0
    drawdown = benchmark / benchmark.cummax() - 1.0
    stress = build_stress_states(close, benchmark)
    q = lambda s, p: s.rolling(252, min_periods=100).quantile(p)

    states = pd.DataFrame(index=close.index)
    states["TREND_HOSTILE"] = ((benchmark < bench_ma60) | (bench_ret20 < 0)).fillna(False)
    states["WEAK_BREADTH"] = (breadth20 < q(breadth20, 0.35)).fillna(False)
    states["BREADTH_REPAIR"] = (breadth_repair > q(breadth_repair, 0.60)).fillna(False)
    states["LIQUIDITY_REPAIR"] = (liquidity_repair > q(liquidity_repair, 0.60)).fillna(False)
    states["LOW_EXTENSION_MARKET"] = (bench_ret40.abs() < q(bench_ret40.abs(), 0.60)).fillna(False)
    states["VOL_NORMALIZING"] = ((bench_vol20 < bench_vol60) & (bench_vol20.diff(10) < 0)).fillna(False)
    states["RECENT_STRESS"] = (
        stress[["drawdown_acceleration", "volatility_spike", "panic_liquidity_stress"]]
        .rolling(20, min_periods=1)
        .max()
        .max(axis=1)
        .astype(bool)
    )
    states["DRAWDOWN"] = (drawdown < -0.05).fillna(False)
    states["PARTICIPATION_REPAIR_HOSTILE"] = (
        states["TREND_HOSTILE"] & states["BREADTH_REPAIR"]
    ).fillna(False)
    states["STRESS_NORMALIZATION"] = (
        states["RECENT_STRESS"] & (states["BREADTH_REPAIR"] | states["LIQUIDITY_REPAIR"]) & states["VOL_NORMALIZING"]
    ).fillna(False)
    return states


def build_candidate_panels(panels: dict[str, pd.DataFrame], benchmark: pd.Series) -> tuple[dict[str, pd.DataFrame], pd.DataFrame]:
    close = panels["close"]
    volume = panels["volume"].astype(float).where(panels["volume"].astype(float) > 0)

    ret1 = close.pct_change(1, fill_method=None)
    ret10 = close.pct_change(10, fill_method=None)
    ret20 = close.pct_change(20, fill_method=None)
    ret40 = close.pct_change(40, fill_method=None)
    ret20_rank = _rank_cs(ret20)

    participation_10 = (ret1 > 0).rolling(10, min_periods=7).mean()
    participation_20 = (ret1 > 0).rolling(20, min_periods=15).mean()
    participation_40 = (ret1 > 0).rolling(40, min_periods=25).mean()
    participation_repair = participation_10 - participation_40
    participation_stability = -participation_20.rolling(20, min_periods=12).std()

    dollar_volume = close * volume
    dollar_liquidity_10 = dollar_volume.rolling(10, min_periods=7).mean()
    dollar_liquidity_20 = dollar_volume.rolling(20, min_periods=15).mean()
    dollar_liquidity_60 = dollar_volume.rolling(60, min_periods=40).mean()
    liquidity_repair = _winsor(dollar_liquidity_20 / dollar_liquidity_60 - 1.0, -3, 3)
    liquidity_repair_fast = _winsor(dollar_liquidity_10 / dollar_liquidity_60 - 1.0, -3, 3)
    liquidity_stability = -_zscore_ts(dollar_volume.pct_change(1, fill_method=None).abs(), 40)

    modest_extension = (1.0 - ret20_rank.abs()).clip(lower=0)
    low_extension = (ret40.abs().rank(axis=1, pct=True) < 0.70).astype(float)

    states = _build_market_states(close, volume, benchmark)
    hostile_repair_gate = _market_state_panel(states["PARTICIPATION_REPAIR_HOSTILE"], close.columns)
    liquidity_gate = _market_state_panel(states["LIQUIDITY_REPAIR"], close.columns)
    stress_norm_gate = _market_state_panel(states["STRESS_NORMALIZATION"], close.columns)

    participation_repair_raw = _rank_cs(
        (
            participation_repair.clip(lower=0)
            * (1.0 + participation_stability.rank(axis=1, pct=True).fillna(0.5))
            * modest_extension
        ).rolling(5, min_periods=3).mean()
    )
    participation_repair_signal = _rank_cs(_cs_neutralize(participation_repair_raw, ret20_rank))
    participation_repair_signal = _rank_cs(_rebalance_interval(participation_repair_signal * hostile_repair_gate, 10))

    liquidity_repair_raw = _rank_cs(
        (
            liquidity_repair.clip(lower=0)
            * liquidity_repair_fast.clip(lower=0)
            * (1.0 + liquidity_stability.rank(axis=1, pct=True).fillna(0.5))
            * low_extension
        ).rolling(5, min_periods=3).mean()
    )
    liquidity_repair_signal = _rank_cs(_cs_neutralize(liquidity_repair_raw, ret20_rank))
    liquidity_repair_signal = _rank_cs(liquidity_repair_signal.rolling(5, min_periods=3).mean() * liquidity_gate)

    stress_repair_raw = _rank_cs(
        (
            participation_repair.clip(lower=0)
            * liquidity_repair.clip(lower=0)
            * (1.0 - ret10.rank(axis=1, pct=True).sub(0.5).abs() * 2.0).clip(lower=0)
        ).rolling(5, min_periods=3).mean()
    )
    stress_repair_signal = _rank_cs(_cs_neutralize(stress_repair_raw, ret20_rank))
    stress_repair_signal = _rank_cs(_rebalance_interval(stress_repair_signal * stress_norm_gate, 10))

    signals = {
        "participation_breadth_repair_under_hostile_trend": participation_repair_signal,
        "nonprice_liquidity_repair_without_price_extension": liquidity_repair_signal,
        "stress_to_normalization_participation_repair": stress_repair_signal,
    }
    return {name: _clean_panel(panel) for name, panel in signals.items()}, states


def reference_panels(signals: dict[str, pd.DataFrame], panels: dict[str, pd.DataFrame], benchmark: pd.Series) -> dict[str, pd.DataFrame]:
    refs = baseline_panels(signals, panels, benchmark)
    first = next(iter(signals.values()))
    prior_path = V4_DIR / "participation_liquidity_state_shift_20_60_signal_panel.parquet"
    if prior_path.exists():
        refs["prior_participation_liquidity_state_shift_20_60"] = pd.read_parquet(prior_path).reindex(
            index=first.index,
            columns=first.columns,
        )
    fixed_path = INTEGRATION_DIR / "fixed_variant_integration_review.csv"
    if fixed_path.exists():
        # Metric-only reference marker. Actual fixed-variant panels were produced in validation artifacts, not this review table.
        refs["prior_integration_review_metric_reference"] = refs["prior_participation_liquidity_state_shift_20_60"]
    return refs


def active_coverage_summary(signals: dict[str, pd.DataFrame]) -> pd.DataFrame:
    rows = []
    for name, panel in signals.items():
        rows.append({"signal_name": name, **_active_stats(panel)})
    return pd.DataFrame(rows)


def state_attribution(
    daily_ics: pd.DataFrame,
    scores: pd.DataFrame,
    states: pd.DataFrame,
) -> pd.DataFrame:
    best = scores.loc[scores["is_best_horizon"], ["signal_name", "best_horizon"]].set_index("signal_name")["best_horizon"]
    rows = []
    for signal_name, horizon in best.items():
        series = daily_ics[
            daily_ics["signal_name"].eq(signal_name) & daily_ics["horizon"].eq(horizon)
        ].set_index("Date")["ic"]
        for state in states.columns:
            dates = states.index[states[state]]
            sample = series.reindex(dates).dropna()
            std = sample.std(ddof=0) if len(sample) > 1 else np.nan
            rows.append(
                {
                    "signal_name": signal_name,
                    "horizon": int(horizon),
                    "state": state,
                    "n_dates": int(len(sample)),
                    "mean_ic": float(sample.mean()) if len(sample) else np.nan,
                    "ic_ir": float(sample.mean() / std) if pd.notna(std) and std > 0 else np.nan,
                    "positive_ic_rate": float((sample > 0).mean()) if len(sample) else np.nan,
                }
            )
    return pd.DataFrame(rows)


def _max_corr_table(orth: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for name, group in orth.groupby("signal_name"):
        group = group.dropna(subset=["abs_value_corr"])
        if group.empty:
            continue
        top = group.loc[group["abs_value_corr"].idxmax()]
        prior = group[group["comparison"].str.contains("participation_liquidity_state_shift_20_60", na=False)]
        prior_corr = float(prior["abs_value_corr"].max()) if not prior.empty else np.nan
        reversal = group[group["comparison"].isin(["unweighted_reversal_20", "plain_smoothed_reversal_20"])]
        momentum = group[group["comparison"].isin(["plain_momentum_60"])]
        rows.append(
            {
                "signal_name": name,
                "top_comparison": top["comparison"],
                "max_abs_baseline_corr": float(top["abs_value_corr"]),
                "prior_participation_liquidity_corr": prior_corr,
                "max_reversal_corr": float(reversal["abs_value_corr"].max()) if not reversal.empty else np.nan,
                "max_momentum_corr": float(momentum["abs_value_corr"].max()) if not momentum.empty else np.nan,
            }
        )
    return pd.DataFrame(rows)


def classify_candidates(
    structural: pd.DataFrame,
    scores: pd.DataFrame,
    wfv: pd.DataFrame,
    stress: pd.DataFrame,
    orth_summary: pd.DataFrame,
    active: pd.DataFrame,
) -> pd.DataFrame:
    best = scores.loc[scores["is_best_horizon"]].copy()
    stress_counts = (
        stress.groupby("signal_name")["mean_ic"]
        .agg(positive_regime_count=lambda s: int((s > 0.004).sum()), best_regime_ic="max")
        .reset_index()
    )
    summary = (
        best.merge(structural, on="signal_name", how="left")
        .merge(wfv, on=["signal_name", "horizon"], how="left")
        .merge(stress_counts, on="signal_name", how="left")
        .merge(orth_summary, on="signal_name", how="left")
        .merge(active, on="signal_name", how="left")
    )
    rows = []
    for _, row in summary.iterrows():
        issues = []
        if row["missing_pct"] > 0.25:
            issues.append("high_missingness")
        if row["turnover_proxy"] > 0.12:
            issues.append("high_turnover")
        if row["mean_ic"] < 0:
            issues.append("direction_mismatch")
        if row["abs_mean_ic"] < 0.006:
            issues.append("weak_best_horizon_ic")
        if row["positive_ic_rate"] < 0.52:
            issues.append("weak_positive_ic_rate")
        if pd.notna(row.get("persistence")) and row["persistence"] < 0.75:
            issues.append("weak_wfv_persistence")
        if pd.notna(row.get("sign_consistency")) and row["sign_consistency"] < 0.75:
            issues.append("weak_wfv_sign_consistency")
        if row.get("max_reversal_corr", 0) > 0.55:
            issues.append("reversal_similarity_risk")
        if row.get("max_momentum_corr", 0) > 0.55:
            issues.append("momentum_similarity_risk")
        if row.get("prior_participation_liquidity_corr", 0) > 0.65:
            issues.append("too_close_to_prior_participation_liquidity")
        if row.get("active_date_ratio", 1) < 0.15:
            issues.append("sparse_activation")

        if (
            row["mean_ic"] > 0.012
            and row["positive_ic_rate"] >= 0.54
            and row.get("persistence", 0) >= 0.75
            and row.get("sign_consistency", 0) >= 0.75
            and row["turnover_proxy"] <= 0.12
            and row.get("max_reversal_corr", 1) <= 0.55
            and row.get("max_momentum_corr", 1) <= 0.55
            and row.get("prior_participation_liquidity_corr", 1) <= 0.65
            and row.get("active_date_ratio", 0) >= 0.20
        ):
            status = "CANDIDATE_FOR_CONDITIONAL_VALIDATION"
        elif (
            row["mean_ic"] > 0.006
            and row.get("best_regime_ic", 0) > 0.012
            and row.get("max_reversal_corr", 1) <= 0.60
            and row.get("active_date_ratio", 0) >= 0.15
        ):
            status = "CONDITIONAL_REFINEMENT_CANDIDATE"
        elif (
            row.get("positive_regime_count", 0) >= 2
            and row.get("max_reversal_corr", 1) <= 0.65
            and row.get("active_date_ratio", 0) >= 0.12
        ):
            status = "CONDITIONAL_ONLY_RESEARCH"
        else:
            status = "REJECT_RESEARCH"

        rows.append(
            {
                "signal_name": row["signal_name"],
                "family": _family_for(row["signal_name"]),
                "best_horizon": int(row["horizon"]),
                "mean_ic": row["mean_ic"],
                "abs_mean_ic": row["abs_mean_ic"],
                "ic_ir": row["ic_ir"],
                "positive_ic_rate": row["positive_ic_rate"],
                "turnover_proxy": row["turnover_proxy"],
                "missing_pct": row["missing_pct"],
                "active_date_ratio": row.get("active_date_ratio"),
                "max_abs_baseline_corr": row.get("max_abs_baseline_corr"),
                "prior_participation_liquidity_corr": row.get("prior_participation_liquidity_corr"),
                "max_reversal_corr": row.get("max_reversal_corr"),
                "max_momentum_corr": row.get("max_momentum_corr"),
                "wfv_persistence": row.get("persistence"),
                "wfv_sign_consistency": row.get("sign_consistency"),
                "positive_regime_count": int(row.get("positive_regime_count", 0) or 0),
                "best_regime_ic": row.get("best_regime_ic"),
                "status": status,
                "review_issues": "; ".join(issues) if issues else "none",
            }
        )
    return pd.DataFrame(rows).sort_values(["status", "abs_mean_ic"], ascending=[True, False])


def _family_for(signal_name: str) -> str:
    for spec in CANDIDATES:
        if spec["signal_name"] == signal_name:
            return spec["family"]
    return "unknown"


def write_note(
    registry: pd.DataFrame,
    structural: pd.DataFrame,
    scores: pd.DataFrame,
    wfv: pd.DataFrame,
    stress: pd.DataFrame,
    state_attr: pd.DataFrame,
    orth_summary: pd.DataFrame,
    active: pd.DataFrame,
    decisions: pd.DataFrame,
) -> None:
    best = scores.loc[scores["is_best_horizon"]].sort_values("abs_mean_ic", ascending=False)
    h20 = scores[scores["horizon"].eq(20)].sort_values("mean_ic", ascending=False)
    state_best = state_attr.sort_values("mean_ic", ascending=False).groupby("signal_name").head(5)
    status_counts = decisions["status"].value_counts().to_dict()
    advanced = decisions[decisions["status"].isin(["CONDITIONAL_REFINEMENT_CANDIDATE", "CANDIDATE_FOR_CONDITIONAL_VALIDATION"])]
    lines = [
        "# Track B v5 Focused Discovery",
        "",
        "## Executive Takeaway",
        "",
        f"This research-only run implemented the three highest-priority concepts from the Track B v5 concept screen under `{RUN_ID}`.",
        "",
        "This was a small focused batch, not broad discovery. It did not productionize `participation_liquidity_state_shift_20_60`, register new signals, promote survivor/watchlist state, alter gates or schemas, change thresholds, use ML, modify portfolio logic, or wire production Conditional-Alpha paths.",
        "",
        f"Candidates tested: {len(registry)}",
        f"Status counts: `{json.dumps(status_counts, sort_keys=True)}`",
        "",
        "## Source Notes",
        "",
        f"- Concept screen: `{CONCEPT_NOTE}`",
        f"- Track B closeout: `{CLOSEOUT_NOTE}`",
        "- Prior governed candidate remains frozen: `participation_liquidity_state_shift_20_60` -> `CONDITIONAL_ALPHA_REVIEW_READY_WITH_GUARDRAILS`.",
        "",
        "## Candidate Set",
        "",
        registry.to_markdown(index=False),
        "",
        "## Structural Quality And Active Coverage",
        "",
        structural.merge(active, on="signal_name", how="left")[
            [
                "signal_name",
                "missing_pct",
                "finite_pct",
                "date_coverage",
                "turnover_proxy",
                "turnover_p95",
                "active_date_ratio",
                "activation_transitions",
                "mean_active_coverage",
            ]
        ].to_markdown(index=False),
        "",
        "## Multi-Horizon IC",
        "",
        scores[["signal_name", "horizon", "mean_ic", "abs_mean_ic", "ic_ir", "positive_ic_rate", "n_dates", "is_best_horizon"]].to_markdown(index=False),
        "",
        "## h20 Behavior",
        "",
        h20[["signal_name", "mean_ic", "abs_mean_ic", "ic_ir", "positive_ic_rate", "n_dates"]].to_markdown(index=False),
        "",
        "## WFV-Style Diagnostics",
        "",
        wfv.to_markdown(index=False) if not wfv.empty else "WFV-style diagnostics were unavailable.",
        "",
        "## Orthogonality / Redundancy",
        "",
        orth_summary.to_markdown(index=False),
        "",
        "## Stress / Regime Attribution",
        "",
        stress.sort_values("mean_ic", ascending=False).groupby("signal_name").head(4)[
            ["signal_name", "horizon", "state", "n_dates", "mean_ic", "ic_ir", "positive_ic_rate"]
        ].to_markdown(index=False),
        "",
        "## Concept State Attribution",
        "",
        state_best[["signal_name", "horizon", "state", "n_dates", "mean_ic", "ic_ir", "positive_ic_rate"]].to_markdown(index=False),
        "",
        "## Candidate Decisions",
        "",
        decisions.to_markdown(index=False),
        "",
        "## Interpretation",
        "",
    ]
    if advanced.empty:
        lines.extend(
            [
                "No v5 concept reached `CONDITIONAL_REFINEMENT_CANDIDATE` or `CANDIDATE_FOR_CONDITIONAL_VALIDATION` status. Treat this as useful negative evidence and do not broaden the batch reflexively.",
                "",
            ]
        )
    else:
        lines.extend(
            [
                "At least one v5 concept produced enough conditional structure for follow-up research. Any follow-up should remain narrow and should not reuse this first pass as permission for broad parameter search.",
                "",
                advanced.to_markdown(index=False),
                "",
            ]
        )
    lines.extend(
        [
            "## Concept Notes",
            "",
            "### participation_breadth_repair_under_hostile_trend",
            "",
            "This concept tests whether participation repair inside hostile trend states can extend the successful Track B state-transition pattern. It is closest to the prior governed candidate but intentionally emphasizes breadth repair rather than the original liquidity/participation state shift.",
            "",
            "### nonprice_liquidity_repair_without_price_extension",
            "",
            "This concept tests whether non-price liquidity repair can stand farther away from price-rank and reversal baselines. It should be rejected or redesigned if it behaves like generic liquidity/size exposure or converges back to the prior participation/liquidity signal.",
            "",
            "### stress_to_normalization_participation_repair",
            "",
            "This concept tests whether participation repair after stress normalization is a distinct conditional mechanism rather than a delayed rebound/reversal proxy. Sparse activation and crisis-window overfit are the key risks.",
            "",
            "## Recommended Next Step",
            "",
            _recommendation(decisions),
        ]
    )
    NOTE_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _recommendation(decisions: pd.DataFrame) -> str:
    validation = decisions[decisions["status"].eq("CANDIDATE_FOR_CONDITIONAL_VALIDATION")]
    refinement = decisions[decisions["status"].eq("CONDITIONAL_REFINEMENT_CANDIDATE")]
    if not validation.empty:
        names = ", ".join(f"`{name}`" for name in validation["signal_name"])
        return f"Run a narrow conditional-validation planning pass only for {names}. Do not broaden v5 or productionize anything."
    if not refinement.empty:
        names = ", ".join(f"`{name}`" for name in refinement["signal_name"])
        return f"Run a focused refinement diagnostics pass only for {names}; keep parameter exploration small and pre-declared."
    keep = decisions[decisions["status"].eq("CONDITIONAL_ONLY_RESEARCH")]
    if not keep.empty:
        names = ", ".join(f"`{name}`" for name in keep["signal_name"])
        return f"Keep {names} as conditional-only research ingredients. Do not refine until a stronger state thesis is documented."
    return "Reject the v5 first wave as useful negative evidence and return to concept design before implementing more candidates."


def main() -> None:
    _ensure_dirs()
    panels, benchmark = load_inputs()
    signals, states = build_candidate_panels(panels, benchmark)
    registry = pd.DataFrame(CANDIDATES)
    registry["run_id"] = RUN_ID
    registry["research_status"] = "TRACK_B_V5_RESEARCH_ONLY"

    structural = structural_summary(signals)
    scores, daily_ics = score_signals(signals, panels["close"])
    stress_states = build_stress_states(panels["close"], benchmark)
    stress = stress_attribution(daily_ics, scores, stress_states)
    state_attr = state_attribution(daily_ics, scores, states)
    wfv_summary, wfv_windows = wfv_diagnostics(daily_ics, scores)
    refs = reference_panels(signals, panels, benchmark)
    orth = orthogonality(signals, refs)
    orth_summary = _max_corr_table(orth)
    active = active_coverage_summary(signals)
    decisions = classify_candidates(structural, scores, wfv_summary, stress, orth_summary, active)

    registry.to_csv(OUT_DIR / "candidate_registry.csv", index=False)
    structural.to_csv(OUT_DIR / "structural_quality_summary.csv", index=False)
    scores.to_csv(OUT_DIR / "multi_horizon_scoring.csv", index=False)
    daily_ics.to_csv(OUT_DIR / "daily_ic_by_signal_horizon.csv", index=False)
    states.to_csv(OUT_DIR / "market_state_flags.csv", index=True)
    stress.to_csv(OUT_DIR / "stress_regime_attribution.csv", index=False)
    state_attr.to_csv(OUT_DIR / "concept_state_attribution.csv", index=False)
    wfv_summary.to_csv(OUT_DIR / "wfv_style_summary.csv", index=False)
    wfv_windows.to_csv(OUT_DIR / "wfv_window_diagnostics.csv", index=False)
    orth.to_csv(OUT_DIR / "orthogonality_redundancy_audit.csv", index=False)
    orth_summary.to_csv(OUT_DIR / "orthogonality_summary.csv", index=False)
    active.to_csv(OUT_DIR / "active_coverage_summary.csv", index=False)
    decisions.to_csv(OUT_DIR / "candidate_classification.csv", index=False)
    for name, panel in signals.items():
        panel.to_parquet(OUT_DIR / f"{name}_signal_panel.parquet")
    (OUT_DIR / "manifest.json").write_text(
        json.dumps(
            {
                "run_id": RUN_ID,
                "research_only": True,
                "source_concept_screen": str(CONCEPT_NOTE),
                "source_closeout": str(CLOSEOUT_NOTE),
                "candidate_count": len(signals),
                "candidate_names": list(signals.keys()),
                "production_registration": False,
                "survivor_watchlist_mutation": False,
                "portfolio_integration": False,
                "ml_integration": False,
                "production_conditional_alpha_wiring": False,
                "gates_schemas_thresholds_modified": False,
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )
    write_note(registry, structural, scores, wfv_summary, stress, state_attr, orth_summary, active, decisions)
    print(f"WROTE {OUT_DIR}")
    print(f"WROTE {NOTE_PATH}")
    print(decisions.to_string(index=False))


if __name__ == "__main__":
    main()
