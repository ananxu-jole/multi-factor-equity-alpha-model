from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from pipelines.ohlcv_volatility_of_volatility_refinement_v1 import (
    BLOCKED_CANDIDATE_IDS,
    BLOCKED_FAMILY_PREFIXES,
    FAMILY,
    IMPLEMENTED_REFINEMENT_IDS,
    MODULE_ID,
)
from pipelines.run_ohlcv_volatility_of_volatility_refinement_panel_generation_v1 import (
    PANEL_COLUMNS,
    TIMING_POLICY,
    validate_refinement_panel_artifacts,
)


RUN_ID = "ohlcv_volatility_of_volatility_bounded_refinement_ic_discovery_v1"
SOURCE_PANEL_ROOT = Path("artifacts/research/ohlcv_volatility_of_volatility_refinement_v1/panel_v1")
OUT_DIR = Path("artifacts/research/ohlcv_volatility_of_volatility_refinement_v1/ic_discovery_v1")
CLOSE_PATH = Path("data/processed/phase2/nb01_data_foundation/close_prices.parquet")
HORIZONS = (1, 5, 10, 20)
PRIMARY_HORIZONS = ("h10", "h20")
ROLLING_WINDOWS = (63, 126, 252)
MIN_DAILY_OBSERVATIONS = 25
ADVANCE_MEAN_IC_MIN = 0.005
ADVANCE_IC_IR_MIN = 0.030
ADVANCE_POSITIVE_IC_RATE_MIN = 0.530
ADVANCE_COVERAGE_RATIO_MIN = 0.300
ADVANCE_MEAN_IC_DELTA_VS_ANCHOR_MIN = 0.0005
WATCH_MEAN_IC_MIN = 0.0
WATCH_POSITIVE_IC_RATE_MIN = 0.500
WATCH_COVERAGE_RATIO_MIN = 0.300
CLASSIFICATION_THRESHOLDS = {
    "anchor_advance": {
        "mean_ic_min": ADVANCE_MEAN_IC_MIN,
        "ic_ir_min": ADVANCE_IC_IR_MIN,
        "positive_ic_rate_min": ADVANCE_POSITIVE_IC_RATE_MIN,
        "coverage_ratio_min": ADVANCE_COVERAGE_RATIO_MIN,
    },
    "refinement_advance": {
        "mean_ic_min": ADVANCE_MEAN_IC_MIN,
        "ic_ir_min": ADVANCE_IC_IR_MIN,
        "positive_ic_rate_min": ADVANCE_POSITIVE_IC_RATE_MIN,
        "coverage_ratio_min": ADVANCE_COVERAGE_RATIO_MIN,
        "mean_ic_delta_vs_anchor_min": ADVANCE_MEAN_IC_DELTA_VS_ANCHOR_MIN,
    },
    "watch": {
        "mean_ic_min_exclusive": WATCH_MEAN_IC_MIN,
        "positive_ic_rate_min": WATCH_POSITIVE_IC_RATE_MIN,
        "coverage_ratio_min": WATCH_COVERAGE_RATIO_MIN,
    },
}

ANCHOR_BY_FAMILY = {
    "vov_01_refinement": "vov_01_ref_anchor",
    "vov_03_refinement": "vov_03_ref_anchor",
}

RESEARCH_ONLY_GUARDRAIL = (
    "Research-only bounded VoV refinement IC discovery. No formula changes, panel "
    "regeneration, approved panel mutation, validation, governance mutation, production "
    "registration, threshold change, ML work, or blocked candidate inclusion is performed."
)


def _ensure_out_dir(out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)


def _sha256_file(path: Path) -> str | None:
    if not path.exists():
        return None
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _blocked_candidate_present(values: pd.Series) -> bool:
    for value in values.dropna().astype(str):
        if value in BLOCKED_CANDIDATE_IDS:
            return True
        if value.startswith(BLOCKED_FAMILY_PREFIXES):
            return True
    return False


