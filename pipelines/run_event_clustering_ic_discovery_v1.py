from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from pipelines.event_clustering_research_module_v1 import (
    CONTAMINATION_CONTROLS,
    FAMILY,
    IMPLEMENTED_CANDIDATE_IDS,
    MODULE_ID,
    RESEARCH_STATUS,
    SPEC_ID,
    TIMING_POLICY,
)
from pipelines.run_event_clustering_panel_generation_v1 import PANEL_COLUMNS, PANEL_FILE_STEMS


RUN_ID = "event_clustering_ic_discovery_v1"
SOURCE_PANEL_ROOT = Path("artifacts/research/event_clustering_research_module_v1/panel_v1")
APPROVED_AUDIT_PATH = Path("docs/research_notes/event_clustering_panel_audit_v1.md")
OUT_DIR = Path("artifacts/research/event_clustering_research_module_v1/ic_discovery_v1")
CLOSE_PATH = Path("data/processed/phase2/nb01_data_foundation/close_prices.parquet")
HORIZONS = (1, 5, 10, 20)
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
    "IC discovery only for audited Event Clustering panels. No panel regeneration, "
    "formula implementation, refinement, validation, governance mutation, production "
    "registration, threshold change, or ML work is performed."
)

EXPECTED_ARTIFACTS = (
    "daily_ic.csv",
    "candidate_ic_summary.csv",
    "candidate_horizon_summary.csv",
    "candidate_rankings.csv",
    "rolling_stability_summary.csv",
    "ic_discovery_manifest.json",
)

LINEAGE_COLUMNS = (
    "candidate_id",
    "candidate_name",
    "mechanism",
    "module_id",
    "spec_id",
    "source_spec_id",
    "research_status",
    "primary_horizon",
    "secondary_horizons",
    "expected_sign",
    "timing_metadata",
    "after_close_policy",
    "scientific_lineage",
    "contamination_metadata",
    "isolated_event_anchor",
    "formula_text",
    "activation_text",
    "scientific_question",
    "expected_evidence",
    "stop_conditions",
    "anchor_comparators",
)

