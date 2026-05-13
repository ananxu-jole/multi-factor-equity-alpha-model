from __future__ import annotations

from contextlib import nullcontext, redirect_stdout
from io import StringIO
from pathlib import Path

import numpy as np
import pandas as pd

from src.db import load_price_table, load_table
from src.forward_returns import make_forward_returns
from src.run_config import make_run_id, make_run_timestamp
from src.scoring.decay_storage import save_signal_decay_outputs
from src.signal_storage import (
    load_candidate_signals_by_names,
    pivot_signal_long_to_panel,
    validate_signal_date_quality,
    validate_signal_long_uniqueness,
)


STABLE = "STABLE"
DECAYING = "DECAYING"
UNSTABLE = "UNSTABLE"
INSUFFICIENT_DATA = "INSUFFICIENT_DATA"
HIGH_DECAY_RISK = "HIGH_DECAY_RISK"
MODERATE_DECAY_RISK = "MODERATE_DECAY_RISK"
LOW_DECAY_RISK = "LOW_DECAY_RISK"
DECAY_VERSION = "phase2_signal_decay_v1"
ROLLING_IC_WINDOW = 63
MIN_ROLLING_OBS = 8
HORIZONS = [1, 5, 10, 20]
IC_METHOD = "spearman"
REQUIRED_INPUT_TABLES = (
    "candidate_signals_current",
    "signal_scores_current",
    "signal_best_horizon_current",
    "clean_close_prices_current",
)


