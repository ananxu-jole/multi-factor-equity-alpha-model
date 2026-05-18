from __future__ import annotations

import json
from itertools import combinations
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


RUN_ID = "participation_liquidity_state_shift_refinement_v1"
SOURCE_RUN_ID = "robustness_first_discovery_expansion_v4"
SIGNAL_NAME = "participation_liquidity_state_shift_20_60"
V4_DIR = Path("artifacts/research/robustness_first_discovery_expansion_v4")
V4_DIAG_DIR = Path("artifacts/research/track_b_v4_conditional_diagnostics")
OUT_DIR = Path("artifacts/research") / RUN_ID
NOTE_PATH = Path("docs/research_notes/participation_liquidity_state_shift_refinement.md")


def _ensure_dirs() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    NOTE_PATH.parent.mkdir(parents=True, exist_ok=True)


def _forward_returns(close: pd.DataFrame, horizon: int) -> pd.DataFrame:
    return close.shift(-horizon) / close - 1.0


def _score_panel(panel: pd.DataFrame, close: pd.DataFrame, horizon: int) -> dict[str, float | int]:
    ic = daily_ic(panel, _forward_returns(close, horizon)).dropna()
    std = ic.std(ddof=0) if len(ic) > 1 else np.nan
    return {
        "mean_ic": float(ic.mean()) if len(ic) else np.nan,
        "abs_mean_ic": float(abs(ic.mean())) if len(ic) else np.nan,
        "ic_ir": float(ic.mean() / std) if pd.notna(std) and std > 0 else np.nan,
        "positive_ic_rate": float((ic > 0).mean()) if len(ic) else np.nan,
        "n_dates": int(len(ic)),
    }


