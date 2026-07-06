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

from pipelines.dispersion_path_dependence_research_module_v1 import (
    BLOCKED_CANDIDATE_IDS,
    BLOCKED_FAMILY_PREFIXES,
    DIAGNOSTIC_COLUMNS,
    FAMILY,
    IMPLEMENTED_CANDIDATE_IDS,
    LONG_FORM_PANEL_COLUMNS,
    MODULE_ID,
    RESEARCH_STATUS,
    SPEC_ID,
)
from pipelines.run_dispersion_path_dependence_panel_generation_v1 import (
    PANEL_COLUMNS,
    TIMING_POLICY,
    validate_dpath_panel_artifacts,
)


RUN_ID = "dispersion_path_dependence_ic_discovery_v1"
SOURCE_PANEL_ROOT = Path("artifacts/research/dispersion_path_dependence_research_module_v1/panel_v1")
OUT_DIR = Path("artifacts/research/dispersion_path_dependence_research_module_v1/ic_discovery_v1")
CLOSE_PATH = Path("data/processed/phase2/nb01_data_foundation/close_prices.parquet")
HORIZONS = (1, 5, 10, 20)
PRIMARY_HORIZONS = ("h10", "h20")
ROLLING_WINDOWS = (63, 126, 252)
MIN_DAILY_OBSERVATIONS = 25

ADVANCE_MEAN_IC_MIN = 0.005
ADVANCE_IC_IR_MIN = 0.030
ADVANCE_POSITIVE_IC_RATE_MIN = 0.530
ADVANCE_COVERAGE_RATIO_MIN = 0.300
WATCH_MEAN_IC_MIN = 0.0
WATCH_POSITIVE_IC_RATE_MIN = 0.500
WATCH_COVERAGE_RATIO_MIN = 0.250
PARK_ACTIVATION_RATE_MIN = 0.020

CLASSIFICATION_THRESHOLDS = {
    "advance_to_research_review": {
        "mean_ic_min": ADVANCE_MEAN_IC_MIN,
        "ic_ir_min": ADVANCE_IC_IR_MIN,
        "positive_ic_rate_min": ADVANCE_POSITIVE_IC_RATE_MIN,
        "coverage_ratio_min": ADVANCE_COVERAGE_RATIO_MIN,
    },
    "watch": {
        "mean_ic_min_exclusive": WATCH_MEAN_IC_MIN,
        "positive_ic_rate_min": WATCH_POSITIVE_IC_RATE_MIN,
        "coverage_ratio_min": WATCH_COVERAGE_RATIO_MIN,
    },
    "park": {
        "activation_rate_min": PARK_ACTIVATION_RATE_MIN,
    },
}

RESEARCH_ONLY_GUARDRAIL = (
    "Research-only IC discovery for audited Dispersion Path-Dependence panels. No panel "
    "regeneration, formula change, implementation change, refinement, validation, governance "
    "mutation, production registration, threshold change, or ML work is performed."
)

LINEAGE_COLUMNS = (
    "candidate_id",
    "candidate_name",
    "mechanism_family",
    "hypothesis",
    "scientific_question",
    "expected_evidence",
    "primary_falsification_criterion",
    "observable_implication",
    "expected_orthogonality",
    "contamination_controls",
    "anchor_comparators",
    "formula_text",
    "activation_text",
    "primary_horizon",
    "secondary_horizons",
    "expected_sign",
    "research_status",
)

