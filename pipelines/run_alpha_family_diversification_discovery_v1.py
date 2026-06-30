from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
try:
    from pipelines.utils.registry_validation import validate_registry_df, RegistryValidationError
except Exception:
    # When the runner is executed as a script (python pipelines/run_*.py) the
    # package import path may not resolve. Add repository root to sys.path and
    # retry.
    import sys

    ROOT = Path(__file__).resolve().parent.parent
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    from pipelines.utils.registry_validation import validate_registry_df, RegistryValidationError

RUN_ID = "alpha_family_diversification_discovery_v1"
OUT_DIR = Path("artifacts/research") / RUN_ID
CANDIDATE_INVENTORY_DIR = OUT_DIR / "candidate_inventory"
DISCOVERY_SUMMARY_DIR = OUT_DIR / "discovery_summary"
DIAGNOSTICS_DIR = OUT_DIR / "diagnostics"
REDUNDANCY_SCREENING_DIR = OUT_DIR / "redundancy_screening"
GOVERNANCE_REVIEW_DIR = OUT_DIR / "governance_review"
CANDIDATE_PANELS_DIR = OUT_DIR / "candidate_panels"

NOTE_PATH = Path("docs/research_notes/alpha_family_diversification_framework_implementation_v1.md")
SOURCE_PANEL_DIR = Path("artifacts/panels/signals")
PANEL_GENERATION_LOOKBACK_ROWS = 504
STATISTICAL_SCREENING_LOOKBACK_ROWS = 252

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

RESEARCH_ONLY_GUARDRAIL = (
    "This is a research-only alpha-family diversification discovery framework scaffold. "
    "It does not register production candidates, mutate survivor/watchlist state, change "
    "validation thresholds, alter governance, or route anything into portfolio, ML, or "
    "optimization workflows."
)

