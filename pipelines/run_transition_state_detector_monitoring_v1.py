from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

from run_transition_state_composite_detector_v1 import STATE_ORDER


RUN_ID = "transition_state_detector_monitoring_v1"
DETECTOR_RUN_ID = "transition_state_composite_detector_v1"
ATTRIBUTION_RUN_ID = "transition_state_conditional_attribution_v1"
OUT_DIR = Path("artifacts/research") / RUN_ID
NOTE_PATH = Path("docs/research_notes/transition_state_detector_monitoring_v1.md")
DETECTOR_DIR = Path("artifacts/research") / DETECTOR_RUN_ID
ATTRIBUTION_DIR = Path("artifacts/research") / ATTRIBUTION_RUN_ID
HORIZONS = (1, 5, 10, 15, 20)
MONITOR_WINDOWS = 4

RESEARCH_ONLY_GUARDRAIL = (
    "This is a research-only longitudinal monitoring framework for detector-conditioned attribution. "
    "It does not modify detector labels, optimize thresholds, promote detector usage, change gates/schemas/"
    "governance, or route the detector into production, portfolio, ML, blending, or optimization logic."
)


def _ensure_dirs() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    NOTE_PATH.parent.mkdir(parents=True, exist_ok=True)


def _load_required_csv(path: Path, parse_dates: list[str] | None = None) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Missing required artifact: {path}")
    return pd.read_csv(path, parse_dates=parse_dates)


def load_inputs() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    labels = _load_required_csv(DETECTOR_DIR / "composite_state_labels.csv", parse_dates=["Date"]).set_index("Date")
    daily_ic = _load_required_csv(ATTRIBUTION_DIR / "daily_ic_by_candidate.csv", parse_dates=["Date"])
    daily_ls = _load_required_csv(ATTRIBUTION_DIR / "daily_long_short_by_candidate.csv", parse_dates=["Date"])
    baseline = _load_required_csv(ATTRIBUTION_DIR / "candidate_by_state_attribution.csv")
    return labels.sort_index(), daily_ic, daily_ls, baseline


def assign_windows(labels: pd.DataFrame, n_windows: int = MONITOR_WINDOWS) -> pd.Series:
    order = pd.Series(np.arange(len(labels)), index=labels.index)
    return pd.qcut(order, q=n_windows, labels=False, duplicates="drop").astype(int) + 1


def window_metadata(labels: pd.DataFrame, windows: pd.Series) -> pd.DataFrame:
    rows = []
    for window_id, idx in windows.groupby(windows).groups.items():
        dates = pd.Index(idx)
        rows.append(
            {
                "window_id": int(window_id),
                "start_date": str(dates.min().date()),
                "end_date": str(dates.max().date()),
                "n_dates": int(len(dates)),
            }
        )
    return pd.DataFrame(rows)


def state_frequency_drift(labels: pd.DataFrame, windows: pd.Series) -> pd.DataFrame:
    full_dist = labels["state_label"].value_counts(normalize=True).reindex(STATE_ORDER, fill_value=0.0)
    rows = []
    for window_id in sorted(windows.unique()):
        sample = labels.loc[windows.eq(window_id), "state_label"]
        dist = sample.value_counts(normalize=True).reindex(STATE_ORDER, fill_value=0.0)
        for state_label in STATE_ORDER:
            rows.append(
                {
                    "window_id": int(window_id),
                    "state_label": state_label,
                    "window_state_ratio": float(dist[state_label]),
                    "full_state_ratio": float(full_dist[state_label]),
                    "ratio_drift": float(dist[state_label] - full_dist[state_label]),
                    "abs_ratio_drift": float(abs(dist[state_label] - full_dist[state_label])),
                    "window_state_dates": int(sample.eq(state_label).sum()),
                    "thin_state_warning": bool(sample.eq(state_label).sum() < 30),
                }
            )
    return pd.DataFrame(rows)


