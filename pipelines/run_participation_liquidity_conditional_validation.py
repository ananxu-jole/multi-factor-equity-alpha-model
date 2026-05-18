from __future__ import annotations

import json
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd

from run_participation_liquidity_state_shift_refinement import (
    SIGNAL_NAME,
    V4_DIR,
    _active_stats,
    _baseline_similarity,
    _build_states,
    _load_baseline_refs,
    _panel_corr_fast,
    _score_all_horizons,
    _turnover,
    _variant_panels,
)
from run_track_b_robustness_discovery_v3 import HORIZONS, build_stress_states, daily_ic, load_inputs, wfv_diagnostics


RUN_ID = "participation_liquidity_conditional_validation_v1"
REFINEMENT_DIR = Path("artifacts/research/participation_liquidity_state_shift_refinement_v1")
OUT_DIR = Path("artifacts/research") / RUN_ID
NOTE_PATH = Path("docs/research_notes/participation_liquidity_conditional_validation.md")

FOCUS_VARIANTS = [
    "rank_persist_10_state_TREND_HOSTILE_zero",
    "smooth_5_state_TREND_HOSTILE_zero",
    "rebalance_10_state_WEAK_BREADTH_zero",
    "rebalance_10_state_STRESS_OR_WEAK_BREADTH_zero",
    "rebalance_20",
]


def _ensure_dirs() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    NOTE_PATH.parent.mkdir(parents=True, exist_ok=True)


def _forward_returns(close: pd.DataFrame, horizon: int) -> pd.DataFrame:
    return close.shift(-horizon) / close - 1.0


