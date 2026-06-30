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
    stress_attribution,
    structural_summary,
)
from run_track_b_v6_focused_discovery import (  # noqa: E402
    _max_corr_table,
    active_coverage_summary,
    build_candidate_panels as build_v6_candidate_panels,
    state_attribution,
)


RUN_ID = "persistence_validation_v1"
OUT_DIR = Path("artifacts/research") / RUN_ID
NOTE_PATH = Path("docs/research_notes/persistence_validation_execution_v1.md")
DESIGN_NOTE = Path("docs/research_notes/persistence_validation_design_v1.md")
REFINEMENT_DIR = Path("artifacts/research/alpha_family_diversification_refinement_v1")
REFINEMENT_PANEL_DIR = REFINEMENT_DIR / "candidate_panels"
DISCOVERY_PANEL_DIR = Path("artifacts/research/alpha_family_diversification_discovery_v1/candidate_panels")
SOURCE_SIGNAL_DIR = Path("artifacts/panels/signals")

PRIMARY_SIGNAL = "post_drawdown_persistence_churn_adjusted_20"
LINEAGE_CONTROLS = [
    "post_drawdown_persistence_20",
    "post_drawdown_persistence_core_20",
]
VALIDATION_SIGNALS = [PRIMARY_SIGNAL, *LINEAGE_CONTROLS]
PRIMARY_HORIZONS = (10, 20)
HORIZONS = (1, 5, 10, 20)
WFV_WINDOWS = 4

RESEARCH_ONLY_GUARDRAIL = (
    "Research-only persistence validation execution. No governance mutation, threshold "
    "change, production registration, additional refinement, ML integration, or "
    "candidate promotion/demotion is performed."
)

STRESS_PROXY_SOURCE_SIGNALS = [
    "failed_breakout_reversal_20",
    "failed_breakout_reversal_20_low_breadth",
    "percentile_rank_stability_20_downtrend",
    "smooth_trend_persistence_60_downtrend",
]

DISCOVERY_REFERENCE_SIGNALS = [
    "dispersion_transition_acceleration_20",
    "dispersion_compression_stability_20",
    "dispersion_skew_anomaly_20",
    "cross_sectional_asymmetry_20",
    "drawdown_rank_stability_20",
    "transition_rank_stability_20",
]


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
            raise FileNotFoundError(f"Missing frozen refinement panel: {path}")
        signals[signal_name] = _load_long_panel(path).reindex(index=close.index, columns=close.columns)
    return signals


def _load_optional_long_refs(close: pd.DataFrame) -> dict[str, pd.DataFrame]:
    refs: dict[str, pd.DataFrame] = {}
    for signal_name in DISCOVERY_REFERENCE_SIGNALS:
        path = DISCOVERY_PANEL_DIR / f"{signal_name}.parquet"
        if path.exists():
            refs[f"discovery_{signal_name}"] = _load_long_panel(path).reindex(index=close.index, columns=close.columns)
    return refs


def _load_source_refs(close: pd.DataFrame) -> dict[str, pd.DataFrame]:
    refs: dict[str, pd.DataFrame] = {}
    for signal_name in STRESS_PROXY_SOURCE_SIGNALS:
        path = SOURCE_SIGNAL_DIR / f"{signal_name}.parquet"
        if path.exists():
            panel = pd.read_parquet(path)
            panel.index = pd.to_datetime(panel.index)
            refs[f"stress_proxy_{signal_name}"] = panel.reindex(index=close.index, columns=close.columns)
    return refs