def _align_panels(
    signal_panel: pd.DataFrame,
    forward_returns_panel: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    signal = signal_panel.copy()
    forward = forward_returns_panel.copy()
    signal.index = pd.to_datetime(signal.index, errors="coerce")
    forward.index = pd.to_datetime(forward.index, errors="coerce")
    signal = signal.sort_index().apply(pd.to_numeric, errors="coerce")
    forward = forward.sort_index().apply(pd.to_numeric, errors="coerce")
    common_index = signal.index.intersection(forward.index)
    common_columns = signal.columns.intersection(forward.columns)
    return (
        signal.reindex(index=common_index, columns=common_columns),
        forward.reindex(index=common_index, columns=common_columns),
    )


def _cross_sectional_ic_by_date(
    signal_panel: pd.DataFrame,
    forward_returns_panel: pd.DataFrame,
    method: str = "spearman",
) -> pd.Series:
    if method not in {"spearman", "pearson"}:
        raise ValueError("method must be 'spearman' or 'pearson'.")

    signal, forward = _align_panels(signal_panel, forward_returns_panel)
    ic_values: list[float] = []

    for date in signal.index:
        signal_row = signal.loc[date]
        forward_row = forward.loc[date]
        valid_mask = signal_row.notna() & forward_row.notna()
        if valid_mask.sum() < 3:
            ic_values.append(np.nan)
            continue
        ic_values.append(signal_row[valid_mask].corr(forward_row[valid_mask], method=method))

    return pd.Series(ic_values, index=signal.index, name="ic")


def compute_rolling_ic_series(
    signal_panel: pd.DataFrame,
    forward_returns_panel: pd.DataFrame,
    window: int = 63,
    method: str = "spearman",
) -> pd.DataFrame:
    """Compute rolling mean cross-sectional IC over time."""
    if window < 1:
        raise ValueError("window must be at least 1.")

    daily_ic = _cross_sectional_ic_by_date(signal_panel, forward_returns_panel, method=method)
    rolling_ic = daily_ic.rolling(window=window, min_periods=window).mean()
    return pd.DataFrame({"Date": rolling_ic.index, "rolling_ic": rolling_ic.to_numpy()})


def _decay_slope(values: pd.Series) -> float:
    clean = values.dropna()
    if len(clean) < 2:
        return np.nan
    x = np.arange(len(clean), dtype=float)
    return float(np.polyfit(x, clean.to_numpy(dtype=float), 1)[0])


def _sign_stability(values: pd.Series) -> float:
    clean = values.dropna()
    if clean.empty:
        return np.nan
    mean_ic = clean.mean()
    if mean_ic >= 0:
        return float(clean.ge(0).mean())
    return float(clean.le(0).mean())


def _rolling_ic_autocorr(values: pd.Series) -> float:
    clean = values.dropna()
    if len(clean) < 3:
        return np.nan
    return float(clean.autocorr(lag=1))


def _cumulative_ic_drawdown(values: pd.Series) -> float:
    clean = values.dropna()
    if clean.empty:
        return np.nan
    cumulative_ic = clean.cumsum()
    drawdown = cumulative_ic.sub(cumulative_ic.cummax())
    return float(drawdown.min())


def _rolling_ic_drawdown(values: pd.Series) -> float:
    clean = values.dropna()
    if clean.empty:
        return np.nan
    drawdown = clean.sub(clean.cummax())
    return float(drawdown.min())


def _half_life_proxy(mean_rolling_ic: float, decay_slope: float) -> float:
    if pd.isna(mean_rolling_ic) or pd.isna(decay_slope) or decay_slope >= 0:
        return np.nan
    return float(abs(mean_rolling_ic / decay_slope)) if decay_slope != 0 else np.nan


def _assign_decay_status(
    n_observations: int,
    decay_slope: float,
    sign_stability: float,
    min_rolling_obs: int,
) -> str:
    if n_observations < min_rolling_obs or pd.isna(decay_slope) or pd.isna(sign_stability):
        return INSUFFICIENT_DATA
    if sign_stability < 0.50:
        return UNSTABLE
    if decay_slope < -0.00005:
        return DECAYING
    if decay_slope >= -0.00005 and sign_stability >= 0.60:
        return STABLE
    return UNSTABLE


def _assign_decay_risk_flag(
    decay_status: str,
    sign_stability: float,
    ic_change: float,
) -> str:
    if decay_status == DECAYING or (not pd.isna(sign_stability) and sign_stability < 0.50):
        return HIGH_DECAY_RISK
    if (
        (not pd.isna(sign_stability) and sign_stability < 0.60)
        or (not pd.isna(ic_change) and ic_change < -0.02)
    ):
        return MODERATE_DECAY_RISK
    return LOW_DECAY_RISK


def compute_signal_decay_metrics(
    rolling_ic_df: pd.DataFrame,
    min_rolling_obs: int = 8,
) -> pd.DataFrame:
    """Summarize rolling IC decay diagnostics for each signal/horizon pair."""
    if rolling_ic_df.empty:
        return pd.DataFrame(
            columns=[
                "signal_name",
                "horizon",
                "n_rolling_obs",
                "mean_rolling_ic",
                "ic_volatility",
                "rolling_ic_min",
                "rolling_ic_max",
                "rolling_ic_recent_252d_mean",
                "decay_slope",
                "abs_decay_slope",
                "recent_ic",
                "early_ic",
                "ic_change",
                "sign_stability",
                "rolling_ic_autocorr",
                "cumulative_ic_drawdown",
                "min_rolling_ic_drawdown",
                "half_life_proxy",
                "decay_status",
                "decay_risk_flag",
            ]
        )

    group_columns = [column for column in ["signal_name", "horizon"] if column in rolling_ic_df.columns]
    if not group_columns:
        groups = [((), rolling_ic_df)]
    else:
        groups = rolling_ic_df.groupby(group_columns, dropna=False)

    rows: list[dict[str, object]] = []
    for group_key, group in groups:
        rolling_ic = pd.Series(group["rolling_ic"], dtype=float).dropna()
        n_obs = len(rolling_ic)
        split_size = max(1, int(np.ceil(n_obs * 0.25))) if n_obs else 0
        early_ic = float(rolling_ic.head(split_size).mean()) if n_obs else np.nan
        recent_ic = float(rolling_ic.tail(split_size).mean()) if n_obs else np.nan
        slope = _decay_slope(rolling_ic)
        stability = _sign_stability(rolling_ic)
        mean_ic = float(rolling_ic.mean()) if n_obs else np.nan
        ic_change = recent_ic - early_ic if not pd.isna(recent_ic) and not pd.isna(early_ic) else np.nan
        decay_status = _assign_decay_status(n_obs, slope, stability, min_rolling_obs)

        row = {
            "n_rolling_obs": int(n_obs),
            "mean_rolling_ic": mean_ic,
            "ic_volatility": float(rolling_ic.std()) if n_obs > 1 else np.nan,
            "rolling_ic_min": float(rolling_ic.min()) if n_obs else np.nan,
            "rolling_ic_max": float(rolling_ic.max()) if n_obs else np.nan,
            "rolling_ic_recent_252d_mean": (
                float(rolling_ic.tail(252).mean()) if n_obs >= 252 else np.nan
            ),
            "decay_slope": slope,
            "abs_decay_slope": abs(slope) if not pd.isna(slope) else np.nan,
            "recent_ic": recent_ic,
            "early_ic": early_ic,
            "ic_change": ic_change,
            "sign_stability": stability,
            "rolling_ic_autocorr": _rolling_ic_autocorr(rolling_ic),
            "cumulative_ic_drawdown": _cumulative_ic_drawdown(rolling_ic),
            "min_rolling_ic_drawdown": _rolling_ic_drawdown(rolling_ic),
            "half_life_proxy": _half_life_proxy(mean_ic, slope),
            "decay_status": decay_status,
            "decay_risk_flag": _assign_decay_risk_flag(decay_status, stability, ic_change),
        }

        if group_columns:
            if not isinstance(group_key, tuple):
                group_key = (group_key,)
            row.update(dict(zip(group_columns, group_key, strict=False)))

        rows.append(row)

    output = pd.DataFrame(rows)
    ordered = [
        "signal_name",
        "horizon",
        "n_rolling_obs",
        "mean_rolling_ic",
        "ic_volatility",
        "rolling_ic_min",
        "rolling_ic_max",
        "rolling_ic_recent_252d_mean",
        "decay_slope",
        "abs_decay_slope",
        "recent_ic",
        "early_ic",
        "ic_change",
        "sign_stability",
        "rolling_ic_autocorr",
        "cumulative_ic_drawdown",
        "min_rolling_ic_drawdown",
        "half_life_proxy",
        "decay_status",
        "decay_risk_flag",
    ]
    return output[[column for column in ordered if column in output.columns]]


def run_signal_decay_analysis(
    signal_scores: pd.DataFrame,
    candidate_signals_long: pd.DataFrame,
    close_prices: pd.DataFrame,
    horizons: list[int] | tuple[int, ...] = (1, 5, 10, 20),
    window: int = 63,
    method: str = "spearman",
    min_rolling_obs: int = 8,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Run rolling IC and decay diagnostics for scored candidate signal/horizon pairs."""
    required_score_columns = {"signal_name", "horizon"}
    missing_score_columns = required_score_columns.difference(signal_scores.columns)
    if missing_score_columns:
        raise ValueError(f"signal_scores is missing columns: {sorted(missing_score_columns)}")

    candidate_pairs = (
        signal_scores.loc[signal_scores["horizon"].isin(horizons), ["signal_name", "horizon"]]
        .dropna()
        .drop_duplicates()
        .sort_values(["signal_name", "horizon"])
    )
    if candidate_pairs.empty:
        empty_curve = pd.DataFrame(columns=["Date", "rolling_ic", "signal_name", "horizon", "method", "window"])
        return empty_curve, compute_signal_decay_metrics(empty_curve, min_rolling_obs=min_rolling_obs)

    forward_returns = make_forward_returns(close_prices, tuple(sorted(set(int(h) for h in horizons))))
    needed_signal_names = candidate_pairs["signal_name"].astype(str).drop_duplicates().tolist()
    selected_signal_long = candidate_signals_long.loc[
        candidate_signals_long["signal_name"].isin(needed_signal_names)
    ].copy()
    panel_cache: dict[str, pd.DataFrame] = {
        signal_name: pivot_signal_long_to_panel(group, signal_name)
        for signal_name, group in selected_signal_long.groupby("signal_name", sort=False)
    }
    curve_frames: list[pd.DataFrame] = []

    for row in candidate_pairs.itertuples(index=False):
        signal_name = str(row.signal_name)
        horizon = int(row.horizon)
        if signal_name not in panel_cache:
            raise ValueError(f"signal_name '{signal_name}' not found in candidate_signals_long.")

        rolling_ic = compute_rolling_ic_series(
            signal_panel=panel_cache[signal_name],
            forward_returns_panel=forward_returns[horizon],
            window=window,
            method=method,
        )
        rolling_ic["signal_name"] = signal_name
        rolling_ic["horizon"] = horizon
        rolling_ic["method"] = method
        rolling_ic["window"] = window
        curve_frames.append(rolling_ic)

    decay_curve = pd.concat(curve_frames, ignore_index=True) if curve_frames else pd.DataFrame()
    decay_summary = compute_signal_decay_metrics(decay_curve, min_rolling_obs=min_rolling_obs)
    return decay_curve, decay_summary


def _needed_signal_names(signal_scores: pd.DataFrame, horizons: list[int] | tuple[int, ...]) -> list[str]:
    return (
        signal_scores.loc[signal_scores["horizon"].isin(horizons), "signal_name"]
        .dropna()
        .astype(str)
        .drop_duplicates()
        .sort_values()
        .tolist()
    )


def _load_candidate_signals_for_decay(
    signal_names: list[str],
    db_path: str | Path | None,
    verbose: bool,
) -> pd.DataFrame:
    load_context = nullcontext() if verbose else redirect_stdout(StringIO())
    with load_context:
        candidate_signals = load_candidate_signals_by_names(
            signal_names,
            current=True,
            db_path=db_path,
            chunksize=500_000,
        )
    validation_context = nullcontext() if verbose else redirect_stdout(StringIO())
    with validation_context:
        validate_signal_date_quality(
            candidate_signals,
            context="03C candidate_signals",
            max_null_rate=0.0,
        )
        validate_signal_long_uniqueness(
            candidate_signals,
            key_cols=["signal_name", "Date", "ticker"],
            strict=True,
            context="03C candidate_signals",
        )
    return candidate_signals


def build_signal_decay_pipeline_summary(
    run_id: str,
    run_timestamp: str,
    decay_version: str,
    signal_names: list[str],
    candidate_signals: pd.DataFrame,
    decay_curve: pd.DataFrame,
    decay_summary: pd.DataFrame,
) -> pd.DataFrame:
    status_counts = (
        decay_summary["decay_status"].value_counts(dropna=False).sort_index().astype(int).to_dict()
        if not decay_summary.empty and "decay_status" in decay_summary.columns
        else {}
    )
    risk_counts = (
        decay_summary["decay_risk_flag"].value_counts(dropna=False).sort_index().astype(int).to_dict()
        if not decay_summary.empty and "decay_risk_flag" in decay_summary.columns
        else {}
    )
    return pd.DataFrame(
        [
            {"metric": "run_id", "value": run_id},
            {"metric": "run_timestamp", "value": run_timestamp},
            {"metric": "decay_version", "value": decay_version},
            {"metric": "requested_signal_count", "value": len(signal_names)},
            {"metric": "candidate_signal_rows_loaded", "value": len(candidate_signals)},
            {"metric": "decay_curve_rows", "value": len(decay_curve)},
            {"metric": "decay_summary_rows", "value": len(decay_summary)},
            {"metric": "decay_status_counts", "value": status_counts},
            {"metric": "decay_risk_counts", "value": risk_counts},
        ]
    )


def run_03c_signal_decay(
    db_path: str | Path | None = None,
    decay_version: str = DECAY_VERSION,
    run_id: str | None = None,
    horizons: list[int] | tuple[int, ...] = tuple(HORIZONS),
    window: int = ROLLING_IC_WINDOW,
    method: str = IC_METHOD,
    min_rolling_obs: int = MIN_ROLLING_OBS,
    write: bool = False,
    verbose: bool = True,
) -> dict[str, object]:
    """Run the 03C signal decay workflow with notebook-equivalent logic."""
    resolved_run_id = run_id or make_run_id(prefix="phase2_nb03c_signal_decay")
    run_timestamp = make_run_timestamp()

    if verbose:
        print("03C signal decay: loading score metadata")
    signal_scores = load_table("signal_scores_current", db_path=db_path)
    signal_best_horizon = load_table("signal_best_horizon_current", db_path=db_path)
    signal_scoring_gate = load_table("signal_scoring_gate_current", db_path=db_path)
    needed_signal_names = _needed_signal_names(signal_scores, list(horizons))

    if verbose:
        print(f"03C signal decay: loading {len(needed_signal_names):,} candidate signals by name")
    candidate_signals = _load_candidate_signals_for_decay(
        needed_signal_names,
        db_path=db_path,
        verbose=verbose,
    )
    close_prices = load_price_table("clean_close_prices_current", db_path=db_path)

    if verbose:
        print("03C signal decay: running rolling IC decay analysis")
    compute_context = nullcontext() if verbose else redirect_stdout(StringIO())
    with compute_context:
        decay_curve, decay_summary = run_signal_decay_analysis(
            signal_scores=signal_scores,
            candidate_signals_long=candidate_signals,
            close_prices=close_prices,
            horizons=list(horizons),
            window=window,
            method=method,
            min_rolling_obs=min_rolling_obs,
        )
    metadata_columns = [
        "signal_name",
        "signal_family",
        "best_horizon",
        "signal_direction",
        "signal_strength",
    ]
    metadata = signal_best_horizon[[column for column in metadata_columns if column in signal_best_horizon.columns]]
    decay_summary_enriched = decay_summary.merge(metadata, on="signal_name", how="left")
    pipeline_summary = build_signal_decay_pipeline_summary(
        run_id=resolved_run_id,
        run_timestamp=run_timestamp,
        decay_version=decay_version,
        signal_names=needed_signal_names,
        candidate_signals=candidate_signals,
        decay_curve=decay_curve,
        decay_summary=decay_summary_enriched,
    )

    saved_paths: dict[str, Path] = {}
    if write:
        if verbose:
            print("03C signal decay: writing SQLite outputs")
        saved_paths = save_signal_decay_outputs(
            decay_curve=decay_curve,
            decay_summary=decay_summary_enriched,
            db_path=db_path,
            run_id=resolved_run_id,
            decay_version=decay_version,
        )

    return {
        "run_id": resolved_run_id,
        "run_timestamp": run_timestamp,
        "decay_version": decay_version,
        "signal_scores": signal_scores,
        "signal_best_horizon": signal_best_horizon,
        "signal_scoring_gate": signal_scoring_gate,
        "needed_signal_names": needed_signal_names,
        "candidate_signals": candidate_signals,
        "close_prices": close_prices,
        "decay_curve": decay_curve,
        "decay_summary": decay_summary_enriched,
        "summary": pipeline_summary,
        "saved_paths": saved_paths,
    }


__all__ = [
    "DECAYING",
    "DECAY_VERSION",
    "HIGH_DECAY_RISK",
    "HORIZONS",
    "IC_METHOD",
    "INSUFFICIENT_DATA",
    "LOW_DECAY_RISK",
    "MIN_ROLLING_OBS",
    "MODERATE_DECAY_RISK",
    "REQUIRED_INPUT_TABLES",
    "ROLLING_IC_WINDOW",
    "STABLE",
    "UNSTABLE",
    "build_signal_decay_pipeline_summary",
    "compute_rolling_ic_series",
    "compute_signal_decay_metrics",
    "run_03c_signal_decay",
    "run_signal_decay_analysis",
]
