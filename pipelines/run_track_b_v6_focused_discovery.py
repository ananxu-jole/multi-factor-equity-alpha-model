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
)
from run_track_b_robustness_discovery_v4 import _cs_neutralize


RUN_ID = "track_b_v6_focused_discovery"
OUT_DIR = Path("artifacts/research") / RUN_ID
NOTE_PATH = Path("docs/research_notes/track_b_v6_focused_discovery.md")
CONCEPT_NOTE = Path("docs/research_notes/track_b_v6_concept_screening.md")
INVENTORY_NOTE = Path("docs/research_notes/conditional_alpha_inventory_v1.md")
INVENTORY_DIR = Path("artifacts/research/conditional_alpha_inventory_v1")
LIQUIDITY_INVENTORY_PATH = Path("artifacts/research/robustness_first_discovery_expansion_v4/participation_liquidity_state_shift_20_60_signal_panel.parquet")
BREADTH_INVENTORY_PATH = Path("artifacts/research/participation_breadth_repair_refinement_v1/strict_weak_breadth_rebalance_10_signal_panel.parquet")


CANDIDATES: list[dict[str, str]] = [
    {
        "signal_name": "volatility_compression_after_stress_stabilization",
        "family": "volatility_dispersion_stabilization",
        "mechanism_thesis": "After stress or volatility spike, names whose realized range compresses without price extension may show cleaner forward behavior.",
        "state_transition_logic": "Recent volatility/panic stress followed by individual range compression and low price extension.",
        "differs_from_inventory": "Uses volatility/range normalization rather than participation, liquidity repair, or breadth repair.",
        "differs_from_reversal_momentum": "Does not fade prior returns or chase price rank; price rank is neutralized and extension is capped.",
        "expected_activation_state": "Recent volatility spike or panic/liquidity stress with range compression.",
        "expected_horizon": "h10-h20",
        "expected_turnover_profile": "Low-medium after smoothing.",
        "expected_active_coverage": "moderate",
    },
    {
        "signal_name": "dispersion_peak_to_cross_sectional_stability",
        "family": "dispersion_state_transition",
        "mechanism_thesis": "Cross-sectional dispersion peaks followed by stabilizing rank dispersion may identify healthier rotation after unstable markets.",
        "state_transition_logic": "Market dispersion transitions from elevated to stabilizing while individual rank churn declines.",
        "differs_from_inventory": "Uses dispersion and cross-sectional stability, not participation or weak-breadth repair.",
        "differs_from_reversal_momentum": "Selects stabilization after dispersion stress rather than prior underperformance or mature leadership.",
        "expected_activation_state": "High recent dispersion with current dispersion normalization.",
        "expected_horizon": "h10-h20",
        "expected_turnover_profile": "Low-medium.",
        "expected_active_coverage": "moderate",
    },
    {
        "signal_name": "event_gap_quality_continuation_filter",
        "family": "event_quality_structure",
        "mechanism_thesis": "Large gaps followed by orderly range containment and non-extreme volume may identify event quality rather than noisy reversal or chase behavior.",
        "state_transition_logic": "Material gap event with contained intraday range, close-location confirmation, and controlled churn.",
        "differs_from_inventory": "Event-quality focused; not participation, liquidity, or breadth repair.",
        "differs_from_reversal_momentum": "Requires post-event quality and range containment rather than fading or chasing raw price moves.",
        "expected_activation_state": "Material gap event with orderly post-gap behavior.",
        "expected_horizon": "h5-h20",
        "expected_turnover_profile": "Medium.",
        "expected_active_coverage": "moderate-to-sparse",
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


def _rolling_quantile(series: pd.Series, q: float) -> pd.Series:
    return series.rolling(252, min_periods=100).quantile(q)


def _rebalance_interval(panel: pd.DataFrame, interval: int) -> pd.DataFrame:
    out = panel.copy() * np.nan
    out.iloc[::interval] = panel.iloc[::interval]
    return out.ffill()


def _safe_div(numerator: pd.DataFrame, denominator: pd.DataFrame) -> pd.DataFrame:
    return numerator / denominator.replace(0.0, np.nan)


def _build_states(panels: dict[str, pd.DataFrame], benchmark: pd.Series) -> pd.DataFrame:
    close = panels["close"]
    high = panels["high"]
    low = panels["low"]
    ret1 = close.pct_change(1, fill_method=None)
    ret20 = close.pct_change(20, fill_method=None)
    bench_ret = benchmark.pct_change(1, fill_method=None)
    bench_vol20 = bench_ret.rolling(20, min_periods=15).std()
    bench_vol60 = bench_ret.rolling(60, min_periods=40).std()
    dispersion20 = ret20.std(axis=1)
    dispersion60 = ret1.rolling(60, min_periods=40).std().mean(axis=1)
    avg_range = ((high - low) / close.shift(1)).replace([np.inf, -np.inf], np.nan).mean(axis=1)
    stress = build_stress_states(close, benchmark)

    states = pd.DataFrame(index=close.index)
    states["RECENT_VOL_STRESS"] = (
        stress[["volatility_spike", "panic_liquidity_stress"]]
        .rolling(20, min_periods=1)
        .max()
        .max(axis=1)
        .astype(bool)
    )
    states["VOL_NORMALIZING"] = ((bench_vol20 < bench_vol60) & (bench_vol20.diff(10) < 0)).fillna(False)
    states["RANGE_NORMALIZING"] = (avg_range < avg_range.rolling(60, min_periods=40).mean()).fillna(False)
    states["DISPERSION_ELEVATED_RECENT"] = (
        dispersion20.rolling(20, min_periods=10).max() > _rolling_quantile(dispersion20, 0.75)
    ).fillna(False)
    states["DISPERSION_NORMALIZING"] = (
        (dispersion20 < dispersion20.rolling(60, min_periods=40).mean()) & (dispersion20.diff(10) < 0)
    ).fillna(False)
    states["DISPERSION_STABILITY_TRANSITION"] = (
        states["DISPERSION_ELEVATED_RECENT"] & states["DISPERSION_NORMALIZING"]
    ).fillna(False)
    states["EVENT_GAP_DAY"] = False
    return states


def build_candidate_panels(panels: dict[str, pd.DataFrame], benchmark: pd.Series) -> tuple[dict[str, pd.DataFrame], pd.DataFrame]:
    open_ = panels["open"]
    high = panels["high"]
    low = panels["low"]
    close = panels["close"]
    volume = panels["volume"].astype(float).where(panels["volume"].astype(float) > 0)
    ret1 = close.pct_change(1, fill_method=None)
    ret10 = close.pct_change(10, fill_method=None)
    ret20 = close.pct_change(20, fill_method=None)
    ret60 = close.pct_change(60, fill_method=None)
    ret20_rank = _rank_cs(ret20)

    states = _build_states(panels, benchmark)
    stress_gate = _market_state_panel(states["RECENT_VOL_STRESS"] & states["RANGE_NORMALIZING"], close.columns)
    dispersion_gate = _market_state_panel(states["DISPERSION_STABILITY_TRANSITION"], close.columns)

    true_range = ((high - low) / close.shift(1)).replace([np.inf, -np.inf], np.nan)
    range20 = true_range.rolling(20, min_periods=15).mean()
    range60 = true_range.rolling(60, min_periods=40).mean()
    range_compression = (1.0 - _safe_div(range20, range60)).clip(lower=0, upper=1)
    low_extension = (1.0 - ret20_rank.abs()).clip(lower=0)
    low_jumpiness = (1.0 - true_range.rank(axis=1, pct=True)).clip(lower=0)
    volatility_stabilization = _rank_cs(
        (range_compression * low_extension * low_jumpiness.rolling(5, min_periods=3).mean()).rolling(5, min_periods=3).mean()
    )
    volatility_stabilization = _rank_cs(_cs_neutralize(volatility_stabilization, ret20_rank) * stress_gate)

    rank20 = ret20.rank(axis=1, pct=True)
    rank_churn = rank20.diff().abs().rolling(20, min_periods=12).mean()
    rank_stability = (1.0 - rank_churn.rank(axis=1, pct=True)).clip(lower=0)
    idio_vol = (ret1.sub(ret1.mean(axis=1), axis=0)).rolling(20, min_periods=15).std()
    idio_stability = (1.0 - idio_vol.rank(axis=1, pct=True)).clip(lower=0)
    neutral_rank_level = (1.0 - ret60.rank(axis=1, pct=True).sub(0.5).abs() * 2.0).clip(lower=0)
    dispersion_stability = _rank_cs(
        (rank_stability * idio_stability * neutral_rank_level).rolling(5, min_periods=3).mean()
    )
    dispersion_stability = _rank_cs(_cs_neutralize(dispersion_stability, ret20_rank) * dispersion_gate)
    dispersion_stability = _rank_cs(_rebalance_interval(dispersion_stability, 10))

    prev_close = close.shift(1)
    gap = open_ / prev_close - 1.0
    intraday_ret = close / open_ - 1.0
    close_location = ((close - low) / (high - low).replace(0.0, np.nan)).clip(0, 1)
    gap_abs_rank = gap.abs().rank(axis=1, pct=True)
    material_gap = (gap_abs_rank >= 0.80).astype(float)
    contained_range = (1.0 - true_range.rank(axis=1, pct=True)).clip(lower=0)
    volume_ratio = _safe_div(volume, volume.rolling(20, min_periods=10).mean()).clip(0, 5)
    controlled_volume = (1.0 - (volume_ratio - 1.5).abs().rank(axis=1, pct=True)).clip(lower=0)
    direction_confirm = np.sign(gap) * (close_location - 0.5) * 2.0
    no_extreme_chase = (1.0 - ret10.rank(axis=1, pct=True).sub(0.5).abs() * 2.0).clip(lower=0)
    gap_quality = _rank_cs(material_gap * direction_confirm * contained_range * controlled_volume * no_extreme_chase)
    gap_quality = _rank_cs(_cs_neutralize(gap_quality, ret20_rank))
    states["EVENT_GAP_DAY"] = (gap_abs_rank >= 0.80).any(axis=1).fillna(False)

    signals = {
        "volatility_compression_after_stress_stabilization": volatility_stabilization,
        "dispersion_peak_to_cross_sectional_stability": dispersion_stability,
        "event_gap_quality_continuation_filter": gap_quality,
    }
    return {name: _clean_panel(panel) for name, panel in signals.items()}, states


def reference_panels(signals: dict[str, pd.DataFrame], panels: dict[str, pd.DataFrame], benchmark: pd.Series) -> dict[str, pd.DataFrame]:
    refs = baseline_panels(signals, panels, benchmark)
    first = next(iter(signals.values()))
    if LIQUIDITY_INVENTORY_PATH.exists():
        refs["inventory_participation_liquidity_state_shift_20_60"] = pd.read_parquet(LIQUIDITY_INVENTORY_PATH).reindex(
            index=first.index,
            columns=first.columns,
        )
    if BREADTH_INVENTORY_PATH.exists():
        refs["inventory_participation_breadth_repair_under_hostile_trend"] = pd.read_parquet(BREADTH_INVENTORY_PATH).reindex(
            index=first.index,
            columns=first.columns,
        )
    return refs


def active_coverage_summary(signals: dict[str, pd.DataFrame]) -> pd.DataFrame:
    rows = []
    for name, panel in signals.items():
        valid_count = panel.notna().sum(axis=1)
        mean_abs = panel.abs().mean(axis=1, skipna=True)
        active = (valid_count >= 25) & (mean_abs > 0.02)
        transitions = active.astype(int).diff().abs().fillna(0)
        rows.append(
            {
                "signal_name": name,
                "active_dates": int(active.sum()),
                "active_date_ratio": float(active.mean()),
                "activation_transitions": int(transitions.sum()),
                "mean_active_coverage": float(panel[active].notna().mean(axis=1).mean()) if active.any() else np.nan,
            }
        )
    return pd.DataFrame(rows)


def state_attribution(daily_ics: pd.DataFrame, scores: pd.DataFrame, states: pd.DataFrame) -> pd.DataFrame:
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
        liquidity = group[group["comparison"].eq("inventory_participation_liquidity_state_shift_20_60")]
        breadth = group[group["comparison"].eq("inventory_participation_breadth_repair_under_hostile_trend")]
        reversal = group[group["comparison"].isin(["unweighted_reversal_20", "plain_smoothed_reversal_20"])]
        momentum = group[group["comparison"].isin(["plain_momentum_60"])]
        rows.append(
            {
                "signal_name": name,
                "top_comparison": top["comparison"],
                "max_abs_baseline_corr": float(top["abs_value_corr"]),
                "inventory_liquidity_corr": float(liquidity["abs_value_corr"].max()) if not liquidity.empty else np.nan,
                "inventory_breadth_corr": float(breadth["abs_value_corr"].max()) if not breadth.empty else np.nan,
                "max_inventory_corr": float(
                    pd.concat([liquidity["abs_value_corr"], breadth["abs_value_corr"]]).max()
                )
                if not liquidity.empty or not breadth.empty
                else np.nan,
                "max_reversal_corr": float(reversal["abs_value_corr"].max()) if not reversal.empty else np.nan,
                "max_momentum_corr": float(momentum["abs_value_corr"].max()) if not momentum.empty else np.nan,
            }
        )
    return pd.DataFrame(rows)


def _family_for(signal_name: str) -> str:
    for spec in CANDIDATES:
        if spec["signal_name"] == signal_name:
            return spec["family"]
    return "unknown"


def classify_candidates(
    structural: pd.DataFrame,
    scores: pd.DataFrame,
    wfv: pd.DataFrame,
    stress: pd.DataFrame,
    orth_summary: pd.DataFrame,
    active: pd.DataFrame,
) -> pd.DataFrame:
    best = scores.loc[scores["is_best_horizon"]].copy()
    h20 = scores[scores["horizon"].eq(20)].rename(
        columns={"mean_ic": "h20_mean_ic", "ic_ir": "h20_ic_ir", "positive_ic_rate": "h20_positive_ic_rate", "n_dates": "h20_n_dates"}
    )
    stress_counts = (
        stress.groupby("signal_name")["mean_ic"]
        .agg(positive_regime_count=lambda s: int((s > 0.004).sum()), best_regime_ic="max")
        .reset_index()
    )
    summary = (
        best.merge(h20[["signal_name", "h20_mean_ic", "h20_ic_ir", "h20_positive_ic_rate", "h20_n_dates"]], on="signal_name", how="left")
        .merge(structural, on="signal_name", how="left")
        .merge(wfv, on=["signal_name", "horizon"], how="left")
        .merge(stress_counts, on="signal_name", how="left")
        .merge(orth_summary, on="signal_name", how="left")
        .merge(active, on="signal_name", how="left")
    )
    rows = []
    for _, row in summary.iterrows():
        issues = []
        if row["missing_pct"] > 0.35:
            issues.append("high_missingness")
        if row["turnover_proxy"] > 0.16:
            issues.append("high_turnover")
        if row["mean_ic"] < 0:
            issues.append("direction_mismatch")
        if row["abs_mean_ic"] < 0.006:
            issues.append("weak_best_horizon_ic")
        if row["h20_mean_ic"] < 0.006:
            issues.append("weak_h20_ic")
        if row["positive_ic_rate"] < 0.52:
            issues.append("weak_positive_ic_rate")
        if pd.notna(row.get("persistence")) and row["persistence"] < 0.75:
            issues.append("weak_wfv_persistence")
        if pd.notna(row.get("sign_consistency")) and row["sign_consistency"] < 0.75:
            issues.append("weak_wfv_sign_consistency")
        if row.get("max_inventory_corr", 0) > 0.50:
            issues.append("inventory_similarity_risk")
        if row.get("max_reversal_corr", 0) > 0.50:
            issues.append("reversal_similarity_risk")
        if row.get("max_momentum_corr", 0) > 0.50:
            issues.append("momentum_similarity_risk")
        if row.get("active_date_ratio", 1) < 0.12:
            issues.append("sparse_activation")

        if (
            row["h20_mean_ic"] > 0.014
            and row["h20_positive_ic_rate"] >= 0.54
            and row.get("persistence", 0) >= 0.75
            and row.get("sign_consistency", 0) >= 0.75
            and row["turnover_proxy"] <= 0.12
            and row.get("max_inventory_corr", 1) <= 0.45
            and row.get("max_reversal_corr", 1) <= 0.50
            and row.get("active_date_ratio", 0) >= 0.15
        ):
            status = "CANDIDATE_FOR_CONDITIONAL_VALIDATION"
        elif (
            row["h20_mean_ic"] > 0.008
            and row.get("best_regime_ic", 0) > 0.012
            and row.get("max_inventory_corr", 1) <= 0.50
            and row.get("max_reversal_corr", 1) <= 0.55
            and row.get("active_date_ratio", 0) >= 0.12
        ):
            status = "CONDITIONAL_REFINEMENT_CANDIDATE"
        elif (
            row.get("positive_regime_count", 0) >= 2
            and row.get("max_inventory_corr", 1) <= 0.55
            and row.get("active_date_ratio", 0) >= 0.10
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
                "h20_mean_ic": row["h20_mean_ic"],
                "h20_positive_ic_rate": row["h20_positive_ic_rate"],
                "ic_ir": row["ic_ir"],
                "positive_ic_rate": row["positive_ic_rate"],
                "turnover_proxy": row["turnover_proxy"],
                "missing_pct": row["missing_pct"],
                "active_date_ratio": row.get("active_date_ratio"),
                "max_abs_baseline_corr": row.get("max_abs_baseline_corr"),
                "inventory_liquidity_corr": row.get("inventory_liquidity_corr"),
                "inventory_breadth_corr": row.get("inventory_breadth_corr"),
                "max_inventory_corr": row.get("max_inventory_corr"),
                "max_reversal_corr": row.get("max_reversal_corr"),
                "max_momentum_corr": row.get("max_momentum_corr"),
                "wfv_persistence": row.get("persistence"),
                "wfv_sign_consistency": row.get("sign_consistency"),
                "effective_test_ic_ir": row.get("effective_test_ic_ir"),
                "positive_regime_count": int(row.get("positive_regime_count", 0) or 0),
                "best_regime_ic": row.get("best_regime_ic"),
                "status": status,
                "review_issues": "; ".join(issues) if issues else "none",
            }
        )
    return pd.DataFrame(rows).sort_values(["status", "h20_mean_ic"], ascending=[True, False])


def _recommendation(decisions: pd.DataFrame) -> str:
    validation = decisions[decisions["status"].eq("CANDIDATE_FOR_CONDITIONAL_VALIDATION")]
    if not validation.empty:
        names = ", ".join(f"`{name}`" for name in validation["signal_name"])
        return f"Run a formal conditional-validation pass only for {names}; do not broaden v6 or tune parameters."
    refinement = decisions[decisions["status"].eq("CONDITIONAL_REFINEMENT_CANDIDATE")]
    if not refinement.empty:
        names = ", ".join(f"`{name}`" for name in refinement["signal_name"])
        return f"Run a narrow refinement diagnostics pass only for {names}. Keep any refinements pre-declared and small."
    keep = decisions[decisions["status"].eq("CONDITIONAL_ONLY_RESEARCH")]
    if not keep.empty:
        names = ", ".join(f"`{name}`" for name in keep["signal_name"])
        return f"Keep {names} as conditional-only research evidence. Do not add variants until the state thesis is sharpened."
    return "Reject this v6 implementation wave as useful negative evidence and return to concept design before expanding."


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
    h20 = scores[scores["horizon"].eq(20)].sort_values("mean_ic", ascending=False)
    state_best = state_attr.sort_values("mean_ic", ascending=False).groupby("signal_name").head(4)
    status_counts = decisions["status"].value_counts().to_dict()
    lines = [
        "# Track B v6 Focused Discovery",
        "",
        "## Executive Takeaway",
        "",
        f"This research-only run implemented the three shortlisted concepts from the Track B v6 concept screen under `{RUN_ID}`.",
        "",
        "This was a small focused batch: one simple formulation per concept, no parameter grid, no broad discovery, and no production wiring.",
        "",
        f"Candidates tested: {len(registry)}",
        f"Status counts: `{json.dumps(status_counts, sort_keys=True)}`",
        "",
        "No production registration, survivor/watchlist promotion, portfolio integration, ML integration, production Conditional-Alpha wiring, gate/schema/threshold change, or trading logic change was made.",
        "",
        "## Source Context",
        "",
        f"- Concept screen: `{CONCEPT_NOTE}`",
        f"- Conditional Alpha Inventory v1: `{INVENTORY_NOTE}`",
        "- Current inventory candidates used as similarity baselines: `participation_liquidity_state_shift_20_60` and `participation_breadth_repair_under_hostile_trend`.",
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
        "## Mechanism-Family Assessment",
        "",
        "- The run explicitly tested volatility/dispersion/event-quality mechanisms against the existing participation/liquidity/breadth inventory.",
        "- A concept should be considered a genuinely new family only if it has positive h20 behavior, adequate active coverage, and low similarity to both inventory candidates and reversal/momentum baselines.",
        "- Rejections are expected. The objective is to learn whether a third conditional-alpha family exists, not to force inventory expansion.",
        "",
        "## Recommended Next Step",
        "",
        _recommendation(decisions),
    ]
    NOTE_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    _ensure_dirs()
    panels, benchmark = load_inputs()
    signals, states = build_candidate_panels(panels, benchmark)
    registry = pd.DataFrame(CANDIDATES)
    registry["run_id"] = RUN_ID
    registry["research_status"] = "TRACK_B_V6_RESEARCH_ONLY"

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

    artifact_files = [
        "candidate_registry.csv",
        "structural_quality_summary.csv",
        "multi_horizon_scoring.csv",
        "daily_ic_by_signal_horizon.csv",
        "market_state_flags.csv",
        "stress_regime_attribution.csv",
        "concept_state_attribution.csv",
        "wfv_style_summary.csv",
        "wfv_window_diagnostics.csv",
        "orthogonality_redundancy_audit.csv",
        "orthogonality_summary.csv",
        "active_coverage_summary.csv",
        "candidate_classification.csv",
    ]
    registry.to_csv(OUT_DIR / artifact_files[0], index=False)
    structural.to_csv(OUT_DIR / artifact_files[1], index=False)
    scores.to_csv(OUT_DIR / artifact_files[2], index=False)
    daily_ics.to_csv(OUT_DIR / artifact_files[3], index=False)
    states.to_csv(OUT_DIR / artifact_files[4], index=True)
    stress.to_csv(OUT_DIR / artifact_files[5], index=False)
    state_attr.to_csv(OUT_DIR / artifact_files[6], index=False)
    wfv_summary.to_csv(OUT_DIR / artifact_files[7], index=False)
    wfv_windows.to_csv(OUT_DIR / artifact_files[8], index=False)
    orth.to_csv(OUT_DIR / artifact_files[9], index=False)
    orth_summary.to_csv(OUT_DIR / artifact_files[10], index=False)
    active.to_csv(OUT_DIR / artifact_files[11], index=False)
    decisions.to_csv(OUT_DIR / artifact_files[12], index=False)
    for name, panel in signals.items():
        panel_file = f"{name}_signal_panel.parquet"
        panel.to_parquet(OUT_DIR / panel_file)
        artifact_files.append(panel_file)
    artifact_files.append("manifest.json")
    (OUT_DIR / "manifest.json").write_text(
        json.dumps(
            {
                "run_id": RUN_ID,
                "research_only": True,
                "source_concept_screen": str(CONCEPT_NOTE),
                "source_inventory": str(INVENTORY_NOTE),
                "candidate_count": len(signals),
                "candidate_names": list(signals.keys()),
                "one_formulation_per_concept": True,
                "parameter_grid": False,
                "production_registration": False,
                "survivor_watchlist_promotion": False,
                "portfolio_integration": False,
                "ml_integration": False,
                "production_conditional_alpha_wiring": False,
                "gates_schemas_thresholds_modified": False,
                "artifact_files": sorted(artifact_files),
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
