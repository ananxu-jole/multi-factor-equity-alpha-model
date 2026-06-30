from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from pipelines.ohlcv_non_hostile_transition_leadership_rotation_candidate_implementation import (
    APPROVED_CANDIDATE_IDS,
    REQUIRED_PANEL_COLUMNS,
)


RUN_ID = "ohlcv_non_hostile_transition_and_leadership_rotation_ic_discovery_v1"
SOURCE_RUN_ID = "ohlcv_non_hostile_transition_and_leadership_rotation_discovery_v1"
SOURCE_DIR = Path("artifacts/research") / SOURCE_RUN_ID
CANDIDATE_PANEL_GENERATION_DIR = SOURCE_DIR / "candidate_panel_generation"
OUT_DIR = Path("artifacts/research") / RUN_ID
CLOSE_PATH = Path("data/processed/phase2/nb01_data_foundation/close_prices.parquet")
HORIZONS = (1, 5, 10, 20)
ROLLING_WINDOWS = (63, 126, 252)
MIN_DAILY_OBSERVATIONS = 25

RESEARCH_ONLY_GUARDRAIL = (
    "Research-only IC discovery pass using approved OHLCV non-hostile transition and "
    "leadership rotation candidate panels. No refinement, validation, governance mutation, "
    "threshold change, production registration, ML, formula modification, or panel modification is performed."
)


def _ensure_out_dir(out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)


def _load_panel_manifest(source_dir: Path = SOURCE_DIR) -> pd.DataFrame:
    manifest_path = source_dir / "candidate_panel_generation" / "panel_manifest.csv"
    manifest = pd.read_csv(manifest_path)
    ids = list(manifest["candidate_id"].astype(str))
    if ids != APPROVED_CANDIDATE_IDS:
        raise ValueError("panel manifest candidate IDs do not match approved registry order")
    if "nhlr_06" in ids:
        raise ValueError("excluded candidate nhlr_06 is present in panel manifest")
    required = {"candidate_id", "panel_path", "horizon", "formula_name", "formula_version"}
    missing = required - set(manifest.columns)
    if missing:
        raise ValueError("panel manifest missing required columns: " + ", ".join(sorted(missing)))
    return manifest


def _load_candidate_panel(path: str | Path) -> pd.DataFrame:
    panel_long = pd.read_parquet(path)
    missing = set(REQUIRED_PANEL_COLUMNS) - set(panel_long.columns)
    if missing:
        raise ValueError(f"candidate panel {path} missing columns: {sorted(missing)}")
    if panel_long[["date", "ticker", "candidate_id"]].duplicated().any():
        raise ValueError(f"candidate panel {path} contains duplicate date/ticker/candidate rows")
    if not panel_long["warmup_complete"].astype(bool).all():
        raise ValueError(f"candidate panel {path} contains warmup-incomplete rows")
    panel = panel_long.pivot(index="date", columns="ticker", values="signal_value")
    panel.index = pd.to_datetime(panel.index)
    return panel.sort_index()


def _load_candidate_panels(manifest: pd.DataFrame) -> dict[str, pd.DataFrame]:
    return {
        str(row["candidate_id"]): _load_candidate_panel(row["panel_path"])
        for row in manifest.to_dict(orient="records")
    }


def _load_close(close_path: Path = CLOSE_PATH) -> pd.DataFrame:
    close = pd.read_parquet(close_path)
    close.index = pd.to_datetime(close.index)
    return close.sort_index()


def _forward_returns(close: pd.DataFrame, horizon: int) -> pd.DataFrame:
    return close.shift(-horizon) / close - 1.0


def _daily_ic_frame(signal: pd.DataFrame, fwd: pd.DataFrame, horizon: int) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for date in signal.index.intersection(fwd.index):
        s = signal.loc[date]
        r = fwd.loc[date]
        signal_count = int(s.notna().sum())
        target_count = int(r.notna().sum())
        valid = s.notna() & r.notna()
        observation_count = int(valid.sum())
        if observation_count < MIN_DAILY_OBSERVATIONS:
            ic = np.nan
        else:
            ic = float(s[valid].rank().corr(r[valid].rank()))
        rows.append(
            {
                "date": date,
                "horizon": f"h{horizon}",
                "ic": ic,
                "observation_count": observation_count,
                "signal_count": signal_count,
                "target_count": target_count,
                "coverage_ratio": observation_count / signal_count if signal_count else np.nan,
            }
        )
    return pd.DataFrame(rows)


