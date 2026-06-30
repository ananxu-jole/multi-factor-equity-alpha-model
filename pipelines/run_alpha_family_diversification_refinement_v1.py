from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd


RUN_ID = "alpha_family_diversification_refinement_v1"
SOURCE_RUN_ID = "alpha_family_diversification_discovery_v1"
SOURCE_PANEL_DIR = Path("artifacts/panels/signals")
SOURCE_DISCOVERY_DIR = Path("artifacts/research") / SOURCE_RUN_ID
SOURCE_CANDIDATE_PANEL_DIR = SOURCE_DISCOVERY_DIR / "candidate_panels"
OUT_DIR = Path("artifacts/research") / RUN_ID
CANDIDATE_PANEL_DIR = OUT_DIR / "candidate_panels"
CLOSE_PATH = Path("data/processed/phase2/nb01_data_foundation/close_prices.parquet")

PANEL_GENERATION_LOOKBACK_ROWS = 504
REDUNDANCY_LOOKBACK_ROWS = 252
HORIZONS = (1, 5, 10, 20)

SOURCE_PANEL_NAMES = [
    "failed_breakout_reversal_20",
    "failed_breakout_reversal_20_low_breadth",
    "percentile_rank_stability_20",
    "percentile_rank_stability_20_downtrend",
    "range_compression_breakout_10",
    "range_expansion_failure_5",
    "relative_return_rank_20",
    "relative_return_zscore_60",
    "residual_return_vs_universe_20",
    "smooth_trend_persistence_60",
    "smooth_trend_persistence_60_downtrend",
    "trend_consistency_20_60",
    "trend_consistency_20_60_persistent",
    "vol_compression_breakout_20_60",
    "vol_of_vol_20",
    "vol_surprise_20_60",
]

APPROVED_ANCHORS = {
    "post_drawdown_persistence_20",
    "dispersion_transition_acceleration_20",
}

APPROVED_DISCOVERY_COMPARISON_SIGNALS = [
    "dispersion_expansion_momentum_20",
    "dispersion_transition_acceleration_20",
    "dispersion_compression_stability_20",
    "dispersion_skew_anomaly_20",
    "cross_sectional_asymmetry_20",
    "drawdown_rank_stability_20",
    "post_drawdown_persistence_20",
    "transition_rank_stability_20",
]

STRESS_REPAIR_PROXY_SIGNALS = [
    "failed_breakout_reversal_20",
    "failed_breakout_reversal_20_low_breadth",
    "percentile_rank_stability_20_downtrend",
]

RESEARCH_ONLY_GUARDRAIL = (
    "Research-only alpha-family diversification refinement execution. No validation, "
    "governance mutation, threshold change, production registration, ML integration, "
    "or candidate promotion/demotion is performed."
)