def state_transition_drift(labels: pd.DataFrame, windows: pd.Series) -> pd.DataFrame:
    transitions = labels["state_label"].shift(1) + "_TO_" + labels["state_label"]
    full = transitions.dropna().value_counts(normalize=True)
    rows = []
    for window_id in sorted(windows.unique()):
        sample = transitions.loc[windows.eq(window_id)].dropna()
        dist = sample.value_counts(normalize=True)
        for transition in sorted(set(full.index).union(dist.index)):
            rows.append(
                {
                    "window_id": int(window_id),
                    "state_transition": transition,
                    "window_transition_ratio": float(dist.get(transition, 0.0)),
                    "full_transition_ratio": float(full.get(transition, 0.0)),
                    "transition_ratio_drift": float(dist.get(transition, 0.0) - full.get(transition, 0.0)),
                    "window_transition_dates": int((sample == transition).sum()),
                    "thin_transition_warning": bool((sample == transition).sum() < 20),
                }
            )
    return pd.DataFrame(rows)


def transition_persistence(labels: pd.DataFrame, windows: pd.Series) -> pd.DataFrame:
    rows = []
    for window_id in sorted(windows.unique()):
        sample = labels.loc[windows.eq(window_id), "state_label"]
        prev = sample.shift(1)
        for state_label in STATE_ORDER:
            starts = prev.eq(state_label)
            rows.append(
                {
                    "window_id": int(window_id),
                    "state_label": state_label,
                    "same_state_persistence_rate": float(sample[starts].eq(state_label).mean()) if starts.any() else np.nan,
                    "eligible_transition_dates": int(starts.sum()),
                }
            )
    return pd.DataFrame(rows)


def _with_state_window(data: pd.DataFrame, labels: pd.DataFrame, windows: pd.Series) -> pd.DataFrame:
    out = data.merge(labels["state_label"].rename("state_label"), left_on="Date", right_index=True, how="left")
    out = out.merge(windows.rename("window_id"), left_on="Date", right_index=True, how="left")
    return out


def rolling_attribution_stability(
    daily_ic: pd.DataFrame,
    daily_ls: pd.DataFrame,
    labels: pd.DataFrame,
    windows: pd.Series,
) -> pd.DataFrame:
    ic = _with_state_window(daily_ic, labels, windows)
    ls = _with_state_window(daily_ls, labels, windows)
    rows = []
    for (signal_name, horizon, state_label, window_id), group in ic.groupby(
        ["signal_name", "horizon", "state_label", "window_id"]
    ):
        ic_sample = group["ic"].dropna()
        ls_sample = ls[
            ls["signal_name"].eq(signal_name)
            & ls["horizon"].eq(horizon)
            & ls["state_label"].eq(state_label)
            & ls["window_id"].eq(window_id)
        ]["long_short_return"].dropna()
        rows.append(
            {
                "signal_name": signal_name,
                "horizon": int(horizon),
                "state_label": state_label,
                "window_id": int(window_id),
                "mean_ic": float(ic_sample.mean()) if not ic_sample.empty else np.nan,
                "positive_ic_rate": float((ic_sample > 0).mean()) if not ic_sample.empty else np.nan,
                "n_ic_dates": int(ic_sample.shape[0]),
                "mean_long_short_return": float(ls_sample.mean()) if not ls_sample.empty else np.nan,
                "hit_rate": float((ls_sample > 0).mean()) if not ls_sample.empty else np.nan,
                "n_return_dates": int(ls_sample.shape[0]),
                "thin_sample_warning": bool(ic_sample.shape[0] < 20 or ls_sample.shape[0] < 20),
            }
        )
    return pd.DataFrame(rows)