def _load_panel_manifest(panel_root: Path = SOURCE_PANEL_ROOT) -> pd.DataFrame:
    ok, errors = validate_refinement_panel_artifacts(panel_root)
    if not ok:
        raise ValueError("audited VoV refinement panel validation failed: " + "; ".join(errors))
    manifest = pd.read_csv(panel_root / "panel_manifest.csv")
    ids = tuple(manifest["candidate_id"].astype(str))
    if ids != IMPLEMENTED_REFINEMENT_IDS:
        raise ValueError(f"VoV refinement panel manifest candidate IDs mismatch: {ids}")
    if _blocked_candidate_present(manifest["candidate_id"]):
        raise ValueError("blocked candidate appeared in VoV refinement panel manifest")
    required = {
        "candidate_id",
        "parent_candidate_id",
        "source_spec_id",
        "refinement_family",
        "panel_path",
        "row_count",
        "duplicate_key_count",
        "timing_policy",
        "schema_status",
        "blocked_candidate_check",
    }
    missing = required - set(manifest.columns)
    if missing:
        raise ValueError("VoV refinement panel manifest missing required columns: " + ", ".join(sorted(missing)))
    if set(manifest["timing_policy"].astype(str)) != {TIMING_POLICY}:
        raise ValueError("VoV refinement panel manifest timing policy mismatch")
    if int(manifest["duplicate_key_count"].sum()) != 0:
        raise ValueError("VoV refinement panel manifest reports duplicate keys")
    if set(manifest["schema_status"].astype(str)) != {"PASS"}:
        raise ValueError("VoV refinement panel manifest has non-PASS schema status")
    if set(manifest["blocked_candidate_check"].astype(str)) != {"PASS"}:
        raise ValueError("VoV refinement panel manifest has non-PASS blocked candidate check")
    return manifest


def _load_candidate_panel(path: str | Path, candidate_id: str) -> tuple[pd.DataFrame, dict[str, object]]:
    panel_long = pd.read_parquet(path)
    missing = set(PANEL_COLUMNS) - set(panel_long.columns)
    if missing:
        raise ValueError(f"refinement panel {path} missing columns: {sorted(missing)}")
    if panel_long[["date", "ticker", "candidate_id"]].duplicated().any():
        raise ValueError(f"refinement panel {path} contains duplicate date/ticker/candidate rows")
    if set(panel_long["candidate_id"].astype(str)) != {candidate_id}:
        raise ValueError(f"refinement panel {path} candidate_id mismatch")
    if _blocked_candidate_present(panel_long["candidate_id"]):
        raise ValueError(f"blocked candidate appeared in {path}")
    if set(panel_long["module_id"].astype(str)) != {MODULE_ID}:
        raise ValueError(f"refinement panel {path} module_id mismatch")
    if set(panel_long["family"].astype(str)) != {FAMILY}:
        raise ValueError(f"refinement panel {path} family mismatch")
    if set(panel_long["timing_policy"].astype(str)) != {TIMING_POLICY}:
        raise ValueError(f"refinement panel {path} timing policy mismatch")

    metadata = {
        "candidate_id": candidate_id,
        "source_spec_id": str(panel_long["source_spec_id"].iloc[0]),
        "parent_candidate_id": str(panel_long["parent_candidate_id"].iloc[0]),
        "module_id": str(panel_long["module_id"].iloc[0]),
        "refinement_family": str(panel_long["refinement_family"].iloc[0]),
        "family": str(panel_long["family"].iloc[0]),
        "research_status": str(panel_long["research_status"].iloc[0]),
        "primary_horizon": str(panel_long["primary_horizon"].iloc[0]),
        "secondary_horizons": str(panel_long["secondary_horizons"].iloc[0]),
        "timing_policy": str(panel_long["timing_policy"].iloc[0]),
        "panel_row_count": int(len(panel_long)),
        "non_null_signal_count": int(panel_long["signal_value"].notna().sum()),
        "warmup_incomplete_count": int((~panel_long["feature_warmup_complete"].astype(bool)).sum()),
        "inactive_row_count": int((~panel_long["is_active"].astype(bool)).sum()),
    }
    panel = panel_long.pivot(index="date", columns="ticker", values="signal_value")
    panel.index = pd.to_datetime(panel.index)
    return panel.sort_index(), metadata


def _load_candidate_panels(manifest: pd.DataFrame) -> tuple[dict[str, pd.DataFrame], dict[str, dict[str, object]]]:
    panels: dict[str, pd.DataFrame] = {}
    metadata: dict[str, dict[str, object]] = {}
    for row in manifest.to_dict(orient="records"):
        candidate_id = str(row["candidate_id"])
        panel, meta = _load_candidate_panel(row["panel_path"], candidate_id)
        panels[candidate_id] = panel
        metadata[candidate_id] = meta
    return panels, metadata


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


