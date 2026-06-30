from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

from run_dispersion_recovery_stability_after_stress_v1 import VOLATILITY_INVENTORY_PATH
from run_structural_interaction_alpha_discovery_batch_v1 import (
    _active_coverage_summary,
    _clean_panel,
    _finalize_signal,
    _market_state_panel,
    _max_corr_table,
    _rank01,
    _rank_cs,
    _safe_div,
    fragility_concentration_summary,
    reference_panels,
    state_attribution,
)
from run_track_b_robustness_discovery_v3 import (
    build_stress_states,
    daily_ic,
    forward_returns,
    load_inputs,
    orthogonality,
    score_signals,
    stress_attribution,
    structural_summary,
    wfv_diagnostics,
)
from run_track_b_robustness_discovery_v4 import _cs_neutralize
from run_track_b_v6_focused_discovery import BREADTH_INVENTORY_PATH, LIQUIDITY_INVENTORY_PATH


RUN_ID = "proxy_relative_residual_alpha_batch_v1"
OUT_DIR = Path("artifacts/research") / RUN_ID
NOTE_PATH = Path("docs/research_notes/proxy_relative_residual_alpha_batch_v1.md")
HORIZONS = (1, 5, 10, 15, 20)

RESEARCH_ONLY_GUARDRAIL = (
    "This is a research-only proxy-relative residual alpha batch. It is not sector-relative research, "
    "does not fetch external metadata, does not modify detector code or labels, does not register "
    "production signals, does not mutate survivor/watchlist state, does not change gates, schemas, "
    "thresholds, validation logic, or governance, and does not route anything into portfolio, ML, "
    "blending, or optimization workflows."
)


CANDIDATES: list[dict[str, str]] = [
    {
        "signal_name": "proxy_relative_resilience_20",
        "family": "proxy_relative_resilience",
        "proxy_bucket": "market_relative_behavior_bucket",
        "mechanism_thesis": "Residual resilience is more informative when compared against names with similar trailing market-relative behavior.",
        "expected_horizon": "h10-h20",
    },
    {
        "signal_name": "liquidity_bucket_relative_repair_20",
        "family": "liquidity_bucket_repair",
        "proxy_bucket": "liquidity_bucket",
        "mechanism_thesis": "Liquidity repair should be judged against names with similar trailing liquidity, not the whole universe.",
        "expected_horizon": "h10-h20",
    },
    {
        "signal_name": "volatility_bucket_residual_stability_20",
        "family": "volatility_bucket_stability",
        "proxy_bucket": "volatility_bucket",
        "mechanism_thesis": "Residual stability may be cleaner when measured relative to similarly volatile names.",
        "expected_horizon": "h10-h20",
    },
    {
        "signal_name": "turnover_bucket_exhaustion_residual_10_20",
        "family": "turnover_bucket_exhaustion",
        "proxy_bucket": "turnover_bucket",
        "mechanism_thesis": "Turnover exhaustion should be compared with names experiencing similar turnover intensity to avoid raw volume-event duplication.",
        "expected_horizon": "h10-h20",
    },
    {
        "signal_name": "residual_vol_bucket_quality_recovery_20",
        "family": "residual_vol_bucket_recovery",
        "proxy_bucket": "residual_vol_bucket",
        "mechanism_thesis": "Quality recovery among names with similar residual volatility may separate idiosyncratic repair from low-volatility carry.",
        "expected_horizon": "h10-h20",
    },
    {
        "signal_name": "liquidity_volatility_peer_residual_quality_20",
        "family": "liquidity_volatility_peer_quality",
        "proxy_bucket": "liquidity_x_volatility_proxy_bucket",
        "mechanism_thesis": "Residual quality that survives joint liquidity and volatility proxy comparison may be less broad than absolute-state interaction signals.",
        "expected_horizon": "h10-h20",
    },
]


def _ensure_dirs() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    NOTE_PATH.parent.mkdir(parents=True, exist_ok=True)


def _series_to_panel(series: pd.Series, columns: pd.Index) -> pd.DataFrame:
    return pd.DataFrame(np.repeat(series.to_numpy()[:, None], len(columns), axis=1), index=series.index, columns=columns)


def _bucketize(panel: pd.DataFrame, n_buckets: int = 3, min_names: int = 25, shift: int = 1) -> pd.DataFrame:
    ranked = panel.rank(axis=1, pct=True, method="average")
    buckets = np.ceil(ranked * n_buckets).clip(1, n_buckets)
    buckets = buckets.where(panel.notna())
    if shift:
        buckets = buckets.shift(shift)
    counts = buckets.notna().sum(axis=1)
    buckets = buckets.where(counts.ge(min_names))
    return buckets.astype("float")


def _bucket_demean(values: pd.DataFrame, buckets: pd.DataFrame, min_bucket_size: int = 10) -> pd.DataFrame:
    values, buckets = values.align(buckets, join="inner", axis=0)
    values, buckets = values.align(buckets, join="inner", axis=1)
    out = pd.DataFrame(np.nan, index=values.index, columns=values.columns)
    for date in values.index:
        row = values.loc[date]
        bucket_row = buckets.loc[date]
        for bucket in sorted(bucket_row.dropna().unique()):
            members = bucket_row.eq(bucket) & row.notna()
            if int(members.sum()) >= min_bucket_size:
                out.loc[date, members] = row.loc[members] - row.loc[members].mean()
    return _clean_panel(out)


