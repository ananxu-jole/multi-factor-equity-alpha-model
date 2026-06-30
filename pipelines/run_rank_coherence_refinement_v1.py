from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd


RUN_ID = "rank_coherence_refinement_v1"
SOURCE_RUN_ID = "rank_coherence_family_discovery_v1"
SOURCE_DIR = Path("artifacts/research") / SOURCE_RUN_ID
SOURCE_PANEL_DIR = Path("artifacts/panels/signals")
SOURCE_CANDIDATE_PANEL_DIR = SOURCE_DIR / "candidate_panels"
SOURCE_IC_DIR = SOURCE_DIR / "ic_discovery"
OUT_DIR = Path("artifacts/research") / RUN_ID
CANDIDATE_PANEL_DIR = OUT_DIR / "candidate_panels"
CLOSE_PATH = Path("data/processed/phase2/nb01_data_foundation/close_prices.parquet")

PANEL_GENERATION_LOOKBACK_ROWS = 504
REDUNDANCY_LOOKBACK_ROWS = 252
HORIZONS = (1, 5, 10, 20)
MAX_TOTAL_CANDIDATES = 6

SOURCE_PANEL_NAMES = [
    "relative_return_rank_20",
    "relative_return_zscore_60",
    "percentile_rank_stability_20",
    "trend_consistency_20_60",
    "trend_consistency_20_60_persistent",
    "smooth_trend_persistence_60",
    "residual_return_vs_universe_20",
    "expanded_reversal_5d",
    "close_position_reversal_5",
    "failed_breakout_reversal_20",
    "failed_breakout_reversal_20_low_breadth",
    "percentile_rank_stability_20_downtrend",
]

APPROVED_PARENT_CANDIDATES = {
    "rank_coherence_regime_independent_02",
    "rank_coherence_churn_avoidance_02",
}

APPROVED_ANCHOR_SIGNALS = {
    "nonhostile_transition_rank_coherence_20",
    "relative_rank_turnover_resilience_20",
}

STRESS_REPAIR_PROXY_SIGNALS = [
    "failed_breakout_reversal_20",
    "failed_breakout_reversal_20_low_breadth",
    "percentile_rank_stability_20_downtrend",
]

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
]

RESEARCH_ONLY_GUARDRAIL = (
    "Research-only rank-coherence refinement execution for two approved candidates. "
    "No validation, governance mutation, threshold change, production registration, "
    "ML integration, or candidate promotion/demotion is performed."
)

