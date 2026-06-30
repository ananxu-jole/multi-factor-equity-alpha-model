from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

from run_dispersion_recovery_stability_after_stress_v1 import VOLATILITY_INVENTORY_PATH
from run_track_b_robustness_discovery_v3 import (
    build_stress_states,
    daily_ic,
    forward_returns,
    load_inputs,
)
from run_track_b_v6_focused_discovery import BREADTH_INVENTORY_PATH, LIQUIDITY_INVENTORY_PATH
from run_transition_state_composite_detector_v1 import STATE_ORDER


RUN_ID = "transition_state_conditional_attribution_v1"
DETECTOR_RUN_ID = "transition_state_composite_detector_v1"
OUT_DIR = Path("artifacts/research") / RUN_ID
NOTE_PATH = Path("docs/research_notes/transition_state_conditional_attribution_v1.md")
DETECTOR_LABEL_PATH = Path("artifacts/research") / DETECTOR_RUN_ID / "composite_state_labels.csv"
HORIZONS = (1, 5, 10, 15, 20)
WFV_WINDOWS = 4

RESEARCH_ONLY_GUARDRAIL = (
    "This is a research-only conditional attribution pass. It does not register, promote, validate, blend, "
    "optimize, route, or productionize the Transition-State Composite Detector or any candidate panel. "
    "Findings are explanatory diagnostics only and should be used, at most, to motivate future validation or "
    "monitoring work."
)

INVENTORY_PANELS = {
    "participation_liquidity_state_shift_20_60": LIQUIDITY_INVENTORY_PATH,
    "participation_breadth_repair_under_hostile_trend": BREADTH_INVENTORY_PATH,
    "volatility_compression_after_stress_stabilization": VOLATILITY_INVENTORY_PATH,
}


def _ensure_dirs() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    NOTE_PATH.parent.mkdir(parents=True, exist_ok=True)


def load_detector_labels() -> pd.DataFrame:
    if not DETECTOR_LABEL_PATH.exists():
        raise FileNotFoundError(f"Missing detector label artifact: {DETECTOR_LABEL_PATH}")
    labels = pd.read_csv(DETECTOR_LABEL_PATH, parse_dates=["Date"]).set_index("Date").sort_index()
    if "state_label" not in labels.columns:
        raise ValueError(f"Detector label artifact does not include state_label: {DETECTOR_LABEL_PATH}")
    return labels


def load_inventory_panels(index: pd.Index, columns: pd.Index) -> dict[str, pd.DataFrame]:
    panels = {}
    for name, path in INVENTORY_PANELS.items():
        if path.exists():
            panels[name] = pd.read_parquet(path).reindex(index=index, columns=columns)
    if not panels:
        raise FileNotFoundError("No inventory signal panels were available for attribution.")
    return panels


def long_short_returns(signal: pd.DataFrame, fwd: pd.DataFrame) -> pd.Series:
    values = []
    dates = []
    for date in signal.index.intersection(fwd.index):
        s = signal.loc[date]
        r = fwd.loc[date]
        valid = s.notna() & r.notna()
        if int(valid.sum()) < 25:
            values.append(np.nan)
            dates.append(date)
            continue
        ranked = s[valid].rank(pct=True)
        long = r[valid & ranked.ge(0.80)]
        short = r[valid & ranked.le(0.20)]
        if long.empty or short.empty:
            values.append(np.nan)
        else:
            values.append(float(long.mean() - short.mean()))
        dates.append(date)
    return pd.Series(values, index=pd.Index(dates, name="Date"), dtype=float)


def active_coverage(signal: pd.DataFrame) -> pd.Series:
    return signal.notna().mean(axis=1)


def turnover_series(signal: pd.DataFrame) -> pd.Series:
    return signal.diff().abs().mean(axis=1, skipna=True)


