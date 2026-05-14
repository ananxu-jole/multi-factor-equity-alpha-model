from __future__ import annotations

import time
from contextlib import contextmanager, nullcontext, redirect_stdout
from io import StringIO
from pathlib import Path

import numpy as np
import pandas as pd

from src.db import load_price_table, load_table
from src.forward_returns import make_forward_returns
from src.run_config import make_run_id, make_run_timestamp
from src.scoring.daily_ic_cache import (
    DEFAULT_SOURCE_TABLE as DAILY_IC_SOURCE_TABLE,
    daily_ic_config_hash,
    daily_ic_frame_from_series,
    daily_ic_series_from_frame,
    forward_return_config_hash,
    load_daily_ic_cache,
    panel_checksum,
    write_daily_ic_cache,
)
from src.scoring.panel_cache import (
    build_signal_panel_cache,
    load_signal_panels_from_cache,
    validate_signal_panel_cache,
)
from src.scoring.regime_ic_storage import save_regime_ic_outputs
from src.signal_storage import (
    load_candidate_signals_by_names,
    pivot_signal_long_to_panel,
    validate_signal_date_quality,
    validate_signal_long_uniqueness,
)


LOW_VOL = "LOW_VOL"
MID_VOL = "MID_VOL"
HIGH_VOL = "HIGH_VOL"
UPTREND = "UPTREND"
DOWNTREND = "DOWNTREND"
SIDEWAYS = "SIDEWAYS"
LOW_DRAWDOWN = "LOW_DRAWDOWN"
HIGH_DRAWDOWN = "HIGH_DRAWDOWN"
LOW_CORR = "LOW_CORR"
MID_CORR = "MID_CORR"
HIGH_CORR = "HIGH_CORR"

HIGH_REGIME_FRAGILITY = "HIGH_REGIME_FRAGILITY"
MODERATE_REGIME_FRAGILITY = "MODERATE_REGIME_FRAGILITY"
LOW_REGIME_FRAGILITY = "LOW_REGIME_FRAGILITY"

GLOBAL = "GLOBAL"
CONDITIONAL = "CONDITIONAL"
AVOID = "AVOID"
WATCHLIST = "WATCHLIST"
REGIME_IC_VERSION = "phase2_regime_ic_v1"
REGIME_COLUMNS = [
    "benchmark_vol_regime",
    "benchmark_trend_regime",
    "drawdown_regime",
    "correlation_regime",
]
HORIZONS = [1, 5, 10, 20]
IC_METHOD = "spearman"
REQUIRED_INPUT_TABLES = (
    "candidate_signals_current",
    "signal_scores_current",
    "signal_best_horizon_current",
    "clean_close_prices_current",
)


def _memory_usage_mb() -> float | None:
    try:
        import psutil  # type: ignore[import-not-found]
    except ImportError:
        return None
    try:
        return psutil.Process().memory_info().rss / (1024 * 1024)
    except Exception:
        return None


@contextmanager
def _profile_block(profile_records: list[dict[str, object]] | None, block_name: str):
    memory_before = _memory_usage_mb()
    start = time.perf_counter()
    yield
    elapsed = time.perf_counter() - start
    memory_after = _memory_usage_mb()
    if profile_records is not None:
        profile_records.append(
            {
                "block": block_name,
                "elapsed_seconds": elapsed,
                "memory_before_mb": memory_before,
                "memory_after_mb": memory_after,
                "memory_delta_mb": (
                    memory_after - memory_before
                    if memory_before is not None and memory_after is not None
                    else None
                ),
            }
        )


def _tercile_regime(
    values: pd.Series,
    low_label: str,
    mid_label: str,
    high_label: str,
) -> pd.Series:
    valid = values.dropna()
    regime = pd.Series(np.nan, index=values.index, dtype="object")
    if valid.empty:
        return regime
    low_threshold = valid.quantile(1 / 3)
    high_threshold = valid.quantile(2 / 3)
    regime.loc[values <= low_threshold] = low_label
    regime.loc[(values > low_threshold) & (values < high_threshold)] = mid_label
    regime.loc[values >= high_threshold] = high_label
    return regime