CANDIDATES: list[dict[str, str]] = [
    {
        "candidate_id": "dispersion_expansion_transition_01",
        "signal_name": "dispersion_expansion_leadership_20",
        "family": "dispersion",
        "theme": "Dispersion Expansion Transition",
        "feature_group": "dispersion_leadership",
        "horizon": "h10-h20",
        "redundancy_risk": "medium",
        "research_status": "RESEARCH_ONLY",
        "mechanism_thesis": "Early dispersion leaders outperform as cross-sectional differences widen during a transition.",
    },
    {
        "candidate_id": "dispersion_expansion_transition_02",
        "signal_name": "dispersion_expansion_momentum_20",
        "family": "dispersion",
        "theme": "Dispersion Expansion Transition",
        "feature_group": "dispersion_leadership",
        "horizon": "h10-h20",
        "redundancy_risk": "medium",
        "research_status": "RESEARCH_ONLY",
        "mechanism_thesis": "Rising relative dispersion momentum identifies securities that are differentiating ahead of the market.",
    },
    {
        "candidate_id": "dispersion_expansion_transition_03",
        "signal_name": "relative_dispersion_ranking_20",
        "family": "dispersion",
        "theme": "Dispersion Expansion Transition",
        "feature_group": "dispersion_leadership",
        "horizon": "h10-h20",
        "redundancy_risk": "medium",
        "research_status": "RESEARCH_ONLY",
        "mechanism_thesis": "Rank securities by rising cross-sectional dispersion relative to the universe rather than by simple volatility growth.",
    },
    {
        "candidate_id": "dispersion_expansion_transition_04",
        "signal_name": "dispersion_transition_acceleration_20",
        "family": "dispersion",
        "theme": "Dispersion Expansion Transition",
        "feature_group": "dispersion_leadership",
        "horizon": "h10-h20",
        "redundancy_risk": "medium",
        "research_status": "RESEARCH_ONLY",
        "mechanism_thesis": "Acceleration of dispersion growth signals names that lead the structural reorganization of cross-sectional breadth.",
    },
    {
        "candidate_id": "dispersion_compression_reversal_01",
        "signal_name": "compression_reversal_quality_20",
        "family": "dispersion",
        "theme": "Dispersion Compression Reversal",
        "feature_group": "dispersion_compression",
        "horizon": "h10-h20",
        "redundancy_risk": "medium",
        "research_status": "RESEARCH_ONLY",
        "mechanism_thesis": "Names that stabilize earlier than peers during dispersion compression may outperform as the market rotates back toward coherence.",
    },
    {
        "candidate_id": "dispersion_compression_reversal_02",
        "signal_name": "dispersion_compression_stability_20",
        "family": "dispersion",
        "theme": "Dispersion Compression Reversal",
        "feature_group": "dispersion_compression",
        "horizon": "h10-h20",
        "redundancy_risk": "medium",
        "research_status": "RESEARCH_ONLY",
        "mechanism_thesis": "Stability-oriented dispersion compression captures securities that remain structurally resilient as cross-sectional variance falls.",
    },
    {
        "candidate_id": "dispersion_compression_reversal_03",
        "signal_name": "compression_leadership_confirmation_20",
        "family": "dispersion",
        "theme": "Dispersion Compression Reversal",
        "feature_group": "dispersion_compression",
        "horizon": "h10-h20",
        "redundancy_risk": "medium",
        "research_status": "RESEARCH_ONLY",
        "mechanism_thesis": "Relative compression leadership rewards names that normalize ahead of the market while remaining directional.",
    },
    {
        "candidate_id": "dispersion_compression_reversal_04",
        "signal_name": "relative_correlation_compression_20",
        "family": "dispersion",
        "theme": "Dispersion Compression Reversal",
        "feature_group": "dispersion_compression",
        "horizon": "h10-h20",
        "redundancy_risk": "medium-high",
        "research_status": "RESEARCH_ONLY",
        "mechanism_thesis": "Improving pairwise correlation and dispersion compression may reveal early coherent leaders.",
    },
    {
        "candidate_id": "dispersion_structure_anomalies_01",
        "signal_name": "dispersion_skew_anomaly_20",
        "family": "dispersion",
        "theme": "Dispersion Structure Anomalies",
        "feature_group": "dispersion_anomaly",
        "horizon": "h10-h20",
        "redundancy_risk": "medium-high",
        "research_status": "RESEARCH_ONLY",
        "mechanism_thesis": "Skewed dispersion exposure may capture non-reversion behavior in structurally unusual names.",
    },
    {
        "candidate_id": "dispersion_structure_anomalies_02",
        "signal_name": "cluster_dispersion_tail_20",
        "family": "dispersion",
        "theme": "Dispersion Structure Anomalies",
        "feature_group": "dispersion_anomaly",
        "horizon": "h10-h20",
        "redundancy_risk": "medium-high",
        "research_status": "RESEARCH_ONLY",
        "mechanism_thesis": "Tail dispersion clusters may reveal securities with persistent, asymmetric cross-sectional behavior.",
    },
    {
        "candidate_id": "dispersion_structure_anomalies_03",
        "signal_name": "cross_sectional_asymmetry_20",
        "family": "dispersion",
        "theme": "Dispersion Structure Anomalies",
        "feature_group": "dispersion_anomaly",
        "horizon": "h10-h20",
        "redundancy_risk": "medium-high",
        "research_status": "RESEARCH_ONLY",
        "mechanism_thesis": "Asymmetric dispersion profiles can identify names whose market placement is structurally distinct.",
    },
    {
        "candidate_id": "rank_stability_after_drawdown_01",
        "signal_name": "drawdown_rank_stability_20",
        "family": "persistence",
        "theme": "Rank Stability After Drawdown",
        "feature_group": "rank_stability",
        "horizon": "h10-h20",
        "redundancy_risk": "medium",
        "research_status": "RESEARCH_ONLY",
        "mechanism_thesis": "Names that maintain rank stability after drawdown may offer durable persistence over the next medium term.",
    },
    {
        "candidate_id": "rank_stability_after_drawdown_02",
        "signal_name": "post_drawdown_persistence_20",
        "family": "persistence",
        "theme": "Rank Stability After Drawdown",
        "feature_group": "rank_stability",
        "horizon": "h10-h20",
        "redundancy_risk": "medium",
        "research_status": "RESEARCH_ONLY",
        "mechanism_thesis": "Persistent rank behavior following a drawdown may separate durable leadership from noisy recovery.",
    },
    {
        "candidate_id": "rank_stability_after_drawdown_03",
        "signal_name": "rank_churn_resilience_20",
        "family": "persistence",
        "theme": "Rank Stability After Drawdown",
        "feature_group": "rank_stability",
        "horizon": "h10-h20",
        "redundancy_risk": "medium",
        "research_status": "RESEARCH_ONLY",
        "mechanism_thesis": "Low rank churn after drawdown signals relative stability and reduced leadership turnover.",
    },
    {
        "candidate_id": "rank_coherence_regime_transition_01",
        "signal_name": "regime_coherence_transition_20",
        "family": "persistence",
        "theme": "Rank Coherence Regime Transition",
        "feature_group": "rank_coherence",
        "horizon": "h10-h20",
        "redundancy_risk": "medium",
        "research_status": "RESEARCH_ONLY",
        "mechanism_thesis": "Improved rank coherence during regime transitions may identify names that are structurally aligned with the new regime.",
    },
    {
        "candidate_id": "rank_coherence_regime_transition_02",
        "signal_name": "transition_rank_stability_20",
        "family": "persistence",
        "theme": "Rank Coherence Regime Transition",
        "feature_group": "rank_coherence",
        "horizon": "h10-h20",
        "redundancy_risk": "medium",
        "research_status": "RESEARCH_ONLY",
        "mechanism_thesis": "Rank stability through a regime shift may be a signal of new-regime leadership rather than stress repair.",
    },
    {
        "candidate_id": "rank_coherence_regime_transition_03",
        "signal_name": "coherence_improvement_20",
        "family": "persistence",
        "theme": "Rank Coherence Regime Transition",
        "feature_group": "rank_coherence",
        "horizon": "h10-h20",
        "redundancy_risk": "medium",
        "research_status": "RESEARCH_ONLY",
        "mechanism_thesis": "Improving rank coherence relative to peers may capture stable leadership during a regime change.",
    },
]


