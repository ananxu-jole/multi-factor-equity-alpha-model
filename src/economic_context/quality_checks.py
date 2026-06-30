from __future__ import annotations

import pandas as pd

from src.economic_context.metadata_loader import normalize_ticker
from src.economic_context.schema import SNAPSHOT_WARNING


def ticker_mismatch_summary(metadata: pd.DataFrame, universe_tickers: set[str]) -> pd.DataFrame:
    metadata_tickers = set(normalize_ticker(metadata["ticker"])) if "ticker" in metadata else set()
    metadata_tickers.discard("")
    universe = {str(ticker).strip().upper() for ticker in universe_tickers if str(ticker).strip()}
    matched = metadata_tickers & universe
    return pd.DataFrame(
        [
            {
                "metadata_tickers": int(len(metadata_tickers)),
                "universe_tickers": int(len(universe)),
                "matched_tickers": int(len(matched)),
                "missing_universe_tickers": int(len(universe - metadata_tickers)),
                "extra_metadata_tickers": int(len(metadata_tickers - universe)),
                "coverage_ratio": float(len(matched) / len(universe)) if universe else 0.0,
                "snapshot_warning": SNAPSHOT_WARNING,
                "diagnostic_only": True,
            }
        ]
    )


def missing_ticker_report(
    metadata: pd.DataFrame,
    universe_tickers: set[str],
    benchmark_tickers: set[str] | None = None,
) -> pd.DataFrame:
    """Report universe tickers missing from the metadata layer with conservative cause labels."""
    benchmark_tickers = {str(ticker).strip().upper() for ticker in (benchmark_tickers or set())}
    metadata_tickers = set(normalize_ticker(metadata["ticker"])) if "ticker" in metadata else set()
    metadata_tickers.discard("")
    universe = {str(ticker).strip().upper() for ticker in universe_tickers if str(ticker).strip()}
    normalized_metadata = {ticker.replace(".", "-").replace("/", "-"): ticker for ticker in metadata_tickers}

    rows = []
    for ticker in sorted(universe - metadata_tickers):
        normalized_variant = ticker.replace(".", "-").replace("/", "-")
        if ticker in benchmark_tickers:
            likely_cause = "ETF/benchmark/non-common-stock issue"
            remediation = "keep excluded from stock metadata unless benchmark diagnostics need a separate layer"
        elif normalized_variant in normalized_metadata:
            likely_cause = "naming/symbol normalization issue"
            remediation = "review ticker normalization alias mapping"
        elif any(character in ticker for character in [".", "/", "^"]):
            likely_cause = "naming/symbol normalization issue"
            remediation = "review project ticker convention and source symbol convention"
        elif "-" in ticker:
            likely_cause = "ticker mismatch or share-class symbol convention"
            remediation = "manual review of share-class ticker mapping"
        else:
            likely_cause = "source coverage gap"
            remediation = "add reviewed static metadata row or inspect alternate metadata source"
        rows.append(
            {
                "ticker": ticker,
                "likely_missingness_cause": likely_cause,
                "metadata_available": False,
                "benchmark_ticker": ticker in benchmark_tickers,
                "normalization_variant_present": normalized_variant in normalized_metadata,
                "recommended_action": remediation,
                "snapshot_warning": SNAPSHOT_WARNING,
                "diagnostic_only": True,
            }
        )
    return pd.DataFrame(rows)