def build_regime_features_for_ic(
    close_prices: pd.DataFrame,
    benchmark_ticker: str = "SPY",
) -> pd.DataFrame:
    """Build trailing market regime features for regime-conditioned IC diagnostics."""
    if benchmark_ticker not in close_prices.columns:
        raise ValueError(f"benchmark_ticker '{benchmark_ticker}' not found in close_prices.")

    close = close_prices.copy()
    close.index = pd.to_datetime(close.index, errors="coerce")
    close = close.sort_index().apply(pd.to_numeric, errors="coerce")

    benchmark_prices = close[benchmark_ticker]
    benchmark_return_1d = benchmark_prices.pct_change(fill_method=None)
    benchmark_vol_20d = benchmark_return_1d.rolling(20).std()
    benchmark_vol_regime = _tercile_regime(
        benchmark_vol_20d,
        low_label=LOW_VOL,
        mid_label=MID_VOL,
        high_label=HIGH_VOL,
    )

    ma_50 = benchmark_prices.rolling(50).mean()
    ma_200 = benchmark_prices.rolling(200).mean()
    benchmark_trend_regime = pd.Series(SIDEWAYS, index=close.index, dtype="object")
    benchmark_trend_regime.loc[(ma_50 > ma_200) & (benchmark_prices > ma_200)] = UPTREND
    benchmark_trend_regime.loc[(ma_50 < ma_200) & (benchmark_prices < ma_200)] = DOWNTREND
    benchmark_trend_regime.loc[ma_50.isna() | ma_200.isna() | benchmark_prices.isna()] = np.nan

    market_drawdown = benchmark_prices.div(benchmark_prices.cummax()).sub(1.0)
    drawdown_regime = pd.Series(LOW_DRAWDOWN, index=close.index, dtype="object")
    drawdown_regime.loc[market_drawdown <= -0.10] = HIGH_DRAWDOWN
    drawdown_regime.loc[market_drawdown.isna()] = np.nan

    returns = close.pct_change(fill_method=None)
    asset_returns = returns.drop(columns=[benchmark_ticker], errors="ignore")
    rolling_corr = asset_returns.rolling(20).corr(benchmark_return_1d)
    correlation_20d = rolling_corr.mean(axis=1, skipna=True)
    correlation_regime = _tercile_regime(
        correlation_20d,
        low_label=LOW_CORR,
        mid_label=MID_CORR,
        high_label=HIGH_CORR,
    )

    regime_features = pd.DataFrame(
        {
            "Date": close.index,
            "benchmark_return_1d": benchmark_return_1d.to_numpy(),
            "benchmark_vol_20d": benchmark_vol_20d.to_numpy(),
            "benchmark_vol_regime": benchmark_vol_regime.to_numpy(),
            "benchmark_trend_regime": benchmark_trend_regime.to_numpy(),
            "market_drawdown": market_drawdown.to_numpy(),
            "drawdown_regime": drawdown_regime.to_numpy(),
            "correlation_20d": correlation_20d.to_numpy(),
            "correlation_regime": correlation_regime.to_numpy(),
        }
    )
    return regime_features