def daily_signal_diagnostics(signals: dict[str, pd.DataFrame], close: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    ic_rows = []
    ls_rows = []
    for signal_name, panel in signals.items():
        coverage = active_coverage(panel)
        turnover = turnover_series(panel)
        for horizon in HORIZONS:
            fwd = forward_returns(close, horizon)
            ic = daily_ic(panel, fwd)
            ls = long_short_returns(panel, fwd)
            ic_rows.extend(
                {
                    "Date": date,
                    "signal_name": signal_name,
                    "horizon": horizon,
                    "ic": value,
                    "active_coverage": coverage.reindex([date]).iloc[0] if date in coverage.index else np.nan,
                    "turnover": turnover.reindex([date]).iloc[0] if date in turnover.index else np.nan,
                }
                for date, value in ic.items()
            )
            ls_rows.extend(
                {
                    "Date": date,
                    "signal_name": signal_name,
                    "horizon": horizon,
                    "long_short_return": value,
                    "hit": value > 0 if pd.notna(value) else np.nan,
                }
                for date, value in ls.items()
            )
    return pd.DataFrame(ic_rows), pd.DataFrame(ls_rows)


def candidate_by_state_attribution(
    daily_ics: pd.DataFrame,
    daily_ls: pd.DataFrame,
    labels: pd.DataFrame,
) -> pd.DataFrame:
    state = labels["state_label"]
    ic = daily_ics.merge(state.rename("state_label"), left_on="Date", right_index=True, how="left")
    ls = daily_ls.merge(state.rename("state_label"), left_on="Date", right_index=True, how="left")
    rows = []
    for (signal_name, horizon, state_label), group in ic.groupby(["signal_name", "horizon", "state_label"]):
        ls_group = ls[
            ls["signal_name"].eq(signal_name)
            & ls["horizon"].eq(horizon)
            & ls["state_label"].eq(state_label)
        ]
        valid_ic = group["ic"].dropna()
        valid_ls = ls_group["long_short_return"].dropna()
        rows.append(
            {
                "signal_name": signal_name,
                "state_label": state_label,
                "horizon": int(horizon),
                "mean_ic": float(valid_ic.mean()) if not valid_ic.empty else np.nan,
                "median_ic": float(valid_ic.median()) if not valid_ic.empty else np.nan,
                "positive_ic_rate": float((valid_ic > 0).mean()) if not valid_ic.empty else np.nan,
                "n_ic_dates": int(valid_ic.shape[0]),
                "mean_long_short_return": float(valid_ls.mean()) if not valid_ls.empty else np.nan,
                "median_long_short_return": float(valid_ls.median()) if not valid_ls.empty else np.nan,
                "hit_rate": float((valid_ls > 0).mean()) if not valid_ls.empty else np.nan,
                "n_return_dates": int(valid_ls.shape[0]),
                "mean_active_coverage": float(group["active_coverage"].mean()),
                "mean_turnover": float(group["turnover"].mean()),
            }
        )
    out = pd.DataFrame(rows)
    return out.sort_values(["signal_name", "horizon", "state_label"])


def conditional_ic_summary(candidate_state: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for (signal_name, horizon), group in candidate_state.groupby(["signal_name", "horizon"]):
        group = group.copy()
        best = group.loc[group["mean_ic"].idxmax()] if group["mean_ic"].notna().any() else None
        worst = group.loc[group["mean_ic"].idxmin()] if group["mean_ic"].notna().any() else None
        neutral = group[group["state_label"].eq("NEUTRAL")]
        rows.append(
            {
                "signal_name": signal_name,
                "horizon": int(horizon),
                "best_state": best["state_label"] if best is not None else None,
                "best_state_mean_ic": float(best["mean_ic"]) if best is not None else np.nan,
                "worst_state": worst["state_label"] if worst is not None else None,
                "worst_state_mean_ic": float(worst["mean_ic"]) if worst is not None else np.nan,
                "neutral_mean_ic": float(neutral["mean_ic"].iloc[0]) if not neutral.empty else np.nan,
                "state_ic_range": float(group["mean_ic"].max() - group["mean_ic"].min()),
                "state_positive_rate_range": float(group["positive_ic_rate"].max() - group["positive_ic_rate"].min()),
                "min_state_ic_dates": int(group["n_ic_dates"].min()),
            }
        )
    return pd.DataFrame(rows)


def conditional_return_summary(candidate_state: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for (signal_name, horizon), group in candidate_state.groupby(["signal_name", "horizon"]):
        best = group.loc[group["mean_long_short_return"].idxmax()] if group["mean_long_short_return"].notna().any() else None
        worst = group.loc[group["mean_long_short_return"].idxmin()] if group["mean_long_short_return"].notna().any() else None
        rows.append(
            {
                "signal_name": signal_name,
                "horizon": int(horizon),
                "best_return_state": best["state_label"] if best is not None else None,
                "best_state_mean_long_short_return": float(best["mean_long_short_return"]) if best is not None else np.nan,
                "worst_return_state": worst["state_label"] if worst is not None else None,
                "worst_state_mean_long_short_return": float(worst["mean_long_short_return"]) if worst is not None else np.nan,
                "state_return_range": float(
                    group["mean_long_short_return"].max() - group["mean_long_short_return"].min()
                ),
                "state_hit_rate_range": float(group["hit_rate"].max() - group["hit_rate"].min()),
                "min_state_return_dates": int(group["n_return_dates"].min()),
            }
        )
    return pd.DataFrame(rows)


def drawdown_clustering(daily_ls: pd.DataFrame, labels: pd.DataFrame) -> pd.DataFrame:
    state = labels["state_label"]
    data = daily_ls.merge(state.rename("state_label"), left_on="Date", right_index=True, how="left")
    rows = []
    for (signal_name, horizon), group in data.groupby(["signal_name", "horizon"]):
        valid = group.dropna(subset=["long_short_return"])
        if valid.empty:
            continue
        tail_threshold = valid["long_short_return"].quantile(0.10)
        valid = valid.copy()
        valid["tail_loss"] = valid["long_short_return"].le(tail_threshold)
        total_tail = int(valid["tail_loss"].sum())
        state_total = valid["state_label"].value_counts()
        for state_label in STATE_ORDER:
            sample = valid[valid["state_label"].eq(state_label)]
            if sample.empty:
                rows.append(
                    {
                        "signal_name": signal_name,
                        "horizon": int(horizon),
                        "state_label": state_label,
                        "tail_loss_threshold": float(tail_threshold),
                        "state_dates": 0,
                        "tail_loss_dates": 0,
                        "tail_loss_rate": np.nan,
                        "tail_loss_share": np.nan,
                        "state_date_share": 0.0,
                        "tail_loss_concentration_ratio": np.nan,
                        "worst_long_short_return": np.nan,
                    }
                )
                continue
            tail_count = int(sample["tail_loss"].sum())
            state_share = float(state_total.get(state_label, 0) / len(valid))
            tail_share = float(tail_count / total_tail) if total_tail else np.nan
            rows.append(
                {
                    "signal_name": signal_name,
                    "horizon": int(horizon),
                    "state_label": state_label,
                    "tail_loss_threshold": float(tail_threshold),
                    "state_dates": int(sample.shape[0]),
                    "tail_loss_dates": tail_count,
                    "tail_loss_rate": float(sample["tail_loss"].mean()),
                    "tail_loss_share": tail_share,
                    "state_date_share": state_share,
                    "tail_loss_concentration_ratio": tail_share / state_share if state_share and pd.notna(tail_share) else np.nan,
                    "worst_long_short_return": float(sample["long_short_return"].min()),
                }
            )
    return pd.DataFrame(rows)


def state_conditioned_rankings(candidate_state: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for (state_label, horizon), group in candidate_state.groupby(["state_label", "horizon"]):
        ranked = group.copy()
        ranked["ic_rank_in_state"] = ranked["mean_ic"].rank(ascending=False, method="min")
        ranked["return_rank_in_state"] = ranked["mean_long_short_return"].rank(ascending=False, method="min")
        rows.extend(ranked.to_dict("records"))
    return pd.DataFrame(rows).sort_values(["state_label", "horizon", "ic_rank_in_state"])


def state_transition_interaction(daily_ics: pd.DataFrame, daily_ls: pd.DataFrame, labels: pd.DataFrame) -> pd.DataFrame:
    transitions = labels["state_label"].shift(1).fillna("START") + "_TO_" + labels["state_label"]
    ic = daily_ics.merge(transitions.rename("state_transition"), left_on="Date", right_index=True, how="left")
    ls = daily_ls.merge(transitions.rename("state_transition"), left_on="Date", right_index=True, how="left")
    rows = []
    for (signal_name, horizon, transition), group in ic.groupby(["signal_name", "horizon", "state_transition"]):
        if transition.startswith("START_TO_"):
            continue
        valid_ic = group["ic"].dropna()
        if valid_ic.shape[0] < 20:
            continue
        ls_group = ls[
            ls["signal_name"].eq(signal_name)
            & ls["horizon"].eq(horizon)
            & ls["state_transition"].eq(transition)
        ]["long_short_return"].dropna()
        rows.append(
            {
                "signal_name": signal_name,
                "horizon": int(horizon),
                "state_transition": transition,
                "n_ic_dates": int(valid_ic.shape[0]),
                "mean_ic": float(valid_ic.mean()),
                "positive_ic_rate": float((valid_ic > 0).mean()),
                "mean_long_short_return": float(ls_group.mean()) if not ls_group.empty else np.nan,
                "hit_rate": float((ls_group > 0).mean()) if not ls_group.empty else np.nan,
                "n_return_dates": int(ls_group.shape[0]),
            }
        )
    return pd.DataFrame(rows).sort_values(["signal_name", "horizon", "state_transition"])


def sample_size_sanity(candidate_state: pd.DataFrame, labels: pd.DataFrame) -> pd.DataFrame:
    state_counts = labels["state_label"].value_counts().to_dict()
    rows = []
    for signal_name, group in candidate_state.groupby("signal_name"):
        for state_label in STATE_ORDER:
            subset = group[group["state_label"].eq(state_label)]
            rows.append(
                {
                    "signal_name": signal_name,
                    "state_label": state_label,
                    "detector_state_dates": int(state_counts.get(state_label, 0)),
                    "min_ic_dates_across_horizons": int(subset["n_ic_dates"].min()) if not subset.empty else 0,
                    "min_return_dates_across_horizons": int(subset["n_return_dates"].min()) if not subset.empty else 0,
                    "mean_active_coverage": float(subset["mean_active_coverage"].mean()) if not subset.empty else np.nan,
                    "mean_turnover": float(subset["mean_turnover"].mean()) if not subset.empty else np.nan,
                }
            )
    return pd.DataFrame(rows)


def window_stability(daily_ics: pd.DataFrame, labels: pd.DataFrame) -> pd.DataFrame:
    state = labels["state_label"]
    data = daily_ics.merge(state.rename("state_label"), left_on="Date", right_index=True, how="left")
    date_order = pd.Series(np.arange(len(labels)), index=labels.index)
    windows = pd.qcut(date_order, q=WFV_WINDOWS, labels=False, duplicates="drop")
    data = data.merge(windows.rename("window_id"), left_on="Date", right_index=True, how="left")
    rows = []
    for (signal_name, horizon, state_label), group in data.groupby(["signal_name", "horizon", "state_label"]):
        full = group["ic"].dropna()
        if full.empty:
            continue
        full_mean = float(full.mean())
        window_means = []
        for window_id, window_group in group.groupby("window_id"):
            sample = window_group["ic"].dropna()
            if sample.shape[0] < 10:
                continue
            window_means.append(float(sample.mean()))
            rows.append(
                {
                    "signal_name": signal_name,
                    "horizon": int(horizon),
                    "state_label": state_label,
                    "window_id": int(window_id) + 1,
                    "window_mean_ic": float(sample.mean()),
                    "window_positive_ic_rate": float((sample > 0).mean()),
                    "n_ic_dates": int(sample.shape[0]),
                    "full_state_mean_ic": full_mean,
                    "same_sign_as_full_state": bool(np.sign(sample.mean()) == np.sign(full_mean)),
                }
            )
        if window_means:
            same = [np.sign(value) == np.sign(full_mean) for value in window_means]
            rows.append(
                {
                    "signal_name": signal_name,
                    "horizon": int(horizon),
                    "state_label": state_label,
                    "window_id": 0,
                    "window_mean_ic": float(np.mean(window_means)),
                    "window_positive_ic_rate": np.nan,
                    "n_ic_dates": int(full.shape[0]),
                    "full_state_mean_ic": full_mean,
                    "same_sign_as_full_state": float(np.mean(same)),
                }
            )
    return pd.DataFrame(rows).sort_values(["signal_name", "horizon", "state_label", "window_id"])


def detector_usefulness_summary(
    ic_summary: pd.DataFrame,
    return_summary: pd.DataFrame,
    drawdowns: pd.DataFrame,
    samples: pd.DataFrame,
) -> pd.DataFrame:
    rows = []
    for signal_name in sorted(ic_summary["signal_name"].unique()):
        h10 = ic_summary[ic_summary["signal_name"].eq(signal_name) & ic_summary["horizon"].eq(10)]
        h20 = ic_summary[ic_summary["signal_name"].eq(signal_name) & ic_summary["horizon"].eq(20)]
        ret_h10 = return_summary[return_summary["signal_name"].eq(signal_name) & return_summary["horizon"].eq(10)]
        dd_h10 = drawdowns[drawdowns["signal_name"].eq(signal_name) & drawdowns["horizon"].eq(10)]
        sample = samples[samples["signal_name"].eq(signal_name)]
        rows.append(
            {
                "signal_name": signal_name,
                "h10_best_state": h10["best_state"].iloc[0] if not h10.empty else None,
                "h10_worst_state": h10["worst_state"].iloc[0] if not h10.empty else None,
                "h10_state_ic_range": float(h10["state_ic_range"].iloc[0]) if not h10.empty else np.nan,
                "h20_best_state": h20["best_state"].iloc[0] if not h20.empty else None,
                "h20_worst_state": h20["worst_state"].iloc[0] if not h20.empty else None,
                "h20_state_ic_range": float(h20["state_ic_range"].iloc[0]) if not h20.empty else np.nan,
                "h10_best_return_state": ret_h10["best_return_state"].iloc[0] if not ret_h10.empty else None,
                "h10_worst_return_state": ret_h10["worst_return_state"].iloc[0] if not ret_h10.empty else None,
                "largest_h10_tail_loss_concentration_state": dd_h10.loc[dd_h10["tail_loss_concentration_ratio"].idxmax(), "state_label"]
                if not dd_h10.empty and dd_h10["tail_loss_concentration_ratio"].notna().any()
                else None,
                "largest_h10_tail_loss_concentration_ratio": float(dd_h10["tail_loss_concentration_ratio"].max())
                if not dd_h10.empty
                else np.nan,
                "min_state_ic_dates": int(sample["min_ic_dates_across_horizons"].min()) if not sample.empty else 0,
                "detector_appears_contextually_useful": bool(
                    (not h10.empty and h10["state_ic_range"].iloc[0] >= 0.02)
                    or (not h20.empty and h20["state_ic_range"].iloc[0] >= 0.025)
                ),
            }
        )
    return pd.DataFrame(rows)


def stress_overlap_by_state(labels: pd.DataFrame, close: pd.DataFrame, benchmark: pd.Series) -> pd.DataFrame:
    stress = build_stress_states(close, benchmark).fillna(False).astype(bool)
    rows = []
    for state_label in STATE_ORDER:
        state_mask = labels["state_label"].eq(state_label)
        state_dates = int(state_mask.sum())
        for stress_name, stress_mask in stress.items():
            overlap = state_mask & stress_mask
            rows.append(
                {
                    "state_label": state_label,
                    "stress_regime": stress_name,
                    "state_dates": state_dates,
                    "overlap_dates": int(overlap.sum()),
                    "overlap_ratio_with_state": float(overlap.sum() / state_dates) if state_dates else np.nan,
                }
            )
    return pd.DataFrame(rows)


def write_note(
    candidate_state: pd.DataFrame,
    ic_summary: pd.DataFrame,
    return_summary: pd.DataFrame,
    drawdowns: pd.DataFrame,
    usefulness: pd.DataFrame,
    samples: pd.DataFrame,
) -> None:
    h10 = candidate_state[candidate_state["horizon"].eq(10)].copy()
    h10_table = h10[
        [
            "signal_name",
            "state_label",
            "mean_ic",
            "positive_ic_rate",
            "n_ic_dates",
            "mean_long_short_return",
            "hit_rate",
            "mean_active_coverage",
            "mean_turnover",
        ]
    ].to_markdown(index=False, floatfmt=".6f")
    usefulness_table = usefulness.to_markdown(index=False, floatfmt=".6f")
    ic_table = ic_summary[ic_summary["horizon"].isin([10, 20])].to_markdown(index=False, floatfmt=".6f")
    return_table = return_summary[return_summary["horizon"].isin([10, 20])].to_markdown(index=False, floatfmt=".6f")
    dd_focus = drawdowns[drawdowns["horizon"].eq(10)].sort_values(
        ["signal_name", "tail_loss_concentration_ratio"], ascending=[True, False]
    )
    dd_table = dd_focus.head(20).to_markdown(index=False, floatfmt=".6f")
    sample_table = samples.to_markdown(index=False, floatfmt=".6f")

    note = f"""# Transition-State Conditional Attribution v1

Date: 2026-05-21

Run id: `{RUN_ID}`

Detector input: `{DETECTOR_RUN_ID}`

Status: RESEARCH_ONLY_CONDITIONAL_ATTRIBUTION

## Research-Only Guardrail

{RESEARCH_ONLY_GUARDRAIL}

This pass does not tune detector labels, create candidates, or claim causal proof. It asks whether existing inventory candidates exhibit different behavior under pre-existing detector states.

## Attribution Targets

- `participation_liquidity_state_shift_20_60`
- `participation_breadth_repair_under_hostile_trend`
- `volatility_compression_after_stress_stabilization`

## h10 Candidate-By-State Attribution

{h10_table}

## Detector Usefulness Summary

{usefulness_table}

## Conditional IC Summary

{ic_table}

## Conditional Return Summary

{return_table}

## h10 Drawdown Clustering

Tail-loss clustering uses each candidate/horizon's 10th percentile long-short return as the tail threshold. Concentration ratios above 1.0 indicate tail losses are more common in that state than its date share.

{dd_table}

## Sample-Size Sanity

{sample_table}

## Interpretation

The detector appears useful only if state slices repeatedly explain changing candidate behavior while maintaining adequate samples. Strong state IC differences are attribution evidence, not promotion evidence. Thin slices, especially for sparse candidates, should be treated as provisional.

## Recommendation

Keep this as a research-only attribution artifact. If the state-conditioned relationships remain stable in a future monitoring pass, the next appropriate step is a formal conditional validation design for attribution use, not production routing or alpha promotion.

## Artifacts

- `candidate_by_state_attribution.csv`
- `conditional_ic_summary.csv`
- `conditional_return_summary.csv`
- `drawdown_clustering.csv`
- `state_conditioned_rankings.csv`
- `state_transition_interaction.csv`
- `sample_size_sanity.csv`
- `window_stability.csv`
- `stress_overlap_by_state.csv`
- `detector_usefulness_summary.csv`
- `daily_ic_by_candidate.csv`
- `daily_long_short_by_candidate.csv`
- `manifest.json`
"""
    NOTE_PATH.write_text(note)


def write_manifest(artifacts: list[str], signals: dict[str, pd.DataFrame], labels: pd.DataFrame) -> None:
    manifest = {
        "run_id": RUN_ID,
        "detector_run_id": DETECTOR_RUN_ID,
        "status": "RESEARCH_ONLY_CONDITIONAL_ATTRIBUTION",
        "research_only_guardrail": RESEARCH_ONLY_GUARDRAIL,
        "state_labels": STATE_ORDER,
        "candidate_panels_analyzed": sorted(signals.keys()),
        "date_count": int(labels.shape[0]),
        "start_date": str(labels.index.min().date()),
        "end_date": str(labels.index.max().date()),
        "artifacts": artifacts,
        "intentional_non_changes": {
            "production_registration_changed": False,
            "survivor_watchlist_changed": False,
            "validation_logic_changed": False,
            "gates_schemas_thresholds_governance_changed": False,
            "portfolio_ml_blending_optimization_route_changed": False,
            "detector_labels_tuned_for_performance": False,
            "causal_proof_claimed": False,
        },
    }
    (OUT_DIR / "manifest.json").write_text(json.dumps(manifest, indent=2))


def main() -> None:
    _ensure_dirs()
    labels = load_detector_labels()
    panels, benchmark = load_inputs()
    close = panels["close"]
    labels = labels.reindex(close.index).dropna(subset=["state_label"])
    close = close.reindex(labels.index)
    signals = load_inventory_panels(labels.index, close.columns)

    daily_ics, daily_ls = daily_signal_diagnostics(signals, close)
    candidate_state = candidate_by_state_attribution(daily_ics, daily_ls, labels)
    ic_summary = conditional_ic_summary(candidate_state)
    return_summary = conditional_return_summary(candidate_state)
    drawdowns = drawdown_clustering(daily_ls, labels)
    rankings = state_conditioned_rankings(candidate_state)
    transitions = state_transition_interaction(daily_ics, daily_ls, labels)
    samples = sample_size_sanity(candidate_state, labels)
    stability = window_stability(daily_ics, labels)
    stress_overlap = stress_overlap_by_state(labels, close, benchmark.reindex(labels.index))
    usefulness = detector_usefulness_summary(ic_summary, return_summary, drawdowns, samples)

    artifacts = [
        "candidate_by_state_attribution.csv",
        "conditional_ic_summary.csv",
        "conditional_return_summary.csv",
        "drawdown_clustering.csv",
        "state_conditioned_rankings.csv",
        "state_transition_interaction.csv",
        "sample_size_sanity.csv",
        "window_stability.csv",
        "stress_overlap_by_state.csv",
        "detector_usefulness_summary.csv",
        "daily_ic_by_candidate.csv",
        "daily_long_short_by_candidate.csv",
        "manifest.json",
    ]

    candidate_state.to_csv(OUT_DIR / "candidate_by_state_attribution.csv", index=False)
    ic_summary.to_csv(OUT_DIR / "conditional_ic_summary.csv", index=False)
    return_summary.to_csv(OUT_DIR / "conditional_return_summary.csv", index=False)
    drawdowns.to_csv(OUT_DIR / "drawdown_clustering.csv", index=False)
    rankings.to_csv(OUT_DIR / "state_conditioned_rankings.csv", index=False)
    transitions.to_csv(OUT_DIR / "state_transition_interaction.csv", index=False)
    samples.to_csv(OUT_DIR / "sample_size_sanity.csv", index=False)
    stability.to_csv(OUT_DIR / "window_stability.csv", index=False)
    stress_overlap.to_csv(OUT_DIR / "stress_overlap_by_state.csv", index=False)
    usefulness.to_csv(OUT_DIR / "detector_usefulness_summary.csv", index=False)
    daily_ics.to_csv(OUT_DIR / "daily_ic_by_candidate.csv", index=False)
    daily_ls.to_csv(OUT_DIR / "daily_long_short_by_candidate.csv", index=False)
    write_manifest(artifacts, signals, labels)
    write_note(candidate_state, ic_summary, return_summary, drawdowns, usefulness, samples)

    print(f"Wrote {RUN_ID} artifacts to {OUT_DIR}")
    print(f"Wrote research note to {NOTE_PATH}")
    print(RESEARCH_ONLY_GUARDRAIL)


if __name__ == "__main__":
    main()