CONTAMINATION_DIAGNOSTICS = (
    "disp_20",
    "disp_z_20",
    "disp_slope_5",
    "disp_slope_10",
    "divergence_intensity",
    "mkt_vol_20",
    "mkt_vol_slope_10",
    "mkt_stress_20",
    "mkt_stress_slope_10",
    "vov_5_20",
    "rank_churn_5",
    "low_churn_5",
    "low_extension_20",
    "leadership_crowding_60",
    "emerging_improvement_5_20",
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
        if "smooth" in value.lower() or "burst" in value.lower():
            return True
    return False


def _load_panel_manifest(panel_root: Path = SOURCE_PANEL_ROOT) -> pd.DataFrame:
    ok, errors = validate_dpath_panel_artifacts(panel_root)
    if not ok:
        raise ValueError("audited DPath panel validation failed: " + "; ".join(errors))
    manifest = pd.read_csv(panel_root / "panel_manifest.csv")
    ids = tuple(manifest["candidate_id"].astype(str))
    if ids != IMPLEMENTED_CANDIDATE_IDS:
        raise ValueError(f"DPath panel manifest candidate IDs mismatch: {ids}")
    if _blocked_candidate_present(manifest["candidate_id"]):
        raise ValueError("blocked candidate appeared in DPath panel manifest")
    required = {
        "candidate_id",
        "candidate_name",
        "mechanism_family",
        "module_id",
        "panel_path",
        "row_count",
        "duplicate_key_count",
        "blocked_candidate_count",
        "timing_policy",
        "schema_status",
    }
    missing = required - set(manifest.columns)
    if missing:
        raise ValueError("DPath panel manifest missing required columns: " + ", ".join(sorted(missing)))
    if set(manifest["module_id"].astype(str)) != {MODULE_ID}:
        raise ValueError("DPath panel manifest module_id mismatch")
    if set(manifest["timing_policy"].astype(str)) != {TIMING_POLICY}:
        raise ValueError("DPath panel manifest timing policy mismatch")
    if int(manifest["duplicate_key_count"].sum()) != 0:
        raise ValueError("DPath panel manifest reports duplicate keys")
    if int(manifest["blocked_candidate_count"].sum()) != 0:
        raise ValueError("DPath panel manifest reports blocked candidate rows")
    if set(manifest["schema_status"].astype(str)) != {"PASS"}:
        raise ValueError("DPath panel manifest has non-PASS schema status")
    return manifest


def _lineage_from_panel(panel_long: pd.DataFrame, candidate_id: str) -> dict[str, object]:
    lineage: dict[str, object] = {}
    for column in LINEAGE_COLUMNS:
        if column not in panel_long.columns:
            raise ValueError(f"{candidate_id} missing lineage column: {column}")
        values = panel_long[column].dropna().astype(str).unique()
        if len(values) != 1:
            raise ValueError(f"{candidate_id} lineage column is not constant: {column}")
        lineage[column] = values[0]
    return lineage


def _max_abs_contamination_indicator(panel_long: pd.DataFrame) -> tuple[float, str | None]:
    best_name: str | None = None
    best_value = np.nan
    signal = pd.to_numeric(panel_long["signal_value"], errors="coerce")
    for column in CONTAMINATION_DIAGNOSTICS:
        if column not in panel_long.columns:
            continue
        diagnostic = pd.to_numeric(panel_long[column], errors="coerce")
        valid = signal.notna() & diagnostic.notna()
        if int(valid.sum()) < MIN_DAILY_OBSERVATIONS:
            continue
        corr = signal[valid].rank().corr(diagnostic[valid].rank())
        if pd.notna(corr) and (pd.isna(best_value) or abs(corr) > abs(best_value)):
            best_value = float(corr)
            best_name = column
    return float(best_value) if pd.notna(best_value) else np.nan, best_name


def _turnover_proxy(panel: pd.DataFrame) -> float:
    ranks = panel.rank(axis=1, pct=True)
    daily_turnover = ranks.diff().abs().mean(axis=1, skipna=True)
    return float(daily_turnover.dropna().mean()) if daily_turnover.notna().any() else np.nan


def _load_candidate_panel(path: str | Path, candidate_id: str) -> tuple[pd.DataFrame, dict[str, object]]:
    panel_long = pd.read_parquet(path)
    missing = set(PANEL_COLUMNS) - set(panel_long.columns)
    if missing:
        raise ValueError(f"DPath panel {path} missing columns: {sorted(missing)}")
    if panel_long[["date", "ticker", "candidate_id"]].duplicated().any():
        raise ValueError(f"DPath panel {path} contains duplicate date/ticker/candidate rows")
    if set(panel_long["candidate_id"].astype(str)) != {candidate_id}:
        raise ValueError(f"DPath panel {path} candidate_id mismatch")
    if _blocked_candidate_present(panel_long["candidate_id"]):
        raise ValueError(f"blocked candidate appeared in {path}")
    if set(panel_long["module_id"].astype(str)) != {MODULE_ID}:
        raise ValueError(f"DPath panel {path} module_id mismatch")
    if set(panel_long["spec_id"].astype(str)) != {SPEC_ID}:
        raise ValueError(f"DPath panel {path} spec_id mismatch")
    if set(panel_long["research_status"].astype(str)) != {RESEARCH_STATUS}:
        raise ValueError(f"DPath panel {path} research_status mismatch")
    if set(panel_long["timing_policy"].astype(str)) != {TIMING_POLICY}:
        raise ValueError(f"DPath panel {path} timing policy mismatch")

    lineage = _lineage_from_panel(panel_long, candidate_id)
    max_diag_corr, max_diag_name = _max_abs_contamination_indicator(panel_long)
    panel = panel_long.pivot(index="date", columns="ticker", values="signal_value")
    panel.index = pd.to_datetime(panel.index)
    panel = panel.sort_index()
    active_rows = int(panel_long["is_active"].astype(bool).sum())
    feature_ready_rows = int(panel_long["feature_warmup_complete"].astype(bool).sum())
    metadata = {
        **lineage,
        "module_id": str(panel_long["module_id"].iloc[0]),
        "spec_id": str(panel_long["spec_id"].iloc[0]),
        "family": FAMILY,
        "timing_policy": str(panel_long["timing_policy"].iloc[0]),
        "panel_row_count": int(len(panel_long)),
        "non_null_signal_count": int(panel_long["signal_value"].notna().sum()),
        "warmup_incomplete_count": int((~panel_long["feature_warmup_complete"].astype(bool)).sum()),
        "inactive_row_count": int((~panel_long["is_active"].astype(bool)).sum()),
        "active_row_count": active_rows,
        "feature_ready_row_count": feature_ready_rows,
        "activation_rate": active_rows / feature_ready_rows if feature_ready_rows else np.nan,
        "turnover_proxy": _turnover_proxy(panel),
        "max_abs_internal_diagnostic_corr": abs(max_diag_corr) if pd.notna(max_diag_corr) else np.nan,
        "max_internal_diagnostic_corr": max_diag_corr,
        "max_internal_diagnostic_corr_name": max_diag_name,
    }
    return panel, metadata


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
        for candidate_id in IMPLEMENTED_CANDIDATE_IDS:
            panel = panels[candidate_id].reindex(index=close.index, columns=close.columns)
            daily = _daily_ic_frame(panel, fwd, horizon)
            meta = metadata[candidate_id]
            for key in (
                "candidate_name",
                "mechanism_family",
                "module_id",
                "spec_id",
                "family",
                "primary_horizon",
                "secondary_horizons",
                "expected_sign",
                "timing_policy",
                "hypothesis",
                "scientific_question",
                "expected_evidence",
                "primary_falsification_criterion",
                "observable_implication",
                "expected_orthogonality",
                "contamination_controls",
                "anchor_comparators",
            ):
                daily[key] = meta[key]
            daily["candidate_id"] = candidate_id
            valid_ic = daily["ic"].dropna()
            mean_ic = float(valid_ic.mean()) if len(valid_ic) else np.nan
            median_ic = float(valid_ic.median()) if len(valid_ic) else np.nan
            ic_std = float(valid_ic.std(ddof=0)) if len(valid_ic) > 1 else np.nan
            summary_rows.append(
                {
                    "candidate_id": candidate_id,
                    "candidate_name": meta["candidate_name"],
                    "mechanism_family": meta["mechanism_family"],
                    "module_id": meta["module_id"],
                    "spec_id": meta["spec_id"],
                    "family": meta["family"],
                    "primary_horizon": meta["primary_horizon"],
                    "secondary_horizons": meta["secondary_horizons"],
                    "expected_sign": meta["expected_sign"],
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
                    "active_row_count": meta["active_row_count"],
                    "activation_rate": meta["activation_rate"],
                    "turnover_proxy": meta["turnover_proxy"],
                    "max_abs_internal_diagnostic_corr": meta["max_abs_internal_diagnostic_corr"],
                    "max_internal_diagnostic_corr_name": meta["max_internal_diagnostic_corr_name"],
                    "hypothesis": meta["hypothesis"],
                    "scientific_question": meta["scientific_question"],
                    "expected_evidence": meta["expected_evidence"],
                    "primary_falsification_criterion": meta["primary_falsification_criterion"],
                    "observable_implication": meta["observable_implication"],
                    "expected_orthogonality": meta["expected_orthogonality"],
                    "contamination_controls": meta["contamination_controls"],
                    "anchor_comparators": meta["anchor_comparators"],
                }
            )
            daily_rows.append(daily)
    daily_ic = pd.concat(daily_rows, ignore_index=True)
    daily_ic = daily_ic[
        [
            "date",
            "candidate_id",
            "candidate_name",
            "mechanism_family",
            "module_id",
            "spec_id",
            "family",
            "primary_horizon",
            "secondary_horizons",
            "expected_sign",
            "timing_policy",
            "horizon",
            "ic",
            "observation_count",
            "signal_count",
            "target_count",
            "coverage_ratio",
            "hypothesis",
            "scientific_question",
            "expected_evidence",
            "primary_falsification_criterion",
            "observable_implication",
            "expected_orthogonality",
            "contamination_controls",
            "anchor_comparators",
        ]
    ]
    return daily_ic, pd.DataFrame(summary_rows)


def rolling_ic_diagnostics(daily_ic: pd.DataFrame) -> pd.DataFrame:
    rows: list[pd.DataFrame] = []
    for (candidate_id, horizon), group in daily_ic.sort_values("date").groupby(["candidate_id", "horizon"]):
        out = group[["date", "candidate_id", "candidate_name", "mechanism_family", "family", "horizon"]].copy()
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
            mean_turnover_proxy=("turnover_proxy", "mean"),
            total_observation_count=("observation_count", "sum"),
        )
    )
    out["horizon_order"] = out["horizon"].map({f"h{horizon}": idx for idx, horizon in enumerate(HORIZONS)})
    return out.sort_values("horizon_order").drop(columns="horizon_order")