def _ensure_dirs() -> None:
    for path in (
        OUT_DIR,
        CANDIDATE_INVENTORY_DIR,
        DISCOVERY_SUMMARY_DIR,
        DIAGNOSTICS_DIR,
        REDUNDANCY_SCREENING_DIR,
        GOVERNANCE_REVIEW_DIR,
    ):
        path.mkdir(parents=True, exist_ok=True)
    NOTE_PATH.parent.mkdir(parents=True, exist_ok=True)


def _ensure_panel_generation_dirs() -> None:
    for path in (
        OUT_DIR,
        CANDIDATE_INVENTORY_DIR,
        DISCOVERY_SUMMARY_DIR,
        DIAGNOSTICS_DIR,
        REDUNDANCY_SCREENING_DIR,
        CANDIDATE_PANELS_DIR,
    ):
        path.mkdir(parents=True, exist_ok=True)


def _candidate_registry() -> pd.DataFrame:
    registry = pd.DataFrame(CANDIDATES)
    registry["run_id"] = RUN_ID
    return registry


def _candidate_panel_cache_complete(registry: pd.DataFrame) -> bool:
    return all((CANDIDATE_PANELS_DIR / f"{signal_name}.parquet").exists() for signal_name in registry["signal_name"])


def _rank_cs(panel: pd.DataFrame) -> pd.DataFrame:
    return panel.rank(axis=1, pct=True).sub(0.5).mul(2.0)


def _clean_panel(panel: pd.DataFrame) -> pd.DataFrame:
    cleaned = panel.replace([np.inf, -np.inf], np.nan)
    return cleaned.clip(lower=-1.0, upper=1.0)