def candidate_state_stability_summary(rolling_attr: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for (signal_name, horizon, state_label), group in rolling_attr.groupby(["signal_name", "horizon", "state_label"]):
        valid = group.dropna(subset=["mean_ic"])
        if valid.empty:
            continue
        full_mean = float(valid["mean_ic"].mean())
        signs = np.sign(valid["mean_ic"])
        nonzero = signs[signs != 0]
        dominant_sign = np.sign(full_mean)
        rows.append(
            {
                "signal_name": signal_name,
                "horizon": int(horizon),
                "state_label": state_label,
                "window_count": int(valid.shape[0]),
                "valid_window_count": int((valid["n_ic_dates"] >= 20).sum()),
                "mean_window_ic": full_mean,
                "ic_window_std": float(valid["mean_ic"].std(ddof=0)) if valid.shape[0] > 1 else np.nan,
                "same_sign_window_rate": float((nonzero == dominant_sign).mean()) if len(nonzero) else np.nan,
                "mean_window_long_short_return": float(valid["mean_long_short_return"].mean()),
                "return_same_sign_window_rate": float(
                    (np.sign(valid["mean_long_short_return"]) == np.sign(valid["mean_long_short_return"].mean())).mean()
                )
                if valid["mean_long_short_return"].notna().any()
                else np.nan,
                "min_window_ic_dates": int(valid["n_ic_dates"].min()),
                "thin_window_count": int(valid["thin_sample_warning"].sum()),
                "stable_direction_warning": bool(len(nonzero) > 0 and (nonzero == dominant_sign).mean() < 0.75),
                "thin_sample_warning": bool(valid["n_ic_dates"].min() < 20),
            }
        )
    return pd.DataFrame(rows)


def drawdown_clustering_drift(daily_ls: pd.DataFrame, labels: pd.DataFrame, windows: pd.Series) -> pd.DataFrame:
    data = _with_state_window(daily_ls, labels, windows).dropna(subset=["long_short_return"])
    rows = []
    for (signal_name, horizon, window_id), group in data.groupby(["signal_name", "horizon", "window_id"]):
        threshold = group["long_short_return"].quantile(0.10)
        group = group.copy()
        group["tail_loss"] = group["long_short_return"].le(threshold)
        total_tail = int(group["tail_loss"].sum())
        state_counts = group["state_label"].value_counts()
        for state_label in STATE_ORDER:
            sample = group[group["state_label"].eq(state_label)]
            state_share = float(state_counts.get(state_label, 0) / len(group)) if len(group) else np.nan
            tail_count = int(sample["tail_loss"].sum()) if not sample.empty else 0
            tail_share = float(tail_count / total_tail) if total_tail else np.nan
            rows.append(
                {
                    "signal_name": signal_name,
                    "horizon": int(horizon),
                    "window_id": int(window_id),
                    "state_label": state_label,
                    "tail_loss_threshold": float(threshold),
                    "state_dates": int(sample.shape[0]),
                    "tail_loss_dates": tail_count,
                    "tail_loss_rate": float(sample["tail_loss"].mean()) if not sample.empty else np.nan,
                    "tail_loss_concentration_ratio": tail_share / state_share if state_share and pd.notna(tail_share) else np.nan,
                    "thin_sample_warning": bool(sample.shape[0] < 20),
                }
            )
    return pd.DataFrame(rows)


def rolling_conditional_rankings(rolling_attr: pd.DataFrame) -> pd.DataFrame:
    ranked = rolling_attr.copy()
    ranked["ic_rank_in_window_state"] = ranked.groupby(["window_id", "horizon", "state_label"])["mean_ic"].rank(
        ascending=False, method="min"
    )
    ranked["return_rank_in_window_state"] = ranked.groupby(["window_id", "horizon", "state_label"])[
        "mean_long_short_return"
    ].rank(ascending=False, method="min")
    return ranked.sort_values(["window_id", "horizon", "state_label", "ic_rank_in_window_state"])


def detector_consistency_diagnostics(
    rolling_attr: pd.DataFrame,
    stability: pd.DataFrame,
    freq_drift: pd.DataFrame,
) -> pd.DataFrame:
    rows = []
    for (signal_name, horizon), group in rolling_attr.groupby(["signal_name", "horizon"]):
        by_window = []
        for window_id, wgroup in group.groupby("window_id"):
            if wgroup["mean_ic"].notna().sum() < 2:
                continue
            best = wgroup.loc[wgroup["mean_ic"].idxmax()]
            worst = wgroup.loc[wgroup["mean_ic"].idxmin()]
            by_window.append(
                {
                    "window_id": int(window_id),
                    "best_state": best["state_label"],
                    "worst_state": worst["state_label"],
                    "state_ic_range": float(wgroup["mean_ic"].max() - wgroup["mean_ic"].min()),
                }
            )
        if not by_window:
            continue
        window_df = pd.DataFrame(by_window)
        best_mode = window_df["best_state"].mode().iloc[0]
        worst_mode = window_df["worst_state"].mode().iloc[0]
        rows.append(
            {
                "signal_name": signal_name,
                "horizon": int(horizon),
                "window_count": int(window_df.shape[0]),
                "modal_best_state": best_mode,
                "modal_best_state_rate": float(window_df["best_state"].eq(best_mode).mean()),
                "modal_worst_state": worst_mode,
                "modal_worst_state_rate": float(window_df["worst_state"].eq(worst_mode).mean()),
                "mean_state_ic_range": float(window_df["state_ic_range"].mean()),
                "min_state_ic_range": float(window_df["state_ic_range"].min()),
                "max_state_ic_range": float(window_df["state_ic_range"].max()),
                "stable_best_worst_warning": bool(
                    window_df["best_state"].eq(best_mode).mean() < 0.75
                    or window_df["worst_state"].eq(worst_mode).mean() < 0.75
                ),
            }
        )
    consistency = pd.DataFrame(rows)
    if consistency.empty:
        return consistency
    max_freq_drift = freq_drift.groupby("window_id")["abs_ratio_drift"].max().mean()
    consistency["mean_max_state_frequency_drift"] = float(max_freq_drift)
    consistency["detector_usefulness_persistent"] = (
        (consistency["mean_state_ic_range"] >= 0.02)
        & (consistency["modal_best_state_rate"] >= 0.50)
        & (consistency["modal_worst_state_rate"] >= 0.50)
    )
    return consistency


def monitoring_alerts(
    freq_drift: pd.DataFrame,
    transition_drift: pd.DataFrame,
    stability: pd.DataFrame,
    drawdown_drift: pd.DataFrame,
    consistency: pd.DataFrame,
) -> pd.DataFrame:
    rows = []
    for _, row in freq_drift[freq_drift["abs_ratio_drift"].ge(0.10)].iterrows():
        rows.append(
            {
                "alert_type": "STATE_FREQUENCY_DRIFT",
                "severity": "WATCH",
                "signal_name": None,
                "horizon": None,
                "state_label": row["state_label"],
                "window_id": int(row["window_id"]),
                "detail": f"state ratio drift {row['ratio_drift']:.3f}",
            }
        )
    for _, row in transition_drift[transition_drift["transition_ratio_drift"].abs().ge(0.08)].iterrows():
        rows.append(
            {
                "alert_type": "STATE_TRANSITION_DRIFT",
                "severity": "WATCH",
                "signal_name": None,
                "horizon": None,
                "state_label": row["state_transition"],
                "window_id": int(row["window_id"]),
                "detail": f"transition ratio drift {row['transition_ratio_drift']:.3f}",
            }
        )
    for _, row in stability[stability["thin_sample_warning"] | stability["stable_direction_warning"]].iterrows():
        severity = "THIN_SAMPLE" if row["thin_sample_warning"] else "WATCH"
        rows.append(
            {
                "alert_type": "CANDIDATE_STATE_STABILITY",
                "severity": severity,
                "signal_name": row["signal_name"],
                "horizon": int(row["horizon"]),
                "state_label": row["state_label"],
                "window_id": None,
                "detail": (
                    f"same-sign rate {row['same_sign_window_rate']:.3f}; "
                    f"min window dates {row['min_window_ic_dates']}"
                ),
            }
        )
    for _, row in drawdown_drift[drawdown_drift["tail_loss_concentration_ratio"].ge(1.50)].iterrows():
        rows.append(
            {
                "alert_type": "DRAWDOWN_CLUSTERING",
                "severity": "WATCH",
                "signal_name": row["signal_name"],
                "horizon": int(row["horizon"]),
                "state_label": row["state_label"],
                "window_id": int(row["window_id"]),
                "detail": f"tail-loss concentration ratio {row['tail_loss_concentration_ratio']:.3f}",
            }
        )
    for _, row in consistency[consistency["stable_best_worst_warning"]].iterrows():
        rows.append(
            {
                "alert_type": "BEST_WORST_STATE_INSTABILITY",
                "severity": "WATCH",
                "signal_name": row["signal_name"],
                "horizon": int(row["horizon"]),
                "state_label": None,
                "window_id": None,
                "detail": (
                    f"best-state rate {row['modal_best_state_rate']:.3f}; "
                    f"worst-state rate {row['modal_worst_state_rate']:.3f}"
                ),
            }
        )
    return pd.DataFrame(rows)


def dashboard_summary(
    freq_drift: pd.DataFrame,
    stability: pd.DataFrame,
    consistency: pd.DataFrame,
    alerts: pd.DataFrame,
) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "metric": "max_abs_state_frequency_drift",
                "value": float(freq_drift["abs_ratio_drift"].max()),
                "interpretation": "Lower is more stable; values above 0.10 are watch items.",
            },
            {
                "metric": "candidate_state_pairs_with_thin_windows",
                "value": int(stability["thin_sample_warning"].sum()),
                "interpretation": "Thin state/candidate slices should not be overinterpreted.",
            },
            {
                "metric": "candidate_state_pairs_with_direction_instability",
                "value": int(stability["stable_direction_warning"].sum()),
                "interpretation": "Sign instability weakens claims of repeatable conditional behavior.",
            },
            {
                "metric": "h10_or_h20_relationships_persistent",
                "value": int(
                    consistency[
                        consistency["horizon"].isin([10, 20]) & consistency["detector_usefulness_persistent"]
                    ].shape[0]
                ),
                "interpretation": "Persistent means differentiated enough and not purely one-window best/worst behavior.",
            },
            {
                "metric": "total_monitoring_alerts",
                "value": int(alerts.shape[0]),
                "interpretation": "Alerts are monitoring flags, not downgrade or promotion decisions.",
            },
        ]
    )