def score_candidate_panels(
    panels: dict[str, pd.DataFrame],
    close: pd.DataFrame,
    metadata: dict[str, dict[str, object]],
) -> tuple[pd.DataFrame, pd.DataFrame]:
    daily_rows: list[pd.DataFrame] = []
    summary_rows: list[dict[str, object]] = []
    for horizon in HORIZONS:
        fwd = _forward_returns(close, horizon)
        for candidate_id in IMPLEMENTED_REFINEMENT_IDS:
            panel = panels[candidate_id].reindex(index=close.index, columns=close.columns)
            daily = _daily_ic_frame(panel, fwd, horizon)
            meta = metadata[candidate_id]
            for key, value in meta.items():
                daily[key] = value
            daily = daily[
                [
                    "date",
                    "candidate_id",
                    "source_spec_id",
                    "parent_candidate_id",
                    "module_id",
                    "refinement_family",
                    "family",
                    "primary_horizon",
                    "secondary_horizons",
                    "timing_policy",
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
                    "source_spec_id": meta["source_spec_id"],
                    "parent_candidate_id": meta["parent_candidate_id"],
                    "module_id": meta["module_id"],
                    "refinement_family": meta["refinement_family"],
                    "family": meta["family"],
                    "primary_horizon": meta["primary_horizon"],
                    "secondary_horizons": meta["secondary_horizons"],
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
                    "panel_row_count": meta["panel_row_count"],
                    "non_null_signal_count": meta["non_null_signal_count"],
                    "warmup_incomplete_count": meta["warmup_incomplete_count"],
                    "inactive_row_count": meta["inactive_row_count"],
                }
            )
            daily_rows.append(daily)
    scored = pd.DataFrame(summary_rows)
    scored = add_anchor_comparisons(scored)
    return pd.concat(daily_rows, ignore_index=True), scored


def add_anchor_comparisons(candidate_horizon_scores: pd.DataFrame) -> pd.DataFrame:
    out = candidate_horizon_scores.copy()
    anchor = out.loc[
        out["candidate_id"].isin(ANCHOR_BY_FAMILY.values()),
        ["candidate_id", "refinement_family", "horizon", "mean_ic", "ic_ir", "positive_ic_rate"],
    ].rename(
        columns={
            "candidate_id": "anchor_candidate_id",
            "mean_ic": "anchor_mean_ic",
            "ic_ir": "anchor_ic_ir",
            "positive_ic_rate": "anchor_positive_ic_rate",
        }
    )
    out = out.merge(anchor, on=["refinement_family", "horizon"], how="left")
    out["mean_ic_delta_vs_anchor"] = out["mean_ic"] - out["anchor_mean_ic"]
    out["ic_ir_delta_vs_anchor"] = out["ic_ir"] - out["anchor_ic_ir"]
    out["positive_ic_rate_delta_vs_anchor"] = out["positive_ic_rate"] - out["anchor_positive_ic_rate"]
    out.loc[out["candidate_id"].eq(out["anchor_candidate_id"]), [
        "mean_ic_delta_vs_anchor",
        "ic_ir_delta_vs_anchor",
        "positive_ic_rate_delta_vs_anchor",
    ]] = 0.0
    return out