CONTAMINATION_DIAGNOSTICS = (
    "security_vov_20",
    "vol_compression_20",
    "stress_proxy_20",
    "volume_intensity_5",
    "rank_coherence_proxy_20",
    "persistence_proxy_20",
    "static_dispersion_20",
    "dispersion_path_proxy_10",
    "non_hostile_transition_proxy_20",
    "static_event_anchor_20",
    "isolated_event_anchor_20",
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


def _panel_path(panel_root: Path, candidate_id: str) -> Path:
    return panel_root / f"{PANEL_FILE_STEMS[candidate_id]}_signal_panel.parquet"


def _load_panel_manifest(panel_root: Path) -> pd.DataFrame:
    manifest_path = panel_root / "panel_manifest.csv"
    if not manifest_path.exists():
        raise FileNotFoundError(f"missing audited panel manifest: {manifest_path}")
    manifest = pd.read_csv(manifest_path)
    ids = tuple(manifest["candidate_id"].astype(str))
    if ids != IMPLEMENTED_CANDIDATE_IDS:
        raise ValueError(f"Event Clustering panel manifest candidate IDs mismatch: {ids}")
    if manifest["candidate_id"].astype(str).str.startswith(("vov_", "dpath_")).any():
        raise ValueError("foreign candidate appeared in Event Clustering panel manifest")
    required = {
        "candidate_id",
        "panel_file",
        "module_id",
        "row_count",
        "duplicate_key_count",
        "schema_validation_status",
        "lineage_validation_status",
        "registry_validation_status",
        "contamination_metadata_status",
        "activation_neutrality_status",
        "source_spec_id",
    }
    missing = required - set(manifest.columns)
    if missing:
        raise ValueError("Event Clustering panel manifest missing columns: " + ", ".join(sorted(missing)))
    if set(manifest["module_id"].astype(str)) != {MODULE_ID}:
        raise ValueError("Event Clustering panel manifest module_id mismatch")
    if int(manifest["duplicate_key_count"].sum()) != 0:
        raise ValueError("Event Clustering panel manifest reports duplicate keys")
    for column in (
        "schema_validation_status",
        "lineage_validation_status",
        "registry_validation_status",
        "contamination_metadata_status",
        "activation_neutrality_status",
    ):
        if set(manifest[column].astype(str)) != {"PASS"}:
            raise ValueError(f"Event Clustering panel manifest has non-PASS {column}")
    for candidate_id in IMPLEMENTED_CANDIDATE_IDS:
        expected_path = _panel_path(panel_root, candidate_id)
        if not expected_path.exists():
            raise FileNotFoundError(f"missing audited panel: {expected_path}")
    extra_panels = sorted(path.name for path in panel_root.glob("*_signal_panel.parquet"))
    expected_panels = sorted(f"{PANEL_FILE_STEMS[candidate_id]}_signal_panel.parquet" for candidate_id in IMPLEMENTED_CANDIDATE_IDS)
    if extra_panels != expected_panels:
        raise ValueError(f"unexpected Event Clustering panel inventory: {extra_panels}")
    return manifest


def _constant_value(panel_long: pd.DataFrame, candidate_id: str, column: str) -> object:
    if column not in panel_long.columns:
        raise ValueError(f"{candidate_id} missing required metadata column: {column}")
    values = panel_long[column].dropna().astype(str).unique()
    if len(values) != 1:
        raise ValueError(f"{candidate_id} metadata column is not constant: {column}")
    return values[0]


def _lineage_from_panel(panel_long: pd.DataFrame, candidate_id: str) -> dict[str, object]:
    lineage: dict[str, object] = {}
    for column in LINEAGE_COLUMNS:
        if column == "isolated_event_anchor":
            if column not in panel_long.columns:
                raise ValueError(f"{candidate_id} missing required metadata column: {column}")
            non_null_count = int(panel_long[column].notna().sum())
            lineage[column] = f"{column}_present|non_null_count={non_null_count}"
            continue
        lineage[column] = _constant_value(panel_long, candidate_id, column)
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
        raise ValueError(f"Event Clustering panel {path} missing columns: {sorted(missing)}")
    if panel_long[["date", "ticker", "candidate_id"]].duplicated().any():
        raise ValueError(f"Event Clustering panel {path} contains duplicate date/ticker/candidate rows")
    if set(panel_long["candidate_id"].astype(str)) != {candidate_id}:
        raise ValueError(f"Event Clustering panel {path} candidate_id mismatch")
    if panel_long["candidate_id"].astype(str).str.startswith(("vov_", "dpath_")).any():
        raise ValueError(f"foreign candidate appeared in {path}")
    if set(panel_long["module_id"].astype(str)) != {MODULE_ID}:
        raise ValueError(f"Event Clustering panel {path} module_id mismatch")
    if set(panel_long["spec_id"].astype(str)) != {SPEC_ID}:
        raise ValueError(f"Event Clustering panel {path} formula spec_id mismatch")
    if set(panel_long["research_status"].astype(str)) != {RESEARCH_STATUS}:
        raise ValueError(f"Event Clustering panel {path} research_status mismatch")
    if set(panel_long["after_close_policy"].astype(str)) != {TIMING_POLICY}:
        raise ValueError(f"Event Clustering panel {path} after-close policy mismatch")
    if set(panel_long["candidate_version"].astype(str)) != {"v1"}:
        raise ValueError(f"Event Clustering panel {path} candidate_version mismatch")
    for control in CONTAMINATION_CONTROLS:
        if not panel_long["contamination_metadata"].astype(str).str.contains(control, regex=False).all():
            raise ValueError(f"Event Clustering panel {path} missing contamination control: {control}")

    lineage = _lineage_from_panel(panel_long, candidate_id)
    max_diag_corr, max_diag_name = _max_abs_contamination_indicator(panel_long)
    panel = panel_long.pivot(index="date", columns="ticker", values="signal_value")
    panel.index = pd.to_datetime(panel.index)
    panel = panel.sort_index()
    active_rows = int(panel_long["activation_state"].eq("active").sum())
    feature_ready_rows = int(panel_long["warmup_state"].eq("warmup_complete").sum())
    metadata = {
        **lineage,
        "family": FAMILY,
        "panel_row_count": int(len(panel_long)),
        "non_null_signal_count": int(panel_long["signal_value"].notna().sum()),
        "warmup_incomplete_count": int(panel_long["warmup_state"].eq("rolling_warmup").sum()),
        "inactive_row_count": int(panel_long["activation_state"].eq("inactive_neutralized").sum()),
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
        panel, meta = _load_candidate_panel(row["panel_file"], candidate_id)
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
                "mechanism",
                "module_id",
                "spec_id",
                "source_spec_id",
                "family",
                "research_status",
                "primary_horizon",
                "secondary_horizons",
                "expected_sign",
                "after_close_policy",
                "timing_metadata",
                "scientific_lineage",
                "contamination_metadata",
                "isolated_event_anchor",
                "scientific_question",
                "expected_evidence",
                "stop_conditions",
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
                    "mechanism": meta["mechanism"],
                    "module_id": meta["module_id"],
                    "spec_id": meta["spec_id"],
                    "source_spec_id": meta["source_spec_id"],
                    "family": meta["family"],
                    "research_status": meta["research_status"],
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
                    "scientific_lineage": meta["scientific_lineage"],
                    "contamination_metadata": meta["contamination_metadata"],
                    "isolated_event_anchor": meta["isolated_event_anchor"],
                    "scientific_question": meta["scientific_question"],
                    "expected_evidence": meta["expected_evidence"],
                    "stop_conditions": meta["stop_conditions"],
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
            "mechanism",
            "module_id",
            "spec_id",
            "source_spec_id",
            "family",
            "research_status",
            "primary_horizon",
            "secondary_horizons",
            "expected_sign",
            "after_close_policy",
            "timing_metadata",
            "horizon",
            "ic",
            "observation_count",
            "signal_count",
            "target_count",
            "coverage_ratio",
            "scientific_lineage",
            "contamination_metadata",
            "isolated_event_anchor",
            "scientific_question",
            "expected_evidence",
            "stop_conditions",
            "anchor_comparators",
        ]
    ]
    return daily_ic, pd.DataFrame(summary_rows)


