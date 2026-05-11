from __future__ import annotations

import numpy as np
import pandas as pd

from src.db import load_table
from src.forward_returns import make_forward_returns
from src.signal_storage import pivot_signal_long_to_panel


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

    candidate_pairs = (
        signal_scores.loc[signal_scores["horizon"].isin(horizons), ["signal_name", "horizon"]]
        .dropna()
        .drop_duplicates()
        .sort_values(["signal_name", "horizon"])
    )
    if candidate_pairs.empty:
        regime_features = build_regime_features_for_ic(close_prices)
        empty_daily = pd.DataFrame(
            columns=["Date", "regime_column", "regime_value", "daily_ic", "signal_name", "horizon", "method"]
        )
        empty_summary = summarize_regime_ic(empty_daily)
        return regime_features, empty_daily, empty_summary, compute_regime_fragility(empty_summary)

    regime_features = build_regime_features_for_ic(close_prices)
    forward_returns = make_forward_returns(close_prices, tuple(sorted(set(int(h) for h in horizons))))

    needed_signal_names = candidate_pairs["signal_name"].astype(str).drop_duplicates().tolist()
    selected_signal_long = candidate_signals_long.loc[
        candidate_signals_long["signal_name"].isin(needed_signal_names)
    ].copy()
    panel_cache = {
        signal_name: pivot_signal_long_to_panel(group, signal_name)
        for signal_name, group in selected_signal_long.groupby("signal_name", sort=False)
    }

    daily_frames: list[pd.DataFrame] = []
    for row in candidate_pairs.itertuples(index=False):
        signal_name = str(row.signal_name)
        horizon = int(row.horizon)
        if signal_name not in panel_cache:
            raise ValueError(f"signal_name '{signal_name}' not found in candidate_signals_long.")
        for regime_column in regime_columns:
            daily_ic = compute_daily_signal_ic_by_regime(
                signal_panel=panel_cache[signal_name],
                forward_returns_panel=forward_returns[horizon],
                regime_features=regime_features,
                regime_column=regime_column,
                method=method,
            )
            daily_ic["signal_name"] = signal_name
            daily_ic["horizon"] = horizon
            daily_ic["method"] = method
            daily_frames.append(daily_ic)

    daily_regime_ic = pd.concat(daily_frames, ignore_index=True) if daily_frames else pd.DataFrame()
    regime_summary = summarize_regime_ic(daily_regime_ic)
    regime_fragility = compute_regime_fragility(regime_summary)
    return regime_features, daily_regime_ic, regime_summary, regime_fragility


__all__ = [
    "HIGH_REGIME_FRAGILITY",
    "LOW_REGIME_FRAGILITY",
    "MODERATE_REGIME_FRAGILITY",
    "build_regime_opportunity_summary",
    "build_regime_features_for_ic",
    "compute_daily_signal_ic_by_regime",
    "compute_regime_fragility",
    "run_regime_ic_analysis",
    "summarize_regime_ic",
]