REFINEMENT_CANDIDATES = [
    {
        "candidate_id": "rank_stability_after_drawdown_02_anchor",
        "parent_candidate_id": "rank_stability_after_drawdown_02",
        "signal_name": "post_drawdown_persistence_20",
        "family": "persistence",
        "theme": "Rank Stability After Drawdown",
        "horizon": "h10-h20",
        "variant_role": "original_anchor",
        "diagnostic_purpose": "Retain original post-drawdown persistence representative as the comparison anchor.",
    },
    {
        "candidate_id": "rank_stability_after_drawdown_02_core",
        "parent_candidate_id": "rank_stability_after_drawdown_02",
        "signal_name": "post_drawdown_persistence_core_20",
        "family": "persistence",
        "theme": "Rank Stability After Drawdown",
        "horizon": "h10-h20",
        "variant_role": "rank_persistence_definition",
        "diagnostic_purpose": "Test rank persistence without the smooth-downtrend additive layer.",
    },
    {
        "candidate_id": "rank_stability_after_drawdown_02_churn_adjusted",
        "parent_candidate_id": "rank_stability_after_drawdown_02",
        "signal_name": "post_drawdown_persistence_churn_adjusted_20",
        "family": "persistence",
        "theme": "Rank Stability After Drawdown",
        "horizon": "h10-h20",
        "variant_role": "rank_churn_definition",
        "diagnostic_purpose": "Penalize post-drawdown rank churn while preserving the persistence thesis.",
    },
    {
        "candidate_id": "rank_stability_after_drawdown_02_smoothed",
        "parent_candidate_id": "rank_stability_after_drawdown_02",
        "signal_name": "post_drawdown_persistence_smoothed_20",
        "family": "persistence",
        "theme": "Rank Stability After Drawdown",
        "horizon": "h10-h20",
        "variant_role": "light_noise_control",
        "diagnostic_purpose": "Apply light smoothing to test sensitivity to daily rank noise.",
    },
    {
        "candidate_id": "rank_stability_after_drawdown_02_strict",
        "parent_candidate_id": "rank_stability_after_drawdown_02",
        "signal_name": "post_drawdown_persistence_strict_20",
        "family": "persistence",
        "theme": "Rank Stability After Drawdown",
        "horizon": "h10-h20",
        "variant_role": "drawdown_context_strictness",
        "diagnostic_purpose": "Require stronger downtrend-rank context without adding stress-repair features.",
    },
    {
        "candidate_id": "dispersion_expansion_transition_04_anchor",
        "parent_candidate_id": "dispersion_expansion_transition_04",
        "signal_name": "dispersion_transition_acceleration_20",
        "family": "dispersion",
        "theme": "Dispersion Expansion Transition",
        "horizon": "h10-h20",
        "variant_role": "original_anchor",
        "diagnostic_purpose": "Retain original dispersion-transition acceleration representative as the comparison anchor.",
    },
    {
        "candidate_id": "dispersion_expansion_transition_04_alt_accel",
        "parent_candidate_id": "dispersion_expansion_transition_04",
        "signal_name": "dispersion_transition_acceleration_alt_20",
        "family": "dispersion",
        "theme": "Dispersion Expansion Transition",
        "horizon": "h10-h20",
        "variant_role": "acceleration_measurement",
        "diagnostic_purpose": "Use a nearby acceleration definition to test transition-measure robustness.",
    },
    {
        "candidate_id": "dispersion_expansion_transition_04_smoothed",
        "parent_candidate_id": "dispersion_expansion_transition_04",
        "signal_name": "dispersion_transition_acceleration_smoothed_20",
        "family": "dispersion",
        "theme": "Dispersion Expansion Transition",
        "horizon": "h10-h20",
        "variant_role": "light_noise_control",
        "diagnostic_purpose": "Smooth acceleration lightly to test sensitivity to transient dispersion spikes.",
    },
    {
        "candidate_id": "dispersion_expansion_transition_04_rising_state",
        "parent_candidate_id": "dispersion_expansion_transition_04",
        "signal_name": "dispersion_transition_acceleration_rising_state_20",
        "family": "dispersion",
        "theme": "Dispersion Expansion Transition",
        "horizon": "h10-h20",
        "variant_role": "transition_state_definition",
        "diagnostic_purpose": "Narrow activation to rising-dispersion states without adding hostile/stress triggers.",
    },
    {
        "candidate_id": "dispersion_expansion_transition_04_neutralized",
        "parent_candidate_id": "dispersion_expansion_transition_04",
        "signal_name": "dispersion_transition_acceleration_neutralized_20",
        "family": "dispersion",
        "theme": "Dispersion Expansion Transition",
        "horizon": "h10-h20",
        "variant_role": "leadership_ranking_layer",
        "diagnostic_purpose": "Separate acceleration from raw high-dispersion exposure.",
    },
]


def _ensure_dirs() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    CANDIDATE_PANEL_DIR.mkdir(parents=True, exist_ok=True)


def _rank_cs(panel: pd.DataFrame) -> pd.DataFrame:
    return panel.rank(axis=1, pct=True).sub(0.5).mul(2.0)