REFINEMENT_CANDIDATES = [
    {
        "candidate_id": "rank_coherence_regime_independent_02_anchor",
        "parent_candidate_id": "rank_coherence_regime_independent_02",
        "signal_name": "nonhostile_transition_rank_coherence_20",
        "family": "rank_coherence",
        "theme": "Regime-Independent Rank Coherence",
        "horizon": "h10-h20",
        "variant_role": "original_anchor",
        "diagnostic_purpose": "Retain original non-hostile transition rank-coherence representative.",
    },
    {
        "candidate_id": "rank_coherence_regime_independent_02_strict",
        "parent_candidate_id": "rank_coherence_regime_independent_02",
        "signal_name": "nonhostile_transition_rank_coherence_strict_20",
        "family": "rank_coherence",
        "theme": "Regime-Independent Rank Coherence",
        "horizon": "h10-h20",
        "variant_role": "stricter_nonhostile_transition_definition",
        "diagnostic_purpose": "Require stronger ordinary-state rank agreement without adding hostile or stress-repair inputs.",
    },
    {
        "candidate_id": "rank_coherence_regime_independent_02_smoothed",
        "parent_candidate_id": "rank_coherence_regime_independent_02",
        "signal_name": "nonhostile_transition_rank_coherence_smoothed_20",
        "family": "rank_coherence",
        "theme": "Regime-Independent Rank Coherence",
        "horizon": "h10-h20",
        "variant_role": "light_rank_agreement_smoothing",
        "diagnostic_purpose": "Apply light smoothing to test sensitivity to daily rank noise.",
    },
    {
        "candidate_id": "rank_coherence_churn_avoidance_02_anchor",
        "parent_candidate_id": "rank_coherence_churn_avoidance_02",
        "signal_name": "relative_rank_turnover_resilience_20",
        "family": "rank_coherence",
        "theme": "Rank Churn Avoidance",
        "horizon": "h10-h20",
        "variant_role": "original_anchor",
        "diagnostic_purpose": "Retain original rank-turnover resilience representative.",
    },
    {
        "candidate_id": "rank_coherence_churn_avoidance_02_penalized",
        "parent_candidate_id": "rank_coherence_churn_avoidance_02",
        "signal_name": "relative_rank_turnover_resilience_penalized_20",
        "family": "rank_coherence",
        "theme": "Rank Churn Avoidance",
        "horizon": "h10-h20",
        "variant_role": "conservative_churn_penalty",
        "diagnostic_purpose": "Increase churn penalty modestly to test turnover-resilience robustness.",
    },
    {
        "candidate_id": "rank_coherence_churn_avoidance_02_overlap_adjusted",
        "parent_candidate_id": "rank_coherence_churn_avoidance_02",
        "signal_name": "relative_rank_turnover_resilience_overlap_adjusted_20",
        "family": "rank_coherence",
        "theme": "Rank Churn Avoidance",
        "horizon": "h10-h20",
        "variant_role": "regime_independent_overlap_diagnostic",
        "diagnostic_purpose": "Reduce direct overlap with non-hostile transition coherence using fixed pre-declared residualization.",
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
        panels[name] = panel.sort_index().tail(PANEL_GENERATION_LOOKBACK_ROWS).astype(float)
    return _align_sources(panels)


def _align_sources(panels: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
    common_index = None
    common_columns = None
    for panel in panels.values():
        common_index = panel.index if common_index is None else common_index.intersection(panel.index)
        common_columns = panel.columns if common_columns is None else common_columns.intersection(panel.columns)
    if common_index is None or common_columns is None or len(common_index) == 0 or len(common_columns) == 0:
        raise ValueError("Rank-coherence refinement source panels do not share a usable date/ticker intersection.")
    return {
        name: panel.reindex(index=common_index, columns=common_columns).astype(float)
        for name, panel in panels.items()
    }


def _refinement_signal_panels(source: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
    rr = _rank_cs(source["relative_return_rank_20"])
    stability = _rank_cs(source["percentile_rank_stability_20"])
    trend = _rank_cs(source["trend_consistency_20_60"])
    trend_persistent = _rank_cs(source["trend_consistency_20_60_persistent"])
    smooth = _rank_cs(source["smooth_trend_persistence_60"])

    rank_churn = rr.diff().abs().rolling(20, min_periods=10).mean()
    universe_churn = rank_churn.mean(axis=1)
    relative_churn_resilience = rank_churn.rsub(universe_churn, axis=0)
    cross_window_disagreement = rr.sub(trend.add(smooth, fill_value=0.0).div(2.0), fill_value=0.0).abs()

    transition_coherence = (
        stability.add(trend.diff(20), fill_value=0.0)
        .add(smooth.diff(20), fill_value=0.0)
        .add(trend_persistent, fill_value=0.0)
        .sub(rr.diff(5).abs(), fill_value=0.0)
    )
    ordinary_rank_agreement = rr.add(trend, fill_value=0.0).add(smooth, fill_value=0.0).sub(
        cross_window_disagreement,
        fill_value=0.0,
    )
    strict_transition = transition_coherence.add(stability.clip(lower=0.0), fill_value=0.0).add(
        ordinary_rank_agreement.clip(lower=0.0),
        fill_value=0.0,
    )
    smoothed_transition = transition_coherence.rolling(5, min_periods=3).mean()

    churn_anchor = relative_churn_resilience.add(stability, fill_value=0.0).add(smooth, fill_value=0.0)
    churn_penalized = relative_churn_resilience.mul(1.25).add(stability, fill_value=0.0).add(smooth, fill_value=0.0)
    churn_overlap_adjusted = churn_anchor.sub(_rank_cs(transition_coherence).mul(0.25), fill_value=0.0)

    return {
        "nonhostile_transition_rank_coherence_20": _clean_panel(_rank_cs(transition_coherence)),
        "nonhostile_transition_rank_coherence_strict_20": _clean_panel(_rank_cs(strict_transition)),
        "nonhostile_transition_rank_coherence_smoothed_20": _clean_panel(_rank_cs(smoothed_transition)),
        "relative_rank_turnover_resilience_20": _clean_panel(_rank_cs(churn_anchor)),
        "relative_rank_turnover_resilience_penalized_20": _clean_panel(_rank_cs(churn_penalized)),
        "relative_rank_turnover_resilience_overlap_adjusted_20": _clean_panel(_rank_cs(churn_overlap_adjusted)),
    }


def _validate_registry(registry: pd.DataFrame) -> None:
    if len(registry) != MAX_TOTAL_CANDIDATES:
        raise ValueError(f"Rank-coherence refinement must contain exactly {MAX_TOTAL_CANDIDATES} candidates including anchors.")
    if len(registry) > MAX_TOTAL_CANDIDATES:
        raise ValueError(f"Rank-coherence refinement exceeds approved cap of {MAX_TOTAL_CANDIDATES}.")
    if set(registry["parent_candidate_id"]) != APPROVED_PARENT_CANDIDATES:
        raise ValueError("Rank-coherence refinement includes an unapproved parent candidate.")
    anchors = set(registry.loc[registry["variant_role"] == "original_anchor", "signal_name"])
    if anchors != APPROVED_ANCHOR_SIGNALS:
        raise ValueError("Rank-coherence refinement anchors do not match approved discovery candidates.")
    if set(registry["family"]) != {"rank_coherence"}:
        raise ValueError("Rank-coherence refinement may not expand into another family.")
    if set(registry["theme"]) != {"Regime-Independent Rank Coherence", "Rank Churn Avoidance"}:
        raise ValueError("Rank-coherence refinement may not add new themes.")


def _panel_to_long(panel: pd.DataFrame, rec: dict[str, object]) -> pd.DataFrame:
    long_panel = panel.stack(future_stack=True).dropna().rename("signal_value").reset_index()
    long_panel.columns = ["date", "ticker", "signal_value"]
    long_panel["candidate_id"] = rec["candidate_id"]
    long_panel["parent_candidate_id"] = rec["parent_candidate_id"]
    long_panel["signal_name"] = rec["signal_name"]
    long_panel["family"] = rec["family"]
    long_panel["theme"] = rec["theme"]
    long_panel["horizon"] = rec["horizon"]
    return long_panel[
        ["date", "ticker", "candidate_id", "parent_candidate_id", "signal_name", "signal_value", "family", "theme", "horizon"]
    ]


def _write_candidate_panels(registry: pd.DataFrame, panels: dict[str, pd.DataFrame]) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for rec in registry.to_dict(orient="records"):
        signal_name = rec["signal_name"]
        if signal_name not in panels:
            raise KeyError(f"No rank-coherence refinement panel registered for {signal_name}")
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
                    "refinement_only": True,
                    "variant_role": rec["variant_role"],
                    "diagnostic_purpose": rec["diagnostic_purpose"],
                    "source_panel_dir": str(SOURCE_PANEL_DIR),
                    "source_panel_names": SOURCE_PANEL_NAMES,
                    "lookback_rows": PANEL_GENERATION_LOOKBACK_ROWS,
                    "panel_format": "long",
                    "date_min": str(long_panel["date"].min().date()) if not long_panel.empty else None,
                    "date_max": str(long_panel["date"].max().date()) if not long_panel.empty else None,
                    "row_count": int(len(long_panel)),
                    "guardrails": {
                        "validation_executed": False,
                        "governance_modified": False,
                        "thresholds_modified": False,
                        "production_registration": False,
                        "ml_integration": False,
                        "candidate_promotion_or_demotion": False,
                    },
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


def _long_to_wide(path: str | Path) -> pd.DataFrame:
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
                    "theme": rec["theme"],
                    "horizon": horizon,
                    "ic": value,
                }
                for date, value in valid_ic.items()
            )
    return pd.DataFrame(score_rows), pd.DataFrame(daily_rows)


def _coverage_diagnostics(manifest: pd.DataFrame, close: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for rec in manifest.to_dict(orient="records"):
        panel = _long_to_wide(rec["panel_path"])
        aligned = panel.reindex(index=close.index, columns=close.columns)
        active_by_date = aligned.notna().sum(axis=1)
        active_dates = active_by_date[active_by_date > 0]
        rows.append(
            {
                "candidate_id": rec["candidate_id"],
                "parent_candidate_id": rec["parent_candidate_id"],
                "signal_name": rec["signal_name"],
                "family": rec["family"],
                "theme": rec["theme"],
                "declared_horizon": rec["horizon"],
                "active_date_count": int(len(active_dates)),
                "active_date_ratio": float(len(active_dates) / len(aligned.index)) if len(aligned.index) else np.nan,
                "mean_active_tickers": float(active_dates.mean()) if len(active_dates) else np.nan,
                "min_active_tickers": int(active_dates.min()) if len(active_dates) else 0,
                "max_active_tickers": int(active_dates.max()) if len(active_dates) else 0,
            }
        )
    return pd.DataFrame(rows)


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


def _load_reference_panels(source: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
    refs: dict[str, pd.DataFrame] = {}
    for path in SOURCE_CANDIDATE_PANEL_DIR.glob("*.parquet"):
        refs[f"rank_discovery::{path.stem}"] = _long_to_wide(path)

    persistence_dir = Path("artifacts/research/alpha_family_diversification_refinement_v1/candidate_panels")
    for signal in PERSISTENCE_REFERENCE_SIGNALS:
        path = persistence_dir / f"{signal}.parquet"
        if path.exists():
            refs[f"persistence::{signal}"] = _long_to_wide(path)

    dispersion_dir = Path("artifacts/research/alpha_family_diversification_refinement_v1/candidate_panels")
    for signal in DISPERSION_REFERENCE_SIGNALS:
        path = dispersion_dir / f"{signal}.parquet"
        if path.exists():
            refs[f"dispersion::{signal}"] = _long_to_wide(path)

    for signal in STRESS_REPAIR_PROXY_SIGNALS:
        if signal in source:
            refs[f"stress_proxy::{signal}"] = source[signal]
    return refs


def _redundancy_context(manifest: pd.DataFrame, source: dict[str, pd.DataFrame]) -> pd.DataFrame:
    refinement_panels = {rec["signal_name"]: _long_to_wide(rec["panel_path"]) for rec in manifest.to_dict(orient="records")}
    comparison_panels = {f"refinement::{k}": v for k, v in refinement_panels.items()}
    comparison_panels.update(_load_reference_panels(source))

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
                    "parent_candidate_id": rec["parent_candidate_id"],
                    "signal_name": signal_name,
                    "family": rec["family"],
                    "theme": rec["theme"],
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


def _discovery_anchor_metrics() -> pd.DataFrame:
    path = SOURCE_IC_DIR / "candidate_horizon_ic_scores.csv"
    if not path.exists():
        return pd.DataFrame()
    scores = pd.read_csv(path)
    return scores[scores["candidate_id"].isin(APPROVED_PARENT_CANDIDATES)].copy()


def _candidate_summary(scores: pd.DataFrame, redundancy: pd.DataFrame, coverage: pd.DataFrame) -> pd.DataFrame:
    idx_cols = ["candidate_id", "parent_candidate_id", "signal_name", "family", "theme", "variant_role", "declared_horizon"]
    wide = scores.pivot_table(index=idx_cols, columns="scored_horizon", values="mean_ic")
    wide = wide.rename(columns={h: f"h{h}_mean_ic" for h in HORIZONS}).reset_index()
    pos = scores.pivot_table(index=["candidate_id"], columns="scored_horizon", values="positive_ic_rate")
    pos = pos.rename(columns={h: f"h{h}_positive_ic_rate" for h in HORIZONS}).reset_index()
    ir = scores.pivot_table(index=["candidate_id"], columns="scored_horizon", values="ic_ir")
    ir = ir.rename(columns={h: f"h{h}_ic_ir" for h in HORIZONS}).reset_index()
    best = scores.loc[scores.groupby("candidate_id")["abs_mean_ic"].idxmax()].copy()
    primary = scores[scores["scored_horizon"].isin([10, 20])].copy()
    primary = primary.loc[primary.groupby("candidate_id")["abs_mean_ic"].idxmax()]

    red_rows: list[dict[str, object]] = []
    for candidate_id, group in redundancy.groupby("candidate_id"):
        row = {"candidate_id": candidate_id}
        for scope in ["refinement", "rank_discovery", "persistence", "dispersion", "stress_proxy"]:
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
    out = out.merge(ir, on="candidate_id", how="left")
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
    out = out.merge(red, on="candidate_id", how="left")
    out = out.merge(
        coverage[
            [
                "candidate_id",
                "active_date_count",
                "active_date_ratio",
                "mean_active_tickers",
                "min_active_tickers",
                "max_active_tickers",
            ]
        ],
        on="candidate_id",
        how="left",
    )
    return out


def _refinement_deltas(scores: pd.DataFrame) -> pd.DataFrame:
    discovery = _discovery_anchor_metrics()
    if discovery.empty:
        return pd.DataFrame()
    discovery = discovery.rename(
        columns={
            "candidate_id": "parent_candidate_id",
            "mean_ic": "discovery_anchor_mean_ic",
            "ic_ir": "discovery_anchor_ic_ir",
            "positive_ic_rate": "discovery_anchor_positive_ic_rate",
        }
    )[
        [
            "parent_candidate_id",
            "scored_horizon",
            "discovery_anchor_mean_ic",
            "discovery_anchor_ic_ir",
            "discovery_anchor_positive_ic_rate",
        ]
    ]
    merged = scores.merge(discovery, on=["parent_candidate_id", "scored_horizon"], how="left")
    merged["mean_ic_delta_vs_discovery_anchor"] = merged["mean_ic"] - merged["discovery_anchor_mean_ic"]
    merged["ic_ir_delta_vs_discovery_anchor"] = merged["ic_ir"] - merged["discovery_anchor_ic_ir"]
    merged["positive_ic_rate_delta_vs_discovery_anchor"] = (
        merged["positive_ic_rate"] - merged["discovery_anchor_positive_ic_rate"]
    )
    return merged[
        [
            "candidate_id",
            "parent_candidate_id",
            "signal_name",
            "variant_role",
            "scored_horizon",
            "mean_ic",
            "discovery_anchor_mean_ic",
            "mean_ic_delta_vs_discovery_anchor",
            "ic_ir",
            "discovery_anchor_ic_ir",
            "ic_ir_delta_vs_discovery_anchor",
            "positive_ic_rate",
            "discovery_anchor_positive_ic_rate",
            "positive_ic_rate_delta_vs_discovery_anchor",
        ]
    ]


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


def _write_guardrail_review() -> None:
    pd.DataFrame(
        [
            ("validation_executed", False),
            ("governance_modified", False),
            ("thresholds_modified", False),
            ("production_registration", False),
            ("ml_integration", False),
            ("candidate_promotion_or_demotion", False),
            ("new_family_expansion", False),
            ("new_theme_expansion", False),
        ],
        columns=["guardrail", "executed_or_modified"],
    ).to_csv(OUT_DIR / "guardrail_review.csv", index=False)


def main() -> int:
    _ensure_dirs()
    registry = pd.DataFrame(REFINEMENT_CANDIDATES)
    registry["run_id"] = RUN_ID
    _validate_registry(registry)

    source = _load_source_panels()
    panels = _refinement_signal_panels(source)
    manifest = _write_candidate_panels(registry, panels)

    close = pd.read_parquet(CLOSE_PATH)
    close.index = pd.to_datetime(close.index)
    close = close.sort_index()
    scores, daily = _score_panels(manifest, close)
    coverage = _coverage_diagnostics(manifest, close)
    redundancy = _redundancy_context(manifest, source)
    candidate_summary = _candidate_summary(scores, redundancy, coverage)
    deltas = _refinement_deltas(scores)
    family_summary = _family_summary(scores)

    registry.to_csv(OUT_DIR / "refinement_candidate_inventory.csv", index=False)
    manifest.to_csv(OUT_DIR / "panel_manifest.csv", index=False)
    scores.to_csv(OUT_DIR / "candidate_horizon_scores.csv", index=False)
    daily.to_csv(OUT_DIR / "daily_ic_by_candidate_horizon.csv", index=False)
    candidate_summary.to_csv(OUT_DIR / "candidate_refinement_summary.csv", index=False)
    family_summary.to_csv(OUT_DIR / "family_refinement_summary.csv", index=False)
    redundancy.to_csv(OUT_DIR / "redundancy_context.csv", index=False)
    coverage.to_csv(OUT_DIR / "coverage_diagnostics.csv", index=False)
    deltas.to_csv(OUT_DIR / "refinement_deltas_vs_discovery.csv", index=False)
    _write_guardrail_review()
    (OUT_DIR / "manifest.json").write_text(
        json.dumps(
            {
                "run_id": RUN_ID,
                "source_run_id": SOURCE_RUN_ID,
                "research_only": True,
                "research_only_guardrail": RESEARCH_ONLY_GUARDRAIL,
                "approved_parent_candidate_ids": sorted(APPROVED_PARENT_CANDIDATES),
                "candidate_count": int(len(registry)),
                "max_total_candidates": MAX_TOTAL_CANDIDATES,
                "anchor_count": int((registry["variant_role"] == "original_anchor").sum()),
                "new_variant_count": int((registry["variant_role"] != "original_anchor").sum()),
                "horizons": list(HORIZONS),
                "outputs": {
                    "refinement_candidate_inventory": str(OUT_DIR / "refinement_candidate_inventory.csv"),
                    "panel_manifest": str(OUT_DIR / "panel_manifest.csv"),
                    "candidate_horizon_scores": str(OUT_DIR / "candidate_horizon_scores.csv"),
                    "daily_ic_by_candidate_horizon": str(OUT_DIR / "daily_ic_by_candidate_horizon.csv"),
                    "candidate_refinement_summary": str(OUT_DIR / "candidate_refinement_summary.csv"),
                    "family_refinement_summary": str(OUT_DIR / "family_refinement_summary.csv"),
                    "redundancy_context": str(OUT_DIR / "redundancy_context.csv"),
                    "coverage_diagnostics": str(OUT_DIR / "coverage_diagnostics.csv"),
                    "refinement_deltas_vs_discovery": str(OUT_DIR / "refinement_deltas_vs_discovery.csv"),
                    "guardrail_review": str(OUT_DIR / "guardrail_review.csv"),
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
    print(f"Wrote research-only rank-coherence refinement outputs for {len(registry)} candidates to {OUT_DIR}")
    print(RESEARCH_ONLY_GUARDRAIL)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
