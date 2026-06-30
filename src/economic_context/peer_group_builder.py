from __future__ import annotations

import pandas as pd

from src.economic_context.schema import SNAPSHOT_WARNING, STATIC_SNAPSHOT_ONLY


def build_static_peer_groups(
    metadata: pd.DataFrame,
    min_industry_size: int = 8,
    min_sector_size: int = 10,
    run_id: str = "",
    created_at: str = "",
) -> pd.DataFrame:
    """Build diagnostic-only peer groups with industry-first, sector-fallback logic."""
    if metadata.empty:
        return pd.DataFrame()

    frame = metadata.copy()
    industry_sizes = frame.groupby("industry")["ticker"].transform("nunique")
    sector_sizes = frame.groupby("sector")["ticker"].transform("nunique")
    use_industry = industry_sizes >= min_industry_size
    use_sector = ~use_industry & (sector_sizes >= min_sector_size)

    frame["peer_group_label_resolved"] = ""
    frame.loc[use_industry, "peer_group_label_resolved"] = "industry:" + frame.loc[use_industry, "industry"].astype(str)
    frame.loc[use_sector, "peer_group_label_resolved"] = "sector:" + frame.loc[use_sector, "sector"].astype(str)
    frame["peer_group_level"] = ""
    frame.loc[use_industry, "peer_group_level"] = "industry"
    frame.loc[use_sector, "peer_group_level"] = "sector"
    frame["fallback_used"] = use_sector

    resolved_sizes = frame.groupby("peer_group_label_resolved")["ticker"].transform("nunique")
    output = pd.DataFrame(
        {
            "date": frame.get("as_of_date", ""),
            "ticker": frame["ticker"],
            "peer_group_label": frame["peer_group_label_resolved"],
            "peer_group_level": frame["peer_group_level"],
            "peer_group_method": "industry_or_sector_fallback_static_diagnostic",
            "fallback_used": frame["fallback_used"],
            "peer_group_size": resolved_sizes.fillna(0).astype(int),
            "peer_group_min_size": min_industry_size,
            "source_metadata_version": frame.get("metadata_version", ""),
            "point_in_time_quality": frame.get("point_in_time_quality", STATIC_SNAPSHOT_ONLY),
            "run_id": run_id,
            "created_at": created_at,
            "notes": "diagnostic-only peer groups; blocked from alpha validation unless point-in-time approved",
        }
    )
    output["snapshot_warning"] = SNAPSHOT_WARNING
    return output


