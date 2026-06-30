from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

RUN_ID = "research_only_metadata_seed_layer_v1"
METADATA_VERSION = "ticker_classification_seed_v1"
SNAPSHOT_WARNING = "STATIC_SNAPSHOT_RESEARCH_ONLY"

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.universe import DYNAMIC_TOP300_LIQUIDITY_VERSION, get_phase2_universe_metadata

SEED_PATH = ROOT / "data" / "metadata" / "ticker_classification_seed_v1.csv"
UNIVERSE_METADATA_CSV = ROOT / "data" / "processed" / "phase2" / "nb01_data_foundation" / "universe_metadata.csv"
OUT_DIR = ROOT / "artifacts" / "research" / RUN_ID
NOTE_PATH = ROOT / "docs" / "research_notes" / "research_only_metadata_seed_layer_v1.md"

REQUIRED_COLUMNS = [
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

GROUP_COLUMNS = ["sector", "industry", "peer_group_label", "market_cap_bucket", "size_bucket"]
THIN_GROUP_MIN_SIZE = 8


def _timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _file_sha256(path: Path) -> str | None:
    if not path.exists():
        return None
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _load_seed() -> pd.DataFrame:
    if not SEED_PATH.exists():
        raise FileNotFoundError(f"Missing seed CSV: {SEED_PATH}")
    seed = pd.read_csv(SEED_PATH, dtype=str, keep_default_na=False)
    missing_columns = [column for column in REQUIRED_COLUMNS if column not in seed.columns]
    if missing_columns:
        raise ValueError(f"Seed CSV is missing required columns: {missing_columns}")
    return seed[REQUIRED_COLUMNS].copy()


def _load_universe() -> pd.DataFrame:
    if UNIVERSE_METADATA_CSV.exists():
        universe = pd.read_csv(UNIVERSE_METADATA_CSV, dtype=str, keep_default_na=False)
        if "ticker" in universe.columns:
            return universe
    return get_phase2_universe_metadata(mode="dynamic_top300_liquidity", include_benchmarks=False)


def _normalize_ticker(series: pd.Series) -> pd.Series:
    return series.fillna("").astype(str).str.strip().str.upper()


def _field_completeness(seed: pd.DataFrame) -> pd.DataFrame:
    rows = []
    total = len(seed)
    for column in REQUIRED_COLUMNS:
        non_missing = int(seed[column].astype(str).str.strip().ne("").sum()) if column in seed.columns else 0
        rows.append(
            {
                "field": column,
                "non_missing_rows": non_missing,
                "missing_rows": int(total - non_missing),
                "non_missing_ratio": float(non_missing / total) if total else 0.0,
            }
        )
    return pd.DataFrame(rows)


def _coverage_summary(seed: pd.DataFrame, universe: pd.DataFrame) -> pd.DataFrame:
    seed_tickers = set(_normalize_ticker(seed["ticker"]))
    seed_tickers.discard("")
    universe_tickers = set(_normalize_ticker(universe["ticker"]))
    universe_tickers.discard("")
    matched = seed_tickers & universe_tickers
    return pd.DataFrame(
        [
            {
                "run_id": RUN_ID,
                "metadata_version": METADATA_VERSION,
                "snapshot_warning": SNAPSHOT_WARNING,
                "universe_version": _infer_universe_version(universe),
                "seed_rows": int(len(seed)),
                "seed_distinct_tickers": int(len(seed_tickers)),
                "universe_distinct_tickers": int(len(universe_tickers)),
                "matched_universe_tickers": int(len(matched)),
                "missing_universe_tickers": int(len(universe_tickers - seed_tickers)),
                "extra_seed_tickers_not_in_universe": int(len(seed_tickers - universe_tickers)),
                "coverage_ratio": float(len(matched) / len(universe_tickers)) if universe_tickers else 0.0,
                "point_in_time_validity": False,
                "historical_alpha_validation_allowed": False,
            }
        ]
    )


def _infer_universe_version(universe: pd.DataFrame) -> str:
    if "universe_version" in universe.columns:
        values = sorted(v for v in universe["universe_version"].dropna().astype(str).unique() if v)
        if values:
            return "|".join(values)
    return DYNAMIC_TOP300_LIQUIDITY_VERSION


def _missingness_summary(seed: pd.DataFrame) -> pd.DataFrame:
    rows = []
    total = len(seed)
    for column in ["sector", "industry", "peer_group_label", "market_cap_bucket", "size_bucket"]:
        missing = int(seed[column].astype(str).str.strip().eq("").sum()) if total else 0
        rows.append(
            {
                "field": column,
                "missing_rows": missing,
                "total_rows": int(total),
                "missing_ratio": float(missing / total) if total else 0.0,
            }
        )
    return pd.DataFrame(rows)


def _group_size_distribution(seed: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for column in GROUP_COLUMNS:
        if seed.empty:
            rows.append(
                {
                    "group_field": column,
                    "group_label": "",
                    "ticker_count": 0,
                    "thin_group": True,
                    "notes": "seed_empty",
                }
            )
            continue
        values = seed.loc[seed[column].astype(str).str.strip().ne(""), ["ticker", column]].copy()
        counts = values.groupby(column, dropna=False)["ticker"].nunique().reset_index(name="ticker_count")
        for row in counts.to_dict("records"):
            rows.append(
                {
                    "group_field": column,
                    "group_label": row[column],
                    "ticker_count": int(row["ticker_count"]),
                    "thin_group": bool(int(row["ticker_count"]) < THIN_GROUP_MIN_SIZE),
                    "notes": "",
                }
            )
    return pd.DataFrame(rows)


def _duplicate_checks(seed: pd.DataFrame) -> pd.DataFrame:
    tickers = _normalize_ticker(seed["ticker"])
    duplicate_mask = tickers.ne("") & tickers.duplicated(keep=False)
    duplicates = seed.loc[duplicate_mask].copy()
    if duplicates.empty:
        return pd.DataFrame(
            [{"check": "duplicate_tickers", "duplicate_rows": 0, "duplicate_tickers": "", "passed": True}]
        )
    duplicate_tickers = sorted(set(_normalize_ticker(duplicates["ticker"])))
    return pd.DataFrame(
        [
            {
                "check": "duplicate_tickers",
                "duplicate_rows": int(len(duplicates)),
                "duplicate_tickers": "|".join(duplicate_tickers),
                "passed": False,
            }
        ]
    )


def _ticker_mismatch_checks(seed: pd.DataFrame, universe: pd.DataFrame) -> pd.DataFrame:
    seed_tickers = set(_normalize_ticker(seed["ticker"]))
    seed_tickers.discard("")
    universe_tickers = set(_normalize_ticker(universe["ticker"]))
    universe_tickers.discard("")
    missing = sorted(universe_tickers - seed_tickers)
    extra = sorted(seed_tickers - universe_tickers)
    return pd.DataFrame(
        [
            {
                "check": "universe_tickers_missing_from_seed",
                "count": int(len(missing)),
                "tickers": "|".join(missing[:250]),
                "truncated": bool(len(missing) > 250),
                "passed": len(missing) == 0,
            },
            {
                "check": "seed_tickers_not_in_universe",
                "count": int(len(extra)),
                "tickers": "|".join(extra[:250]),
                "truncated": bool(len(extra) > 250),
                "passed": len(extra) == 0,
            },
        ]
    )


def _snapshot_warnings(seed: pd.DataFrame) -> pd.DataFrame:
    warnings = [
        {
            "warning": "static_snapshot_research_only",
            "severity": "HIGH",
            "active": True,
            "details": "This seed layer is not point-in-time and must not be used for historical sector-relative alpha validation.",
        },
        {
            "warning": "no_external_fetch_performed",
            "severity": "INFO",
            "active": True,
            "details": "The runner reads only the local seed CSV and local universe metadata.",
        },
        {
            "warning": "empty_seed_template",
            "severity": "HIGH" if seed.empty else "INFO",
            "active": bool(seed.empty),
            "details": "The seed CSV currently has no reviewed metadata rows." if seed.empty else "Seed contains reviewed rows; static-snapshot caveats still apply.",
        },
    ]
    if not seed.empty:
        invalid_warning = seed.loc[seed["snapshot_warning"].astype(str).str.strip().ne(SNAPSHOT_WARNING)]
        warnings.append(
            {
                "warning": "snapshot_warning_field_check",
                "severity": "HIGH" if not invalid_warning.empty else "INFO",
                "active": bool(not invalid_warning.empty),
                "details": f"{len(invalid_warning)} rows do not carry {SNAPSHOT_WARNING}.",
            }
        )
    return pd.DataFrame(warnings)


def _lineage_source_audit(seed: pd.DataFrame) -> pd.DataFrame:
    sources = sorted(v for v in seed.get("source", pd.Series(dtype=str)).astype(str).str.strip().unique() if v)
    source_refs = sorted(
        v for v in seed.get("source_url_or_reference", pd.Series(dtype=str)).astype(str).str.strip().unique() if v
    )
    return pd.DataFrame(
        [
            {
                "run_id": RUN_ID,
                "metadata_version": METADATA_VERSION,
                "seed_path": str(SEED_PATH.relative_to(ROOT)),
                "seed_sha256": _file_sha256(SEED_PATH),
                "collection_timestamp": _timestamp(),
                "seed_rows": int(len(seed)),
                "source_count": int(len(sources)),
                "sources": "|".join(sources),
                "source_reference_count": int(len(source_refs)),
                "source_references": "|".join(source_refs[:50]),
                "snapshot_warning": SNAPSHOT_WARNING,
                "point_in_time_validity": False,
                "historical_alpha_validation_allowed": False,
                "external_data_fetched": False,
                "sqlite_modified": False,
            }
        ]
    )


def _seed_validation_summary(seed: pd.DataFrame, coverage: pd.DataFrame, duplicates: pd.DataFrame) -> pd.DataFrame:
    required_present = all(column in seed.columns for column in REQUIRED_COLUMNS)
    duplicate_passed = bool(duplicates["passed"].all()) if "passed" in duplicates.columns else False
    coverage_ratio = float(coverage["coverage_ratio"].iloc[0]) if not coverage.empty else 0.0
    return pd.DataFrame(
        [
            {
                "check": "required_columns_present",
                "passed": required_present,
                "details": "all required columns present" if required_present else "required columns missing",
            },
            {
                "check": "no_duplicate_seed_tickers",
                "passed": duplicate_passed,
                "details": "no duplicate seed tickers" if duplicate_passed else "duplicate seed tickers found",
            },
            {
                "check": "coverage_ready_for_research_inspection",
                "passed": coverage_ratio > 0,
                "details": f"coverage_ratio={coverage_ratio:.6f}; zero is expected for the empty template",
            },
            {
                "check": "point_in_time_validation_allowed",
                "passed": False,
                "details": "static snapshot seed layer is never validation-quality without point-in-time source dates",
            },
        ]
    )


def _write_note(
    seed: pd.DataFrame,
    coverage: pd.DataFrame,
    missingness: pd.DataFrame,
    warnings: pd.DataFrame,
    artifact_files: list[str],
) -> None:
    coverage_row = coverage.iloc[0].to_dict()
    warning_rows = "\n".join(
        f"- `{row['warning']}`: {row['details']}" for row in warnings.to_dict("records") if row.get("active")
    )
    missing_table = missingness.to_markdown(index=False)
    lines = [
        "# Research-Only Metadata Seed Layer v1",
        "",
        "Date: 2026-05-24",
        "",
        "Status: `STATIC_SNAPSHOT_RESEARCH_ONLY`",
        "",
        "## Objective",
        "",
        "Implement a small research-only seed layer scaffold for sector / industry / peer and market-cap / size coverage inspection.",
        "",
        "This note documents the seed CSV template and coverage-audit runner. It does not create point-in-time metadata and does not authorize historical sector-relative alpha validation.",
        "",
        "## Guardrail",
        "",
        "This metadata layer is static-snapshot research scaffolding only. It must not be used for production registration, survivor/watchlist mutation, validation routing, gates, schemas, governance, detector logic, portfolio, ML, blending, optimization, or alpha research claims.",
        "",
        "## Files",
        "",
        "- `data/metadata/ticker_classification_seed_v1.csv`",
        "- `pipelines/run_metadata_seed_layer_v1.py`",
        "- `artifacts/research/research_only_metadata_seed_layer_v1/`",
        "",
        "## Seed Fields",
        "",
        "- `ticker`",
        "- `company_name`",
        "- `sector`",
        "- `industry`",
        "- `peer_group_label`",
        "- `market_cap_bucket`",
        "- `size_bucket`",
        "- `source`",
        "- `source_url_or_reference`",
        "- `as_of_date`",
        "- `effective_date`",
        "- `collection_timestamp`",
        "- `universe_version`",
        "- `metadata_version`",
        "- `snapshot_warning`",
        "",
        "## Coverage Result",
        "",
        f"- Seed rows: `{int(coverage_row['seed_rows'])}`",
        f"- Seed distinct tickers: `{int(coverage_row['seed_distinct_tickers'])}`",
        f"- Universe distinct tickers: `{int(coverage_row['universe_distinct_tickers'])}`",
        f"- Matched universe tickers: `{int(coverage_row['matched_universe_tickers'])}`",
        f"- Coverage ratio: `{float(coverage_row['coverage_ratio']):.6f}`",
        "",
        "If this is the empty template run, zero coverage is expected. Coverage becomes meaningful only after reviewed metadata rows are added in a separately approved step.",
        "",
        "## Missingness Summary",
        "",
        missing_table,
        "",
        "## Active Warnings",
        "",
        warning_rows if warning_rows else "- none",
        "",
        "## Diagnostics Produced",
        "",
        *[f"- `{name}`" for name in artifact_files],
        "",
        "## Interpretation",
        "",
        "The scaffold is ready for controlled metadata coverage inspection. It is not an ingested classification layer, not point-in-time, and not suitable for historical sector-relative or size-relative alpha validation.",
        "",
        "## Recommended Next Step",
        "",
        "Populate a small manually reviewed pilot seed in a future approved step, then rerun this audit to inspect coverage, ticker mismatches, group sizes, missingness, and lineage quality before any database ingestion is considered.",
        "",
        "## Intentional Non-Changes",
        "",
        "- no external data fetched",
        "- no SQLite writes or metadata tables created",
        "- no universe definition changes",
        "- no gate, schema, validation, governance, production, survivor/watchlist, detector, portfolio, ML, blending, or optimization changes",
        "- no sector-relative alpha research started",
        "",
    ]
    NOTE_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    seed = _load_seed()
    universe = _load_universe()

    seed["ticker"] = _normalize_ticker(seed["ticker"])
    for column in REQUIRED_COLUMNS:
        seed[column] = seed[column].astype(str).str.strip()

    coverage = _coverage_summary(seed, universe)
    missingness = _missingness_summary(seed)
    field_completeness = _field_completeness(seed)
    group_sizes = _group_size_distribution(seed)
    thin_groups = group_sizes.loc[group_sizes["thin_group"].astype(bool)].copy()
    duplicates = _duplicate_checks(seed)
    mismatches = _ticker_mismatch_checks(seed, universe)
    warnings = _snapshot_warnings(seed)
    lineage = _lineage_source_audit(seed)
    validation = _seed_validation_summary(seed, coverage, duplicates)

    outputs = {
        "seed_normalized_preview.csv": seed.head(1000),
        "coverage_summary.csv": coverage,
        "missingness_summary.csv": missingness,
        "field_completeness.csv": field_completeness,
        "group_size_distribution.csv": group_sizes,
        "thin_peer_groups.csv": thin_groups,
        "duplicate_ticker_checks.csv": duplicates,
        "ticker_mismatch_checks.csv": mismatches,
        "static_snapshot_warnings.csv": warnings,
        "lineage_source_audit.csv": lineage,
        "seed_validation_summary.csv": validation,
    }
    for filename, frame in outputs.items():
        frame.to_csv(OUT_DIR / filename, index=False)

    artifact_files = sorted([*outputs.keys(), "manifest.json"])
    manifest = {
        "run_id": RUN_ID,
        "status": "STATIC_SNAPSHOT_RESEARCH_ONLY",
        "metadata_version": METADATA_VERSION,
        "seed_path": str(SEED_PATH.relative_to(ROOT)),
        "seed_sha256": _file_sha256(SEED_PATH),
        "artifact_files": artifact_files,
        "seed_rows": int(len(seed)),
        "coverage_ratio": float(coverage["coverage_ratio"].iloc[0]),
        "snapshot_warning": SNAPSHOT_WARNING,
        "point_in_time_validity": False,
        "historical_alpha_validation_allowed": False,
        "external_data_fetched": False,
        "sqlite_modified": False,
        "metadata_tables_created": False,
        "universe_definitions_modified": False,
        "production_registration_changed": False,
        "survivor_watchlist_changed": False,
        "detector_modified": False,
        "portfolio_ml_blending_optimization_route_changed": False,
        "gates_schemas_thresholds_validation_governance_changed": False,
        "generated_at": _timestamp(),
    }
    (OUT_DIR / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    _write_note(seed, coverage, missingness, warnings, artifact_files)
    print(json.dumps({"run_id": RUN_ID, "seed_rows": len(seed), "coverage_ratio": manifest["coverage_ratio"]}, indent=2))


if __name__ == "__main__":
    main()