def family_summary(candidate_horizon_scores: pd.DataFrame) -> pd.DataFrame:
    out = (
        candidate_horizon_scores.groupby(["family", "horizon"], as_index=False)
        .agg(
            candidate_count=("candidate_id", "nunique"),
            mean_ic=("mean_ic", "mean"),
            median_ic=("mean_ic", "median"),
            mean_abs_ic=("mean_ic", lambda values: values.abs().mean()),
            mean_ic_ir=("ic_ir", "mean"),
            mean_positive_ic_rate=("positive_ic_rate", "mean"),
            mean_coverage_ratio=("coverage_ratio", "mean"),
            mean_turnover_proxy=("turnover_proxy", "mean"),
            total_observation_count=("observation_count", "sum"),
        )
    )
    out["horizon_order"] = out["horizon"].map({f"h{horizon}": idx for idx, horizon in enumerate(HORIZONS)})
    return out.sort_values(["family", "horizon_order"]).drop(columns="horizon_order")


def _best_horizon_row(candidate_horizon_scores: pd.DataFrame, candidate_id: str, horizons: tuple[str, ...]) -> pd.Series:
    subset = candidate_horizon_scores[
        candidate_horizon_scores["candidate_id"].eq(candidate_id)
        & candidate_horizon_scores["horizon"].isin(horizons)
    ]
    return subset.sort_values("mean_ic", ascending=False).iloc[0]


