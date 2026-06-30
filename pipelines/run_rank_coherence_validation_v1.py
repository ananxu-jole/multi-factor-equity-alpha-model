from __future__ import annotations

import json
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parent.parent
PIPELINES = ROOT / "pipelines"
if str(PIPELINES) not in sys.path:
    sys.path.insert(0, str(PIPELINES))

from run_track_b_robustness_discovery_v3 import (  # noqa: E402
    baseline_panels,
    build_stress_states,
    load_inputs,
    orthogonality,
    score_signals,
    structural_summary,
)
from run_track_b_v6_focused_discovery import (  # noqa: E402
    active_coverage_summary,
    build_candidate_panels as build_v6_candidate_panels,
)


RUN_ID = "rank_coherence_validation_v1"
OUT_DIR = Path("artifacts/research") / RUN_ID
NOTE_PATH = Path("docs/research_notes/rank_coherence_validation_execution_v1.md")
DESIGN_NOTE = Path("docs/research_notes/rank_coherence_validation_design_v1.md")
REFINEMENT_DIR = Path("artifacts/research/rank_coherence_refinement_v1")
REFINEMENT_PANEL_DIR = REFINEMENT_DIR / "candidate_panels"
ALPHA_REFINEMENT_PANEL_DIR = Path("artifacts/research/alpha_family_diversification_refinement_v1/candidate_panels")
SOURCE_SIGNAL_DIR = Path("artifacts/panels/signals")

PRIMARY_SIGNAL = "relative_rank_turnover_resilience_overlap_adjusted_20"
PRIMARY_CANDIDATE_ID = "rank_coherence_churn_avoidance_02_overlap_adjusted"
VALIDATION_SIGNAL_MAP = {
    PRIMARY_SIGNAL: PRIMARY_CANDIDATE_ID,
    "relative_rank_turnover_resilience_20": "rank_coherence_churn_avoidance_02_anchor",
    "relative_rank_turnover_resilience_penalized_20": "rank_coherence_churn_avoidance_02_penalized",
    "nonhostile_transition_rank_coherence_20": "rank_coherence_regime_independent_02_anchor",
    "nonhostile_transition_rank_coherence_strict_20": "rank_coherence_regime_independent_02_strict",
    "nonhostile_transition_rank_coherence_smoothed_20": "rank_coherence_regime_independent_02_smoothed",
}
LINEAGE_CONTROLS = [
    "relative_rank_turnover_resilience_20",
    "relative_rank_turnover_resilience_penalized_20",
]
SIBLING_CONTROLS = [
    "nonhostile_transition_rank_coherence_20",
    "nonhostile_transition_rank_coherence_strict_20",
    "nonhostile_transition_rank_coherence_smoothed_20",
]
VALIDATION_SIGNALS = [PRIMARY_SIGNAL, *LINEAGE_CONTROLS, *SIBLING_CONTROLS]
PRIMARY_HORIZONS = (10, 20)
HORIZONS = (1, 5, 10, 20)
WFV_WINDOWS = 4

PERSISTENCE_REFERENCE_SIGNALS = [
    "post_drawdown_persistence_20",
    "post_drawdown_persistence_churn_adjusted_20",
    "post_drawdown_persistence_core_20",
    "post_drawdown_persistence_smoothed_20",
    "post_drawdown_persistence_strict_20",
]
DISPERSION_REFERENCE_SIGNALS = [
    "dispersion_transition_acceleration_20",
    "dispersion_transition_acceleration_smoothed_20",
    "dispersion_transition_acceleration_neutralized_20",
    "dispersion_transition_acceleration_alt_20",
    "dispersion_transition_acceleration_rising_state_20",
]
STRESS_PROXY_SOURCE_SIGNALS = [
    "failed_breakout_reversal_20",
    "failed_breakout_reversal_20_low_breadth",
    "percentile_rank_stability_20_downtrend",
    "smooth_trend_persistence_60_downtrend",
]

RESEARCH_ONLY_GUARDRAIL = (
    "Research-only rank-coherence validation execution for one frozen candidate. "
    "No refinement, new variants, governance mutation, threshold change, production "
    "registration, ML integration, or candidate promotion/demotion is performed."
)


def _ensure_dirs() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    NOTE_PATH.parent.mkdir(parents=True, exist_ok=True)


