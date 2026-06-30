from __future__ import annotations

from dataclasses import dataclass


SNAPSHOT_WARNING = "STATIC_SNAPSHOT_RESEARCH_ONLY"
DIAGNOSTIC_ONLY_LABEL = "DIAGNOSTIC_ONLY_NOT_ALPHA_VALIDATION"
POINT_IN_TIME_VALIDATED = "POINT_IN_TIME_VALIDATED"
STATIC_SNAPSHOT_ONLY = "STATIC_SNAPSHOT_ONLY"


@dataclass(frozen=True)
class TablePair:
    current: str
    history: str


CLASSIFICATION_TABLES = TablePair(
    current="economic_context_classification_current",
    history="economic_context_classification_history",
)
SIZE_TABLES = TablePair(
    current="economic_context_size_current",
    history="economic_context_size_history",
)
BEHAVIOR_BUCKET_TABLES = TablePair(
    current="economic_context_behavior_bucket_current",
    history="economic_context_behavior_bucket_history",
)
PEER_GROUP_TABLES = TablePair(
    current="economic_context_peer_group_current",
    history="economic_context_peer_group_history",
)
COVERAGE_DIAGNOSTICS_TABLES = TablePair(
    current="economic_context_coverage_diagnostics_current",
    history="economic_context_coverage_diagnostics_history",
)
SOURCE_AUDIT_TABLES = TablePair(
    current="economic_context_source_audit_current",
    history="economic_context_source_audit_history",
)
QUALITY_ALERTS_TABLES = TablePair(
    current="economic_context_quality_alerts_current",
    history="economic_context_quality_alerts_history",
)


CLASSIFICATION_COLUMNS = [
    "ticker",
    "company_name",
    "sector",
    "industry",
    "subindustry",
    "peer_group_label",
    "peer_group_level",
    "classification_system",
    "source",
    "source_version",
    "source_record_id",
    "as_of_date",
    "effective_start",
    "effective_end",
    "is_current",
    "point_in_time_quality",
    "snapshot_warning",
    "universe_version",
    "metadata_version",
    "run_id",
    "collection_timestamp",
    "record_hash",
    "notes",
]

SIZE_COLUMNS = [
    "ticker",
    "market_cap",
    "market_cap_bucket",
    "size_bucket",
    "currency",
    "market_cap_as_of_date",
    "effective_start",
    "effective_end",
    "source",
    "source_version",
    "point_in_time_quality",
    "snapshot_warning",
    "universe_version",
    "metadata_version",
    "run_id",
    "collection_timestamp",
    "record_hash",
    "notes",
]

BEHAVIOR_BUCKET_COLUMNS = [
    "date",
    "ticker",
    "liquidity_bucket",
    "volatility_bucket",
    "residual_vol_bucket",
    "turnover_bucket",
    "beta_bucket",
    "style_bucket",
    "lookback_window",
    "calculation_method",
    "min_history_days",
    "as_of_date",
    "metadata_version",
    "run_id",
    "created_at",
    "notes",
]

PEER_GROUP_COLUMNS = [
    "date",
    "ticker",
    "peer_group_label",
    "peer_group_level",
    "peer_group_method",
    "fallback_used",
    "peer_group_size",
    "peer_group_min_size",
    "source_metadata_version",
    "point_in_time_quality",
    "run_id",
    "created_at",
    "notes",
]

COVERAGE_DIAGNOSTIC_COLUMNS = [
    "run_id",
    "diagnostic_name",
    "metadata_version",
    "universe_version",
    "total_universe_tickers",
    "covered_tickers",
    "missing_tickers",
    "coverage_ratio",
    "sector_count",
    "industry_count",
    "peer_group_count",
    "thin_group_count",
    "point_in_time_quality",
    "snapshot_warning",
    "diagnostic_only",
    "created_at",
    "notes",
]

SOURCE_AUDIT_COLUMNS = [
    "run_id",
    "metadata_version",
    "source",
    "source_version",
    "source_file_path",
    "source_url_or_reference",
    "source_file_hash",
    "record_count_raw",
    "record_count_clean",
    "collection_timestamp",
    "point_in_time_quality",
    "snapshot_warning",
    "license_or_usage_notes",
    "notes",
]

QUALITY_ALERT_COLUMNS = [
    "run_id",
    "alert_type",
    "severity",
    "field",
    "ticker",
    "message",
    "point_in_time_quality",
    "snapshot_warning",
    "diagnostic_only",
    "created_at",
]

REQUIRED_STATIC_SEED_COLUMNS = [
    "ticker",
    "company_name",
    "sector",
    "industry",
    "peer_group_label",
    "market_cap_bucket",
    "size_bucket",
    "source",
    "source_url_or_reference",
    "as_of_date",
    "effective_date",
    "collection_timestamp",
    "universe_version",
    "metadata_version",
    "snapshot_warning",
]

MARKET_CAP_TO_SIZE_BUCKET = {
    "mega_cap": "mega",
    "large_cap": "large",
    "mid_large_cap": "mid_large",
    "mid_cap": "mid",
    "small_cap": "small",
}


def all_table_pairs() -> list[TablePair]:
    return [
        CLASSIFICATION_TABLES,
        SIZE_TABLES,
        BEHAVIOR_BUCKET_TABLES,
        PEER_GROUP_TABLES,
        COVERAGE_DIAGNOSTICS_TABLES,
        SOURCE_AUDIT_TABLES,
        QUALITY_ALERTS_TABLES,
    ]