def _clean_panel(panel: pd.DataFrame) -> pd.DataFrame:
    return panel.replace([np.inf, -np.inf], np.nan).clip(lower=-1.0, upper=1.0)


def _load_source_panels() -> dict[str, pd.DataFrame]:
    panels: dict[str, pd.DataFrame] = {}
    for name in SOURCE_PANEL_NAMES:
        path = SOURCE_PANEL_DIR / f"{name}.parquet"
        if not path.exists():
            raise FileNotFoundError(f"Missing required source panel: {path}")
        panel = pd.read_parquet(path)
        panel.index = pd.to_datetime(panel.index)
        panels[name] = panel.sort_index().tail(PANEL_GENERATION_LOOKBACK_ROWS)
    return _align_sources(panels)


def _align_sources(panels: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
    common_index = None
    common_columns = None
    for panel in panels.values():
        common_index = panel.index if common_index is None else common_index.intersection(panel.index)
        common_columns = panel.columns if common_columns is None else common_columns.intersection(panel.columns)
    if common_index is None or common_columns is None or len(common_index) == 0 or len(common_columns) == 0:
        raise ValueError("Source panels do not share a usable date/ticker intersection.")
    return {
        name: panel.reindex(index=common_index, columns=common_columns).astype(float)
        for name, panel in panels.items()
    }


def _refinement_signal_panels(source: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
    rr_z = source["relative_return_zscore_60"]
    rank_stability_downtrend = source["percentile_rank_stability_20_downtrend"]
    trend_persistent = source["trend_consistency_20_60_persistent"]
    smooth_downtrend = source["smooth_trend_persistence_60_downtrend"]

    rank_churn = rank_stability_downtrend.diff().abs().rolling(20, min_periods=10).mean()
    persistence_base = rank_stability_downtrend.add(trend_persistent, fill_value=0.0).add(smooth_downtrend, fill_value=0.0)
    persistence_core = rank_stability_downtrend.add(trend_persistent, fill_value=0.0)
    persistence_smoothed = persistence_base.rolling(5, min_periods=3).mean()
    strict_context = _rank_cs(rank_stability_downtrend).clip(lower=0.0)

    dispersion_level = _rank_cs(rr_z.abs())
    dispersion_accel = dispersion_level.diff(5).sub(dispersion_level.diff(20), fill_value=0.0)
    dispersion_alt_accel = dispersion_level.diff(10).sub(dispersion_level.diff(20), fill_value=0.0)
    dispersion_smoothed = dispersion_accel.rolling(5, min_periods=3).mean()
    universe_dispersion = rr_z.abs().mean(axis=1)
    rising_state = universe_dispersion.diff(20).gt(0.0).astype(float).reindex(dispersion_accel.index).fillna(0.0)
    dispersion_neutralized = dispersion_accel.sub(dispersion_level, fill_value=0.0)

    return {
        "post_drawdown_persistence_20": _clean_panel(_rank_cs(persistence_base)),
        "post_drawdown_persistence_core_20": _clean_panel(_rank_cs(persistence_core)),
        "post_drawdown_persistence_churn_adjusted_20": _clean_panel(
            _rank_cs(persistence_core.sub(rank_churn, fill_value=0.0))
        ),
        "post_drawdown_persistence_smoothed_20": _clean_panel(_rank_cs(persistence_smoothed)),
        "post_drawdown_persistence_strict_20": _clean_panel(_rank_cs(persistence_base.mul(strict_context))),
        "dispersion_transition_acceleration_20": _clean_panel(_rank_cs(dispersion_accel)),
        "dispersion_transition_acceleration_alt_20": _clean_panel(_rank_cs(dispersion_alt_accel)),
        "dispersion_transition_acceleration_smoothed_20": _clean_panel(_rank_cs(dispersion_smoothed)),
        "dispersion_transition_acceleration_rising_state_20": _clean_panel(
            _rank_cs(dispersion_accel.mul(rising_state, axis=0))
        ),
        "dispersion_transition_acceleration_neutralized_20": _clean_panel(_rank_cs(dispersion_neutralized)),
    }


def _panel_to_long(panel: pd.DataFrame, rec: dict[str, object]) -> pd.DataFrame:
    long_panel = panel.stack(future_stack=True).dropna().rename("signal_value").reset_index()
    long_panel.columns = ["date", "ticker", "signal_value"]
    long_panel["candidate_id"] = rec["candidate_id"]
    long_panel["parent_candidate_id"] = rec["parent_candidate_id"]
    long_panel["family"] = rec["family"]
    long_panel["theme"] = rec["theme"]
    long_panel["horizon"] = rec["horizon"]
    return long_panel[
        ["date", "ticker", "candidate_id", "parent_candidate_id", "signal_value", "family", "theme", "horizon"]
    ]


def _write_candidate_panels(registry: pd.DataFrame, panels: dict[str, pd.DataFrame]) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for rec in registry.to_dict(orient="records"):
        signal_name = rec["signal_name"]
        if signal_name not in panels:
            raise KeyError(f"No refinement panel registered for {signal_name}")
        long_panel = _panel_to_long(panels[signal_name], rec)
        panel_path = CANDIDATE_PANEL_DIR / f"{signal_name}.parquet"
        metadata_path = CANDIDATE_PANEL_DIR / f"{signal_name}.metadata.json"
        long_panel.to_parquet(panel_path, index=False)
        metadata_path.write_text(
            json.dumps(
                {
                    "run_id": RUN_ID,
                    "source_run_id": SOURCE_RUN_ID,
                    "candidate_id": rec["candidate_id"],
                    "parent_candidate_id": rec["parent_candidate_id"],
                    "signal_name": signal_name,
                    "research_only": True,
                    "variant_role": rec["variant_role"],
                    "diagnostic_purpose": rec["diagnostic_purpose"],
                    "source_panel_dir": str(SOURCE_PANEL_DIR),
                    "source_panel_names": SOURCE_PANEL_NAMES,
                    "lookback_rows": PANEL_GENERATION_LOOKBACK_ROWS,
                    "panel_format": "long",
                    "date_min": str(long_panel["date"].min().date()) if not long_panel.empty else None,
                    "date_max": str(long_panel["date"].max().date()) if not long_panel.empty else None,
                    "row_count": int(len(long_panel)),
                },
                indent=2,
                sort_keys=True,
            ),
            encoding="utf-8",
        )
        rows.append(
            {
                **rec,
                "panel_path": str(panel_path),
                "metadata_path": str(metadata_path),
                "row_count": int(len(long_panel)),
                "date_min": str(long_panel["date"].min().date()) if not long_panel.empty else None,
                "date_max": str(long_panel["date"].max().date()) if not long_panel.empty else None,
                "ticker_count": int(long_panel["ticker"].nunique()) if not long_panel.empty else 0,
                "generation_status": "generated",
            }
        )
    return pd.DataFrame(rows)


def _long_to_wide(path: str) -> pd.DataFrame:
    panel_long = pd.read_parquet(path)
    panel = panel_long.pivot_table(index="date", columns="ticker", values="signal_value", aggfunc="last")
    panel.index = pd.to_datetime(panel.index)
    return panel.sort_index()


def _forward_returns(close: pd.DataFrame, horizon: int) -> pd.DataFrame:
    return close.shift(-horizon) / close - 1.0


def _daily_ic(signal: pd.DataFrame, fwd: pd.DataFrame) -> pd.Series:
    values: list[float] = []
    dates: list[pd.Timestamp] = []
    for date in signal.index.intersection(fwd.index):
        s = signal.loc[date]
        r = fwd.loc[date]
        valid = s.notna() & r.notna()
        if int(valid.sum()) < 25:
            values.append(np.nan)
        else:
            values.append(float(s[valid].rank().corr(r[valid].rank())))
        dates.append(date)
    return pd.Series(values, index=pd.Index(dates, name="date"), dtype=float)


def _score_panels(manifest: pd.DataFrame, close: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    metadata = manifest.set_index("signal_name").to_dict("index")
    panels = {rec["signal_name"]: _long_to_wide(rec["panel_path"]) for rec in manifest.to_dict(orient="records")}
    score_rows: list[dict[str, object]] = []
    daily_rows: list[dict[str, object]] = []
    for horizon in HORIZONS:
        fwd = _forward_returns(close, horizon)
        for signal_name, panel in panels.items():
            rec = metadata[signal_name]
            aligned_panel = panel.reindex(index=close.index, columns=close.columns)
            ic = _daily_ic(aligned_panel, fwd)
            valid_ic = ic.dropna()
            mean_ic = float(valid_ic.mean()) if len(valid_ic) else np.nan
            std_ic = float(valid_ic.std(ddof=0)) if len(valid_ic) > 1 else np.nan
            score_rows.append(
                {
                    "candidate_id": rec["candidate_id"],
                    "parent_candidate_id": rec["parent_candidate_id"],
                    "signal_name": signal_name,
                    "family": rec["family"],
                    "theme": rec["theme"],
                    "variant_role": rec["variant_role"],
                    "declared_horizon": rec["horizon"],
                    "scored_horizon": horizon,
                    "mean_ic": mean_ic,
                    "abs_mean_ic": abs(mean_ic) if pd.notna(mean_ic) else np.nan,
                    "ic_std": std_ic,
                    "ic_ir": mean_ic / std_ic if pd.notna(std_ic) and std_ic > 0 else np.nan,
                    "positive_ic_rate": float((valid_ic > 0).mean()) if len(valid_ic) else np.nan,
                    "n_dates": int(len(valid_ic)),
                }
            )
            daily_rows.extend(
                {
                    "date": date,
                    "candidate_id": rec["candidate_id"],
                    "parent_candidate_id": rec["parent_candidate_id"],
                    "signal_name": signal_name,
                    "family": rec["family"],
                    "horizon": horizon,
                    "ic": value,
                }
                for date, value in valid_ic.items()
            )
    return pd.DataFrame(score_rows), pd.DataFrame(daily_rows)


def _correlation_pair(a: pd.DataFrame, b: pd.DataFrame) -> dict[str, object]:
    idx = a.index.intersection(b.index)
    cols = a.columns.intersection(b.columns)
    if len(idx) > REDUNDANCY_LOOKBACK_ROWS:
        idx = idx[-REDUNDANCY_LOOKBACK_ROWS:]
    aa = a.reindex(index=idx, columns=cols)
    bb = b.reindex(index=idx, columns=cols)
    flat = pd.DataFrame({"a": aa.to_numpy().ravel(), "b": bb.to_numpy().ravel()}).dropna()
    if len(flat) < 25:
        return {
            "value_correlation": np.nan,
            "rank_correlation": np.nan,
            "overlap_observations": int(len(flat)),
            "overlap_dates": int(len(idx)),
            "overlap_tickers": int(len(cols)),
        }
    return {
        "value_correlation": float(flat["a"].corr(flat["b"])),
        "rank_correlation": float(flat["a"].rank().corr(flat["b"].rank())),
        "overlap_observations": int(len(flat)),
        "overlap_dates": int(len(idx)),
        "overlap_tickers": int(len(cols)),
    }


def _load_discovery_comparison_panels() -> dict[str, pd.DataFrame]:
    panels: dict[str, pd.DataFrame] = {}
    for signal in APPROVED_DISCOVERY_COMPARISON_SIGNALS:
        path = SOURCE_CANDIDATE_PANEL_DIR / f"{signal}.parquet"
        if path.exists():
            panels[f"discovery::{signal}"] = _long_to_wide(str(path))
    return panels


def _redundancy_context(manifest: pd.DataFrame, source: dict[str, pd.DataFrame]) -> pd.DataFrame:
    refinement_panels = {rec["signal_name"]: _long_to_wide(rec["panel_path"]) for rec in manifest.to_dict(orient="records")}
    comparison_panels = {f"refinement::{k}": v for k, v in refinement_panels.items()}
    comparison_panels.update(_load_discovery_comparison_panels())
    comparison_panels.update({f"stress_proxy::{name}": source[name] for name in STRESS_REPAIR_PROXY_SIGNALS})

    rows: list[dict[str, object]] = []
    for rec in manifest.to_dict(orient="records"):
        signal_name = rec["signal_name"]
        panel = refinement_panels[signal_name]
        for comparison_name, comparison_panel in comparison_panels.items():
            if comparison_name == f"refinement::{signal_name}":
                continue
            corr = _correlation_pair(panel, comparison_panel)
            scope, comparison_signal = comparison_name.split("::", 1)
            rows.append(
                {
                    "candidate_id": rec["candidate_id"],
                    "signal_name": signal_name,
                    "family": rec["family"],
                    "comparison_scope": scope,
                    "comparison_signal": comparison_signal,
                    **corr,
                }
            )

    out = pd.DataFrame(rows)
    out["abs_value_correlation"] = out["value_correlation"].abs()
    out["abs_rank_correlation"] = out["rank_correlation"].abs()
    out["max_abs_correlation"] = out[["abs_value_correlation", "abs_rank_correlation"]].max(axis=1)
    return out


def _candidate_summary(scores: pd.DataFrame, redundancy: pd.DataFrame) -> pd.DataFrame:
    idx_cols = ["candidate_id", "parent_candidate_id", "signal_name", "family", "theme", "variant_role", "declared_horizon"]
    wide = scores.pivot_table(index=idx_cols, columns="scored_horizon", values="mean_ic")
    wide = wide.rename(columns={h: f"h{h}_mean_ic" for h in HORIZONS}).reset_index()
    pos = scores.pivot_table(index=["candidate_id"], columns="scored_horizon", values="positive_ic_rate")
    pos = pos.rename(columns={h: f"h{h}_positive_ic_rate" for h in HORIZONS}).reset_index()
    best = scores.loc[scores.groupby("candidate_id")["abs_mean_ic"].idxmax()].copy()
    primary = scores[scores["scored_horizon"].isin([10, 20])].copy()
    primary = primary.loc[primary.groupby("candidate_id")["abs_mean_ic"].idxmax()]

    red_rows: list[dict[str, object]] = []
    for candidate_id, group in redundancy.groupby("candidate_id"):
        row = {"candidate_id": candidate_id}
        for scope in ["refinement", "discovery", "stress_proxy"]:
            scoped = group[group["comparison_scope"] == scope]
            if scoped.empty:
                row[f"max_{scope}_abs_corr"] = np.nan
                row[f"top_{scope}_peer"] = None
            else:
                top = scoped.sort_values("max_abs_correlation", ascending=False).iloc[0]
                row[f"max_{scope}_abs_corr"] = float(top["max_abs_correlation"])
                row[f"top_{scope}_peer"] = top["comparison_signal"]
        red_rows.append(row)
    red = pd.DataFrame(red_rows)

    out = wide.merge(pos, on="candidate_id", how="left")
    out = out.merge(
        best[["candidate_id", "scored_horizon", "mean_ic", "ic_ir", "positive_ic_rate", "n_dates"]].rename(
            columns={
                "scored_horizon": "best_horizon",
                "mean_ic": "best_mean_ic",
                "ic_ir": "best_ic_ir",
                "positive_ic_rate": "best_positive_ic_rate",
                "n_dates": "best_n_dates",
            }
        ),
        on="candidate_id",
        how="left",
    )
    out = out.merge(
        primary[["candidate_id", "scored_horizon", "mean_ic", "ic_ir", "positive_ic_rate", "n_dates"]].rename(
            columns={
                "scored_horizon": "best_h10_h20_horizon",
                "mean_ic": "best_h10_h20_mean_ic",
                "ic_ir": "best_h10_h20_ic_ir",
                "positive_ic_rate": "best_h10_h20_positive_ic_rate",
                "n_dates": "best_h10_h20_n_dates",
            }
        ),
        on="candidate_id",
        how="left",
    )
    return out.merge(red, on="candidate_id", how="left")


def _family_summary(scores: pd.DataFrame) -> pd.DataFrame:
    return (
        scores.groupby(["family", "scored_horizon"], as_index=False)
        .agg(
            candidate_count=("candidate_id", "nunique"),
            mean_ic=("mean_ic", "mean"),
            median_ic=("mean_ic", "median"),
            mean_abs_ic=("abs_mean_ic", "mean"),
            mean_ic_ir=("ic_ir", "mean"),
            mean_positive_ic_rate=("positive_ic_rate", "mean"),
            total_dates=("n_dates", "sum"),
        )
        .sort_values(["family", "scored_horizon"])
    )


def main() -> int:
    _ensure_dirs()
    registry = pd.DataFrame(REFINEMENT_CANDIDATES)
    registry["run_id"] = RUN_ID
    if len(registry) != 10:
        raise ValueError("Refinement scope must remain 8 variants plus 2 original anchors.")
    if set(registry.loc[registry["variant_role"] == "original_anchor", "signal_name"]) != APPROVED_ANCHORS:
        raise ValueError("Refinement anchors do not match the approved candidates.")

    source = _load_source_panels()
    panels = _refinement_signal_panels(source)
    manifest = _write_candidate_panels(registry, panels)
    close = pd.read_parquet(CLOSE_PATH)
    close.index = pd.to_datetime(close.index)
    scores, daily = _score_panels(manifest, close)
    redundancy = _redundancy_context(manifest, source)
    candidate_scores = _candidate_summary(scores, redundancy)
    family_summary = _family_summary(scores)

    registry.to_csv(OUT_DIR / "candidate_inventory.csv", index=False)
    manifest.to_csv(OUT_DIR / "panel_manifest.csv", index=False)
    scores.to_csv(OUT_DIR / "candidate_horizon_scores.csv", index=False)
    daily.to_csv(OUT_DIR / "daily_ic_by_candidate_horizon.csv", index=False)
    candidate_scores.to_csv(OUT_DIR / "refinement_candidate_scores.csv", index=False)
    family_summary.to_csv(OUT_DIR / "family_summary.csv", index=False)
    redundancy.to_csv(OUT_DIR / "redundancy_context.csv", index=False)
    (OUT_DIR / "manifest.json").write_text(
        json.dumps(
            {
                "run_id": RUN_ID,
                "source_run_id": SOURCE_RUN_ID,
                "research_only": True,
                "research_only_guardrail": RESEARCH_ONLY_GUARDRAIL,
                "eligible_parent_candidate_ids": [
                    "rank_stability_after_drawdown_02",
                    "dispersion_expansion_transition_04",
                ],
                "candidate_count": int(len(registry)),
                "new_variant_count": int(len(registry) - 2),
                "horizons": list(HORIZONS),
                "outputs": {
                    "candidate_inventory": str(OUT_DIR / "candidate_inventory.csv"),
                    "panel_manifest": str(OUT_DIR / "panel_manifest.csv"),
                    "candidate_horizon_scores": str(OUT_DIR / "candidate_horizon_scores.csv"),
                    "daily_ic_by_candidate_horizon": str(OUT_DIR / "daily_ic_by_candidate_horizon.csv"),
                    "refinement_candidate_scores": str(OUT_DIR / "refinement_candidate_scores.csv"),
                    "family_summary": str(OUT_DIR / "family_summary.csv"),
                    "redundancy_context": str(OUT_DIR / "redundancy_context.csv"),
                },
                "validation_executed": False,
                "governance_modified": False,
                "thresholds_modified": False,
                "production_registration": False,
                "ml_integration": False,
                "candidate_promotion_or_demotion": False,
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )
    print(f"Wrote research-only refinement outputs for {len(registry)} candidates to {OUT_DIR}")
    print(RESEARCH_ONLY_GUARDRAIL)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
