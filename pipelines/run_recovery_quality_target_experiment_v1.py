from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

from run_track_b_robustness_discovery_v3 import (
    build_stress_states,
    daily_ic,
    forward_returns,
    load_inputs,
    structural_summary,
)


RUN_ID = "recovery_quality_target_experiment_v1"
OUT_DIR = Path("artifacts/research") / RUN_ID
NOTE_PATH = Path("docs/research_notes/recovery_quality_target_experiment_v1.md")

HORIZONS = (10, 20)
SNAPSHOT = "RESEARCH_ONLY_DIAGNOSTIC_ONLY"

PANEL_PATHS = {
    "participation_liquidity_state_shift_20_60": Path(
        "artifacts/research/robustness_first_discovery_expansion_v4/"
        "participation_liquidity_state_shift_20_60_signal_panel.parquet"
    ),
    "participation_breadth_repair_under_hostile_trend": Path(
        "artifacts/research/track_b_v5_focused_discovery/"
        "participation_breadth_repair_under_hostile_trend_signal_panel.parquet"
    ),
    "volatility_compression_after_stress_stabilization": Path(
        "artifacts/research/track_b_v6_focused_discovery/"
        "volatility_compression_after_stress_stabilization_signal_panel.parquet"
    ),
    "volatility_participation_asymmetry_20_original": Path(
        "artifacts/research/volatility_participation_asymmetry_20_refinement_v1/"
        "volatility_participation_asymmetry_20_original_signal_panel.parquet"
    ),
    "turnover_shock_exhaustion_repair_20": Path(
        "artifacts/research/event_defined_liquidity_turnover_exhaustion_alpha_v1/"
        "turnover_shock_exhaustion_repair_20_signal_panel.parquet"
    ),
    "short_horizon_volatility_shock_absorption_10": Path(
        "artifacts/research/short_horizon_volatility_shock_absorption_10_refinement/"
        "rebalance_5_zero_signal_panel.parquet"
    ),
}

INVENTORY_CANDIDATES = {
    "participation_liquidity_state_shift_20_60",
    "participation_breadth_repair_under_hostile_trend",
    "volatility_compression_after_stress_stabilization",
}


def _timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _ensure_dirs() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    NOTE_PATH.parent.mkdir(parents=True, exist_ok=True)


def _rank01(df: pd.DataFrame) -> pd.DataFrame:
    return df.rank(axis=1, pct=True)


def _future_path_returns(close: pd.DataFrame, horizon: int) -> list[pd.DataFrame]:
    return [close.shift(-step) / close - 1.0 for step in range(1, horizon + 1)]


def _future_min_return(close: pd.DataFrame, horizon: int) -> pd.DataFrame:
    return pd.concat(_future_path_returns(close, horizon), keys=range(1, horizon + 1)).groupby(level=1).min()


def _future_realized_vol(close: pd.DataFrame, horizon: int) -> pd.DataFrame:
    ret1 = close.pct_change(1, fill_method=None)
    shifted = [ret1.shift(-step) for step in range(1, horizon + 1)]
    return pd.concat(shifted, keys=range(1, horizon + 1)).groupby(level=1).std()


def _future_average_range(high: pd.DataFrame, low: pd.DataFrame, close: pd.DataFrame, horizon: int) -> pd.DataFrame:
    true_range = ((high - low) / close.shift(1)).replace([np.inf, -np.inf], np.nan)
    shifted = [true_range.shift(-step) for step in range(1, horizon + 1)]
    return pd.concat(shifted, keys=range(1, horizon + 1)).groupby(level=1).mean()


def _future_close_location_improvement(
    high: pd.DataFrame, low: pd.DataFrame, close: pd.DataFrame, horizon: int
) -> pd.DataFrame:
    close_location = ((close - low) / (high - low).replace(0.0, np.nan)).clip(0.0, 1.0)
    future_close_location = pd.concat(
        [close_location.shift(-step) for step in range(1, horizon + 1)],
        keys=range(1, horizon + 1),
    ).groupby(level=1).mean()
    prior_close_location = close_location.rolling(10, min_periods=6).mean()
    return future_close_location - prior_close_location