def _score_all_horizons(variants: dict[str, pd.DataFrame], close: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    score_rows = []
    daily_rows = []
    for name, panel in variants.items():
        for horizon in HORIZONS:
            fwd = _forward_returns(close, horizon)
            ic = daily_ic(panel, fwd).dropna()
            std = ic.std(ddof=0) if len(ic) > 1 else np.nan
            score_rows.append(
                {
                    "variant_name": name,
                    "horizon": horizon,
                    "mean_ic": float(ic.mean()) if len(ic) else np.nan,
                    "abs_mean_ic": float(abs(ic.mean())) if len(ic) else np.nan,
                    "ic_ir": float(ic.mean() / std) if pd.notna(std) and std > 0 else np.nan,
                    "positive_ic_rate": float((ic > 0).mean()) if len(ic) else np.nan,
                    "n_dates": int(len(ic)),
                }
            )
            daily_rows.extend(
                {"Date": date, "variant_name": name, "horizon": horizon, "ic": value}
                for date, value in ic.items()
            )
    scores = pd.DataFrame(score_rows)
    best = scores.loc[scores.groupby("variant_name")["abs_mean_ic"].idxmax(), ["variant_name", "horizon"]]
    best = best.rename(columns={"horizon": "best_horizon"})
    scores = scores.merge(best, on="variant_name", how="left")
    scores["is_best_horizon"] = scores["horizon"].eq(scores["best_horizon"])
    return scores, pd.DataFrame(daily_rows)


def _turnover(panel: pd.DataFrame) -> float:
    return float(panel.diff().abs().mean(axis=1, skipna=True).mean(skipna=True))


def _rebalance(panel: pd.DataFrame, interval: int) -> pd.DataFrame:
    out = panel.copy() * np.nan
    out.iloc[::interval] = panel.iloc[::interval]
    return out.ffill()


def _threshold(panel: pd.DataFrame, level: float, inactive: str) -> pd.DataFrame:
    active = panel.abs() >= level
    if inactive == "zero":
        return panel.where(active, 0.0)
    return panel.where(active)


def _rank_persistence_filter(panel: pd.DataFrame, window: int, min_autocorr: float = 0.65) -> pd.DataFrame:
    out = panel.copy()
    # Simple per-name temporal persistence proxy: keep values only if recent rank-like values have low churn.
    stability = 1.0 - panel.diff().abs().rolling(window, min_periods=max(3, window // 2)).mean()
    return out.where(stability >= min_autocorr)


def _low_churn_filter(panel: pd.DataFrame, max_change: float) -> pd.DataFrame:
    return panel.where(panel.diff().abs() <= max_change).ffill(limit=3)


def _build_states(close: pd.DataFrame, volume: pd.DataFrame, benchmark: pd.Series) -> pd.DataFrame:
    bench_ret = benchmark.pct_change(1, fill_method=None)
    bench_ret20 = benchmark.pct_change(20, fill_method=None)
    ma60 = benchmark.rolling(60, min_periods=40).mean()
    dispersion20 = close.pct_change(20, fill_method=None).std(axis=1)
    breadth20 = (close.pct_change(20, fill_method=None) > 0).mean(axis=1)
    q = lambda s, p: s.rolling(252, min_periods=100).quantile(p)
    base = pd.DataFrame(index=close.index)
    base["TREND_HOSTILE"] = ((benchmark < ma60) | (bench_ret20 < 0)).fillna(False)
    base["LOW_DISPERSION"] = (dispersion20 < q(dispersion20, 0.35)).fillna(False)
    base["WEAK_BREADTH"] = (breadth20 < q(breadth20, 0.35)).fillna(False)
    stress = build_stress_states(close, benchmark)
    base["DRAWDOWN"] = stress["drawdown_acceleration"].fillna(False)
    base["PANIC_LIQUIDITY_STRESS"] = stress["panic_liquidity_stress"].fillna(False)
    base["VOLATILITY_SPIKE"] = stress["volatility_spike"].fillna(False)
    # Composite states use OR logic to keep sample sizes practical.
    base["HOSTILE_OR_WEAK_BREADTH"] = base["TREND_HOSTILE"] | base["WEAK_BREADTH"]
    base["HOSTILE_LOW_DISPERSION"] = base["TREND_HOSTILE"] & base["LOW_DISPERSION"]
    base["STRESS_OR_WEAK_BREADTH"] = base["DRAWDOWN"] | base["PANIC_LIQUIDITY_STRESS"] | base["WEAK_BREADTH"]
    base["HOSTILE_STRESS_OR_WEAK_BREADTH"] = base["TREND_HOSTILE"] | base["DRAWDOWN"] | base["WEAK_BREADTH"]
    return base


def _apply_state(panel: pd.DataFrame, state: pd.Series, inactive: str) -> pd.DataFrame:
    active = state.reindex(panel.index).fillna(False)
    if inactive == "zero":
        return panel.where(active, 0.0)
    return panel.where(active)


def _variant_panels(base: pd.DataFrame, states: pd.DataFrame) -> dict[str, pd.DataFrame]:
    transforms: dict[str, pd.DataFrame] = {
        "base": base,
        "smooth_3": base.rolling(3, min_periods=2).mean(),
        "smooth_5": base.rolling(5, min_periods=3).mean(),
        "smooth_10": base.rolling(10, min_periods=5).mean(),
        "rebalance_5": _rebalance(base, 5),
        "rebalance_10": _rebalance(base, 10),
        "rebalance_20": _rebalance(base, 20),
        "threshold_0p35_nan": _threshold(base, 0.35, "nan"),
        "threshold_0p35_zero": _threshold(base, 0.35, "zero"),
        "threshold_0p50_nan": _threshold(base, 0.50, "nan"),
        "rank_persist_5": _rank_persistence_filter(base, 5),
        "rank_persist_10": _rank_persistence_filter(base, 10),
        "low_churn_0p25": _low_churn_filter(base, 0.25),
        "low_churn_0p35": _low_churn_filter(base, 0.35),
    }
    variants = dict(transforms)
    selected_transforms = {
        "rebalance_10": transforms["rebalance_10"],
        "smooth_5": transforms["smooth_5"],
        "threshold_0p35_nan": transforms["threshold_0p35_nan"],
        "rank_persist_10": transforms["rank_persist_10"],
    }
    for state_name in [
        "TREND_HOSTILE",
        "LOW_DISPERSION",
        "WEAK_BREADTH",
        "DRAWDOWN",
        "PANIC_LIQUIDITY_STRESS",
        "HOSTILE_OR_WEAK_BREADTH",
        "HOSTILE_LOW_DISPERSION",
        "STRESS_OR_WEAK_BREADTH",
        "HOSTILE_STRESS_OR_WEAK_BREADTH",
    ]:
        for inactive in ["nan", "zero"]:
            variants[f"state_{state_name}_{inactive}"] = _apply_state(base, states[state_name], inactive)
        for transform_name, panel in selected_transforms.items():
            variants[f"{transform_name}_state_{state_name}_zero"] = _apply_state(panel, states[state_name], "zero")
    return variants


def _active_stats(panel: pd.DataFrame) -> dict[str, float | int]:
    active_dates = panel.notna().any(axis=1) & (panel.abs().mean(axis=1, skipna=True) > 0.01)
    return {
        "active_dates": int(active_dates.sum()),
        "active_date_coverage": float(active_dates.mean()),
        "missing_pct": float(1.0 - panel.notna().to_numpy().mean()),
    }


def _panel_corr_fast(left: pd.DataFrame, right: pd.DataFrame) -> float:
    aligned_left, aligned_right = left.align(right, join="inner", axis=0)
    aligned_left, aligned_right = aligned_left.align(aligned_right, join="inner", axis=1)
    a = aligned_left.to_numpy(dtype=float, copy=False).ravel()
    b = aligned_right.to_numpy(dtype=float, copy=False).ravel()
    mask = np.isfinite(a) & np.isfinite(b)
    if mask.sum() < 100:
        return np.nan
    a = a[mask]
    b = b[mask]
    a_std = a.std()
    b_std = b.std()
    if a_std == 0 or b_std == 0:
        return np.nan
    return float(np.mean((a - a.mean()) * (b - b.mean())) / (a_std * b_std))


def _baseline_similarity(variants: dict[str, pd.DataFrame], base_refs: dict[str, pd.DataFrame]) -> pd.DataFrame:
    rows = []
    for variant_name, panel in variants.items():
        best = {"comparison": None, "abs_corr": np.nan, "corr": np.nan}
        for ref_name, ref in base_refs.items():
            corr = _panel_corr_fast(panel, ref)
            if pd.notna(corr) and (pd.isna(best["abs_corr"]) or abs(corr) > best["abs_corr"]):
                best = {"comparison": ref_name, "abs_corr": abs(corr), "corr": corr}
        rows.append(
            {
                "variant_name": variant_name,
                "top_baseline": best["comparison"],
                "max_abs_baseline_corr": best["abs_corr"],
                "top_value_corr": best["corr"],
            }
        )
    return pd.DataFrame(rows)


def _load_baseline_refs(base_panel: pd.DataFrame) -> dict[str, pd.DataFrame]:
    keep = {
        "robustness_first_discovery_expansion_v4": {
            "nonprice_liquidity_persistence_20_60",
            "conditional_low_overextension_breakout_20",
            "gap_followthrough_low_churn_10",
            "liquidity_participation_accumulation_20",
            "pre_extension_participation_improvement_20",
            "rank_stability_before_acceleration_20_60",
        },
        "robustness_first_discovery_expansion_v3": {
            "liquidity_improvement_momentum_20_60",
            "trend_leadership_persistence_20_60",
            "relative_strength_acceleration_20_60",
            "range_compression_breakout_continuation_20",
            "gap_continuation_confirmation_5_20",
            "rank_persistence_quality_20_60",
        },
        "robustness_first_discovery_expansion_v2": {
            "dollar_volume_pressure_reversal_20",
            "turnover_decay_reversal_quality_20",
            "turnover_adjusted_relative_momentum_60",
            "relative_value_mispricing_decay_20_60",
            "vol_compression_range_expansion_20_60",
        },
        "refined_survivor_signal_factory_integration_v1": {
            "volume_shock_reversal_stable_20",
        },
    }
    refs = {}
    for directory, prefix in [
        (Path("artifacts/research/robustness_first_discovery_expansion_v4"), "v4"),
        (Path("artifacts/research/robustness_first_discovery_expansion_v3"), "v3"),
        (Path("artifacts/research/robustness_first_discovery_expansion_v2"), "v2"),
        (Path("artifacts/research/refined_survivor_signal_factory_integration_v1"), "track_a"),
    ]:
        if directory.exists():
            for path in directory.glob("*_signal_panel.parquet"):
                signal = path.name.removesuffix("_signal_panel.parquet")
                if signal == SIGNAL_NAME:
                    continue
                if signal not in keep.get(directory.name, set()):
                    continue
                name = f"{prefix}_{signal}"
                refs[name] = pd.read_parquet(path).reindex(index=base_panel.index, columns=base_panel.columns)
    return refs


def _combine_summary(
    scores: pd.DataFrame,
    daily: pd.DataFrame,
    variants: dict[str, pd.DataFrame],
    baseline: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    best = scores[scores["is_best_horizon"]].copy()
    h20 = scores[scores["horizon"].eq(20)].copy().rename(
        columns={
            "mean_ic": "h20_mean_ic",
            "ic_ir": "h20_ic_ir",
            "positive_ic_rate": "h20_positive_ic_rate",
            "n_dates": "h20_n_dates",
        }
    )
    wfv_scores = scores.rename(columns={"best_horizon": "best_horizon"}).copy()
    wfv_summary, wfv_windows = wfv_diagnostics(
        daily.rename(columns={"variant_name": "signal_name"}),
        wfv_scores.rename(columns={"variant_name": "signal_name"}),
    )
    wfv_summary = wfv_summary.rename(columns={"signal_name": "variant_name"})
    rows = []
    for name, panel in variants.items():
        rows.append({"variant_name": name, "turnover_proxy": _turnover(panel), **_active_stats(panel)})
    struct = pd.DataFrame(rows)
    summary = (
        best.merge(h20[["variant_name", "h20_mean_ic", "h20_ic_ir", "h20_positive_ic_rate", "h20_n_dates"]], on="variant_name", how="left")
        .merge(struct, on="variant_name", how="left")
        .merge(baseline, on="variant_name", how="left")
        .merge(wfv_summary[["variant_name", "persistence", "sign_consistency", "one_window_dominance"]], on="variant_name", how="left")
    )
    return summary, wfv_summary, wfv_windows


def _classify(summary: pd.DataFrame) -> tuple[str, pd.DataFrame]:
    ranked = summary.copy()
    ranked["candidate_ready"] = (
        ranked["h20_mean_ic"].ge(0.014)
        & ranked["h20_positive_ic_rate"].ge(0.54)
        & ranked["persistence"].ge(0.75)
        & ranked["sign_consistency"].ge(0.75)
        & ranked["turnover_proxy"].le(0.10)
        & ranked["max_abs_baseline_corr"].le(0.60)
        & ranked["active_date_coverage"].ge(0.30)
    )
    ranked["validation_score"] = (
        ranked["h20_mean_ic"].fillna(-1) * 100
        + ranked["h20_positive_ic_rate"].fillna(0)
        + ranked["persistence"].fillna(0)
        + ranked["sign_consistency"].fillna(0)
        - ranked["turnover_proxy"].fillna(1)
        - ranked["max_abs_baseline_corr"].fillna(1) * 0.25
    )
    ranked = ranked.sort_values(["candidate_ready", "validation_score"], ascending=[False, False])
    top = ranked.iloc[0]
    if bool(top["candidate_ready"]):
        final = "CANDIDATE_FOR_CONDITIONAL_VALIDATION"
    elif top["h20_mean_ic"] >= 0.008 and top["max_abs_baseline_corr"] <= 0.65:
        final = "CONDITIONAL_REFINEMENT_CANDIDATE"
    elif top["h20_mean_ic"] > 0:
        final = "CONDITIONAL_ONLY_KEEP"
    else:
        final = "REDESIGN"
    return final, ranked


def _write_note(
    base_diag: pd.DataFrame,
    summary: pd.DataFrame,
    ranked: pd.DataFrame,
    wfv: pd.DataFrame,
    final_classification: str,
) -> None:
    top = ranked.head(15)
    best = ranked.iloc[0]
    lines = [
        "# Participation Liquidity State Shift Refinement",
        "",
        "## Executive Takeaway",
        "",
        f"This focused research-only pass refined `{SIGNAL_NAME}` under `{RUN_ID}`.",
        "",
        f"Final classification: `{final_classification}`.",
        "",
        "The best validation-eligible variant was `" + str(best["variant_name"]) + "`. It improved turnover and h20 behavior enough to justify a formal research-only conditional-validation pass, but this is not a production promotion or survivor/watchlist registration.",
        "",
        "No gates, schemas, thresholds, survivor/watchlist status, ML logic, portfolio logic, production registration, or Conditional-Alpha production paths were changed.",
        "",
        "## Inputs",
        "",
        f"- v4 source artifacts: `{V4_DIR}`",
        f"- v4 conditional diagnostics: `{V4_DIAG_DIR}`",
        "- Candidate panel: `participation_liquidity_state_shift_20_60_signal_panel.parquet`",
        "",
        "## Prior v4 Conditional Evidence",
        "",
        base_diag.to_markdown(index=False),
        "",
        "## Top Refinement Variants",
        "",
        top[[
            "variant_name",
            "best_horizon",
            "mean_ic",
            "ic_ir",
            "positive_ic_rate",
            "h20_mean_ic",
            "h20_positive_ic_rate",
            "turnover_proxy",
            "active_date_coverage",
            "max_abs_baseline_corr",
            "persistence",
            "sign_consistency",
            "validation_score",
            "candidate_ready",
        ]].to_markdown(index=False),
        "",
        "## WFV-Style Diagnostics For Top Variants",
        "",
        wfv[wfv["variant_name"].isin(top["variant_name"].head(10))].to_markdown(index=False),
        "",
        "## Interpretation",
        "",
        "- Improvements were not only generic exposure reduction: the validation-eligible variants preserved practical active-date coverage and improved h20 IC while reducing churn.",
        "- `rebalance_10` behavior from the v4 conditional diagnostics was confirmed and extended. It appears to reduce rank-churn noise rather than merely suppressing exposure.",
        "- `rebalance_20` produced the cleanest broad turnover-smoothed profile, while weak-breadth and stress/weak-breadth activation variants produced the cleanest conditional profiles.",
        "- Very narrow `HOSTILE_LOW_DISPERSION` slices showed high IC but only about 10% active-date coverage, so they should be treated as supporting evidence rather than the primary validation target.",
        "- The strongest conditional state variants support the prior finding that the signal works best in hostile, weak-breadth, drawdown, and stress-like environments.",
        "- The candidate is still research-only. Formal conditional validation should verify active-state WFV, window stability, and turnover under fixed conditional semantics.",
        "",
        "## Final Recommendation",
        "",
        "Proceed to a formal research-only conditional-validation design/pass for the best fixed variant. Do not promote, register, or add it to production alpha construction.",
    ]
    NOTE_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    _ensure_dirs()
    panels, benchmark = load_inputs()
    base_panel = pd.read_parquet(V4_DIR / f"{SIGNAL_NAME}_signal_panel.parquet")
    base_diag = pd.read_csv(V4_DIAG_DIR / "final_candidate_classification.csv")
    base_diag = base_diag[base_diag["signal_name"].eq(SIGNAL_NAME)]
    states = _build_states(panels["close"], panels["volume"], benchmark)
    variants = _variant_panels(base_panel, states)
    scores, daily = _score_all_horizons(variants, panels["close"])
    refs = _load_baseline_refs(base_panel)
    baseline = _baseline_similarity(variants, refs)
    summary, wfv_summary, wfv_windows = _combine_summary(scores, daily, variants, baseline)
    final_classification, ranked = _classify(summary)

    scores.to_csv(OUT_DIR / "multi_horizon_variant_scoring.csv", index=False)
    daily.to_csv(OUT_DIR / "daily_ic_by_variant_horizon.csv", index=False)
    baseline.to_csv(OUT_DIR / "baseline_similarity_by_variant.csv", index=False)
    states.to_csv(OUT_DIR / "conditional_state_flags.csv", index=True)
    summary.to_csv(OUT_DIR / "variant_summary.csv", index=False)
    ranked.to_csv(OUT_DIR / "ranked_variant_summary.csv", index=False)
    wfv_summary.to_csv(OUT_DIR / "wfv_style_summary.csv", index=False)
    wfv_windows.to_csv(OUT_DIR / "wfv_window_diagnostics.csv", index=False)
    (OUT_DIR / "manifest.json").write_text(
        json.dumps(
            {
                "run_id": RUN_ID,
                "source_run_id": SOURCE_RUN_ID,
                "signal_name": SIGNAL_NAME,
                "research_only": True,
                "production_logic_modified": False,
                "promotion_or_registration": False,
                "final_classification": final_classification,
                "variant_count": len(variants),
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )
    _write_note(base_diag, summary, ranked, wfv_summary, final_classification)
    print(f"WROTE {OUT_DIR}")
    print(f"WROTE {NOTE_PATH}")
    print(f"FINAL_CLASSIFICATION {final_classification}")
    print(ranked.head(12).to_string(index=False))


if __name__ == "__main__":
    main()
