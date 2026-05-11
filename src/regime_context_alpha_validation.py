from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.alpha_scoring import score_alpha_library
from src.db import load_table


APPROVED_FOR_REGIME_CONTEXT_WFV = "APPROVED_FOR_REGIME_CONTEXT_WFV"


def load_regime_context_alpha_validation_inputs(
    db_path: str | Path | None = None,
) -> dict[str, pd.DataFrame]:
    """Load current Notebook 05 regime-context alpha artifacts for Notebook 06 validation."""
    return {
        "alpha_long": load_table("regime_context_alpha_candidates_current", db_path=db_path),
        "quality": load_table("regime_context_alpha_quality_current", db_path=db_path),
        "metadata": load_table("regime_context_alpha_metadata_current", db_path=db_path),
        "diagnostics": load_table("regime_context_alpha_diagnostics_current", db_path=db_path),
        "activation": load_table("regime_context_alpha_activation_current", db_path=db_path),
    }


def select_approved_regime_context_alphas(
    quality: pd.DataFrame,
    metadata: pd.DataFrame | None = None,
) -> pd.DataFrame:
    """Return Notebook 05 overlay candidates approved for Notebook 06 validation."""
    approved = quality.loc[quality["status"].eq(APPROVED_FOR_REGIME_CONTEXT_WFV)].copy()
    if metadata is not None and not metadata.empty:
        metadata_columns = [
            "alpha_name",
            "overlay_type",
            "base_alpha_name",
            "source_alpha_wfv_status",
            "source_alpha_wfv_horizon",
            "source_effective_mean_test_ic",
            "source_persistence_ratio",
        ]
        available_columns = [column for column in metadata_columns if column in metadata.columns]
        approved = approved.merge(
            metadata[available_columns].drop_duplicates("alpha_name"),
            on="alpha_name",
            how="left",
        )
    return approved.sort_values("alpha_name").reset_index(drop=True)


def prepare_regime_context_alpha_scoring_input(
    alpha_long: pd.DataFrame,
    approved_quality: pd.DataFrame,
    regime_context_version_column: str = "regime_context_version",
) -> pd.DataFrame:
    """Filter long alpha observations to approved regime-context alpha candidates."""
    approved_names = approved_quality["alpha_name"].dropna().astype(str).unique().tolist()
    scoring_input = alpha_long.loc[alpha_long["alpha_name"].isin(approved_names)].copy()
    if regime_context_version_column in scoring_input.columns:
        scoring_input["alpha_version"] = scoring_input[regime_context_version_column]
    return scoring_input


def score_regime_context_alpha_library(
    alpha_long_df: pd.DataFrame,
    close_prices: pd.DataFrame,
    horizons: list[int] | tuple[int, ...],
    method: str = "spearman",
) -> pd.DataFrame:
    """Score horizon-agnostic regime-context alpha panels across multiple horizons."""
    scores: list[pd.DataFrame] = []
    for horizon in sorted({int(value) for value in horizons}):
        alpha_for_horizon = alpha_long_df.copy()
        alpha_for_horizon["horizon"] = int(horizon)
        horizon_scores = score_alpha_library(
            alpha_long_df=alpha_for_horizon,
            close_prices=close_prices,
            horizons=[int(horizon)],
            method=method,
        )
        scores.append(horizon_scores)

    if not scores:
        return pd.DataFrame()

    return pd.concat(scores, ignore_index=True).sort_values(["alpha_name", "horizon"]).reset_index(drop=True)


__all__ = [
    "APPROVED_FOR_REGIME_CONTEXT_WFV",
    "load_regime_context_alpha_validation_inputs",
    "prepare_regime_context_alpha_scoring_input",
    "score_regime_context_alpha_library",
    "select_approved_regime_context_alphas",
]
