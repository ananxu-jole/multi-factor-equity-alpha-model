from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd


RUN_ID = "metadata_diagnostic_integration_v1"
SNAPSHOT_WARNING = "STATIC_SNAPSHOT_RESEARCH_ONLY"
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.universe import get_phase2_stock_universe


SEED_PATH = ROOT / "data" / "metadata" / "ticker_classification_seed_v1.csv"
UNIVERSE_METADATA_CSV = ROOT / "data" / "processed" / "phase2" / "nb01_data_foundation" / "universe_metadata.csv"
SEED_AUDIT_DIR = ROOT / "artifacts" / "research" / "research_only_metadata_seed_layer_v1"
INVENTORY_MONITORING_DIR = ROOT / "artifacts" / "research" / "conditional_alpha_inventory_monitoring_v2"
OUT_DIR = ROOT / "artifacts" / "research" / RUN_ID
NOTE_PATH = ROOT / "docs" / "research_notes" / "metadata_diagnostic_integration_v1.md"

INVENTORY_PANELS = {
    "participation_liquidity_state_shift_20_60": ROOT
    / "artifacts"
    / "research"
    / "robustness_first_discovery_expansion_v4"
    / "participation_liquidity_state_shift_20_60_signal_panel.parquet",
    "participation_breadth_repair_under_hostile_trend": ROOT
    / "artifacts"
    / "research"
    / "track_b_v5_focused_discovery"
    / "participation_breadth_repair_under_hostile_trend_signal_panel.parquet",
    "volatility_compression_after_stress_stabilization": ROOT
    / "artifacts"
    / "research"
    / "track_b_v6_focused_discovery"
    / "volatility_compression_after_stress_stabilization_signal_panel.parquet",
}

ACTIVE_ABS_THRESHOLD = 0.02
MIN_SECTOR_SIZE = 10
MIN_PEER_SIZE = 8


def _timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _ensure_dirs() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    NOTE_PATH.parent.mkdir(parents=True, exist_ok=True)


def _read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path) if path.exists() else pd.DataFrame()


def _load_seed() -> pd.DataFrame:
    seed = pd.read_csv(SEED_PATH, dtype=str, keep_default_na=False)
    seed["ticker"] = seed["ticker"].astype(str).str.strip().str.upper()
    return seed


def _load_universe_tickers() -> set[str]:
    if UNIVERSE_METADATA_CSV.exists():
        universe = pd.read_csv(UNIVERSE_METADATA_CSV, dtype=str, keep_default_na=False)
        if "ticker" in universe.columns:
            return set(universe["ticker"].astype(str).str.strip().str.upper())
    return set(t.upper() for t in get_phase2_stock_universe("dynamic_top300_liquidity"))


def _sector_distribution(seed: pd.DataFrame, universe_tickers: set[str]) -> pd.DataFrame:
    rows = []
    total_seed = len(seed)
    for sector, group in seed.groupby("sector", dropna=False):
        rows.append(
            {
                "sector": sector,
                "ticker_count": int(group["ticker"].nunique()),
                "seed_share": float(group["ticker"].nunique() / total_seed) if total_seed else 0.0,
                "universe_coverage_share": float(group["ticker"].nunique() / len(universe_tickers)) if universe_tickers else 0.0,
                "sector_size_ready_for_diagnostics": bool(group["ticker"].nunique() >= MIN_SECTOR_SIZE),
                "snapshot_warning": SNAPSHOT_WARNING,
            }
        )
    return pd.DataFrame(rows).sort_values(["ticker_count", "sector"], ascending=[False, True])


def _group_distribution(seed: pd.DataFrame, column: str, min_size: int) -> pd.DataFrame:
    rows = []
    for label, group in seed.groupby(column, dropna=False):
        count = int(group["ticker"].nunique())
        rows.append(
            {
                "group_field": column,
                "group_label": label,
                "ticker_count": count,
                "thin_group": bool(count < min_size),
                "min_size": int(min_size),
                "snapshot_warning": SNAPSHOT_WARNING,
            }
        )
    return pd.DataFrame(rows).sort_values(["ticker_count", "group_label"], ascending=[False, True])


