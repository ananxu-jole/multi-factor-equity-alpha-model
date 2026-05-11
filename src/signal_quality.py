from __future__ import annotations

import numpy as np
import pandas as pd


SIGNAL_QUALITY_COLUMNS = [
    "signal_name",
    "signal_family",
    "n_dates",
    "n_tickers",
    "missing_pct",
    "finite_pct",
    "first_valid_date",
    "last_valid_date",
    "run_id",
    "signal_version",
]


APPROVED_FOR_SCORING = "APPROVED_FOR_SCORING"
WATCHLIST = "WATCHLIST"
REJECTED_DATA_QUALITY = "REJECTED_DATA_QUALITY"

SIGNAL_STATUS_LABELS = [
    APPROVED_FOR_SCORING,
    WATCHLIST,
    REJECTED_DATA_QUALITY,
]

SIGNAL_FAMILY_SUMMARY_COLUMNS = [
    "signal_family",
    "n_signals",
    "avg_missing_pct",
    "avg_finite_pct",
    "min_first_valid_date",
    "max_first_valid_date",
]


def _finite_mask(df: pd.DataFrame) -> pd.DataFrame:
    numeric = df.apply(pd.to_numeric, errors="coerce")
    return pd.DataFrame(
        np.isfinite(numeric.to_numpy(dtype=float)),
        index=df.index,
        columns=df.columns,
    )


def build_signal_quality_summary(
    signals: dict[str, pd.DataFrame],
    metadata: pd.DataFrame,
    run_id: str,
    signal_version: str,
) -> pd.DataFrame:
    """Build per-signal coverage and finite-value quality summaries."""
    family_by_signal = metadata.set_index("signal_name")["signal_family"].to_dict()
    rows: list[dict[str, object]] = []

    for signal_name, signal_df in signals.items():
        finite = _finite_mask(signal_df)
        valid_dates = finite.any(axis=1)
        total_cells = signal_df.size

        rows.append(
            {
                "signal_name": signal_name,
                "signal_family": family_by_signal.get(signal_name),
                "n_dates": int(signal_df.shape[0]),
                "n_tickers": int(signal_df.shape[1]),
                "missing_pct": float(signal_df.isna().sum().sum() / total_cells) if total_cells else np.nan,
                "finite_pct": float(finite.sum().sum() / total_cells) if total_cells else np.nan,
                "first_valid_date": signal_df.index[valid_dates].min() if valid_dates.any() else pd.NaT,
                "last_valid_date": signal_df.index[valid_dates].max() if valid_dates.any() else pd.NaT,
                "run_id": run_id,
                "signal_version": signal_version,
            }
        )

    return pd.DataFrame(rows, columns=SIGNAL_QUALITY_COLUMNS)


def _assign_status(
    row: pd.Series,
    min_finite_pct: float,
    max_missing_pct: float,
    min_dates: int,
) -> str:
    finite_pct = row.get("finite_pct")
    missing_pct = row.get("missing_pct")
    n_dates = row.get("n_dates")

    if pd.isna(finite_pct) or pd.isna(missing_pct) or pd.isna(n_dates) or int(n_dates) < min_dates:
        return REJECTED_DATA_QUALITY

    if float(finite_pct) >= min_finite_pct and float(missing_pct) <= max_missing_pct:
        return APPROVED_FOR_SCORING

    watchlist_finite_floor = min_finite_pct * 0.90
    watchlist_missing_ceiling = max_missing_pct * 1.50
    if float(finite_pct) >= watchlist_finite_floor and float(missing_pct) <= watchlist_missing_ceiling:
        return WATCHLIST

    return REJECTED_DATA_QUALITY


def filter_signal_quality(
    quality_df: pd.DataFrame,
    min_finite_pct: float = 0.95,
    max_missing_pct: float = 0.10,
    min_dates: int = 1000,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Apply structural quality gates and return approved and non-approved signals."""
    gated = quality_df.copy()
    gated["status"] = gated.apply(
        _assign_status,
        axis=1,
        min_finite_pct=min_finite_pct,
        max_missing_pct=max_missing_pct,
        min_dates=min_dates,
    )
    gated["quality_gate_notes"] = gated["status"].map(
        {
            APPROVED_FOR_SCORING: "Meets structural coverage thresholds.",
            WATCHLIST: "Near threshold; keep visible but exclude from default scoring set.",
            REJECTED_DATA_QUALITY: "Fails structural data quality thresholds.",
        }
    )

    approved_quality = gated[gated["status"] == APPROVED_FOR_SCORING].reset_index(drop=True)
    rejected_quality = gated[gated["status"] != APPROVED_FOR_SCORING].reset_index(drop=True)
    return approved_quality, rejected_quality


def build_signal_family_summary(quality_df: pd.DataFrame) -> pd.DataFrame:
    """Summarize candidate signal quality by signal family."""
    quality = quality_df.copy()
    quality["first_valid_date"] = pd.to_datetime(quality["first_valid_date"], errors="coerce")

    summary = (
        quality.groupby("signal_family", dropna=False)
        .agg(
            n_signals=("signal_name", "nunique"),
            avg_missing_pct=("missing_pct", "mean"),
            avg_finite_pct=("finite_pct", "mean"),
            min_first_valid_date=("first_valid_date", "min"),
            max_first_valid_date=("first_valid_date", "max"),
        )
        .reset_index()
    )
    return summary[SIGNAL_FAMILY_SUMMARY_COLUMNS]


__all__ = [
    "APPROVED_FOR_SCORING",
    "REJECTED_DATA_QUALITY",
    "SIGNAL_FAMILY_SUMMARY_COLUMNS",
    "SIGNAL_QUALITY_COLUMNS",
    "SIGNAL_STATUS_LABELS",
    "WATCHLIST",
    "build_signal_family_summary",
    "build_signal_quality_summary",
    "filter_signal_quality",
]
