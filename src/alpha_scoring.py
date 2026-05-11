from __future__ import annotations

import re

import numpy as np
import pandas as pd

from src.forward_returns import make_forward_returns


APPROVED_FOR_ALPHA_WFV = "APPROVED_FOR_ALPHA_WFV"
WATCHLIST_ALPHA_WFV = "WATCHLIST_ALPHA_WFV"
REJECTED_ALPHA_LOW_SIGNAL = "REJECTED_ALPHA_LOW_SIGNAL"

POSITIVE_EDGE = "POSITIVE_EDGE"
NEGATIVE_EDGE_REVERSE_ALPHA = "NEGATIVE_EDGE_REVERSE_ALPHA"
NO_CLEAR_DIRECTION = "NO_CLEAR_DIRECTION"

STRONG = "STRONG"
MODERATE = "MODERATE"
WEAK = "WEAK"
NO_SIGNAL = "NO_SIGNAL"

ALPHA_SCORING_STATUS_LABELS = [
    APPROVED_FOR_ALPHA_WFV,
    WATCHLIST_ALPHA_WFV,
    REJECTED_ALPHA_LOW_SIGNAL,
]

ALPHA_SCORE_COLUMNS = [
    "alpha_name",
    "horizon",
    "method",
    "n_obs",
    "mean_ic",
    "median_ic",
    "ic_std",
    "ic_ir",
    "hit_rate",
    "positive_ic_rate",
    "missing_pct",
    "alpha_version",
]


def _validate_method(method: str) -> None:
    if method not in {"spearman", "pearson", "kendall"}:
        raise ValueError("method must be one of: spearman, pearson, kendall.")


def _infer_horizon_from_alpha_name(alpha_name: object) -> int | None:
    match = re.search(r"_(\d+)d_", str(alpha_name))
    return int(match.group(1)) if match else None


def _resolve_alpha_horizon(alpha_group: pd.DataFrame, horizons: list[int]) -> int:
    if "horizon" in alpha_group.columns:
        horizon_values = pd.to_numeric(alpha_group["horizon"], errors="coerce").dropna().unique()
        if len(horizon_values) == 1:
            return int(horizon_values[0])

    inferred_horizon = _infer_horizon_from_alpha_name(alpha_group["alpha_name"].iloc[0])
    if inferred_horizon is not None:
        return inferred_horizon

    if len(horizons) == 1:
        return int(horizons[0])

    raise ValueError(
        "alpha_long_df must include a single horizon per alpha_name, or alpha_name must contain '<horizon>d'."
    )


def _pivot_alpha_long_to_panel(alpha_long_df: pd.DataFrame, alpha_name: str) -> pd.DataFrame:
    alpha_rows = alpha_long_df.loc[alpha_long_df["alpha_name"].eq(alpha_name)].copy()
    alpha_rows["Date"] = pd.to_datetime(alpha_rows["Date"], errors="coerce")
    alpha_rows["alpha_value"] = pd.to_numeric(alpha_rows["alpha_value"], errors="coerce")
    alpha_rows = alpha_rows.dropna(subset=["Date", "ticker"])
    return alpha_rows.pivot_table(
        index="Date",
        columns="ticker",
        values="alpha_value",
        aggfunc="last",
    ).sort_index()