def rolling_stability_summary(daily_ic: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for (candidate_id, horizon), group in daily_ic.sort_values("date").groupby(["candidate_id", "horizon"]):
        series = group["ic"]
        base = group.iloc[0]
        row: dict[str, object] = {
            "candidate_id": candidate_id,
            "candidate_name": base["candidate_name"],
            "mechanism": base["mechanism"],
            "family": base["family"],
            "horizon": horizon,
            "scored_date_count": int(series.notna().sum()),
        }
        for window in ROLLING_WINDOWS:
            min_periods = max(20, window // 3)
            rolling_mean = series.rolling(window, min_periods=min_periods).mean()
            rolling_std = series.rolling(window, min_periods=min_periods).std(ddof=0)
            rolling_ir = rolling_mean / rolling_std.replace(0, np.nan)
            rolling_positive = series.gt(0).rolling(window, min_periods=min_periods).mean()
            row[f"rolling_{window}_mean_ic_latest"] = float(rolling_mean.dropna().iloc[-1]) if rolling_mean.notna().any() else np.nan
            row[f"rolling_{window}_mean_ic_min"] = float(rolling_mean.min()) if rolling_mean.notna().any() else np.nan
            row[f"rolling_{window}_mean_ic_max"] = float(rolling_mean.max()) if rolling_mean.notna().any() else np.nan
            row[f"rolling_{window}_ic_ir_latest"] = float(rolling_ir.dropna().iloc[-1]) if rolling_ir.notna().any() else np.nan
            row[f"rolling_{window}_positive_ic_rate_latest"] = (
                float(rolling_positive.dropna().iloc[-1]) if rolling_positive.notna().any() else np.nan
            )
        rows.append(row)
    return pd.DataFrame(rows)


def _horizon_order(horizon: str) -> int:
    return {f"h{value}": idx for idx, value in enumerate(HORIZONS)}[horizon]


def _best_horizon_row(candidate_horizon_summary: pd.DataFrame, candidate_id: str, horizons: tuple[str, ...]) -> pd.Series:
    subset = candidate_horizon_summary[
        candidate_horizon_summary["candidate_id"].eq(candidate_id)
        & candidate_horizon_summary["horizon"].isin(horizons)
    ].copy()
    subset["horizon_order"] = subset["horizon"].map(_horizon_order)
    return subset.sort_values(["mean_ic", "ic_ir", "horizon_order"], ascending=[False, False, True]).iloc[0]


def hypothesis_consistency(candidate_horizon_summary: pd.DataFrame, candidate_id: str) -> str:
    expected = str(
        candidate_horizon_summary.loc[
            candidate_horizon_summary["candidate_id"].eq(candidate_id), "primary_horizon"
        ].iloc[0]
    )
    expected_row = _best_horizon_row(candidate_horizon_summary, candidate_id, (expected,))
    best_any = _best_horizon_row(candidate_horizon_summary, candidate_id, tuple(f"h{horizon}" for horizon in HORIZONS))
    if (
        best_any["horizon"] == expected
        and pd.notna(expected_row["mean_ic"])
        and expected_row["mean_ic"] > 0
        and pd.notna(expected_row["positive_ic_rate"])
        and expected_row["positive_ic_rate"] >= 0.50
    ):
        return "MATCH"
    if (
        pd.notna(expected_row["mean_ic"])
        and expected_row["mean_ic"] > 0
        and pd.notna(expected_row["positive_ic_rate"])
        and expected_row["positive_ic_rate"] >= 0.48
    ) or (pd.notna(best_any["mean_ic"]) and best_any["mean_ic"] > 0):
        return "PARTIAL_MATCH"
    return "MISMATCH"


def classify_candidate(row: pd.Series) -> str:
    if (
        pd.notna(row["expected_primary_mean_ic"])
        and row["expected_primary_mean_ic"] >= ADVANCE_MEAN_IC_MIN
        and pd.notna(row["expected_primary_ic_ir"])
        and row["expected_primary_ic_ir"] >= ADVANCE_IC_IR_MIN
        and pd.notna(row["expected_primary_positive_ic_rate"])
        and row["expected_primary_positive_ic_rate"] >= ADVANCE_POSITIVE_IC_RATE_MIN
        and pd.notna(row["expected_primary_coverage_ratio"])
        and row["expected_primary_coverage_ratio"] >= ADVANCE_COVERAGE_RATIO_MIN
    ):
        return "ADVANCE_TO_RESEARCH_REVIEW"
    if pd.notna(row["activation_rate"]) and row["activation_rate"] < PARK_ACTIVATION_RATE_MIN:
        return "PARK"
    if (
        pd.notna(row["expected_primary_mean_ic"])
        and row["expected_primary_mean_ic"] > WATCH_MEAN_IC_MIN
        and pd.notna(row["expected_primary_positive_ic_rate"])
        and row["expected_primary_positive_ic_rate"] >= WATCH_POSITIVE_IC_RATE_MIN
        and pd.notna(row["expected_primary_coverage_ratio"])
        and row["expected_primary_coverage_ratio"] >= WATCH_COVERAGE_RATIO_MIN
    ):
        return "WATCH"
    if pd.notna(row["best_any_mean_ic"]) and row["best_any_mean_ic"] > WATCH_MEAN_IC_MIN:
        return "PARK"
    return "REJECT"


def candidate_rankings(candidate_horizon_summary: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for candidate_id in IMPLEMENTED_CANDIDATE_IDS:
        expected = str(
            candidate_horizon_summary.loc[
                candidate_horizon_summary["candidate_id"].eq(candidate_id), "primary_horizon"
            ].iloc[0]
        )
        expected_row = _best_horizon_row(candidate_horizon_summary, candidate_id, (expected,))
        best_any = _best_horizon_row(candidate_horizon_summary, candidate_id, tuple(f"h{h}" for h in HORIZONS))
        row = {
            "candidate_id": candidate_id,
            "candidate_name": expected_row["candidate_name"],
            "mechanism": expected_row["mechanism"],
            "module_id": expected_row["module_id"],
            "spec_id": expected_row["spec_id"],
            "source_spec_id": expected_row["source_spec_id"],
            "family": expected_row["family"],
            "expected_primary_horizon": expected,
            "observed_primary_horizon": best_any["horizon"],
            "horizon_consistency": "MATCH" if best_any["horizon"] == expected else "MISMATCH",
            "hypothesis_consistency": hypothesis_consistency(candidate_horizon_summary, candidate_id),
            "expected_primary_mean_ic": expected_row["mean_ic"],
            "expected_primary_ic_ir": expected_row["ic_ir"],
            "expected_primary_positive_ic_rate": expected_row["positive_ic_rate"],
            "expected_primary_coverage_ratio": expected_row["coverage_ratio"],
            "expected_primary_observation_count": expected_row["observation_count"],
            "best_any_horizon": best_any["horizon"],
            "best_any_mean_ic": best_any["mean_ic"],
            "best_any_ic_ir": best_any["ic_ir"],
            "best_any_positive_ic_rate": best_any["positive_ic_rate"],
            "activation_rate": expected_row["activation_rate"],
            "turnover_proxy": expected_row["turnover_proxy"],
            "max_abs_internal_diagnostic_corr": expected_row["max_abs_internal_diagnostic_corr"],
            "max_internal_diagnostic_corr_name": expected_row["max_internal_diagnostic_corr_name"],
            "scientific_lineage": expected_row["scientific_lineage"],
            "contamination_metadata": expected_row["contamination_metadata"],
            "isolated_event_anchor": expected_row["isolated_event_anchor"],
            "scientific_question": expected_row["scientific_question"],
            "expected_evidence": expected_row["expected_evidence"],
            "stop_conditions": expected_row["stop_conditions"],
            "anchor_comparators": expected_row["anchor_comparators"],
        }
        row["recommendation"] = classify_candidate(pd.Series(row))
        rows.append(row)
    rankings = pd.DataFrame(rows)
    rankings["rank"] = rankings["expected_primary_mean_ic"].rank(method="first", ascending=False).astype(int)
    return rankings.sort_values("rank")


def candidate_ic_summary(candidate_horizon_summary: pd.DataFrame, rankings: pd.DataFrame) -> pd.DataFrame:
    base = (
        candidate_horizon_summary.groupby(
            [
                "candidate_id",
                "candidate_name",
                "mechanism",
                "module_id",
                "spec_id",
                "source_spec_id",
                "family",
                "primary_horizon",
                "secondary_horizons",
                "expected_sign",
            ],
            as_index=False,
        )
        .agg(
            mean_ic_across_horizons=("mean_ic", "mean"),
            best_mean_ic=("mean_ic", "max"),
            mean_ic_ir_across_horizons=("ic_ir", "mean"),
            mean_positive_ic_rate=("positive_ic_rate", "mean"),
            total_observation_count=("observation_count", "sum"),
            panel_row_count=("panel_row_count", "max"),
            non_null_signal_count=("non_null_signal_count", "max"),
            warmup_incomplete_count=("warmup_incomplete_count", "max"),
            inactive_row_count=("inactive_row_count", "max"),
            active_row_count=("active_row_count", "max"),
            activation_rate=("activation_rate", "max"),
            turnover_proxy=("turnover_proxy", "max"),
            max_abs_internal_diagnostic_corr=("max_abs_internal_diagnostic_corr", "max"),
        )
    )
    ranking_fields = rankings[
        [
            "candidate_id",
            "rank",
            "expected_primary_horizon",
            "observed_primary_horizon",
            "horizon_consistency",
            "hypothesis_consistency",
            "expected_primary_mean_ic",
            "expected_primary_ic_ir",
            "expected_primary_positive_ic_rate",
            "best_any_horizon",
            "best_any_mean_ic",
            "recommendation",
        ]
    ]
    return base.merge(ranking_fields, on="candidate_id", how="left").sort_values("rank")


def discovery_classification(rankings: pd.DataFrame) -> str:
    recommendations = set(rankings["recommendation"].astype(str))
    if recommendations:
        return "IC_DISCOVERY_COMPLETE"
    return "IC_DISCOVERY_INCOMPLETE"


def _manifest_payload(
    *,
    panel_root: Path,
    close_path: Path,
    out_dir: Path,
    rankings: pd.DataFrame,
    candidate_horizon: pd.DataFrame,
) -> dict[str, object]:
    panel_checksums = {
        _panel_path(panel_root, candidate_id).name: _sha256_file(_panel_path(panel_root, candidate_id))
        for candidate_id in IMPLEMENTED_CANDIDATE_IDS
    }
    output_checksums = {name: _sha256_file(out_dir / name) for name in EXPECTED_ARTIFACTS if name != "ic_discovery_manifest.json"}
    return {
        "run_id": RUN_ID,
        "module_id": MODULE_ID,
        "source_panel_root": str(panel_root),
        "approved_audit": str(APPROVED_AUDIT_PATH),
        "close_path": str(close_path),
        "classification": discovery_classification(rankings),
        "research_only": True,
        "research_only_guardrail": RESEARCH_ONLY_GUARDRAIL,
        "approved_candidate_count": len(IMPLEMENTED_CANDIDATE_IDS),
        "approved_candidate_ids": list(IMPLEMENTED_CANDIDATE_IDS),
        "horizons": [f"h{horizon}" for horizon in HORIZONS],
        "rolling_windows": list(ROLLING_WINDOWS),
        "minimum_daily_observations": MIN_DAILY_OBSERVATIONS,
        "timing_policy": TIMING_POLICY,
        "classification_thresholds": CLASSIFICATION_THRESHOLDS,
        "recommendation_vocabulary": ["ADVANCE_TO_RESEARCH_REVIEW", "WATCH", "PARK", "REJECT"],
        "candidate_recommendations": rankings[["candidate_id", "recommendation"]].to_dict(orient="records"),
        "best_by_horizon": {
            horizon: candidate_horizon[candidate_horizon["horizon"].eq(horizon)]
            .sort_values(["mean_ic", "ic_ir"], ascending=False)
            .head(1)[["candidate_id", "mean_ic", "ic_ir", "positive_ic_rate"]]
            .to_dict(orient="records")
            for horizon in [f"h{value}" for value in HORIZONS]
        },
        "input_lineage_checksums": {
            "panel_manifest_sha256": _sha256_file(panel_root / "panel_manifest.csv"),
            "panel_generation_manifest_sha256": _sha256_file(panel_root / "panel_generation_manifest.json"),
            "approved_audit_sha256": _sha256_file(APPROVED_AUDIT_PATH),
            "approved_panel_parquet_sha256": panel_checksums,
            "close_source_sha256": _sha256_file(close_path),
        },
        "output_checksums": output_checksums,
        "outputs": {name.removesuffix(".csv"): str(out_dir / name) for name in EXPECTED_ARTIFACTS},
        "panel_audit_approved_before_ic": True,
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
        "created_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
    }


def run_ic_discovery(
    *,
    panel_root: Path = SOURCE_PANEL_ROOT,
    close_path: Path = CLOSE_PATH,
    out_dir: Path = OUT_DIR,
) -> dict[str, pd.DataFrame]:
    _ensure_out_dir(out_dir)
    if not APPROVED_AUDIT_PATH.exists():
        raise FileNotFoundError(f"missing approved panel audit: {APPROVED_AUDIT_PATH}")
    manifest = _load_panel_manifest(panel_root)
    panels, metadata = _load_candidate_panels(manifest)
    close = _load_close(close_path)
    daily_ic, candidate_horizon = score_candidate_panels(panels, close, metadata)
    rolling = rolling_stability_summary(daily_ic)
    rankings = candidate_rankings(candidate_horizon)
    candidate_summary = candidate_ic_summary(candidate_horizon, rankings)

    daily_ic.to_csv(out_dir / "daily_ic.csv", index=False)
    candidate_horizon.to_csv(out_dir / "candidate_horizon_summary.csv", index=False)
    rankings.to_csv(out_dir / "candidate_rankings.csv", index=False)
    candidate_summary.to_csv(out_dir / "candidate_ic_summary.csv", index=False)
    rolling.to_csv(out_dir / "rolling_stability_summary.csv", index=False)
    manifest_payload = _manifest_payload(
        panel_root=panel_root,
        close_path=close_path,
        out_dir=out_dir,
        rankings=rankings,
        candidate_horizon=candidate_horizon,
    )
    (out_dir / "ic_discovery_manifest.json").write_text(
        json.dumps(manifest_payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return {
        "daily_ic": daily_ic,
        "candidate_horizon_summary": candidate_horizon,
        "candidate_ic_summary": candidate_summary,
        "candidate_rankings": rankings,
        "rolling_stability_summary": rolling,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Event Clustering research-only IC discovery.")
    parser.add_argument("--panel-root", type=Path, default=SOURCE_PANEL_ROOT)
    parser.add_argument("--close-path", type=Path, default=CLOSE_PATH)
    parser.add_argument("--out-dir", type=Path, default=OUT_DIR)
    args = parser.parse_args()
    outputs = run_ic_discovery(panel_root=args.panel_root, close_path=args.close_path, out_dir=args.out_dir)
    rankings = outputs["candidate_rankings"]
    print(f"Wrote Event Clustering IC discovery artifacts for {len(IMPLEMENTED_CANDIDATE_IDS)} candidates to {args.out_dir}")
    print(
        rankings[
            [
                "rank",
                "candidate_id",
                "expected_primary_horizon",
                "observed_primary_horizon",
                "expected_primary_mean_ic",
                "expected_primary_ic_ir",
                "expected_primary_positive_ic_rate",
                "hypothesis_consistency",
                "recommendation",
            ]
        ].to_string(index=False)
    )
    print(RESEARCH_ONLY_GUARDRAIL)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
