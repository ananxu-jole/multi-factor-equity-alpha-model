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

from pipelines.ohlcv_volatility_of_volatility_refinement_v1 import (
    BLOCKED_CANDIDATE_IDS,
    BLOCKED_FAMILY_PREFIXES,
    FAMILY,
    MODULE_ID,
)
from pipelines.run_ohlcv_volatility_of_volatility_refinement_panel_generation_v1 import (
    PANEL_COLUMNS,
    TIMING_POLICY,
    validate_refinement_panel_artifacts,
)


RUN_ID = "ohlcv_volatility_of_volatility_validation_runner_and_artifact_contract_v1"
VALIDATION_DESIGN_ID = "ohlcv_volatility_of_volatility_validation_design_review_v1"
READINESS_ID = "ohlcv_volatility_of_volatility_validation_readiness_after_integrity_hardening_v1"
SOURCE_PANEL_ROOT = Path("artifacts/research/ohlcv_volatility_of_volatility_refinement_v1/panel_v1")
OUT_DIR = Path("artifacts/research/ohlcv_volatility_of_volatility_refinement_v1/validation_design_v1")
CLOSE_PATH = Path("data/processed/phase2/nb01_data_foundation/close_prices.parquet")

VALIDATION_CANDIDATE_IDS = ("vov_03_ref_strict_chop", "vov_01_ref_smoothed_calm")
BASELINE_COMPARATOR_IDS = ("vov_03_ref_anchor", "vov_01_ref_anchor")
VALIDATION_SCOPE_IDS = (
    "vov_03_ref_strict_chop",
    "vov_01_ref_smoothed_calm",
    "vov_03_ref_anchor",
    "vov_01_ref_anchor",
)
EXCLUDED_CANDIDATE_IDS = (
    "vov_01_ref_longer_memory",
    "vov_01_ref_strict_calm",
    "vov_03_ref_longer_chop",
    "vov_03_ref_extension_controlled",
    "vov_02",
    "vov_04",
    "vov_05",
    "dpath_*",
    "ecluster_*",
)
ANCHOR_BY_CANDIDATE = {
    "vov_03_ref_strict_chop": "vov_03_ref_anchor",
    "vov_01_ref_smoothed_calm": "vov_01_ref_anchor",
}
PRIMARY_HORIZON_BY_CANDIDATE = {
    "vov_03_ref_strict_chop": "h10",
    "vov_01_ref_smoothed_calm": "h20",
}
SECONDARY_HORIZONS_BY_CANDIDATE = {
    "vov_03_ref_strict_chop": ("h5", "h20"),
    "vov_01_ref_smoothed_calm": ("h5", "h10"),
}
HORIZONS = (1, 5, 10, 20)
ROLLING_WINDOWS = (63, 126, 252)
MIN_DAILY_OBSERVATIONS = 25
VALIDATION_THRESHOLDS = {
    "minimum_daily_observations": MIN_DAILY_OBSERVATIONS,
    "rolling_windows": list(ROLLING_WINDOWS),
    "primary_horizon_required_positive_mean_ic": True,
    "anchor_delta_required_metric": "mean_ic_or_ic_ir_nonnegative",
    "baseline_comparators_are_not_validation_candidates": True,
}
REFERENCE_FAMILIES = (
    "volatility_compression",
    "hostile_stress_repair",
    "persistence_rank_stability",
    "rank_coherence",
    "plain_reversal",
    "volume_shock_reversal",
    "vov_05_like_behavior",
)
RESEARCH_GUARDRAIL = (
    "Validation runner infrastructure for two approved bounded VoV refinement candidates. "
    "No formula changes, panel regeneration, historical IC artifact recomputation, governance "
    "mutation, production registration, threshold change, ML work, or candidate promotion is performed."
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


def _blocked_candidate_present(values: pd.Series | list[object] | tuple[object, ...]) -> bool:
    for value in pd.Series(values).dropna().astype(str):
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
        raise ValueError("VoV refinement panel manifest missing columns: " + ", ".join(sorted(missing)))
    if _blocked_candidate_present(manifest["candidate_id"]):
        raise ValueError("blocked candidate appeared in VoV refinement panel manifest")
    if set(manifest["timing_policy"].astype(str)) != {TIMING_POLICY}:
        raise ValueError("VoV refinement panel manifest timing policy mismatch")
    if int(manifest["duplicate_key_count"].sum()) != 0:
        raise ValueError("VoV refinement panel manifest reports duplicate keys")
    if set(manifest["schema_status"].astype(str)) != {"PASS"}:
        raise ValueError("VoV refinement panel manifest has non-PASS schema status")
    if set(manifest["blocked_candidate_check"].astype(str)) != {"PASS"}:
        raise ValueError("VoV refinement panel manifest has non-PASS blocked candidate check")

    manifest_ids = set(manifest["candidate_id"].astype(str))
    missing_scope = set(VALIDATION_SCOPE_IDS) - manifest_ids
    if missing_scope:
        raise ValueError("approved validation scope is missing panel rows: " + ", ".join(sorted(missing_scope)))
    return manifest.loc[manifest["candidate_id"].astype(str).isin(VALIDATION_SCOPE_IDS)].copy()


def _load_candidate_panel(path: str | Path, candidate_id: str) -> tuple[pd.DataFrame, dict[str, object], pd.DataFrame]:
    panel_long = pd.read_parquet(path)
    missing = set(PANEL_COLUMNS) - set(panel_long.columns)
    if missing:
        raise ValueError(f"validation panel {path} missing columns: {sorted(missing)}")
    if panel_long[["date", "ticker", "candidate_id"]].duplicated().any():
        raise ValueError(f"validation panel {path} contains duplicate date/ticker/candidate rows")
    if set(panel_long["candidate_id"].astype(str)) != {candidate_id}:
        raise ValueError(f"validation panel {path} candidate_id mismatch")
    if candidate_id not in VALIDATION_SCOPE_IDS:
        raise ValueError(f"candidate is outside validation scope: {candidate_id}")
    if _blocked_candidate_present(panel_long["candidate_id"]):
        raise ValueError(f"blocked candidate appeared in {path}")
    if set(panel_long["module_id"].astype(str)) != {MODULE_ID}:
        raise ValueError(f"validation panel {path} module_id mismatch")
    if set(panel_long["family"].astype(str)) != {FAMILY}:
        raise ValueError(f"validation panel {path} family mismatch")
    if set(panel_long["timing_policy"].astype(str)) != {TIMING_POLICY}:
        raise ValueError(f"validation panel {path} timing policy mismatch")

    metadata = {
        "candidate_id": candidate_id,
        "validation_role": "validation_candidate"
        if candidate_id in VALIDATION_CANDIDATE_IDS
        else "baseline_comparator",
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
        "active_row_count": int(panel_long["is_active"].astype(bool).sum()),
        "inactive_row_count": int((~panel_long["is_active"].astype(bool)).sum()),
        "warmup_incomplete_count": int((~panel_long["feature_warmup_complete"].astype(bool)).sum()),
        "missing_signal_count": int(panel_long["signal_value"].isna().sum()),
        "date_count": int(pd.to_datetime(panel_long["date"]).nunique()),
        "ticker_count": int(panel_long["ticker"].nunique()),
    }
    panel = panel_long.pivot(index="date", columns="ticker", values="signal_value")
    panel.index = pd.to_datetime(panel.index)
    return panel.sort_index(), metadata, panel_long


def _load_candidate_panels(
    manifest: pd.DataFrame,
) -> tuple[dict[str, pd.DataFrame], dict[str, dict[str, object]], dict[str, pd.DataFrame]]:
    panels: dict[str, pd.DataFrame] = {}
    metadata: dict[str, dict[str, object]] = {}
    long_panels: dict[str, pd.DataFrame] = {}
    for row in manifest.to_dict(orient="records"):
        candidate_id = str(row["candidate_id"])
        panel, meta, panel_long = _load_candidate_panel(row["panel_path"], candidate_id)
        panels[candidate_id] = panel
        metadata[candidate_id] = meta
        long_panels[candidate_id] = panel_long
    if set(panels) != set(VALIDATION_SCOPE_IDS):
        raise ValueError("loaded validation scope does not match approved candidates and comparators")
    return panels, metadata, long_panels


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
        ic = np.nan
        if observation_count >= MIN_DAILY_OBSERVATIONS:
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


def score_validation_scope(
    panels: dict[str, pd.DataFrame],
    close: pd.DataFrame,
    metadata: dict[str, dict[str, object]],
) -> tuple[pd.DataFrame, pd.DataFrame]:
    daily_rows: list[pd.DataFrame] = []
    summary_rows: list[dict[str, object]] = []
    for horizon in HORIZONS:
        fwd = _forward_returns(close, horizon)
        for candidate_id in VALIDATION_SCOPE_IDS:
            panel = panels[candidate_id].reindex(index=close.index, columns=close.columns)
            daily = _daily_ic_frame(panel, fwd, horizon)
            meta = metadata[candidate_id]
            for key, value in meta.items():
                daily[key] = value
            daily = daily[
                [
                    "date",
                    "candidate_id",
                    "validation_role",
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
            ic_std = float(valid_ic.std(ddof=0)) if len(valid_ic) > 1 else np.nan
            summary_rows.append(
                {
                    "candidate_id": candidate_id,
                    "validation_role": meta["validation_role"],
                    "source_spec_id": meta["source_spec_id"],
                    "parent_candidate_id": meta["parent_candidate_id"],
                    "module_id": meta["module_id"],
                    "refinement_family": meta["refinement_family"],
                    "family": meta["family"],
                    "primary_horizon": meta["primary_horizon"],
                    "secondary_horizons": meta["secondary_horizons"],
                    "horizon": f"h{horizon}",
                    "mean_ic": mean_ic,
                    "median_ic": float(valid_ic.median()) if len(valid_ic) else np.nan,
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
    return pd.concat(daily_rows, ignore_index=True), pd.DataFrame(summary_rows)


def rolling_validation_diagnostics(daily_ic: pd.DataFrame) -> pd.DataFrame:
    rows: list[pd.DataFrame] = []
    for (candidate_id, horizon), group in daily_ic.sort_values("date").groupby(["candidate_id", "horizon"]):
        out = group[
            [
                "date",
                "candidate_id",
                "validation_role",
                "source_spec_id",
                "parent_candidate_id",
                "refinement_family",
                "family",
                "horizon",
            ]
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


def anchor_comparison(candidate_horizon_scores: pd.DataFrame) -> pd.DataFrame:
    anchor_scores = candidate_horizon_scores[
        candidate_horizon_scores["candidate_id"].isin(BASELINE_COMPARATOR_IDS)
    ][["candidate_id", "refinement_family", "horizon", "mean_ic", "ic_ir", "positive_ic_rate"]].rename(
        columns={
            "candidate_id": "anchor_candidate_id",
            "mean_ic": "anchor_mean_ic",
            "ic_ir": "anchor_ic_ir",
            "positive_ic_rate": "anchor_positive_ic_rate",
        }
    )
    candidate_scores = candidate_horizon_scores[
        candidate_horizon_scores["candidate_id"].isin(VALIDATION_CANDIDATE_IDS)
    ].copy()
    out = candidate_scores.merge(anchor_scores, on=["refinement_family", "horizon"], how="left")
    out["mean_ic_delta_vs_anchor"] = out["mean_ic"] - out["anchor_mean_ic"]
    out["ic_ir_delta_vs_anchor"] = out["ic_ir"] - out["anchor_ic_ir"]
    out["positive_ic_rate_delta_vs_anchor"] = out["positive_ic_rate"] - out["anchor_positive_ic_rate"]
    out["is_primary_horizon"] = out.apply(
        lambda row: row["horizon"] == PRIMARY_HORIZON_BY_CANDIDATE[str(row["candidate_id"])],
        axis=1,
    )
    return out


def coverage_turnover_diagnostics(
    panels: dict[str, pd.DataFrame],
    metadata: dict[str, dict[str, object]],
) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for candidate_id in VALIDATION_SCOPE_IDS:
        panel = panels[candidate_id]
        ranks = panel.rank(axis=1, pct=True)
        turnover = ranks.diff().abs().mean(axis=1, skipna=True)
        meta = metadata[candidate_id]
        rows.append(
            {
                "candidate_id": candidate_id,
                "validation_role": meta["validation_role"],
                "date_count": meta["date_count"],
                "ticker_count": meta["ticker_count"],
                "panel_row_count": meta["panel_row_count"],
                "non_null_signal_count": meta["non_null_signal_count"],
                "active_row_count": meta["active_row_count"],
                "inactive_row_count": meta["inactive_row_count"],
                "warmup_incomplete_count": meta["warmup_incomplete_count"],
                "missing_signal_count": meta["missing_signal_count"],
                "active_coverage_ratio": meta["active_row_count"] / meta["panel_row_count"]
                if meta["panel_row_count"]
                else np.nan,
                "non_null_signal_ratio": meta["non_null_signal_count"] / meta["panel_row_count"]
                if meta["panel_row_count"]
                else np.nan,
                "mean_rank_turnover_proxy": float(turnover.mean()) if turnover.notna().any() else np.nan,
                "median_rank_turnover_proxy": float(turnover.median()) if turnover.notna().any() else np.nan,
            }
        )
    return pd.DataFrame(rows)


def stability_window_summary(daily_ic: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    ordered_dates = pd.Index(sorted(pd.to_datetime(daily_ic["date"]).unique()))
    if len(ordered_dates) == 0:
        return pd.DataFrame()
    midpoint = len(ordered_dates) // 2
    windows = {
        "full_sample": ordered_dates,
        "first_half": ordered_dates[:midpoint],
        "second_half": ordered_dates[midpoint:],
        "recent_252": ordered_dates[-252:],
    }
    daily = daily_ic.copy()
    daily["date"] = pd.to_datetime(daily["date"])
    for (candidate_id, horizon), group in daily.groupby(["candidate_id", "horizon"]):
        for window_name, dates in windows.items():
            part = group[group["date"].isin(dates)]
            valid = part["ic"].dropna()
            rows.append(
                {
                    "candidate_id": candidate_id,
                    "horizon": horizon,
                    "window": window_name,
                    "date_count": int(len(part)),
                    "scored_date_count": int(len(valid)),
                    "mean_ic": float(valid.mean()) if len(valid) else np.nan,
                    "positive_ic_rate": float((valid > 0).mean()) if len(valid) else np.nan,
                    "minimum_ic": float(valid.min()) if len(valid) else np.nan,
                    "maximum_ic": float(valid.max()) if len(valid) else np.nan,
                }
            )
    return pd.DataFrame(rows)


def contamination_placeholders() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "candidate_id": candidate_id,
                "reference_family": reference,
                "check_status": "PLACEHOLDER_REFERENCE_NOT_PROVIDED",
                "correlation": np.nan,
                "coactivation_rate": np.nan,
                "blocking_issue": False,
            }
            for candidate_id in VALIDATION_CANDIDATE_IDS
            for reference in REFERENCE_FAMILIES
        ]
    )


def validation_decision_inputs(
    candidate_horizon_scores: pd.DataFrame,
    anchor_delta: pd.DataFrame,
    coverage_turnover: pd.DataFrame,
) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for candidate_id in VALIDATION_CANDIDATE_IDS:
        primary = PRIMARY_HORIZON_BY_CANDIDATE[candidate_id]
        score = candidate_horizon_scores[
            candidate_horizon_scores["candidate_id"].eq(candidate_id)
            & candidate_horizon_scores["horizon"].eq(primary)
        ].iloc[0]
        anchor = anchor_delta[
            anchor_delta["candidate_id"].eq(candidate_id) & anchor_delta["horizon"].eq(primary)
        ].iloc[0]
        coverage = coverage_turnover[coverage_turnover["candidate_id"].eq(candidate_id)].iloc[0]
        rows.append(
            {
                "candidate_id": candidate_id,
                "validation_role": "validation_candidate",
                "primary_horizon": primary,
                "secondary_horizons": "|".join(SECONDARY_HORIZONS_BY_CANDIDATE[candidate_id]),
                "anchor_candidate_id": ANCHOR_BY_CANDIDATE[candidate_id],
                "primary_mean_ic": score["mean_ic"],
                "primary_ic_ir": score["ic_ir"],
                "primary_positive_ic_rate": score["positive_ic_rate"],
                "primary_coverage_ratio": score["coverage_ratio"],
                "primary_mean_ic_delta_vs_anchor": anchor["mean_ic_delta_vs_anchor"],
                "primary_ic_ir_delta_vs_anchor": anchor["ic_ir_delta_vs_anchor"],
                "active_coverage_ratio": coverage["active_coverage_ratio"],
                "mean_rank_turnover_proxy": coverage["mean_rank_turnover_proxy"],
                "contamination_checks_status": "PLACEHOLDER_REFERENCE_NOT_PROVIDED",
                "validation_decision": "PENDING_VALIDATION_REVIEW",
            }
        )
    return pd.DataFrame(rows)


def _manifest_payload(
    *,
    panel_root: Path,
    close_path: Path,
    out_dir: Path,
    validate_only: bool,
    outputs: dict[str, str] | None = None,
) -> dict[str, object]:
    return {
        "run_id": RUN_ID,
        "module_id": MODULE_ID,
        "validation_design_id": VALIDATION_DESIGN_ID,
        "readiness_note_id": READINESS_ID,
        "artifact_root": str(out_dir),
        "source_panel_root": str(panel_root),
        "close_path": str(close_path),
        "validation_candidate_ids": list(VALIDATION_CANDIDATE_IDS),
        "baseline_comparator_ids": list(BASELINE_COMPARATOR_IDS),
        "validation_scope_ids": list(VALIDATION_SCOPE_IDS),
        "excluded_candidate_ids": list(EXCLUDED_CANDIDATE_IDS),
        "anchor_by_candidate": ANCHOR_BY_CANDIDATE,
        "primary_horizon_by_candidate": PRIMARY_HORIZON_BY_CANDIDATE,
        "secondary_horizons_by_candidate": {
            key: list(value) for key, value in SECONDARY_HORIZONS_BY_CANDIDATE.items()
        },
        "horizons": [f"h{horizon}" for horizon in HORIZONS],
        "rolling_windows": list(ROLLING_WINDOWS),
        "timing_policy": TIMING_POLICY,
        "validation_thresholds": VALIDATION_THRESHOLDS,
        "input_lineage_checksums": {
            "panel_manifest_sha256": _sha256_file(panel_root / "panel_manifest.csv"),
            "close_source_sha256": _sha256_file(close_path),
        },
        "research_guardrail": RESEARCH_GUARDRAIL,
        "created_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "validate_only": validate_only,
        "validation_executed": not validate_only,
        "panel_validation_executed": True,
        "panel_generation_executed": False,
        "historical_ic_artifacts_recomputed": False,
        "approved_panels_modified": False,
        "formulas_modified": False,
        "watch_or_park_candidates_included": False,
        "blocked_candidates_used": False,
        "baseline_comparators_promoted": False,
        "governance_modified": False,
        "production_registration": False,
        "thresholds_modified": False,
        "ml_integration": False,
        "outputs": outputs or {},
    }


def run_validation(
    *,
    panel_root: Path = SOURCE_PANEL_ROOT,
    close_path: Path = CLOSE_PATH,
    out_dir: Path = OUT_DIR,
    validate_only: bool = False,
) -> dict[str, pd.DataFrame]:
    manifest = _load_panel_manifest(panel_root)
    panels, metadata, _ = _load_candidate_panels(manifest)
    if validate_only:
        return {}

    _ensure_out_dir(out_dir)
    close = _load_close(close_path)
    daily_ic, candidate_horizon = score_validation_scope(panels, close, metadata)
    rolling = rolling_validation_diagnostics(daily_ic)
    anchor_delta = anchor_comparison(candidate_horizon)
    coverage_turnover = coverage_turnover_diagnostics(panels, metadata)
    stability = stability_window_summary(daily_ic)
    contamination = contamination_placeholders()
    decisions = validation_decision_inputs(candidate_horizon, anchor_delta, coverage_turnover)

    outputs = {
        "daily_validation_ic": str(out_dir / "daily_validation_ic.csv"),
        "candidate_horizon_validation_scores": str(out_dir / "candidate_horizon_validation_scores.csv"),
        "rolling_validation_diagnostics": str(out_dir / "rolling_validation_diagnostics.csv"),
        "anchor_comparison": str(out_dir / "anchor_comparison.csv"),
        "coverage_turnover_diagnostics": str(out_dir / "coverage_turnover_diagnostics.csv"),
        "contamination_correlation_matrix": str(out_dir / "contamination_correlation_matrix.csv"),
        "contamination_overlap_summary": str(out_dir / "contamination_overlap_summary.csv"),
        "stability_window_summary": str(out_dir / "stability_window_summary.csv"),
        "validation_decision_inputs": str(out_dir / "validation_decision_inputs.csv"),
        "approved_panel_manifest_copy": str(out_dir / "approved_panel_manifest_copy.csv"),
        "reference_manifest": str(out_dir / "reference_manifest.csv"),
        "validation_manifest": str(out_dir / "validation_manifest.json"),
    }

    daily_ic.to_csv(out_dir / "daily_validation_ic.csv", index=False)
    candidate_horizon.to_csv(out_dir / "candidate_horizon_validation_scores.csv", index=False)
    rolling.to_csv(out_dir / "rolling_validation_diagnostics.csv", index=False)
    anchor_delta.to_csv(out_dir / "anchor_comparison.csv", index=False)
    coverage_turnover.to_csv(out_dir / "coverage_turnover_diagnostics.csv", index=False)
    contamination.to_csv(out_dir / "contamination_correlation_matrix.csv", index=False)
    contamination.to_csv(out_dir / "contamination_overlap_summary.csv", index=False)
    stability.to_csv(out_dir / "stability_window_summary.csv", index=False)
    decisions.to_csv(out_dir / "validation_decision_inputs.csv", index=False)
    manifest.to_csv(out_dir / "approved_panel_manifest_copy.csv", index=False)
    pd.DataFrame(
        [{"reference_family": reference, "status": "PLACEHOLDER_REFERENCE_NOT_PROVIDED"} for reference in REFERENCE_FAMILIES]
    ).to_csv(out_dir / "reference_manifest.csv", index=False)
    (out_dir / "validation_manifest.json").write_text(
        json.dumps(
            _manifest_payload(
                panel_root=panel_root,
                close_path=close_path,
                out_dir=out_dir,
                validate_only=False,
                outputs=outputs,
            ),
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    return {
        "daily_validation_ic": daily_ic,
        "candidate_horizon_validation_scores": candidate_horizon,
        "rolling_validation_diagnostics": rolling,
        "anchor_comparison": anchor_delta,
        "coverage_turnover_diagnostics": coverage_turnover,
        "contamination_correlation_matrix": contamination,
        "contamination_overlap_summary": contamination,
        "stability_window_summary": stability,
        "validation_decision_inputs": decisions,
    }


def write_validate_only_manifest(
    *,
    panel_root: Path = SOURCE_PANEL_ROOT,
    close_path: Path = CLOSE_PATH,
    out_dir: Path = OUT_DIR,
) -> None:
    _load_panel_manifest(panel_root)
    _ensure_out_dir(out_dir)
    (out_dir / "validation_manifest.json").write_text(
        json.dumps(
            _manifest_payload(panel_root=panel_root, close_path=close_path, out_dir=out_dir, validate_only=True),
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Run VoV validation infrastructure for approved candidates only.")
    parser.add_argument("--panel-root", type=Path, default=SOURCE_PANEL_ROOT)
    parser.add_argument("--close-path", type=Path, default=CLOSE_PATH)
    parser.add_argument("--out-dir", type=Path, default=OUT_DIR)
    parser.add_argument("--validate-only", action="store_true", help="Validate inputs and write only manifest metadata.")
    parser.add_argument("--dry-run", action="store_true", help="Alias for --validate-only.")
    args = parser.parse_args()

    if args.validate_only or args.dry_run:
        write_validate_only_manifest(panel_root=args.panel_root, close_path=args.close_path, out_dir=args.out_dir)
    else:
        run_validation(panel_root=args.panel_root, close_path=args.close_path, out_dir=args.out_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