def hypothesis_consistency(candidate_horizon_scores: pd.DataFrame, candidate_id: str) -> str:
    h10 = candidate_horizon_scores[
        candidate_horizon_scores["candidate_id"].eq(candidate_id)
        & candidate_horizon_scores["horizon"].eq("h10")
    ].iloc[0]
    best_any = _best_horizon_row(candidate_horizon_scores, candidate_id, tuple(f"h{h}" for h in HORIZONS))
    if (
        pd.notna(h10["mean_ic"])
        and h10["mean_ic"] > 0
        and pd.notna(h10["positive_ic_rate"])
        and h10["positive_ic_rate"] >= 0.50
        and best_any["horizon"] in {"h5", "h10"}
    ):
        return "MATCH"
    if (
        pd.notna(h10["mean_ic"])
        and h10["mean_ic"] > 0
        and pd.notna(h10["positive_ic_rate"])
        and h10["positive_ic_rate"] >= 0.48
    ) or (pd.notna(best_any["mean_ic"]) and best_any["mean_ic"] > 0 and best_any["horizon"] in {"h5", "h10", "h20"}):
        return "PARTIAL_MATCH"
    return "MISMATCH"


def candidate_ic_summary(candidate_horizon_scores: pd.DataFrame, rolling: pd.DataFrame) -> pd.DataFrame:
    primary = candidate_horizon_scores[candidate_horizon_scores["horizon"].isin(PRIMARY_HORIZONS)]
    base = (
        primary.groupby(
            [
                "candidate_id",
                "candidate_name",
                "mechanism_family",
                "module_id",
                "spec_id",
                "family",
                "primary_horizon",
                "secondary_horizons",
                "expected_sign",
            ],
            as_index=False,
        )
        .agg(
            primary_mean_ic=("mean_ic", "mean"),
            primary_best_mean_ic=("mean_ic", "max"),
            primary_mean_ic_ir=("ic_ir", "mean"),
            primary_mean_positive_ic_rate=("positive_ic_rate", "mean"),
            primary_observation_count=("observation_count", "sum"),
            non_null_signal_count=("non_null_signal_count", "max"),
            warmup_incomplete_count=("warmup_incomplete_count", "max"),
            inactive_row_count=("inactive_row_count", "max"),
            active_row_count=("active_row_count", "max"),
            activation_rate=("activation_rate", "max"),
            turnover_proxy=("turnover_proxy", "max"),
            max_abs_internal_diagnostic_corr=("max_abs_internal_diagnostic_corr", "max"),
        )
    )
    consistency = [
        {
            "candidate_id": candidate_id,
            "hypothesis_consistency": hypothesis_consistency(candidate_horizon_scores, candidate_id),
        }
        for candidate_id in base["candidate_id"].astype(str)
    ]
    return base.merge(pd.DataFrame(consistency), on="candidate_id", how="left")