def _bucket_rank(values: pd.DataFrame, buckets: pd.DataFrame, min_bucket_size: int = 10) -> pd.DataFrame:
    values, buckets = values.align(buckets, join="inner", axis=0)
    values, buckets = values.align(buckets, join="inner", axis=1)
    out = pd.DataFrame(np.nan, index=values.index, columns=values.columns)
    for date in values.index:
        row = values.loc[date]
        bucket_row = buckets.loc[date]
        for bucket in sorted(bucket_row.dropna().unique()):
            members = bucket_row.eq(bucket) & row.notna()
            if int(members.sum()) >= min_bucket_size:
                ranked = row.loc[members].rank(pct=True, method="average")
                out.loc[date, members] = (ranked - 0.5) * 2.0
    return _clean_panel(out)


def _bucket_name_counts(buckets: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for date in buckets.index:
        row = buckets.loc[date].dropna()
        for bucket, count in row.value_counts().sort_index().items():
            rows.append({"Date": date, "bucket": int(bucket), "n_names": int(count)})
    return pd.DataFrame(rows)


def _soft_balance(*components: pd.DataFrame) -> pd.DataFrame:
    stacked = pd.concat([component.stack().rename(i) for i, component in enumerate(components)], axis=1)
    if stacked.empty:
        return components[0] * np.nan
    dispersion = stacked.std(axis=1)
    mean = stacked.mean(axis=1)
    balance = (mean - dispersion).unstack().reindex(index=components[0].index, columns=components[0].columns)
    return balance.clip(lower=0.0)


def _finalize_proxy_signal(raw: pd.DataFrame, exposures: list[pd.DataFrame], rebalance: int = 10) -> pd.DataFrame:
    active = raw.notna() & raw.gt(0)
    return _finalize_signal(raw, active, exposures, rebalance=rebalance)


def _candidate_metadata() -> pd.DataFrame:
    registry = pd.DataFrame(CANDIDATES)
    registry["run_id"] = RUN_ID
    registry["research_status"] = "RESEARCH_ONLY"
    registry["relative_label"] = "proxy_relative_not_sector_relative"
    return registry


def _beta_panel(ret1: pd.DataFrame, benchmark: pd.Series, window: int = 60) -> pd.DataFrame:
    bench_ret = benchmark.pct_change(1, fill_method=None)
    bench_panel = _series_to_panel(bench_ret, ret1.columns)
    cov = ret1.rolling(window, min_periods=40).cov(bench_panel)
    var = bench_ret.rolling(window, min_periods=40).var()
    return cov.divide(var, axis=0).clip(-3, 3).replace([np.inf, -np.inf], np.nan)


def build_candidate_panels(
    panels: dict[str, pd.DataFrame],
    benchmark: pd.Series,
) -> tuple[
    dict[str, pd.DataFrame],
    dict[str, dict[str, pd.DataFrame]],
    dict[str, pd.DataFrame],
    dict[str, pd.DataFrame],
    pd.DataFrame,
    pd.DataFrame,
    pd.DataFrame,
]:
    close = panels["close"]
    high = panels["high"]
    low = panels["low"]
    volume = panels["volume"].astype(float).where(panels["volume"].astype(float) > 0)

    ret1 = close.pct_change(1, fill_method=None)
    ret5 = close.pct_change(5, fill_method=None)
    ret10 = close.pct_change(10, fill_method=None)
    ret20 = close.pct_change(20, fill_method=None)
    ret60 = close.pct_change(60, fill_method=None)
    bench_ret1 = benchmark.pct_change(1, fill_method=None)
    bench_ret5 = benchmark.pct_change(5, fill_method=None)
    bench_ret10 = benchmark.pct_change(10, fill_method=None)
    bench_ret20 = benchmark.pct_change(20, fill_method=None)
    bench_ret60 = benchmark.pct_change(60, fill_method=None)

    residual1 = ret1.sub(bench_ret1, axis=0)
    residual5 = ret5.sub(bench_ret5, axis=0)
    residual10 = ret10.sub(bench_ret10, axis=0)
    residual20 = ret20.sub(bench_ret20, axis=0)
    residual60 = ret60.sub(bench_ret60, axis=0)
    residual_vol10 = residual1.rolling(10, min_periods=7).std()
    residual_vol20 = residual1.rolling(20, min_periods=12).std()
    residual_vol60 = residual1.rolling(60, min_periods=40).std()

    true_range = ((high - low) / close.shift(1)).replace([np.inf, -np.inf], np.nan)
    range5 = true_range.rolling(5, min_periods=4).mean()
    range20 = true_range.rolling(20, min_periods=12).mean()
    range60 = true_range.rolling(60, min_periods=40).mean()
    close_location = ((close - low) / (high - low).replace(0.0, np.nan)).clip(0.0, 1.0)
    close_support = close_location.rolling(10, min_periods=6).mean()

    dollar_volume = close * volume
    adv20 = dollar_volume.rolling(20, min_periods=12).mean()
    adv60 = dollar_volume.rolling(60, min_periods=40).mean()
    turnover_ratio = _safe_div(adv20, adv60).clip(0, 5)
    turnover5 = _safe_div(dollar_volume.rolling(5, min_periods=4).mean(), adv20).clip(0, 5)
    turnover_decay = (1.0 - _rank01(turnover5)).clip(lower=0.0)
    liquidity_quality = (_rank01(turnover_ratio) * (1.0 - _rank01(_safe_div(true_range, dollar_volume.replace(0.0, np.nan)).rolling(10, min_periods=6).mean()))).clip(lower=0.0)

    vol20 = ret1.rolling(20, min_periods=12).std()
    vol60 = ret1.rolling(60, min_periods=40).std()
    beta = _beta_panel(ret1, benchmark)
    rank_churn20 = residual20.rank(axis=1, pct=True).diff().abs().rolling(20, min_periods=12).mean()
    rank_stability = (1.0 - _rank01(rank_churn20)).clip(lower=0.0)
    residual_vol_stability = (1.0 - _rank01(_safe_div(residual_vol10, residual_vol60))).clip(lower=0.0)
    range_repair = (1.0 - _rank01(_safe_div(range5, range20))).clip(lower=0.0)
    range_normalization = (1.0 - _rank01(_safe_div(range20, range60))).clip(lower=0.0)
    low_extension = (1.0 - ret20.rank(axis=1, pct=True).sub(0.5).abs() * 2.0).clip(lower=0.0)
    low_short_extension = (1.0 - ret5.rank(axis=1, pct=True).sub(0.5).abs() * 2.0).clip(lower=0.0)
    drawdown20 = close / close.rolling(20, min_periods=12).max() - 1.0
    residual_drawdown_pressure = _rank01((-drawdown20).clip(lower=0.0))
    residual_recovery = _rank01(residual10.clip(lower=0.0) + residual20.clip(lower=0.0))
    recovery_efficiency = _rank01(_safe_div(close_support.diff(10).clip(lower=0.0), range20 + residual_vol20))

    liquidity_bucket = _bucketize(_rank01(adv20), n_buckets=3, shift=1)
    volatility_bucket = _bucketize(_rank01(vol20), n_buckets=3, shift=1)
    residual_vol_bucket = _bucketize(_rank01(residual_vol20), n_buckets=3, shift=1)
    turnover_bucket = _bucketize(_rank01(turnover_ratio), n_buckets=3, shift=1)
    beta_bucket = _bucketize(_rank01(beta), n_buckets=3, shift=1)
    market_relative_bucket = _bucketize(_rank01(residual20), n_buckets=3, shift=1)

    liq_vol_combo_exposure = (_rank01(adv20) + _rank01(vol20)) / 2.0
    liq_vol_bucket = _bucketize(liq_vol_combo_exposure, n_buckets=3, shift=1)

    residual_resilience = _bucket_rank(residual20 * low_extension, market_relative_bucket)
    liquidity_repair = _bucket_rank(liquidity_quality * range_repair * close_support, liquidity_bucket)
    vol_relative_stability = _bucket_rank(rank_stability * residual_vol_stability * close_support, volatility_bucket)
    turnover_exhaustion = _bucket_rank(turnover_decay * range_repair * low_short_extension, turnover_bucket)
    residual_vol_quality = _bucket_rank(recovery_efficiency * residual_vol_stability * liquidity_quality, residual_vol_bucket)
    liq_vol_quality = _bucket_rank(
        _soft_balance(liquidity_quality, residual_vol_stability, close_support, range_normalization, low_extension),
        liq_vol_bucket,
    )

    raw_scores = {
        "proxy_relative_resilience_20": residual_resilience,
        "liquidity_bucket_relative_repair_20": liquidity_repair,
        "volatility_bucket_residual_stability_20": vol_relative_stability,
        "turnover_bucket_exhaustion_residual_10_20": turnover_exhaustion,
        "residual_vol_bucket_quality_recovery_20": residual_vol_quality,
        "liquidity_volatility_peer_residual_quality_20": liq_vol_quality,
    }
    components = {
        "proxy_relative_resilience_20": {
            "bucket_relative_residual_resilience": residual_resilience,
            "residual20": _rank_cs(residual20),
            "low_extension": low_extension,
            "market_relative_bucket": market_relative_bucket,
        },
        "liquidity_bucket_relative_repair_20": {
            "bucket_relative_liquidity_repair": liquidity_repair,
            "liquidity_quality": liquidity_quality,
            "range_repair": range_repair,
            "close_support": close_support,
        },
        "volatility_bucket_residual_stability_20": {
            "bucket_relative_stability": vol_relative_stability,
            "rank_stability": rank_stability,
            "residual_vol_stability": residual_vol_stability,
            "close_support": close_support,
        },
        "turnover_bucket_exhaustion_residual_10_20": {
            "bucket_relative_turnover_exhaustion": turnover_exhaustion,
            "turnover_decay": turnover_decay,
            "range_repair": range_repair,
            "low_short_extension": low_short_extension,
        },
        "residual_vol_bucket_quality_recovery_20": {
            "bucket_relative_quality_recovery": residual_vol_quality,
            "recovery_efficiency": recovery_efficiency,
            "residual_vol_stability": residual_vol_stability,
            "liquidity_quality": liquidity_quality,
        },
        "liquidity_volatility_peer_residual_quality_20": {
            "bucket_relative_liq_vol_quality": liq_vol_quality,
            "liquidity_quality": liquidity_quality,
            "residual_vol_stability": residual_vol_stability,
            "range_normalization": range_normalization,
            "low_extension": low_extension,
        },
    }

    exposures = [
        _rank_cs(ret5),
        _rank_cs(ret20),
        _rank_cs(ret60),
        _rank_cs(-ret5),
        _rank_cs(-ret20),
        _rank_cs(vol20),
        _rank_cs(residual_vol20),
    ]
    signals = {
        name: _finalize_proxy_signal(raw, exposures, rebalance=10)
        for name, raw in raw_scores.items()
    }

    stress = build_stress_states(close, benchmark)
    states = pd.DataFrame(index=close.index)
    states["HIGH_LIQUIDITY_PROXY"] = liquidity_bucket.eq(3).sum(axis=1).ge(25)
    states["HIGH_VOLATILITY_PROXY"] = volatility_bucket.eq(3).sum(axis=1).ge(25)
    states["HIGH_RESIDUAL_VOL_PROXY"] = residual_vol_bucket.eq(3).sum(axis=1).ge(25)
    states["HIGH_TURNOVER_PROXY"] = turnover_bucket.eq(3).sum(axis=1).ge(25)
    states["HIGH_BETA_PROXY"] = beta_bucket.eq(3).sum(axis=1).ge(25)
    states["BROAD_STRESS"] = stress[["drawdown_acceleration", "volatility_spike", "panic_liquidity_stress", "weak_breadth"]].any(axis=1)
    states["VOLATILITY_SPIKE"] = stress["volatility_spike"].fillna(False)
    states["WEAK_BREADTH"] = stress["weak_breadth"].fillna(False)

    buckets = {
        "liquidity_bucket": liquidity_bucket,
        "volatility_bucket": volatility_bucket,
        "residual_vol_bucket": residual_vol_bucket,
        "turnover_bucket": turnover_bucket,
        "beta_bucket": beta_bucket,
        "market_relative_bucket": market_relative_bucket,
        "liquidity_volatility_bucket": liq_vol_bucket,
    }
    bucket_frames = []
    for bucket_name, bucket_panel in buckets.items():
        counts = _bucket_name_counts(bucket_panel)
        if not counts.empty:
            counts["proxy_bucket_name"] = bucket_name
            bucket_frames.append(counts)
    bucket_long = pd.concat(bucket_frames, ignore_index=True) if bucket_frames else pd.DataFrame()

    references = {
        "plain_residual_momentum_20": _rank_cs(residual20),
        "plain_residual_reversal_20": _rank_cs(-residual20),
        "plain_low_volatility_20": _rank_cs(-vol20),
        "plain_low_residual_volatility_20": _rank_cs(-residual_vol20),
        "plain_beta_60": _rank_cs(beta),
        "plain_liquidity_quality": _rank_cs(liquidity_quality),
        "plain_recovery_efficiency": _rank_cs(recovery_efficiency),
        "plain_drawdown_pressure": _rank_cs(residual_drawdown_pressure),
        "plain_residual_recovery": _rank_cs(residual_recovery),
    }

    return (
        {k: _clean_panel(v) for k, v in signals.items()},
        components,
        references,
        buckets,
        bucket_long,
        states.fillna(False).astype(bool),
        stress,
    )


def bucket_coverage_summary(bucket_long: pd.DataFrame) -> pd.DataFrame:
    if bucket_long.empty:
        return pd.DataFrame()
    rows = []
    for (name, bucket), group in bucket_long.groupby(["proxy_bucket_name", "bucket"]):
        rows.append(
            {
                "proxy_bucket_name": name,
                "bucket": int(bucket),
                "n_dates": int(group["Date"].nunique()),
                "mean_names": float(group["n_names"].mean()),
                "min_names": int(group["n_names"].min()),
                "p10_names": float(group["n_names"].quantile(0.10)),
                "thin_bucket_date_ratio_lt10": float(group["n_names"].lt(10).mean()),
                "thin_bucket_date_ratio_lt25": float(group["n_names"].lt(25).mean()),
            }
        )
    return pd.DataFrame(rows)


def bucket_stability_summary(bucket_long: pd.DataFrame) -> pd.DataFrame:
    if bucket_long.empty:
        return pd.DataFrame()
    rows = []
    pivot = bucket_long.pivot_table(index=["Date", "proxy_bucket_name"], columns="bucket", values="n_names", aggfunc="sum")
    for name, group in pivot.groupby(level="proxy_bucket_name"):
        data = group.droplevel("proxy_bucket_name").sort_index()
        total = data.sum(axis=1).replace(0, np.nan)
        shares = data.div(total, axis=0)
        drift = shares.diff().abs().sum(axis=1)
        rows.append(
            {
                "proxy_bucket_name": name,
                "mean_total_names": float(total.mean()),
                "mean_abs_bucket_share_drift": float(drift.mean()),
                "p95_abs_bucket_share_drift": float(drift.quantile(0.95)),
                "max_abs_bucket_share_drift": float(drift.max()),
                "dominant_bucket_share_mean": float(shares.max(axis=1).mean()),
                "dominant_bucket_share_p95": float(shares.max(axis=1).quantile(0.95)),
                "bucket_instability_flag": bool(drift.mean() > 0.20 or shares.max(axis=1).quantile(0.95) > 0.60),
            }
        )
    return pd.DataFrame(rows)


def bucket_conditioned_ic_summary(
    signals: dict[str, pd.DataFrame],
    close: pd.DataFrame,
    scores: pd.DataFrame,
    bucket_panels: dict[str, pd.DataFrame],
) -> pd.DataFrame:
    if not bucket_panels:
        return pd.DataFrame()
    best = scores.loc[scores["is_best_horizon"], ["signal_name", "best_horizon"]].set_index("signal_name")["best_horizon"]
    rows = []
    for signal_name, horizon in best.items():
        fwd = forward_returns(close, int(horizon))
        signal = signals[signal_name]
        for proxy_bucket_name, bucket_panel in bucket_panels.items():
            for bucket in sorted(bucket_panel.stack().dropna().unique()):
                mask = bucket_panel.eq(bucket)
                masked_signal = signal.where(mask)
                sample = daily_ic(masked_signal, fwd).dropna()
                rows.append(
                    {
                        "signal_name": signal_name,
                        "horizon": int(horizon),
                        "proxy_bucket_name": proxy_bucket_name,
                        "bucket": int(bucket),
                        "n_dates": int(len(sample)),
                        "mean_ic": float(sample.mean()) if len(sample) else np.nan,
                        "positive_ic_rate": float((sample > 0).mean()) if len(sample) else np.nan,
                    }
                )
    return pd.DataFrame(rows)


def proxy_fragility_summary(
    decisions_base: pd.DataFrame,
    bucket_ic: pd.DataFrame,
    bucket_stability: pd.DataFrame,
) -> pd.DataFrame:
    rows = []
    for signal_name, group in bucket_ic.groupby("signal_name"):
        valid = group.dropna(subset=["mean_ic"])
        if valid.empty:
            continue
        positive = valid[valid["mean_ic"] > 0]
        best = valid.loc[valid["mean_ic"].idxmax()]
        one_bucket_dominance = float(best["mean_ic"] / positive["mean_ic"].sum()) if not positive.empty and positive["mean_ic"].sum() > 0 else np.nan
        unstable_proxy_count = int(bucket_stability["bucket_instability_flag"].sum()) if not bucket_stability.empty else 0
        rows.append(
            {
                "signal_name": signal_name,
                "best_proxy_bucket_name": best["proxy_bucket_name"],
                "best_proxy_bucket": int(best["bucket"]),
                "best_bucket_mean_ic": float(best["mean_ic"]),
                "best_bucket_positive_ic_rate": float(best["positive_ic_rate"]) if pd.notna(best["positive_ic_rate"]) else np.nan,
                "one_bucket_dominance": one_bucket_dominance,
                "one_bucket_dominance_flag": bool(pd.notna(one_bucket_dominance) and one_bucket_dominance > 0.65),
                "unstable_proxy_count": unstable_proxy_count,
                "peer_group_drift_flag": bool(unstable_proxy_count > 0),
            }
        )
    return pd.DataFrame(rows)


def low_vol_overlap_summary(orth: pd.DataFrame) -> pd.DataFrame:
    refs = {
        "plain_low_volatility_20",
        "plain_low_residual_volatility_20",
        "simple_volatility_reversal",
    }
    rows = []
    for name, group in orth.groupby("signal_name"):
        subset = group[group["comparison"].isin(refs)]
        rows.append(
            {
                "signal_name": name,
                "max_low_vol_volcarry_corr": float(subset["abs_value_corr"].max()) if not subset.empty else np.nan,
                "hidden_low_vol_overlap_flag": bool((not subset.empty) and subset["abs_value_corr"].max() > 0.35),
            }
        )
    return pd.DataFrame(rows)


def classify_candidates(
    structural: pd.DataFrame,
    scores: pd.DataFrame,
    wfv: pd.DataFrame,
    stress_attr: pd.DataFrame,
    orth_summary: pd.DataFrame,
    active: pd.DataFrame,
    fragility: pd.DataFrame,
    proxy_fragility: pd.DataFrame,
    low_vol: pd.DataFrame,
) -> pd.DataFrame:
    best = scores.loc[scores["is_best_horizon"]].copy()
    h10 = scores[scores["horizon"].eq(10)].rename(columns={"mean_ic": "h10_mean_ic", "positive_ic_rate": "h10_positive_ic_rate"})
    h20 = scores[scores["horizon"].eq(20)].rename(columns={"mean_ic": "h20_mean_ic", "positive_ic_rate": "h20_positive_ic_rate"})
    stress_counts = (
        stress_attr.groupby("signal_name")["mean_ic"]
        .agg(positive_regime_count=lambda s: int((s > 0.004).sum()), best_regime_ic="max")
        .reset_index()
    )
    summary = (
        best.merge(h10[["signal_name", "h10_mean_ic", "h10_positive_ic_rate"]], on="signal_name", how="left")
        .merge(h20[["signal_name", "h20_mean_ic", "h20_positive_ic_rate"]], on="signal_name", how="left")
        .merge(structural, on="signal_name", how="left")
        .merge(wfv, left_on=["signal_name", "best_horizon"], right_on=["signal_name", "horizon"], how="left")
        .merge(stress_counts, on="signal_name", how="left")
        .merge(orth_summary, on="signal_name", how="left")
        .merge(active, on="signal_name", how="left")
        .merge(fragility[["signal_name", "stress_only_dependency_flag", "crisis_concentration_flag", "one_window_concentration_flag", "regime_exclusivity_flag"]], on="signal_name", how="left")
        .merge(proxy_fragility, on="signal_name", how="left")
        .merge(low_vol, on="signal_name", how="left")
    )
    rows = []
    for _, row in summary.iterrows():
        issues = []
        medium_ic = max(row.get("h10_mean_ic", -np.inf), row.get("h20_mean_ic", -np.inf))
        if row.get("mean_ic", np.nan) < 0:
            issues.append("direction_mismatch")
        if row.get("best_horizon") in (1, 5):
            issues.append("short_horizon_led")
        if row.get("abs_mean_ic", 0) < 0.008:
            issues.append("weak_best_horizon_ic")
        if medium_ic < 0.008:
            issues.append("weak_medium_horizon_ic")
        if row.get("positive_ic_rate", 0) < 0.53:
            issues.append("weak_positive_ic_rate")
        if row.get("persistence", 0) < 0.75:
            issues.append("weak_wfv_persistence")
        if row.get("sign_consistency", 0) < 0.75:
            issues.append("weak_wfv_sign_consistency")
        if row.get("one_window_dominance", 1) > 0.60:
            issues.append("one_window_dominance")
        if row.get("active_date_ratio", 0) > 0.80:
            issues.append("broad_activation_with_weak_ic")
        if row.get("active_date_ratio", 1) < 0.08:
            issues.append("sparse_activation")
        if row.get("max_inventory_corr", 0) > 0.35:
            issues.append("inventory_similarity_risk")
        if row.get("max_reversal_corr", 0) > 0.35:
            issues.append("hidden_reversal_overlap")
        if row.get("max_momentum_corr", 0) > 0.35:
            issues.append("hidden_momentum_overlap")
        if row.get("hidden_low_vol_overlap_flag", False):
            issues.append("hidden_low_vol_volcarry_overlap")
        if row.get("stress_only_dependency_flag", False):
            issues.append("stress_only_dependency")
        if row.get("crisis_concentration_flag", False):
            issues.append("crisis_only_or_crisis_concentration")
        if row.get("one_window_concentration_flag", False):
            issues.append("one_window_concentration_flag")
        if row.get("one_bucket_dominance_flag", False):
            issues.append("one_bucket_dominance")
        if row.get("peer_group_drift_flag", False):
            issues.append("peer_group_drift")

        validation_ready = (
            medium_ic >= 0.018
            and row.get("best_horizon") in (10, 15, 20)
            and row.get("positive_ic_rate", 0) >= 0.56
            and row.get("persistence", 0) >= 0.75
            and row.get("sign_consistency", 0) >= 0.75
            and row.get("one_window_dominance", 1) <= 0.55
            and row.get("max_inventory_corr", 1) <= 0.30
            and row.get("max_reversal_corr", 1) <= 0.30
            and row.get("max_momentum_corr", 1) <= 0.30
            and not row.get("hidden_low_vol_overlap_flag", True)
            and not row.get("crisis_concentration_flag", True)
            and not row.get("one_bucket_dominance_flag", True)
            and not row.get("peer_group_drift_flag", True)
        )
        refinement_ready = (
            medium_ic >= 0.010
            and row.get("best_horizon") in (10, 15, 20)
            and row.get("positive_ic_rate", 0) >= 0.53
            and row.get("persistence", 0) >= 0.75
            and row.get("sign_consistency", 0) >= 0.75
            and row.get("max_inventory_corr", 1) <= 0.35
            and row.get("max_reversal_corr", 1) <= 0.35
            and row.get("max_momentum_corr", 1) <= 0.35
            and not row.get("crisis_concentration_flag", True)
            and not row.get("one_bucket_dominance_flag", True)
        )
        conditional_only = (
            medium_ic >= 0.004
            and row.get("best_horizon") in (10, 15, 20)
            and row.get("positive_regime_count", 0) >= 1
            and row.get("max_inventory_corr", 1) <= 0.45
        )
        if validation_ready:
            status = "CANDIDATE_FOR_CONDITIONAL_VALIDATION"
        elif refinement_ready:
            status = "CONDITIONAL_REFINEMENT_CANDIDATE"
        elif conditional_only:
            status = "CONDITIONAL_ONLY_RESEARCH"
        else:
            status = "REJECT_RESEARCH"

        out = row.to_dict()
        out["status"] = status
        out["review_issues"] = "; ".join(dict.fromkeys(issues)) if issues else "none"
        rows.append(out)
    return pd.DataFrame(rows).sort_values(["status", "h20_mean_ic"], ascending=[True, False])


def write_note(
    registry: pd.DataFrame,
    structural: pd.DataFrame,
    scores: pd.DataFrame,
    wfv: pd.DataFrame,
    stress_attr: pd.DataFrame,
    state_attr: pd.DataFrame,
    orth_summary: pd.DataFrame,
    active: pd.DataFrame,
    bucket_coverage: pd.DataFrame,
    bucket_stability: pd.DataFrame,
    bucket_ic: pd.DataFrame,
    fragility: pd.DataFrame,
    proxy_fragility: pd.DataFrame,
    low_vol: pd.DataFrame,
    decisions: pd.DataFrame,
) -> None:
    status_counts = decisions["status"].value_counts().to_dict()
    h10 = scores[scores["horizon"].eq(10)].sort_values("mean_ic", ascending=False)
    h20 = scores[scores["horizon"].eq(20)].sort_values("mean_ic", ascending=False)
    live = decisions[decisions["status"].isin(["CANDIDATE_FOR_CONDITIONAL_VALIDATION", "CONDITIONAL_REFINEMENT_CANDIDATE"])]
    if live.empty:
        recommendation = "Do not advance to validation or refinement from this batch. Preserve any weak clues as research evidence only."
    else:
        recommendation = "Treat live names as research leads only; require one-by-one review before any refinement or validation plan."
    lines = [
        "# Proxy-Relative Residual Alpha Batch v1",
        "",
        "Date: 2026-05-23",
        "",
        f"Run id: `{RUN_ID}`",
        "",
        "Status: RESEARCH_ONLY_ALPHA_BATCH",
        "",
        "## Research-Only Guardrail",
        "",
        RESEARCH_ONLY_GUARDRAIL,
        "",
        "This batch is proxy-relative, not sector-relative. No sector, industry, GICS, or external peer metadata was used.",
        "",
        "## Executive Takeaway",
        "",
        "This batch tested whether internally defined behavioral peer proxies can improve medium-horizon residual alpha quality.",
        "",
        f"Candidates tested: `{len(registry)}`",
        f"Status counts: `{json.dumps(status_counts, sort_keys=True)}`",
        "",
        "## Candidate Set",
        "",
        registry.to_markdown(index=False),
        "",
        "## Structural Quality And Active Coverage",
        "",
        structural.merge(active, on="signal_name", how="left")[
            [
                "signal_name",
                "missing_pct",
                "finite_pct",
                "date_coverage",
                "turnover_proxy",
                "turnover_p95",
                "active_date_ratio",
                "activation_transitions",
                "mean_active_coverage",
            ]
        ].to_markdown(index=False),
        "",
        "## Multi-Horizon IC",
        "",
        scores[["signal_name", "horizon", "mean_ic", "abs_mean_ic", "ic_ir", "positive_ic_rate", "n_dates", "is_best_horizon"]].to_markdown(index=False),
        "",
        "## h10 Ranking",
        "",
        h10[["signal_name", "mean_ic", "positive_ic_rate", "n_dates"]].to_markdown(index=False),
        "",
        "## h20 Ranking",
        "",
        h20[["signal_name", "mean_ic", "positive_ic_rate", "n_dates"]].to_markdown(index=False),
        "",
        "## WFV-Style Diagnostics",
        "",
        wfv.to_markdown(index=False) if not wfv.empty else "WFV diagnostics unavailable.",
        "",
        "## Proxy Bucket Coverage",
        "",
        bucket_coverage.to_markdown(index=False) if not bucket_coverage.empty else "Bucket coverage unavailable.",
        "",
        "## Proxy Bucket Stability / Drift",
        "",
        bucket_stability.to_markdown(index=False) if not bucket_stability.empty else "Bucket stability unavailable.",
        "",
        "## Bucket-Conditioned IC",
        "",
        bucket_ic.sort_values("mean_ic", ascending=False).groupby("signal_name").head(5).to_markdown(index=False)
        if not bucket_ic.empty
        else "Bucket-conditioned IC unavailable.",
        "",
        "## Baseline / Inventory / Reversal / Momentum Similarity",
        "",
        orth_summary.merge(low_vol, on="signal_name", how="left").to_markdown(index=False),
        "",
        "## Stress / Regime Attribution",
        "",
        stress_attr.sort_values("mean_ic", ascending=False).groupby("signal_name").head(4)[
            ["signal_name", "horizon", "state", "n_dates", "mean_ic", "ic_ir", "positive_ic_rate"]
        ].to_markdown(index=False),
        "",
        "## Proxy State Attribution",
        "",
        state_attr.sort_values("mean_ic", ascending=False).groupby("signal_name").head(4)[
            ["signal_name", "horizon", "state", "n_dates", "mean_ic", "ic_ir", "positive_ic_rate"]
        ].to_markdown(index=False),
        "",
        "## Fragility / Concentration Summary",
        "",
        fragility.to_markdown(index=False),
        "",
        "## Proxy Fragility / One-Bucket Dominance",
        "",
        proxy_fragility.to_markdown(index=False) if not proxy_fragility.empty else "Proxy fragility unavailable.",
        "",
        "## Candidate Decisions",
        "",
        decisions.to_markdown(index=False),
        "",
        "## Recommendation",
        "",
        recommendation,
        "",
        "No candidate should be promoted, registered, added to survivor/watchlist, or routed into validation, portfolio, ML, blending, or optimization from this batch alone.",
    ]
    NOTE_PATH.write_text("\n".join(lines) + "\n")


def main() -> None:
    _ensure_dirs()
    panels, benchmark = load_inputs()
    signals, components, proxy_refs, bucket_panels, bucket_long, states, stress_states = build_candidate_panels(panels, benchmark)
    registry = _candidate_metadata()

    structural = structural_summary(signals)
    scores, daily_ics = score_signals(signals, panels["close"])
    wfv_summary, wfv_windows = wfv_diagnostics(daily_ics, scores)
    stress_attr = stress_attribution(daily_ics, scores, stress_states)
    state_attr = state_attribution(daily_ics, scores, states)
    refs = reference_panels(signals, panels, benchmark)
    refs.update(proxy_refs)
    if LIQUIDITY_INVENTORY_PATH.exists():
        refs["inventory_participation_liquidity_state_shift_20_60"] = pd.read_parquet(LIQUIDITY_INVENTORY_PATH).reindex(
            index=panels["close"].index,
            columns=panels["close"].columns,
        )
    if BREADTH_INVENTORY_PATH.exists():
        refs["inventory_participation_breadth_repair_under_hostile_trend"] = pd.read_parquet(BREADTH_INVENTORY_PATH).reindex(
            index=panels["close"].index,
            columns=panels["close"].columns,
        )
    if VOLATILITY_INVENTORY_PATH.exists():
        refs["inventory_volatility_compression_after_stress_stabilization"] = pd.read_parquet(VOLATILITY_INVENTORY_PATH).reindex(
            index=panels["close"].index,
            columns=panels["close"].columns,
        )
    orth = orthogonality(signals, refs)
    orth_summary = _max_corr_table(orth)
    active = _active_coverage_summary(signals)
    bucket_coverage = bucket_coverage_summary(bucket_long)
    bucket_stability = bucket_stability_summary(bucket_long)
    bucket_ic = bucket_conditioned_ic_summary(signals, panels["close"], scores, bucket_panels)
    fragility = fragility_concentration_summary(daily_ics, scores, stress_states, wfv_summary)
    proxy_fragility = proxy_fragility_summary(scores, bucket_ic, bucket_stability)
    low_vol = low_vol_overlap_summary(orth)
    decisions = classify_candidates(
        structural,
        scores,
        wfv_summary,
        stress_attr,
        orth_summary,
        active,
        fragility,
        proxy_fragility,
        low_vol,
    )

    artifact_files = [
        "candidate_metadata.csv",
        "candidate_score_summary.csv",
        "daily_ic_by_signal_horizon.csv",
        "wfv_summary.csv",
        "wfv_windows.csv",
        "active_coverage_summary.csv",
        "stress_regime_attribution.csv",
        "proxy_state_attribution.csv",
        "baseline_similarity_summary.csv",
        "orthogonality_redundancy_audit.csv",
        "bucket_panel_counts.csv",
        "bucket_panel_manifest.csv",
        "bucket_coverage_summary.csv",
        "bucket_stability_summary.csv",
        "bucket_conditioned_ic_summary.csv",
        "fragility_concentration_summary.csv",
        "proxy_fragility_summary.csv",
        "low_vol_overlap_summary.csv",
        "candidate_decisions.csv",
        "proxy_state_flags.csv",
        "structural_summary.csv",
    ]
    registry.to_csv(OUT_DIR / "candidate_metadata.csv", index=False)
    scores.to_csv(OUT_DIR / "candidate_score_summary.csv", index=False)
    daily_ics.to_csv(OUT_DIR / "daily_ic_by_signal_horizon.csv", index=False)
    wfv_summary.to_csv(OUT_DIR / "wfv_summary.csv", index=False)
    wfv_windows.to_csv(OUT_DIR / "wfv_windows.csv", index=False)
    active.to_csv(OUT_DIR / "active_coverage_summary.csv", index=False)
    stress_attr.to_csv(OUT_DIR / "stress_regime_attribution.csv", index=False)
    state_attr.to_csv(OUT_DIR / "proxy_state_attribution.csv", index=False)
    orth_summary.to_csv(OUT_DIR / "baseline_similarity_summary.csv", index=False)
    orth.to_csv(OUT_DIR / "orthogonality_redundancy_audit.csv", index=False)
    bucket_long.to_csv(OUT_DIR / "bucket_panel_counts.csv", index=False)
    bucket_panel_manifest = pd.DataFrame(
        [
            {
                "proxy_bucket_name": name,
                "rows": panel.shape[0],
                "columns": panel.shape[1],
                "finite_pct": float(np.isfinite(panel.to_numpy(dtype=float)).mean()),
                "date_coverage": float(panel.notna().any(axis=1).mean()),
            }
            for name, panel in bucket_panels.items()
        ]
    )
    bucket_panel_manifest.to_csv(OUT_DIR / "bucket_panel_manifest.csv", index=False)
    bucket_coverage.to_csv(OUT_DIR / "bucket_coverage_summary.csv", index=False)
    bucket_stability.to_csv(OUT_DIR / "bucket_stability_summary.csv", index=False)
    bucket_ic.to_csv(OUT_DIR / "bucket_conditioned_ic_summary.csv", index=False)
    fragility.to_csv(OUT_DIR / "fragility_concentration_summary.csv", index=False)
    proxy_fragility.to_csv(OUT_DIR / "proxy_fragility_summary.csv", index=False)
    low_vol.to_csv(OUT_DIR / "low_vol_overlap_summary.csv", index=False)
    decisions.to_csv(OUT_DIR / "candidate_decisions.csv", index=False)
    states.to_csv(OUT_DIR / "proxy_state_flags.csv", index=True)
    structural.to_csv(OUT_DIR / "structural_summary.csv", index=False)

    for name, panel in signals.items():
        file_name = f"{name}_signal_panel.parquet"
        panel.to_parquet(OUT_DIR / file_name)
        artifact_files.append(file_name)

    artifact_files.append("manifest.json")
    (OUT_DIR / "manifest.json").write_text(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": "RESEARCH_ONLY_ALPHA_BATCH",
                "research_only_guardrail": RESEARCH_ONLY_GUARDRAIL,
                "relative_framework": "proxy_relative_not_sector_relative",
                "external_metadata_fetched": False,
                "sector_industry_gics_metadata_used": False,
                "candidate_count": len(signals),
                "candidate_names": list(signals.keys()),
                "proxy_bucket_types": [
                    "liquidity_bucket",
                    "volatility_bucket",
                    "residual_vol_bucket",
                    "turnover_bucket",
                    "beta_bucket",
                    "market_relative_bucket",
                    "liquidity_volatility_bucket",
                ],
                "detector_modified": False,
                "production_registration_changed": False,
                "survivor_watchlist_changed": False,
                "gates_schemas_thresholds_validation_governance_changed": False,
                "portfolio_ml_blending_optimization_route_changed": False,
                "artifact_files": sorted(artifact_files),
            },
            indent=2,
            sort_keys=True,
        )
    )
    write_note(
        registry,
        structural,
        scores,
        wfv_summary,
        stress_attr,
        state_attr,
        orth_summary,
        active,
        bucket_coverage,
        bucket_stability,
        bucket_ic,
        fragility,
        proxy_fragility,
        low_vol,
        decisions,
    )
    print(f"WROTE {OUT_DIR}")
    print(f"WROTE {NOTE_PATH}")
    print(decisions[["signal_name", "status", "best_horizon", "mean_ic", "h10_mean_ic", "h20_mean_ic", "review_issues"]].to_string(index=False))


if __name__ == "__main__":
    main()
