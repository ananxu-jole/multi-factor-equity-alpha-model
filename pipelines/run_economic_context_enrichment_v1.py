from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd


RUN_ID = "economic_context_enrichment_v1"
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.economic_context.enrichment_diagnostics import (  # noqa: E402
    build_coverage_diagnostics,
    build_distribution_reports,
    build_readiness_summary,
)
from src.economic_context.metadata_loader import (  # noqa: E402
    load_override_csv,
    load_static_seed_csv,
    merge_seed_with_overrides,
    overrides_to_seed_rows,
    static_seed_to_classification_frame,
    static_seed_to_size_frame,
)
from src.economic_context.metadata_validator import validate_overrides, validate_static_seed  # noqa: E402
from src.economic_context.peer_group_builder import (  # noqa: E402
    build_peer_group_fallback_report,
    build_static_peer_groups,
    fallback_hierarchy_summary,
    peer_quality_level_summary,
    peer_group_readiness_summary,
)
from src.economic_context.quality_checks import (  # noqa: E402
    invalid_effective_date_summary,
    missing_ticker_report,
    override_coverage_report,
    thin_group_diagnosis,
    ticker_normalization_audit,
    ticker_mismatch_summary,
    universe_count_reconciliation_report,
)
from src.economic_context.schema import (  # noqa: E402
    BEHAVIOR_BUCKET_COLUMNS,
    CLASSIFICATION_COLUMNS,
    COVERAGE_DIAGNOSTIC_COLUMNS,
    PEER_GROUP_COLUMNS,
    QUALITY_ALERT_COLUMNS,
    SIZE_COLUMNS,
    SNAPSHOT_WARNING,
    SOURCE_AUDIT_COLUMNS,
)
from src.economic_context.size_bucket_builder import (  # noqa: E402
    validate_size_bucket_mapping,
)
from src.economic_context.source_lineage import build_source_audit_frame  # noqa: E402
from src.universe import (  # noqa: E402
    DYNAMIC_TOP300_LIQUIDITY_VERSION,
    get_benchmark_tickers,
    get_phase2_universe_metadata,
)


SEED_PATH = ROOT / "data" / "metadata" / "ticker_classification_seed_v1.csv"
OVERRIDE_PATH = ROOT / "data" / "metadata" / "economic_context_overrides_v1.csv"
OUT_DIR = ROOT / "artifacts" / "research" / RUN_ID
NOTE_PATH = ROOT / "docs" / "research_notes" / "economic_context_enrichment_v1_implementation.md"


def _timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _load_universe_tickers() -> set[str]:
    universe = get_phase2_universe_metadata(mode="dynamic_top300_liquidity", include_benchmarks=False)
    if "ticker" not in universe.columns:
        return set()
    return set(universe["ticker"].fillna("").astype(str).str.strip().str.upper()) - {""}


def _load_benchmark_tickers() -> set[str]:
    return set(str(ticker).strip().upper() for ticker in get_benchmark_tickers())


def _write_csv(frame: pd.DataFrame, name: str) -> Path:
    path = OUT_DIR / name
    path.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(path, index=False)
    return path


def _schema_manifest() -> pd.DataFrame:
    rows = []
    for table_name, columns in {
        "economic_context_classification_current/history": CLASSIFICATION_COLUMNS,
        "economic_context_size_current/history": SIZE_COLUMNS,
        "economic_context_behavior_bucket_current/history": BEHAVIOR_BUCKET_COLUMNS,
        "economic_context_peer_group_current/history": PEER_GROUP_COLUMNS,
        "economic_context_coverage_diagnostics_current/history": COVERAGE_DIAGNOSTIC_COLUMNS,
        "economic_context_source_audit_current/history": SOURCE_AUDIT_COLUMNS,
        "economic_context_quality_alerts_current/history": QUALITY_ALERT_COLUMNS,
    }.items():
        for position, column in enumerate(columns):
            rows.append(
                {
                    "table_family": table_name,
                    "position": position,
                    "column": column,
                    "diagnostic_only": True,
                    "snapshot_warning": SNAPSHOT_WARNING,
                }
            )
    return pd.DataFrame(rows)