def _load_long_panel(path: Path) -> pd.DataFrame:
    panel_long = pd.read_parquet(path)
    date_col = "date" if "date" in panel_long.columns else "Date"
    required = {date_col, "ticker", "signal_value"}
    missing = required - set(panel_long.columns)
    if missing:
        raise ValueError(f"Panel {path} missing required columns: {sorted(missing)}")
    panel = panel_long.pivot_table(index=date_col, columns="ticker", values="signal_value", aggfunc="last")
    panel.index = pd.to_datetime(panel.index)
    return panel.sort_index().sort_index(axis=1)


def _load_validation_signals(close: pd.DataFrame) -> dict[str, pd.DataFrame]:
    signals: dict[str, pd.DataFrame] = {}
    for signal_name in VALIDATION_SIGNALS:
        path = REFINEMENT_PANEL_DIR / f"{signal_name}.parquet"
        if not path.exists():
            raise FileNotFoundError(f"Missing frozen rank-coherence refinement panel: {path}")
        signals[signal_name] = _load_long_panel(path).reindex(index=close.index, columns=close.columns)
    return signals


def _load_alpha_ref(close: pd.DataFrame, signal_name: str) -> pd.DataFrame | None:
    path = ALPHA_REFINEMENT_PANEL_DIR / f"{signal_name}.parquet"
    if not path.exists():
        return None
    return _load_long_panel(path).reindex(index=close.index, columns=close.columns)


def _load_source_ref(close: pd.DataFrame, signal_name: str) -> pd.DataFrame | None:
    path = SOURCE_SIGNAL_DIR / f"{signal_name}.parquet"
    if not path.exists():
        return None
    panel = pd.read_parquet(path)
    panel.index = pd.to_datetime(panel.index)
    return panel.reindex(index=close.index, columns=close.columns)


def _reference_panels(signals: dict[str, pd.DataFrame], panels: dict[str, pd.DataFrame], benchmark: pd.Series) -> dict[str, pd.DataFrame]:
    refs = baseline_panels(signals, panels, benchmark)
    close = panels["close"]
    for signal_name in PERSISTENCE_REFERENCE_SIGNALS:
        panel = _load_alpha_ref(close, signal_name)
        if panel is not None:
            refs[f"persistence::{signal_name}"] = panel
    for signal_name in DISPERSION_REFERENCE_SIGNALS:
        panel = _load_alpha_ref(close, signal_name)
        if panel is not None:
            refs[f"dispersion::{signal_name}"] = panel
    for signal_name in STRESS_PROXY_SOURCE_SIGNALS:
        panel = _load_source_ref(close, signal_name)
        if panel is not None:
            refs[f"stress_proxy::{signal_name}"] = panel
    for name, panel in signals.items():
        refs[f"sibling_rank_coherence::{name}"] = panel
    return refs


