from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd


RUN_ID = "economic_context_inventory_exposure_audit_v1"
SNAPSHOT_WARNING = "STATIC_SNAPSHOT_RESEARCH_ONLY"
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.db import load_ohlcv_panels  # noqa: E402
from src.universe import get_benchmark_tickers  # noqa: E402


ECONOMIC_CONTEXT_DIR = ROOT / "artifacts" / "research" / "economic_context_enrichment_v1"
OUT_DIR = ECONOMIC_CONTEXT_DIR / "inventory_exposure_audit"
NOTE_PATH = ROOT / "docs" / "research_notes" / "economic_context_enrichment_v1_implementation.md"

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

EXPOSURE_FIELDS = [
    "sector",
    "industry",
    "size_bucket",
    "market_cap_bucket",
    "liquidity_bucket",
    "volatility_bucket",
    "fallback_level",
    "fallback_peer_group",
    "assigned_diagnostic_peer_group_level",
    "peer_group_quality_status",
    "fallback_distance",
]

DEFENSIVE_SECTORS = {"Utilities", "Consumer Staples", "Health Care", "Real Estate"}


def _timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _load_csv(name: str) -> pd.DataFrame:
    return pd.read_csv(ECONOMIC_CONTEXT_DIR / name, dtype=str, keep_default_na=False)


def _write_csv(frame: pd.DataFrame, name: str) -> str:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUT_DIR / name
    frame.to_csv(path, index=False)
    return str(path.relative_to(ROOT))


def _bucket_series(values: pd.Series, labels: list[str]) -> pd.Series:
    values = values.dropna()
    output = pd.Series("", index=values.index, dtype=object)
    if values.empty:
        return output
    ranks = values.rank(method="first")
    try:
        buckets = pd.qcut(ranks, q=len(labels), labels=labels, duplicates="drop")
        output.loc[buckets.index] = buckets.astype(str)
    except ValueError:
        output.loc[values.index] = "unbucketed"
    return output


def _build_behavior_context(tickers: list[str]) -> pd.DataFrame:
    panels = load_ohlcv_panels(current=True)
    close = panels["close"].reindex(columns=tickers)
    volume = panels["volume"].reindex(columns=tickers)
    returns = close.pct_change(fill_method=None)
    dollar_volume = close * volume

    median_dollar_volume = dollar_volume.median(axis=0, skipna=True)
    realized_volatility = returns.std(axis=0, skipna=True)

    liquidity_bucket = _bucket_series(
        median_dollar_volume,
        ["low_liquidity", "medium_liquidity", "high_liquidity"],
    )
    volatility_bucket = _bucket_series(
        realized_volatility,
        ["low_volatility", "medium_volatility", "high_volatility"],
    )
    context = pd.DataFrame(
        {
            "ticker": median_dollar_volume.index.astype(str),
            "median_dollar_volume": median_dollar_volume.values,
            "realized_volatility": realized_volatility.reindex(median_dollar_volume.index).values,
            "liquidity_bucket": liquidity_bucket.reindex(median_dollar_volume.index).fillna("").values,
            "volatility_bucket": volatility_bucket.reindex(median_dollar_volume.index).fillna("").values,
            "bucket_method": "full_sample_descriptive_only_not_alpha_input",
            "snapshot_warning": SNAPSHOT_WARNING,
            "diagnostic_only": True,
        }
    )
    return context


def _load_context() -> pd.DataFrame:
    classification = _load_csv("classification_schema_preview.csv")
    size = _load_csv("size_schema_preview.csv")
    fallback = _load_csv("peer_group_fallback_report.csv")
    tickers = sorted(set(classification["ticker"].astype(str)))
    behavior = _build_behavior_context(tickers)

    context = classification[
        ["ticker", "company_name", "sector", "industry", "peer_group_label", "point_in_time_quality", "snapshot_warning"]
    ].merge(
        size[["ticker", "market_cap_bucket", "size_bucket"]],
        on="ticker",
        how="left",
    )
    context = context.merge(
        fallback[
            [
                "ticker",
                "fallback_peer_group",
                "fallback_level",
                "fallback_group_size",
                "assigned_diagnostic_peer_group",
                "assigned_diagnostic_peer_group_level",
                "fallback_distance",
                "peer_confidence_score",
                "peer_group_quality_status",
                "peer_group_min_threshold_met",
                "fallback_reason",
                "usable_for_diagnostics_only",
            ]
        ],
        on="ticker",
        how="left",
    )
    context = context.merge(
        behavior[["ticker", "median_dollar_volume", "realized_volatility", "liquidity_bucket", "volatility_bucket"]],
        on="ticker",
        how="left",
    )
    for column in [
        "fallback_group_size",
        "fallback_distance",
        "peer_confidence_score",
        "median_dollar_volume",
        "realized_volatility",
    ]:
        if column in context.columns:
            context[column] = pd.to_numeric(context[column], errors="coerce")
    context["diagnostic_only"] = True
    context["alpha_validation_allowed"] = False
    context["peer_relative_transform_allowed"] = False
    context["production_use_allowed"] = False
    return context


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
                    "tickers": int(panel.shape[1]),
                    "snapshot_warning": SNAPSHOT_WARNING,
                    "diagnostic_only": True,
                }
            )
        else:
            rows.append(
                {
                    "signal_name": signal_name,
                    "panel_path": str(path.relative_to(ROOT)),
                    "available": False,
                    "rows": 0,
                    "tickers": 0,
                    "snapshot_warning": SNAPSHOT_WARNING,
                    "diagnostic_only": True,
                }
            )
    return panels, pd.DataFrame(rows)