def _build_targets(panels: dict[str, pd.DataFrame], benchmark: pd.Series) -> tuple[dict[str, pd.DataFrame], pd.DataFrame]:
    close = panels["close"]
    high = panels["high"]
    low = panels["low"]
    ret1 = close.pct_change(1, fill_method=None)
    prior_vol20 = ret1.rolling(20, min_periods=12).std()
    prior_range20 = ((high - low) / close.shift(1)).replace([np.inf, -np.inf], np.nan).rolling(20, min_periods=12).mean()

    stress = build_stress_states(close, benchmark)
    stress_like = stress[["drawdown_acceleration", "volatility_spike", "panic_liquidity_stress", "weak_breadth"]].any(axis=1)
    stress_recent = stress_like.rolling(20, min_periods=1).max().astype(bool)
    stress_recent_panel = pd.DataFrame(
        np.where(stress_recent.to_numpy()[:, None], 1.0, np.nan).repeat(len(close.columns), axis=1),
        index=close.index,
        columns=close.columns,
    )

    targets: dict[str, pd.DataFrame] = {}
    target_meta_rows = []
    for horizon in HORIZONS:
        raw = forward_returns(close, horizon)
        min_path = _future_min_return(close, horizon)
        future_vol = _future_realized_vol(close, horizon)
        future_range = _future_average_range(high, low, close, horizon)
        close_location_improvement = _future_close_location_improvement(high, low, close, horizon)

        drawdown_containment = min_path.clip(upper=0.0)
        vol_reduction = (prior_vol20 - future_vol) / prior_vol20.replace(0.0, np.nan)
        range_reduction = (prior_range20 - future_range) / prior_range20.replace(0.0, np.nan)

        target_defs = {
            f"raw_h{horizon}_forward_return": raw,
            f"drawdown_adjusted_h{horizon}_forward_return": raw + drawdown_containment,
            f"downside_controlled_h{horizon}_return": raw - (min_path < -0.06).astype(float) * min_path.abs(),
            f"recovery_quality_h{horizon}_composite": (
                _rank01(raw)
                + _rank01(min_path)
                + _rank01(vol_reduction)
                + _rank01(range_reduction)
                + _rank01(close_location_improvement)
            )
            / 5.0,
            f"post_stress_stabilization_h{horizon}_target": (
                (_rank01(min_path) + _rank01(vol_reduction) + _rank01(range_reduction) + _rank01(close_location_improvement))
                / 4.0
            )
            * stress_recent_panel,
        }
        for target_name, target in target_defs.items():
            targets[target_name] = target.replace([np.inf, -np.inf], np.nan)
            target_meta_rows.append(
                {
                    "target_name": target_name,
                    "horizon": horizon,
                    "target_family": target_name.replace(f"_h{horizon}", "").replace("_target", ""),
                    "research_only": True,
                    "validation_anchor": target_name.startswith("raw_"),
                    "notes": "Alternative target is diagnostic only; raw h10/h20 forward return remains validation anchor.",
                }
            )
    return targets, pd.DataFrame(target_meta_rows)


def _load_candidate_panels(index: pd.Index, columns: pd.Index) -> tuple[dict[str, pd.DataFrame], pd.DataFrame]:
    panels = {}
    rows = []
    for signal_name, path in PANEL_PATHS.items():
        available = path.exists()
        if available:
            panel = pd.read_parquet(path)
            panel.index = pd.to_datetime(panel.index)
            panel.columns = panel.columns.astype(str).str.upper()
            panel = panel.reindex(index=index, columns=columns)
            panels[signal_name] = panel
        rows.append(
            {
                "signal_name": signal_name,
                "candidate_group": "current_inventory" if signal_name in INVENTORY_CANDIDATES else "parked_weak_research_evidence",
                "panel_path": str(path),
                "available": bool(available),
                "rows": int(panels[signal_name].shape[0]) if available else 0,
                "columns": int(panels[signal_name].shape[1]) if available else 0,
                "status_change_allowed": False,
            }
        )
    return panels, pd.DataFrame(rows)