def rolling_ic_diagnostics(daily_ic: pd.DataFrame) -> pd.DataFrame:
    rows: list[pd.DataFrame] = []
    for (candidate_id, horizon), group in daily_ic.sort_values("date").groupby(["candidate_id", "horizon"]):
        out = group[
            ["date", "candidate_id", "source_spec_id", "parent_candidate_id", "refinement_family", "family", "horizon"]
        ].copy()
        series = group["ic"]
        for window in ROLLING_WINDOWS:
            min_periods = max(20, window // 3)
            rolling_mean = series.rolling(window, min_periods=min_periods).mean()
            rolling_std = series.rolling(window, min_periods=min_periods).std(ddof=0)
            out[f"rolling_{window}_mean_ic"] = rolling_mean
            out[f"rolling_{window}_ic_ir"] = rolling_mean / rolling_std.replace(0, np.nan)
            out[f"rolling_{window}_positive_ic_rate"] = series.gt(0).rolling(window, min_periods=min_periods).mean()
        rows.append(out)
    return pd.concat(rows, ignore_index=True)


def horizon_summary(candidate_horizon_scores: pd.DataFrame) -> pd.DataFrame:
    out = (
        candidate_horizon_scores.groupby("horizon", as_index=False)
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


def family_summary(candidate_horizon_scores: pd.DataFrame) -> pd.DataFrame:
    out = (
        candidate_horizon_scores.groupby(["family", "refinement_family", "horizon"], as_index=False)
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
    return out.sort_values(["family", "refinement_family", "horizon_order"]).drop(columns="horizon_order")


def candidate_ic_summary(candidate_horizon_scores: pd.DataFrame) -> pd.DataFrame:
    primary = candidate_horizon_scores[candidate_horizon_scores["horizon"].isin(PRIMARY_HORIZONS)]
    out = (
        primary.groupby(
            [
                "candidate_id",
                "source_spec_id",
                "parent_candidate_id",
                "module_id",
                "refinement_family",
                "family",
                "primary_horizon",
            ],
            as_index=False,
        )
        .agg(
            primary_mean_ic=("mean_ic", "mean"),
            primary_best_mean_ic=("mean_ic", "max"),
            primary_mean_ic_ir=("ic_ir", "mean"),
            primary_mean_positive_ic_rate=("positive_ic_rate", "mean"),
            primary_mean_delta_vs_anchor=("mean_ic_delta_vs_anchor", "mean"),
            primary_best_delta_vs_anchor=("mean_ic_delta_vs_anchor", "max"),
            primary_observation_count=("observation_count", "sum"),
            non_null_signal_count=("non_null_signal_count", "max"),
            warmup_incomplete_count=("warmup_incomplete_count", "max"),
            inactive_row_count=("inactive_row_count", "max"),
        )
    )
    return out


def classify_candidate(
    candidate_id: str,
    mean_ic: float,
    ic_ir: float,
    positive_ic_rate: float,
    coverage_ratio: float,
    mean_ic_delta_vs_anchor: float,
) -> str:
    if candidate_id in ANCHOR_BY_FAMILY.values():
        if (
            pd.notna(mean_ic)
            and mean_ic >= ADVANCE_MEAN_IC_MIN
            and pd.notna(ic_ir)
            and ic_ir >= ADVANCE_IC_IR_MIN
            and pd.notna(positive_ic_rate)
            and positive_ic_rate >= ADVANCE_POSITIVE_IC_RATE_MIN
            and pd.notna(coverage_ratio)
            and coverage_ratio >= ADVANCE_COVERAGE_RATIO_MIN
        ):
            return "ADVANCE_TO_VALIDATION_DESIGN"
        if (
            pd.notna(mean_ic)
            and mean_ic > WATCH_MEAN_IC_MIN
            and pd.notna(positive_ic_rate)
            and positive_ic_rate >= WATCH_POSITIVE_IC_RATE_MIN
        ):
            return "WATCH"
        return "REJECT"

    if (
        pd.notna(mean_ic)
        and mean_ic >= ADVANCE_MEAN_IC_MIN
        and pd.notna(ic_ir)
        and ic_ir >= ADVANCE_IC_IR_MIN
        and pd.notna(positive_ic_rate)
        and positive_ic_rate >= ADVANCE_POSITIVE_IC_RATE_MIN
        and pd.notna(coverage_ratio)
        and coverage_ratio >= ADVANCE_COVERAGE_RATIO_MIN
        and pd.notna(mean_ic_delta_vs_anchor)
        and mean_ic_delta_vs_anchor >= ADVANCE_MEAN_IC_DELTA_VS_ANCHOR_MIN
    ):
        return "ADVANCE_TO_VALIDATION_DESIGN"
    if (
        pd.notna(mean_ic)
        and mean_ic > WATCH_MEAN_IC_MIN
        and pd.notna(positive_ic_rate)
        and positive_ic_rate >= WATCH_POSITIVE_IC_RATE_MIN
        and pd.notna(coverage_ratio)
        and coverage_ratio >= WATCH_COVERAGE_RATIO_MIN
    ):
        return "WATCH"
    return "REJECT"


def candidate_rankings(candidate_horizon_scores: pd.DataFrame) -> pd.DataFrame:
    primary = candidate_horizon_scores[candidate_horizon_scores["horizon"].isin(PRIMARY_HORIZONS)].copy()
    best_primary = (
        primary.sort_values(["candidate_id", "mean_ic"], ascending=[True, False])
        .groupby("candidate_id", as_index=False)
        .head(1)
    )
    best_any = (
        candidate_horizon_scores.sort_values(["candidate_id", "mean_ic"], ascending=[True, False])
        .groupby("candidate_id", as_index=False)
        .head(1)
    )
    rows: list[dict[str, object]] = []
    for row in best_primary.to_dict(orient="records"):
        candidate_id = str(row["candidate_id"])
        any_row = best_any[best_any["candidate_id"].eq(candidate_id)].iloc[0]
        recommendation = classify_candidate(
            candidate_id,
            float(row["mean_ic"]),
            float(row["ic_ir"]),
            float(row["positive_ic_rate"]),
            float(row["coverage_ratio"]),
            float(row["mean_ic_delta_vs_anchor"]),
        )
        rows.append(
            {
                "candidate_id": candidate_id,
                "source_spec_id": row["source_spec_id"],
                "parent_candidate_id": row["parent_candidate_id"],
                "module_id": row["module_id"],
                "refinement_family": row["refinement_family"],
                "anchor_candidate_id": row["anchor_candidate_id"],
                "family": row["family"],
                "primary_horizon": row["primary_horizon"],
                "best_primary_horizon": row["horizon"],
                "best_primary_mean_ic": row["mean_ic"],
                "best_primary_ic_ir": row["ic_ir"],
                "best_primary_positive_ic_rate": row["positive_ic_rate"],
                "best_primary_coverage_ratio": row["coverage_ratio"],
                "best_primary_observation_count": row["observation_count"],
                "best_primary_mean_ic_delta_vs_anchor": row["mean_ic_delta_vs_anchor"],
                "best_primary_ic_ir_delta_vs_anchor": row["ic_ir_delta_vs_anchor"],
                "best_primary_positive_ic_rate_delta_vs_anchor": row["positive_ic_rate_delta_vs_anchor"],
                "best_any_horizon": any_row["horizon"],
                "best_any_mean_ic": any_row["mean_ic"],
                "best_any_ic_ir": any_row["ic_ir"],
                "best_any_positive_ic_rate": any_row["positive_ic_rate"],
                "recommendation": recommendation,
            }
        )
    ranking = pd.DataFrame(rows)
    ranking["rank"] = ranking["best_primary_mean_ic"].rank(method="first", ascending=False).astype(int)
    return ranking.sort_values("rank")


def discovery_classification(rankings: pd.DataFrame) -> str:
    recommendations = set(rankings["recommendation"].astype(str))
    if "ADVANCE_TO_VALIDATION_DESIGN" in recommendations:
        return "REFINEMENT_IC_DISCOVERY_COMPLETE_ADVANCE_CANDIDATES"
    if recommendations == {"WATCH"} or "WATCH" in recommendations:
        return "REFINEMENT_IC_DISCOVERY_COMPLETE_WATCH_ONLY"
    if recommendations == {"REJECT"}:
        return "REFINEMENT_IC_DISCOVERY_COMPLETE_NO_ADVANCE"
    return "REFINEMENT_IC_DISCOVERY_INCONCLUSIVE"


def run_ic_discovery(
    *,
    panel_root: Path = SOURCE_PANEL_ROOT,
    close_path: Path = CLOSE_PATH,
    out_dir: Path = OUT_DIR,
) -> dict[str, pd.DataFrame]:
    _ensure_out_dir(out_dir)
    manifest = _load_panel_manifest(panel_root)
    panels, metadata = _load_candidate_panels(manifest)
    close = _load_close(close_path)
    daily_ic, candidate_horizon = score_candidate_panels(panels, close, metadata)
    rolling = rolling_ic_diagnostics(daily_ic)
    horizons = horizon_summary(candidate_horizon)
    family = family_summary(candidate_horizon)
    candidate_summary = candidate_ic_summary(candidate_horizon)
    rankings = candidate_rankings(candidate_horizon)
    classification = discovery_classification(rankings)

    daily_ic.to_csv(out_dir / "daily_ic.csv", index=False)
    candidate_horizon.to_csv(out_dir / "candidate_horizon_ic_scores.csv", index=False)
    candidate_summary.to_csv(out_dir / "candidate_ic_summary.csv", index=False)
    horizons.to_csv(out_dir / "horizon_summary.csv", index=False)
    family.to_csv(out_dir / "family_summary.csv", index=False)
    rankings.to_csv(out_dir / "candidate_rankings.csv", index=False)
    rolling.to_csv(out_dir / "rolling_ic_diagnostics.csv", index=False)
    manifest.to_csv(out_dir / "approved_panel_manifest.csv", index=False)
    (out_dir / "manifest.json").write_text(
        json.dumps(
            {
                "run_id": RUN_ID,
                "module_id": MODULE_ID,
                "source_panel_root": str(panel_root),
                "close_path": str(close_path),
                "classification": classification,
                "research_only": True,
                "research_only_guardrail": RESEARCH_ONLY_GUARDRAIL,
                "approved_candidate_count": len(IMPLEMENTED_REFINEMENT_IDS),
                "approved_candidate_ids": list(IMPLEMENTED_REFINEMENT_IDS),
                "blocked_candidates": [*BLOCKED_CANDIDATE_IDS, "dpath_*", "ecluster_*"],
                "horizons": [f"h{horizon}" for horizon in HORIZONS],
                "primary_review_horizons": list(PRIMARY_HORIZONS),
                "rolling_windows": list(ROLLING_WINDOWS),
                "minimum_daily_observations": MIN_DAILY_OBSERVATIONS,
                "timing_policy": TIMING_POLICY,
                "anchor_by_family": ANCHOR_BY_FAMILY,
                "classification_thresholds": CLASSIFICATION_THRESHOLDS,
                "input_lineage_checksums": {
                    "panel_manifest_sha256": _sha256_file(panel_root / "panel_manifest.csv"),
                    "close_source_sha256": _sha256_file(close_path),
                },
                "outputs": {
                    "daily_ic": str(out_dir / "daily_ic.csv"),
                    "candidate_horizon_ic_scores": str(out_dir / "candidate_horizon_ic_scores.csv"),
                    "candidate_ic_summary": str(out_dir / "candidate_ic_summary.csv"),
                    "horizon_summary": str(out_dir / "horizon_summary.csv"),
                    "family_summary": str(out_dir / "family_summary.csv"),
                    "candidate_rankings": str(out_dir / "candidate_rankings.csv"),
                    "rolling_ic_diagnostics": str(out_dir / "rolling_ic_diagnostics.csv"),
                    "approved_panel_manifest": str(out_dir / "approved_panel_manifest.csv"),
                },
                "panel_validation_executed_before_ic": True,
                "ic_discovery_executed": True,
                "panel_generation_executed": False,
                "approved_panels_modified": False,
                "formulas_modified": False,
                "blocked_candidates_used": False,
                "validation_executed": False,
                "governance_modified": False,
                "production_registration": False,
                "thresholds_modified": False,
                "ml_integration": False,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    return {
        "daily_ic": daily_ic,
        "candidate_horizon_ic_scores": candidate_horizon,
        "candidate_ic_summary": candidate_summary,
        "horizon_summary": horizons,
        "family_summary": family,
        "candidate_rankings": rankings,
        "rolling_ic_diagnostics": rolling,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run bounded VoV refinement research-only IC discovery.")
    parser.add_argument("--panel-root", type=Path, default=SOURCE_PANEL_ROOT)
    parser.add_argument("--close-path", type=Path, default=CLOSE_PATH)
    parser.add_argument("--out-dir", type=Path, default=OUT_DIR)
    args = parser.parse_args()
    outputs = run_ic_discovery(panel_root=args.panel_root, close_path=args.close_path, out_dir=args.out_dir)
    rankings = outputs["candidate_rankings"]
    print(f"Wrote bounded VoV refinement IC discovery artifacts for {len(IMPLEMENTED_REFINEMENT_IDS)} variants to {args.out_dir}")
    print(
        rankings[
            [
                "rank",
                "candidate_id",
                "best_primary_horizon",
                "best_primary_mean_ic",
                "best_primary_mean_ic_delta_vs_anchor",
                "best_primary_ic_ir",
                "best_primary_positive_ic_rate",
                "recommendation",
            ]
        ].to_string(index=False)
    )
    print(RESEARCH_ONLY_GUARDRAIL)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
