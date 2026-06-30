from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd


RUN_ID = "economic_context_peer_group_refinement_v1"
SNAPSHOT_WARNING = "STATIC_SNAPSHOT_RESEARCH_ONLY"
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.economic_context.peer_group_builder import (  # noqa: E402
    build_peer_group_fallback_report,
    fallback_hierarchy_summary,
    peer_quality_level_summary,
)


ECONOMIC_CONTEXT_DIR = ROOT / "artifacts" / "research" / "economic_context_enrichment_v1"
OUT_DIR = ECONOMIC_CONTEXT_DIR / "peer_group_refinement"
NOTE_PATH = ROOT / "docs" / "research_notes" / "economic_context_enrichment_v1_implementation.md"


def _timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _write_csv(frame: pd.DataFrame, name: str) -> str:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUT_DIR / name
    frame.to_csv(path, index=False)
    return str(path.relative_to(ROOT))


def _load_metadata() -> pd.DataFrame:
    classification = pd.read_csv(
        ECONOMIC_CONTEXT_DIR / "classification_schema_preview.csv",
        dtype=str,
        keep_default_na=False,
    )
    size = pd.read_csv(
        ECONOMIC_CONTEXT_DIR / "size_schema_preview.csv",
        dtype=str,
        keep_default_na=False,
    )
    return classification.merge(
        size[["ticker", "size_bucket", "market_cap_bucket"]],
        on="ticker",
        how="left",
    )


def _fallback_distance_summary(report: pd.DataFrame) -> pd.DataFrame:
    return (
        report.groupby(["fallback_distance", "peer_group_quality_status"], dropna=False)
        .agg(
            ticker_count=("ticker", "nunique"),
            median_peer_group_size=("fallback_group_size", "median"),
            median_peer_confidence_score=("peer_confidence_score", "median"),
        )
        .reset_index()
        .assign(
            validation_usage_allowed=False,
            peer_relative_transform_allowed=False,
            snapshot_warning=SNAPSHOT_WARNING,
            diagnostic_only=True,
        )
        .sort_values(["fallback_distance", "ticker_count"], ascending=[True, False])
    )


def _peer_confidence_summary(report: pd.DataFrame) -> pd.DataFrame:
    return (
        report.groupby("peer_group_quality_status", dropna=False)
        .agg(
            ticker_count=("ticker", "nunique"),
            median_peer_confidence_score=("peer_confidence_score", "median"),
            median_fallback_distance=("fallback_distance", "median"),
            median_peer_group_size=("fallback_group_size", "median"),
        )
        .reset_index()
        .assign(
            validation_usage_allowed=False,
            peer_relative_transform_allowed=False,
            snapshot_warning=SNAPSHOT_WARNING,
            diagnostic_only=True,
        )
        .sort_values(["ticker_count", "peer_group_quality_status"], ascending=[False, True])
    )


def _append_note(level_summary: pd.DataFrame, artifacts: dict[str, str]) -> None:
    existing = NOTE_PATH.read_text(encoding="utf-8") if NOTE_PATH.exists() else ""
    marker = "\n## Peer Group Refinement v1"
    if marker in existing:
        existing = existing.split(marker)[0].rstrip() + "\n"

    lines = [
        "",
        "## Peer Group Refinement v1",
        "",
        f"Refinement timestamp: `{_timestamp()}`",
        "",
        "Purpose: reduce blind sector-level fallback dependence by adding diagnostic peer quality metrics.",
        "",
        "Fallback hierarchy used for reporting:",
        "",
        "1. industry if the industry peer count is sufficient",
        "2. sector x size if industry is thin and the cross group is sufficient",
        "3. sector if sector x size is thin or unavailable",
        "4. broad size bucket if needed",
        "5. blocked / insufficient peer context",
        "",
        "Peer quality metric definitions:",
        "",
        "- `fallback_distance = 0`: high-confidence industry peer",
        "- `fallback_distance = 1`: medium-confidence broad sector peer",
        "- `fallback_distance = 2`: medium-confidence sector x size peer",
        "- `fallback_distance = 3`: low-confidence broad size fallback",
        "- `fallback_distance = 4`: blocked / insufficient context",
        "",
        "Peer quality distribution:",
    ]
    for row in level_summary.to_dict("records"):
        lines.append(
            f"- `{row['peer_group_quality_status']}` / `{row['assigned_diagnostic_peer_group_level']}`: "
            f"`{row['ticker_count']}` tickers"
        )
    lines.extend(
        [
            "",
            "All peer quality outputs remain diagnostic-only. Static metadata is not point-in-time safe, so peer-relative validation transforms remain blocked.",
            "",
            "Artifacts:",
        ]
    )
    for name, path in sorted(artifacts.items()):
        lines.append(f"- `{name}`: `{path}`")
    lines.append("")

    NOTE_PATH.write_text(existing + "\n".join(lines), encoding="utf-8")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    created_at = _timestamp()
    metadata = _load_metadata()
    report = build_peer_group_fallback_report(metadata)
    level_summary = peer_quality_level_summary(report)
    confidence_summary = _peer_confidence_summary(report)
    distance_summary = _fallback_distance_summary(report)
    fallback_summary = fallback_hierarchy_summary(report)

    artifacts = {
        "peer_group_quality_report.csv": report,
        "peer_group_level_summary.csv": level_summary,
        "peer_confidence_summary.csv": confidence_summary,
        "fallback_distance_summary.csv": distance_summary,
        "fallback_hierarchy_summary_refined.csv": fallback_summary,
    }
    written = {name: _write_csv(frame, name) for name, frame in artifacts.items()}

    manifest = {
        "run_id": RUN_ID,
        "created_at": created_at,
        "snapshot_warning": SNAPSHOT_WARNING,
        "diagnostic_only": True,
        "alpha_validation_allowed": False,
        "peer_relative_transform_allowed": False,
        "production_use_allowed": False,
        "fallback_hierarchy": [
            "industry",
            "sector_size",
            "sector",
            "size",
            "blocked",
        ],
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
    _append_note(level_summary, written)
    print(json.dumps({"run_id": RUN_ID, "out_dir": str(OUT_DIR), "note": str(NOTE_PATH)}, indent=2))


if __name__ == "__main__":
    main()