def _align_signal_forward(
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


def compute_daily_signal_ic_by_regime(
    signal_panel: pd.DataFrame,
    forward_returns_panel: pd.DataFrame,
    regime_features: pd.DataFrame,
    regime_column: str,
    method: str = "spearman",
) -> pd.DataFrame:
    """Compute daily cross-sectional IC and attach one regime label per date."""
    if method not in {"spearman", "pearson"}:
        raise ValueError("method must be 'spearman' or 'pearson'.")
    if regime_column not in regime_features.columns:
        raise ValueError(f"regime_features is missing regime_column '{regime_column}'.")

    signal, forward = _align_signal_forward(signal_panel, forward_returns_panel)
    regimes = regime_features[["Date", regime_column]].copy()
    regimes["Date"] = pd.to_datetime(regimes["Date"], errors="coerce")
    regime_by_date = regimes.drop_duplicates("Date").set_index("Date")[regime_column]

    rows: list[dict[str, object]] = []
    for date in signal.index:
        signal_row = signal.loc[date]
        forward_row = forward.loc[date]
        valid_mask = signal_row.notna() & forward_row.notna()
        daily_ic = (
            signal_row[valid_mask].corr(forward_row[valid_mask], method=method)
            if valid_mask.sum() >= 3
            else np.nan
        )
        rows.append(
            {
                "Date": date,
                "regime_column": regime_column,
                "regime_value": regime_by_date.get(date, np.nan),
                "daily_ic": daily_ic,
            }
        )
    return pd.DataFrame(rows)


def compute_daily_signal_ic_for_regime_columns(
    signal_panel: pd.DataFrame,
    forward_returns_panel: pd.DataFrame,
    regime_features: pd.DataFrame,
    regime_columns: list[str] | tuple[str, ...],
    method: str = "spearman",
    daily_ic_series: pd.Series | None = None,
) -> pd.DataFrame:
    """Compute daily IC once and attach each requested regime label column."""
    if method not in {"spearman", "pearson"}:
        raise ValueError("method must be 'spearman' or 'pearson'.")
    missing_regime_columns = [column for column in regime_columns if column not in regime_features.columns]
    if missing_regime_columns:
        raise ValueError(f"regime_features is missing regime columns: {missing_regime_columns}")

    signal, forward = _align_signal_forward(signal_panel, forward_returns_panel)
    regimes = regime_features[["Date", *regime_columns]].copy()
    regimes["Date"] = pd.to_datetime(regimes["Date"], errors="coerce")
    regime_by_date = regimes.drop_duplicates("Date").set_index("Date")
    regime_by_date = regime_by_date.reindex(signal.index)

    if daily_ic_series is None:
        daily_ic_series = _daily_signal_ic_series(signal, forward, method=method)
    else:
        daily_ic_series = daily_ic_series.reindex(signal.index)

    base = pd.DataFrame({"Date": signal.index, "daily_ic": daily_ic_series.to_numpy()})
    frames: list[pd.DataFrame] = []
    for regime_column in regime_columns:
        frame = base.copy()
        frame.insert(1, "regime_column", regime_column)
        frame.insert(2, "regime_value", regime_by_date[regime_column].to_numpy())
        frames.append(frame)
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()


def _daily_signal_ic_series(
    signal_panel: pd.DataFrame,
    forward_returns_panel: pd.DataFrame,
    method: str = "spearman",
) -> pd.Series:
    if method not in {"spearman", "pearson"}:
        raise ValueError("method must be 'spearman' or 'pearson'.")
    signal, forward = _align_signal_forward(signal_panel, forward_returns_panel)
    daily_values: list[float] = []
    for date in signal.index:
        signal_row = signal.loc[date]
        forward_row = forward.loc[date]
        valid_mask = signal_row.notna() & forward_row.notna()
        daily_ic = (
            signal_row[valid_mask].corr(forward_row[valid_mask], method=method)
            if valid_mask.sum() >= 3
            else np.nan
        )
        daily_values.append(daily_ic)
    return pd.Series(daily_values, index=signal.index, name="ic")


def _n_pairs_by_date(
    signal_panel: pd.DataFrame,
    forward_returns_panel: pd.DataFrame,
) -> pd.Series:
    signal, forward = _align_signal_forward(signal_panel, forward_returns_panel)
    values = [
        int((signal.loc[date].notna() & forward.loc[date].notna()).sum())
        for date in signal.index
    ]
    return pd.Series(values, index=signal.index, name="n_pairs")


def _daily_ic_with_read_through_cache(
    signal_panel: pd.DataFrame,
    forward_returns_panel: pd.DataFrame,
    signal_name: str,
    horizon: int,
    method: str,
    use_daily_ic_cache: bool,
    daily_ic_cache_dir: str | Path | None,
    rebuild_daily_ic_cache: bool,
    cache_records: list[dict[str, object]] | None,
) -> pd.Series:
    if not use_daily_ic_cache:
        return _daily_signal_ic_series(signal_panel, forward_returns_panel, method=method)

    panel_hash = panel_checksum(signal_panel)
    forward_hash = forward_return_config_hash(forward_returns_panel, horizon)
    config_hash = daily_ic_config_hash(
        signal_name=signal_name,
        horizon=horizon,
        ic_method=method,
        panel_checksum_sha256=panel_hash,
        forward_config_hash=forward_hash,
        source_table=DAILY_IC_SOURCE_TABLE,
    )
    cache_status = "miss"
    if not rebuild_daily_ic_cache:
        cached = load_daily_ic_cache(
            signal_name=signal_name,
            horizon=horizon,
            ic_method=method,
            config_hash=config_hash,
            panel_checksum_sha256=panel_hash,
            forward_config_hash=forward_hash,
            source_table=DAILY_IC_SOURCE_TABLE,
            cache_dir=daily_ic_cache_dir,
        )
        if cached is not None:
            cache_status = "hit"
            if cache_records is not None:
                cache_records.append(
                    {
                        "signal_name": signal_name,
                        "horizon": int(horizon),
                        "config_hash": config_hash,
                        "cache_status": cache_status,
                        "rows": len(cached),
                    }
                )
            return daily_ic_series_from_frame(cached)

    daily_ic = _daily_signal_ic_series(signal_panel, forward_returns_panel, method=method)
    n_pairs = _n_pairs_by_date(signal_panel, forward_returns_panel)
    frame = daily_ic_frame_from_series(
        daily_ic=daily_ic,
        signal_name=signal_name,
        horizon=horizon,
        ic_method=method,
        n_pairs=n_pairs,
        source_table=DAILY_IC_SOURCE_TABLE,
        panel_checksum_sha256=panel_hash,
        forward_config_hash=forward_hash,
        config_hash=config_hash,
    )
    paths = write_daily_ic_cache(
        daily_ic=frame,
        signal_name=signal_name,
        horizon=horizon,
        ic_method=method,
        config_hash=config_hash,
        panel_checksum_sha256=panel_hash,
        forward_config_hash=forward_hash,
        source_table=DAILY_IC_SOURCE_TABLE,
        cache_dir=daily_ic_cache_dir,
    )
    if cache_records is not None:
        cache_records.append(
            {
                "signal_name": signal_name,
                "horizon": int(horizon),
                "config_hash": config_hash,
                "cache_status": "rebuilt" if rebuild_daily_ic_cache else cache_status,
                "rows": len(frame),
                "path": str(paths["daily_ic"]),
            }
        )
    return daily_ic


def summarize_regime_ic(daily_regime_ic: pd.DataFrame) -> pd.DataFrame:
    """Summarize daily regime-conditioned IC by signal, horizon, and regime."""
    if daily_regime_ic.empty:
        return pd.DataFrame(
            columns=[
                "signal_name",
                "horizon",
                "regime_column",
                "regime_value",
                "n_obs",
                "mean_ic",
                "median_ic",
                "ic_std",
                "ic_ir",
                "positive_ic_rate",
                "abs_mean_ic",
            ]
        )

    rows: list[dict[str, object]] = []
    group_columns = ["signal_name", "horizon", "regime_column", "regime_value"]
    for keys, group in daily_regime_ic.dropna(subset=["regime_value"]).groupby(group_columns, dropna=False):
        daily_ic = pd.Series(group["daily_ic"], dtype=float).dropna()
        mean_ic = float(daily_ic.mean()) if not daily_ic.empty else np.nan
        ic_std = float(daily_ic.std()) if len(daily_ic) > 1 else np.nan
        rows.append(
            {
                "signal_name": keys[0],
                "horizon": int(keys[1]),
                "regime_column": keys[2],
                "regime_value": keys[3],
                "n_obs": int(len(daily_ic)),
                "mean_ic": mean_ic,
                "median_ic": float(daily_ic.median()) if not daily_ic.empty else np.nan,
                "ic_std": ic_std,
                "ic_ir": mean_ic / ic_std if ic_std and not pd.isna(ic_std) else np.nan,
                "positive_ic_rate": float(daily_ic.gt(0).mean()) if not daily_ic.empty else np.nan,
                "abs_mean_ic": abs(mean_ic) if not pd.isna(mean_ic) else np.nan,
            }
        )

    return pd.DataFrame(rows)


def _fragility_flag(sign_flip: bool, dependency_ratio: float) -> str:
    if sign_flip or dependency_ratio > 5:
        return HIGH_REGIME_FRAGILITY
    if dependency_ratio > 2:
        return MODERATE_REGIME_FRAGILITY
    return LOW_REGIME_FRAGILITY


def compute_regime_fragility(regime_summary: pd.DataFrame) -> pd.DataFrame:
    """Compute regime dependency and fragility diagnostics by signal/horizon/regime type."""
    if regime_summary.empty:
        return pd.DataFrame(
            columns=[
                "signal_name",
                "horizon",
                "regime_column",
                "best_regime",
                "worst_regime",
                "best_abs_mean_ic",
                "worst_abs_mean_ic",
                "regime_ic_spread",
                "regime_dependency_ratio",
                "sign_flip_across_regimes",
                "regime_fragility_flag",
            ]
        )

    rows: list[dict[str, object]] = []
    for keys, group in regime_summary.groupby(["signal_name", "horizon", "regime_column"], dropna=False):
        valid = group.dropna(subset=["abs_mean_ic"]).copy()
        if valid.empty:
            continue
        best = valid.loc[valid["abs_mean_ic"].idxmax()]
        worst = valid.loc[valid["abs_mean_ic"].idxmin()]
        mean_ics = valid["mean_ic"].dropna()
        sign_flip = bool(mean_ics.gt(0).any() and mean_ics.lt(0).any())
        ratio = float(best["abs_mean_ic"] / max(float(worst["abs_mean_ic"]), 1e-6))
        spread = float(best["abs_mean_ic"] - worst["abs_mean_ic"])
        rows.append(
            {
                "signal_name": keys[0],
                "horizon": int(keys[1]),
                "regime_column": keys[2],
                "best_regime": best["regime_value"],
                "worst_regime": worst["regime_value"],
                "best_abs_mean_ic": float(best["abs_mean_ic"]),
                "worst_abs_mean_ic": float(worst["abs_mean_ic"]),
                "regime_ic_spread": spread,
                "regime_dependency_ratio": ratio,
                "sign_flip_across_regimes": sign_flip,
                "regime_fragility_flag": _fragility_flag(sign_flip, ratio),
            }
        )
    return pd.DataFrame(rows)


def _recommended_use(regime_fragility_flag: str, best_abs_mean_ic: float) -> str:
    if pd.isna(best_abs_mean_ic) or best_abs_mean_ic < 0.012:
        return AVOID
    if regime_fragility_flag == LOW_REGIME_FRAGILITY and best_abs_mean_ic >= 0.012:
        return GLOBAL
    if regime_fragility_flag in {MODERATE_REGIME_FRAGILITY, HIGH_REGIME_FRAGILITY} and best_abs_mean_ic >= 0.020:
        return CONDITIONAL
    return WATCHLIST


def _opportunity_notes(
    recommended_use: str,
    regime_dependency_ratio: float,
    worst_abs_mean_ic: float,
    regime_sample_weight: float = np.nan,
    regime_consistency_score: float = np.nan,
) -> str:
    notes: list[str] = []
    if recommended_use == CONDITIONAL:
        notes.append("Strong conditional regime edge")
    elif recommended_use == GLOBAL:
        notes.append("Low fragility broad signal")
    elif recommended_use == AVOID:
        notes.append("Weak across regimes")
    else:
        notes.append("Monitor before using")

    if (
        not pd.isna(regime_dependency_ratio)
        and not pd.isna(worst_abs_mean_ic)
        and regime_dependency_ratio > 5
        and worst_abs_mean_ic < 0.001
    ):
        notes.append("High dependency ratio due to near-zero worst regime")
    if not pd.isna(regime_sample_weight) and regime_sample_weight < 1:
        notes.append("sample-size adjusted")
    if not pd.isna(regime_consistency_score):
        if regime_consistency_score < 0.50:
            notes.append("low regime sign consistency")
        elif regime_consistency_score >= 0.75:
            notes.append("high regime sign consistency")
    return "; ".join(notes)


def _regime_sample_weight(n_obs: float) -> float:
    if pd.isna(n_obs):
        return np.nan
    return float(min(1.0, max(float(n_obs), 0.0) / 300.0))


def _regime_consistency_score(
    summary: pd.DataFrame,
    signal_name: str,
    horizon: int,
    regime_column: str,
    best_regime_value: object,
) -> float:
    group = summary.loc[
        summary["signal_name"].eq(signal_name)
        & summary["horizon"].eq(horizon)
        & summary["regime_column"].eq(regime_column)
    ].dropna(subset=["mean_ic"])
    if group.empty:
        return np.nan

    best_rows = group.loc[group["regime_value"].eq(best_regime_value)]
    if best_rows.empty:
        return np.nan

    best_mean_ic = best_rows["mean_ic"].iloc[0]
    if pd.isna(best_mean_ic) or best_mean_ic == 0:
        return np.nan

    best_sign = np.sign(float(best_mean_ic))
    valid_signs = np.sign(group["mean_ic"].astype(float))
    valid_signs = valid_signs.loc[valid_signs.ne(0)]
    if valid_signs.empty:
        return np.nan
    return float(valid_signs.eq(best_sign).mean())


def build_regime_opportunity_summary(
    regime_summary: pd.DataFrame,
    fragility: pd.DataFrame,
) -> pd.DataFrame:
    """Build one row per signal/horizon with best conditional regime opportunity."""
    if regime_summary.empty or fragility.empty:
        return pd.DataFrame(
            columns=[
                "signal_name",
                "horizon",
                "signal_family",
                "signal_direction",
                "signal_strength",
                "best_regime_column",
                "best_regime_value",
                "best_abs_mean_ic",
                "regime_sample_weight",
                "adjusted_best_abs_ic",
                "mean_ic_in_best_regime",
                "ic_ir_in_best_regime",
                "positive_ic_rate_in_best_regime",
                "regime_consistency_score",
                "worst_regime_column",
                "worst_regime_value",
                "worst_abs_mean_ic",
                "regime_ic_spread",
                "regime_dependency_ratio",
                "sign_flip_across_regimes",
                "regime_fragility_flag",
                "recommended_use",
                "opportunity_notes",
            ]
        )

    summary = regime_summary.copy()
    frag = fragility.copy()
    rows: list[dict[str, object]] = []
    metadata_columns = ["signal_family", "signal_direction", "signal_strength"]

    for keys, group in frag.groupby(["signal_name", "horizon"], dropna=False):
        valid_frag = group.dropna(subset=["best_abs_mean_ic"]).copy()
        if valid_frag.empty:
            continue
        best_fragility_row = valid_frag.loc[valid_frag["best_abs_mean_ic"].idxmax()]

        signal_name = keys[0]
        horizon = int(keys[1])
        best_regime_column = best_fragility_row["regime_column"]
        best_regime_value = best_fragility_row["best_regime"]

        best_summary = summary.loc[
            summary["signal_name"].eq(signal_name)
            & summary["horizon"].eq(horizon)
            & summary["regime_column"].eq(best_regime_column)
            & summary["regime_value"].eq(best_regime_value)
        ]
        best_summary_row = best_summary.iloc[0] if not best_summary.empty else pd.Series(dtype=object)
        sample_weight = _regime_sample_weight(best_summary_row.get("n_obs", np.nan))
        adjusted_best_abs_ic = float(best_fragility_row["best_abs_mean_ic"]) * sample_weight
        consistency_score = _regime_consistency_score(
            summary,
            signal_name,
            horizon,
            best_regime_column,
            best_regime_value,
        )

        recommended = _recommended_use(
            str(best_fragility_row["regime_fragility_flag"]),
            float(best_fragility_row["best_abs_mean_ic"]),
        )
        row = {
            "signal_name": signal_name,
            "horizon": horizon,
            "best_regime_column": best_regime_column,
            "best_regime_value": best_regime_value,
            "best_abs_mean_ic": float(best_fragility_row["best_abs_mean_ic"]),
            "regime_sample_weight": sample_weight,
            "adjusted_best_abs_ic": adjusted_best_abs_ic,
            "mean_ic_in_best_regime": best_summary_row.get("mean_ic", np.nan),
            "ic_ir_in_best_regime": best_summary_row.get("ic_ir", np.nan),
            "positive_ic_rate_in_best_regime": best_summary_row.get("positive_ic_rate", np.nan),
            "regime_consistency_score": consistency_score,
            "worst_regime_column": best_regime_column,
            "worst_regime_value": best_fragility_row["worst_regime"],
            "worst_abs_mean_ic": float(best_fragility_row["worst_abs_mean_ic"]),
            "regime_ic_spread": float(best_fragility_row["regime_ic_spread"]),
            "regime_dependency_ratio": float(best_fragility_row["regime_dependency_ratio"]),
            "sign_flip_across_regimes": bool(best_fragility_row["sign_flip_across_regimes"]),
            "regime_fragility_flag": best_fragility_row["regime_fragility_flag"],
            "recommended_use": recommended,
            "opportunity_notes": _opportunity_notes(
                recommended,
                float(best_fragility_row["regime_dependency_ratio"]),
                float(best_fragility_row["worst_abs_mean_ic"]),
                sample_weight,
                consistency_score,
            ),
        }
        for column in metadata_columns:
            if column in valid_frag.columns:
                row[column] = valid_frag[column].dropna().iloc[0] if valid_frag[column].notna().any() else np.nan
            elif column in summary.columns:
                values = summary.loc[
                    summary["signal_name"].eq(signal_name) & summary["horizon"].eq(horizon),
                    column,
                ].dropna()
                row[column] = values.iloc[0] if not values.empty else np.nan

        rows.append(row)

    output = pd.DataFrame(rows)
    ordered = [
        "signal_name",
        "horizon",
        "signal_family",
        "signal_direction",
        "signal_strength",
        "best_regime_column",
        "best_regime_value",
        "best_abs_mean_ic",
        "regime_sample_weight",
        "adjusted_best_abs_ic",
        "mean_ic_in_best_regime",
        "ic_ir_in_best_regime",
        "positive_ic_rate_in_best_regime",
        "regime_consistency_score",
        "worst_regime_column",
        "worst_regime_value",
        "worst_abs_mean_ic",
        "regime_ic_spread",
        "regime_dependency_ratio",
        "sign_flip_across_regimes",
        "regime_fragility_flag",
        "recommended_use",
        "opportunity_notes",
    ]
    return output[[column for column in ordered if column in output.columns]].sort_values(
        ["signal_name", "horizon"]
    ).reset_index(drop=True)


def run_regime_ic_analysis(
    candidate_signals_long: pd.DataFrame,
    close_prices: pd.DataFrame,
    horizons: list[int] | tuple[int, ...] = (1, 5, 10, 20),
    regime_columns: list[str] | tuple[str, ...] | None = None,
    signal_scores: pd.DataFrame | None = None,
    method: str = "spearman",
    profile_records: list[dict[str, object]] | None = None,
    signal_panels: dict[str, pd.DataFrame] | None = None,
    use_daily_ic_cache: bool = False,
    daily_ic_cache_dir: str | Path | None = None,
    rebuild_daily_ic_cache: bool = False,
    daily_ic_cache_records: list[dict[str, object]] | None = None,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Run regime-conditioned IC diagnostics for scored signal/horizon pairs."""
    regime_columns = list(
        regime_columns
        if regime_columns is not None
        else [
            "benchmark_vol_regime",
            "benchmark_trend_regime",
            "drawdown_regime",
            "correlation_regime",
        ]
    )
    if signal_scores is None:
        signal_scores = load_table("signal_scores_current")

    with _profile_block(profile_records, "eligible candidate pair filtering"):
        candidate_pairs = (
            signal_scores.loc[signal_scores["horizon"].isin(horizons), ["signal_name", "horizon"]]
            .dropna()
            .drop_duplicates()
            .sort_values(["signal_name", "horizon"])
        )
    if candidate_pairs.empty:
        with _profile_block(profile_records, "regime feature construction"):
            regime_features = build_regime_features_for_ic(close_prices)
        empty_daily = pd.DataFrame(
            columns=["Date", "regime_column", "regime_value", "daily_ic", "signal_name", "horizon", "method"]
        )
        with _profile_block(profile_records, "regime grouping/summary"):
            empty_summary = summarize_regime_ic(empty_daily)
        with _profile_block(profile_records, "fragility scoring"):
            empty_fragility = compute_regime_fragility(empty_summary)
        return regime_features, empty_daily, empty_summary, empty_fragility

    with _profile_block(profile_records, "regime feature construction"):
        regime_features = build_regime_features_for_ic(close_prices)
    with _profile_block(profile_records, "forward return construction"):
        forward_returns = make_forward_returns(close_prices, tuple(sorted(set(int(h) for h in horizons))))

    with _profile_block(profile_records, "pivot/panel construction"):
        needed_signal_names = candidate_pairs["signal_name"].astype(str).drop_duplicates().tolist()
        if signal_panels is not None:
            missing_panels = [signal_name for signal_name in needed_signal_names if signal_name not in signal_panels]
            if missing_panels:
                raise ValueError(f"signal panel cache is missing signal_names: {missing_panels}")
            panel_cache = {signal_name: signal_panels[signal_name] for signal_name in needed_signal_names}
        else:
            selected_signal_long = candidate_signals_long.loc[
                candidate_signals_long["signal_name"].isin(needed_signal_names)
            ]
            panel_cache = {
                signal_name: pivot_signal_long_to_panel(group, signal_name)
                for signal_name, group in selected_signal_long.groupby("signal_name", sort=False)
            }

    daily_frames: list[pd.DataFrame] = []
    with _profile_block(profile_records, "daily IC calculation"):
        for row in candidate_pairs.itertuples(index=False):
            signal_name = str(row.signal_name)
            horizon = int(row.horizon)
            if signal_name not in panel_cache:
                raise ValueError(f"signal_name '{signal_name}' not found in candidate_signals_long.")
            daily_ic_series = _daily_ic_with_read_through_cache(
                signal_panel=panel_cache[signal_name],
                forward_returns_panel=forward_returns[horizon],
                signal_name=signal_name,
                horizon=horizon,
                method=method,
                use_daily_ic_cache=use_daily_ic_cache,
                daily_ic_cache_dir=daily_ic_cache_dir,
                rebuild_daily_ic_cache=rebuild_daily_ic_cache,
                cache_records=daily_ic_cache_records,
            )
            daily_ic = compute_daily_signal_ic_for_regime_columns(
                signal_panel=panel_cache[signal_name],
                forward_returns_panel=forward_returns[horizon],
                regime_features=regime_features,
                regime_columns=regime_columns,
                method=method,
                daily_ic_series=daily_ic_series,
            )
            daily_ic["signal_name"] = signal_name
            daily_ic["horizon"] = horizon
            daily_ic["method"] = method
            daily_frames.append(daily_ic)

    daily_regime_ic = pd.concat(daily_frames, ignore_index=True) if daily_frames else pd.DataFrame()
    with _profile_block(profile_records, "regime grouping/summary"):
        regime_summary = summarize_regime_ic(daily_regime_ic)
    with _profile_block(profile_records, "fragility scoring"):
        regime_fragility = compute_regime_fragility(regime_summary)
    return regime_features, daily_regime_ic, regime_summary, regime_fragility


def _needed_signal_names(signal_scores: pd.DataFrame, horizons: list[int] | tuple[int, ...]) -> list[str]:
    return (
        signal_scores.loc[signal_scores["horizon"].isin(horizons), "signal_name"]
        .dropna()
        .astype(str)
        .drop_duplicates()
        .sort_values()
        .tolist()
    )


def _load_candidate_signals_for_regime_ic(
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
            context="03D candidate_signals_long",
            max_null_rate=0.0,
        )
        validate_signal_long_uniqueness(
            candidate_signals,
            key_cols=["signal_name", "Date", "ticker"],
            strict=True,
            context="03D candidate_signals_long",
        )
    return candidate_signals


def build_regime_ic_pipeline_summary(
    run_id: str,
    run_timestamp: str,
    regime_ic_version: str,
    signal_names: list[str],
    candidate_signals_long: pd.DataFrame,
    regime_features: pd.DataFrame,
    daily_regime_ic: pd.DataFrame,
    regime_summary: pd.DataFrame,
    regime_fragility: pd.DataFrame,
    regime_opportunity_summary: pd.DataFrame,
    candidate_signal_rows_loaded: int | None = None,
) -> pd.DataFrame:
    fragility_counts = (
        regime_fragility["regime_fragility_flag"].value_counts(dropna=False).sort_index().astype(int).to_dict()
        if not regime_fragility.empty and "regime_fragility_flag" in regime_fragility.columns
        else {}
    )
    recommended_use_counts = (
        regime_opportunity_summary["recommended_use"].value_counts(dropna=False).sort_index().astype(int).to_dict()
        if not regime_opportunity_summary.empty and "recommended_use" in regime_opportunity_summary.columns
        else {}
    )
    return pd.DataFrame(
        [
            {"metric": "run_id", "value": run_id},
            {"metric": "run_timestamp", "value": run_timestamp},
            {"metric": "regime_ic_version", "value": regime_ic_version},
            {"metric": "requested_signal_count", "value": len(signal_names)},
            {
                "metric": "candidate_signal_rows_loaded",
                "value": len(candidate_signals_long) if candidate_signal_rows_loaded is None else candidate_signal_rows_loaded,
            },
            {"metric": "regime_feature_rows", "value": len(regime_features)},
            {"metric": "daily_regime_ic_rows", "value": len(daily_regime_ic)},
            {"metric": "regime_summary_rows", "value": len(regime_summary)},
            {"metric": "regime_fragility_rows", "value": len(regime_fragility)},
            {"metric": "regime_opportunity_rows", "value": len(regime_opportunity_summary)},
            {"metric": "fragility_counts", "value": fragility_counts},
            {"metric": "recommended_use_counts", "value": recommended_use_counts},
        ]
    )


def run_03d_regime_ic(
    db_path: str | Path | None = None,
    regime_ic_version: str = REGIME_IC_VERSION,
    run_id: str | None = None,
    horizons: list[int] | tuple[int, ...] = tuple(HORIZONS),
    regime_columns: list[str] | tuple[str, ...] = tuple(REGIME_COLUMNS),
    method: str = IC_METHOD,
    use_panel_cache: bool = False,
    panel_cache_dir: str | Path | None = None,
    rebuild_panel_cache: bool = False,
    use_daily_ic_cache: bool = False,
    daily_ic_cache_dir: str | Path | None = None,
    rebuild_daily_ic_cache: bool = False,
    write: bool = False,
    verbose: bool = True,
) -> dict[str, object]:
    """Run the 03D regime-conditioned IC workflow with notebook-equivalent logic."""
    resolved_run_id = run_id or make_run_id(prefix="phase2_nb03d_regime_ic")
    run_timestamp = make_run_timestamp()
    profile_records: list[dict[str, object]] = []

    with _profile_block(profile_records, "input table loading"):
        if verbose:
            print("03D regime IC: loading score metadata")
        signal_scores = load_table("signal_scores_current", db_path=db_path)
        signal_best_horizon = load_table("signal_best_horizon_current", db_path=db_path)
        needed_signal_names = _needed_signal_names(signal_scores, list(horizons))

    panel_cache_validation = pd.DataFrame()
    panel_cache_metadata = pd.DataFrame()
    signal_panels: dict[str, pd.DataFrame] | None = None
    candidate_signal_rows_loaded = 0
    if use_panel_cache:
        cache_context = nullcontext() if verbose else redirect_stdout(StringIO())
        with _profile_block(profile_records, "panel cache validation/build"):
            with cache_context:
                panel_cache_metadata = build_signal_panel_cache(
                    needed_signal_names,
                    db_path=db_path,
                    cache_dir=panel_cache_dir,
                    force=rebuild_panel_cache,
                    verbose=verbose,
                )
                panel_cache_validation = validate_signal_panel_cache(
                    needed_signal_names,
                    db_path=db_path,
                    cache_dir=panel_cache_dir,
                    validate_checksum=False,
                )
            if not panel_cache_validation["fresh"].all():
                stale = panel_cache_validation.loc[~panel_cache_validation["fresh"]]
                raise ValueError(
                    "Panel cache validation failed for 03D: "
                    f"{stale[['signal_name', 'exists', 'fresh', 'error']].to_dict('records')}"
                )
            if "source_row_count" in panel_cache_metadata.columns:
                candidate_signal_rows_loaded = int(panel_cache_metadata["source_row_count"].fillna(0).astype(int).sum())
        with _profile_block(profile_records, "panel cache loading"):
            signal_panels = load_signal_panels_from_cache(
                needed_signal_names,
                cache_dir=panel_cache_dir,
                validate_checksum=False,
            )
        candidate_signals_long = pd.DataFrame()
    else:
        with _profile_block(profile_records, "selective signal loading"):
            if verbose:
                print(f"03D regime IC: loading {len(needed_signal_names):,} candidate signals by name")
            candidate_signals_long = _load_candidate_signals_for_regime_ic(
                needed_signal_names,
                db_path=db_path,
                verbose=verbose,
            )
        candidate_signal_rows_loaded = len(candidate_signals_long)
    with _profile_block(profile_records, "forward return input loading"):
        close_prices = load_price_table("clean_close_prices_current", db_path=db_path)

    if verbose:
        print("03D regime IC: running regime-conditioned IC analysis")
    compute_context = nullcontext() if verbose else redirect_stdout(StringIO())
    daily_ic_cache_records: list[dict[str, object]] = []
    with compute_context:
        regime_features, daily_regime_ic, regime_summary, regime_fragility = run_regime_ic_analysis(
            candidate_signals_long=candidate_signals_long,
            close_prices=close_prices,
            horizons=list(horizons),
            regime_columns=list(regime_columns),
            signal_scores=signal_scores,
            method=method,
            profile_records=profile_records,
            signal_panels=signal_panels,
            use_daily_ic_cache=use_daily_ic_cache,
            daily_ic_cache_dir=daily_ic_cache_dir,
            rebuild_daily_ic_cache=rebuild_daily_ic_cache,
            daily_ic_cache_records=daily_ic_cache_records,
        )
    with _profile_block(profile_records, "fragility/opportunity scoring"):
        metadata_columns = [
            "signal_name",
            "signal_family",
            "best_horizon",
            "signal_direction",
            "signal_strength",
        ]
        metadata = signal_best_horizon[[column for column in metadata_columns if column in signal_best_horizon.columns]]
        regime_summary_enriched = regime_summary.merge(metadata, on="signal_name", how="left")
        regime_fragility_enriched = regime_fragility.merge(metadata, on="signal_name", how="left")
        regime_opportunity_summary = build_regime_opportunity_summary(
            regime_summary=regime_summary_enriched,
            fragility=regime_fragility_enriched,
        )
    pipeline_summary = build_regime_ic_pipeline_summary(
        run_id=resolved_run_id,
        run_timestamp=run_timestamp,
        regime_ic_version=regime_ic_version,
        signal_names=needed_signal_names,
        candidate_signals_long=candidate_signals_long,
        regime_features=regime_features,
        daily_regime_ic=daily_regime_ic,
        regime_summary=regime_summary_enriched,
        regime_fragility=regime_fragility_enriched,
        regime_opportunity_summary=regime_opportunity_summary,
        candidate_signal_rows_loaded=candidate_signal_rows_loaded,
    )

    saved_paths: dict[str, Path] = {}
    if write:
        with _profile_block(profile_records, "SQLite writes"):
            if verbose:
                print("03D regime IC: writing SQLite outputs")
            saved_paths = save_regime_ic_outputs(
                regime_features=regime_features,
                daily_regime_ic=daily_regime_ic,
                regime_summary=regime_summary_enriched,
                regime_fragility=regime_fragility_enriched,
                regime_opportunity_summary=regime_opportunity_summary,
                db_path=db_path,
                run_id=resolved_run_id,
                regime_ic_version=regime_ic_version,
            )
    profile = pd.DataFrame(profile_records)
    daily_ic_cache_metadata = pd.DataFrame(daily_ic_cache_records)

    return {
        "run_id": resolved_run_id,
        "run_timestamp": run_timestamp,
        "regime_ic_version": regime_ic_version,
        "signal_scores": signal_scores,
        "signal_best_horizon": signal_best_horizon,
        "needed_signal_names": needed_signal_names,
        "candidate_signals_long": candidate_signals_long,
        "use_panel_cache": use_panel_cache,
        "panel_cache_metadata": panel_cache_metadata,
        "panel_cache_validation": panel_cache_validation,
        "signal_panels": signal_panels,
        "use_daily_ic_cache": use_daily_ic_cache,
        "daily_ic_cache_metadata": daily_ic_cache_metadata,
        "close_prices": close_prices,
        "regime_features": regime_features,
        "daily_regime_ic": daily_regime_ic,
        "regime_summary": regime_summary_enriched,
        "regime_fragility": regime_fragility_enriched,
        "regime_opportunity_summary": regime_opportunity_summary,
        "summary": pipeline_summary,
        "profile": profile,
        "saved_paths": saved_paths,
    }


__all__ = [
    "HIGH_REGIME_FRAGILITY",
    "LOW_REGIME_FRAGILITY",
    "MODERATE_REGIME_FRAGILITY",
    "build_regime_opportunity_summary",
    "build_regime_ic_pipeline_summary",
    "build_regime_features_for_ic",
    "compute_daily_signal_ic_by_regime",
    "compute_daily_signal_ic_for_regime_columns",
    "compute_regime_fragility",
    "HORIZONS",
    "IC_METHOD",
    "REGIME_COLUMNS",
    "REGIME_IC_VERSION",
    "REQUIRED_INPUT_TABLES",
    "build_signal_panel_cache",
    "load_signal_panels_from_cache",
    "run_03d_regime_ic",
    "run_regime_ic_analysis",
    "summarize_regime_ic",
    "validate_signal_panel_cache",
]