def _wfv_for_horizons(daily_ics: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    window_rows: list[dict[str, object]] = []
    summary_rows: list[dict[str, object]] = []
    for signal_name in VALIDATION_SIGNALS:
        for horizon in PRIMARY_HORIZONS:
            series = daily_ics[
                daily_ics["signal_name"].eq(signal_name) & daily_ics["horizon"].eq(horizon)
            ].set_index("Date")["ic"].dropna().sort_index()
            if len(series) < WFV_WINDOWS * 25:
                continue
            splits = np.array_split(series.index, WFV_WINDOWS)
            window_means: list[float] = []
            for idx, dates in enumerate(splits, start=1):
                sample = series.loc[dates]
                mean_ic = float(sample.mean())
                std_ic = float(sample.std(ddof=0))
                window_means.append(mean_ic)
                window_rows.append(
                    {
                        "signal_name": signal_name,
                        "candidate_id": VALIDATION_SIGNAL_MAP[signal_name],
                        "horizon": horizon,
                        "window": idx,
                        "start_date": str(sample.index.min().date()),
                        "end_date": str(sample.index.max().date()),
                        "mean_test_ic": mean_ic,
                        "test_ic_ir": mean_ic / std_ic if std_ic > 0 else np.nan,
                        "positive_ic_rate": float((sample > 0).mean()),
                        "valid_ic_dates": int(len(sample)),
                    }
                )
            arr = np.array(window_means, dtype=float)
            std = float(np.std(arr)) if len(arr) > 1 else np.nan
            summary_rows.append(
                {
                    "signal_name": signal_name,
                    "candidate_id": VALIDATION_SIGNAL_MAP[signal_name],
                    "horizon": horizon,
                    "n_windows": int(len(arr)),
                    "effective_mean_test_ic": float(np.mean(arr)),
                    "effective_test_ic_ir": float(np.mean(arr) / std) if pd.notna(std) and std > 0 else np.nan,
                    "persistence": float((arr > 0).mean()),
                    "sign_consistency": float(max((arr > 0).mean(), (arr < 0).mean())),
                    "one_window_dominance": float(np.max(np.abs(arr)) / np.sum(np.abs(arr))) if np.sum(np.abs(arr)) > 0 else np.nan,
                }
            )
    return pd.DataFrame(summary_rows), pd.DataFrame(window_rows)


def _window_concentration(window_results: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for (signal_name, horizon), group in window_results.groupby(["signal_name", "horizon"]):
        group = group.sort_values("window")
        values = group["mean_test_ic"].astype(float)
        positive = values[values > 0]
        rows.append(
            {
                "signal_name": signal_name,
                "candidate_id": VALIDATION_SIGNAL_MAP[signal_name],
                "horizon": int(horizon),
                "positive_window_count": int((values > 0).sum()),
                "negative_window_count": int((values <= 0).sum()),
                "min_window_ic": float(values.min()),
                "max_window_ic": float(values.max()),
                "window_ic_range": float(values.max() - values.min()),
                "positive_ic_sum": float(positive.sum()) if not positive.empty else 0.0,
                "largest_positive_window_share": float(positive.max() / positive.sum()) if positive.sum() > 0 else np.nan,
                "recent_window_ic": float(group.iloc[-1]["mean_test_ic"]),
                "recent_window_positive_ic_rate": float(group.iloc[-1]["positive_ic_rate"]),
                "valid_ic_dates_min": int(group["valid_ic_dates"].min()),
                "valid_ic_dates_max": int(group["valid_ic_dates"].max()),
            }
        )
    return pd.DataFrame(rows)


def _state_attribution_for_horizons(daily_ics: pd.DataFrame, states: pd.DataFrame, horizons: tuple[int, ...]) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for signal_name in VALIDATION_SIGNALS:
        for horizon in horizons:
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
                        "candidate_id": VALIDATION_SIGNAL_MAP[signal_name],
                        "horizon": int(horizon),
                        "state": state,
                        "n_dates": int(len(sample)),
                        "mean_ic": float(sample.mean()) if len(sample) else np.nan,
                        "ic_ir": float(sample.mean() / std) if pd.notna(std) and std > 0 else np.nan,
                        "positive_ic_rate": float((sample > 0).mean()) if len(sample) else np.nan,
                    }
                )
    return pd.DataFrame(rows)


def _top_corr_by_scope(orth: pd.DataFrame, signal_name: str, scope: str) -> tuple[float, str | None]:
    group = orth[
        orth["signal_name"].eq(signal_name)
        & orth["comparison"].str.startswith(f"{scope}::", na=False)
    ].dropna(subset=["abs_value_corr"])
    if scope == "sibling_rank_coherence":
        group = group[~group["comparison"].eq(f"sibling_rank_coherence::{signal_name}")]
    if group.empty:
        return np.nan, None
    top = group.sort_values("abs_value_corr", ascending=False).iloc[0]
    return float(top["abs_value_corr"]), str(top["comparison"])