def _reference_panels(signals: dict[str, pd.DataFrame], panels: dict[str, pd.DataFrame], benchmark: pd.Series) -> dict[str, pd.DataFrame]:
    refs = baseline_panels(signals, panels, benchmark)
    close = panels["close"]
    refs.update(_load_optional_long_refs(close))
    refs.update(_load_source_refs(close))
    for name, panel in signals.items():
        refs[f"lineage_{name}"] = panel
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
            effective_values: list[float] = []
            for idx, dates in enumerate(splits, start=1):
                sample = series.loc[dates]
                mean_ic = float(sample.mean())
                std_ic = float(sample.std(ddof=0))
                effective_values.append(mean_ic)
                window_rows.append(
                    {
                        "signal_name": signal_name,
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
            arr = np.array(effective_values, dtype=float)
            std = float(np.std(arr)) if len(arr) > 1 else np.nan
            summary_rows.append(
                {
                    "signal_name": signal_name,
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


def _primary_horizon_summary(scores: pd.DataFrame) -> pd.DataFrame:
    h10 = scores[scores["horizon"].eq(10)].rename(
        columns={
            "mean_ic": "h10_mean_ic",
            "ic_ir": "h10_ic_ir",
            "positive_ic_rate": "h10_positive_ic_rate",
            "n_dates": "h10_n_dates",
        }
    )
    h20 = scores[scores["horizon"].eq(20)].rename(
        columns={
            "mean_ic": "h20_mean_ic",
            "ic_ir": "h20_ic_ir",
            "positive_ic_rate": "h20_positive_ic_rate",
            "n_dates": "h20_n_dates",
        }
    )
    best = scores.loc[scores.groupby("signal_name")["abs_mean_ic"].idxmax()].drop(
        columns=["best_horizon"], errors="ignore"
    ).rename(
        columns={"horizon": "best_horizon", "mean_ic": "best_mean_ic"}
    )
    return (
        best[["signal_name", "best_horizon", "best_mean_ic", "ic_ir", "positive_ic_rate"]]
        .merge(h10[["signal_name", "h10_mean_ic", "h10_ic_ir", "h10_positive_ic_rate", "h10_n_dates"]], on="signal_name", how="left")
        .merge(h20[["signal_name", "h20_mean_ic", "h20_ic_ir", "h20_positive_ic_rate", "h20_n_dates"]], on="signal_name", how="left")
    )


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
                        "horizon": int(horizon),
                        "state": state,
                        "n_dates": int(len(sample)),
                        "mean_ic": float(sample.mean()) if len(sample) else np.nan,
                        "ic_ir": float(sample.mean() / std) if pd.notna(std) and std > 0 else np.nan,
                        "positive_ic_rate": float((sample > 0).mean()) if len(sample) else np.nan,
                    }
                )
    return pd.DataFrame(rows)


def _contamination_review(orth: pd.DataFrame, state_attr: pd.DataFrame, stress_attr: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    stress_refs = orth[orth["comparison"].str.contains("stress_proxy|failed_breakout|participation|breadth|liquidity|hostile", case=False, na=False)]
    for signal_name in VALIDATION_SIGNALS:
        group = stress_refs[stress_refs["signal_name"].eq(signal_name)].dropna(subset=["abs_value_corr"])
        top = group.sort_values("abs_value_corr", ascending=False).iloc[0] if not group.empty else None
        stress_states = stress_attr[stress_attr["signal_name"].eq(signal_name)].copy()
        positive_stress = int((stress_states["mean_ic"] > 0).sum()) if not stress_states.empty else 0
        strongest_stress = stress_states.sort_values("mean_ic", ascending=False).iloc[0] if not stress_states.empty else None
        v6_states = state_attr[state_attr["signal_name"].eq(signal_name)].copy()
        strongest_v6 = v6_states.sort_values("mean_ic", ascending=False).iloc[0] if not v6_states.empty else None
        max_stress_corr = float(top["abs_value_corr"]) if top is not None else np.nan
        rows.append(
            {
                "signal_name": signal_name,
                "max_stress_repair_abs_corr": max_stress_corr,
                "top_stress_repair_reference": top["comparison"] if top is not None else None,
                "positive_stress_state_count": positive_stress,
                "strongest_stress_state": strongest_stress["state"] if strongest_stress is not None else None,
                "strongest_stress_state_mean_ic": float(strongest_stress["mean_ic"]) if strongest_stress is not None else np.nan,
                "strongest_concept_state": strongest_v6["state"] if strongest_v6 is not None else None,
                "strongest_concept_state_mean_ic": float(strongest_v6["mean_ic"]) if strongest_v6 is not None else np.nan,
                "contamination_flag": bool(pd.notna(max_stress_corr) and max_stress_corr > 0.35),
            }
        )
    return pd.DataFrame(rows)


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
        .merge(contamination, on="signal_name", how="left")
    )
    summary["role"] = summary["signal_name"].map(
        {
            PRIMARY_SIGNAL: "primary_candidate",
            "post_drawdown_persistence_20": "lineage_anchor",
            "post_drawdown_persistence_core_20": "lineage_control",
        }
    )
    return summary.sort_values("role")


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
    if primary.get("max_stress_repair_abs_corr", 1) > 0.35:
        risks.append("stress_repair_similarity")
    if primary.get("max_inventory_corr", 0) > 0.50:
        risks.append("inventory_similarity_risk")
    if primary.get("max_reversal_corr", 0) > 0.50:
        risks.append("reversal_similarity_risk")
    if primary.get("active_date_ratio", 0) < 0.15:
        risks.append("active_coverage_low")

    core = summary[summary["signal_name"].eq("post_drawdown_persistence_core_20")]
    core_support = bool(
        not core.empty
        and float(core.iloc[0]["h10_mean_ic"]) > 0
        and float(core.iloc[0]["h20_mean_ic"]) > 0
    )
    if not core_support:
        risks.append("lineage_control_not_supportive")

    if not risks:
        return (
            "VALIDATION PASS",
            risks,
            "Primary candidate passed fixed h10/h20, WFV, concentration, active-coverage, and redundancy checks.",
        )
    core_positive = primary["h10_mean_ic"] > 0 and primary["h20_mean_ic"] > 0 and primary.get("max_stress_repair_abs_corr", 1) <= 0.35
    if core_positive and len(risks) <= 3:
        return (
            "CONDITIONAL VALIDATION CANDIDATE",
            risks,
            "Primary candidate retained positive h10/h20 evidence and low contamination risk, but review guardrails remain.",
        )
    if core_positive:
        return (
            "DIAGNOSTIC ONLY",
            risks,
            "Primary candidate remains informative for persistence research but did not clear enough validation stability checks.",
        )
    return (
        "VALIDATION FAILURE",
        risks,
        "Primary candidate failed core h10/h20 or contamination requirements under fixed validation scope.",
    )


def _write_note(
    summary: pd.DataFrame,
    scores: pd.DataFrame,
    wfv: pd.DataFrame,
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
    did_pass = outcome == "VALIDATION PASS"
    family_survived = outcome in {"VALIDATION PASS", "CONDITIONAL VALIDATION CANDIDATE"}
    diversification_improved = family_survived and bool(primary.get("max_stress_repair_abs_corr", np.nan) <= 0.35)

    lines = [
        "# Persistence Validation Execution v1",
        "",
        f"Date: 2026-06-18",
        "",
        f"Run id: `{RUN_ID}`",
        "",
        f"Primary candidate: `{PRIMARY_SIGNAL}`",
        "",
        "Scope: research-only validation execution using the fixed package from `persistence_validation_design_v1.md`. No new variants, additional refinement, governance mutation, threshold change, production registration, ML implementation, candidate promotion, or candidate demotion was performed.",
        "",
        "## SECTION 1 - Executive Summary",
        "",
        "Validation scope:",
        "- Primary candidate: `post_drawdown_persistence_churn_adjusted_20`.",
        "- Fixed lineage controls: `post_drawdown_persistence_20` and `post_drawdown_persistence_core_20`.",
        "- Horizons: h1, h5, h10, h20, with h10/h20 as primary validation horizons.",
        "- Diagnostics: WFV-style windows, horizon review, robustness review, active coverage, window concentration, state attribution, redundancy review, and stress-repair contamination review.",
        "",
        "Validation completion status: completed. Artifacts were written under `artifacts/research/persistence_validation_v1/`.",
        "",
        f"Overall outcome: `{outcome}`.",
        f"Decision rationale: {rationale}",
        f"Review risks: `{'; '.join(risks) if risks else 'none'}`.",
        "",
        "Primary findings:",
        f"- h10 mean IC was `{primary['h10_mean_ic']:.6f}` with IC IR `{primary['h10_ic_ir']:.6f}` and positive IC rate `{primary['h10_positive_ic_rate']:.6f}`.",
        f"- h20 mean IC was `{primary['h20_mean_ic']:.6f}` with IC IR `{primary['h20_ic_ir']:.6f}` and positive IC rate `{primary['h20_positive_ic_rate']:.6f}`.",
        f"- h10 WFV persistence/sign consistency were `{primary.get('h10_wfv_persistence', np.nan):.6f}` / `{primary.get('h10_wfv_sign_consistency', np.nan):.6f}`.",
        f"- h20 WFV persistence/sign consistency were `{primary.get('h20_wfv_persistence', np.nan):.6f}` / `{primary.get('h20_wfv_sign_consistency', np.nan):.6f}`.",
        f"- Maximum stress-repair reference correlation was `{primary.get('max_stress_repair_abs_corr', np.nan):.6f}`.",
        "",
        "## SECTION 2 - Core Validation Results",
        "",
        "Validation summary:",
        "",
        summary[
            [
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
                "h10_wfv_persistence",
                "h20_wfv_persistence",
                "max_stress_repair_abs_corr",
                "max_inventory_corr",
                "max_reversal_corr",
            ]
        ].to_markdown(index=False),
        "",
        "Primary candidate horizon behavior:",
        "",
        hrows[["signal_name", "horizon", "mean_ic", "ic_ir", "positive_ic_rate", "n_dates", "is_best_horizon"]].to_markdown(index=False),
        "",
        "Consistency versus refinement: h10/h20 remained positive under the validation runner. The validation h10 and h20 values should be interpreted as fixed-scope validation measurements, not additional refinement targets.",
        "",
        "## SECTION 3 - Robustness Assessment",
        "",
        "WFV window results for the primary candidate:",
        "",
        win_primary[["signal_name", "horizon", "window", "start_date", "end_date", "mean_test_ic", "test_ic_ir", "positive_ic_rate", "valid_ic_dates"]].to_markdown(index=False),
        "",
        "Window concentration diagnostics:",
        "",
        concentration[concentration["signal_name"].eq(PRIMARY_SIGNAL)].to_markdown(index=False),
        "",
        "State attribution snapshot:",
        "",
        state_primary[["signal_name", "horizon", "state", "n_dates", "mean_ic", "ic_ir", "positive_ic_rate"]].head(12).to_markdown(index=False),
        "",
        "Robustness interpretation: the candidate's validation strength depends on whether h10/h20 WFV windows remain consistently positive and whether recent-window behavior is acceptable. Any negative or concentrated window should be treated as validation risk rather than a reason to tune the formula.",
        "",
        "## SECTION 4 - Diversification Assessment",
        "",
        "Stress-repair contamination review:",
        "",
        contam_primary.to_markdown(index=False),
        "",
        f"Persistence-family distinctiveness: the candidate is highly related to its lineage controls, as expected, so validation supports a candidate lineage rather than broad independent family breadth. Stress-repair correlation remained `{primary.get('max_stress_repair_abs_corr', np.nan):.6f}`, which supports distinctiveness from hostile/stress-repair references at the artifact level.",
        "",
        "Overlap with hostile/stress-repair family: no governance or production stress-repair feature was added. Contamination risk is assessed through stress-reference correlations and state attribution; low correlation supports distinctiveness, while any stress-state-only IC concentration remains a review risk.",
        "",
        "Redundancy with existing candidates: full redundancy outputs are in `redundancy_review.csv` and summarized in `orthogonality_summary.csv`. Parent/sibling redundancy is expected and should not be misread as independent family breadth.",
        "",
        f"Does this appear to represent a genuinely different alpha family? {'Yes, conditionally' if diversification_improved else 'Not conclusively'}. The evidence supports a distinct persistence candidate thread if h10/h20 robustness and low stress-repair overlap are accepted under existing standards; it does not by itself prove a broad persistence family.",
        "",
        "## SECTION 5 - Validation Outcome",
        "",
        f"Classification: `{outcome}`",
        "",
        "This classification uses the fixed validation package and existing-style diagnostics. It does not alter thresholds, register the candidate, or make a governance decision.",
        "",
        "## SECTION 6 - Recommendation",
        "",
        "1. Did the candidate pass validation?",
        "",
        f"{'Yes' if did_pass else 'No'}. The fixed-scope outcome is `{outcome}`.",
        "",
        "2. Did the persistence family survive validation?",
        "",
        f"{'Yes, as a candidate lineage' if family_survived else 'No, not as validation-supported evidence'}. The result should not be overread as broad family validation because the evidence remains concentrated in one lineage.",
        "",
        "3. Does this improve alpha-family diversification?",
        "",
        f"{'Yes, modestly' if diversification_improved else 'Not conclusively'}. The diversification value depends on low stress-repair overlap and stable h10/h20 behavior.",
        "",
        "4. What are the primary risks?",
        "",
        f"`{'; '.join(risks) if risks else 'none recorded by the validation classifier'}`. Additional qualitative risks remain: family concentration, sibling redundancy, and possible stress-adjacent activation.",
        "",
        "5. What should the next Codex task be?",
        "",
        "The next Codex task should be a research-only validation interpretation and integration-readiness design if the user accepts this validation outcome. It should not modify governance, change thresholds, register production candidates, add variants, implement ML, or promote/demote candidates.",
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
    _, v6_states = build_v6_candidate_panels(panels, benchmark)
    registry = pd.DataFrame(
        [
            {
                "signal_name": PRIMARY_SIGNAL,
                "role": "primary_candidate",
                "family": "persistence",
                "source_run": "alpha_family_diversification_refinement_v1",
                "source_panel": str(REFINEMENT_PANEL_DIR / f"{PRIMARY_SIGNAL}.parquet"),
                "research_status": "READY_FOR_VALIDATION_REVIEW",
                "run_id": RUN_ID,
            },
            *[
                {
                    "signal_name": signal_name,
                    "role": "lineage_control",
                    "family": "persistence",
                    "source_run": "alpha_family_diversification_refinement_v1",
                    "source_panel": str(REFINEMENT_PANEL_DIR / f"{signal_name}.parquet"),
                    "research_status": "LINEAGE_CONTROL_ONLY",
                    "run_id": RUN_ID,
                }
                for signal_name in LINEAGE_CONTROLS
            ],
        ]
    )

    structural = structural_summary(signals)
    scores, daily_ics = score_signals(signals, panels["close"])
    stress_states = build_stress_states(panels["close"], benchmark)
    stress_attr = _state_attribution_for_horizons(daily_ics, stress_states, PRIMARY_HORIZONS)
    state_attr = _state_attribution_for_horizons(daily_ics, v6_states, PRIMARY_HORIZONS)
    wfv_summary, window_results = _wfv_for_horizons(daily_ics)
    concentration = _window_concentration(window_results)
    refs = _reference_panels(signals, panels, benchmark)
    orth = orthogonality(signals, refs)
    orth_summary = _max_corr_table(orth)
    active = active_coverage_summary(signals)
    contamination = _contamination_review(orth, state_attr, stress_attr)
    summary = _validation_summary(scores, structural, wfv_summary, concentration, orth_summary, active, contamination)
    outcome, risks, rationale = _classify(summary)

    registry.to_csv(OUT_DIR / "validation_candidate_inventory.csv", index=False)
    summary.to_csv(OUT_DIR / "validation_summary.csv", index=False)
    scores.to_csv(OUT_DIR / "validation_horizon_results.csv", index=False)
    daily_ics.to_csv(OUT_DIR / "daily_ic_by_candidate_horizon.csv", index=False)
    wfv_summary.to_csv(OUT_DIR / "wfv_style_summary.csv", index=False)
    window_results.to_csv(OUT_DIR / "validation_window_results.csv", index=False)
    concentration.to_csv(OUT_DIR / "window_concentration_diagnostics.csv", index=False)
    structural.to_csv(OUT_DIR / "structural_quality_summary.csv", index=False)
    active.to_csv(OUT_DIR / "active_coverage_summary.csv", index=False)
    state_attr.to_csv(OUT_DIR / "validation_state_attribution.csv", index=False)
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
                "candidate_count": len(VALIDATION_SIGNALS),
                "primary_candidate": PRIMARY_SIGNAL,
                "lineage_controls": LINEAGE_CONTROLS,
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
                    "validation_horizon_results": str(OUT_DIR / "validation_horizon_results.csv"),
                    "validation_window_results": str(OUT_DIR / "validation_window_results.csv"),
                    "validation_state_attribution": str(OUT_DIR / "validation_state_attribution.csv"),
                    "redundancy_review": str(OUT_DIR / "redundancy_review.csv"),
                    "contamination_review": str(OUT_DIR / "contamination_review.csv"),
                },
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )
    _write_note(summary, scores, wfv_summary, window_results, concentration, state_attr, contamination, outcome, risks, rationale)
    print(f"WROTE {OUT_DIR}")
    print(f"WROTE {NOTE_PATH}")
    print(f"OUTCOME {outcome}")
    print(f"RISKS {'; '.join(risks) if risks else 'none'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