def _align_panels(
    alpha_panel: pd.DataFrame,
    fwd_return_panel: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    alpha = alpha_panel.copy()
    fwd = fwd_return_panel.copy()
    alpha.index = pd.to_datetime(alpha.index, errors="coerce")
    fwd.index = pd.to_datetime(fwd.index, errors="coerce")

    common_dates = alpha.index.intersection(fwd.index).sort_values()
    common_tickers = alpha.columns.intersection(fwd.columns).sort_values()
    if common_dates.empty:
        raise ValueError("alpha_panel and fwd_return_panel have no overlapping dates.")
    if common_tickers.empty:
        raise ValueError("alpha_panel and fwd_return_panel have no overlapping tickers.")

    return (
        alpha.reindex(index=common_dates, columns=common_tickers).apply(pd.to_numeric, errors="coerce"),
        fwd.reindex(index=common_dates, columns=common_tickers).apply(pd.to_numeric, errors="coerce"),
    )


def _safe_corr(df: pd.DataFrame, method: str) -> float:
    if len(df) < 2:
        return np.nan
    if df["alpha"].nunique(dropna=True) < 2 or df["fwd_return"].nunique(dropna=True) < 2:
        return np.nan
    return float(df["alpha"].corr(df["fwd_return"], method=method))


def _score_alpha_against_forward_returns(
    alpha_panel: pd.DataFrame,
    fwd_return_panel: pd.DataFrame,
    method: str,
    alpha_name: str,
    horizon: int,
    alpha_version: object = None,
) -> dict[str, object]:
    alpha, fwd = _align_panels(alpha_panel, fwd_return_panel)
    total_cells = int(alpha.size)

    paired = pd.concat(
        [
            alpha.stack(future_stack=True).rename("alpha"),
            fwd.stack(future_stack=True).rename("fwd_return"),
        ],
        axis=1,
    ).dropna()

    n_obs = int(len(paired))
    missing_pct = float(1.0 - n_obs / total_cells) if total_cells else np.nan
    row: dict[str, object] = {
        "alpha_name": alpha_name,
        "horizon": int(horizon),
        "method": method,
        "n_obs": n_obs,
        "mean_ic": np.nan,
        "median_ic": np.nan,
        "ic_std": np.nan,
        "ic_ir": np.nan,
        "hit_rate": np.nan,
        "positive_ic_rate": np.nan,
        "missing_pct": missing_pct,
        "alpha_version": alpha_version,
    }

    if paired.empty:
        return row

    ic_by_date = paired.groupby(level=0, sort=True).apply(_safe_corr, method=method).dropna()
    alpha_sign = np.sign(paired["alpha"])
    return_sign = np.sign(paired["fwd_return"])
    sign_mask = (alpha_sign != 0) & (return_sign != 0)
    row["hit_rate"] = (
        float((alpha_sign[sign_mask] == return_sign[sign_mask]).mean())
        if sign_mask.any()
        else np.nan
    )

    if ic_by_date.empty:
        return row

    mean_ic = float(ic_by_date.mean())
    ic_std = float(ic_by_date.std(ddof=1)) if len(ic_by_date) > 1 else np.nan
    row.update(
        {
            "mean_ic": mean_ic,
            "median_ic": float(ic_by_date.median()),
            "ic_std": ic_std,
            "ic_ir": float(mean_ic / ic_std) if ic_std and not pd.isna(ic_std) else np.nan,
            "positive_ic_rate": float((ic_by_date > 0).mean()),
        }
    )
    return row


def score_alpha_library(
    alpha_long_df: pd.DataFrame,
    close_prices: pd.DataFrame,
    horizons: list[int] | tuple[int, ...],
    method: str = "spearman",
) -> pd.DataFrame:
    """Score alpha candidates against their matching forward-return horizons."""
    _validate_method(method)
    required_columns = {"Date", "ticker", "alpha_name", "alpha_value"}
    missing_columns = required_columns.difference(alpha_long_df.columns)
    if missing_columns:
        raise ValueError(f"alpha_long_df is missing required columns: {sorted(missing_columns)}")

    horizon_values = sorted({int(horizon) for horizon in horizons})
    if not horizon_values:
        raise ValueError("horizons must contain at least one horizon.")

    forward_returns = make_forward_returns(close_prices, horizon_values)
    rows: list[dict[str, object]] = []
    alpha_long = alpha_long_df.copy()

    for alpha_name, alpha_group in alpha_long.groupby("alpha_name", sort=True, dropna=False):
        horizon = _resolve_alpha_horizon(alpha_group, horizon_values)
        if horizon not in forward_returns:
            raise ValueError(f"forward returns are missing alpha horizon {horizon}.")

        alpha_version = (
            alpha_group["alpha_version"].dropna().iloc[0]
            if "alpha_version" in alpha_group.columns and not alpha_group["alpha_version"].dropna().empty
            else None
        )
        alpha_panel = _pivot_alpha_long_to_panel(alpha_long, str(alpha_name))
        rows.append(
            _score_alpha_against_forward_returns(
                alpha_panel=alpha_panel,
                fwd_return_panel=forward_returns[horizon],
                method=method,
                alpha_name=str(alpha_name),
                horizon=horizon,
                alpha_version=alpha_version,
            )
        )

    scores = pd.DataFrame(rows)
    if scores.empty:
        return pd.DataFrame(columns=ALPHA_SCORE_COLUMNS)

    return scores[ALPHA_SCORE_COLUMNS].sort_values(["alpha_name", "horizon"]).reset_index(drop=True)


def interpret_alpha_direction(mean_ic: float | int | None) -> str:
    if pd.isna(mean_ic):
        return NO_CLEAR_DIRECTION
    if float(mean_ic) > 0:
        return POSITIVE_EDGE
    if float(mean_ic) < 0:
        return NEGATIVE_EDGE_REVERSE_ALPHA
    return NO_CLEAR_DIRECTION


def bucket_alpha_strength(mean_ic: float | int | None) -> str:
    if pd.isna(mean_ic):
        return NO_SIGNAL

    abs_mean_ic = abs(float(mean_ic))
    if abs_mean_ic >= 0.03:
        return STRONG
    if abs_mean_ic >= 0.02:
        return MODERATE
    if abs_mean_ic >= 0.012:
        return WEAK
    return NO_SIGNAL


def _assign_alpha_scoring_status(row: pd.Series) -> str:
    mean_ic = row.get("mean_ic")
    ic_ir = row.get("ic_ir")
    n_obs = row.get("n_obs")

    if pd.isna(mean_ic) or pd.isna(n_obs) or int(n_obs) < 10000:
        return REJECTED_ALPHA_LOW_SIGNAL

    abs_mean_ic = abs(float(mean_ic))
    abs_ic_ir = abs(float(ic_ir)) if not pd.isna(ic_ir) else np.nan
    if abs_mean_ic >= 0.025 and not pd.isna(abs_ic_ir) and abs_ic_ir >= 0.10:
        return APPROVED_FOR_ALPHA_WFV

    if abs_mean_ic >= 0.012:
        return WATCHLIST_ALPHA_WFV

    return REJECTED_ALPHA_LOW_SIGNAL


def build_alpha_scoring_gate(scores_df: pd.DataFrame) -> pd.DataFrame:
    """Apply preliminary alpha scoring thresholds before alpha WFV."""
    gated = scores_df.copy()
    if gated.empty:
        return gated.assign(
            abs_mean_ic=pd.Series(dtype=float),
            abs_ic_ir=pd.Series(dtype=float),
            alpha_direction=pd.Series(dtype=object),
            alpha_strength=pd.Series(dtype=object),
            status=pd.Series(dtype=object),
            scoring_gate_notes=pd.Series(dtype=object),
        )

    gated["abs_mean_ic"] = pd.to_numeric(gated["mean_ic"], errors="coerce").abs()
    gated["abs_ic_ir"] = pd.to_numeric(gated["ic_ir"], errors="coerce").abs()
    gated["alpha_direction"] = gated["mean_ic"].map(interpret_alpha_direction)
    gated["alpha_strength"] = gated["mean_ic"].map(bucket_alpha_strength)
    gated["status"] = gated.apply(_assign_alpha_scoring_status, axis=1)
    gated["scoring_gate_notes"] = gated["status"].map(
        {
            APPROVED_FOR_ALPHA_WFV: "Meets alpha IC, IC IR, and observation thresholds for WFV.",
            WATCHLIST_ALPHA_WFV: "Meets alpha watchlist IC and observation thresholds for WFV.",
            REJECTED_ALPHA_LOW_SIGNAL: "Fails preliminary alpha predictive scoring thresholds.",
        }
    )
    return gated


def build_alpha_best_horizon_summary(scores_df: pd.DataFrame) -> pd.DataFrame:
    """Select each alpha's best scored horizon by highest absolute mean IC."""
    columns = [
        "alpha_name",
        "best_horizon",
        "best_mean_ic",
        "best_abs_mean_ic",
        "best_ic_ir",
        "best_positive_ic_rate",
        "best_hit_rate",
        "alpha_direction",
        "alpha_strength",
        "alpha_version",
    ]
    if scores_df.empty:
        return pd.DataFrame(columns=columns)

    scores = scores_df.copy()
    scores["abs_mean_ic"] = pd.to_numeric(scores["mean_ic"], errors="coerce").abs()
    sortable = scores.dropna(subset=["alpha_name", "abs_mean_ic"])
    if sortable.empty:
        return pd.DataFrame(columns=columns)

    best_idx = sortable.groupby("alpha_name")["abs_mean_ic"].idxmax()
    best = scores.loc[best_idx].copy()
    output = pd.DataFrame(
        {
            "alpha_name": best["alpha_name"],
            "best_horizon": best["horizon"],
            "best_mean_ic": best["mean_ic"],
            "best_abs_mean_ic": best["abs_mean_ic"],
            "best_ic_ir": best["ic_ir"],
            "best_positive_ic_rate": best["positive_ic_rate"],
            "best_hit_rate": best["hit_rate"],
            "alpha_direction": best["mean_ic"].map(interpret_alpha_direction),
            "alpha_strength": best["mean_ic"].map(bucket_alpha_strength),
            "alpha_version": best["alpha_version"] if "alpha_version" in best.columns else None,
        }
    )
    return output[columns].sort_values("best_abs_mean_ic", ascending=False).reset_index(drop=True)


__all__ = [
    "ALPHA_SCORE_COLUMNS",
    "ALPHA_SCORING_STATUS_LABELS",
    "APPROVED_FOR_ALPHA_WFV",
    "MODERATE",
    "NEGATIVE_EDGE_REVERSE_ALPHA",
    "NO_CLEAR_DIRECTION",
    "NO_SIGNAL",
    "POSITIVE_EDGE",
    "REJECTED_ALPHA_LOW_SIGNAL",
    "STRONG",
    "WATCHLIST_ALPHA_WFV",
    "WEAK",
    "bucket_alpha_strength",
    "build_alpha_best_horizon_summary",
    "build_alpha_scoring_gate",
    "interpret_alpha_direction",
    "score_alpha_library",
]
