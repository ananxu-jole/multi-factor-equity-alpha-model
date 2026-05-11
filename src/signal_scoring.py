from __future__ import annotations

import numpy as np
import pandas as pd


APPROVED_FOR_WFV = "APPROVED_FOR_WFV"
WATCHLIST = "WATCHLIST"
REJECTED_LOW_SIGNAL = "REJECTED_LOW_SIGNAL"

POSITIVE_EDGE = "POSITIVE_EDGE"
NEGATIVE_EDGE_REVERSE_SIGNAL = "NEGATIVE_EDGE_REVERSE_SIGNAL"
NO_CLEAR_DIRECTION = "NO_CLEAR_DIRECTION"

STRONG = "STRONG"
MODERATE = "MODERATE"
WEAK = "WEAK"
NO_SIGNAL = "NO_SIGNAL"

SCORING_STATUS_LABELS = [
    APPROVED_FOR_WFV,
    WATCHLIST,
    REJECTED_LOW_SIGNAL,
]


def _align_signal_and_forward_return_panels(
    signal_panel: pd.DataFrame,
    fwd_return_panel: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    if not isinstance(signal_panel, pd.DataFrame):
        raise TypeError("signal_panel must be a pandas DataFrame.")
    if not isinstance(fwd_return_panel, pd.DataFrame):
        raise TypeError("fwd_return_panel must be a pandas DataFrame.")

    signal = signal_panel.copy()
    fwd = fwd_return_panel.copy()
    signal.index = pd.to_datetime(signal.index, errors="coerce")
    fwd.index = pd.to_datetime(fwd.index, errors="coerce")

    if signal.index.isna().any() or fwd.index.isna().any():
        raise ValueError("signal_panel and fwd_return_panel indexes must be date-like.")

    common_dates = signal.index.intersection(fwd.index).sort_values()
    common_tickers = signal.columns.intersection(fwd.columns).sort_values()
    if common_dates.empty:
        raise ValueError("signal_panel and fwd_return_panel have no overlapping dates.")
    if common_tickers.empty:
        raise ValueError("signal_panel and fwd_return_panel have no overlapping ticker columns.")

    signal_aligned = signal.reindex(index=common_dates, columns=common_tickers)
    fwd_aligned = fwd.reindex(index=common_dates, columns=common_tickers)
    return (
        signal_aligned.apply(pd.to_numeric, errors="coerce"),
        fwd_aligned.apply(pd.to_numeric, errors="coerce"),
    )


def _safe_corr(df: pd.DataFrame, method: str) -> float:
    if len(df) < 2:
        return np.nan
    if df["signal"].nunique(dropna=True) < 2 or df["fwd_return"].nunique(dropna=True) < 2:
        return np.nan
    return float(df["signal"].corr(df["fwd_return"], method=method))


def score_signal_against_forward_returns(
    signal_panel: pd.DataFrame,
    fwd_return_panel: pd.DataFrame,
    method: str = "spearman",
    min_obs: int = 1000,
    signal_name: str | None = None,
    horizon: int | None = None,
) -> dict[str, object]:
    """
    Score one signal against one forward return horizon using date-level cross-sectional IC.

    IC is computed cross-sectionally within each Date, then summarized across dates.
    """
    if method not in {"spearman", "pearson", "kendall"}:
        raise ValueError("method must be one of: spearman, pearson, kendall.")
    if min_obs < 0:
        raise ValueError("min_obs must be non-negative.")

    signal, fwd = _align_signal_and_forward_return_panels(signal_panel, fwd_return_panel)
    total_cells = int(signal.size)

    paired = pd.concat(
        [
            signal.stack(future_stack=True).rename("signal"),
            fwd.stack(future_stack=True).rename("fwd_return"),
        ],
        axis=1,
    ).dropna()

    n_obs = int(len(paired))
    missing_pct = float(1.0 - n_obs / total_cells) if total_cells else np.nan

    result: dict[str, object] = {
        "signal_name": signal_name,
        "horizon": horizon,
        "method": method,
        "n_obs": n_obs,
        "mean_ic": np.nan,
        "median_ic": np.nan,
        "ic_std": np.nan,
        "ic_ir": np.nan,
        "hit_rate": np.nan,
        "positive_ic_rate": np.nan,
        "missing_pct": missing_pct,
    }

    if n_obs < min_obs:
        return result

    ic_by_date = paired.groupby(level=0, sort=True).apply(_safe_corr, method=method)
    ic_by_date = ic_by_date.dropna()

    signal_sign = np.sign(paired["signal"])
    return_sign = np.sign(paired["fwd_return"])
    sign_mask = (signal_sign != 0) & (return_sign != 0)
    hit_rate = (
        float((signal_sign[sign_mask] == return_sign[sign_mask]).mean())
        if sign_mask.any()
        else np.nan
    )

    if ic_by_date.empty:
        result["hit_rate"] = hit_rate
        return result

    mean_ic = float(ic_by_date.mean())
    ic_std = float(ic_by_date.std(ddof=1)) if len(ic_by_date) > 1 else np.nan
    result.update(
        {
            "mean_ic": mean_ic,
            "median_ic": float(ic_by_date.median()),
            "ic_std": ic_std,
            "ic_ir": float(mean_ic / ic_std) if ic_std and not pd.isna(ic_std) else np.nan,
            "hit_rate": hit_rate,
            "positive_ic_rate": float((ic_by_date > 0).mean()),
        }
    )
    return result


def score_signal_library_multi_horizon(
    signals: dict[str, pd.DataFrame],
    forward_returns: dict[int, pd.DataFrame],
    metadata: pd.DataFrame | None = None,
    horizons: list[int] | tuple[int, ...] = (1, 5, 10, 20),
    method: str = "spearman",
    min_obs: int = 1000,
) -> pd.DataFrame:
    """Score a library of signal panels against multiple forward return horizons."""
    rows: list[dict[str, object]] = []
    metadata_by_signal: dict[str, dict[str, object]] = {}
    if metadata is not None and not metadata.empty and "signal_name" in metadata.columns:
        metadata_by_signal = metadata.set_index("signal_name").to_dict(orient="index")

    for signal_name, signal_panel in signals.items():
        signal_metadata = metadata_by_signal.get(signal_name, {})
        for horizon in horizons:
            if horizon not in forward_returns:
                raise ValueError(f"forward_returns is missing horizon {horizon}.")
            row = score_signal_against_forward_returns(
                signal_panel=signal_panel,
                fwd_return_panel=forward_returns[horizon],
                method=method,
                min_obs=min_obs,
                signal_name=signal_name,
                horizon=int(horizon),
            )
            for key, value in signal_metadata.items():
                if key not in row:
                    row[key] = value
            rows.append(row)

    scores = pd.DataFrame(rows)
    if scores.empty:
        return scores

    leading_columns = [
        "signal_name",
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
    ]
    remaining_columns = [column for column in scores.columns if column not in leading_columns]
    return scores[leading_columns + remaining_columns].sort_values(
        ["signal_name", "horizon"]
    ).reset_index(drop=True)


def build_signal_score_summary(scores_df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate per-horizon scoring rows to one preliminary summary row per signal."""
    if scores_df.empty:
        return pd.DataFrame(
            columns=[
                "signal_name",
                "n_horizons_scored",
                "best_horizon",
                "best_abs_mean_ic",
                "best_mean_ic",
                "mean_abs_mean_ic",
                "avg_positive_ic_rate",
                "avg_hit_rate",
                "max_n_obs",
                "avg_missing_pct",
            ]
        )

    scores = scores_df.copy()
    scores["abs_mean_ic"] = scores["mean_ic"].abs()
    best_idx = scores.groupby("signal_name")["abs_mean_ic"].idxmax()
    best_rows = scores.loc[best_idx, ["signal_name", "horizon", "abs_mean_ic", "mean_ic"]].rename(
        columns={
            "horizon": "best_horizon",
            "abs_mean_ic": "best_abs_mean_ic",
            "mean_ic": "best_mean_ic",
        }
    )

    summary = (
        scores.groupby("signal_name", dropna=False)
        .agg(
            n_horizons_scored=("horizon", "nunique"),
            mean_abs_mean_ic=("abs_mean_ic", "mean"),
            avg_positive_ic_rate=("positive_ic_rate", "mean"),
            avg_hit_rate=("hit_rate", "mean"),
            max_n_obs=("n_obs", "max"),
            avg_missing_pct=("missing_pct", "mean"),
        )
        .reset_index()
        .merge(best_rows, on="signal_name", how="left")
    )
    columns = [
        "signal_name",
        "n_horizons_scored",
        "best_horizon",
        "best_abs_mean_ic",
        "best_mean_ic",
        "mean_abs_mean_ic",
        "avg_positive_ic_rate",
        "avg_hit_rate",
        "max_n_obs",
        "avg_missing_pct",
    ]
    return summary[columns].sort_values("best_abs_mean_ic", ascending=False).reset_index(drop=True)


def interpret_signal_direction(mean_ic: float | int | None) -> str:
    """Interpret signal direction while preserving negative IC as a reversible edge."""
    if pd.isna(mean_ic):
        return NO_CLEAR_DIRECTION
    if float(mean_ic) > 0:
        return POSITIVE_EDGE
    if float(mean_ic) < 0:
        return NEGATIVE_EDGE_REVERSE_SIGNAL
    return NO_CLEAR_DIRECTION


def bucket_signal_strength(mean_ic: float | int | None) -> str:
    """Bucket signal strength using absolute mean IC."""
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


def _assign_preliminary_status(
    row: pd.Series,
    min_abs_mean_ic: float,
    min_abs_ic_ir: float,
    positive_ic_rate_upper: float,
    positive_ic_rate_lower: float,
    watchlist_abs_mean_ic: float,
    min_n_obs: int,
) -> str:
    mean_ic = row.get("mean_ic")
    ic_ir = row.get("ic_ir")
    positive_ic_rate = row.get("positive_ic_rate")
    n_obs = row.get("n_obs")

    if pd.isna(mean_ic) or pd.isna(n_obs) or int(n_obs) < min_n_obs:
        return REJECTED_LOW_SIGNAL

    abs_mean_ic = abs(float(mean_ic))
    abs_ic_ir = abs(float(ic_ir)) if not pd.isna(ic_ir) else np.nan
    directional_consistency = (
        not pd.isna(positive_ic_rate)
        and (
            float(positive_ic_rate) >= positive_ic_rate_upper
            or float(positive_ic_rate) <= positive_ic_rate_lower
        )
    )

    if (
        abs_mean_ic >= min_abs_mean_ic
        and not pd.isna(abs_ic_ir)
        and abs_ic_ir >= min_abs_ic_ir
        and directional_consistency
    ):
        return APPROVED_FOR_WFV

    if abs_mean_ic >= watchlist_abs_mean_ic:
        return WATCHLIST

    return REJECTED_LOW_SIGNAL


def apply_preliminary_scoring_gate(
    scores_df: pd.DataFrame,
    min_abs_mean_ic: float = 0.025,
    min_abs_ic_ir: float = 0.10,
    positive_ic_rate_upper: float = 0.53,
    positive_ic_rate_lower: float = 0.47,
    watchlist_abs_mean_ic: float = 0.012,
    min_n_obs: int = 10000,
) -> pd.DataFrame:
    """Apply a preliminary scoring gate to signal x horizon score rows."""
    gated = scores_df.copy()
    gated["abs_mean_ic"] = gated["mean_ic"].abs()
    gated["abs_ic_ir"] = gated["ic_ir"].abs()
    gated["signal_direction"] = gated["mean_ic"].map(interpret_signal_direction)
    gated["signal_strength"] = gated["mean_ic"].map(bucket_signal_strength)
    gated["status"] = gated.apply(
        _assign_preliminary_status,
        axis=1,
        min_abs_mean_ic=min_abs_mean_ic,
        min_abs_ic_ir=min_abs_ic_ir,
        positive_ic_rate_upper=positive_ic_rate_upper,
        positive_ic_rate_lower=positive_ic_rate_lower,
        watchlist_abs_mean_ic=watchlist_abs_mean_ic,
        min_n_obs=min_n_obs,
    )
    gated["scoring_gate_notes"] = gated["status"].map(
        {
            APPROVED_FOR_WFV: "Meets preliminary absolute IC, IC IR, directional consistency, and observation thresholds.",
            WATCHLIST: "Meets watchlist absolute IC and observation thresholds.",
            REJECTED_LOW_SIGNAL: "Fails preliminary predictive scoring thresholds.",
        }
    )
    return gated


def build_best_horizon_summary(scores_df: pd.DataFrame) -> pd.DataFrame:
    """Select each signal's best horizon by highest absolute mean IC."""
    columns = [
        "signal_name",
        "signal_family",
        "best_horizon",
        "best_mean_ic",
        "best_abs_mean_ic",
        "best_ic_ir",
        "best_positive_ic_rate",
        "best_hit_rate",
        "signal_direction",
        "signal_strength",
    ]
    if scores_df.empty:
        return pd.DataFrame(columns=columns)

    scores = scores_df.copy()
    scores["abs_mean_ic"] = scores["mean_ic"].abs()
    sortable = scores.dropna(subset=["signal_name", "abs_mean_ic"])
    if sortable.empty:
        return pd.DataFrame(columns=columns)

    best_idx = sortable.groupby("signal_name")["abs_mean_ic"].idxmax()
    best = scores.loc[best_idx].copy()
    output = pd.DataFrame(
        {
            "signal_name": best["signal_name"],
            "signal_family": best["signal_family"] if "signal_family" in best.columns else np.nan,
            "best_horizon": best["horizon"],
            "best_mean_ic": best["mean_ic"],
            "best_abs_mean_ic": best["abs_mean_ic"],
            "best_ic_ir": best["ic_ir"],
            "best_positive_ic_rate": best["positive_ic_rate"],
            "best_hit_rate": best["hit_rate"],
            "signal_direction": best["mean_ic"].map(interpret_signal_direction),
            "signal_strength": best["mean_ic"].map(bucket_signal_strength),
        }
    )
    return output[columns].sort_values("best_abs_mean_ic", ascending=False).reset_index(drop=True)


def build_scoring_family_summary(scores_df: pd.DataFrame) -> pd.DataFrame:
    """Summarize scoring strength by signal family."""
    columns = [
        "signal_family",
        "n_signal_horizons",
        "avg_abs_mean_ic",
        "max_abs_mean_ic",
        "best_signal_name",
        "best_horizon",
    ]
    if scores_df.empty:
        return pd.DataFrame(columns=columns)
    if "signal_family" not in scores_df.columns:
        raise ValueError("scores_df must include signal_family to build family summary.")

    scores = scores_df.copy()
    scores["abs_mean_ic"] = scores["mean_ic"].abs()
    sortable = scores.dropna(subset=["signal_family", "abs_mean_ic"])
    if sortable.empty:
        return pd.DataFrame(columns=columns)

    best_idx = sortable.groupby("signal_family")["abs_mean_ic"].idxmax()
    best = sortable.loc[best_idx, ["signal_family", "signal_name", "horizon", "abs_mean_ic"]].rename(
        columns={
            "signal_name": "best_signal_name",
            "horizon": "best_horizon",
            "abs_mean_ic": "max_abs_mean_ic",
        }
    )
    summary = (
        scores.groupby("signal_family", dropna=False)
        .agg(
            n_signal_horizons=("signal_name", "size"),
            avg_abs_mean_ic=("abs_mean_ic", "mean"),
        )
        .reset_index()
        .merge(best, on="signal_family", how="left")
    )
    return summary[columns].sort_values("max_abs_mean_ic", ascending=False).reset_index(drop=True)


__all__ = [
    "APPROVED_FOR_WFV",
    "MODERATE",
    "NEGATIVE_EDGE_REVERSE_SIGNAL",
    "NO_CLEAR_DIRECTION",
    "NO_SIGNAL",
    "POSITIVE_EDGE",
    "REJECTED_LOW_SIGNAL",
    "SCORING_STATUS_LABELS",
    "STRONG",
    "WATCHLIST",
    "WEAK",
    "apply_preliminary_scoring_gate",
    "bucket_signal_strength",
    "build_best_horizon_summary",
    "build_scoring_family_summary",
    "build_signal_score_summary",
    "interpret_signal_direction",
    "score_signal_against_forward_returns",
    "score_signal_library_multi_horizon",
]