def _metadata_by_candidate(manifest: pd.DataFrame) -> dict[str, dict[str, object]]:
    meta: dict[str, dict[str, object]] = {}
    for row in manifest.to_dict(orient="records"):
        panel = pd.read_parquet(row["panel_path"], columns=["candidate_id", "family", "theme", "working_name"])
        first = panel.iloc[0]
        meta[str(row["candidate_id"])] = {
            "candidate_id": str(row["candidate_id"]),
            "family": str(first["family"]),
            "theme": str(first["theme"]),
            "working_name": str(first["working_name"]),
            "declared_horizon": str(row["horizon"]),
            "formula_name": str(row["formula_name"]),
            "formula_version": str(row["formula_version"]),
        }
    return meta


def score_candidate_panels(
    panels: dict[str, pd.DataFrame],
    close: pd.DataFrame,
    manifest: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    metadata = _metadata_by_candidate(manifest)
    daily_rows: list[pd.DataFrame] = []
    summary_rows: list[dict[str, object]] = []
    for horizon in HORIZONS:
        fwd = _forward_returns(close, horizon)
        for candidate_id in APPROVED_CANDIDATE_IDS:
            panel = panels[candidate_id].reindex(index=close.index, columns=close.columns)
            daily = _daily_ic_frame(panel, fwd, horizon)
            meta = metadata[candidate_id]
            for key, value in meta.items():
                daily[key] = value
            daily = daily[
                [
                    "date",
                    "candidate_id",
                    "working_name",
                    "family",
                    "theme",
                    "declared_horizon",
                    "formula_name",
                    "formula_version",
                    "horizon",
                    "ic",
                    "observation_count",
                    "signal_count",
                    "target_count",
                    "coverage_ratio",
                ]
            ]
            valid_ic = daily["ic"].dropna()
            mean_ic = float(valid_ic.mean()) if len(valid_ic) else np.nan
            median_ic = float(valid_ic.median()) if len(valid_ic) else np.nan
            ic_std = float(valid_ic.std(ddof=0)) if len(valid_ic) > 1 else np.nan
            summary_rows.append(
                {
                    "candidate_id": candidate_id,
                    "working_name": meta["working_name"],
                    "family": meta["family"],
                    "theme": meta["theme"],
                    "declared_horizon": meta["declared_horizon"],
                    "formula_name": meta["formula_name"],
                    "formula_version": meta["formula_version"],
                    "horizon": f"h{horizon}",
                    "mean_ic": mean_ic,
                    "median_ic": median_ic,
                    "ic_std": ic_std,
                    "ic_ir": mean_ic / ic_std if pd.notna(ic_std) and ic_std > 0 else np.nan,
                    "positive_ic_rate": float((valid_ic > 0).mean()) if len(valid_ic) else np.nan,
                    "coverage_ratio": float(daily["coverage_ratio"].mean()) if len(daily) else np.nan,
                    "observation_count": int(daily["observation_count"].sum()),
                    "scored_date_count": int(len(valid_ic)),
                    "daily_row_count": int(len(daily)),
                }
            )
            daily_rows.append(daily)
    return pd.concat(daily_rows, ignore_index=True), pd.DataFrame(summary_rows)


def rolling_ic_diagnostics(daily_ic: pd.DataFrame) -> pd.DataFrame:
    rows: list[pd.DataFrame] = []
    for (candidate_id, horizon), group in daily_ic.sort_values("date").groupby(["candidate_id", "horizon"]):
        out = group[["date", "candidate_id", "horizon"]].copy()
        series = group["ic"]
        for window in ROLLING_WINDOWS:
            rolling_mean = series.rolling(window, min_periods=max(20, window // 3)).mean()
            rolling_std = series.rolling(window, min_periods=max(20, window // 3)).std(ddof=0)
            out[f"rolling_{window}_mean_ic"] = rolling_mean
            out[f"rolling_{window}_ic_ir"] = rolling_mean / rolling_std.replace(0, np.nan)
            out[f"rolling_{window}_positive_ic_rate"] = (
                series.gt(0).rolling(window, min_periods=max(20, window // 3)).mean()
            )
        rows.append(out)
    return pd.concat(rows, ignore_index=True)


def horizon_summary(candidate_horizon_summary: pd.DataFrame) -> pd.DataFrame:
    out = (
        candidate_horizon_summary.groupby("horizon", as_index=False)
        .agg(
            candidate_count=("candidate_id", "nunique"),
            mean_ic=("mean_ic", "mean"),
            median_ic=("mean_ic", "median"),
            mean_abs_ic=("mean_ic", lambda values: values.abs().mean()),
            mean_ic_ir=("ic_ir", "mean"),
            mean_positive_ic_rate=("positive_ic_rate", "mean"),
            mean_coverage_ratio=("coverage_ratio", "mean"),
            total_observation_count=("observation_count", "sum"),
        )
    )
    out["horizon_order"] = out["horizon"].map({f"h{horizon}": idx for idx, horizon in enumerate(HORIZONS)})
    return out.sort_values("horizon_order").drop(columns="horizon_order")


def family_summary(candidate_horizon_summary: pd.DataFrame) -> pd.DataFrame:
    out = (
        candidate_horizon_summary.groupby(["family", "horizon"], as_index=False)
        .agg(
            candidate_count=("candidate_id", "nunique"),
            mean_ic=("mean_ic", "mean"),
            median_ic=("mean_ic", "median"),
            mean_abs_ic=("mean_ic", lambda values: values.abs().mean()),
            mean_ic_ir=("ic_ir", "mean"),
            mean_positive_ic_rate=("positive_ic_rate", "mean"),
            mean_coverage_ratio=("coverage_ratio", "mean"),
            total_observation_count=("observation_count", "sum"),
        )
    )
    out["horizon_order"] = out["horizon"].map({f"h{horizon}": idx for idx, horizon in enumerate(HORIZONS)})
    return out.sort_values(["family", "horizon_order"]).drop(columns="horizon_order")


def classify_candidate(best_primary_mean_ic: float, best_primary_ic_ir: float, best_primary_positive_rate: float, coverage: float) -> str:
    if (
        pd.notna(best_primary_mean_ic)
        and best_primary_mean_ic >= 0.005
        and pd.notna(best_primary_ic_ir)
        and best_primary_ic_ir >= 0.030
        and pd.notna(best_primary_positive_rate)
        and best_primary_positive_rate >= 0.530
        and pd.notna(coverage)
        and coverage >= 0.400
    ):
        return "ADVANCE_TO_REFINEMENT"
    if (
        pd.notna(best_primary_mean_ic)
        and best_primary_mean_ic > 0
        and pd.notna(best_primary_positive_rate)
        and best_primary_positive_rate >= 0.500
        and pd.notna(coverage)
        and coverage >= 0.350
    ):
        return "WATCH"
    return "REJECT"


def candidate_rankings(candidate_horizon_summary: pd.DataFrame) -> pd.DataFrame:
    primary = candidate_horizon_summary[candidate_horizon_summary["horizon"].isin(["h10", "h20"])].copy()
    primary = primary.sort_values(["candidate_id", "mean_ic"], ascending=[True, False])
    best_primary = primary.groupby("candidate_id", as_index=False).head(1)
    any_best = candidate_horizon_summary.sort_values(["candidate_id", "mean_ic"], ascending=[True, False])
    any_best = any_best.groupby("candidate_id", as_index=False).head(1)
    rows: list[dict[str, object]] = []
    for row in best_primary.to_dict(orient="records"):
        candidate_id = str(row["candidate_id"])
        best_any = any_best[any_best["candidate_id"].eq(candidate_id)].iloc[0]
        classification = classify_candidate(
            float(row["mean_ic"]),
            float(row["ic_ir"]),
            float(row["positive_ic_rate"]),
            float(row["coverage_ratio"]),
        )
        rows.append(
            {
                "candidate_id": candidate_id,
                "working_name": row["working_name"],
                "family": row["family"],
                "theme": row["theme"],
                "declared_horizon": row["declared_horizon"],
                "formula_name": row["formula_name"],
                "best_primary_horizon": row["horizon"],
                "best_primary_mean_ic": row["mean_ic"],
                "best_primary_ic_ir": row["ic_ir"],
                "best_primary_positive_ic_rate": row["positive_ic_rate"],
                "best_primary_coverage_ratio": row["coverage_ratio"],
                "best_primary_observation_count": row["observation_count"],
                "best_any_horizon": best_any["horizon"],
                "best_any_mean_ic": best_any["mean_ic"],
                "best_any_ic_ir": best_any["ic_ir"],
                "best_any_positive_ic_rate": best_any["positive_ic_rate"],
                "classification": classification,
            }
        )
    ranking = pd.DataFrame(rows)
    ranking["rank"] = ranking["best_primary_mean_ic"].rank(method="first", ascending=False).astype(int)
    return ranking.sort_values("rank")


def run_ic_discovery(
    source_dir: Path = SOURCE_DIR,
    close_path: Path = CLOSE_PATH,
    out_dir: Path = OUT_DIR,
) -> dict[str, pd.DataFrame]:
    _ensure_out_dir(out_dir)
    manifest = _load_panel_manifest(source_dir)
    panels = _load_candidate_panels(manifest)
    close = _load_close(close_path)
    daily_ic, candidate_horizon = score_candidate_panels(panels, close, manifest)
    rolling = rolling_ic_diagnostics(daily_ic)
    horizons = horizon_summary(candidate_horizon)
    family = family_summary(candidate_horizon)
    rankings = candidate_rankings(candidate_horizon)

    daily_ic.to_csv(out_dir / "daily_ic.csv", index=False)
    candidate_horizon.to_csv(out_dir / "candidate_horizon_ic_scores.csv", index=False)
    candidate_horizon.to_csv(out_dir / "candidate_ic_summary.csv", index=False)
    rolling.to_csv(out_dir / "rolling_ic_diagnostics.csv", index=False)
    horizons.to_csv(out_dir / "horizon_summary.csv", index=False)
    family.to_csv(out_dir / "family_summary.csv", index=False)
    rankings.to_csv(out_dir / "candidate_rankings.csv", index=False)
    manifest.to_csv(out_dir / "approved_panel_manifest.csv", index=False)
    (out_dir / "manifest.json").write_text(
        json.dumps(
            {
                "run_id": RUN_ID,
                "source_run_id": SOURCE_RUN_ID,
                "research_only": True,
                "research_only_guardrail": RESEARCH_ONLY_GUARDRAIL,
                "approved_candidate_count": len(APPROVED_CANDIDATE_IDS),
                "approved_candidate_ids": APPROVED_CANDIDATE_IDS,
                "horizons": [f"h{horizon}" for horizon in HORIZONS],
                "rolling_windows": list(ROLLING_WINDOWS),
                "minimum_daily_observations": MIN_DAILY_OBSERVATIONS,
                "outputs": {
                    "daily_ic": str(out_dir / "daily_ic.csv"),
                    "candidate_ic_summary": str(out_dir / "candidate_ic_summary.csv"),
                    "horizon_summary": str(out_dir / "horizon_summary.csv"),
                    "family_summary": str(out_dir / "family_summary.csv"),
                    "candidate_rankings": str(out_dir / "candidate_rankings.csv"),
                    "rolling_ic_diagnostics": str(out_dir / "rolling_ic_diagnostics.csv"),
                    "candidate_horizon_ic_scores": str(out_dir / "candidate_horizon_ic_scores.csv"),
                },
                "ic_discovery_executed": True,
                "ir_calculated": True,
                "refinement_executed": False,
                "validation_executed": False,
                "governance_modified": False,
                "thresholds_modified": False,
                "production_registered": False,
                "ml_implemented": False,
                "formulas_modified": False,
                "panels_modified": False,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    return {
        "daily_ic": daily_ic,
        "candidate_ic_summary": candidate_horizon,
        "rolling_ic_diagnostics": rolling,
        "horizon_summary": horizons,
        "family_summary": family,
        "candidate_rankings": rankings,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Research-only OHLCV NHT/LR IC discovery pass.")
    parser.add_argument("--source-dir", type=Path, default=SOURCE_DIR)
    parser.add_argument("--close-path", type=Path, default=CLOSE_PATH)
    parser.add_argument("--out-dir", type=Path, default=OUT_DIR)
    args = parser.parse_args()
    outputs = run_ic_discovery(args.source_dir, args.close_path, args.out_dir)
    print(f"Wrote research-only IC discovery outputs for {len(APPROVED_CANDIDATE_IDS)} candidates to {args.out_dir}")
    print(outputs["candidate_rankings"][["rank", "candidate_id", "best_primary_horizon", "best_primary_mean_ic", "classification"]].to_string(index=False))
    print(RESEARCH_ONLY_GUARDRAIL)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