def classify_candidate(row: pd.Series) -> str:
    if (
        pd.notna(row["best_primary_mean_ic"])
        and row["best_primary_mean_ic"] >= ADVANCE_MEAN_IC_MIN
        and pd.notna(row["best_primary_ic_ir"])
        and row["best_primary_ic_ir"] >= ADVANCE_IC_IR_MIN
        and pd.notna(row["best_primary_positive_ic_rate"])
        and row["best_primary_positive_ic_rate"] >= ADVANCE_POSITIVE_IC_RATE_MIN
        and pd.notna(row["best_primary_coverage_ratio"])
        and row["best_primary_coverage_ratio"] >= ADVANCE_COVERAGE_RATIO_MIN
    ):
        return "ADVANCE_TO_RESEARCH_REVIEW"
    if pd.notna(row["activation_rate"]) and row["activation_rate"] < PARK_ACTIVATION_RATE_MIN:
        return "PARK"
    if (
        pd.notna(row["best_primary_mean_ic"])
        and row["best_primary_mean_ic"] > WATCH_MEAN_IC_MIN
        and pd.notna(row["best_primary_positive_ic_rate"])
        and row["best_primary_positive_ic_rate"] >= WATCH_POSITIVE_IC_RATE_MIN
        and pd.notna(row["best_primary_coverage_ratio"])
        and row["best_primary_coverage_ratio"] >= WATCH_COVERAGE_RATIO_MIN
    ):
        return "WATCH"
    if pd.notna(row["best_any_mean_ic"]) and row["best_any_mean_ic"] > WATCH_MEAN_IC_MIN:
        return "PARK"
    return "REJECT"