def _missing_cause_summary(missing_report: pd.DataFrame) -> pd.DataFrame:
    if missing_report.empty:
        return pd.DataFrame(
            [
                {
                    "likely_missingness_cause": "none",
                    "ticker_count": 0,
                    "snapshot_warning": SNAPSHOT_WARNING,
                    "diagnostic_only": True,
                }
            ]
        )
    return (
        missing_report.groupby("likely_missingness_cause", dropna=False)
        .agg(ticker_count=("ticker", "nunique"))
        .reset_index()
        .assign(snapshot_warning=SNAPSHOT_WARNING, diagnostic_only=True)
        .sort_values(["ticker_count", "likely_missingness_cause"], ascending=[False, True])
    )


def _fallback_coverage_summary(
    universe_tickers: set[str],
    fallback_report: pd.DataFrame,
    missing_report: pd.DataFrame,
) -> pd.DataFrame:
    universe_count = len(universe_tickers)
    fallback_count = (
        int(fallback_report.loc[fallback_report["usable_for_diagnostics_only"].astype(bool), "ticker"].nunique())
        if not fallback_report.empty
        else 0
    )
    blocked_count = int(len(missing_report))
    return pd.DataFrame(
        [
            {
                "universe_tickers": universe_count,
                "tickers_with_diagnostic_fallback": fallback_count,
                "blocked_tickers_without_metadata": blocked_count,
                "fallback_coverage_ratio_over_universe": float(fallback_count / universe_count) if universe_count else 0.0,
                "fallback_coverage_ratio_over_metadata": 1.0 if fallback_count else 0.0,
                "alpha_validation_allowed": False,
                "peer_relative_transform_allowed": False,
                "production_use_allowed": False,
                "snapshot_warning": SNAPSHOT_WARNING,
                "diagnostic_only": True,
            }
        ]
    )


def _blocked_ticker_report(missing_report: pd.DataFrame) -> pd.DataFrame:
    if missing_report.empty:
        return pd.DataFrame(
            columns=[
                "ticker",
                "likely_missingness_cause",
                "metadata_available",
                "benchmark_ticker",
                "normalization_variant_present",
                "recommended_action",
                "snapshot_warning",
                "diagnostic_only",
                "blocked_reason",
                "alpha_validation_allowed",
                "peer_relative_transform_allowed",
                "production_use_allowed",
            ]
        )
    output = missing_report.copy()
    output["blocked_reason"] = "missing static metadata; no point-in-time peer context"
    output["alpha_validation_allowed"] = False
    output["peer_relative_transform_allowed"] = False
    output["production_use_allowed"] = False
    return output


def _metadata_source_lineage_report(seed: pd.DataFrame) -> pd.DataFrame:
    if seed.empty:
        return pd.DataFrame()
    rows = []
    group_cols = ["source", "source_url_or_reference", "metadata_version", "snapshot_warning"]
    for keys, group in seed.groupby(group_cols, dropna=False):
        source, source_ref, metadata_version, snapshot_warning = keys
        rows.append(
            {
                "source": source,
                "source_url_or_reference": source_ref,
                "metadata_version": metadata_version,
                "snapshot_warning": snapshot_warning,
                "ticker_count": int(group["ticker"].nunique()),
                "validation_usage_allowed": False,
                "diagnostic_usage_allowed": True,
                "diagnostic_only": True,
            }
        )
    return pd.DataFrame(rows).sort_values(["ticker_count", "source"], ascending=[False, True])