def _load_source_panels() -> tuple[dict[str, pd.DataFrame], list[dict[str, object]]]:
    panels: dict[str, pd.DataFrame] = {}
    rows: list[dict[str, object]] = []
    for name in SOURCE_PANEL_NAMES:
        path = SOURCE_PANEL_DIR / f"{name}.parquet"
        metadata_path = SOURCE_PANEL_DIR / f"{name}.metadata.json"
        if not path.exists():
            rows.append({"source_signal": name, "status": "missing", "path": str(path), "rows": 0, "tickers": 0})
            continue
        panel = pd.read_parquet(path)
        panel.index = pd.to_datetime(panel.index)
        if PANEL_GENERATION_LOOKBACK_ROWS > 0:
            panel = panel.tail(PANEL_GENERATION_LOOKBACK_ROWS)
        panels[name] = panel.sort_index()
        metadata = {}
        if metadata_path.exists():
            metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        rows.append(
            {
                "source_signal": name,
                "status": "loaded",
                "path": str(path),
                "rows": int(len(panel)),
                "tickers": int(len(panel.columns)),
                "date_min": str(panel.index.min().date()) if len(panel.index) else None,
                "date_max": str(panel.index.max().date()) if len(panel.index) else None,
                "source_created_at": metadata.get("created_at"),
            }
        )
    missing = [row["source_signal"] for row in rows if row["status"] == "missing"]
    if missing:
        raise FileNotFoundError(f"Missing required source signal panels: {', '.join(missing)}")
    return panels, rows


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


