from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd


RUN_ID = "robustness_first_discovery_expansion_v2"
OUT_DIR = Path("artifacts/research") / RUN_ID
NOTE_PATH = Path("docs/research_notes/robustness_first_discovery_expansion_v2.md")
DATA_PATH = Path("data/processed/phase2/nb01_data_foundation/raw_ohlcv.parquet")
BENCHMARK_PATH = Path("data/processed/phase2/nb01_data_foundation/benchmark_close_prices.csv")
VOLUME_BASELINE_PATH = Path(
    "artifacts/research/volume_shock_reversal_production_candidate_v1/"
    "volume_shock_reversal_stable_20_signal_panel.parquet"
)
REFINED_VOL_BASELINE_PATH = Path(
    "artifacts/research/refined_survivor_signal_factory_integration_v1/"
    "volatility_surprise_reversal_20_60_smooth_signal_panel.parquet"
)

HORIZONS = (1, 5, 10, 20)
WFV_WINDOWS = 4


CANDIDATES: list[dict[str, str]] = [
    {
        "signal_name": "dollar_volume_pressure_reversal_20",
        "family": "liquidity_flow",
        "intuition": "Medium-horizon reversal after price moves accompanied by abnormal dollar-volume pressure.",
        "expected_horizon": "h10-h20",
        "expected_failure_mode": "May collapse into plain reversal or volume-shock reversal.",
    },
    {
        "signal_name": "overnight_gap_flow_reversal_10",
        "family": "liquidity_flow",
        "intuition": "Reversal after large overnight gaps with abnormal volume confirmation.",
        "expected_horizon": "h5-h10",
        "expected_failure_mode": "Gap noise and high turnover.",
    },
    {
        "signal_name": "beta_residual_reversal_stability_20",
        "family": "residual_relative_value",
        "intuition": "Reversal of benchmark-beta residual return, smoothed to reduce noisy beta leakage.",
        "expected_horizon": "h10-h20",
        "expected_failure_mode": "Hidden plain reversal or beta estimation noise.",
    },
    {
        "signal_name": "relative_value_mispricing_decay_20_60",
        "family": "residual_relative_value",
        "intuition": "Mean reversion in short-term relative overextension versus longer relative trend.",
        "expected_horizon": "h10-h20",
        "expected_failure_mode": "Generic momentum/reversal duplication.",
    },
    {
        "signal_name": "vol_compression_range_expansion_20_60",
        "family": "volatility_structure",
        "intuition": "Continuation after returns improve from compressed range and volatility structure.",
        "expected_horizon": "h10-h20",
        "expected_failure_mode": "Low signal strength from over-smoothing.",
    },
    {
        "signal_name": "vol_expansion_reversal_quality_10_40",
        "family": "volatility_structure",
        "intuition": "Reversal after short volatility expansion and recent return stress.",
        "expected_horizon": "h10-h20",
        "expected_failure_mode": "Similarity to simple volatility reversal.",
    },
    {
        "signal_name": "dispersion_extreme_reversal_20",
        "family": "dispersion_aware",
        "intuition": "Reversal among names far from the cross-sectional return center during high dispersion.",
        "expected_horizon": "h10-h20",
        "expected_failure_mode": "Becomes plain cross-sectional reversal.",
    },
    {
        "signal_name": "dispersion_stable_leadership_60",
        "family": "dispersion_aware",
        "intuition": "Continuation for stable leaders when cross-sectional dispersion is persistent rather than spiky.",
        "expected_horizon": "h20",
        "expected_failure_mode": "Hidden momentum/trend exposure.",
    },
    {
        "signal_name": "flow_volatility_interaction_reversal_20",
        "family": "interaction",
        "intuition": "Reversal when abnormal flow and volatility surprise jointly indicate overreaction.",
        "expected_horizon": "h10-h20",
        "expected_failure_mode": "Blend camouflage or duplicated reversal exposure.",
    },
    {
        "signal_name": "turnover_adjusted_relative_momentum_60",
        "family": "turnover_aware",
        "intuition": "Relative momentum quality penalized by unstable volume turnover.",
        "expected_horizon": "h20",
        "expected_failure_mode": "Momentum duplication or stale low-turnover bias.",
    },
    {
        "signal_name": "turnover_decay_reversal_quality_20",
        "family": "turnover_aware",
        "intuition": "Reversal where price dislocation persists while turnover pressure decays.",
        "expected_horizon": "h10-h20",
        "expected_failure_mode": "Low coverage or redundant reversal behavior.",
    },
]


