from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd


RUN_ID = "alpha_family_diversification_ic_discovery_v1"
SOURCE_RUN_ID = "alpha_family_diversification_discovery_v1"
SOURCE_DIR = Path("artifacts/research") / SOURCE_RUN_ID
CANDIDATE_PANEL_DIR = SOURCE_DIR / "candidate_panels"
DISCOVERY_SUMMARY_DIR = SOURCE_DIR / "discovery_summary"
REDUNDANCY_DIR = SOURCE_DIR / "redundancy_screening"
OUT_DIR = SOURCE_DIR / "ic_discovery"
CLOSE_PATH = Path("data/processed/phase2/nb01_data_foundation/close_prices.parquet")
HORIZONS = (1, 5, 10, 20)

APPROVED_CANDIDATES = [
    "dispersion_expansion_transition_02",
    "dispersion_expansion_transition_04",
    "dispersion_compression_reversal_02",
    "dispersion_structure_anomalies_01",
    "dispersion_structure_anomalies_03",
    "rank_stability_after_drawdown_01",
    "rank_stability_after_drawdown_02",
    "rank_coherence_regime_transition_02",
]

RESEARCH_ONLY_GUARDRAIL = (
    "Research-only IC discovery pass for the approved 8-candidate subset. "
    "No validation, refinement, governance mutation, threshold change, production "
    "registration, ML, promotion, or demotion is performed."
)


def _ensure_dirs() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)


def _load_manifest_subset() -> pd.DataFrame:
    manifest = pd.read_csv(DISCOVERY_SUMMARY_DIR / "panel_manifest.csv")
    subset = manifest[manifest["candidate_id"].isin(APPROVED_CANDIDATES)].copy()
    missing = sorted(set(APPROVED_CANDIDATES) - set(subset["candidate_id"]))
    if missing:
        raise ValueError(f"Approved candidates missing from panel manifest: {missing}")
    if len(subset) != len(APPROVED_CANDIDATES):
        raise ValueError("Approved subset did not resolve to exactly 8 manifest rows.")
    subset["subset_order"] = subset["candidate_id"].map({cid: i for i, cid in enumerate(APPROVED_CANDIDATES)})
    return subset.sort_values("subset_order").drop(columns=["subset_order"])


def _load_candidate_panel(path: str) -> pd.DataFrame:
    panel_long = pd.read_parquet(path)
    required = {"date", "ticker", "signal_value"}
    missing = required - set(panel_long.columns)
    if missing:
        raise ValueError(f"Candidate panel {path} missing columns: {sorted(missing)}")
    panel = panel_long.pivot_table(index="date", columns="ticker", values="signal_value", aggfunc="last")
    panel.index = pd.to_datetime(panel.index)
    return panel.sort_index()


def _load_candidate_panels(subset: pd.DataFrame) -> dict[str, pd.DataFrame]:
    panels: dict[str, pd.DataFrame] = {}
    for rec in subset.to_dict(orient="records"):
        panels[rec["signal_name"]] = _load_candidate_panel(rec["panel_path"])
    return panels


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