def write_note(
    dashboard: pd.DataFrame,
    consistency: pd.DataFrame,
    stability: pd.DataFrame,
    freq_drift: pd.DataFrame,
    alerts: pd.DataFrame,
) -> None:
    dashboard_table = dashboard.to_markdown(index=False, floatfmt=".6f")
    consistency_focus = consistency[consistency["horizon"].isin([10, 20])].copy()
    consistency_table = consistency_focus.to_markdown(index=False, floatfmt=".6f")
    stability_focus = stability[
        stability["horizon"].isin([10, 20])
        & stability["state_label"].isin(["ABSORPTION", "PROPAGATION", "UNRESOLVED_STRESS", "NORMALIZATION"])
    ].copy()
    stability_table = stability_focus.head(40).to_markdown(index=False, floatfmt=".6f")
    drift_table = (
        freq_drift.sort_values("abs_ratio_drift", ascending=False)
        .head(12)
        .to_markdown(index=False, floatfmt=".6f")
    )
    alert_table = alerts.head(40).to_markdown(index=False, floatfmt=".6f") if not alerts.empty else "No alerts generated."

    note = f"""# Transition-State Detector Monitoring Framework v1

Date: 2026-05-21

Run id: `{RUN_ID}`

Detector input: `{DETECTOR_RUN_ID}`

Attribution input: `{ATTRIBUTION_RUN_ID}`

Status: RESEARCH_ONLY_MONITORING_FRAMEWORK

## Research-Only Guardrail

{RESEARCH_ONLY_GUARDRAIL}

This monitoring framework does not refine detector labels, optimize thresholds, create alpha candidates, or claim deployment readiness. It tracks whether detector-conditioned attribution relationships are stable enough to justify future conditional-validation research.

## Dashboard Summary

{dashboard_table}

## Detector Usefulness Persistence

{consistency_table}

## Candidate-State Stability

{stability_table}

## Largest State Frequency Drift

{drift_table}

## Monitoring Alerts

{alert_table}

## Interpretation

The detector continues to look behaviorally meaningful only where candidate-state relationships are directionally repeatable, supported by adequate samples, and not dominated by one monitoring window. Thin slices and unstable best/worst states should remain watch items.

## Recommendation

Keep the Transition-State Composite Detector in research-only monitoring. The next appropriate step is to rerun this monitor after the next inventory monitoring cycle and compare alert persistence. Do not route the detector into production, validation, portfolio, ML, blending, or optimization from this monitoring pass.

## Artifacts

- `rolling_attribution_stability.csv`
- `state_frequency_drift.csv`
- `state_transition_drift.csv`
- `detector_consistency_diagnostics.csv`
- `candidate_state_stability_summary.csv`
- `instability_alerts.csv`
- `rolling_conditional_rankings.csv`
- `transition_persistence_diagnostics.csv`
- `drawdown_clustering_drift.csv`
- `monitoring_dashboard_summary.csv`
- `window_metadata.csv`
- `manifest.json`
"""
    NOTE_PATH.write_text(note)