def _write_note(
    readiness: pd.DataFrame,
    coverage: pd.DataFrame,
    validation_checks: pd.DataFrame,
    override_coverage: pd.DataFrame,
    missing_report: pd.DataFrame,
    reconciliation: pd.DataFrame,
    thin_groups: pd.DataFrame,
    fallback_summary: pd.DataFrame,
    fallback_coverage: pd.DataFrame,
) -> None:
    readiness_row = readiness.iloc[0].to_dict() if not readiness.empty else {}
    coverage_row = coverage.iloc[0].to_dict() if not coverage.empty else {}
    failed = validation_checks.loc[~validation_checks["passed"].astype(bool)] if "passed" in validation_checks else pd.DataFrame()
    reconciliation_note = (
        reconciliation["likely_discrepancy_cause"].iloc[0]
        if not reconciliation.empty and "likely_discrepancy_cause" in reconciliation
        else "use current repo universe loader as source of truth"
    )
    fallback_lines = []
    if not fallback_summary.empty:
        for row in fallback_summary.to_dict("records"):
            fallback_lines.append(
                f"- `{row['fallback_level']}`: `{row['ticker_count']}` tickers "
                f"({row['fallback_reason']})"
            )
    else:
        fallback_lines.append("- No fallback rows generated.")
    fallback_coverage_row = fallback_coverage.iloc[0].to_dict() if not fallback_coverage.empty else {}
    override_coverage_row = override_coverage.iloc[0].to_dict() if not override_coverage.empty else {}
    NOTE_PATH.parent.mkdir(parents=True, exist_ok=True)
    NOTE_PATH.write_text(
        "\n".join(
            [
                "# Economic Context Enrichment v1 Implementation",
                "",
                f"Date: {_timestamp()}",
                "",
                f"Run id: `{RUN_ID}`",
                "",
                f"Status: `{readiness_row.get('status', 'ECONOMIC_CONTEXT_DIAGNOSTIC_SUBSTRATE_READY_STATIC_ONLY')}`",
                "",
                "## Scope",
                "",
                "Implemented the foundational research-only economic context substrate described in "
                "`docs/research_notes/economic_context_enrichment_design_v1.md`.",
                "",
                "This implementation is diagnostic-only. It does not create alpha candidates, change validation "
                "anchors, alter WFV logic, change candidate statuses, modify production paths, change governance, "
                "implement ML, or route metadata into portfolio/blending/optimization logic.",
                "",
                "Raw h10/h20 IC remains the validation anchor. Recovery/post-stress targets remain sidecars only.",
                "",
                "## Implemented",
                "",
                "- `src/economic_context/` package scaffold.",
                "- Schema definitions for proposed current/history economic context tables.",
                "- Static metadata loader and schema adapters.",
                "- Metadata validation and use-case blocking helpers.",
                "- Sector/industry/peer distribution scaffolds.",
                "- Static size bucket consistency diagnostics.",
                "- Date-aware behavioral bucket scaffolds.",
                "- Diagnostic-only peer-group fallback builder.",
                "- Source lineage hashing/audit helper.",
                "- SQLite table creation and current/history persistence helpers.",
                "- Diagnostic runner and artifact outputs.",
                "",
                "## Diagnostic Findings",
                "",
                f"- Metadata coverage ratio: `{coverage_row.get('coverage_ratio', 0.0):.6f}`",
                f"- Covered tickers: `{coverage_row.get('covered_tickers', 0)}`",
                f"- Total universe tickers: `{coverage_row.get('total_universe_tickers', 0)}`",
                f"- Base coverage ratio before overrides: `{override_coverage_row.get('base_coverage_ratio', 0.0):.6f}`",
                f"- Override new universe tickers added: `{override_coverage_row.get('override_new_universe_tickers', 0)}`",
                f"- Final diagnostic coverage ratio: `{override_coverage_row.get('final_coverage_ratio', 0.0):.6f}`",
                f"- Failed validation checks: `{len(failed)}`",
                f"- Missing universe tickers: `{len(missing_report)}`",
                f"- Thin original peer groups: `{len(thin_groups)}`",
                f"- Peer groups meeting threshold: `{readiness_row.get('ready_peer_group_count', 0)}`",
                f"- Diagnostic fallback coverage over universe: `{fallback_coverage_row.get('fallback_coverage_ratio_over_universe', 0.0):.6f}`",
                f"- Blocked tickers without metadata: `{fallback_coverage_row.get('blocked_tickers_without_metadata', 0)}`",
                f"- Alpha validation allowed: `{readiness_row.get('alpha_validation_allowed', False)}`",
                f"- Peer-relative transform allowed: `{readiness_row.get('peer_relative_transform_allowed', False)}`",
                "",
                "## Missing Ticker Diagnosis",
                "",
                f"The base metadata seed was missing `{override_coverage_row.get('override_new_universe_tickers', 0)}` tickers from the stock universe used by the runner.",
                "",
                f"After controlled diagnostic overrides, the merged diagnostic metadata layer is missing `{len(missing_report)}` tickers.",
                "",
                "The missing ticker report is diagnostic-only and does not imply exclusion from the universe or validation eligibility.",
                "",
                "Primary observed base-layer cause:",
                "",
                "- source coverage gap / unpopulated manual static metadata rows.",
                "",
                "Artifact:",
                "",
                "- `missing_ticker_report.csv`",
                "- `missing_ticker_cause_summary.csv`",
                "- `base_missing_ticker_report.csv`",
                "",
                "## Override Coverage Repair",
                "",
                "A controlled manual override file was added at `data/metadata/economic_context_overrides_v1.csv`.",
                "",
                "All override rows are marked static snapshot, diagnostic-only, and blocked from validation usage.",
                "",
                "Artifacts:",
                "",
                "- `override_coverage_report.csv`",
                "- `override_validation_checks.csv`",
                "- `override_seed_rows.csv`",
                "- `metadata_source_lineage_report.csv`",
                "- `ticker_normalization_audit.csv`",
                "",
                "## Universe Count Reconciliation",
                "",
                "The enrichment runner uses the repo's current stock-universe loader with benchmarks excluded as the source of truth.",
                "",
                f"Reconciliation: {reconciliation_note}.",
                "",
                "Artifact:",
                "",
                "- `universe_count_reconciliation.csv`",
                "",
                "## Peer-Group Thinness Diagnosis",
                "",
                f"`{len(thin_groups)}` original peer groups remain below the 8-name diagnostic threshold.",
                "",
                "The dominant cause is industry-level granularity: sectors are broadly populated, but many industry labels contain only a few names.",
                "",
                "Artifacts:",
                "",
                "- `peer_group_thinness_report.csv`",
                "- `peer_group_distribution.csv`",
                "",
                "## Diagnostic Fallback Hierarchy",
                "",
                "Fallback hierarchy used for reporting only:",
                "",
                "1. industry group if peer count is sufficient",
                "2. otherwise sector group",
                "3. otherwise sector x size bucket",
                "4. otherwise broad size bucket",
                "5. otherwise blocked / insufficient peer context",
                "",
                *fallback_lines,
                "",
                "Fallback assignments remain diagnostic-only and blocked from alpha validation.",
                "",
                "Artifacts:",
                "",
                "- `peer_group_fallback_report.csv`",
                "- `fallback_hierarchy_summary.csv`",
                "- `fallback_coverage_summary.csv`",
                "- `blocked_ticker_report.csv`",
                "",
                "## Coverage Improvement Plan",
                "",
                "- Move from static internal overrides toward a point-in-time sector/industry/size source before validation use.",
                "- Keep the override file as a controlled diagnostic repair layer, not an alpha input.",
                "- Add a ticker alias/mapping audit only where symbol conventions require review.",
                "- Preserve source lineage and `STATIC_SNAPSHOT_RESEARCH_ONLY` warnings.",
                "- Evaluate a point-in-time sector/industry/size source before allowing validation use.",
                "- Keep benchmarks/ETFs in a separate metadata layer if benchmark diagnostics need coverage.",
                "",
                "## Still Diagnostic Only",
                "",
                "- Static sector/industry labels.",
                "- Static market-cap/size buckets.",
                "- Descriptive inventory exposure by metadata.",
                "- Peer-group thinness diagnostics.",
                "- Sector/industry distribution dashboards.",
                "",
                "## Blocked Until Point-In-Time Metadata Exists",
                "",
                "- Sector-relative ranks.",
                "- Industry-relative z-scores.",
                "- Peer-relative residual alpha candidates.",
                "- Size-neutral alpha claims.",
                "- Sector-conditioned IC conclusions.",
                "- Validation decisions based on metadata slices.",
                "- Production, portfolio, ML, blending, or optimization use.",
                "",
                "## Artifacts",
                "",
                f"Artifacts were written under `{OUT_DIR.relative_to(ROOT)}/`.",
                "",
                "## Intentional Non-Changes",
                "",
                "- No alpha candidates implemented.",
                "- No validation anchors changed.",
                "- No WFV logic changed.",
                "- No candidate statuses changed.",
                "- No production paths changed.",
                "- No governance changed.",
                "- No ML, portfolio, blending, or optimization logic implemented.",
                "- No SQLite database writes performed by the runner.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    created_at = _timestamp()

    base_seed = load_static_seed_csv(SEED_PATH)
    universe_tickers = _load_universe_tickers()
    benchmark_tickers = _load_benchmark_tickers()
    metadata_version = (
        str(base_seed["metadata_version"].mode().iloc[0])
        if "metadata_version" in base_seed.columns and not base_seed["metadata_version"].empty
        else "ticker_classification_seed_v1"
    )
    overrides = load_override_csv(OVERRIDE_PATH)
    override_seed_rows = overrides_to_seed_rows(
        overrides,
        universe_version=DYNAMIC_TOP300_LIQUIDITY_VERSION,
        metadata_version=metadata_version,
        collection_timestamp=created_at,
    )
    seed = merge_seed_with_overrides(base_seed, override_seed_rows)

    classification = static_seed_to_classification_frame(seed, run_id=RUN_ID)
    size = static_seed_to_size_frame(seed, run_id=RUN_ID)
    peer_groups = build_static_peer_groups(
        classification,
        min_industry_size=8,
        min_sector_size=10,
        run_id=RUN_ID,
        created_at=created_at,
    )

    validation_checks = validate_static_seed(seed)
    base_validation_checks = validate_static_seed(base_seed)
    override_validation_checks = validate_overrides(overrides)
    size_checks = validate_size_bucket_mapping(seed)
    date_checks = invalid_effective_date_summary(classification)
    mismatch = ticker_mismatch_summary(seed, universe_tickers)
    base_missing_report = missing_ticker_report(base_seed, universe_tickers, benchmark_tickers=benchmark_tickers)
    missing_report = missing_ticker_report(seed, universe_tickers, benchmark_tickers=benchmark_tickers)
    reconciliation = universe_count_reconciliation_report(
        stock_universe_tickers=universe_tickers,
        benchmark_tickers=benchmark_tickers,
        prior_reference_count=489,
    )
    thin_groups = thin_group_diagnosis(seed, group_column="peer_group_label", min_group_size=8)
    coverage = build_coverage_diagnostics(
        metadata=seed,
        universe_tickers=universe_tickers,
        run_id=RUN_ID,
        created_at=created_at,
        metadata_version=metadata_version,
        universe_version=DYNAMIC_TOP300_LIQUIDITY_VERSION,
    )
    distributions = build_distribution_reports(seed)
    peer_readiness = peer_group_readiness_summary(peer_groups)
    fallback_report = build_peer_group_fallback_report(seed)
    fallback_summary = fallback_hierarchy_summary(fallback_report)
    peer_quality_summary = peer_quality_level_summary(fallback_report)
    missing_cause_summary = _missing_cause_summary(missing_report)
    fallback_coverage = _fallback_coverage_summary(universe_tickers, fallback_report, missing_report)
    blocked_tickers = _blocked_ticker_report(missing_report)
    override_coverage = override_coverage_report(base_seed, override_seed_rows, seed, universe_tickers)
    normalization_audit = ticker_normalization_audit(seed, universe_tickers, benchmark_tickers=benchmark_tickers)
    source_lineage = _metadata_source_lineage_report(seed)
    base_source_audit = build_source_audit_frame(
        source_path=SEED_PATH,
        source="ticker_classification_seed_v1",
        metadata_version=metadata_version,
        run_id=RUN_ID,
        collection_timestamp=created_at,
        record_count_raw=len(base_seed),
        record_count_clean=len(base_seed),
        source_version=metadata_version,
        source_url_or_reference="manual_static_seed_internal_review_no_external_fetch",
    )
    override_source_audit = build_source_audit_frame(
        source_path=OVERRIDE_PATH,
        source="economic_context_overrides_v1",
        metadata_version=metadata_version,
        run_id=RUN_ID,
        collection_timestamp=created_at,
        record_count_raw=len(overrides),
        record_count_clean=len(override_seed_rows),
        source_version="economic_context_overrides_v1",
        source_url_or_reference="economic_context_overrides_v1_internal_review_no_external_fetch",
    )
    source_audit = pd.concat([base_source_audit, override_source_audit], ignore_index=True)
    readiness = build_readiness_summary(coverage, validation_checks, peer_groups)
    if not readiness.empty:
        readiness = readiness.copy()
        readiness["fallback_coverage_ratio_over_universe"] = fallback_coverage[
            "fallback_coverage_ratio_over_universe"
        ].iloc[0]
        readiness["blocked_tickers_without_metadata"] = fallback_coverage[
            "blocked_tickers_without_metadata"
        ].iloc[0]

    artifacts = {
        "classification_schema_preview.csv": classification,
        "size_schema_preview.csv": size,
        "peer_group_assignments_diagnostic.csv": peer_groups,
        "peer_group_readiness_summary.csv": peer_readiness,
        "validation_checks.csv": validation_checks,
        "base_validation_checks.csv": base_validation_checks,
        "override_validation_checks.csv": override_validation_checks,
        "override_seed_rows.csv": override_seed_rows,
        "override_coverage_report.csv": override_coverage,
        "size_bucket_checks.csv": size_checks,
        "effective_date_checks.csv": date_checks,
        "ticker_mismatch_summary.csv": mismatch,
        "missing_ticker_report.csv": missing_report,
        "base_missing_ticker_report.csv": base_missing_report,
        "missing_ticker_cause_summary.csv": missing_cause_summary,
        "ticker_normalization_audit.csv": normalization_audit,
        "universe_count_reconciliation.csv": reconciliation,
        "peer_group_thinness_report.csv": thin_groups,
        "peer_group_fallback_report.csv": fallback_report,
        "fallback_hierarchy_summary.csv": fallback_summary,
        "peer_quality_level_summary.csv": peer_quality_summary,
        "fallback_coverage_summary.csv": fallback_coverage,
        "blocked_ticker_report.csv": blocked_tickers,
        "coverage_diagnostics.csv": coverage,
        "source_audit.csv": source_audit,
        "metadata_source_lineage_report.csv": source_lineage,
        "readiness_summary.csv": readiness,
        "table_schema_manifest.csv": _schema_manifest(),
    }
    artifacts.update({f"{name}.csv": frame for name, frame in distributions.items()})

    written = {}
    for name, frame in artifacts.items():
        written[name] = str(_write_csv(frame, name).relative_to(ROOT))

    manifest = {
        "run_id": RUN_ID,
        "created_at": created_at,
        "status": "ECONOMIC_CONTEXT_DIAGNOSTIC_SUBSTRATE_READY_STATIC_ONLY",
        "snapshot_warning": SNAPSHOT_WARNING,
        "diagnostic_only": True,
        "alpha_validation_allowed": False,
        "raw_h10_h20_ic_validation_anchor_preserved": True,
        "recovery_targets_validation_use_allowed": False,
        "sqlite_database_written": False,
        "base_missing_universe_ticker_count": int(len(base_missing_report)),
        "missing_universe_ticker_count": int(len(missing_report)),
        "override_rows": int(len(overrides)),
        "override_new_universe_tickers": int(
            override_coverage["override_new_universe_tickers"].iloc[0]
        ),
        "thin_original_peer_group_count": int(len(thin_groups)),
        "fallback_coverage_ratio_over_universe": float(
            fallback_coverage["fallback_coverage_ratio_over_universe"].iloc[0]
        ),
        "blocked_tickers_without_metadata": int(
            fallback_coverage["blocked_tickers_without_metadata"].iloc[0]
        ),
        "fallback_summary": fallback_summary.to_dict("records"),
        "peer_quality_summary": peer_quality_summary.to_dict("records"),
        "seed_path": str(SEED_PATH.relative_to(ROOT)),
        "artifacts": written,
        "intentional_non_changes": [
            "no_alpha_candidates",
            "no_validation_anchor_changes",
            "no_wfv_changes",
            "no_candidate_status_changes",
            "no_production_changes",
            "no_governance_changes",
            "no_ml_portfolio_blending_optimization",
        ],
    }
    manifest_path = OUT_DIR / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    _write_note(
        readiness,
        coverage,
        validation_checks,
        override_coverage,
        missing_report,
        reconciliation,
        thin_groups,
        fallback_summary,
        fallback_coverage,
    )
    print(json.dumps({"run_id": RUN_ID, "out_dir": str(OUT_DIR), "note": str(NOTE_PATH)}, indent=2))


if __name__ == "__main__":
    main()