def _score_against_targets(
    signals: dict[str, pd.DataFrame],
    targets: dict[str, pd.DataFrame],
) -> tuple[pd.DataFrame, pd.DataFrame]:
    rows = []
    daily_rows = []
    for target_name, target in targets.items():
        horizon = int(target_name.split("_h")[-1].split("_")[0])
        family = target_name.replace(f"_h{horizon}", "")
        for signal_name, signal in signals.items():
            ic = daily_ic(signal, target)
            valid = ic.dropna()
            mean_ic = float(valid.mean()) if len(valid) else np.nan
            std_ic = float(valid.std(ddof=0)) if len(valid) > 1 else np.nan
            rows.append(
                {
                    "signal_name": signal_name,
                    "target_name": target_name,
                    "target_family": family,
                    "horizon": horizon,
                    "mean_ic": mean_ic,
                    "ic_ir": mean_ic / std_ic if pd.notna(std_ic) and std_ic > 0 else np.nan,
                    "positive_ic_rate": float((valid > 0).mean()) if len(valid) else np.nan,
                    "n_dates": int(len(valid)),
                    "research_only": True,
                }
            )
            daily_rows.extend(
                {
                    "Date": date,
                    "signal_name": signal_name,
                    "target_name": target_name,
                    "target_family": family,
                    "horizon": horizon,
                    "ic": value,
                }
                for date, value in valid.items()
            )
    return pd.DataFrame(rows), pd.DataFrame(daily_rows)


def _target_correlation_matrix(targets: dict[str, pd.DataFrame]) -> pd.DataFrame:
    series = {}
    for name, panel in targets.items():
        series[name] = panel.stack(future_stack=True)
    frame = pd.DataFrame(series)
    return frame.corr(method="spearman")


def _target_lowvol_overlap(targets: dict[str, pd.DataFrame], close: pd.DataFrame) -> pd.DataFrame:
    low_vol = -close.pct_change(1, fill_method=None).rolling(20, min_periods=12).std()
    rows = []
    for target_name, target in targets.items():
        ic = daily_ic(low_vol, target).dropna()
        rows.append(
            {
                "target_name": target_name,
                "mean_lowvol_rank_corr": float(ic.mean()) if len(ic) else np.nan,
                "abs_mean_lowvol_rank_corr": float(abs(ic.mean())) if len(ic) else np.nan,
                "positive_corr_rate": float((ic > 0).mean()) if len(ic) else np.nan,
                "n_dates": int(len(ic)),
                "lowvol_reward_warning": bool(abs(ic.mean()) > 0.20) if len(ic) else False,
            }
        )
    return pd.DataFrame(rows)


