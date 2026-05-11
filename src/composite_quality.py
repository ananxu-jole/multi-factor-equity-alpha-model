from __future__ import annotations

import numpy as np
import pandas as pd


APPROVED_FOR_COMPOSITE_SCORING = "APPROVED_FOR_COMPOSITE_SCORING"
WATCHLIST_COMPOSITE = "WATCHLIST_COMPOSITE"
REJECTED_COMPOSITE_QUALITY = "REJECTED_COMPOSITE_QUALITY"


def _finite_mask(df: pd.DataFrame) -> pd.DataFrame:
    numeric = df.apply(pd.to_numeric, errors="coerce")
    return pd.DataFrame(
        np.isfinite(numeric.to_numpy(dtype=float)),
        index=df.index,
        columns=df.columns,
    )


def _assign_status(finite_pct: float) -> str:
    if pd.isna(finite_pct):
        return REJECTED_COMPOSITE_QUALITY
    if finite_pct >= 0.85:
        return APPROVED_FOR_COMPOSITE_SCORING
    if finite_pct >= 0.70:
        return WATCHLIST_COMPOSITE
    return REJECTED_COMPOSITE_QUALITY


def build_composite_quality_report(
    composite_signals: dict[str, pd.DataFrame],
    metadata: pd.DataFrame,
) -> pd.DataFrame:
    """Build per-composite structural coverage and quality status report."""
    component_counts = (
        metadata.set_index("composite_name")["n_components"].to_dict()
        if metadata is not None and not metadata.empty
        else {}
    )
    rows: list[dict[str, object]] = []

    for composite_name, composite_df in composite_signals.items():
        finite = _finite_mask(composite_df)
        valid_dates = finite.any(axis=1)
        total_cells = composite_df.size
        finite_pct = float(finite.sum().sum() / total_cells) if total_cells else np.nan
        missing_pct = float(composite_df.isna().sum().sum() / total_cells) if total_cells else np.nan

        rows.append(
            {
                "composite_name": composite_name,
                "n_components": int(component_counts.get(composite_name, 0)),
                "n_dates": int(composite_df.shape[0]),
                "n_tickers": int(composite_df.shape[1]),
                "finite_pct": finite_pct,
                "missing_pct": missing_pct,
                "first_valid_date": composite_df.index[valid_dates].min() if valid_dates.any() else pd.NaT,
                "last_valid_date": composite_df.index[valid_dates].max() if valid_dates.any() else pd.NaT,
                "status": _assign_status(finite_pct),
            }
        )

    return pd.DataFrame(
        rows,
        columns=[
            "composite_name",
            "n_components",
            "n_dates",
            "n_tickers",
            "finite_pct",
            "missing_pct",
            "first_valid_date",
            "last_valid_date",
            "status",
        ],
    )


__all__ = [
    "APPROVED_FOR_COMPOSITE_SCORING",
    "REJECTED_COMPOSITE_QUALITY",
    "WATCHLIST_COMPOSITE",
    "build_composite_quality_report",
]
