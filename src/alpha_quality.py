from __future__ import annotations

import numpy as np
import pandas as pd


ALPHA_QUALITY_COLUMNS = [
    "alpha_name",
    "source_signal",
    "horizon",
    "active_pct",
    "missing_pct",
    "finite_pct",
    "active_days_count",
    "avg_active_tickers_per_active_day",
    "n_active_dates",
    "n_total_dates",
    "status",
    "first_valid_date",
    "last_valid_date",
    "regime_filter_description",
]

APPROVED_FOR_ALPHA_SCORING = "APPROVED_FOR_ALPHA_SCORING"
WATCHLIST_ALPHA = "WATCHLIST_ALPHA"
REJECTED_ALPHA_QUALITY = "REJECTED_ALPHA_QUALITY"

ALPHA_STATUS_LABELS = [
    APPROVED_FOR_ALPHA_SCORING,
    WATCHLIST_ALPHA,
    REJECTED_ALPHA_QUALITY,
]


def _finite_mask(df: pd.DataFrame) -> pd.DataFrame:
    numeric = df.apply(pd.to_numeric, errors="coerce")
    return pd.DataFrame(
        np.isfinite(numeric.to_numpy(dtype=float)),
        index=df.index,
        columns=df.columns,
    )


def _assign_status(active_pct: float, finite_pct: float, n_active_dates: int) -> str:
    if (
        pd.notna(active_pct)
        and pd.notna(finite_pct)
        and float(active_pct) >= 0.10
        and float(finite_pct) >= 0.10
        and int(n_active_dates) >= 100
    ):
        return APPROVED_FOR_ALPHA_SCORING

    if (
        pd.notna(active_pct)
        and float(active_pct) >= 0.05
        and int(n_active_dates) >= 50
    ):
        return WATCHLIST_ALPHA

    return REJECTED_ALPHA_QUALITY


def build_alpha_quality_summary(
    alpha_candidates: dict[str, pd.DataFrame],
    alpha_metadata: pd.DataFrame | None = None,
) -> pd.DataFrame:
    """Build structural coverage and finite-value QA for conditional alpha panels."""
    metadata_by_alpha: dict[str, dict[str, object]] = {}
    if alpha_metadata is not None and not alpha_metadata.empty:
        metadata_by_alpha = alpha_metadata.set_index("alpha_name").to_dict("index")

    rows: list[dict[str, object]] = []
    for alpha_name, alpha_df in alpha_candidates.items():
        finite = _finite_mask(alpha_df)
        valid_dates = finite.any(axis=1)
        total_cells = alpha_df.size
        active_tickers_by_date = alpha_df.notna().sum(axis=1)
        active_dates = active_tickers_by_date > 0
        active_cells = active_tickers_by_date.sum()
        active_pct = float(active_cells / total_cells) if total_cells else np.nan
        finite_pct = float(finite.sum().sum() / total_cells) if total_cells else np.nan
        n_active_dates = int(active_dates.sum())
        n_total_dates = int(alpha_df.shape[0])
        metadata = metadata_by_alpha.get(alpha_name, {})

        rows.append(
            {
                "alpha_name": alpha_name,
                "source_signal": metadata.get("source_signal"),
                "horizon": metadata.get("horizon"),
                "active_pct": active_pct,
                "missing_pct": float(alpha_df.isna().sum().sum() / total_cells) if total_cells else np.nan,
                "finite_pct": finite_pct,
                "active_days_count": n_active_dates,
                "avg_active_tickers_per_active_day": (
                    float(active_tickers_by_date[active_dates].mean()) if n_active_dates else 0.0
                ),
                "n_active_dates": n_active_dates,
                "n_total_dates": n_total_dates,
                "status": _assign_status(active_pct, finite_pct, n_active_dates),
                "first_valid_date": alpha_df.index[valid_dates].min() if valid_dates.any() else pd.NaT,
                "last_valid_date": alpha_df.index[valid_dates].max() if valid_dates.any() else pd.NaT,
                "regime_filter_description": metadata.get("regime_filter_description"),
            }
        )

    return pd.DataFrame(rows, columns=ALPHA_QUALITY_COLUMNS)


__all__ = [
    "ALPHA_QUALITY_COLUMNS",
    "ALPHA_STATUS_LABELS",
    "APPROVED_FOR_ALPHA_SCORING",
    "REJECTED_ALPHA_QUALITY",
    "WATCHLIST_ALPHA",
    "build_alpha_quality_summary",
]