def _candidate_ticker_exposure(panels: dict[str, pd.DataFrame], context: pd.DataFrame) -> pd.DataFrame:
    context_by_ticker = context.set_index("ticker")
    benchmark_tickers = set(get_benchmark_tickers())
    rows = []
    for signal_name, panel in panels.items():
        active = panel.abs().gt(0) & panel.notna()
        active_obs = active.sum(axis=0)
        mean_abs_signal = panel.abs().mean(axis=0, skipna=True)
        for ticker in panel.columns.astype(str):
            metadata = context_by_ticker.loc[ticker].to_dict() if ticker in context_by_ticker.index else {}
            benchmark_ticker = ticker in benchmark_tickers
            rows.append(
                {
                    "signal_name": signal_name,
                    "ticker": ticker,
                    "active_observations": int(active_obs.get(ticker, 0)),
                    "active_ticker": bool(active_obs.get(ticker, 0) > 0),
                    "mean_abs_signal": float(mean_abs_signal.get(ticker, 0.0)),
                    "metadata_covered": bool(ticker in context_by_ticker.index),
                    "benchmark_ticker": benchmark_ticker,
                    "included_in_stock_exposure_audit": bool((ticker in context_by_ticker.index) and not benchmark_ticker),
                    **metadata,
                }
            )
    return pd.DataFrame(rows)


def _exposure_by_field(exposure: pd.DataFrame, field: str) -> pd.DataFrame:
    rows = []
    audit_exposure = exposure.loc[exposure["included_in_stock_exposure_audit"].astype(bool)].copy()
    for signal_name, group in audit_exposure.groupby("signal_name"):
        total_obs = float(group["active_observations"].sum())
        total_tickers = int(group.loc[group["active_ticker"], "ticker"].nunique())
        if total_obs <= 0:
            continue
        grouped = (
            group.groupby(field, dropna=False)
            .agg(
                active_observations=("active_observations", "sum"),
                active_tickers=("active_ticker", "sum"),
            )
            .reset_index()
        )
        for row in grouped.to_dict("records"):
            rows.append(
                {
                    "signal_name": signal_name,
                    "exposure_field": field,
                    "group_label": row[field],
                    "active_observations": int(row["active_observations"]),
                    "active_observation_share": float(row["active_observations"] / total_obs),
                    "active_tickers": int(row["active_tickers"]),
                    "active_ticker_share": float(row["active_tickers"] / total_tickers) if total_tickers else 0.0,
                    "snapshot_warning": SNAPSHOT_WARNING,
                    "diagnostic_only": True,
                }
            )
    return pd.DataFrame(rows).sort_values(
        ["signal_name", "exposure_field", "active_observation_share"],
        ascending=[True, True, False],
    )


def _all_exposures(exposure: pd.DataFrame) -> dict[str, pd.DataFrame]:
    return {f"{field}_exposure_by_candidate.csv": _exposure_by_field(exposure, field) for field in EXPOSURE_FIELDS}