def candidate_rankings(candidate_horizon_scores: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for candidate_id in IMPLEMENTED_CANDIDATE_IDS:
        best_primary = _best_horizon_row(candidate_horizon_scores, candidate_id, PRIMARY_HORIZONS)
        best_any = _best_horizon_row(candidate_horizon_scores, candidate_id, tuple(f"h{h}" for h in HORIZONS))
        h10 = candidate_horizon_scores[
            candidate_horizon_scores["candidate_id"].eq(candidate_id)
            & candidate_horizon_scores["horizon"].eq("h10")
        ].iloc[0]
        row = {
            "candidate_id": candidate_id,
            "candidate_name": best_primary["candidate_name"],
            "mechanism_family": best_primary["mechanism_family"],
            "module_id": best_primary["module_id"],
            "spec_id": best_primary["spec_id"],
            "family": best_primary["family"],
            "primary_horizon": best_primary["primary_horizon"],
            "expected_primary_horizon": best_primary["primary_horizon"],
            "observed_strongest_horizon": best_any["horizon"],
            "best_primary_horizon": best_primary["horizon"],
            "best_primary_mean_ic": best_primary["mean_ic"],
            "best_primary_ic_ir": best_primary["ic_ir"],
            "best_primary_positive_ic_rate": best_primary["positive_ic_rate"],
            "best_primary_coverage_ratio": best_primary["coverage_ratio"],
            "best_primary_observation_count": best_primary["observation_count"],
            "h10_mean_ic": h10["mean_ic"],
            "h10_ic_ir": h10["ic_ir"],
            "h10_positive_ic_rate": h10["positive_ic_rate"],
            "h10_coverage_ratio": h10["coverage_ratio"],
            "best_any_horizon": best_any["horizon"],
            "best_any_mean_ic": best_any["mean_ic"],
            "best_any_ic_ir": best_any["ic_ir"],
            "best_any_positive_ic_rate": best_any["positive_ic_rate"],
            "activation_rate": best_primary["activation_rate"],
            "turnover_proxy": best_primary["turnover_proxy"],
            "max_abs_internal_diagnostic_corr": best_primary["max_abs_internal_diagnostic_corr"],
            "max_internal_diagnostic_corr_name": best_primary["max_internal_diagnostic_corr_name"],
            "expected_orthogonality": best_primary["expected_orthogonality"],
            "contamination_controls": best_primary["contamination_controls"],
            "anchor_comparators": best_primary["anchor_comparators"],
            "hypothesis": best_primary["hypothesis"],
            "scientific_question": best_primary["scientific_question"],
            "expected_evidence": best_primary["expected_evidence"],
            "hypothesis_consistency": hypothesis_consistency(candidate_horizon_scores, candidate_id),
        }
        row["recommendation"] = classify_candidate(pd.Series(row))
        rows.append(row)
    ranking = pd.DataFrame(rows)
    ranking["rank"] = ranking["best_primary_mean_ic"].rank(method="first", ascending=False).astype(int)
    return ranking.sort_values("rank")


def discovery_classification(rankings: pd.DataFrame) -> str:
    recommendations = set(rankings["recommendation"].astype(str))
    if "ADVANCE_TO_RESEARCH_REVIEW" in recommendations:
        return "IC_DISCOVERY_COMPLETE_ADVANCE_CANDIDATES"
    if recommendations & {"WATCH", "PARK"}:
        return "IC_DISCOVERY_COMPLETE_WITH_NOTES"
    return "IC_DISCOVERY_INCONCLUSIVE"


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
    rankings = candidate_rankings(candidate_horizon)
    candidate_summary = candidate_ic_summary(candidate_horizon, rolling)
    classification = discovery_classification(rankings)

    daily_ic.to_csv(out_dir / "daily_ic.csv", index=False)
    candidate_horizon.to_csv(out_dir / "candidate_horizon_ic_scores.csv", index=False)
    candidate_summary.to_csv(out_dir / "candidate_ic_summary.csv", index=False)
    horizons.to_csv(out_dir / "horizon_summary.csv", index=False)
    family.to_csv(out_dir / "family_summary.csv", index=False)
    rankings.to_csv(out_dir / "candidate_rankings.csv", index=False)
    rolling.to_csv(out_dir / "rolling_ic_diagnostics.csv", index=False)
    manifest.to_csv(out_dir / "approved_panel_manifest.csv", index=False)
    panel_checksums = {
        Path(str(row["panel_path"])).name: _sha256_file(Path(str(row["panel_path"])))
        for row in manifest.to_dict(orient="records")
    }
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
                "approved_candidate_count": len(IMPLEMENTED_CANDIDATE_IDS),
                "approved_candidate_ids": list(IMPLEMENTED_CANDIDATE_IDS),
                "blocked_candidate_ids": list(BLOCKED_CANDIDATE_IDS),
                "blocked_candidate_prefixes": list(BLOCKED_FAMILY_PREFIXES),
                "horizons": [f"h{horizon}" for horizon in HORIZONS],
                "primary_review_horizons": list(PRIMARY_HORIZONS),
                "rolling_windows": list(ROLLING_WINDOWS),
                "minimum_daily_observations": MIN_DAILY_OBSERVATIONS,
                "timing_policy": TIMING_POLICY,
                "classification_thresholds": CLASSIFICATION_THRESHOLDS,
                "input_lineage_checksums": {
                    "panel_manifest_sha256": _sha256_file(panel_root / "panel_manifest.csv"),
                    "panel_generation_manifest_sha256": _sha256_file(panel_root / "panel_generation_manifest.json"),
                    "approved_panel_parquet_sha256": panel_checksums,
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
                "panels_modified": False,
                "formulas_modified": False,
                "implementation_modified": False,
                "refinement_executed": False,
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
    parser = argparse.ArgumentParser(description="Run DPath research-only IC discovery.")
    parser.add_argument("--panel-root", type=Path, default=SOURCE_PANEL_ROOT)
    parser.add_argument("--close-path", type=Path, default=CLOSE_PATH)
    parser.add_argument("--out-dir", type=Path, default=OUT_DIR)
    args = parser.parse_args()
    outputs = run_ic_discovery(panel_root=args.panel_root, close_path=args.close_path, out_dir=args.out_dir)
    rankings = outputs["candidate_rankings"]
    print(f"Wrote DPath IC discovery artifacts for {len(IMPLEMENTED_CANDIDATE_IDS)} candidates to {args.out_dir}")
    print(
        rankings[
            [
                "rank",
                "candidate_id",
                "observed_strongest_horizon",
                "h10_mean_ic",
                "best_primary_mean_ic",
                "best_primary_ic_ir",
                "best_primary_positive_ic_rate",
                "hypothesis_consistency",
                "recommendation",
            ]
        ].to_string(index=False)
    )
    print(RESEARCH_ONLY_GUARDRAIL)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
