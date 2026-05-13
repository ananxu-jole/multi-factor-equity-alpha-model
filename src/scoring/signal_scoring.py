from __future__ import annotations

from contextlib import nullcontext, redirect_stdout
from datetime import datetime, timezone
from io import StringIO
from pathlib import Path

import numpy as np
import pandas as pd

from src.db import load_price_table
from src.forward_returns import make_forward_returns, validate_forward_return_panels
from src.signal_storage import (
    load_and_pivot_signal_panels_by_names,
    load_candidate_signal_quality_gate,
)


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
APPROVED_FOR_SCORING = "APPROVED_FOR_SCORING"
SCORING_VERSION = "phase2_signal_scoring_v2"
HORIZONS = [1, 5, 10, 20]
IC_METHOD = "spearman"
MIN_SCORE_OBS = 1000
MIN_GATE_OBS = 10000
GATE_MIN_ABS_MEAN_IC = 0.025
GATE_MIN_ABS_IC_IR = 0.10
GATE_POSITIVE_IC_RATE_UPPER = 0.53
GATE_POSITIVE_IC_RATE_LOWER = 0.47
GATE_WATCHLIST_ABS_MEAN_IC = 0.012
REQUIRED_INPUT_TABLES = (
    "candidate_signals_current",
    "candidate_signal_quality_gate_current",
    "clean_close_prices_current",
)


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


def _make_scoring_run_context(run_id: str | None = None) -> tuple[str, str]:
    run_timestamp = datetime.now(timezone.utc).replace(microsecond=0)
    resolved_run_id = run_id or f"signal_scoring_{run_timestamp.strftime('%Y%m%d_%H%M%S')}"
    return resolved_run_id, run_timestamp.isoformat()


def select_approved_scoring_candidates(quality_gate: pd.DataFrame) -> pd.DataFrame:
    """Return notebook-equivalent APPROVED_FOR_SCORING rows from the quality gate."""
    approved_candidates = quality_gate.loc[
        quality_gate["status"].eq(APPROVED_FOR_SCORING)
    ].copy()
    if approved_candidates.empty:
        raise ValueError("No APPROVED_FOR_SCORING rows found in candidate_signal_quality_gate_current.")
    return approved_candidates


def validate_signal_panels(signal_panels: dict[str, pd.DataFrame], expected_signal_names: list[str]) -> None:
    if len(signal_panels) != len(expected_signal_names):
        raise ValueError(
            f"Expected {len(expected_signal_names)} signal panels, got {len(signal_panels)}."
        )

    panel_validation_failures = []
    for signal_name, panel in signal_panels.items():
        if panel.empty:
            panel_validation_failures.append(f"{signal_name}: empty panel")
        if not panel.index.is_unique:
            panel_validation_failures.append(f"{signal_name}: non-unique Date index")
        if panel.shape[1] == 0:
            panel_validation_failures.append(f"{signal_name}: no ticker columns")

    if panel_validation_failures:
        raise ValueError(
            "Signal panel validation failed: " + "; ".join(panel_validation_failures[:10])
        )


def build_signal_scoring_pipeline_summary(
    run_id: str,
    run_timestamp_utc: str,
    scoring_version: str,
    approved_signal_names: list[str],
    horizons: list[int] | tuple[int, ...],
    scores: pd.DataFrame,
    score_summary: pd.DataFrame,
    scoring_gate: pd.DataFrame,
    best_horizon_summary: pd.DataFrame,
    family_summary: pd.DataFrame,
) -> pd.DataFrame:
    status_counts = (
        scoring_gate["status"].value_counts(dropna=False).sort_index().astype(int).to_dict()
        if not scoring_gate.empty and "status" in scoring_gate.columns
        else {}
    )
    best_horizon_counts = (
        best_horizon_summary["best_horizon"].value_counts(dropna=False).sort_index().astype(int).to_dict()
        if not best_horizon_summary.empty and "best_horizon" in best_horizon_summary.columns
        else {}
    )
    return pd.DataFrame(
        [
            {"metric": "scoring_run_id", "value": run_id},
            {"metric": "run_timestamp_utc", "value": run_timestamp_utc},
            {"metric": "scoring_version", "value": scoring_version},
            {"metric": "approved_signal_count", "value": len(approved_signal_names)},
            {"metric": "signals_scored", "value": scores["signal_name"].nunique() if "signal_name" in scores.columns else 0},
            {"metric": "horizons_scored", "value": len(horizons)},
            {"metric": "score_rows", "value": len(scores)},
            {"metric": "score_summary_rows", "value": len(score_summary)},
            {"metric": "scoring_gate_rows", "value": len(scoring_gate)},
            {"metric": "best_horizon_rows", "value": len(best_horizon_summary)},
            {"metric": "family_summary_rows", "value": len(family_summary)},
            {"metric": "status_counts", "value": status_counts},
            {"metric": "best_horizon_counts", "value": best_horizon_counts},
        ]
    )


