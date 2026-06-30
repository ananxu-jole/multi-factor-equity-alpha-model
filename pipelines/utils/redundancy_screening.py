from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import List

import pandas as pd


# Advisory classes
LOW_METADATA_REDUNDANCY = "LOW_METADATA_REDUNDANCY"
MODERATE_METADATA_REDUNDANCY = "MODERATE_METADATA_REDUNDANCY"
HIGH_METADATA_REDUNDANCY = "HIGH_METADATA_REDUNDANCY"
REVIEW_REQUIRED = "REVIEW_REQUIRED"

STATISTICAL_REDUNDANCY_COLUMNS = [
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

_STRESS_PARTICIPATION_KEYWORDS = (
    r"stress",
    r"participation",
    r"survivor",
    r"freeze",
    r"survivor_freeze",
)


def _contains_keyword(text: str | None, keywords: List[str]) -> bool:
    if not text:
        return False
    txt = text.lower()
    return any(k in txt for k in keywords)


def classify_candidate_metadata(candidate: dict, others: List[dict]) -> tuple[str, List[str], bool, str]:
    """Classify a single candidate given other registry entries.

    Returns: (advisory_class, triggered_checks, review_required, notes)
    """
    cid = candidate.get("candidate_id")
    signal = candidate.get("signal_name", "")
    family = candidate.get("family", "")
    theme = candidate.get("theme", "")
    feature_group = candidate.get("feature_group", "")
    horizon = candidate.get("horizon", "")
    redundancy_risk = (candidate.get("redundancy_risk") or "").lower()

    triggered: List[str] = []
    score = 0
    review_required = False
    notes: List[str] = []

    # Stress/participation contamination
    if _contains_keyword(" ".join([cid or "", signal, theme, feature_group]), list(_STRESS_PARTICIPATION_KEYWORDS)):
        triggered.append("stress_participation_keyword")
        review_required = True
        notes.append("Detected stress/participation keyword in metadata.")

    # Duplicate signal_name
    for o in others:
        if o.get("candidate_id") == cid:
            continue
        if o.get("signal_name") and signal and o.get("signal_name").lower() == signal.lower():
            triggered.append("duplicate_signal_name")
            score += 3
            notes.append(f"Signal name duplicates {o.get('candidate_id')}")
            break

    # family overlap
    fam_overlap = any(o.get("family") == family and o.get("candidate_id") != cid for o in others)
    if fam_overlap:
        triggered.append("family_overlap")
        score += 1

    # theme overlap
    theme_overlap = any(o.get("theme") == theme and o.get("candidate_id") != cid for o in others)
    if theme_overlap:
        triggered.append("theme_overlap")
        score += 2

    # feature_group overlap
    fg_overlap = any(o.get("feature_group") == feature_group and o.get("candidate_id") != cid for o in others)
    if fg_overlap:
        triggered.append("feature_group_overlap")
        score += 2

    # horizon overlap
    hor_overlap = any(o.get("horizon") == horizon and o.get("candidate_id") != cid for o in others)
    if hor_overlap:
        triggered.append("horizon_overlap")
        score += 1

    # redundancy risk flag
    if redundancy_risk in {"medium-high", "high"}:
        triggered.append("flagged_high_redundancy_risk")
        score += 2
        notes.append(f"Declared redundancy_risk={redundancy_risk}")

    # near-duplicate structure: candidate_id similarity
    for o in others:
        if o.get("candidate_id") == cid:
            continue
        # simple near-duplicate: common prefix of candidate_id
        if cid and o.get("candidate_id") and (cid.split("_")[0] == o.get("candidate_id").split("_")[0]):
            triggered.append("candidate_id_prefix_overlap")
            score += 1
            break

    # classification by score and review flag
    if review_required:
        classification = REVIEW_REQUIRED
    else:
        if score >= 4:
            classification = HIGH_METADATA_REDUNDANCY
        elif score >= 2:
            classification = MODERATE_METADATA_REDUNDANCY
        else:
            classification = LOW_METADATA_REDUNDANCY

    return classification, triggered, review_required, "; ".join(notes)


def screen_registry_df(df: pd.DataFrame) -> pd.DataFrame:
    """Run metadata-only redundancy screening on the candidate registry DataFrame.

    Returns a DataFrame with columns: candidate_id, family, theme, horizon,
    feature_group, redundancy_risk, advisory_redundancy_class, triggered_checks,
    review_required, notes
    """
    records = df.to_dict(orient="records")
    out_rows = []

    for rec in records:
        classification, triggered, review_required, notes = classify_candidate_metadata(rec, records)
        out_rows.append(
            {
                "candidate_id": rec.get("candidate_id"),
                "family": rec.get("family"),
                "theme": rec.get("theme"),
                "horizon": rec.get("horizon"),
                "feature_group": rec.get("feature_group"),
                "redundancy_risk": rec.get("redundancy_risk"),
                "advisory_redundancy_class": classification,
                "triggered_checks": ";".join(triggered),
                "review_required": bool(review_required),
                "notes": notes,
            }
        )

    return pd.DataFrame(out_rows)


@dataclass(frozen=True)
class StatisticalRedundancyConfig:
    """Configuration for diagnostic-only cached-panel correlation screening."""

    panel_dir: Path = Path("artifacts/panels/signals")
    lookback_rows: int | None = None
    min_overlap_observations: int = 30


def empty_statistical_redundancy_screening() -> pd.DataFrame:
    return pd.DataFrame(columns=STATISTICAL_REDUNDANCY_COLUMNS)


def _panel_paths(panel_dir: Path, signal_name: str) -> tuple[Path, Path]:
    return panel_dir / f"{signal_name}.parquet", panel_dir / f"{signal_name}.metadata.json"


def _read_panel_metadata(metadata_path: Path) -> dict:
    if not metadata_path.exists():
        return {}
    return json.loads(metadata_path.read_text(encoding="utf-8"))


def _load_cached_panel(panel_dir: Path, signal_name: str) -> tuple[pd.DataFrame | None, dict, Path, str | None]:
    panel_path, metadata_path = _panel_paths(panel_dir, signal_name)
    metadata = _read_panel_metadata(metadata_path)
    if not panel_path.exists():
        return None, metadata, panel_path, f"missing cached panel for {signal_name}"
    panel = pd.read_parquet(panel_path)
    if not isinstance(panel, pd.DataFrame) or panel.empty:
        return None, metadata, panel_path, f"empty cached panel for {signal_name}"
    long_columns = set(panel.columns)
    if {"date", "ticker", "signal_value"}.issubset(long_columns):
        panel = panel.pivot_table(index="date", columns="ticker", values="signal_value", aggfunc="last")
    elif {"Date", "ticker", "signal_value"}.issubset(long_columns):
        panel = panel.pivot_table(index="Date", columns="ticker", values="signal_value", aggfunc="last")
    return panel, metadata, panel_path, None


def _prepare_panel(panel: pd.DataFrame, lookback_rows: int | None) -> pd.DataFrame:
    prepared = panel.copy()
    if lookback_rows is not None and lookback_rows > 0:
        prepared = prepared.tail(lookback_rows)
    prepared.index = pd.to_datetime(prepared.index)
    return prepared.sort_index()


def _aligned_overlap(left: pd.DataFrame, right: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    common_dates = left.index.intersection(right.index)
    common_tickers = left.columns.intersection(right.columns)
    left_aligned = left.loc[common_dates, common_tickers]
    right_aligned = right.loc[common_dates, common_tickers]
    valid = left_aligned.notna() & right_aligned.notna()
    return left_aligned.where(valid), right_aligned.where(valid)


def _flattened_correlation(left: pd.DataFrame, right: pd.DataFrame) -> tuple[float | None, int]:
    left_values = left.stack(future_stack=True).dropna().rename("left")
    right_values = right.stack(future_stack=True).dropna().rename("right")
    pairs = pd.concat([left_values, right_values], axis=1).dropna()
    if len(pairs) < 2:
        return None, len(pairs)
    corr = pairs["left"].corr(pairs["right"])
    if pd.isna(corr):
        return None, len(pairs)
    return float(corr), len(pairs)


def _pairwise_panel_correlation(
    candidate_id: str,
    signal_name: str,
    comparison_signal: str,
    candidate_panel: pd.DataFrame,
    comparison_panel: pd.DataFrame,
    candidate_panel_path: Path,
    comparison_panel_path: Path,
    candidate_metadata: dict,
    comparison_metadata: dict,
    config: StatisticalRedundancyConfig,
) -> dict:
    left = _prepare_panel(candidate_panel, config.lookback_rows)
    right = _prepare_panel(comparison_panel, config.lookback_rows)
    left_overlap, right_overlap = _aligned_overlap(left, right)
    value_correlation, overlap_observations = _flattened_correlation(left_overlap, right_overlap)
    rank_correlation, _ = _flattened_correlation(
        left_overlap.rank(axis=1, pct=True),
        right_overlap.rank(axis=1, pct=True),
    )
    overlap_dates = int((left_overlap.notna() & right_overlap.notna()).any(axis=1).sum())
    overlap_tickers = int((left_overlap.notna() & right_overlap.notna()).any(axis=0).sum())
    status = "computed" if overlap_observations >= config.min_overlap_observations else "insufficient_overlap"

    return {
        "candidate_id": candidate_id,
        "signal_name": signal_name,
        "comparison_signal": comparison_signal,
        "diagnostic_status": status,
        "value_correlation": value_correlation,
        "rank_correlation": rank_correlation,
        "overlap_observations": int(overlap_observations),
        "overlap_dates": overlap_dates,
        "overlap_tickers": overlap_tickers,
        "lookback_rows": config.lookback_rows,
        "candidate_panel_path": str(candidate_panel_path),
        "comparison_panel_path": str(comparison_panel_path),
        "candidate_panel_created_at": candidate_metadata.get("created_at"),
        "comparison_panel_created_at": comparison_metadata.get("created_at"),
        "notes": "diagnostic-only cached-panel correlation; no decisions applied",
    }


def screen_statistical_redundancy_from_cache(
    registry: pd.DataFrame,
    *,
    comparison_signal_names: list[str] | None = None,
    config: StatisticalRedundancyConfig | None = None,
) -> pd.DataFrame:
    """Compute diagnostic-only value/rank correlations from cached signal panels.

    This function reads existing panel cache files only. It does not execute
    discovery, score candidates, validate alpha quality, mutate governance state,
    or apply promotion/demotion thresholds.
    """
    if registry.empty:
        return empty_statistical_redundancy_screening()

    config = config or StatisticalRedundancyConfig()
    panel_dir = Path(config.panel_dir)
    comparison_signal_names = comparison_signal_names or []
    rows: list[dict] = []
    cache: dict[str, tuple[pd.DataFrame | None, dict, Path, str | None]] = {}

    def cached(signal_name: str) -> tuple[pd.DataFrame | None, dict, Path, str | None]:
        if signal_name not in cache:
            cache[signal_name] = _load_cached_panel(panel_dir, signal_name)
        return cache[signal_name]

    for rec in registry.to_dict(orient="records"):
        candidate_id = rec.get("candidate_id")
        signal_name = rec.get("signal_name")
        if not signal_name:
            continue

        candidate_panel, candidate_metadata, candidate_path, candidate_error = cached(signal_name)
        if candidate_error:
            rows.append(
                {
                    "candidate_id": candidate_id,
                    "signal_name": signal_name,
                    "comparison_signal": None,
                    "diagnostic_status": "missing_candidate_panel",
                    "value_correlation": None,
                    "rank_correlation": None,
                    "overlap_observations": 0,
                    "overlap_dates": 0,
                    "overlap_tickers": 0,
                    "lookback_rows": config.lookback_rows,
                    "candidate_panel_path": str(candidate_path),
                    "comparison_panel_path": None,
                    "candidate_panel_created_at": candidate_metadata.get("created_at"),
                    "comparison_panel_created_at": None,
                    "notes": candidate_error,
                }
            )
            continue

        for comparison_signal in comparison_signal_names:
            if comparison_signal == signal_name:
                continue
            comparison_panel, comparison_metadata, comparison_path, comparison_error = cached(comparison_signal)
            if comparison_error:
                rows.append(
                    {
                        "candidate_id": candidate_id,
                        "signal_name": signal_name,
                        "comparison_signal": comparison_signal,
                        "diagnostic_status": "missing_comparison_panel",
                        "value_correlation": None,
                        "rank_correlation": None,
                        "overlap_observations": 0,
                        "overlap_dates": 0,
                        "overlap_tickers": 0,
                        "lookback_rows": config.lookback_rows,
                        "candidate_panel_path": str(candidate_path),
                        "comparison_panel_path": str(comparison_path),
                        "candidate_panel_created_at": candidate_metadata.get("created_at"),
                        "comparison_panel_created_at": comparison_metadata.get("created_at"),
                        "notes": comparison_error,
                    }
                )
                continue

            rows.append(
                _pairwise_panel_correlation(
                    str(candidate_id),
                    signal_name,
                    comparison_signal,
                    candidate_panel,
                    comparison_panel,
                    candidate_path,
                    comparison_path,
                    candidate_metadata,
                    comparison_metadata,
                    config,
                )
            )

    if not rows:
        return empty_statistical_redundancy_screening()
    return pd.DataFrame(rows, columns=STATISTICAL_REDUNDANCY_COLUMNS)