def build_peer_group_fallback_report(
    metadata: pd.DataFrame,
    min_industry_size: int = 8,
    min_sector_size: int = 10,
    min_sector_size_bucket_size: int = 8,
    min_size_bucket_size: int = 20,
) -> pd.DataFrame:
    """Report a diagnostic-only fallback hierarchy for peer context.

    Hierarchy:
    1. industry group when sufficient
    2. sector x size group when industry is thin and cross group is usable
    3. sector group when sector x size is thin or unavailable
    4. broad size bucket
    5. blocked / insufficient peer context
    """
    if metadata.empty:
        return pd.DataFrame()

    frame = metadata.copy()
    frame["original_peer_group"] = frame.get("peer_group_label", "")
    industry_size = frame.groupby("industry")["ticker"].transform("nunique")
    sector_size = frame.groupby("sector")["ticker"].transform("nunique")
    sector_size_label = frame["sector"].astype(str) + " | " + frame.get("size_bucket", "").astype(str)
    frame["_sector_size_label"] = sector_size_label
    sector_size_bucket_size = frame.groupby("_sector_size_label")["ticker"].transform("nunique")
    size_bucket_size = frame.groupby("size_bucket")["ticker"].transform("nunique") if "size_bucket" in frame else pd.Series(0, index=frame.index)

    rows = []
    for idx, row in frame.iterrows():
        original_size = int(industry_size.loc[idx])
        fallback_label = ""
        fallback_level = "blocked"
        fallback_size = 0
        fallback_reason = "insufficient peer context"

        fallback_distance = 4
        peer_quality_status = "BLOCKED_INSUFFICIENT_PEER_CONTEXT"
        peer_confidence_score = 0.0

        if original_size >= min_industry_size:
            fallback_label = str(row.get("original_peer_group", ""))
            fallback_level = "industry"
            fallback_size = original_size
            fallback_reason = "industry group sufficient"
            fallback_distance = 0
            peer_quality_status = "HIGH_CONFIDENCE_INDUSTRY_PEER"
            peer_confidence_score = 1.0
        elif int(sector_size_bucket_size.loc[idx]) >= min_sector_size_bucket_size:
            fallback_label = "sector_size:" + str(row.get("_sector_size_label", ""))
            fallback_level = "sector_size"
            fallback_size = int(sector_size_bucket_size.loc[idx])
            fallback_reason = "industry group thin; sector x size fallback sufficient"
            fallback_distance = 2
            peer_quality_status = "MEDIUM_CONFIDENCE_SECTOR_SIZE_PEER"
            peer_confidence_score = 0.65
        elif int(sector_size.loc[idx]) >= min_sector_size:
            fallback_label = "sector:" + str(row.get("sector", ""))
            fallback_level = "sector"
            fallback_size = int(sector_size.loc[idx])
            fallback_reason = "industry and sector x size thin; sector fallback sufficient"
            fallback_distance = 1
            peer_quality_status = "MEDIUM_CONFIDENCE_SECTOR_PEER"
            peer_confidence_score = 0.5
        elif int(size_bucket_size.loc[idx]) >= min_size_bucket_size:
            fallback_label = "size:" + str(row.get("size_bucket", ""))
            fallback_level = "size"
            fallback_size = int(size_bucket_size.loc[idx])
            fallback_reason = "sector and industry thin; broad size fallback sufficient"
            fallback_distance = 3
            peer_quality_status = "LOW_CONFIDENCE_BROAD_FALLBACK"
            peer_confidence_score = 0.25

        usable_for_diagnostics = bool(fallback_label and fallback_size > 0)
        rows.append(
            {
                "ticker": row["ticker"],
                "sector": row.get("sector", ""),
                "industry": row.get("industry", ""),
                "size_bucket": row.get("size_bucket", ""),
                "original_peer_group": row.get("original_peer_group", ""),
                "original_group_size": original_size,
                "original_peer_group_min_threshold_met": bool(original_size >= min_industry_size),
                "assigned_diagnostic_peer_group": fallback_label,
                "assigned_diagnostic_peer_group_level": fallback_level,
                "fallback_peer_group": fallback_label,
                "fallback_level": fallback_level,
                "fallback_group_size": fallback_size,
                "peer_group_min_threshold_met": bool(fallback_size >= min_industry_size),
                "fallback_level_used": fallback_level,
                "fallback_distance": fallback_distance,
                "peer_confidence_score": peer_confidence_score,
                "peer_group_quality_status": peer_quality_status,
                "fallback_reason": fallback_reason,
                "usable_for_diagnostics_only": usable_for_diagnostics,
                "diagnostic_usage_allowed": usable_for_diagnostics,
                "validation_usage_allowed": False,
                "alpha_validation_allowed": False,
                "peer_relative_transform_allowed": False,
                "blocked_reason": "static snapshot metadata is not point-in-time safe",
                "snapshot_warning": SNAPSHOT_WARNING,
            }
        )
    return pd.DataFrame(rows).sort_values(["fallback_level", "fallback_group_size", "ticker"], ascending=[True, False, True])


def fallback_hierarchy_summary(fallback_report: pd.DataFrame) -> pd.DataFrame:
    if fallback_report.empty:
        return pd.DataFrame()
    summary = (
        fallback_report.groupby(["fallback_level", "peer_group_quality_status", "fallback_reason"], dropna=False)
        .agg(
            ticker_count=("ticker", "nunique"),
            median_original_group_size=("original_group_size", "median"),
            median_fallback_group_size=("fallback_group_size", "median"),
            median_peer_confidence_score=("peer_confidence_score", "median"),
        )
        .reset_index()
    )
    summary["alpha_validation_allowed"] = False
    summary["peer_relative_transform_allowed"] = False
    summary["snapshot_warning"] = SNAPSHOT_WARNING
    return summary.sort_values(["ticker_count", "fallback_level"], ascending=[False, True])


def peer_quality_level_summary(fallback_report: pd.DataFrame) -> pd.DataFrame:
    if fallback_report.empty:
        return pd.DataFrame()
    summary = (
        fallback_report.groupby(["assigned_diagnostic_peer_group_level", "peer_group_quality_status"], dropna=False)
        .agg(
            ticker_count=("ticker", "nunique"),
            median_peer_group_size=("fallback_group_size", "median"),
            median_fallback_distance=("fallback_distance", "median"),
            median_peer_confidence_score=("peer_confidence_score", "median"),
        )
        .reset_index()
    )
    summary["validation_usage_allowed"] = False
    summary["diagnostic_usage_allowed"] = True
    summary["snapshot_warning"] = SNAPSHOT_WARNING
    return summary.sort_values(["ticker_count", "assigned_diagnostic_peer_group_level"], ascending=[False, True])


def peer_group_readiness_summary(peer_groups: pd.DataFrame) -> pd.DataFrame:
    if peer_groups.empty:
        return pd.DataFrame()
    grouped = (
        peer_groups.groupby(["peer_group_label", "peer_group_level"], dropna=False)
        .agg(
            ticker_count=("ticker", "nunique"),
            fallback_share=("fallback_used", "mean"),
        )
        .reset_index()
    )
    grouped["snapshot_warning"] = SNAPSHOT_WARNING
    grouped["diagnostic_only"] = True
    return grouped.sort_values(["ticker_count", "peer_group_label"], ascending=[False, True])