def _contamination_review(orth: pd.DataFrame, state_attr: pd.DataFrame, stress_attr: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for signal_name in VALIDATION_SIGNALS:
        persistence_corr, persistence_peer = _top_corr_by_scope(orth, signal_name, "persistence")
        dispersion_corr, dispersion_peer = _top_corr_by_scope(orth, signal_name, "dispersion")
        stress_corr, stress_peer = _top_corr_by_scope(orth, signal_name, "stress_proxy")
        sibling_corr, sibling_peer = _top_corr_by_scope(orth, signal_name, "sibling_rank_coherence")
        stress_states = stress_attr[stress_attr["signal_name"].eq(signal_name)]
        strongest_stress = stress_states.sort_values("mean_ic", ascending=False).iloc[0] if not stress_states.empty else None
        concept_states = state_attr[state_attr["signal_name"].eq(signal_name)]
        strongest_concept = concept_states.sort_values("mean_ic", ascending=False).iloc[0] if not concept_states.empty else None
        rows.append(
            {
                "signal_name": signal_name,
                "candidate_id": VALIDATION_SIGNAL_MAP[signal_name],
                "max_persistence_abs_corr": persistence_corr,
                "top_persistence_reference": persistence_peer,
                "max_stress_repair_abs_corr": stress_corr,
                "top_stress_repair_reference": stress_peer,
                "max_dispersion_abs_corr": dispersion_corr,
                "top_dispersion_reference": dispersion_peer,
                "max_sibling_rank_coherence_abs_corr": sibling_corr,
                "top_sibling_rank_coherence_reference": sibling_peer,
                "strongest_stress_state": strongest_stress["state"] if strongest_stress is not None else None,
                "strongest_stress_state_mean_ic": float(strongest_stress["mean_ic"]) if strongest_stress is not None else np.nan,
                "strongest_concept_state": strongest_concept["state"] if strongest_concept is not None else None,
                "strongest_concept_state_mean_ic": float(strongest_concept["mean_ic"]) if strongest_concept is not None else np.nan,
                "persistence_contamination_flag": bool(pd.notna(persistence_corr) and persistence_corr > 0.35),
                "stress_repair_contamination_flag": bool(pd.notna(stress_corr) and stress_corr > 0.35),
                "dispersion_contamination_flag": bool(pd.notna(dispersion_corr) and dispersion_corr > 0.35),
                "sibling_duplicate_flag": bool(pd.notna(sibling_corr) and sibling_corr > 0.85),
            }
        )
    return pd.DataFrame(rows)


def _primary_horizon_summary(scores: pd.DataFrame) -> pd.DataFrame:
    h10 = scores[scores["horizon"].eq(10)].rename(
        columns={"mean_ic": "h10_mean_ic", "ic_ir": "h10_ic_ir", "positive_ic_rate": "h10_positive_ic_rate", "n_dates": "h10_n_dates"}
    )
    h20 = scores[scores["horizon"].eq(20)].rename(
        columns={"mean_ic": "h20_mean_ic", "ic_ir": "h20_ic_ir", "positive_ic_rate": "h20_positive_ic_rate", "n_dates": "h20_n_dates"}
    )
    best = scores.loc[scores.groupby("signal_name")["abs_mean_ic"].idxmax()].drop(
        columns=["best_horizon"], errors="ignore"
    ).rename(columns={"horizon": "best_horizon", "mean_ic": "best_mean_ic"})
    out = (
        best[["signal_name", "best_horizon", "best_mean_ic", "ic_ir", "positive_ic_rate"]]
        .merge(h10[["signal_name", "h10_mean_ic", "h10_ic_ir", "h10_positive_ic_rate", "h10_n_dates"]], on="signal_name", how="left")
        .merge(h20[["signal_name", "h20_mean_ic", "h20_ic_ir", "h20_positive_ic_rate", "h20_n_dates"]], on="signal_name", how="left")
    )
    out["candidate_id"] = out["signal_name"].map(VALIDATION_SIGNAL_MAP)
    return out


def _validation_summary(
    scores: pd.DataFrame,
    structural: pd.DataFrame,
    wfv: pd.DataFrame,
    concentration: pd.DataFrame,
    orth_summary: pd.DataFrame,
    active: pd.DataFrame,
    contamination: pd.DataFrame,
) -> pd.DataFrame:
    primary = _primary_horizon_summary(scores)
    w10 = wfv[wfv["horizon"].eq(10)].add_prefix("h10_wfv_").rename(columns={"h10_wfv_signal_name": "signal_name"})
    w20 = wfv[wfv["horizon"].eq(20)].add_prefix("h20_wfv_").rename(columns={"h20_wfv_signal_name": "signal_name"})
    c10 = concentration[concentration["horizon"].eq(10)].add_prefix("h10_window_").rename(columns={"h10_window_signal_name": "signal_name"})
    c20 = concentration[concentration["horizon"].eq(20)].add_prefix("h20_window_").rename(columns={"h20_window_signal_name": "signal_name"})
    summary = (
        primary.merge(structural, on="signal_name", how="left")
        .merge(active, on="signal_name", how="left")
        .merge(w10.drop(columns=["h10_wfv_horizon"], errors="ignore"), on="signal_name", how="left")
        .merge(w20.drop(columns=["h20_wfv_horizon"], errors="ignore"), on="signal_name", how="left")
        .merge(c10.drop(columns=["h10_window_horizon"], errors="ignore"), on="signal_name", how="left")
        .merge(c20.drop(columns=["h20_window_horizon"], errors="ignore"), on="signal_name", how="left")
        .merge(orth_summary, on="signal_name", how="left")
        .merge(contamination, on=["signal_name", "candidate_id"], how="left")
    )
    summary["role"] = summary["signal_name"].map(
        {
            PRIMARY_SIGNAL: "primary_candidate",
            "relative_rank_turnover_resilience_20": "lineage_anchor",
            "relative_rank_turnover_resilience_penalized_20": "lineage_control",
            "nonhostile_transition_rank_coherence_20": "sibling_context",
            "nonhostile_transition_rank_coherence_strict_20": "sibling_context",
            "nonhostile_transition_rank_coherence_smoothed_20": "sibling_context",
        }
    )
    return summary.sort_values(["role", "signal_name"])


def _classify(summary: pd.DataFrame) -> tuple[str, list[str], str]:
    primary = summary[summary["signal_name"].eq(PRIMARY_SIGNAL)].iloc[0]
    risks: list[str] = []
    if primary["h10_mean_ic"] <= 0 or primary["h20_mean_ic"] <= 0:
        risks.append("primary_h10_h20_not_both_positive")
    if primary["h10_positive_ic_rate"] < 0.52 or primary["h20_positive_ic_rate"] < 0.52:
        risks.append("primary_positive_ic_rate_weak")
    if primary.get("h10_wfv_persistence", 0) < 0.75:
        risks.append("h10_wfv_persistence_weak")
    if primary.get("h20_wfv_persistence", 0) < 0.75:
        risks.append("h20_wfv_persistence_weak")
    if primary.get("h10_window_largest_positive_window_share", 1) > 0.70:
        risks.append("h10_window_concentration")
    if primary.get("h20_window_largest_positive_window_share", 1) > 0.70:
        risks.append("h20_window_concentration")
    if primary.get("max_persistence_abs_corr", 1) > 0.35:
        risks.append("persistence_similarity")
    if primary.get("max_stress_repair_abs_corr", 1) > 0.35:
        risks.append("stress_repair_similarity")
    if primary.get("max_dispersion_abs_corr", 1) > 0.35:
        risks.append("dispersion_similarity")
    if primary.get("max_sibling_rank_coherence_abs_corr", 0) > 0.85:
        risks.append("sibling_duplicate_risk")
    if primary.get("active_date_ratio", 0) < 0.15:
        risks.append("active_coverage_low")

    core_positive = primary["h10_mean_ic"] > 0 and primary["h20_mean_ic"] > 0
    contamination_clean = (
        primary.get("max_persistence_abs_corr", 1) <= 0.35
        and primary.get("max_stress_repair_abs_corr", 1) <= 0.35
        and primary.get("max_dispersion_abs_corr", 1) <= 0.35
    )
    if not risks:
        return (
            "VALIDATION PASS",
            risks,
            "Primary candidate passed fixed h10/h20, WFV, concentration, active-coverage, and contamination checks.",
        )
    if core_positive and contamination_clean:
        return (
            "CONDITIONAL VALIDATION CANDIDATE",
            risks,
            "Primary candidate retained positive h10/h20 validation evidence and clean cross-family contamination, but validation risks remain.",
        )
    if core_positive:
        return (
            "CONDITIONAL VALIDATION CANDIDATE",
            risks,
            "Primary candidate retained positive h10/h20 validation evidence, but contamination or concentration risks prevent a pass.",
        )
    return (
        "VALIDATION FAIL",
        risks,
        "Primary candidate failed core h10/h20 validation evidence under the frozen validation scope.",
    )


def _fmt(value: object) -> str:
    return "nan" if pd.isna(value) else f"{float(value):.6f}"


def _write_note(
    summary: pd.DataFrame,
    scores: pd.DataFrame,
    windows: pd.DataFrame,
    concentration: pd.DataFrame,
    state_attr: pd.DataFrame,
    contamination: pd.DataFrame,
    outcome: str,
    risks: list[str],
    rationale: str,
) -> None:
    primary = summary[summary["signal_name"].eq(PRIMARY_SIGNAL)].iloc[0]
    hrows = scores[scores["signal_name"].eq(PRIMARY_SIGNAL)].sort_values("horizon")
    win_primary = windows[windows["signal_name"].eq(PRIMARY_SIGNAL)].sort_values(["horizon", "window"])
    state_primary = state_attr[state_attr["signal_name"].eq(PRIMARY_SIGNAL)].sort_values("mean_ic", ascending=False)
    contam_primary = contamination[contamination["signal_name"].eq(PRIMARY_SIGNAL)]
    survived = outcome in {"VALIDATION PASS", "CONDITIONAL VALIDATION CANDIDATE"}
    serious = survived and primary["h10_mean_ic"] > 0 and primary["h20_mean_ic"] > 0
    lines = [
        "# Project Underdog - Rank-Coherence Validation Execution v1",
        "",
        "Date: 2026-06-19",
        "",
        f"Run id: `{RUN_ID}`",
        "",
        f"Primary candidate: `{PRIMARY_CANDIDATE_ID}`",
        "",
        f"Representative signal: `{PRIMARY_SIGNAL}`",
        "",
        "Scope: research-only validation execution using the frozen package from `rank_coherence_validation_design_v1.md`. No new variants, refinement, governance mutation, threshold change, production registration, ML implementation, candidate promotion, or candidate demotion was performed.",
        "",
        "## SECTION 1 - Executive Summary",
        "",
        "Validation scope:",
        f"- Primary frozen candidate: `{PRIMARY_CANDIDATE_ID}`.",
        "- Diagnostic controls: churn anchor, churn penalized sibling, and regime-independent rank-coherence siblings.",
        "- Horizons: h1, h5, h10, h20, with h10/h20 as primary validation horizons.",
        "- Diagnostics: WFV-style windows, horizon review, active coverage, concentration, state attribution, redundancy, and contamination review.",
        "",
        "Completion status: completed. Artifacts were written under `artifacts/research/rank_coherence_validation_v1/`.",
        "",
        f"Overall outcome: `{outcome}`.",
        f"Decision rationale: {rationale}",
        f"Review risks: `{'; '.join(risks) if risks else 'none'}`.",
        "",
        "Primary findings:",
        f"- h10 mean IC `{_fmt(primary['h10_mean_ic'])}`, IC IR `{_fmt(primary['h10_ic_ir'])}`, positive IC rate `{_fmt(primary['h10_positive_ic_rate'])}`.",
        f"- h20 mean IC `{_fmt(primary['h20_mean_ic'])}`, IC IR `{_fmt(primary['h20_ic_ir'])}`, positive IC rate `{_fmt(primary['h20_positive_ic_rate'])}`.",
        f"- h10 WFV persistence/sign consistency `{_fmt(primary.get('h10_wfv_persistence', np.nan))}` / `{_fmt(primary.get('h10_wfv_sign_consistency', np.nan))}`.",
        f"- h20 WFV persistence/sign consistency `{_fmt(primary.get('h20_wfv_persistence', np.nan))}` / `{_fmt(primary.get('h20_wfv_sign_consistency', np.nan))}`.",
        f"- Persistence/stress/dispersion max correlations `{_fmt(primary.get('max_persistence_abs_corr', np.nan))}` / `{_fmt(primary.get('max_stress_repair_abs_corr', np.nan))}` / `{_fmt(primary.get('max_dispersion_abs_corr', np.nan))}`.",
        "",
        "## SECTION 2 - Core Validation Results",
        "",
        "Primary candidate horizon metrics:",
        "",
        hrows[["signal_name", "horizon", "mean_ic", "ic_ir", "positive_ic_rate", "n_dates", "is_best_horizon"]].to_markdown(index=False),
        "",
        "Validation summary across candidate and controls:",
        "",
        summary[
            [
                "candidate_id",
                "signal_name",
                "role",
                "best_horizon",
                "h10_mean_ic",
                "h10_ic_ir",
                "h10_positive_ic_rate",
                "h20_mean_ic",
                "h20_ic_ir",
                "h20_positive_ic_rate",
                "active_date_ratio",
                "mean_active_coverage",
            ]
        ].to_markdown(index=False),
        "",
        "Coverage and concentration:",
        "",
        concentration[concentration["signal_name"].eq(PRIMARY_SIGNAL)].to_markdown(index=False),
        "",
        "## SECTION 3 - Walk-Forward Review",
        "",
        "WFV-style window results for the primary candidate:",
        "",
        win_primary[["horizon", "window", "start_date", "end_date", "mean_test_ic", "test_ic_ir", "positive_ic_rate", "valid_ic_dates"]].to_markdown(index=False),
        "",
        "Walk-forward interpretation: stability is judged by sign consistency, persistence across windows, recent-window behavior, and one-window dominance. Any weak window is treated as a validation risk, not a prompt to tune the formula.",
        "",
        "State attribution snapshot:",
        "",
        state_primary[["horizon", "state", "n_dates", "mean_ic", "ic_ir", "positive_ic_rate"]].head(12).to_markdown(index=False),
        "",
        "## SECTION 4 - Distinctiveness Review",
        "",
        "Contamination review for the primary candidate:",
        "",
        contam_primary.to_markdown(index=False),
        "",
        "Persistence contamination: validation reviewed persistence references from the diversification refinement set. High correlation would indicate a renamed persistence signal; lower correlation supports rank-coherence distinctiveness.",
        "",
        "Hostile/stress-repair contamination: validation reviewed source stress proxies and state attribution. Stress similarity remains a key risk if positive IC concentrates in stress-repair states.",
        "",
        "Dispersion contamination: validation reviewed dispersion-transition references. Low dispersion overlap supports separation from the exploratory dispersion family.",
        "",
        "Sibling contamination: high sibling/anchor correlation is expected for lineage continuity but cannot be counted as independent family-level evidence.",
        "",
        f"Does the candidate remain a legitimate rank-coherence signal? {'Yes, conditionally' if survived else 'No, not under this validation result'}. The mechanism remains rank-turnover resilience, but the result should be interpreted as one refined candidate lineage.",
        "",
        "## SECTION 5 - Validation Outcome",
        "",
        f"Classification: `{outcome}`",
        "",
        "This classification uses existing-style validation diagnostics only. It does not modify governance, change thresholds, register anything, or promote/demote any candidate.",
        "",
        "## SECTION 6 - Strategic Interpretation",
        "",
        "1. Has rank-coherence survived validation?",
        "",
        f"{'Yes, conditionally' if survived else 'No'}. The validation outcome is `{outcome}`.",
        "",
        "2. Is rank-coherence a credible alpha-family diversification success?",
        "",
        f"{'Yes, at candidate-thread level' if serious else 'Not conclusively'}. The evidence does not yet prove broad family-level success.",
        "",
        "3. Is evidence candidate-level or family-level?",
        "",
        "Candidate-level. The validated object is one refined rank-churn lineage with sibling controls, not multiple independent rank-coherence themes.",
        "",
        "4. What weaknesses remain?",
        "",
        f"`{'; '.join(risks) if risks else 'none recorded by the validation classifier'}`. Qualitative weaknesses include family concentration, h20-led evidence, and sibling/anchor redundancy.",
        "",
        "## SECTION 7 - Final Recommendation",
        "",
        "1. Validation outcome?",
        "",
        f"`{outcome}`.",
        "",
        "2. Key risks?",
        "",
        f"`{'; '.join(risks) if risks else 'none recorded by the validation classifier'}`.",
        "",
        "3. Should rank-coherence remain active research inventory?",
        "",
        f"{'Yes' if survived else 'Only as diagnostic research'}. The candidate should remain research-only unless a separate governance process later authorizes any inventory action.",
        "",
        "4. What should the next Codex task be?",
        "",
        "The next Codex task should be a review-only rank-coherence validation interpretation and integration-readiness review. It should decide whether to freeze the candidate as conditional research inventory, pursue further non-overlapping rank-coherence family breadth, or hold the track as diagnostic. It should not modify governance, change thresholds, register production candidates, add variants, implement ML, or promote/demote candidates.",
        "",
        "## Research Caveat",
        "",
        "This was a research-only validation execution. It does not register production artifacts, modify governance, change thresholds, implement ML, or promote/demote any candidate.",
    ]
    NOTE_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    warnings.filterwarnings("ignore", category=FutureWarning)
    warnings.filterwarnings("ignore", category=RuntimeWarning)
    _ensure_dirs()
    panels, benchmark = load_inputs()
    signals = _load_validation_signals(panels["close"])
    _, concept_states = build_v6_candidate_panels(panels, benchmark)
    registry = pd.DataFrame(
        [
            {
                "candidate_id": VALIDATION_SIGNAL_MAP[signal_name],
                "signal_name": signal_name,
                "role": "primary_candidate" if signal_name == PRIMARY_SIGNAL else "diagnostic_control",
                "family": "rank_coherence",
                "source_run": "rank_coherence_refinement_v1",
                "source_panel": str(REFINEMENT_PANEL_DIR / f"{signal_name}.parquet"),
                "research_status": "FROZEN_VALIDATION_CANDIDATE" if signal_name == PRIMARY_SIGNAL else "CONTROL_ONLY",
                "run_id": RUN_ID,
            }
            for signal_name in VALIDATION_SIGNALS
        ]
    )

    structural = structural_summary(signals)
    scores, daily_ics = score_signals(signals, panels["close"])
    stress_states = build_stress_states(panels["close"], benchmark)
    stress_attr = _state_attribution_for_horizons(daily_ics, stress_states, PRIMARY_HORIZONS)
    state_attr = _state_attribution_for_horizons(daily_ics, concept_states, PRIMARY_HORIZONS)
    wfv_summary, window_results = _wfv_for_horizons(daily_ics)
    concentration = _window_concentration(window_results)
    refs = _reference_panels(signals, panels, benchmark)
    orth = orthogonality(signals, refs)
    from run_track_b_v6_focused_discovery import _max_corr_table  # noqa: PLC0415

    orth_summary = _max_corr_table(orth)
    active = active_coverage_summary(signals)
    contamination = _contamination_review(orth, state_attr, stress_attr)
    summary = _validation_summary(scores, structural, wfv_summary, concentration, orth_summary, active, contamination)
    outcome, risks, rationale = _classify(summary)

    registry.to_csv(OUT_DIR / "validation_candidate_inventory.csv", index=False)
    summary.to_csv(OUT_DIR / "validation_summary.csv", index=False)
    scores.to_csv(OUT_DIR / "horizon_validation_metrics.csv", index=False)
    daily_ics.to_csv(OUT_DIR / "daily_ic_by_candidate_horizon.csv", index=False)
    wfv_summary.to_csv(OUT_DIR / "walk_forward_summary.csv", index=False)
    window_results.to_csv(OUT_DIR / "walk_forward_diagnostics.csv", index=False)
    concentration.to_csv(OUT_DIR / "concentration_review.csv", index=False)
    structural.to_csv(OUT_DIR / "structural_quality_summary.csv", index=False)
    active.to_csv(OUT_DIR / "coverage_review.csv", index=False)
    state_attr.to_csv(OUT_DIR / "state_attribution.csv", index=False)
    stress_attr.to_csv(OUT_DIR / "stress_state_attribution.csv", index=False)
    orth.to_csv(OUT_DIR / "redundancy_review.csv", index=False)
    orth_summary.to_csv(OUT_DIR / "orthogonality_summary.csv", index=False)
    contamination.to_csv(OUT_DIR / "contamination_review.csv", index=False)
    summary[summary["signal_name"].isin(VALIDATION_SIGNALS)].to_csv(OUT_DIR / "lineage_control_comparison.csv", index=False)
    (OUT_DIR / "manifest.json").write_text(
        json.dumps(
            {
                "run_id": RUN_ID,
                "research_only": True,
                "research_only_guardrail": RESEARCH_ONLY_GUARDRAIL,
                "design_note": str(DESIGN_NOTE),
                "primary_candidate_id": PRIMARY_CANDIDATE_ID,
                "primary_signal": PRIMARY_SIGNAL,
                "candidate_count": len(VALIDATION_SIGNALS),
                "new_variants_created": False,
                "additional_refinement_executed": False,
                "validation_executed": True,
                "governance_modified": False,
                "thresholds_modified": False,
                "production_registration": False,
                "ml_integration": False,
                "candidate_promotion_or_demotion": False,
                "outcome": outcome,
                "review_risks": risks,
                "outputs": {
                    "validation_candidate_inventory": str(OUT_DIR / "validation_candidate_inventory.csv"),
                    "validation_summary": str(OUT_DIR / "validation_summary.csv"),
                    "horizon_validation_metrics": str(OUT_DIR / "horizon_validation_metrics.csv"),
                    "walk_forward_diagnostics": str(OUT_DIR / "walk_forward_diagnostics.csv"),
                    "contamination_review": str(OUT_DIR / "contamination_review.csv"),
                    "coverage_review": str(OUT_DIR / "coverage_review.csv"),
                    "concentration_review": str(OUT_DIR / "concentration_review.csv"),
                    "manifest": str(OUT_DIR / "manifest.json"),
                },
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )
    _write_note(summary, scores, window_results, concentration, state_attr, contamination, outcome, risks, rationale)
    print(f"WROTE {OUT_DIR}")
    print(f"WROTE {NOTE_PATH}")
    print(f"OUTCOME {outcome}")
    print(f"RISKS {'; '.join(risks) if risks else 'none'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