def _coverage_summary(seed: pd.DataFrame, universe_tickers: set[str]) -> pd.DataFrame:
    seed_tickers = set(seed["ticker"])
    matched = seed_tickers & universe_tickers
    missing = universe_tickers - seed_tickers
    extra = seed_tickers - universe_tickers
    warning_ok = bool(seed["snapshot_warning"].eq(SNAPSHOT_WARNING).all()) if not seed.empty else False
    return pd.DataFrame(
        [
            {
                "run_id": RUN_ID,
                "metadata_rows": int(len(seed)),
                "metadata_distinct_tickers": int(len(seed_tickers)),
                "universe_distinct_tickers": int(len(universe_tickers)),
                "matched_universe_tickers": int(len(matched)),
                "missing_universe_tickers": int(len(missing)),
                "extra_seed_tickers_not_in_universe": int(len(extra)),
                "coverage_ratio": float(len(matched) / len(universe_tickers)) if universe_tickers else 0.0,
                "snapshot_warning_rows_ok": warning_ok,
                "point_in_time_validity": False,
                "historical_alpha_validation_allowed": False,
                "snapshot_warning": SNAPSHOT_WARNING,
            }
        ]
    )


def _missingness_lineage(seed: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for column in [
        "sector",
        "industry",
        "peer_group_label",
        "market_cap_bucket",
        "size_bucket",
        "source",
        "source_url_or_reference",
        "snapshot_warning",
    ]:
        missing = int(seed[column].astype(str).str.strip().eq("").sum()) if column in seed.columns else len(seed)
        rows.append(
            {
                "field": column,
                "missing_rows": missing,
                "total_rows": int(len(seed)),
                "missing_ratio": float(missing / len(seed)) if len(seed) else 0.0,
                "snapshot_warning": SNAPSHOT_WARNING,
            }
        )
    return pd.DataFrame(rows)


def _load_inventory_panels() -> tuple[dict[str, pd.DataFrame], pd.DataFrame]:
    panels: dict[str, pd.DataFrame] = {}
    rows = []
    for signal_name, path in INVENTORY_PANELS.items():
        if path.exists():
            panel = pd.read_parquet(path)
            panel.columns = panel.columns.astype(str).str.upper()
            panels[signal_name] = panel
            rows.append(
                {
                    "signal_name": signal_name,
                    "panel_path": str(path.relative_to(ROOT)),
                    "available": True,
                    "rows": int(panel.shape[0]),
                    "columns": int(panel.shape[1]),
                    "notes": "loaded for metadata diagnostics only",
                }
            )
        else:
            rows.append(
                {
                    "signal_name": signal_name,
                    "panel_path": str(path.relative_to(ROOT)),
                    "available": False,
                    "rows": 0,
                    "columns": 0,
                    "notes": "panel unavailable",
                }
            )
    return panels, pd.DataFrame(rows)


def _inventory_metadata_coverage(seed: pd.DataFrame, panels: dict[str, pd.DataFrame]) -> pd.DataFrame:
    seed_tickers = set(seed["ticker"])
    rows = []
    for signal_name, panel in panels.items():
        panel_tickers = set(panel.columns.astype(str).str.upper())
        matched = panel_tickers & seed_tickers
        rows.append(
            {
                "signal_name": signal_name,
                "panel_tickers": int(len(panel_tickers)),
                "metadata_covered_tickers": int(len(matched)),
                "metadata_missing_panel_tickers": int(len(panel_tickers - seed_tickers)),
                "metadata_coverage_ratio": float(len(matched) / len(panel_tickers)) if panel_tickers else 0.0,
                "snapshot_warning": SNAPSHOT_WARNING,
                "descriptive_only": True,
            }
        )
    return pd.DataFrame(rows)


def _candidate_sector_exposure(seed: pd.DataFrame, panels: dict[str, pd.DataFrame]) -> tuple[pd.DataFrame, pd.DataFrame]:
    metadata = seed.set_index("ticker")
    exposure_rows = []
    sector_rows = []
    for signal_name, panel in panels.items():
        covered_cols = [ticker for ticker in panel.columns if ticker in metadata.index]
        if not covered_cols:
            exposure_rows.append(
                {
                    "signal_name": signal_name,
                    "covered_panel_tickers": 0,
                    "active_ticker_date_count": 0,
                    "covered_ticker_date_count": 0,
                    "active_share_on_covered_metadata": np.nan,
                    "top_active_sector": "unavailable",
                    "top_active_sector_share": np.nan,
                    "descriptive_only": True,
                    "snapshot_warning": SNAPSHOT_WARNING,
                }
            )
            continue
        covered = panel[covered_cols].astype(float)
        active = covered.abs() > ACTIVE_ABS_THRESHOLD
        active_total = int(active.sum().sum())
        covered_total = int(covered.notna().sum().sum())
        sector_counts = []
        for sector, tickers in metadata.loc[covered_cols].groupby("sector").groups.items():
            sector_tickers = list(tickers)
            sector_active = int(active[sector_tickers].sum().sum())
            sector_available = int(covered[sector_tickers].notna().sum().sum())
            sector_mean_signal = float(covered[sector_tickers].stack().mean()) if sector_available else np.nan
            sector_mean_abs_signal = float(covered[sector_tickers].abs().stack().mean()) if sector_available else np.nan
            sector_counts.append((sector, sector_active))
            sector_rows.append(
                {
                    "signal_name": signal_name,
                    "sector": sector,
                    "covered_tickers": int(len(sector_tickers)),
                    "active_ticker_date_count": sector_active,
                    "covered_ticker_date_count": sector_available,
                    "active_share_within_sector": float(sector_active / sector_available) if sector_available else np.nan,
                    "share_of_candidate_active_exposure": float(sector_active / active_total) if active_total else np.nan,
                    "mean_signal_descriptive": sector_mean_signal,
                    "mean_abs_signal_descriptive": sector_mean_abs_signal,
                    "descriptive_only": True,
                    "snapshot_warning": SNAPSHOT_WARNING,
                }
            )
        top_sector, top_count = max(sector_counts, key=lambda item: item[1]) if sector_counts else ("unavailable", 0)
        exposure_rows.append(
            {
                "signal_name": signal_name,
                "covered_panel_tickers": int(len(covered_cols)),
                "active_ticker_date_count": active_total,
                "covered_ticker_date_count": covered_total,
                "active_share_on_covered_metadata": float(active_total / covered_total) if covered_total else np.nan,
                "top_active_sector": top_sector,
                "top_active_sector_share": float(top_count / active_total) if active_total else np.nan,
                "descriptive_only": True,
                "snapshot_warning": SNAPSHOT_WARNING,
            }
        )
    return pd.DataFrame(exposure_rows), pd.DataFrame(sector_rows)


def _candidate_peer_coverage(seed: pd.DataFrame, panels: dict[str, pd.DataFrame]) -> pd.DataFrame:
    metadata = seed.set_index("ticker")
    rows = []
    for signal_name, panel in panels.items():
        covered_cols = [ticker for ticker in panel.columns if ticker in metadata.index]
        group_counts = metadata.loc[covered_cols, "peer_group_label"].value_counts() if covered_cols else pd.Series(dtype=int)
        rows.append(
            {
                "signal_name": signal_name,
                "covered_tickers": int(len(covered_cols)),
                "peer_groups_covered": int(group_counts.shape[0]),
                "peer_groups_at_min_size": int(group_counts.ge(MIN_PEER_SIZE).sum()),
                "thin_peer_groups": int(group_counts.lt(MIN_PEER_SIZE).sum()),
                "largest_peer_group": str(group_counts.index[0]) if not group_counts.empty else "unavailable",
                "largest_peer_group_count": int(group_counts.iloc[0]) if not group_counts.empty else 0,
                "peer_transform_ready": bool(group_counts.ge(MIN_PEER_SIZE).sum() >= 3),
                "descriptive_only": True,
                "snapshot_warning": SNAPSHOT_WARNING,
            }
        )
    return pd.DataFrame(rows)


def _regime_metadata_context() -> pd.DataFrame:
    regime = _read_csv(INVENTORY_MONITORING_DIR / "regime_overlap_summary.csv")
    coverage = _read_csv(INVENTORY_MONITORING_DIR / "candidate_health_summary.csv")
    if regime.empty:
        return pd.DataFrame()
    rows = []
    for signal_name, group in regime.groupby("signal_name"):
        top = group.sort_values("mean_ic", ascending=False).head(1)
        health_row = coverage.loc[coverage["signal_name"].eq(signal_name)].head(1) if not coverage.empty else pd.DataFrame()
        rows.append(
            {
                "signal_name": signal_name,
                "top_regime_state_from_inventory_monitoring": top.iloc[0]["state"] if not top.empty else "unavailable",
                "top_regime_mean_ic_from_inventory_monitoring": float(top.iloc[0]["mean_ic"]) if not top.empty else np.nan,
                "monitoring_classification": health_row.iloc[0]["monitoring_classification"] if not health_row.empty else "unavailable",
                "metadata_overlay_type": "candidate-level context only; no sector-regime alpha attribution",
                "descriptive_only": True,
                "snapshot_warning": SNAPSHOT_WARNING,
            }
        )
    return pd.DataFrame(rows)


def _readiness_dashboard(
    coverage: pd.DataFrame,
    sector_distribution: pd.DataFrame,
    peer_distribution: pd.DataFrame,
    inventory_coverage: pd.DataFrame,
    missingness: pd.DataFrame,
) -> pd.DataFrame:
    coverage_ratio = float(coverage["coverage_ratio"].iloc[0]) if not coverage.empty else 0.0
    sector_ready_count = int(sector_distribution["sector_size_ready_for_diagnostics"].sum()) if not sector_distribution.empty else 0
    peer_ready_count = int((~peer_distribution["thin_group"].astype(bool)).sum()) if not peer_distribution.empty else 0
    missing_key_rows = int(missingness["missing_rows"].sum()) if not missingness.empty else 0
    min_inventory_coverage = float(inventory_coverage["metadata_coverage_ratio"].min()) if not inventory_coverage.empty else 0.0
    rows = [
        {
            "readiness_item": "static_snapshot_warning_present",
            "status": "PASS" if bool(coverage["snapshot_warning_rows_ok"].iloc[0]) else "BLOCK",
            "value": str(bool(coverage["snapshot_warning_rows_ok"].iloc[0])),
            "interpretation": "All rows must remain STATIC_SNAPSHOT_RESEARCH_ONLY.",
        },
        {
            "readiness_item": "overall_metadata_coverage",
            "status": "WATCH" if coverage_ratio < 0.50 else "PASS",
            "value": f"{coverage_ratio:.6f}",
            "interpretation": (
                "At or above 50% universe coverage; still diagnostic overlay only."
                if coverage_ratio >= 0.50
                else "Below 50% universe coverage; diagnostic overlay only."
            ),
        },
        {
            "readiness_item": "sector_distribution_diagnostics",
            "status": "PARTIAL" if sector_ready_count >= 5 else "WATCH",
            "value": str(sector_ready_count),
            "interpretation": "Number of sectors with at least 10 covered names.",
        },
        {
            "readiness_item": "peer_group_diagnostics",
            "status": "WATCH" if peer_ready_count < 3 else "PARTIAL",
            "value": str(peer_ready_count),
            "interpretation": (
                "Several peer groups are diagnostically usable, but broad peer-relative transforms remain blocked."
                if peer_ready_count >= 3
                else "Peer groups remain too thin for peer-relative transforms."
            ),
        },
        {
            "readiness_item": "inventory_metadata_coverage",
            "status": "WATCH" if min_inventory_coverage < 0.50 else "PASS",
            "value": f"{min_inventory_coverage:.6f}",
            "interpretation": (
                "Inventory panel metadata coverage is above 50%, but descriptive-only."
                if min_inventory_coverage >= 0.50
                else "Coverage over inventory panel columns is still limited."
            ),
        },
        {
            "readiness_item": "key_field_missingness",
            "status": "PASS" if missing_key_rows == 0 else "BLOCK",
            "value": str(missing_key_rows),
            "interpretation": "Key seed fields are populated for all covered rows.",
        },
        {
            "readiness_item": "point_in_time_validity",
            "status": "BLOCK",
            "value": "False",
            "interpretation": "No point-in-time validity; no historical validation claims.",
        },
    ]
    return pd.DataFrame(rows)


def _write_note(
    coverage: pd.DataFrame,
    sector_distribution: pd.DataFrame,
    peer_distribution: pd.DataFrame,
    inventory_coverage: pd.DataFrame,
    sector_exposure: pd.DataFrame,
    readiness: pd.DataFrame,
    artifact_files: list[str],
) -> None:
    coverage_row = coverage.iloc[0].to_dict()
    def md(frame: pd.DataFrame) -> str:
        return frame.astype(str).to_markdown(index=False, disable_numparse=True)

    top_sectors = md(sector_distribution.head(12))
    ready_peers = peer_distribution.loc[~peer_distribution["thin_group"].astype(bool)].head(20)
    ready_peer_text = md(ready_peers) if not ready_peers.empty else "No peer groups met the minimum size threshold."
    inventory_table = md(inventory_coverage)
    top_exposure = (
        sector_exposure.sort_values(["signal_name", "share_of_candidate_active_exposure"], ascending=[True, False])
        .groupby("signal_name")
        .head(5)
    )
    top_exposure_text = md(top_exposure) if not top_exposure.empty else "No inventory sector exposure rows available."
    readiness_text = md(readiness)
    lines = [
        "# Metadata Diagnostic Integration v1",
        "",
        "Date: 2026-05-24",
        "",
        "Status: `STATIC_SNAPSHOT_RESEARCH_ONLY_DIAGNOSTIC_INTEGRATION`",
        "",
        "## Objective",
        "",
        "Integrate the 150-row metadata seed into research-only diagnostics and inventory monitoring context.",
        "",
        "This is not alpha research, not sector-relative validation, not point-in-time metadata, and not a production metadata layer.",
        "",
        "## Guardrail",
        "",
        "All outputs are labeled `STATIC_SNAPSHOT_RESEARCH_ONLY`. The metadata cannot be used for historical sector-relative validation claims, alpha candidate creation, production registration, portfolio routing, ML, blending, or optimization.",
        "",
        "## Coverage",
        "",
        f"- Metadata rows: `{int(coverage_row['metadata_rows'])}`",
        f"- Universe tickers: `{int(coverage_row['universe_distinct_tickers'])}`",
        f"- Matched universe tickers: `{int(coverage_row['matched_universe_tickers'])}`",
        f"- Coverage ratio: `{float(coverage_row['coverage_ratio']):.6f}`",
        f"- Extra seed tickers: `{int(coverage_row['extra_seed_tickers_not_in_universe'])}`",
        "",
        "## Sector Distribution",
        "",
        top_sectors,
        "",
        "## Peer Readiness",
        "",
        ready_peer_text,
        "",
        "Most industry and peer groups remain thin. This blocks peer-relative transforms and limits sector-conditioned interpretation to descriptive diagnostics.",
        "",
        "## Inventory Metadata Coverage",
        "",
        inventory_table,
        "",
        "## Descriptive Inventory Sector Exposure",
        "",
        top_exposure_text,
        "",
        "These are descriptive signal-exposure summaries only. They are not sector-conditioned IC, not return attribution, and not validation evidence.",
        "",
        "## Readiness Dashboard",
        "",
        readiness_text,
        "",
        "## Artifacts",
        "",
        *[f"- `{name}`" for name in artifact_files],
        "",
        "## Decision",
        "",
        "The metadata seed is now integrated into research-only diagnostics. It is useful for coverage, sector distribution, inventory metadata coverage, and thin-group warnings, but it is not ready for sector-relative alpha research or validation.",
        "",
        "## Recommended Next Step",
        "",
        "Expand the seed toward at least 50% universe coverage, prioritizing underrepresented sectors and thin non-semiconductor peer groups. Rerun this diagnostic integration after each controlled expansion.",
        "",
        "## Intentional Non-Changes",
        "",
        "- no alpha candidates created",
        "- no sector-relative signals created",
        "- no validation claims made",
        "- no point-in-time correctness claimed",
        "- no SQLite tables written",
        "- no universe definitions modified",
        "- no gates, schemas, validation logic, or governance changed",
        "- no production registration or survivor/watchlist state changed",
        "- no detector, portfolio, ML, blending, or optimization routing changed",
        "",
    ]
    NOTE_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    _ensure_dirs()
    seed = _load_seed()
    universe_tickers = _load_universe_tickers()
    coverage = _coverage_summary(seed, universe_tickers)
    missingness = _missingness_lineage(seed)
    sector_distribution = _sector_distribution(seed, universe_tickers)
    industry_distribution = _group_distribution(seed, "industry", MIN_PEER_SIZE)
    peer_distribution = _group_distribution(seed, "peer_group_label", MIN_PEER_SIZE)
    market_cap_distribution = _group_distribution(seed, "market_cap_bucket", MIN_SECTOR_SIZE)
    size_distribution = _group_distribution(seed, "size_bucket", MIN_SECTOR_SIZE)
    panels, panel_status = _load_inventory_panels()
    inventory_coverage = _inventory_metadata_coverage(seed, panels)
    candidate_exposure, sector_exposure = _candidate_sector_exposure(seed, panels)
    candidate_peer = _candidate_peer_coverage(seed, panels)
    regime_context = _regime_metadata_context()
    lineage = _read_csv(SEED_AUDIT_DIR / "lineage_source_audit.csv")
    static_warnings = _read_csv(SEED_AUDIT_DIR / "static_snapshot_warnings.csv")
    readiness = _readiness_dashboard(coverage, sector_distribution, peer_distribution, inventory_coverage, missingness)

    outputs = {
        "metadata_coverage_summary.csv": coverage,
        "metadata_missingness_lineage_warnings.csv": missingness,
        "sector_distribution.csv": sector_distribution,
        "industry_distribution.csv": industry_distribution,
        "peer_group_thinness.csv": peer_distribution,
        "market_cap_bucket_distribution.csv": market_cap_distribution,
        "size_bucket_distribution.csv": size_distribution,
        "inventory_panel_status.csv": panel_status,
        "inventory_metadata_coverage.csv": inventory_coverage,
        "inventory_candidate_sector_exposure_summary.csv": candidate_exposure,
        "sector_conditioned_descriptive_signal_summary.csv": sector_exposure,
        "inventory_candidate_peer_group_coverage.csv": candidate_peer,
        "inventory_regime_metadata_context.csv": regime_context,
        "lineage_source_audit.csv": lineage,
        "static_snapshot_warnings.csv": static_warnings,
        "metadata_readiness_dashboard.csv": readiness,
    }
    for filename, frame in outputs.items():
        frame.to_csv(OUT_DIR / filename, index=False)

    artifact_files = sorted([*outputs.keys(), "manifest.json"])
    manifest = {
        "run_id": RUN_ID,
        "status": "STATIC_SNAPSHOT_RESEARCH_ONLY_DIAGNOSTIC_INTEGRATION",
        "metadata_rows": int(len(seed)),
        "coverage_ratio": float(coverage["coverage_ratio"].iloc[0]),
        "inventory_candidates_analyzed": sorted(panels.keys()),
        "artifact_files": artifact_files,
        "snapshot_warning": SNAPSHOT_WARNING,
        "point_in_time_validity": False,
        "historical_alpha_validation_allowed": False,
        "alpha_candidates_created": False,
        "sector_relative_signals_created": False,
        "sqlite_modified": False,
        "universe_definitions_modified": False,
        "production_registration_changed": False,
        "survivor_watchlist_changed": False,
        "detector_modified": False,
        "portfolio_ml_blending_optimization_route_changed": False,
        "gates_schemas_thresholds_validation_governance_changed": False,
        "generated_at": _timestamp(),
    }
    (OUT_DIR / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    _write_note(coverage, sector_distribution, peer_distribution, inventory_coverage, sector_exposure, readiness, artifact_files)
    print(json.dumps({"run_id": RUN_ID, "metadata_rows": len(seed), "coverage_ratio": manifest["coverage_ratio"]}, indent=2))


if __name__ == "__main__":
    main()