def _candidate_signal_panels(source: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
    rr_rank = source["relative_return_rank_20"]
    rr_z = source["relative_return_zscore_60"]
    residual = source["residual_return_vs_universe_20"]
    rank_stability = source["percentile_rank_stability_20"]
    rank_stability_downtrend = source["percentile_rank_stability_20_downtrend"]
    trend = source["trend_consistency_20_60"]
    trend_persistent = source["trend_consistency_20_60_persistent"]
    smooth_trend = source["smooth_trend_persistence_60"]
    smooth_downtrend = source["smooth_trend_persistence_60_downtrend"]
    vol_compression = source["vol_compression_breakout_20_60"]
    vol_of_vol = source["vol_of_vol_20"]
    vol_surprise = source["vol_surprise_20_60"]
    range_compression = source["range_compression_breakout_10"]
    range_failure = source["range_expansion_failure_5"]
    failed_breakout = source["failed_breakout_reversal_20"]
    failed_breakout_low_breadth = source["failed_breakout_reversal_20_low_breadth"]

    rank_churn = rank_stability.diff().abs().rolling(20, min_periods=10).mean()
    dispersion_level = _rank_cs(rr_z.abs())
    dispersion_change = dispersion_level.diff(20)
    dispersion_accel = dispersion_level.diff(5) - dispersion_level.diff(20)
    compression_quality = _rank_cs(vol_compression.add(range_compression, fill_value=0.0).add(trend, fill_value=0.0))
    rank_coherence_change = rank_stability.diff(20).add(trend.diff(20), fill_value=0.0)

    return {
        "dispersion_expansion_leadership_20": _clean_panel(
            _rank_cs(dispersion_change.add(rr_rank, fill_value=0.0))
        ),
        "dispersion_expansion_momentum_20": _clean_panel(
            _rank_cs(vol_surprise.diff(20).add(vol_of_vol.diff(20), fill_value=0.0))
        ),
        "relative_dispersion_ranking_20": _clean_panel(dispersion_level),
        "dispersion_transition_acceleration_20": _clean_panel(_rank_cs(dispersion_accel)),
        "compression_reversal_quality_20": _clean_panel(compression_quality),
        "dispersion_compression_stability_20": _clean_panel(
            _rank_cs(vol_compression.sub(vol_of_vol, fill_value=0.0).add(range_compression, fill_value=0.0))
        ),
        "compression_leadership_confirmation_20": _clean_panel(
            _rank_cs(compression_quality.mul(trend.rank(axis=1, pct=True)))
        ),
        "relative_correlation_compression_20": _clean_panel(
            _rank_cs(vol_compression.sub(residual.abs(), fill_value=0.0))
        ),
        "dispersion_skew_anomaly_20": _clean_panel(_rank_cs(rr_z.pow(3))),
        "cluster_dispersion_tail_20": _clean_panel(_rank_cs(rr_z.abs().mul(vol_of_vol.abs()))),
        "cross_sectional_asymmetry_20": _clean_panel(_rank_cs(rr_z.sub(residual, fill_value=0.0))),
        "drawdown_rank_stability_20": _clean_panel(
            _rank_cs(rank_stability_downtrend.add(failed_breakout_low_breadth, fill_value=0.0))
        ),
        "post_drawdown_persistence_20": _clean_panel(
            _rank_cs(rank_stability_downtrend.add(trend_persistent, fill_value=0.0).add(smooth_downtrend, fill_value=0.0))
        ),
        "rank_churn_resilience_20": _clean_panel(_rank_cs(rank_stability.sub(rank_churn, fill_value=0.0))),
        "regime_coherence_transition_20": _clean_panel(
            _rank_cs(rank_stability.add(trend, fill_value=0.0).sub(vol_of_vol.abs(), fill_value=0.0))
        ),
        "transition_rank_stability_20": _clean_panel(
            _rank_cs(rank_stability_downtrend.add(vol_compression, fill_value=0.0).add(failed_breakout, fill_value=0.0))
        ),
        "coherence_improvement_20": _clean_panel(
            _rank_cs(rank_coherence_change.add(smooth_trend.diff(20), fill_value=0.0).sub(range_failure.abs(), fill_value=0.0))
        ),
    }


def _panel_to_long(panel: pd.DataFrame, candidate: pd.Series) -> pd.DataFrame:
    long_panel = panel.stack(future_stack=True).dropna().rename("signal_value").reset_index()
    long_panel.columns = ["date", "ticker", "signal_value"]
    long_panel["candidate_id"] = candidate["candidate_id"]
    long_panel["family"] = candidate["family"]
    long_panel["theme"] = candidate["theme"]
    long_panel["horizon"] = candidate["horizon"]
    return long_panel[["date", "ticker", "candidate_id", "signal_value", "family", "theme", "horizon"]]


def _write_candidate_panels(registry: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    source_panels, source_rows = _load_source_panels()
    source_panels = _align_sources(source_panels)
    generated = _candidate_signal_panels(source_panels)
    manifest_rows: list[dict[str, object]] = []
    summary_rows: list[dict[str, object]] = []

    registry.to_csv(CANDIDATE_INVENTORY_DIR / "candidate_registry.csv", index=False)
    for rec in registry.to_dict(orient="records"):
        signal_name = rec["signal_name"]
        panel = generated.get(signal_name)
        if panel is None:
            raise KeyError(f"No panel generation method registered for {signal_name}")
        candidate = pd.Series(rec)
        long_panel = _panel_to_long(panel, candidate)
        panel_path = CANDIDATE_PANELS_DIR / f"{signal_name}.parquet"
        metadata_path = CANDIDATE_PANELS_DIR / f"{signal_name}.metadata.json"
        long_panel.to_parquet(panel_path, index=False)
        metadata_path.write_text(
            json.dumps(
                {
                    "run_id": RUN_ID,
                    "candidate_id": rec["candidate_id"],
                    "signal_name": signal_name,
                    "research_only": True,
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
        manifest_rows.append(
            {
                "candidate_id": rec["candidate_id"],
                "signal_name": signal_name,
                "family": rec["family"],
                "theme": rec["theme"],
                "horizon": rec["horizon"],
                "panel_path": str(panel_path),
                "metadata_path": str(metadata_path),
                "row_count": int(len(long_panel)),
                "date_min": str(long_panel["date"].min().date()) if not long_panel.empty else None,
                "date_max": str(long_panel["date"].max().date()) if not long_panel.empty else None,
                "ticker_count": int(long_panel["ticker"].nunique()) if not long_panel.empty else 0,
                "generation_status": "generated",
            }
        )
        summary_rows.append(
            {
                "candidate_id": rec["candidate_id"],
                "signal_name": signal_name,
                "non_null_observations": int(len(long_panel)),
                "mean_signal_value": float(long_panel["signal_value"].mean()) if not long_panel.empty else np.nan,
                "std_signal_value": float(long_panel["signal_value"].std()) if len(long_panel) > 1 else np.nan,
                "min_signal_value": float(long_panel["signal_value"].min()) if not long_panel.empty else np.nan,
                "max_signal_value": float(long_panel["signal_value"].max()) if not long_panel.empty else np.nan,
                "research_status": rec["research_status"],
                "notes": "research-only candidate panel; no validation or candidate decision applied",
            }
        )

    manifest = pd.DataFrame(manifest_rows)
    summary = pd.DataFrame(summary_rows)
    source_summary = pd.DataFrame(source_rows)
    manifest.to_csv(DISCOVERY_SUMMARY_DIR / "panel_manifest.csv", index=False)
    summary.to_csv(DISCOVERY_SUMMARY_DIR / "candidate_panel_generation_summary.csv", index=False)
    source_summary.to_csv(DIAGNOSTICS_DIR / "candidate_panel_source_inputs.csv", index=False)
    return manifest, summary, source_summary


def _write_research_manifest(registry: pd.DataFrame) -> None:
    (OUT_DIR / "manifest.json").write_text(
        json.dumps(
            {
                "run_id": RUN_ID,
                "research_only": True,
                "research_only_guardrail": RESEARCH_ONLY_GUARDRAIL,
                "candidate_count": int(len(registry)),
                "panel_generation": True,
                "validation_executed": False,
                "production_registration": False,
                "survivor_watchlist_mutation": False,
                "validation_thresholds_modified": False,
                "governance_modified": False,
                "candidate_promotion_or_demotion": False,
                "ml_integration": False,
                "artifact_directories": {
                    "candidate_inventory": str(CANDIDATE_INVENTORY_DIR),
                    "candidate_panels": str(CANDIDATE_PANELS_DIR),
                    "discovery_summary": str(DISCOVERY_SUMMARY_DIR),
                    "diagnostics": str(DIAGNOSTICS_DIR),
                    "redundancy_screening": str(REDUNDANCY_SCREENING_DIR),
                },
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )


def _write_scaffold_artifacts(registry: pd.DataFrame) -> None:
    registry.to_csv(CANDIDATE_INVENTORY_DIR / "candidate_registry.csv", index=False)
    (OUT_DIR / "manifest.json").write_text(
        json.dumps(
            {
                "run_id": RUN_ID,
                "research_only": True,
                "research_only_guardrail": RESEARCH_ONLY_GUARDRAIL,
                "candidate_count": len(registry),
                "artifact_directories": {
                    "candidate_inventory": str(CANDIDATE_INVENTORY_DIR),
                    "discovery_summary": str(DISCOVERY_SUMMARY_DIR),
                    "diagnostics": str(DIAGNOSTICS_DIR),
                    "redundancy_screening": str(REDUNDANCY_SCREENING_DIR),
                    "governance_review": str(GOVERNANCE_REVIEW_DIR),
                },
                "production_registration": False,
                "survivor_watchlist_mutation": False,
                "validation_thresholds_modified": False,
                "governance_modified": False,
                "ml_integration": False,
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )
    pd.DataFrame(
        columns=[
            "candidate_id",
            "signal_name",
            "comparison_signal",
            "diagnostic_status",
            "value_correlation",
            "rank_correlation",
            "overlap_observations",
            "overlap_dates",
            "overlap_tickers",
            "lookback_rows",
            "candidate_panel_path",
            "comparison_panel_path",
            "candidate_panel_created_at",
            "comparison_panel_created_at",
            "notes",
        ]
    ).to_csv(REDUNDANCY_SCREENING_DIR / "redundancy_screening_placeholder.csv", index=False)
    pd.DataFrame(
        columns=[
            "signal_name",
            "diagnostic_type",
            "status",
            "notes",
        ]
    ).to_csv(DIAGNOSTICS_DIR / "panel_diagnostics_placeholder.csv", index=False)
    pd.DataFrame(
        columns=["review_item", "status", "notes"]
    ).to_csv(GOVERNANCE_REVIEW_DIR / "framework_governance_review.csv", index=False)
    (DISCOVERY_SUMMARY_DIR / "framework_scaffold_summary.md").write_text(
        """# Alpha Family Diversification Discovery Framework Scaffold Summary

This folder contains scaffolded artifact outputs for the alpha-family diversification discovery framework.

- `candidate_registry.csv`: approved candidate metadata registry.
- `manifest.json`: framework metadata and research-only guardrails.
- `redundancy_screening_placeholder.csv`: placeholder redundancy diagnostics schema.
- `panel_diagnostics_placeholder.csv`: placeholder diagnostics schema.
- `framework_governance_review.csv`: placeholder governance review checklist.

This scaffold does not execute any candidate discovery or signal scoring. It is intended to support a future dry-run review and implementation validation.
""",
        encoding="utf-8",
    )


def _list_candidates(registry: pd.DataFrame) -> None:
    print(registry[
        [
            "candidate_id",
            "signal_name",
            "family",
            "theme",
            "feature_group",
            "horizon",
            "redundancy_risk",
        ]
    ].to_string(index=False))


def _describe_framework() -> None:
    print("Alpha Family Diversification Discovery Framework Scaffold")
    print(f"run_id: {RUN_ID}")
    print("This runner is research-only. --dry-run writes scaffold diagnostics; --run generates candidate panels only.")
    print("")
    print("Artifact directories:")
    print(f"  - {CANDIDATE_INVENTORY_DIR}")
    print(f"  - {DISCOVERY_SUMMARY_DIR}")
    print(f"  - {DIAGNOSTICS_DIR}")
    print(f"  - {REDUNDANCY_SCREENING_DIR}")
    print(f"  - {GOVERNANCE_REVIEW_DIR}")
    print("")
    print("Use --list-candidates to inspect the approved candidate registry.")
    print("Use --dry-run to create scaffold artifacts without executing discovery.")
    print("Use --run to generate research-only candidate signal panels without validation or promotion decisions.")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Research-only scaffold runner for alpha-family diversification discovery."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--list-candidates",
        action="store_true",
        help="List the approved diversification candidate registry.",
    )
    group.add_argument(
        "--describe",
        action="store_true",
        help="Describe the scaffold and artifact layout.",
    )
    group.add_argument(
        "--dry-run",
        action="store_true",
        help="Create scaffold artifact directories and placeholder outputs without executing discovery.",
    )
    group.add_argument(
        "--run",
        action="store_true",
        help="Generate research-only candidate panels without validation, governance mutation, or production registration.",
    )
    args = parser.parse_args()

    registry = _candidate_registry()

    if args.list_candidates:
        _list_candidates(registry)
        return 0
    if args.describe:
        _describe_framework()
        return 0
    if args.dry_run:
        _ensure_dirs()
        try:
            validate_registry_df(registry)
        except RegistryValidationError as exc:
            print("Registry validation failed:", str(exc))
            print("Aborting dry-run artifact write. Fix registry and re-run --dry-run.")
            return 2

        # Attempt metadata-only redundancy screening (research-only advisory)
        try:
            try:
                from pipelines.utils.redundancy_screening import (
                    StatisticalRedundancyConfig,
                    screen_registry_df,
                    screen_statistical_redundancy_from_cache,
                )
            except Exception:
                import sys

                ROOT = Path(__file__).resolve().parent.parent
                if str(ROOT) not in sys.path:
                    sys.path.insert(0, str(ROOT))
                from pipelines.utils.redundancy_screening import (
                    StatisticalRedundancyConfig,
                    screen_registry_df,
                    screen_statistical_redundancy_from_cache,
                )

            screening_df = screen_registry_df(registry)
            screening_df.to_csv(REDUNDANCY_SCREENING_DIR / "redundancy_screening.csv", index=False)
            print("Wrote metadata-only redundancy screening to", REDUNDANCY_SCREENING_DIR / "redundancy_screening.csv")

            statistical_path = REDUNDANCY_SCREENING_DIR / "statistical_redundancy_screening.csv"
            if _candidate_panel_cache_complete(registry) and statistical_path.exists():
                print(
                    "Preserved existing generated-panel statistical redundancy diagnostics at",
                    statistical_path,
                )
                statistical_df = None
            elif _candidate_panel_cache_complete(registry):
                panel_dir = CANDIDATE_PANELS_DIR
                comparison_signal_names = registry["signal_name"].sort_values().tolist()
                statistical_df = screen_statistical_redundancy_from_cache(
                    registry,
                    comparison_signal_names=comparison_signal_names,
                    config=StatisticalRedundancyConfig(
                        panel_dir=panel_dir,
                        lookback_rows=STATISTICAL_SCREENING_LOOKBACK_ROWS,
                    ),
                )
            else:
                panel_dir = SOURCE_PANEL_DIR
                comparison_signal_names = sorted(path.stem for path in panel_dir.glob("*.parquet"))
                statistical_df = screen_statistical_redundancy_from_cache(
                    registry,
                    comparison_signal_names=comparison_signal_names,
                    config=StatisticalRedundancyConfig(
                        panel_dir=panel_dir,
                        lookback_rows=STATISTICAL_SCREENING_LOOKBACK_ROWS,
                    ),
                )
            if statistical_df is not None:
                statistical_df.to_csv(statistical_path, index=False)
                print("Wrote cached-panel statistical redundancy diagnostics to", statistical_path)
        except Exception as exc:
            print("Redundancy screening failed (advisory only):", str(exc))
            print("Leaving placeholder redundancy artifacts in place.")

        _write_scaffold_artifacts(registry)
        print(f"Wrote scaffold artifacts to {OUT_DIR}")
        return 0
    if args.run:
        _ensure_panel_generation_dirs()
        try:
            validate_registry_df(registry)
        except RegistryValidationError as exc:
            print("Registry validation failed:", str(exc))
            print("Aborting research-only panel generation. Fix registry and re-run --run.")
            return 2

        try:
            try:
                from pipelines.utils.redundancy_screening import (
                    StatisticalRedundancyConfig,
                    screen_registry_df,
                    screen_statistical_redundancy_from_cache,
                )
            except Exception:
                import sys

                ROOT = Path(__file__).resolve().parent.parent
                if str(ROOT) not in sys.path:
                    sys.path.insert(0, str(ROOT))
                from pipelines.utils.redundancy_screening import (
                    StatisticalRedundancyConfig,
                    screen_registry_df,
                    screen_statistical_redundancy_from_cache,
                )

            manifest, summary, _ = _write_candidate_panels(registry)
            _write_research_manifest(registry)
            screening_df = screen_registry_df(registry)
            screening_df.to_csv(REDUNDANCY_SCREENING_DIR / "redundancy_screening.csv", index=False)
            statistical_df = screen_statistical_redundancy_from_cache(
                registry,
                comparison_signal_names=registry["signal_name"].sort_values().tolist(),
                config=StatisticalRedundancyConfig(
                    panel_dir=CANDIDATE_PANELS_DIR,
                    lookback_rows=STATISTICAL_SCREENING_LOOKBACK_ROWS,
                ),
            )
            statistical_df.to_csv(
                REDUNDANCY_SCREENING_DIR / "statistical_redundancy_screening.csv",
                index=False,
            )
            print(f"Wrote {len(manifest)} research-only candidate panels to {CANDIDATE_PANELS_DIR}")
            print("Wrote panel manifest to", DISCOVERY_SUMMARY_DIR / "panel_manifest.csv")
            print("Wrote panel generation summary to", DISCOVERY_SUMMARY_DIR / "candidate_panel_generation_summary.csv")
            print(
                "Wrote post-generation statistical redundancy diagnostics to",
                REDUNDANCY_SCREENING_DIR / "statistical_redundancy_screening.csv",
            )
            print(
                "Research-only guardrail: no validation, governance mutation, production registration, ML, or candidate decisions were executed."
            )
            return 0
        except Exception as exc:
            print("Research-only panel generation failed:", str(exc))
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