def _wfv_by_target(daily_ics: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    summary_rows = []
    window_rows = []
    for (signal_name, target_name), group in daily_ics.groupby(["signal_name", "target_name"]):
        series = group.set_index("Date")["ic"].dropna().sort_index()
        if len(series) < 200:
            continue
        splits = np.array_split(series.index, 4)
        values = []
        for idx, dates in enumerate(splits, start=1):
            sample = series.loc[dates]
            mean_ic = float(sample.mean())
            values.append(mean_ic)
            window_rows.append(
                {
                    "signal_name": signal_name,
                    "target_name": target_name,
                    "window": idx,
                    "start_date": str(sample.index.min().date()),
                    "end_date": str(sample.index.max().date()),
                    "mean_ic": mean_ic,
                    "positive_ic_rate": float((sample > 0).mean()),
                    "valid_dates": int(len(sample)),
                }
            )
        arr = np.array(values, dtype=float)
        denom = np.sum(np.abs(arr))
        summary_rows.append(
            {
                "signal_name": signal_name,
                "target_name": target_name,
                "n_windows": int(len(arr)),
                "window_mean_ic": float(arr.mean()),
                "persistence": float((arr > 0).mean()),
                "sign_consistency": float(max((arr > 0).mean(), (arr < 0).mean())),
                "one_window_dominance": float(np.max(np.abs(arr)) / denom) if denom > 0 else np.nan,
            }
        )
    return pd.DataFrame(summary_rows), pd.DataFrame(window_rows)


def _target_sensitivity(scores: pd.DataFrame) -> pd.DataFrame:
    raw = scores[scores["target_family"].str.startswith("raw_")][
        ["signal_name", "horizon", "mean_ic", "positive_ic_rate"]
    ].rename(columns={"mean_ic": "raw_mean_ic", "positive_ic_rate": "raw_positive_ic_rate"})
    rows = []
    for _, row in scores.iterrows():
        base = raw[(raw["signal_name"].eq(row["signal_name"])) & (raw["horizon"].eq(row["horizon"]))]
        if base.empty:
            continue
        raw_mean = float(base.iloc[0]["raw_mean_ic"])
        rows.append(
            {
                "signal_name": row["signal_name"],
                "target_name": row["target_name"],
                "horizon": int(row["horizon"]),
                "target_mean_ic": row["mean_ic"],
                "raw_mean_ic": raw_mean,
                "target_minus_raw_ic": row["mean_ic"] - raw_mean if pd.notna(row["mean_ic"]) else np.nan,
                "target_positive_ic_rate": row["positive_ic_rate"],
                "raw_positive_ic_rate": float(base.iloc[0]["raw_positive_ic_rate"]),
                "raw_validation_anchor_replaced": False,
            }
        )
    return pd.DataFrame(rows)


def _ranking_comparison(scores: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for target_name, group in scores.groupby("target_name"):
        ranked = group.sort_values("mean_ic", ascending=False).reset_index(drop=True)
        for rank, row in enumerate(ranked.to_dict("records"), start=1):
            rows.append(
                {
                    "target_name": target_name,
                    "rank": rank,
                    "signal_name": row["signal_name"],
                    "mean_ic": row["mean_ic"],
                    "positive_ic_rate": row["positive_ic_rate"],
                    "horizon": row["horizon"],
                }
            )
    return pd.DataFrame(rows)


def _fragility_review(scores: pd.DataFrame, wfv_summary: pd.DataFrame, lowvol_overlap: pd.DataFrame) -> pd.DataFrame:
    merged = scores.rename(columns={"n_dates": "score_n_dates"}).merge(wfv_summary, on=["signal_name", "target_name"], how="left")
    merged = merged.merge(lowvol_overlap, on="target_name", how="left")
    rows = []
    for _, row in merged.iterrows():
        warnings = []
        score_n_dates = row.get("score_n_dates", 0)
        if score_n_dates < 250:
            warnings.append("thin_ic_sample")
        if row.get("one_window_dominance", 0) > 0.60:
            warnings.append("one_window_dominance")
        if row.get("persistence", 0) < 0.50 and not str(row["target_family"]).startswith("raw_"):
            warnings.append("weak_target_persistence")
        if row.get("lowvol_reward_warning", False):
            warnings.append("possible_lowvol_reward")
        if str(row["target_family"]).startswith("post_stress_stabilization") and score_n_dates < 120:
            warnings.append("stress_target_thinness")
        rows.append(
            {
                "signal_name": row["signal_name"],
                "target_name": row["target_name"],
                "score_n_dates": int(score_n_dates) if pd.notna(score_n_dates) else 0,
                "mean_ic": row["mean_ic"],
                "persistence": row.get("persistence"),
                "one_window_dominance": row.get("one_window_dominance"),
                "abs_mean_lowvol_rank_corr": row.get("abs_mean_lowvol_rank_corr"),
                "fragility_warnings": "; ".join(warnings) if warnings else "none",
                "diagnostic_only": True,
            }
        )
    return pd.DataFrame(rows)


def _candidate_profiles(scores: pd.DataFrame, sensitivity: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for signal_name, group in scores.groupby("signal_name"):
        raw = group[group["target_family"].str.startswith("raw_")]
        alt = group[~group["target_family"].str.startswith("raw_")]
        best_alt = alt.sort_values("mean_ic", ascending=False).head(1)
        best_raw = raw.sort_values("mean_ic", ascending=False).head(1)
        sens = sensitivity[sensitivity["signal_name"].eq(signal_name)]
        rows.append(
            {
                "signal_name": signal_name,
                "candidate_group": "current_inventory" if signal_name in INVENTORY_CANDIDATES else "parked_weak_research_evidence",
                "best_raw_target": str(best_raw.iloc[0]["target_name"]) if not best_raw.empty else "unavailable",
                "best_raw_mean_ic": float(best_raw.iloc[0]["mean_ic"]) if not best_raw.empty else np.nan,
                "best_alternative_target": str(best_alt.iloc[0]["target_name"]) if not best_alt.empty else "unavailable",
                "best_alternative_mean_ic": float(best_alt.iloc[0]["mean_ic"]) if not best_alt.empty else np.nan,
                "max_target_minus_raw_ic": float(sens["target_minus_raw_ic"].max()) if not sens.empty else np.nan,
                "alternative_lens_helped": bool((sens["target_minus_raw_ic"].max() > 0.005) if not sens.empty else False),
                "status_change_allowed": False,
            }
        )
    return pd.DataFrame(rows)


def _write_note(
    candidate_registry: pd.DataFrame,
    scores: pd.DataFrame,
    sensitivity: pd.DataFrame,
    profiles: pd.DataFrame,
    lowvol_overlap: pd.DataFrame,
    fragility: pd.DataFrame,
    target_corr: pd.DataFrame,
) -> None:
    raw_scores = scores[scores["target_family"].str.startswith("raw_")]
    alt_scores = scores[~scores["target_family"].str.startswith("raw_")]
    best_alt = alt_scores.sort_values("mean_ic", ascending=False).head(8)
    helped = profiles[profiles["alternative_lens_helped"]]
    lowvol_flags = lowvol_overlap[lowvol_overlap["lowvol_reward_warning"]]

    lines = [
        "# Recovery Quality Target Experiment v1",
        "",
        "Date: 2026-05-25",
        "",
        "Status: `RESEARCH_ONLY_DIAGNOSTIC_ONLY`",
        "",
        "## Executive Takeaway",
        "",
        "This experiment compares current inventory candidates and selected parked weak clues against raw h10/h20 forward-return targets and several recovery-oriented diagnostic targets.",
        "",
        "Raw h10/h20 IC remains the validation anchor. Alternative targets in this run are diagnostic lenses only and do not change candidate status, gates, validation logic, production registration, portfolio routing, ML, blending, optimization, detector usage, metadata usage, or governance.",
        "",
        f"Candidate panels available: `{int(candidate_registry['available'].sum())}` / `{len(candidate_registry)}`.",
        "",
        "## Candidates Evaluated",
        "",
        candidate_registry.to_markdown(index=False),
        "",
        "## Target Families",
        "",
        "- raw h10/h20 forward return",
        "- drawdown-adjusted h10/h20 forward return",
        "- downside-controlled h10/h20 return",
        "- recovery-quality h10/h20 composite",
        "- post-stress stabilization h10/h20 target",
        "",
        "## Raw Target Anchor",
        "",
        raw_scores.sort_values(["horizon", "mean_ic"], ascending=[True, False]).to_markdown(index=False),
        "",
        "## Alternative Target Comparison",
        "",
        alt_scores.sort_values(["target_name", "mean_ic"], ascending=[True, False]).to_markdown(index=False),
        "",
        "## Best Alternative Target Clues",
        "",
        best_alt.to_markdown(index=False) if not best_alt.empty else "No alternative target rows were available.",
        "",
        "## Preliminary Interpretation",
        "",
        "- The most visible alternative-target lift appears in `short_horizon_volatility_shock_absorption_10` and `participation_liquidity_state_shift_20_60` under recovery-quality and post-stress stabilization targets.",
        "- `volatility_compression_after_stress_stabilization` improves more under drawdown-adjusted and downside-controlled return than under the recovery-quality composite.",
        "- `participation_breadth_repair_under_hostile_trend` remains strongest on raw h20; alternative targets do not materially improve it in this run.",
        "- `volatility_participation_asymmetry_20_original` and `turnover_shock_exhaustion_repair_20` show only modest drawdown-adjusted improvement and remain parked weak evidence.",
        "- The largest recovery/post-stress effects should be treated as target-feature proximity clues, not alpha evidence, because those target definitions intentionally include stabilization and path-quality terms.",
        "- Drawdown-adjusted targets are highly correlated with raw forward-return targets, so they may be best interpreted as a supplement rather than a distinct target family.",
        "",
        "## Candidate Behavior Profiles",
        "",
        profiles.to_markdown(index=False),
        "",
        "## Target Sensitivity Versus Raw Return",
        "",
        sensitivity.sort_values("target_minus_raw_ic", ascending=False).head(20).to_markdown(index=False),
        "",
        "## Low-Volatility / Passive Reward Check",
        "",
        lowvol_overlap.sort_values("abs_mean_lowvol_rank_corr", ascending=False).to_markdown(index=False),
        "",
        "## Fragility Review",
        "",
        fragility.sort_values(["fragility_warnings", "mean_ic"], ascending=[True, False]).head(40).to_markdown(index=False),
        "",
        "## Research Questions",
        "",
        "1. Do current inventory candidates improve materially under recovery-quality-oriented targets?",
        "",
        f"- Diagnostic answer: `{len(helped)}` candidate profiles showed a target-minus-raw improvement above the simple review threshold of 0.005. This is not a status change and must be reviewed alongside low-volatility and fragility warnings.",
        "",
        "2. Do weak repair/stabilization candidates express value missed by raw IC?",
        "",
        "- Diagnostic answer: alternative targets can surface different behavior, but this run does not convert weak clues into validation candidates. Any apparent improvement is a research clue only.",
        "",
        "3. Which targets best align with surviving signal behavior?",
        "",
        "- Use the target comparison and sensitivity tables. Preference should go to targets that improve interpretation without large low-volatility overlap or one-window dominance.",
        "",
        "4. Are alternative targets identifying true structure or rewarding low-volatility/passive behavior?",
        "",
        f"- `{len(lowvol_flags)}` target definitions crossed the low-volatility reward warning threshold. These require skepticism before any future target work.",
        "",
        "5. Should future research separate alpha return prediction, recovery quality, stabilization quality, downside containment, and context usefulness?",
        "",
        "- Yes. This experiment reinforces object-type separation: raw-return alpha prediction remains separate from recovery/risk diagnostics and context usefulness.",
        "",
        "## Target Correlation Summary",
        "",
        "The full target correlation matrix is saved as `target_correlation_matrix.csv`. High correlations between alternative targets and raw return should be treated as a sign that the alternative lens may not add much information.",
        "",
        "## Interpretation Standard",
        "",
        "A stronger alternative-target IC is not an alpha pass. It only suggests that a mechanism may be more naturally described as recovery quality, stabilization quality, or downside containment. Any future use would need pre-registered target formulas, anti-duplication diagnostics, sample-size checks, and separate governance.",
        "",
        "## Recommended Next Step",
        "",
        "Do not change validation standards. Review the diagnostic artifacts first. If one target family shows consistent, interpretable improvement without passive low-volatility reward or fragility, the next step should be a design-only governance note for target experiment standards before any additional implementation.",
        "",
        "## Artifacts",
        "",
        "- `candidate_registry.csv`",
        "- `target_metadata.csv`",
        "- `target_comparison_table.csv`",
        "- `daily_ic_by_candidate_target.csv`",
        "- `target_sensitivity_analysis.csv`",
        "- `target_correlation_matrix.csv`",
        "- `target_lowvol_overlap.csv`",
        "- `wfv_target_summary.csv`",
        "- `wfv_target_windows.csv`",
        "- `drawdown_adjusted_ranking_comparison.csv`",
        "- `recovery_quality_ranking_comparison.csv`",
        "- `candidate_behavior_profiles.csv`",
        "- `target_fragility_review.csv`",
        "- `structural_summary.csv`",
        "- `manifest.json`",
        "",
        "## Intentional Non-Changes",
        "",
        "This experiment did not:",
        "",
        "- modify validation logic",
        "- modify gates or thresholds",
        "- change candidate statuses",
        "- promote weak candidates",
        "- replace raw h10/h20 IC as the primary validation anchor",
        "- change portfolio, ML, blending, optimization, metadata, detector, governance, or production paths",
        "- make production claims",
    ]
    NOTE_PATH.write_text("\n".join(lines) + "\n")


def main() -> None:
    _ensure_dirs()
    panels, benchmark = load_inputs()
    close = panels["close"]
    columns = close.columns.astype(str).str.upper()
    close.columns = columns
    for key in ["open", "high", "low", "volume"]:
        panels[key].columns = panels[key].columns.astype(str).str.upper()

    signals, candidate_registry = _load_candidate_panels(close.index, columns)
    if not signals:
        raise RuntimeError("No candidate panels were available for recovery-quality target experiment.")

    targets, target_metadata = _build_targets(panels, benchmark)
    scores, daily_ics = _score_against_targets(signals, targets)
    target_corr = _target_correlation_matrix(targets)
    lowvol_overlap = _target_lowvol_overlap(targets, close)
    wfv_summary, wfv_windows = _wfv_by_target(daily_ics)
    sensitivity = _target_sensitivity(scores)
    ranking = _ranking_comparison(scores)
    drawdown_ranking = ranking[ranking["target_name"].str.startswith("drawdown_adjusted")].copy()
    recovery_ranking = ranking[ranking["target_name"].str.startswith("recovery_quality")].copy()
    fragility = _fragility_review(scores, wfv_summary, lowvol_overlap)
    profiles = _candidate_profiles(scores, sensitivity)
    structural = structural_summary(signals)

    candidate_registry.to_csv(OUT_DIR / "candidate_registry.csv", index=False)
    target_metadata.to_csv(OUT_DIR / "target_metadata.csv", index=False)
    scores.to_csv(OUT_DIR / "target_comparison_table.csv", index=False)
    daily_ics.to_csv(OUT_DIR / "daily_ic_by_candidate_target.csv", index=False)
    sensitivity.to_csv(OUT_DIR / "target_sensitivity_analysis.csv", index=False)
    target_corr.to_csv(OUT_DIR / "target_correlation_matrix.csv")
    lowvol_overlap.to_csv(OUT_DIR / "target_lowvol_overlap.csv", index=False)
    wfv_summary.to_csv(OUT_DIR / "wfv_target_summary.csv", index=False)
    wfv_windows.to_csv(OUT_DIR / "wfv_target_windows.csv", index=False)
    ranking.to_csv(OUT_DIR / "state_free_target_ranking_comparison.csv", index=False)
    drawdown_ranking.to_csv(OUT_DIR / "drawdown_adjusted_ranking_comparison.csv", index=False)
    recovery_ranking.to_csv(OUT_DIR / "recovery_quality_ranking_comparison.csv", index=False)
    profiles.to_csv(OUT_DIR / "candidate_behavior_profiles.csv", index=False)
    fragility.to_csv(OUT_DIR / "target_fragility_review.csv", index=False)
    structural.to_csv(OUT_DIR / "structural_summary.csv", index=False)

    manifest = {
        "run_id": RUN_ID,
        "generated_at": _timestamp(),
        "status": SNAPSHOT,
        "candidate_count": int(len(signals)),
        "target_count": int(len(targets)),
        "raw_h10_h20_validation_anchor_replaced": False,
        "validation_logic_changed": False,
        "gates_thresholds_changed": False,
        "candidate_statuses_changed": False,
        "production_paths_changed": False,
        "portfolio_ml_blending_optimization_changed": False,
        "detector_metadata_governance_changed": False,
        "artifacts": sorted(path.name for path in OUT_DIR.glob("*")),
    }
    (OUT_DIR / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")

    _write_note(candidate_registry, scores, sensitivity, profiles, lowvol_overlap, fragility, target_corr)
    print(json.dumps({"run_id": RUN_ID, "candidate_count": len(signals), "target_count": len(targets)}, indent=2))


if __name__ == "__main__":
    main()