def ticker_normalization_audit(
    metadata: pd.DataFrame,
    universe_tickers: set[str],
    benchmark_tickers: set[str] | None = None,
) -> pd.DataFrame:
    benchmark_tickers = {str(ticker).strip().upper() for ticker in (benchmark_tickers or set())}
    metadata_tickers = set(normalize_ticker(metadata["ticker"])) if "ticker" in metadata else set()
    metadata_tickers.discard("")
    universe = {str(ticker).strip().upper() for ticker in universe_tickers if str(ticker).strip()}
    rows = []
    for ticker in sorted(universe | metadata_tickers | benchmark_tickers):
        dot_variant = ticker.replace("-", ".")
        hyphen_variant = ticker.replace(".", "-").replace("/", "-")
        pattern = "none"
        if ticker in benchmark_tickers:
            pattern = "benchmark_or_etf"
        elif "." in ticker or "/" in ticker:
            pattern = "dot_or_slash_symbol"
        elif "-" in ticker:
            pattern = "hyphen_class_share_symbol"
        elif (
            (dot_variant != ticker and dot_variant in metadata_tickers)
            or (hyphen_variant != ticker and hyphen_variant in metadata_tickers)
        ):
            pattern = "normalization_variant_possible"
        rows.append(
            {
                "ticker": ticker,
                "in_universe": ticker in universe,
                "in_metadata": ticker in metadata_tickers,
                "benchmark_ticker": ticker in benchmark_tickers,
                "dot_variant": dot_variant,
                "hyphen_variant": hyphen_variant,
                "potential_mismatch_pattern": pattern,
                "review_needed": bool((ticker in universe) and (ticker not in metadata_tickers) and pattern != "none"),
                "snapshot_warning": SNAPSHOT_WARNING,
                "diagnostic_only": True,
            }
        )
    return pd.DataFrame(rows)


def override_coverage_report(
    base_metadata: pd.DataFrame,
    override_seed_rows: pd.DataFrame,
    final_metadata: pd.DataFrame,
    universe_tickers: set[str],
) -> pd.DataFrame:
    universe = {str(ticker).strip().upper() for ticker in universe_tickers if str(ticker).strip()}
    base = set(normalize_ticker(base_metadata["ticker"])) if "ticker" in base_metadata else set()
    override = set(normalize_ticker(override_seed_rows["ticker"])) if "ticker" in override_seed_rows else set()
    final = set(normalize_ticker(final_metadata["ticker"])) if "ticker" in final_metadata else set()
    base.discard("")
    override.discard("")
    final.discard("")
    added = (override - base) & universe
    return pd.DataFrame(
        [
            {
                "base_covered_tickers": int(len(base & universe)),
                "override_rows": int(len(override_seed_rows)),
                "override_new_universe_tickers": int(len(added)),
                "final_covered_tickers": int(len(final & universe)),
                "universe_tickers": int(len(universe)),
                "base_coverage_ratio": float(len(base & universe) / len(universe)) if universe else 0.0,
                "final_coverage_ratio": float(len(final & universe) / len(universe)) if universe else 0.0,
                "validation_usage_allowed": False,
                "peer_relative_transform_allowed": False,
                "production_use_allowed": False,
                "snapshot_warning": SNAPSHOT_WARNING,
                "diagnostic_only": True,
            }
        ]
    )


def universe_count_reconciliation_report(
    stock_universe_tickers: set[str],
    benchmark_tickers: set[str],
    prior_reference_count: int = 489,
) -> pd.DataFrame:
    stock_count = len({str(ticker).strip().upper() for ticker in stock_universe_tickers if str(ticker).strip()})
    benchmark_count = len({str(ticker).strip().upper() for ticker in benchmark_tickers if str(ticker).strip()})
    with_benchmark = stock_count + benchmark_count
    likely_cause = (
        "prior notes likely counted benchmark tickers; current enrichment runner uses stock universe with benchmarks excluded"
        if with_benchmark == prior_reference_count
        else "count differs from prior notes; use current repo universe loader as source of truth"
    )
    return pd.DataFrame(
        [
            {
                "source": "current_repo_stock_universe_loader",
                "include_benchmarks": False,
                "ticker_count": stock_count,
                "prior_reference_count": prior_reference_count,
                "source_of_truth_for_this_run": True,
                "likely_discrepancy_cause": likely_cause,
                "snapshot_warning": SNAPSHOT_WARNING,
                "diagnostic_only": True,
            },
            {
                "source": "current_repo_stock_universe_loader_plus_benchmarks",
                "include_benchmarks": True,
                "ticker_count": with_benchmark,
                "prior_reference_count": prior_reference_count,
                "source_of_truth_for_this_run": False,
                "likely_discrepancy_cause": likely_cause,
                "snapshot_warning": SNAPSHOT_WARNING,
                "diagnostic_only": True,
            },
        ]
    )