def _score_panels(panels: dict[str, pd.DataFrame], close: pd.DataFrame, subset: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    metadata = subset.set_index("signal_name")[["candidate_id", "family", "theme", "horizon"]].to_dict("index")
    score_rows: list[dict[str, object]] = []
    daily_rows: list[dict[str, object]] = []
    for horizon in HORIZONS:
        fwd = _forward_returns(close, horizon)
        for signal_name, panel in panels.items():
            aligned_panel = panel.reindex(index=close.index, columns=close.columns)
            ic = _daily_ic(aligned_panel, fwd)
            valid_ic = ic.dropna()
            mean_ic = float(valid_ic.mean()) if len(valid_ic) else np.nan
            std_ic = float(valid_ic.std(ddof=0)) if len(valid_ic) > 1 else np.nan
            rec = metadata[signal_name]
            score_rows.append(
                {
                    "candidate_id": rec["candidate_id"],
                    "signal_name": signal_name,
                    "family": rec["family"],
                    "theme": rec["theme"],
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
                    "signal_name": signal_name,
                    "family": rec["family"],
                    "theme": rec["theme"],
                    "horizon": horizon,
                    "ic": value,
                }
                for date, value in valid_ic.items()
            )
    return pd.DataFrame(score_rows), pd.DataFrame(daily_rows)


def _load_redundancy_context(subset: pd.DataFrame) -> pd.DataFrame:
    stat = pd.read_csv(REDUNDANCY_DIR / "statistical_redundancy_screening.csv")
    signal_to_candidate = subset.set_index("signal_name")["candidate_id"].to_dict()
    approved_signals = set(signal_to_candidate)
    rows: list[dict[str, object]] = []
    for signal_name, group in stat[stat["signal_name"].isin(approved_signals)].groupby("signal_name"):
        group = group[group["comparison_signal"].isin(approved_signals)].copy()
        if group.empty:
            rows.append(
                {
                    "candidate_id": signal_to_candidate[signal_name],
                    "signal_name": signal_name,
                    "max_subset_abs_value_corr": np.nan,
                    "max_subset_abs_rank_corr": np.nan,
                    "max_subset_abs_corr": np.nan,
                    "top_redundancy_peer_signal": None,
                    "top_redundancy_peer_candidate_id": None,
                    "redundancy_context": "no approved-subset redundancy comparison",
                }
            )
            continue
        group["abs_value_corr"] = group["value_correlation"].abs()
        group["abs_rank_corr"] = group["rank_correlation"].abs()
        group["max_abs_corr"] = group[["abs_value_corr", "abs_rank_corr"]].max(axis=1)
        top = group.sort_values("max_abs_corr", ascending=False).iloc[0]
        max_corr = float(top["max_abs_corr"])
        if max_corr >= 0.60:
            context = "high approved-subset redundancy"
        elif max_corr >= 0.35:
            context = "moderate approved-subset redundancy"
        else:
            context = "low approved-subset redundancy"
        rows.append(
            {
                "candidate_id": signal_to_candidate[signal_name],
                "signal_name": signal_name,
                "max_subset_abs_value_corr": float(top["abs_value_corr"]),
                "max_subset_abs_rank_corr": float(top["abs_rank_corr"]),
                "max_subset_abs_corr": max_corr,
                "top_redundancy_peer_signal": top["comparison_signal"],
                "top_redundancy_peer_candidate_id": signal_to_candidate.get(top["comparison_signal"]),
                "redundancy_context": context,
            }
        )
    return pd.DataFrame(rows)


def _candidate_summary(scores: pd.DataFrame, redundancy: pd.DataFrame) -> pd.DataFrame:
    wide = scores.pivot_table(index=["candidate_id", "signal_name", "family", "theme", "declared_horizon"], columns="scored_horizon", values="mean_ic")
    wide = wide.rename(columns={h: f"h{h}_mean_ic" for h in HORIZONS}).reset_index()
    pos = scores.pivot_table(index=["candidate_id"], columns="scored_horizon", values="positive_ic_rate")
    pos = pos.rename(columns={h: f"h{h}_positive_ic_rate" for h in HORIZONS}).reset_index()
    best = scores.loc[scores.groupby("candidate_id")["abs_mean_ic"].idxmax()].copy()
    best = best.rename(
        columns={
            "scored_horizon": "best_horizon",
            "mean_ic": "best_mean_ic",
            "ic_ir": "best_ic_ir",
            "positive_ic_rate": "best_positive_ic_rate",
            "n_dates": "best_n_dates",
        }
    )
    primary = scores[scores["scored_horizon"].isin([10, 20])].copy()
    primary = primary.loc[primary.groupby("candidate_id")["abs_mean_ic"].idxmax()]
    primary = primary.rename(
        columns={
            "scored_horizon": "best_h10_h20_horizon",
            "mean_ic": "best_h10_h20_mean_ic",
            "ic_ir": "best_h10_h20_ic_ir",
            "positive_ic_rate": "best_h10_h20_positive_ic_rate",
            "n_dates": "best_h10_h20_n_dates",
        }
    )
    cols = [
        "candidate_id",
        "best_horizon",
        "best_mean_ic",
        "best_ic_ir",
        "best_positive_ic_rate",
        "best_n_dates",
    ]
    primary_cols = [
        "candidate_id",
        "best_h10_h20_horizon",
        "best_h10_h20_mean_ic",
        "best_h10_h20_ic_ir",
        "best_h10_h20_positive_ic_rate",
        "best_h10_h20_n_dates",
    ]
    out = wide.merge(pos, on="candidate_id", how="left")
    out = out.merge(best[cols], on="candidate_id", how="left")
    out = out.merge(primary[primary_cols], on="candidate_id", how="left")
    out = out.merge(redundancy, on=["candidate_id", "signal_name"], how="left")
    return out


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


def _horizon_summary(scores: pd.DataFrame) -> pd.DataFrame:
    return (
        scores.groupby("scored_horizon", as_index=False)
        .agg(
            candidate_count=("candidate_id", "nunique"),
            mean_ic=("mean_ic", "mean"),
            median_ic=("mean_ic", "median"),
            mean_abs_ic=("abs_mean_ic", "mean"),
            mean_ic_ir=("ic_ir", "mean"),
            mean_positive_ic_rate=("positive_ic_rate", "mean"),
        )
        .sort_values("scored_horizon")
    )


def main() -> int:
    _ensure_dirs()
    subset = _load_manifest_subset()
    close = pd.read_parquet(CLOSE_PATH)
    close.index = pd.to_datetime(close.index)
    panels = _load_candidate_panels(subset)
    scores, daily = _score_panels(panels, close, subset)
    redundancy = _load_redundancy_context(subset)
    candidate_summary = _candidate_summary(scores, redundancy)
    family_summary = _family_summary(scores)
    horizon_summary = _horizon_summary(scores)

    subset.to_csv(OUT_DIR / "approved_scoring_subset.csv", index=False)
    scores.to_csv(OUT_DIR / "candidate_horizon_ic_scores.csv", index=False)
    daily.to_csv(OUT_DIR / "daily_ic_by_candidate_horizon.csv", index=False)
    redundancy.to_csv(OUT_DIR / "approved_subset_redundancy_context.csv", index=False)
    candidate_summary.to_csv(OUT_DIR / "candidate_ic_summary.csv", index=False)
    family_summary.to_csv(OUT_DIR / "family_ic_summary.csv", index=False)
    horizon_summary.to_csv(OUT_DIR / "horizon_ic_summary.csv", index=False)
    (OUT_DIR / "manifest.json").write_text(
        json.dumps(
            {
                "run_id": RUN_ID,
                "source_run_id": SOURCE_RUN_ID,
                "research_only": True,
                "research_only_guardrail": RESEARCH_ONLY_GUARDRAIL,
                "approved_candidate_count": len(APPROVED_CANDIDATES),
                "approved_candidate_ids": APPROVED_CANDIDATES,
                "horizons": list(HORIZONS),
                "outputs": {
                    "approved_scoring_subset": str(OUT_DIR / "approved_scoring_subset.csv"),
                    "candidate_horizon_ic_scores": str(OUT_DIR / "candidate_horizon_ic_scores.csv"),
                    "daily_ic_by_candidate_horizon": str(OUT_DIR / "daily_ic_by_candidate_horizon.csv"),
                    "approved_subset_redundancy_context": str(OUT_DIR / "approved_subset_redundancy_context.csv"),
                    "candidate_ic_summary": str(OUT_DIR / "candidate_ic_summary.csv"),
                    "family_ic_summary": str(OUT_DIR / "family_ic_summary.csv"),
                    "horizon_ic_summary": str(OUT_DIR / "horizon_ic_summary.csv"),
                },
                "validation_executed": False,
                "refinement_executed": False,
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
    print(f"Wrote research-only IC discovery outputs for {len(APPROVED_CANDIDATES)} candidates to {OUT_DIR}")
    print(RESEARCH_ONLY_GUARDRAIL)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