def _concentration_summary(exposure_tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    rows = []
    for name, table in exposure_tables.items():
        if table.empty:
            continue
        field = name.replace("_exposure_by_candidate.csv", "")
        for signal_name, group in table.groupby("signal_name"):
            shares = group["active_observation_share"].astype(float)
            top = group.sort_values("active_observation_share", ascending=False).iloc[0]
            rows.append(
                {
                    "signal_name": signal_name,
                    "exposure_field": field,
                    "top_group": top["group_label"],
                    "top_share": float(top["active_observation_share"]),
                    "hhi": float((shares**2).sum()),
                    "group_count": int(group["group_label"].nunique()),
                    "snapshot_warning": SNAPSHOT_WARNING,
                    "diagnostic_only": True,
                }
            )
    return pd.DataFrame(rows)


def _metadata_coverage_by_candidate(exposure: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for signal_name, group in exposure.groupby("signal_name"):
        total = int(group["ticker"].nunique())
        benchmark_count = int(group.loc[group["benchmark_ticker"], "ticker"].nunique())
        stock_group = group.loc[~group["benchmark_ticker"].astype(bool)]
        stock_total = int(stock_group["ticker"].nunique())
        covered = int(stock_group.loc[stock_group["metadata_covered"], "ticker"].nunique())
        rows.append(
            {
                "signal_name": signal_name,
                "panel_tickers": total,
                "benchmark_or_nonstock_tickers": benchmark_count,
                "stock_panel_tickers": stock_total,
                "metadata_covered_stock_tickers": covered,
                "missing_or_blocked_stock_metadata_tickers": stock_total - covered,
                "metadata_coverage_ratio": float(covered / stock_total) if stock_total else 0.0,
                "alpha_validation_allowed": False,
                "peer_relative_transform_allowed": False,
                "production_use_allowed": False,
                "snapshot_warning": SNAPSHOT_WARNING,
                "diagnostic_only": True,
            }
        )
    return pd.DataFrame(rows)


def _candidate_peer_quality_exposure(exposure: pd.DataFrame) -> pd.DataFrame:
    audit_exposure = exposure.loc[exposure["included_in_stock_exposure_audit"].astype(bool)].copy()
    rows = []
    for signal_name, group in audit_exposure.groupby("signal_name"):
        total_obs = float(group["active_observations"].sum())
        total_tickers = int(group.loc[group["active_ticker"], "ticker"].nunique())
        grouped = (
            group.groupby(["peer_group_quality_status", "fallback_distance"], dropna=False)
            .agg(
                active_observations=("active_observations", "sum"),
                active_tickers=("active_ticker", "sum"),
                median_peer_confidence_score=("peer_confidence_score", "median"),
            )
            .reset_index()
        )
        for row in grouped.to_dict("records"):
            rows.append(
                {
                    "signal_name": signal_name,
                    "peer_group_quality_status": row["peer_group_quality_status"],
                    "fallback_distance": int(row["fallback_distance"]),
                    "active_observations": int(row["active_observations"]),
                    "active_observation_share": float(row["active_observations"] / total_obs) if total_obs else 0.0,
                    "active_tickers": int(row["active_tickers"]),
                    "active_ticker_share": float(row["active_tickers"] / total_tickers) if total_tickers else 0.0,
                    "median_peer_confidence_score": float(row["median_peer_confidence_score"]),
                    "validation_usage_allowed": False,
                    "peer_relative_transform_allowed": False,
                    "snapshot_warning": SNAPSHOT_WARNING,
                    "diagnostic_only": True,
                }
            )
    return pd.DataFrame(rows).sort_values(
        ["signal_name", "active_observation_share"],
        ascending=[True, False],
    )


def _candidate_peer_quality_flags(peer_quality_exposure: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for signal_name, group in peer_quality_exposure.groupby("signal_name"):
        high_share = float(
            group.loc[
                group["peer_group_quality_status"].eq("HIGH_CONFIDENCE_INDUSTRY_PEER"),
                "active_observation_share",
            ].sum()
        )
        broad_low_share = float(
            group.loc[
                group["peer_group_quality_status"].isin(
                    ["LOW_CONFIDENCE_BROAD_FALLBACK", "BLOCKED_INSUFFICIENT_PEER_CONTEXT"]
                ),
                "active_observation_share",
            ].sum()
        )
        sector_share = float(
            group.loc[
                group["peer_group_quality_status"].eq("MEDIUM_CONFIDENCE_SECTOR_PEER"),
                "active_observation_share",
            ].sum()
        )
        sector_size_share = float(
            group.loc[
                group["peer_group_quality_status"].eq("MEDIUM_CONFIDENCE_SECTOR_SIZE_PEER"),
                "active_observation_share",
            ].sum()
        )
        rows.extend(
            [
                {
                    "signal_name": signal_name,
                    "peer_quality_flag": "low_high_confidence_industry_share",
                    "triggered": bool(high_share < 0.30),
                    "observed_share": high_share,
                    "threshold": 0.30,
                    "message": "high-confidence industry peer exposure below 30%",
                    "snapshot_warning": SNAPSHOT_WARNING,
                    "diagnostic_only": True,
                },
                {
                    "signal_name": signal_name,
                    "peer_quality_flag": "sector_fallback_dependency",
                    "triggered": bool(sector_share > 0.25),
                    "observed_share": sector_share,
                    "threshold": 0.25,
                    "message": "broad sector fallback exposure above 25%",
                    "snapshot_warning": SNAPSHOT_WARNING,
                    "diagnostic_only": True,
                },
                {
                    "signal_name": signal_name,
                    "peer_quality_flag": "sector_size_fallback_dependency",
                    "triggered": bool(sector_size_share > 0.50),
                    "observed_share": sector_size_share,
                    "threshold": 0.50,
                    "message": "sector x size fallback exposure above 50%",
                    "snapshot_warning": SNAPSHOT_WARNING,
                    "diagnostic_only": True,
                },
                {
                    "signal_name": signal_name,
                    "peer_quality_flag": "low_confidence_or_blocked_dependency",
                    "triggered": bool(broad_low_share > 0.05),
                    "observed_share": broad_low_share,
                    "threshold": 0.05,
                    "message": "low-confidence broad fallback or blocked exposure above 5%",
                    "snapshot_warning": SNAPSHOT_WARNING,
                    "diagnostic_only": True,
                },
            ]
        )
    return pd.DataFrame(rows)


def _risk_flags(exposure_tables: dict[str, pd.DataFrame], concentration: pd.DataFrame) -> pd.DataFrame:
    rows = []
    combined = pd.concat(exposure_tables.values(), ignore_index=True)
    for signal_name in sorted(combined["signal_name"].unique()):
        signal_rows = combined.loc[combined["signal_name"] == signal_name]
        sector_rows = signal_rows.loc[signal_rows["exposure_field"] == "sector"]
        defensive_share = float(
            sector_rows.loc[sector_rows["group_label"].isin(DEFENSIVE_SECTORS), "active_observation_share"].sum()
        )
        checks = [
            (
                "single_sector_dominance",
                concentration,
                "sector",
                0.35,
                "top sector share exceeds 35%",
            ),
            (
                "single_industry_dominance",
                concentration,
                "industry",
                0.20,
                "top industry share exceeds 20%",
            ),
            (
                "size_bucket_concentration",
                concentration,
                "size_bucket",
                0.70,
                "top size bucket share exceeds 70%",
            ),
            (
                "liquidity_bucket_concentration",
                concentration,
                "liquidity_bucket",
                0.70,
                "top liquidity bucket share exceeds 70%",
            ),
            (
                "volatility_bucket_concentration",
                concentration,
                "volatility_bucket",
                0.70,
                "top volatility bucket share exceeds 70%",
            ),
        ]
        for flag, table, field, threshold, message in checks:
            row = table.loc[(table["signal_name"] == signal_name) & (table["exposure_field"] == field)]
            if row.empty:
                continue
            row = row.iloc[0]
            triggered = bool(row["top_share"] >= threshold)
            rows.append(
                {
                    "signal_name": signal_name,
                    "risk_flag": flag,
                    "triggered": triggered,
                    "observed_group": row["top_group"],
                    "observed_share": float(row["top_share"]),
                    "threshold": threshold,
                    "message": message,
                    "snapshot_warning": SNAPSHOT_WARNING,
                    "diagnostic_only": True,
                }
            )
        fallback_rows = signal_rows.loc[signal_rows["exposure_field"] == "fallback_level"]
        for fallback_level, flag, threshold, message in [
            (
                "sector",
                "broad_sector_fallback_dependence",
                0.25,
                "broad sector fallback share exceeds 25%",
            ),
            (
                "sector_size",
                "sector_size_fallback_dependence",
                0.50,
                "sector x size fallback share exceeds 50%",
            ),
            (
                "size",
                "broad_size_fallback_dependence",
                0.10,
                "broad size fallback share exceeds 10%",
            ),
        ]:
            share = float(
                fallback_rows.loc[fallback_rows["group_label"].eq(fallback_level), "active_observation_share"].sum()
            )
            rows.append(
                {
                    "signal_name": signal_name,
                    "risk_flag": flag,
                    "triggered": bool(share >= threshold),
                    "observed_group": fallback_level,
                    "observed_share": share,
                    "threshold": threshold,
                    "message": message,
                    "snapshot_warning": SNAPSHOT_WARNING,
                    "diagnostic_only": True,
                }
            )
        rows.append(
            {
                "signal_name": signal_name,
                "risk_flag": "defensive_sector_tilt",
                "triggered": bool(defensive_share >= 0.50),
                "observed_group": "Utilities|Consumer Staples|Health Care|Real Estate",
                "observed_share": defensive_share,
                "threshold": 0.50,
                "message": "combined defensive sector share exceeds 50%",
                "snapshot_warning": SNAPSHOT_WARNING,
                "diagnostic_only": True,
            }
        )
        for field, group_label, flag, threshold in [
            ("volatility_bucket", "low_volatility", "low_vol_tilt", 0.50),
            ("liquidity_bucket", "high_liquidity", "high_liquidity_tilt", 0.60),
        ]:
            rows_field = signal_rows.loc[
                (signal_rows["exposure_field"] == field) & (signal_rows["group_label"] == group_label)
            ]
            share = float(rows_field["active_observation_share"].sum()) if not rows_field.empty else 0.0
            rows.append(
                {
                    "signal_name": signal_name,
                    "risk_flag": flag,
                    "triggered": bool(share >= threshold),
                    "observed_group": group_label,
                    "observed_share": share,
                    "threshold": threshold,
                    "message": f"{group_label} share exceeds {threshold:.0%}",
                    "snapshot_warning": SNAPSHOT_WARNING,
                    "diagnostic_only": True,
                }
            )
    return pd.DataFrame(rows)


def _audit_summary(
    coverage: pd.DataFrame,
    concentration: pd.DataFrame,
    risk_flags: pd.DataFrame,
    peer_quality_exposure: pd.DataFrame,
) -> pd.DataFrame:
    rows = []
    for signal_name in coverage["signal_name"]:
        signal_conc = concentration.loc[concentration["signal_name"] == signal_name]
        sector = signal_conc.loc[signal_conc["exposure_field"] == "sector"]
        industry = signal_conc.loc[signal_conc["exposure_field"] == "industry"]
        triggered = risk_flags.loc[(risk_flags["signal_name"] == signal_name) & (risk_flags["triggered"])]
        peer_quality = peer_quality_exposure.loc[peer_quality_exposure["signal_name"] == signal_name]
        high_peer_share = float(
            peer_quality.loc[
                peer_quality["peer_group_quality_status"].eq("HIGH_CONFIDENCE_INDUSTRY_PEER"),
                "active_observation_share",
            ].sum()
        )
        sector_size_peer_share = float(
            peer_quality.loc[
                peer_quality["peer_group_quality_status"].eq("MEDIUM_CONFIDENCE_SECTOR_SIZE_PEER"),
                "active_observation_share",
            ].sum()
        )
        sector_peer_share = float(
            peer_quality.loc[
                peer_quality["peer_group_quality_status"].eq("MEDIUM_CONFIDENCE_SECTOR_PEER"),
                "active_observation_share",
            ].sum()
        )
        rows.append(
            {
                "signal_name": signal_name,
                "metadata_coverage_ratio": float(
                    coverage.loc[coverage["signal_name"] == signal_name, "metadata_coverage_ratio"].iloc[0]
                ),
                "top_sector": sector["top_group"].iloc[0] if not sector.empty else "",
                "top_sector_share": float(sector["top_share"].iloc[0]) if not sector.empty else 0.0,
                "top_industry": industry["top_group"].iloc[0] if not industry.empty else "",
                "top_industry_share": float(industry["top_share"].iloc[0]) if not industry.empty else 0.0,
                "high_confidence_industry_peer_share": high_peer_share,
                "sector_size_fallback_share": sector_size_peer_share,
                "broad_sector_fallback_share": sector_peer_share,
                "triggered_risk_flags": "|".join(triggered["risk_flag"].tolist()),
                "alpha_validation_allowed": False,
                "peer_relative_transform_allowed": False,
                "production_use_allowed": False,
                "snapshot_warning": SNAPSHOT_WARNING,
                "diagnostic_only": True,
            }
        )
    return pd.DataFrame(rows)


def _append_note(summary: pd.DataFrame, risk_flags: pd.DataFrame, artifacts: dict[str, str]) -> None:
    triggered_count = int(risk_flags["triggered"].sum()) if not risk_flags.empty else 0
    lines = [
        "",
        "## Current Inventory Exposure Audit",
        "",
        f"Audit timestamp: `{_timestamp()}`",
        "",
        "Scope: diagnostic-only exposure audit for current Conditional Alpha Inventory candidates using the complete static economic context layer.",
        "",
        "Audited candidates:",
    ]
    for signal_name in summary["signal_name"]:
        row = summary.loc[summary["signal_name"] == signal_name].iloc[0]
        lines.append(
            f"- `{signal_name}`: top sector `{row['top_sector']}` share `{row['top_sector_share']:.3f}`, "
            f"top industry `{row['top_industry']}` share `{row['top_industry_share']:.3f}`, "
            f"high-confidence industry peer share `{row['high_confidence_industry_peer_share']:.3f}`, "
            f"sector x size fallback share `{row['sector_size_fallback_share']:.3f}`, "
            f"broad sector fallback share `{row['broad_sector_fallback_share']:.3f}`"
        )
    lines.extend(
        [
            "",
            f"Triggered diagnostic risk flags: `{triggered_count}`",
            "",
            "Main limitations:",
            "",
            "- Metadata remains `STATIC_SNAPSHOT_RESEARCH_ONLY`.",
            "- Liquidity and volatility buckets are full-sample descriptive diagnostics, not alpha inputs.",
            "- This audit does not compute sector-conditioned IC and does not unlock peer-relative transforms.",
            "",
            "Produced audit artifacts:",
        ]
    )
    for name, path in sorted(artifacts.items()):
        lines.append(f"- `{name}`: `{path}`")
    lines.extend(
        [
            "",
            "Decision: inventory exposure diagnostics are useful for concentration monitoring, but alpha validation, peer-relative transforms, production use, ML, portfolio, blending, and optimization remain blocked.",
            "",
        ]
    )
    existing = NOTE_PATH.read_text(encoding="utf-8") if NOTE_PATH.exists() else ""
    marker = "\n## Current Inventory Exposure Audit"
    if marker in existing:
        existing = existing.split(marker)[0].rstrip() + "\n"
    with NOTE_PATH.open("w", encoding="utf-8") as handle:
        handle.write(existing)
        handle.write("\n".join(lines))


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    created_at = _timestamp()

    context = _load_context()
    panels, candidate_inventory = _load_inventory_panels()
    exposure = _candidate_ticker_exposure(panels, context)
    exposure_tables = _all_exposures(exposure)
    concentration = _concentration_summary(exposure_tables)
    coverage = _metadata_coverage_by_candidate(exposure)
    risk_flags = _risk_flags(exposure_tables, concentration)
    peer_quality_exposure = _candidate_peer_quality_exposure(exposure)
    peer_quality_flags = _candidate_peer_quality_flags(peer_quality_exposure)
    summary = _audit_summary(coverage, concentration, risk_flags, peer_quality_exposure)

    artifacts = {
        "audited_candidates.csv": candidate_inventory,
        "ticker_context_panel.csv": context,
        "candidate_ticker_active_exposure.csv": exposure,
        "metadata_coverage_by_candidate.csv": coverage,
        "concentration_summary.csv": concentration,
        "hidden_exposure_risk_flags.csv": risk_flags,
        "candidate_peer_quality_exposure.csv": peer_quality_exposure,
        "candidate_peer_quality_flags.csv": peer_quality_flags,
        "inventory_exposure_audit_summary.csv": summary,
    }
    artifacts.update(exposure_tables)

    written = {}
    for name, frame in artifacts.items():
        written[name] = _write_csv(frame, name)

    manifest = {
        "run_id": RUN_ID,
        "created_at": created_at,
        "snapshot_warning": SNAPSHOT_WARNING,
        "diagnostic_only": True,
        "alpha_validation_allowed": False,
        "peer_relative_transform_allowed": False,
        "production_use_allowed": False,
        "metadata_context_dir": str(ECONOMIC_CONTEXT_DIR.relative_to(ROOT)),
        "audited_candidates": list(INVENTORY_PANELS.keys()),
        "artifacts": written,
        "intentional_non_changes": [
            "no_alpha_candidates",
            "no_candidate_status_changes",
            "no_validation_anchor_changes",
            "no_wfv_changes",
            "no_production_changes",
            "no_governance_changes",
            "no_ml_portfolio_blending_optimization",
        ],
    }
    manifest_path = OUT_DIR / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    written["manifest.json"] = str(manifest_path.relative_to(ROOT))

    _append_note(summary, risk_flags, written)
    print(json.dumps({"run_id": RUN_ID, "out_dir": str(OUT_DIR), "note": str(NOTE_PATH)}, indent=2))


if __name__ == "__main__":
    main()