def write_manifest(artifacts: list[str], labels: pd.DataFrame, daily_ic: pd.DataFrame) -> None:
    manifest = {
        "run_id": RUN_ID,
        "detector_run_id": DETECTOR_RUN_ID,
        "attribution_run_id": ATTRIBUTION_RUN_ID,
        "status": "RESEARCH_ONLY_MONITORING_FRAMEWORK",
        "research_only_guardrail": RESEARCH_ONLY_GUARDRAIL,
        "state_labels": STATE_ORDER,
        "monitor_windows": MONITOR_WINDOWS,
        "candidate_panels_monitored": sorted(daily_ic["signal_name"].unique().tolist()),
        "date_count": int(labels.shape[0]),
        "start_date": str(labels.index.min().date()),
        "end_date": str(labels.index.max().date()),
        "artifacts": artifacts,
        "intentional_non_changes": {
            "detector_labels_modified": False,
            "thresholds_optimized": False,
            "detector_usage_promoted": False,
            "production_routing_changed": False,
            "portfolio_ml_blending_optimization_route_changed": False,
            "gates_schemas_governance_changed": False,
            "performance_tuning_performed": False,
        },
    }
    (OUT_DIR / "manifest.json").write_text(json.dumps(manifest, indent=2))


def main() -> None:
    _ensure_dirs()
    labels, daily_ic, daily_ls, _baseline = load_inputs()
    windows = assign_windows(labels)

    metadata = window_metadata(labels, windows)
    freq_drift = state_frequency_drift(labels, windows)
    transition_drift = state_transition_drift(labels, windows)
    persistence = transition_persistence(labels, windows)
    rolling_attr = rolling_attribution_stability(daily_ic, daily_ls, labels, windows)
    stability = candidate_state_stability_summary(rolling_attr)
    drawdown_drift = drawdown_clustering_drift(daily_ls, labels, windows)
    rankings = rolling_conditional_rankings(rolling_attr)
    consistency = detector_consistency_diagnostics(rolling_attr, stability, freq_drift)
    alerts = monitoring_alerts(freq_drift, transition_drift, stability, drawdown_drift, consistency)
    dashboard = dashboard_summary(freq_drift, stability, consistency, alerts)

    artifacts = [
        "rolling_attribution_stability.csv",
        "state_frequency_drift.csv",
        "state_transition_drift.csv",
        "detector_consistency_diagnostics.csv",
        "candidate_state_stability_summary.csv",
        "instability_alerts.csv",
        "rolling_conditional_rankings.csv",
        "transition_persistence_diagnostics.csv",
        "drawdown_clustering_drift.csv",
        "monitoring_dashboard_summary.csv",
        "window_metadata.csv",
        "manifest.json",
    ]

    rolling_attr.to_csv(OUT_DIR / "rolling_attribution_stability.csv", index=False)
    freq_drift.to_csv(OUT_DIR / "state_frequency_drift.csv", index=False)
    transition_drift.to_csv(OUT_DIR / "state_transition_drift.csv", index=False)
    consistency.to_csv(OUT_DIR / "detector_consistency_diagnostics.csv", index=False)
    stability.to_csv(OUT_DIR / "candidate_state_stability_summary.csv", index=False)
    alerts.to_csv(OUT_DIR / "instability_alerts.csv", index=False)
    rankings.to_csv(OUT_DIR / "rolling_conditional_rankings.csv", index=False)
    persistence.to_csv(OUT_DIR / "transition_persistence_diagnostics.csv", index=False)
    drawdown_drift.to_csv(OUT_DIR / "drawdown_clustering_drift.csv", index=False)
    dashboard.to_csv(OUT_DIR / "monitoring_dashboard_summary.csv", index=False)
    metadata.to_csv(OUT_DIR / "window_metadata.csv", index=False)
    write_manifest(artifacts, labels, daily_ic)
    write_note(dashboard, consistency, stability, freq_drift, alerts)

    print(f"Wrote {RUN_ID} artifacts to {OUT_DIR}")
    print(f"Wrote research note to {NOTE_PATH}")
    print(RESEARCH_ONLY_GUARDRAIL)


if __name__ == "__main__":
    main()