def group_size_summary(
    frame: pd.DataFrame,
    group_column: str,
    ticker_column: str = "ticker",
    min_group_size: int = 8,
) -> pd.DataFrame:
    if frame.empty or group_column not in frame.columns or ticker_column not in frame.columns:
        return pd.DataFrame(
            columns=[
                "group_field",
                "group_label",
                "ticker_count",
                "thin_group",
                "min_group_size",
                "snapshot_warning",
                "diagnostic_only",
            ]
        )
    rows = []
    for label, group in frame.groupby(group_column, dropna=False):
        count = int(group[ticker_column].nunique())
        rows.append(
            {
                "group_field": group_column,
                "group_label": label,
                "ticker_count": count,
                "thin_group": bool(count < min_group_size),
                "min_group_size": int(min_group_size),
                "snapshot_warning": SNAPSHOT_WARNING,
                "diagnostic_only": True,
            }
        )
    return pd.DataFrame(rows).sort_values(["ticker_count", "group_label"], ascending=[False, True])


def thin_group_diagnosis(
    frame: pd.DataFrame,
    group_column: str = "peer_group_label",
    min_group_size: int = 8,
) -> pd.DataFrame:
    if frame.empty or group_column not in frame.columns or "ticker" not in frame.columns:
        return pd.DataFrame()
    rows = []
    sector_sizes = frame.groupby("sector")["ticker"].transform("nunique") if "sector" in frame else pd.Series(0, index=frame.index)
    for label, group in frame.groupby(group_column, dropna=False):
        count = int(group["ticker"].nunique())
        if count >= min_group_size:
            continue
        sectors = sorted(group["sector"].dropna().astype(str).unique()) if "sector" in group else []
        likely_causes = ["overly granular industry mapping"]
        if len(group) < min_group_size and len(frame) < 0:
            likely_causes.append("missing metadata")
        if sectors:
            max_sector_size = int(sector_sizes.loc[group.index].max())
            if max_sector_size < min_group_size:
                likely_causes.append("universe composition")
            else:
                likely_causes.append("sector x industry fragmentation")
        rows.append(
            {
                "group_field": group_column,
                "group_label": label,
                "ticker_count": count,
                "min_group_size": min_group_size,
                "thin_group": True,
                "sectors_represented": "|".join(sectors),
                "likely_thinness_cause": "|".join(dict.fromkeys(likely_causes)),
                "recommended_action": "use diagnostic fallback hierarchy; do not use for validation",
                "snapshot_warning": SNAPSHOT_WARNING,
                "diagnostic_only": True,
            }
        )
    return pd.DataFrame(rows).sort_values(["ticker_count", "group_label"], ascending=[False, True])


def crosstab_summary(
    frame: pd.DataFrame,
    row_field: str,
    column_field: str,
    ticker_column: str = "ticker",
) -> pd.DataFrame:
    if frame.empty or row_field not in frame.columns or column_field not in frame.columns:
        return pd.DataFrame()
    counts = (
        frame.groupby([row_field, column_field], dropna=False)[ticker_column]
        .nunique()
        .reset_index(name="ticker_count")
    )
    counts["snapshot_warning"] = SNAPSHOT_WARNING
    counts["diagnostic_only"] = True
    return counts.sort_values(["ticker_count", row_field, column_field], ascending=[False, True, True])


def invalid_effective_date_summary(frame: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for start_col, end_col in [("effective_start", "effective_end"), ("as_of_date", "effective_end")]:
        if start_col not in frame.columns or end_col not in frame.columns:
            continue
        starts = pd.to_datetime(frame[start_col], errors="coerce")
        ends = pd.to_datetime(frame[end_col].replace("", pd.NA), errors="coerce")
        invalid = starts.notna() & ends.notna() & (ends < starts)
        rows.append(
            {
                "check": f"{end_col}_not_before_{start_col}",
                "invalid_rows": int(invalid.sum()),
                "passed": int(invalid.sum()) == 0,
                "snapshot_warning": SNAPSHOT_WARNING,
                "diagnostic_only": True,
            }
        )
    return pd.DataFrame(rows)