def run_03_signal_scoring(
    db_path: str | Path | None = None,
    scoring_version: str = SCORING_VERSION,
    run_id: str | None = None,
    horizons: list[int] | tuple[int, ...] = tuple(HORIZONS),
    method: str = IC_METHOD,
    min_score_obs: int = MIN_SCORE_OBS,
    min_gate_obs: int = MIN_GATE_OBS,
    write: bool = True,
    verbose: bool = True,
) -> dict[str, object]:
    """Run the 03 multi-horizon signal scoring workflow with notebook-equivalent logic."""
    resolved_run_id, run_timestamp_utc = _make_scoring_run_context(run_id=run_id)

    if verbose:
        print("03 signal scoring: loading candidate quality gate")
    quality_gate = load_candidate_signal_quality_gate(current=True, db_path=db_path)
    approved_candidates = select_approved_scoring_candidates(quality_gate)
    approved_signal_names = (
        approved_candidates["signal_name"].dropna().sort_values().astype(str).tolist()
    )

    if verbose:
        print(f"03 signal scoring: loading and pivoting {len(approved_signal_names):,} approved signals")
    load_context = nullcontext() if verbose else redirect_stdout(StringIO())
    with load_context:
        signal_panels = load_and_pivot_signal_panels_by_names(
            approved_signal_names,
            current=True,
            db_path=db_path,
            duplicate_policy="raise",
            chunksize=500_000,
        )
    validate_signal_panels(signal_panels, approved_signal_names)

    if verbose:
        print("03 signal scoring: loading clean close prices and building forward returns")
    close_prices = load_price_table("clean_close_prices_current", db_path=db_path)
    forward_returns = make_forward_returns(close_prices, list(horizons))
    validate_forward_return_context = nullcontext() if verbose else redirect_stdout(StringIO())
    with validate_forward_return_context:
        validate_forward_return_panels(forward_returns, close_prices)

    if verbose:
        print("03 signal scoring: scoring signal library across horizons")
    scores = score_signal_library_multi_horizon(
        signals=signal_panels,
        forward_returns=forward_returns,
        metadata=approved_candidates[["signal_name", "signal_family", "signal_version"]],
        horizons=list(horizons),
        method=method,
        min_obs=min_score_obs,
    )
    scores = scores.sort_values(["signal_name", "horizon"]).reset_index(drop=True)

    scoring_gate = apply_preliminary_scoring_gate(
        scores,
        min_abs_mean_ic=GATE_MIN_ABS_MEAN_IC,
        min_abs_ic_ir=GATE_MIN_ABS_IC_IR,
        positive_ic_rate_upper=GATE_POSITIVE_IC_RATE_UPPER,
        positive_ic_rate_lower=GATE_POSITIVE_IC_RATE_LOWER,
        watchlist_abs_mean_ic=GATE_WATCHLIST_ABS_MEAN_IC,
        min_n_obs=min_gate_obs,
    )
    score_summary = build_signal_score_summary(scores)
    best_horizon_summary = build_best_horizon_summary(scores)
    family_summary = build_scoring_family_summary(scores)
    pipeline_summary = build_signal_scoring_pipeline_summary(
        run_id=resolved_run_id,
        run_timestamp_utc=run_timestamp_utc,
        scoring_version=scoring_version,
        approved_signal_names=approved_signal_names,
        horizons=list(horizons),
        scores=scores,
        score_summary=score_summary,
        scoring_gate=scoring_gate,
        best_horizon_summary=best_horizon_summary,
        family_summary=family_summary,
    )

    saved_paths: dict[str, Path] = {}
    if write:
        from src.scoring.signal_scoring_storage import save_scoring_outputs

        if verbose:
            print("03 signal scoring: writing SQLite outputs")
        saved_paths = save_scoring_outputs(
            scores=scores,
            summary=score_summary,
            gate=scoring_gate,
            best_horizon=best_horizon_summary,
            family_summary=family_summary,
            db_path=db_path,
            run_id=resolved_run_id,
            scoring_version=scoring_version,
        )

    return {
        "run_id": resolved_run_id,
        "run_timestamp_utc": run_timestamp_utc,
        "scoring_version": scoring_version,
        "quality_gate": quality_gate,
        "approved_candidates": approved_candidates,
        "approved_signal_names": approved_signal_names,
        "signal_panels": signal_panels,
        "close_prices": close_prices,
        "forward_returns": forward_returns,
        "scores": scores,
        "score_summary": score_summary,
        "scoring_gate": scoring_gate,
        "best_horizon_summary": best_horizon_summary,
        "family_summary": family_summary,
        "summary": pipeline_summary,
        "saved_paths": saved_paths,
    }


__all__ = [
    "APPROVED_FOR_WFV",
    "APPROVED_FOR_SCORING",
    "GATE_MIN_ABS_IC_IR",
    "GATE_MIN_ABS_MEAN_IC",
    "GATE_POSITIVE_IC_RATE_LOWER",
    "GATE_POSITIVE_IC_RATE_UPPER",
    "GATE_WATCHLIST_ABS_MEAN_IC",
    "HORIZONS",
    "IC_METHOD",
    "MIN_GATE_OBS",
    "MIN_SCORE_OBS",
    "MODERATE",
    "NEGATIVE_EDGE_REVERSE_SIGNAL",
    "NO_CLEAR_DIRECTION",
    "NO_SIGNAL",
    "POSITIVE_EDGE",
    "REJECTED_LOW_SIGNAL",
    "REQUIRED_INPUT_TABLES",
    "SCORING_STATUS_LABELS",
    "SCORING_VERSION",
    "STRONG",
    "WATCHLIST",
    "WEAK",
    "apply_preliminary_scoring_gate",
    "build_signal_scoring_pipeline_summary",
    "bucket_signal_strength",
    "build_best_horizon_summary",
    "build_scoring_family_summary",
    "build_signal_score_summary",
    "interpret_signal_direction",
    "run_03_signal_scoring",
    "score_signal_against_forward_returns",
    "score_signal_library_multi_horizon",
    "select_approved_scoring_candidates",
    "validate_signal_panels",
]