def _ensure_dirs() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    NOTE_PATH.parent.mkdir(parents=True, exist_ok=True)


def _clean_panel(df: pd.DataFrame) -> pd.DataFrame:
    return df.replace([np.inf, -np.inf], np.nan).sort_index(axis=0).sort_index(axis=1)


def _rank_cs(df: pd.DataFrame) -> pd.DataFrame:
    ranked = df.rank(axis=1, pct=True)
    return _clean_panel((ranked - 0.5) * 2.0)


def _zscore_ts(df: pd.DataFrame, window: int, min_periods: int | None = None) -> pd.DataFrame:
    min_periods = min_periods or max(5, window // 2)
    mean = df.rolling(window, min_periods=min_periods).mean()
    std = df.rolling(window, min_periods=min_periods).std(ddof=0)
    return _clean_panel((df - mean) / std.replace(0.0, np.nan))


def _winsor(df: pd.DataFrame, lower: float = -5.0, upper: float = 5.0) -> pd.DataFrame:
    return df.clip(lower=lower, upper=upper)


def _align_panels(panels: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
    common_index = None
    common_cols = None
    for panel in panels.values():
        common_index = panel.index if common_index is None else common_index.intersection(panel.index)
        common_cols = panel.columns if common_cols is None else common_cols.intersection(panel.columns)
    return {
        name: _clean_panel(panel.loc[common_index, common_cols])
        for name, panel in panels.items()
    }


def load_inputs() -> tuple[dict[str, pd.DataFrame], pd.Series]:
    raw = pd.read_parquet(DATA_PATH)
    fields = {
        "open": "Open",
        "high": "High",
        "low": "Low",
        "close": "Close",
        "volume": "Volume",
    }
    panels = {name: raw[field].copy() for name, field in fields.items()}
    panels = _align_panels(panels)
    liquid_columns = panels["close"].columns[panels["close"].notna().sum() > 252]
    panels = {name: panel.loc[:, liquid_columns] for name, panel in panels.items()}
    panels = _align_panels(panels)
    benchmark = pd.read_csv(BENCHMARK_PATH)
    benchmark["Date"] = pd.to_datetime(benchmark["Date"])
    benchmark = benchmark.set_index("Date")["SPY"].sort_index()
    benchmark = benchmark.reindex(panels["close"].index).ffill()
    return panels, benchmark


def build_candidate_panels(panels: dict[str, pd.DataFrame], benchmark: pd.Series) -> dict[str, pd.DataFrame]:
    close = panels["close"]
    open_ = panels["open"]
    high = panels["high"]
    low = panels["low"]
    volume = panels["volume"].astype(float).where(panels["volume"].astype(float) > 0)

    ret1 = close.pct_change(1, fill_method=None)
    ret5 = close.pct_change(5, fill_method=None)
    ret10 = close.pct_change(10, fill_method=None)
    ret20 = close.pct_change(20, fill_method=None)
    ret60 = close.pct_change(60, fill_method=None)
    bench_ret20 = benchmark.pct_change(20, fill_method=None)
    daily_bench = benchmark.pct_change(1, fill_method=None)

    dollar_volume = close * volume
    dollar_shock_40 = _winsor(dollar_volume / dollar_volume.rolling(40, min_periods=20).mean(), 0.0, 5.0)
    volume_shock_20 = _winsor(volume / volume.rolling(20, min_periods=10).mean(), 0.0, 5.0)
    volume_z_40 = _winsor(_zscore_ts(volume, 40), -4, 4)
    volatility_10 = ret1.rolling(10, min_periods=8).std()
    volatility_20 = ret1.rolling(20, min_periods=15).std()
    volatility_40 = ret1.rolling(40, min_periods=25).std()
    volatility_60 = ret1.rolling(60, min_periods=40).std()
    vol_surprise_10_40 = _winsor(volatility_10 / volatility_40 - 1.0, -3, 3)
    vol_compression = -_rank_cs(volatility_20 / volatility_60 - 1.0)
    true_range = ((high - low) / close).replace([np.inf, -np.inf], np.nan)
    range_compression = -_rank_cs(true_range.rolling(20, min_periods=15).mean())

    bench_daily = pd.DataFrame(
        np.repeat(daily_bench.values[:, None], close.shape[1], axis=1),
        index=close.index,
        columns=close.columns,
    )
    cov = ret1.rolling(60, min_periods=40).cov(bench_daily)
    var = daily_bench.rolling(60, min_periods=40).var()
    beta = cov.divide(var, axis=0).clip(-3, 3)
    beta_residual_20 = ret20 - beta.multiply(bench_ret20, axis=0)
    relative_20 = ret20.subtract(bench_ret20, axis=0)
    relative_60 = ret60.subtract(benchmark.pct_change(60, fill_method=None), axis=0)

    cs_ret20_mean = ret20.mean(axis=1)
    cs_ret20_std = ret20.std(axis=1).replace(0.0, np.nan)
    cs_extreme_20 = ret20.sub(cs_ret20_mean, axis=0).div(cs_ret20_std, axis=0)
    dispersion_20 = ret20.std(axis=1)
    dispersion_z = ((dispersion_20 - dispersion_20.rolling(60, min_periods=40).mean()) /
                    dispersion_20.rolling(60, min_periods=40).std()).clip(-3, 3)
    dispersion_multiplier = pd.DataFrame(
        np.repeat((1.0 + dispersion_z.clip(lower=0).fillna(0)).values[:, None], close.shape[1], axis=1),
        index=close.index,
        columns=close.columns,
    )
    stable_dispersion = -dispersion_20.rolling(20, min_periods=15).std()
    stable_dispersion_multiplier = pd.DataFrame(
        np.repeat(_rank_series_to_01(stable_dispersion).values[:, None], close.shape[1], axis=1),
        index=close.index,
        columns=close.columns,
    )

    turnover_instability = _winsor(_zscore_ts(volume.pct_change(1, fill_method=None).abs(), 40), -3, 3)
    turnover_decay = -_zscore_ts(volume, 20).diff(5)
    low_turnover_quality = -_rank_cs(turnover_instability)

    candidates = {
        "dollar_volume_pressure_reversal_20": _rank_cs((-ret20 * dollar_shock_40).rolling(5, min_periods=3).mean()),
        "overnight_gap_flow_reversal_10": _rank_cs(
            (-(open_ / close.shift(1) - 1.0) * volume_shock_20).rolling(3, min_periods=2).mean()
        ),
        "beta_residual_reversal_stability_20": _rank_cs((-beta_residual_20).rolling(10, min_periods=6).mean()),
        "relative_value_mispricing_decay_20_60": _rank_cs((-(relative_20 - relative_60 / 3.0)).rolling(5, min_periods=3).mean()),
        "vol_compression_range_expansion_20_60": _rank_cs(
            (ret20.rank(axis=1, pct=True) * (vol_compression + range_compression)).rolling(5, min_periods=3).mean()
        ),
        "vol_expansion_reversal_quality_10_40": _rank_cs((-ret10 * (1.0 + vol_surprise_10_40.clip(lower=0))).rolling(5, min_periods=3).mean()),
        "dispersion_extreme_reversal_20": _rank_cs((-cs_extreme_20 * dispersion_multiplier).rolling(5, min_periods=3).mean()),
        "dispersion_stable_leadership_60": _rank_cs((ret60 * stable_dispersion_multiplier).rolling(10, min_periods=6).mean()),
        "flow_volatility_interaction_reversal_20": _rank_cs(
            (-ret20 * dollar_shock_40 * (1.0 + vol_surprise_10_40.clip(lower=0))).rolling(10, min_periods=6).mean()
        ),
        "turnover_adjusted_relative_momentum_60": _rank_cs((relative_60 * (1.0 + low_turnover_quality)).rolling(10, min_periods=6).mean()),
        "turnover_decay_reversal_quality_20": _rank_cs((-ret20 * _winsor(turnover_decay, -3, 3).clip(lower=0)).rolling(5, min_periods=3).mean()),
    }
    return {name: _clean_panel(panel) for name, panel in candidates.items()}


def _rank_series_to_01(series: pd.Series) -> pd.Series:
    ranked = series.rank(pct=True)
    return ranked.fillna(0.5)


def forward_returns(close: pd.DataFrame, horizon: int) -> pd.DataFrame:
    return close.shift(-horizon) / close - 1.0


def daily_ic(signal: pd.DataFrame, fwd: pd.DataFrame) -> pd.Series:
    values: list[float] = []
    dates: list[pd.Timestamp] = []
    for date in signal.index.intersection(fwd.index):
        s = signal.loc[date]
        r = fwd.loc[date]
        valid = s.notna() & r.notna()
        if int(valid.sum()) < 25:
            values.append(np.nan)
        else:
            values.append(s[valid].rank().corr(r[valid].rank()))
        dates.append(date)
    return pd.Series(values, index=pd.Index(dates, name="Date"), dtype=float)


def structural_summary(signals: dict[str, pd.DataFrame]) -> pd.DataFrame:
    rows = []
    for name, panel in signals.items():
        finite = np.isfinite(panel.to_numpy(dtype=float))
        valid = panel.notna().to_numpy()
        turnover_by_date = panel.diff().abs().mean(axis=1, skipna=True)
        rows.append(
            {
                "signal_name": name,
                "rows": panel.shape[0],
                "columns": panel.shape[1],
                "missing_pct": float(1.0 - valid.mean()),
                "finite_pct": float(finite.mean()),
                "date_coverage": float(panel.notna().any(axis=1).mean()),
                "ticker_coverage_mean": float(panel.notna().mean(axis=1).mean()),
                "inf_count": int(np.isinf(panel.to_numpy(dtype=float)).sum()),
                "turnover_proxy": float(turnover_by_date.mean(skipna=True)),
                "turnover_p95": float(turnover_by_date.quantile(0.95)),
                "turnover_max": float(turnover_by_date.max(skipna=True)),
                "concentration_proxy": float(panel.abs().max(axis=1, skipna=True).mean(skipna=True)),
            }
        )
    return pd.DataFrame(rows)


def score_signals(signals: dict[str, pd.DataFrame], close: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    score_rows = []
    daily_rows = []
    for horizon in HORIZONS:
        fwd = forward_returns(close, horizon)
        for name, panel in signals.items():
            ic = daily_ic(panel, fwd)
            valid_ic = ic.dropna()
            mean_ic = float(valid_ic.mean()) if not valid_ic.empty else np.nan
            std_ic = float(valid_ic.std(ddof=0)) if len(valid_ic) > 1 else np.nan
            score_rows.append(
                {
                    "signal_name": name,
                    "horizon": horizon,
                    "mean_ic": mean_ic,
                    "abs_mean_ic": abs(mean_ic) if pd.notna(mean_ic) else np.nan,
                    "ic_ir": mean_ic / std_ic if std_ic and std_ic > 0 else np.nan,
                    "abs_ic_ir": abs(mean_ic / std_ic) if std_ic and std_ic > 0 else np.nan,
                    "positive_ic_rate": float((valid_ic > 0).mean()) if not valid_ic.empty else np.nan,
                    "n_dates": int(valid_ic.shape[0]),
                }
            )
            daily_rows.extend(
                {
                    "Date": date,
                    "signal_name": name,
                    "horizon": horizon,
                    "ic": value,
                }
                for date, value in valid_ic.items()
            )
    scores = pd.DataFrame(score_rows)
    if not scores.empty:
        best = scores.loc[scores.groupby("signal_name")["abs_mean_ic"].idxmax(), ["signal_name", "horizon"]]
        best = best.rename(columns={"horizon": "best_horizon"})
        scores = scores.merge(best, on="signal_name", how="left")
        scores["is_best_horizon"] = scores["horizon"].eq(scores["best_horizon"])
    return scores, pd.DataFrame(daily_rows)


def build_stress_states(close: pd.DataFrame, benchmark: pd.Series) -> pd.DataFrame:
    bench_ret = benchmark.pct_change(1, fill_method=None)
    bench_20 = benchmark.pct_change(20, fill_method=None)
    bench_ma_60 = benchmark.rolling(60, min_periods=40).mean()
    drawdown = benchmark / benchmark.cummax() - 1.0
    realized_vol = bench_ret.rolling(20, min_periods=15).std()
    dispersion = close.pct_change(20, fill_method=None).std(axis=1)
    breadth = (close.pct_change(20, fill_method=None) > 0).mean(axis=1)
    states = pd.DataFrame(index=close.index)
    states["drawdown_acceleration"] = (drawdown.diff(20) < -0.03).fillna(False)
    states["volatility_spike"] = (realized_vol > realized_vol.rolling(252, min_periods=100).quantile(0.80)).fillna(False)
    states["panic_liquidity_stress"] = (states["drawdown_acceleration"] & states["volatility_spike"]).fillna(False)
    states["trend_transition"] = ((benchmark > bench_ma_60) != (benchmark.shift(20) > bench_ma_60.shift(20))).fillna(False)
    states["recovery_phase"] = ((bench_20 > 0.03) & (drawdown < -0.05)).fillna(False)
    states["high_dispersion_rotation"] = (dispersion > dispersion.rolling(252, min_periods=100).quantile(0.75)).fillna(False)
    states["weak_breadth"] = (breadth < breadth.rolling(252, min_periods=100).quantile(0.25)).fillna(False)
    return states


def stress_attribution(daily_ics: pd.DataFrame, scores: pd.DataFrame, states: pd.DataFrame) -> pd.DataFrame:
    best = scores.loc[scores["is_best_horizon"], ["signal_name", "best_horizon"]].set_index("signal_name")["best_horizon"]
    rows = []
    for signal_name, horizon in best.items():
        ic = daily_ics[(daily_ics["signal_name"].eq(signal_name)) & (daily_ics["horizon"].eq(horizon))]
        series = ic.set_index("Date")["ic"]
        for state in states.columns:
            state_dates = states.index[states[state]]
            sample = series.reindex(state_dates).dropna()
            std = sample.std(ddof=0) if len(sample) > 1 else np.nan
            rows.append(
                {
                    "signal_name": signal_name,
                    "horizon": horizon,
                    "state": state,
                    "n_dates": int(len(sample)),
                    "mean_ic": float(sample.mean()) if len(sample) else np.nan,
                    "ic_ir": float(sample.mean() / std) if pd.notna(std) and std > 0 else np.nan,
                    "positive_ic_rate": float((sample > 0).mean()) if len(sample) else np.nan,
                }
            )
    return pd.DataFrame(rows)


def wfv_diagnostics(daily_ics: pd.DataFrame, scores: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    best = scores.loc[scores["is_best_horizon"], ["signal_name", "best_horizon"]].set_index("signal_name")["best_horizon"]
    window_rows = []
    summary_rows = []
    for signal_name, horizon in best.items():
        ic = daily_ics[(daily_ics["signal_name"].eq(signal_name)) & (daily_ics["horizon"].eq(horizon))]
        series = ic.set_index("Date")["ic"].dropna().sort_index()
        if len(series) < WFV_WINDOWS * 50:
            continue
        splits = np.array_split(series.index, WFV_WINDOWS)
        effective_values = []
        signs = []
        for idx, dates in enumerate(splits, start=1):
            sample = series.loc[dates]
            mean_ic = float(sample.mean())
            std_ic = float(sample.std(ddof=0))
            ir = mean_ic / std_ic if std_ic > 0 else np.nan
            pos_rate = float((sample > 0).mean())
            effective_values.append(mean_ic)
            signs.append(np.sign(mean_ic))
            window_rows.append(
                {
                    "signal_name": signal_name,
                    "horizon": horizon,
                    "window": idx,
                    "start_date": str(sample.index.min().date()),
                    "end_date": str(sample.index.max().date()),
                    "mean_test_ic": mean_ic,
                    "test_ic_ir": ir,
                    "positive_ic_rate": pos_rate,
                    "valid_ic_dates": int(len(sample)),
                }
            )
        arr = np.array(effective_values, dtype=float)
        std = float(np.std(arr)) if len(arr) > 1 else np.nan
        summary_rows.append(
            {
                "signal_name": signal_name,
                "horizon": horizon,
                "n_windows": int(len(arr)),
                "effective_mean_test_ic": float(np.mean(arr)),
                "effective_test_ic_ir": float(np.mean(arr) / std) if pd.notna(std) and std > 0 else np.nan,
                "persistence": float((arr > 0).mean()),
                "sign_consistency": float(max((arr > 0).mean(), (arr < 0).mean())),
                "one_window_dominance": float(np.max(np.abs(arr)) / np.sum(np.abs(arr))) if np.sum(np.abs(arr)) > 0 else np.nan,
            }
        )
    return pd.DataFrame(summary_rows), pd.DataFrame(window_rows)


def load_reference_panels(index: pd.Index, columns: pd.Index) -> dict[str, pd.DataFrame]:
    refs: dict[str, pd.DataFrame] = {}
    if VOLUME_BASELINE_PATH.exists():
        refs["track_a_volume_shock_reversal_stable_20"] = pd.read_parquet(VOLUME_BASELINE_PATH).reindex(index=index, columns=columns)
    if REFINED_VOL_BASELINE_PATH.exists():
        refs["paused_volatility_surprise_reversal_20_60_smooth"] = pd.read_parquet(REFINED_VOL_BASELINE_PATH).reindex(index=index, columns=columns)
    return refs


def baseline_panels(signals: dict[str, pd.DataFrame], panels: dict[str, pd.DataFrame], benchmark: pd.Series) -> dict[str, pd.DataFrame]:
    close = panels["close"]
    volume = panels["volume"].astype(float).where(panels["volume"].astype(float) > 0)
    ret20 = close.pct_change(20, fill_method=None)
    ret60 = close.pct_change(60, fill_method=None)
    ret1 = close.pct_change(1, fill_method=None)
    vol20 = ret1.rolling(20, min_periods=15).std()
    simple_volume = _rank_cs((-ret20 * (volume / volume.rolling(20, min_periods=10).mean()).clip(0, 5)).rolling(5, min_periods=3).mean())
    simple_vol_reversal = _rank_cs((-ret20 * (1 + (vol20 / vol20.rolling(60, min_periods=40).mean() - 1).clip(lower=0))).rolling(5, min_periods=3).mean())
    return {
        "unweighted_reversal_20": _rank_cs(-ret20),
        "plain_smoothed_reversal_20": _rank_cs((-ret20).rolling(5, min_periods=3).mean()),
        "plain_momentum_60": _rank_cs(ret60),
        "simple_volume_spike_reversal": simple_volume,
        "simple_volatility_reversal": simple_vol_reversal,
        **load_reference_panels(close.index, close.columns),
    }


def panel_corr(a: pd.DataFrame, b: pd.DataFrame) -> tuple[float, float]:
    aligned_a, aligned_b = a.align(b, join="inner", axis=0)
    aligned_a, aligned_b = aligned_a.align(aligned_b, join="inner", axis=1)
    av = aligned_a.stack(dropna=True)
    bv = aligned_b.stack(dropna=True)
    common = av.index.intersection(bv.index)
    if len(common) < 100:
        return np.nan, np.nan
    value_corr = float(av.loc[common].corr(bv.loc[common]))
    rank_corrs = []
    for date in aligned_a.index:
        x = aligned_a.loc[date]
        y = aligned_b.loc[date]
        valid = x.notna() & y.notna()
        if int(valid.sum()) >= 25:
            rank_corrs.append(x[valid].rank().corr(y[valid].rank()))
    return value_corr, float(np.nanmean(rank_corrs)) if rank_corrs else np.nan


def orthogonality(signals: dict[str, pd.DataFrame], refs: dict[str, pd.DataFrame]) -> pd.DataFrame:
    rows = []
    for signal_name, panel in signals.items():
        for ref_name, ref_panel in refs.items():
            value_corr, rank_corr = panel_corr(panel, ref_panel)
            rows.append(
                {
                    "signal_name": signal_name,
                    "comparison": ref_name,
                    "value_corr": value_corr,
                    "abs_value_corr": abs(value_corr) if pd.notna(value_corr) else np.nan,
                    "mean_rank_corr_by_date": rank_corr,
                    "abs_mean_rank_corr_by_date": abs(rank_corr) if pd.notna(rank_corr) else np.nan,
                }
            )
    return pd.DataFrame(rows)


def classify_candidates(structural: pd.DataFrame, scores: pd.DataFrame, wfv: pd.DataFrame, orth: pd.DataFrame) -> pd.DataFrame:
    best_scores = scores.loc[scores["is_best_horizon"]].copy()
    max_corr = orth.groupby("signal_name")["abs_value_corr"].max().rename("max_abs_baseline_corr")
    summary = best_scores.merge(structural, on="signal_name", how="left").merge(max_corr, on="signal_name", how="left")
    summary = summary.merge(wfv, on=["signal_name", "horizon"], how="left", suffixes=("", "_wfv"))
    decisions = []
    for _, row in summary.iterrows():
        issues = []
        if row["missing_pct"] > 0.20:
            issues.append("high_missingness")
        if row["turnover_proxy"] > 0.22:
            issues.append("high_turnover")
        if row["abs_mean_ic"] < 0.006:
            issues.append("weak_best_horizon_ic")
        if row["positive_ic_rate"] < 0.51:
            issues.append("weak_positive_ic_rate")
        if pd.notna(row.get("persistence")) and row["persistence"] < 0.75:
            issues.append("weak_wfv_persistence")
        if pd.notna(row.get("sign_consistency")) and row["sign_consistency"] < 0.75:
            issues.append("weak_wfv_sign_consistency")
        if row.get("max_abs_baseline_corr", 0) > 0.75:
            issues.append("high_baseline_similarity")
        if not issues:
            status = "CANDIDATE_FOR_FURTHER_VALIDATION"
        elif len(issues) <= 2 and row["abs_mean_ic"] >= 0.006 and row["max_abs_baseline_corr"] <= 0.80:
            status = "WATCHLIST_RESEARCH"
        else:
            status = "REJECT_RESEARCH"
        decisions.append(
            {
                "signal_name": row["signal_name"],
                "family": _family_for(row["signal_name"]),
                "best_horizon": int(row["horizon"]),
                "mean_ic": row["mean_ic"],
                "abs_mean_ic": row["abs_mean_ic"],
                "ic_ir": row["ic_ir"],
                "positive_ic_rate": row["positive_ic_rate"],
                "turnover_proxy": row["turnover_proxy"],
                "missing_pct": row["missing_pct"],
                "max_abs_baseline_corr": row.get("max_abs_baseline_corr"),
                "wfv_persistence": row.get("persistence"),
                "wfv_sign_consistency": row.get("sign_consistency"),
                "status": status,
                "review_issues": "; ".join(issues) if issues else "none",
            }
        )
    return pd.DataFrame(decisions).sort_values(["status", "abs_mean_ic"], ascending=[True, False])


def _family_for(signal_name: str) -> str:
    for spec in CANDIDATES:
        if spec["signal_name"] == signal_name:
            return spec["family"]
    return "unknown"


def write_note(
    registry: pd.DataFrame,
    structural: pd.DataFrame,
    scores: pd.DataFrame,
    wfv: pd.DataFrame,
    stress: pd.DataFrame,
    orth: pd.DataFrame,
    decisions: pd.DataFrame,
) -> None:
    best = scores.loc[scores["is_best_horizon"]].sort_values("abs_mean_ic", ascending=False)
    top_orth = orth.groupby("signal_name")["abs_value_corr"].max().reset_index().rename(columns={"abs_value_corr": "max_abs_corr"})
    status_counts = decisions["status"].value_counts().to_dict()
    watch = decisions[decisions["status"].isin(["CANDIDATE_FOR_FURTHER_VALIDATION", "WATCHLIST_RESEARCH"])]
    rejected = decisions[decisions["status"].eq("REJECT_RESEARCH")]
    lines = [
        "# Robustness-First Discovery Expansion v2",
        "",
        "## Executive Takeaway",
        "",
        f"Track B ran an isolated robustness-first standalone discovery batch under `{RUN_ID}`.",
        "",
        "This was a research-only sidecar batch. It did not register any signals, mutate survivor/watchlist lists, alter gates, change schemas, run portfolio construction, use ML, or touch Conditional-Alpha paths.",
        "",
        f"Candidates tested: {len(registry)}",
        f"Status counts: `{json.dumps(status_counts, sort_keys=True)}`",
        "",
        "Final recommendation: carry forward only the research watchlist/further-validation candidates for deeper diagnostics; reject the rest as useful negative evidence.",
        "",
        "## Scope And Isolation",
        "",
        f"- Run ID: `{RUN_ID}`",
        f"- Artifact directory: `{OUT_DIR}`",
        "- Track A volume governance remained separate.",
        "- `volume_shock_reversal_stable_20` was used only as an orthogonality baseline, not promoted or modified.",
        "",
        "## Candidate Set",
        "",
        registry.to_markdown(index=False),
        "",
        "## Structural Quality Summary",
        "",
        structural[["signal_name", "missing_pct", "finite_pct", "date_coverage", "turnover_proxy", "turnover_p95"]].to_markdown(index=False),
        "",
        "## IC / Horizon Behavior",
        "",
        best[["signal_name", "horizon", "mean_ic", "abs_mean_ic", "ic_ir", "positive_ic_rate", "n_dates"]].to_markdown(index=False),
        "",
        "## WFV-Style Diagnostics",
        "",
        wfv.to_markdown(index=False) if not wfv.empty else "WFV-style diagnostics were not available.",
        "",
        "## Stress / Regime Observations",
        "",
        "Best-state slices by absolute mean IC:",
        "",
        stress.sort_values("mean_ic", key=lambda s: s.abs(), ascending=False).head(20).to_markdown(index=False),
        "",
        "## Orthogonality Summary",
        "",
        top_orth.sort_values("max_abs_corr", ascending=False).to_markdown(index=False),
        "",
        "Important: high baseline correlation is treated as a review or rejection reason even when IC is positive.",
        "",
        "## Candidate Decisions",
        "",
        decisions.to_markdown(index=False),
        "",
        "## Watchlist / Further Validation Candidates",
        "",
        watch.to_markdown(index=False) if not watch.empty else "No candidates advanced to watchlist or further-validation status.",
        "",
        "## Rejected Candidates",
        "",
        rejected.to_markdown(index=False) if not rejected.empty else "No candidates were rejected.",
        "",
        "## Lessons Learned",
        "",
        "- Track B can move faster without loosening rejection discipline.",
        "- Orthogonality checks should remain early in discovery, especially versus plain reversal, momentum, and Track A volume reversal.",
        "- Several candidates can show plausible IC while still failing persistence, sign consistency, or redundancy checks.",
        "- State-specific strength remains diagnostic only; it does not turn a standalone candidate into a conditional-alpha path.",
        "",
        "## Recommended Next Batch",
        "",
        "Run a targeted refinement only around candidates that reached `WATCHLIST_RESEARCH` or `CANDIDATE_FOR_FURTHER_VALIDATION`. Focus on reducing baseline redundancy and improving WFV persistence before any onboarding-style draft definition work.",
    ]
    NOTE_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    _ensure_dirs()
    panels, benchmark = load_inputs()
    signals = build_candidate_panels(panels, benchmark)
    registry = pd.DataFrame(CANDIDATES)
    registry["run_id"] = RUN_ID
    registry["research_status"] = "TRACK_B_RESEARCH_ONLY"

    structural = structural_summary(signals)
    scores, daily_ics = score_signals(signals, panels["close"])
    states = build_stress_states(panels["close"], benchmark)
    stress = stress_attribution(daily_ics, scores, states)
    wfv_summary, wfv_windows = wfv_diagnostics(daily_ics, scores)
    refs = baseline_panels(signals, panels, benchmark)
    orth = orthogonality(signals, refs)
    decisions = classify_candidates(structural, scores, wfv_summary, orth)

    registry.to_csv(OUT_DIR / "candidate_registry.csv", index=False)
    structural.to_csv(OUT_DIR / "structural_quality_summary.csv", index=False)
    scores.to_csv(OUT_DIR / "multi_horizon_scoring.csv", index=False)
    daily_ics.to_csv(OUT_DIR / "daily_ic_by_signal_horizon.csv", index=False)
    stress.to_csv(OUT_DIR / "stress_regime_attribution.csv", index=False)
    wfv_summary.to_csv(OUT_DIR / "wfv_style_summary.csv", index=False)
    wfv_windows.to_csv(OUT_DIR / "wfv_window_diagnostics.csv", index=False)
    orth.to_csv(OUT_DIR / "orthogonality_redundancy_audit.csv", index=False)
    decisions.to_csv(OUT_DIR / "candidate_classification.csv", index=False)
    for name, panel in signals.items():
        panel.to_parquet(OUT_DIR / f"{name}_signal_panel.parquet")
    (OUT_DIR / "manifest.json").write_text(
        json.dumps(
            {
                "run_id": RUN_ID,
                "research_only": True,
                "candidate_count": len(signals),
                "production_registration": False,
                "production_logic_modified": False,
                "track_a_status_modified": False,
                "artifacts": sorted(p.name for p in OUT_DIR.iterdir()),
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )
    write_note(registry, structural, scores, wfv_summary, stress, orth, decisions)
    print(f"WROTE {OUT_DIR}")
    print(f"WROTE {NOTE_PATH}")
    print(decisions.to_string(index=False))


if __name__ == "__main__":
    main()
