from __future__ import annotations

import pandas as pd

from src.economic_context.quality_checks import crosstab_summary, group_size_summary, ticker_mismatch_summary
from src.economic_context.schema import SNAPSHOT_WARNING, STATIC_SNAPSHOT_ONLY


def build_coverage_diagnostics(
    metadata: pd.DataFrame,
    universe_tickers: set[str],
    run_id: str,
    created_at: str,
    metadata_version: str = "",
    universe_version: str = "",
) -> pd.DataFrame:
    mismatch = ticker_mismatch_summary(metadata, universe_tickers).iloc[0].to_dict()
    thin_group_count = 0
    if "peer_group_label" in metadata.columns and "ticker" in metadata.columns:
        peer_sizes = metadata.groupby("peer_group_label", dropna=False)["ticker"].nunique()
        thin_group_count = int((peer_sizes < 8).sum())
    return pd.DataFrame(
        [
            {
                "run_id": run_id,
                "diagnostic_name": "economic_context_metadata_coverage",
                "metadata_version": metadata_version,
                "universe_version": universe_version,
                "total_universe_tickers": mismatch["universe_tickers"],
                "covered_tickers": mismatch["matched_tickers"],
                "missing_tickers": mismatch["missing_universe_tickers"],
                "coverage_ratio": mismatch["coverage_ratio"],
                "sector_count": int(metadata["sector"].nunique()) if "sector" in metadata else 0,
                "industry_count": int(metadata["industry"].nunique()) if "industry" in metadata else 0,
                "peer_group_count": int(metadata["peer_group_label"].nunique()) if "peer_group_label" in metadata else 0,
                "thin_group_count": thin_group_count,
                "point_in_time_quality": STATIC_SNAPSHOT_ONLY,
                "snapshot_warning": SNAPSHOT_WARNING,
                "diagnostic_only": True,
                "created_at": created_at,
                "notes": "coverage diagnostic only; not alpha validation",
            }
        ]
    )


def build_distribution_reports(metadata: pd.DataFrame) -> dict[str, pd.DataFrame]:
    return {
        "sector_distribution": group_size_summary(metadata, "sector", min_group_size=10),
        "industry_distribution": group_size_summary(metadata, "industry", min_group_size=8),
        "peer_group_distribution": group_size_summary(metadata, "peer_group_label", min_group_size=8),
        "size_bucket_distribution": group_size_summary(metadata, "size_bucket", min_group_size=10),
        "market_cap_bucket_distribution": group_size_summary(metadata, "market_cap_bucket", min_group_size=10),
        "sector_size_crosstab": crosstab_summary(metadata, "sector", "size_bucket"),
        "sector_market_cap_crosstab": crosstab_summary(metadata, "sector", "market_cap_bucket"),
    }


def build_readiness_summary(
    coverage: pd.DataFrame,
    validation_checks: pd.DataFrame,
    peer_groups: pd.DataFrame,
) -> pd.DataFrame:
    coverage_row = coverage.iloc[0].to_dict() if not coverage.empty else {}
    failed_checks = int((~validation_checks["passed"].astype(bool)).sum()) if "passed" in validation_checks else 0
    ready_peer_groups = 0
    if not peer_groups.empty and "peer_group_size" in peer_groups:
        ready_peer_groups = int(peer_groups.loc[peer_groups["peer_group_size"] >= 8, "peer_group_label"].nunique())
    return pd.DataFrame(
        [
            {
                "status": "ECONOMIC_CONTEXT_DIAGNOSTIC_SUBSTRATE_READY_STATIC_ONLY",
                "coverage_ratio": coverage_row.get("coverage_ratio", 0.0),
                "failed_validation_checks": failed_checks,
                "ready_peer_group_count": ready_peer_groups,
                "alpha_validation_allowed": False,
                "peer_relative_transform_allowed": False,
                "production_use_allowed": False,
                "snapshot_warning": SNAPSHOT_WARNING,
                "notes": "diagnostic substrate only; point-in-time metadata required before validation use",
            }
        ]
    )