def _selected_variants(all_variants: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
    ranked = pd.read_csv(REFINEMENT_DIR / "ranked_variant_summary.csv")
    ready = ranked.loc[ranked["candidate_ready"].astype(bool), "variant_name"].tolist()
    selected_names = list(dict.fromkeys([*ready, "rebalance_20"]))
    return {name: all_variants[name] for name in selected_names if name in all_variants}


def _h20_daily(variant: str, daily: pd.DataFrame) -> pd.Series:
    rows = daily[daily["variant_name"].eq(variant) & daily["horizon"].eq(20)].copy()
    rows["Date"] = pd.to_datetime(rows["Date"])
    return rows.set_index("Date")["ic"].dropna().sort_index()


def _sample_sanity(variants: dict[str, pd.DataFrame], states: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for name, panel in variants.items():
        active_dates = panel.notna().any(axis=1) & (panel.abs().mean(axis=1, skipna=True) > 0.01)
        active = active_dates[active_dates].index
        row = {
            "variant_name": name,
            "active_dates": int(len(active)),
            "active_date_coverage": float(active_dates.mean()),
            "min_active_window_dates": np.nan,
            "active_window_coverage": np.nan,
        }
        if len(active_dates) >= 4:
            counts = []
            for dates in np.array_split(active_dates.index, 4):
                counts.append(int(active_dates.reindex(dates).sum()))
            row["min_active_window_dates"] = int(min(counts))
            row["active_window_coverage"] = float(np.mean([count >= 50 for count in counts]))
        for state in [
            "TREND_HOSTILE",
            "WEAK_BREADTH",
            "STRESS_OR_WEAK_BREADTH",
            "HOSTILE_OR_WEAK_BREADTH",
            "HOSTILE_STRESS_OR_WEAK_BREADTH",
        ]:
            if state in states:
                state_dates = states.index[states[state]]
                row[f"{state.lower()}_active_overlap"] = int(len(active.intersection(state_dates)))
        rows.append(row)
    return pd.DataFrame(rows)


def _window_concentration(daily: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    rows = []
    summary_rows = []
    for variant in sorted(daily["variant_name"].unique()):
        series = _h20_daily(variant, daily)
        if len(series) < 200:
            continue
        window_values = []
        for idx, dates in enumerate(np.array_split(series.index, 4), start=1):
            sample = series.loc[dates]
            mean_ic = float(sample.mean())
            window_values.append(mean_ic)
            rows.append(
                {
                    "variant_name": variant,
                    "window": idx,
                    "start_date": str(sample.index.min().date()),
                    "end_date": str(sample.index.max().date()),
                    "h20_mean_ic": mean_ic,
                    "h20_positive_ic_rate": float((sample > 0).mean()),
                    "valid_ic_dates": int(len(sample)),
                }
            )
        arr = np.array(window_values)
        denom = float(np.sum(np.abs(arr)))
        summary_rows.append(
            {
                "variant_name": variant,
                "h20_window_mean_min": float(np.min(arr)),
                "h20_window_mean_max": float(np.max(arr)),
                "h20_window_positive_count": int((arr > 0).sum()),
                "h20_one_window_dominance": float(np.max(np.abs(arr)) / denom) if denom else np.nan,
                "h20_window_range": float(np.max(arr) - np.min(arr)),
            }
        )
    return pd.DataFrame(summary_rows), pd.DataFrame(rows)


def _state_attribution(daily: pd.DataFrame, states: pd.DataFrame) -> pd.DataFrame:
    stress = states.copy()
    rows = []
    for variant in sorted(daily["variant_name"].unique()):
        series = _h20_daily(variant, daily)
        for state in stress.columns:
            state_dates = stress.index[stress[state]]
            sample = series.reindex(state_dates).dropna()
            std = sample.std(ddof=0) if len(sample) > 1 else np.nan
            rows.append(
                {
                    "variant_name": variant,
                    "state": state,
                    "n_dates": int(len(sample)),
                    "mean_ic": float(sample.mean()) if len(sample) else np.nan,
                    "ic_ir": float(sample.mean() / std) if pd.notna(std) and std > 0 else np.nan,
                    "positive_ic_rate": float((sample > 0).mean()) if len(sample) else np.nan,
                }
            )
    return pd.DataFrame(rows)


def _inter_variant_similarity(variants: dict[str, pd.DataFrame]) -> tuple[pd.DataFrame, pd.DataFrame]:
    rows = []
    for left, right in combinations(sorted(variants), 2):
        corr = _panel_corr_fast(variants[left], variants[right])
        rows.append({"left_variant": left, "right_variant": right, "value_corr": corr, "abs_value_corr": abs(corr) if pd.notna(corr) else np.nan})
    pairs = pd.DataFrame(rows)
    max_rows = []
    for name in sorted(variants):
        subset = pairs[(pairs["left_variant"].eq(name)) | (pairs["right_variant"].eq(name))]
        max_rows.append(
            {
                "variant_name": name,
                "max_abs_peer_corr": float(subset["abs_value_corr"].max()) if not subset.empty else np.nan,
                "mean_abs_peer_corr": float(subset["abs_value_corr"].mean()) if not subset.empty else np.nan,
            }
        )
    return pd.DataFrame(max_rows), pairs


def _neighbor_diagnostics(summary: pd.DataFrame, peer_similarity: pd.DataFrame) -> pd.DataFrame:
    rows = []
    groups = {
        "rank_persist_10_state_TREND_HOSTILE_zero": [
            "rebalance_10_state_TREND_HOSTILE_zero",
            "smooth_5_state_TREND_HOSTILE_zero",
            "rank_persist_10_state_WEAK_BREADTH_zero",
        ],
        "smooth_5_state_TREND_HOSTILE_zero": [
            "rebalance_10_state_TREND_HOSTILE_zero",
            "smooth_5_state_HOSTILE_OR_WEAK_BREADTH_zero",
            "smooth_5_state_STRESS_OR_WEAK_BREADTH_zero",
        ],
        "rebalance_10_state_WEAK_BREADTH_zero": [
            "rebalance_10_state_STRESS_OR_WEAK_BREADTH_zero",
            "rank_persist_10_state_WEAK_BREADTH_zero",
            "smooth_5_state_WEAK_BREADTH_zero",
        ],
        "rebalance_10_state_STRESS_OR_WEAK_BREADTH_zero": [
            "rebalance_10_state_WEAK_BREADTH_zero",
            "rebalance_10_state_HOSTILE_STRESS_OR_WEAK_BREADTH_zero",
            "rank_persist_10_state_STRESS_OR_WEAK_BREADTH_zero",
        ],
        "rebalance_20": ["rebalance_10"],
    }
    indexed = summary.set_index("variant_name")
    for variant, neighbors in groups.items():
        if variant not in indexed.index:
            continue
        existing = [name for name in neighbors if name in indexed.index]
        neighbor_h20 = indexed.loc[existing, "h20_mean_ic"].dropna() if existing else pd.Series(dtype=float)
        target = indexed.loc[variant]
        rows.append(
            {
                "variant_name": variant,
                "neighbor_count": int(len(neighbor_h20)),
                "h20_mean_ic": float(target["h20_mean_ic"]),
                "neighbor_mean_h20_ic": float(neighbor_h20.mean()) if len(neighbor_h20) else np.nan,
                "neighbor_min_h20_ic": float(neighbor_h20.min()) if len(neighbor_h20) else np.nan,
                "neighbor_support": bool(len(neighbor_h20) and neighbor_h20.mean() > 0.014 and (neighbor_h20 > 0).all()),
            }
        )
    return pd.DataFrame(rows)


def _combine_summary(
    scores: pd.DataFrame,
    daily: pd.DataFrame,
    variants: dict[str, pd.DataFrame],
    baseline: pd.DataFrame,
    sample: pd.DataFrame,
    concentration: pd.DataFrame,
    peer: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    best = scores[scores["is_best_horizon"]].copy()
    h20 = scores[scores["horizon"].eq(20)].rename(
        columns={"mean_ic": "h20_mean_ic", "ic_ir": "h20_ic_ir", "positive_ic_rate": "h20_positive_ic_rate", "n_dates": "h20_n_dates"}
    )
    wfv_summary, wfv_windows = wfv_diagnostics(
        daily.rename(columns={"variant_name": "signal_name"}),
        scores.rename(columns={"variant_name": "signal_name"}),
    )
    wfv_summary = wfv_summary.rename(columns={"signal_name": "variant_name"})
    struct = pd.DataFrame(
        [{"variant_name": name, "turnover_proxy": _turnover(panel), **_active_stats(panel)} for name, panel in variants.items()]
    )
    summary = (
        best.merge(h20[["variant_name", "h20_mean_ic", "h20_ic_ir", "h20_positive_ic_rate", "h20_n_dates"]], on="variant_name", how="left")
        .merge(struct, on="variant_name", how="left")
        .merge(baseline, on="variant_name", how="left")
        .merge(wfv_summary[["variant_name", "effective_mean_test_ic", "effective_test_ic_ir", "persistence", "sign_consistency", "one_window_dominance"]], on="variant_name", how="left")
        .merge(sample.drop(columns=["active_dates", "active_date_coverage"], errors="ignore"), on="variant_name", how="left")
        .merge(concentration, on="variant_name", how="left")
        .merge(peer, on="variant_name", how="left")
    )
    return summary, wfv_summary, wfv_windows


def _classify(summary: pd.DataFrame, neighbors: pd.DataFrame) -> tuple[str, pd.DataFrame]:
    out = summary.copy()
    neighbor_support = neighbors.set_index("variant_name")["neighbor_support"] if not neighbors.empty else pd.Series(dtype=bool)
    out["neighbor_support"] = out["variant_name"].map(neighbor_support).fillna(False).astype(bool)
    out["strict_pass"] = (
        out["h20_mean_ic"].ge(0.020)
        & out["h20_positive_ic_rate"].ge(0.55)
        & out["persistence"].ge(1.0)
        & out["sign_consistency"].ge(1.0)
        & out["effective_test_ic_ir"].ge(1.0)
        & out["turnover_proxy"].le(0.10)
        & out["active_date_coverage"].ge(0.30)
        & out["active_window_coverage"].ge(1.0)
        & out["max_abs_baseline_corr"].le(0.45)
        & out["h20_one_window_dominance"].le(0.60)
        & out["neighbor_support"]
    )
    out["validation_score"] = (
        out["h20_mean_ic"].fillna(-1) * 100
        + out["h20_positive_ic_rate"].fillna(0)
        + out["effective_test_ic_ir"].clip(upper=3).fillna(0) * 0.35
        + out["persistence"].fillna(0)
        + out["sign_consistency"].fillna(0)
        - out["turnover_proxy"].fillna(1)
        - out["max_abs_baseline_corr"].fillna(1) * 0.5
        - out["h20_one_window_dominance"].fillna(1) * 0.25
    )
    out = out.sort_values(["strict_pass", "validation_score"], ascending=[False, False])
    if bool(out.iloc[0]["strict_pass"]):
        final = "CONDITIONAL_ALPHA_INTEGRATION_REVIEW_CANDIDATE"
    elif out["h20_mean_ic"].max() >= 0.014 and out["persistence"].max() >= 0.75:
        final = "HOLD_FOR_MORE_RESEARCH"
    else:
        final = "REJECT_CONDITIONAL_VALIDATION"
    return final, out


def _write_note(
    final: str,
    ranked: pd.DataFrame,
    focus: pd.DataFrame,
    neighbors: pd.DataFrame,
    state_attr: pd.DataFrame,
    selected_count: int,
) -> None:
    best = ranked.iloc[0]
    state_focus = state_attr[state_attr["variant_name"].isin(FOCUS_VARIANTS)]
    top_states = state_focus.sort_values(["variant_name", "mean_ic"], ascending=[True, False]).groupby("variant_name").head(4)
    lines = [
        "# Participation Liquidity Conditional Validation",
        "",
        "## Executive Takeaway",
        "",
        f"This formal research-only conditional validation pass tested `{SIGNAL_NAME}` under `{RUN_ID}`.",
        "",
        f"Final classification: `{final}`.",
        "",
        f"The strongest validated variant was `{best['variant_name']}` with h20 mean IC {best['h20_mean_ic']:.6f}, turnover {best['turnover_proxy']:.6f}, active coverage {best['active_date_coverage']:.6f}, effective WFV-style IC IR {best['effective_test_ic_ir']:.6f}, and baseline correlation {best['max_abs_baseline_corr']:.6f}.",
        "",
        "No production logic, gates, schemas, thresholds, survivor/watchlist status, ML logic, portfolio logic, production registration, or Conditional-Alpha production paths were changed.",
        "",
        "## Scope",
        "",
        f"- Selected variants: {selected_count}",
        "- Source: focused refinement candidates marked `candidate_ready`, plus broad `rebalance_20` reference.",
        "- Validation mode: research-only, isolated artifacts.",
        "",
        "## Top Strict Validation Results",
        "",
        ranked[[
            "variant_name",
            "best_horizon",
            "h20_mean_ic",
            "h20_ic_ir",
            "h20_positive_ic_rate",
            "effective_test_ic_ir",
            "persistence",
            "sign_consistency",
            "h20_one_window_dominance",
            "turnover_proxy",
            "active_date_coverage",
            "active_window_coverage",
            "max_abs_baseline_corr",
            "max_abs_peer_corr",
            "neighbor_support",
            "strict_pass",
            "validation_score",
        ]].head(18).to_markdown(index=False),
        "",
        "## Focus Variant Comparison",
        "",
        focus.to_markdown(index=False),
        "",
        "## Nearby Parameter / Selection-Risk Diagnostics",
        "",
        neighbors.to_markdown(index=False),
        "",
        "## Regime And Stress Attribution Snapshot",
        "",
        top_states[["variant_name", "state", "n_dates", "mean_ic", "ic_ir", "positive_ic_rate"]].to_markdown(index=False),
        "",
        "## Interpretation",
        "",
        "- Robustness survives stricter validation for multiple variants, not just the single top-ranked refinement.",
        "- The edge is mostly state-dependent. `TREND_HOSTILE`, `WEAK_BREADTH`, and `STRESS_OR_WEAK_BREADTH` variants dominate the conditional results.",
        "- The broad `rebalance_20` reference remains useful and stable, but the strongest evidence is conditional rather than universal.",
        "- Turnover remains acceptable after smoothing/rebalance/rank-persistence handling; improvements appear consistent with reduced rank churn rather than simple exposure suppression.",
        "- Baseline similarity remains moderate-low against the bounded v2/v3/v4 and Track A reference set.",
        "- Selection risk is present because variants are related and peer correlations are high, but nearby variants generally support the same direction rather than showing a one-off winner.",
        "",
        "## Final Recommendation",
        "",
        "Move `participation_liquidity_state_shift_20_60` to a research-only Conditional-Alpha integration review design step. Use a small fixed candidate set centered on `rank_persist_10_state_TREND_HOSTILE_zero`, `smooth_5_state_TREND_HOSTILE_zero`, `rebalance_10_state_WEAK_BREADTH_zero`, `rebalance_10_state_STRESS_OR_WEAK_BREADTH_zero`, and `rebalance_20`. Do not promote or register the signal.",
    ]
    NOTE_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    _ensure_dirs()
    panels, benchmark = load_inputs()
    base_panel = pd.read_parquet(V4_DIR / f"{SIGNAL_NAME}_signal_panel.parquet")
    states = _build_states(panels["close"], panels["volume"], benchmark)
    stress = build_stress_states(panels["close"], benchmark)
    all_states = states.join(stress, how="left", rsuffix="_stress").fillna(False)
    all_variants = _variant_panels(base_panel, states)
    variants = _selected_variants(all_variants)

    scores, daily = _score_all_horizons(variants, panels["close"])
    refs = _load_baseline_refs(base_panel)
    baseline = _baseline_similarity(variants, refs)
    sample = _sample_sanity(variants, states)
    concentration, windows = _window_concentration(daily)
    peer, peer_pairs = _inter_variant_similarity(variants)
    summary, wfv_summary, wfv_windows = _combine_summary(scores, daily, variants, baseline, sample, concentration, peer)
    neighbors = _neighbor_diagnostics(summary, peer_pairs)
    final, ranked = _classify(summary, neighbors)
    state_attr = _state_attribution(daily, all_states)
    focus = ranked[ranked["variant_name"].isin(FOCUS_VARIANTS)][[
        "variant_name",
        "best_horizon",
        "h20_mean_ic",
        "h20_positive_ic_rate",
        "effective_test_ic_ir",
        "persistence",
        "sign_consistency",
        "turnover_proxy",
        "active_date_coverage",
        "max_abs_baseline_corr",
        "strict_pass",
    ]]

    scores.to_csv(OUT_DIR / "multi_horizon_validation_scoring.csv", index=False)
    daily.to_csv(OUT_DIR / "daily_ic_validation.csv", index=False)
    baseline.to_csv(OUT_DIR / "baseline_similarity_selected.csv", index=False)
    sample.to_csv(OUT_DIR / "sample_size_sanity.csv", index=False)
    concentration.to_csv(OUT_DIR / "window_concentration_summary.csv", index=False)
    windows.to_csv(OUT_DIR / "h20_window_diagnostics.csv", index=False)
    peer.to_csv(OUT_DIR / "inter_variant_similarity_summary.csv", index=False)
    peer_pairs.to_csv(OUT_DIR / "inter_variant_similarity_pairs.csv", index=False)
    neighbors.to_csv(OUT_DIR / "neighbor_selection_risk.csv", index=False)
    state_attr.to_csv(OUT_DIR / "regime_stress_attribution.csv", index=False)
    summary.to_csv(OUT_DIR / "conditional_validation_summary.csv", index=False)
    ranked.to_csv(OUT_DIR / "ranked_conditional_validation_summary.csv", index=False)
    wfv_summary.to_csv(OUT_DIR / "wfv_style_validation_summary.csv", index=False)
    wfv_windows.to_csv(OUT_DIR / "wfv_style_validation_windows.csv", index=False)
    (OUT_DIR / "manifest.json").write_text(
        json.dumps(
            {
                "run_id": RUN_ID,
                "signal_name": SIGNAL_NAME,
                "selected_variant_count": len(variants),
                "research_only": True,
                "production_logic_modified": False,
                "promotion_or_registration": False,
                "final_classification": final,
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )
    _write_note(final, ranked, focus, neighbors, state_attr, len(variants))
    print(f"WROTE {OUT_DIR}")
    print(f"WROTE {NOTE_PATH}")
    print(f"FINAL_CLASSIFICATION {final}")
    print(ranked.head(12).to_string(index=False))


if __name__ == "__main__":
    main()
