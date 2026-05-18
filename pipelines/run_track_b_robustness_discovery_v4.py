from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

from run_track_b_robustness_discovery_v3 import (
    HORIZONS,
    baseline_panels,
    build_stress_states,
    load_inputs,
    orthogonality,
    score_signals,
    stress_attribution,
    structural_summary,
    wfv_diagnostics,
    _clean_panel,
    _rank_cs,
    _winsor,
    _zscore_ts,
)


RUN_ID = "robustness_first_discovery_expansion_v4"
OUT_DIR = Path("artifacts/research") / RUN_ID
NOTE_PATH = Path("docs/research_notes/robustness_first_discovery_expansion_v4.md")
V3_FAILURE_DIR = Path("artifacts/research/track_b_v3_failure_diagnostics")
V2_DIR = Path("artifacts/research/robustness_first_discovery_expansion_v2")
V3_DIR = Path("artifacts/research/robustness_first_discovery_expansion_v3")


CANDIDATES: list[dict[str, str]] = [
    {
        "signal_name": "early_leadership_formation_5_20",
        "family": "early_leadership",
        "redesigned_mechanism": "New 5-day relative leadership forming before 20-day overextension.",
        "addresses_v3_failure": "Redesigns trend_leadership_persistence_20_60 away from mature trend chasing.",
        "non_reversal_rationale": "Scores early formation under a low-overextension filter rather than fading a prior move.",
        "expected_horizon": "h5-h10",
    },
    {
        "signal_name": "pre_extension_participation_improvement_20",
        "family": "breadth_participation",
        "redesigned_mechanism": "Improving up-day participation before large 20-day price extension.",
        "addresses_v3_failure": "Moves breadth_participation_quality_20 from price-confirmed leadership to pre-extension participation.",
        "non_reversal_rationale": "Uses participation acceleration with neutral/modest price move constraints, not reversal or mature continuation.",
        "expected_horizon": "h5-h20",
    },
    {
        "signal_name": "nonprice_liquidity_persistence_20_60",
        "family": "liquidity_persistence",
        "redesigned_mechanism": "Persistent dollar-volume improvement neutralized against 20-day return rank.",
        "addresses_v3_failure": "Rebuilds liquidity_improvement_momentum_20_60 around non-price liquidity persistence.",
        "non_reversal_rationale": "Removes direct price-rank multiplication and penalizes price exposure.",
        "expected_horizon": "h10-h20",
    },
    {
        "signal_name": "liquidity_participation_accumulation_20",
        "family": "liquidity_participation",
        "redesigned_mechanism": "Volume participation accumulation on non-negative days without strong price extension.",
        "addresses_v3_failure": "Separates accumulation from abnormal-flow reversal and price-rank leadership.",
        "non_reversal_rationale": "Looks for persistent participation quality, not a fade after volume shock.",
        "expected_horizon": "h10-h20",
    },
    {
        "signal_name": "vol_compression_confirmation_20_60",
        "family": "volatility_compression",
        "redesigned_mechanism": "Stable volatility compression confirmed by range location and low jumpiness.",
        "addresses_v3_failure": "Redesigns range_compression_breakout_continuation_20 with stronger confirmation before expansion.",
        "non_reversal_rationale": "Compression quality is the main primitive; price direction is only a mild confirmation.",
        "expected_horizon": "h10-h20",
    },
    {
        "signal_name": "clean_range_expansion_followthrough_20",
        "family": "breakout_quality",
        "redesigned_mechanism": "Clean range expansion after compression with low gap noise and close-location confirmation.",
        "addresses_v3_failure": "Separates clean expansion from noisy chase behavior in breakout continuation.",
        "non_reversal_rationale": "Requires prior compression and low noise; does not invert breakout failures.",
        "expected_horizon": "h5-h10",
    },
    {
        "signal_name": "gap_followthrough_low_churn_10",
        "family": "gap_structure",
        "redesigned_mechanism": "Smoothed gap follow-through with lower event threshold and persistence to reduce sparsity/churn.",
        "addresses_v3_failure": "Redesigns gap_continuation_confirmation_5_20 to reduce missingness and turnover.",
        "non_reversal_rationale": "Measures confirmed follow-through persistence, not gap reversal.",
        "expected_horizon": "h5-h10",
    },
    {
        "signal_name": "rank_stability_before_acceleration_20_60",
        "family": "rank_stability",
        "redesigned_mechanism": "Stable improving rank before top-decile acceleration and overextension.",
        "addresses_v3_failure": "Replaces relative_strength_acceleration_20_60 with pre-acceleration rank quality.",
        "non_reversal_rationale": "Avoids mature extremes and does not invert acceleration.",
        "expected_horizon": "h10-h20",
    },
    {
        "signal_name": "low_overextension_trend_resumption_10_40",
        "family": "regime_gated_continuation",
        "redesigned_mechanism": "Trend resumption only when 40-day return is moderate and volatility is not elevated.",
        "addresses_v3_failure": "Keeps continuation only when overextension risk is low.",
        "non_reversal_rationale": "Conditional continuation gate avoids always-on reversal behavior and late chase entries.",
        "expected_horizon": "h5-h20",
    },
    {
        "signal_name": "dispersion_transition_nonprice_quality_20",
        "family": "dispersion_transition",
        "redesigned_mechanism": "Cross-sectional dispersion transition combined with low idiosyncratic volatility rank.",
        "addresses_v3_failure": "Moves dispersion ideas away from price-rank leadership.",
        "non_reversal_rationale": "State-transition and stability feature, not price-rank or reversal.",
        "expected_horizon": "h10-h20",
    },
    {
        "signal_name": "participation_liquidity_state_shift_20_60",
        "family": "state_shift",
        "redesigned_mechanism": "Joint improvement in participation and liquidity, neutralized against 20-day return rank.",
        "addresses_v3_failure": "Combines participation and liquidity without letting price rank dominate.",
        "non_reversal_rationale": "State-shift feature based on market participation primitives.",
        "expected_horizon": "h10-h20",
    },
    {
        "signal_name": "conditional_low_overextension_breakout_20",
        "family": "conditional_breakout",
        "redesigned_mechanism": "Breakout quality active only when overextension and volatility-spike risk are low.",
        "addresses_v3_failure": "Moves weak breakout continuation into conditional-only research.",
        "non_reversal_rationale": "Conditional activation avoids always-on reversal behavior and noisy chase states.",
        "expected_horizon": "h5-h10",
    },
]


def _ensure_dirs() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    NOTE_PATH.parent.mkdir(parents=True, exist_ok=True)


def _rank_series_to_01(series: pd.Series) -> pd.Series:
    return series.rank(pct=True).fillna(0.5)


def _cs_neutralize(signal: pd.DataFrame, exposure: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for date in signal.index:
        y = signal.loc[date]
        x = exposure.loc[date]
        valid = y.notna() & x.notna()
        resid = pd.Series(np.nan, index=signal.columns, dtype=float)
        if int(valid.sum()) >= 25:
            xv = x[valid].astype(float)
            yv = y[valid].astype(float)
            var = float(xv.var(ddof=0))
            if var > 0:
                beta = float(xv.cov(yv) / var)
                resid.loc[valid] = yv - beta * xv
            else:
                resid.loc[valid] = yv - float(yv.mean())
        rows.append(resid)
    return _clean_panel(pd.DataFrame(rows, index=signal.index, columns=signal.columns))


def _market_state_panel(series: pd.Series, columns: pd.Index) -> pd.DataFrame:
    return pd.DataFrame(
        np.repeat(series.values[:, None], len(columns), axis=1),
        index=series.index,
        columns=columns,
    )


def build_candidate_panels(panels: dict[str, pd.DataFrame], benchmark: pd.Series) -> dict[str, pd.DataFrame]:
    close = panels["close"]
    open_ = panels["open"]
    high = panels["high"]
    low = panels["low"]
    volume = panels["volume"].astype(float).where(panels["volume"].astype(float) > 0)

    ret1 = close.pct_change(1, fill_method=None)
    ret3 = close.pct_change(3, fill_method=None)
    ret5 = close.pct_change(5, fill_method=None)
    ret10 = close.pct_change(10, fill_method=None)
    ret20 = close.pct_change(20, fill_method=None)
    ret40 = close.pct_change(40, fill_method=None)
    ret60 = close.pct_change(60, fill_method=None)

    ret5_rank = _rank_cs(ret5)
    ret10_rank = _rank_cs(ret10)
    ret20_rank = _rank_cs(ret20)
    ret40_rank = _rank_cs(ret40)
    ret60_rank = _rank_cs(ret60)

    price_overextension = ret20_rank.abs()
    low_overextension = (1.0 - price_overextension).clip(lower=0)
    early_leadership = (ret5_rank - ret20_rank.rolling(10, min_periods=6).mean()).clip(lower=0)

    participation_10 = (ret1 > 0).rolling(10, min_periods=7).mean()
    participation_20 = (ret1 > 0).rolling(20, min_periods=15).mean()
    participation_40 = (ret1 > 0).rolling(40, min_periods=25).mean()
    participation_improvement = participation_10 - participation_40

    dollar_volume = close * volume
    dollar_liquidity_10 = dollar_volume.rolling(10, min_periods=7).mean()
    dollar_liquidity_20 = dollar_volume.rolling(20, min_periods=15).mean()
    dollar_liquidity_60 = dollar_volume.rolling(60, min_periods=40).mean()
    liquidity_improvement = _winsor(dollar_liquidity_20 / dollar_liquidity_60 - 1.0, -3, 3)
    liquidity_persistence = _zscore_ts(np.log1p(dollar_liquidity_20), 60).rolling(10, min_periods=6).mean()
    liquidity_accumulation = (
        (volume / volume.rolling(20, min_periods=10).mean()).clip(0, 5)
        * (ret1 >= 0).rolling(5, min_periods=3).mean()
    ).rolling(10, min_periods=6).mean()

    vol10 = ret1.rolling(10, min_periods=8).std()
    vol20 = ret1.rolling(20, min_periods=15).std()
    vol60 = ret1.rolling(60, min_periods=40).std()
    vol_compression = _winsor((vol60 - vol20) / vol60.replace(0, np.nan), -3, 3)
    vol_spike_risk = _rank_cs(vol20 / vol60.replace(0, np.nan) - 1.0).clip(lower=0)
    true_range = ((high - low) / close).replace([np.inf, -np.inf], np.nan)
    tr20 = true_range.rolling(20, min_periods=15).mean()
    tr60 = true_range.rolling(60, min_periods=40).mean()
    range_compression = _winsor((tr60 - tr20) / tr60.replace(0, np.nan), -3, 3)
    range_expansion = _winsor(tr20 / tr20.rolling(60, min_periods=40).mean() - 1.0, -3, 3)
    close_location = (close - low) / (high - low).replace(0, np.nan)
    close_location_10 = close_location.rolling(10, min_periods=6).mean()
    gap_abs = (open_ / close.shift(1) - 1.0).abs()
    low_gap_noise = (1.0 - _rank_cs(gap_abs.rolling(10, min_periods=6).mean()).abs()).clip(lower=0)

    overnight_gap = open_ / close.shift(1) - 1.0
    intraday = close / open_ - 1.0
    gap_followthrough = (np.sign(overnight_gap) * intraday).rolling(10, min_periods=6).mean()
    gap_churn = gap_followthrough.diff().abs().rolling(10, min_periods=6).mean()

    rank_level_20 = ret20.rank(axis=1, pct=True)
    rank_stability = -rank_level_20.rolling(60, min_periods=40).std()
    rank_improvement = rank_level_20 - rank_level_20.shift(20)
    pre_top_decile = (rank_level_20 < 0.85).astype(float)

    dispersion_20 = ret20.std(axis=1)
    dispersion_shift = _rank_series_to_01(dispersion_20 - dispersion_20.rolling(60, min_periods=40).mean())
    dispersion_panel = _market_state_panel(dispersion_shift, close.columns)
    idio_stability = -_rank_cs(vol20)

    bench_ret20 = benchmark.pct_change(20, fill_method=None)
    bench_vol = benchmark.pct_change(1, fill_method=None).rolling(20, min_periods=15).std()
    bench_vol_spike = bench_vol > bench_vol.rolling(252, min_periods=100).quantile(0.75)
    market_low_overextension = benchmark.pct_change(40, fill_method=None).abs() < benchmark.pct_change(40, fill_method=None).abs().rolling(252, min_periods=100).quantile(0.65)
    conditional_ok = _market_state_panel((~bench_vol_spike & market_low_overextension).fillna(False).astype(float), close.columns)

    modest_price_move = (1.0 - ret20_rank.abs()).clip(lower=0)
    low_vol_gate = (1.0 - vol_spike_risk).clip(lower=0)
    mild_trend = ret10_rank.clip(lower=0) * (1.0 - ret40_rank.abs()).clip(lower=0)

    nonprice_liquidity_raw = _rank_cs(liquidity_persistence * liquidity_improvement.clip(lower=0))
    nonprice_liquidity = _rank_cs(_cs_neutralize(nonprice_liquidity_raw, ret20_rank))

    participation_liquidity_raw = _rank_cs(participation_improvement.clip(lower=0) * liquidity_improvement.clip(lower=0))
    participation_liquidity_shift = _rank_cs(_cs_neutralize(participation_liquidity_raw, ret20_rank))

    candidates = {
        "early_leadership_formation_5_20": _rank_cs((early_leadership * low_overextension).rolling(5, min_periods=3).mean()),
        "pre_extension_participation_improvement_20": _rank_cs(
            (participation_improvement.clip(lower=0) * modest_price_move).rolling(5, min_periods=3).mean()
        ),
        "nonprice_liquidity_persistence_20_60": nonprice_liquidity,
        "liquidity_participation_accumulation_20": _rank_cs(
            (liquidity_accumulation * participation_20 * modest_price_move).rolling(5, min_periods=3).mean()
        ),
        "vol_compression_confirmation_20_60": _rank_cs(
            (vol_compression.clip(lower=0) * close_location_10 * low_gap_noise).rolling(5, min_periods=3).mean()
        ),
        "clean_range_expansion_followthrough_20": _rank_cs(
            (range_compression.shift(10).clip(lower=0) * range_expansion.clip(lower=0) * close_location_10 * low_gap_noise).rolling(5, min_periods=3).mean()
        ),
        "gap_followthrough_low_churn_10": _rank_cs(
            (gap_followthrough * (1.0 - _rank_cs(gap_churn).abs()).clip(lower=0)).rolling(5, min_periods=3).mean()
        ),
        "rank_stability_before_acceleration_20_60": _rank_cs(
            (rank_stability.rank(axis=1, pct=True) * rank_improvement.clip(lower=0) * pre_top_decile).rolling(10, min_periods=6).mean()
        ),
        "low_overextension_trend_resumption_10_40": _rank_cs(
            (mild_trend * low_vol_gate * modest_price_move).rolling(5, min_periods=3).mean()
        ),
        "dispersion_transition_nonprice_quality_20": _rank_cs(
            (dispersion_panel * idio_stability.clip(lower=0) * modest_price_move).rolling(5, min_periods=3).mean()
        ),
        "participation_liquidity_state_shift_20_60": participation_liquidity_shift,
        "conditional_low_overextension_breakout_20": _rank_cs(
            (conditional_ok * range_compression.shift(10).clip(lower=0) * close_location_10 * low_vol_gate).rolling(5, min_periods=3).mean()
        ),
    }
    return {name: _clean_panel(panel) for name, panel in candidates.items()}


def load_prior_track_references(index: pd.Index, columns: pd.Index) -> dict[str, pd.DataFrame]:
    refs = {}
    for prefix, directory in [("v2", V2_DIR), ("v3", V3_DIR)]:
        if not directory.exists():
            continue
        for path in sorted(directory.glob("*_signal_panel.parquet")):
            refs[f"{prefix}_{path.name.removesuffix('_signal_panel.parquet')}"] = pd.read_parquet(path).reindex(
                index=index, columns=columns
            )
    return refs


def reference_panels(signals: dict[str, pd.DataFrame], panels: dict[str, pd.DataFrame], benchmark: pd.Series) -> dict[str, pd.DataFrame]:
    refs = baseline_panels(signals, panels, benchmark)
    first_panel = next(iter(signals.values()))
    refs.update(load_prior_track_references(first_panel.index, first_panel.columns))
    return refs


def _family_for(signal_name: str) -> str:
    for spec in CANDIDATES:
        if spec["signal_name"] == signal_name:
            return spec["family"]
    return "unknown"


def _conditional_family(signal_name: str) -> bool:
    return _family_for(signal_name).startswith("conditional") or "conditional" in signal_name


def classify_candidates(structural: pd.DataFrame, scores: pd.DataFrame, wfv: pd.DataFrame, stress: pd.DataFrame, orth: pd.DataFrame) -> pd.DataFrame:
    best_scores = scores.loc[scores["is_best_horizon"]].copy()
    max_corr = orth.groupby("signal_name")["abs_value_corr"].max().rename("max_abs_baseline_corr")
    stress_counts = (
        stress.groupby("signal_name")["mean_ic"]
        .agg(positive_regime_count=lambda s: int((s > 0.002).sum()), best_regime_ic="max")
        .reset_index()
    )
    summary = (
        best_scores.merge(structural, on="signal_name", how="left")
        .merge(max_corr, on="signal_name", how="left")
        .merge(wfv, on=["signal_name", "horizon"], how="left", suffixes=("", "_wfv"))
        .merge(stress_counts, on="signal_name", how="left")
    )
    decisions = []
    for _, row in summary.iterrows():
        issues = []
        if row["missing_pct"] > 0.20:
            issues.append("high_missingness")
        if row["turnover_proxy"] > 0.18:
            issues.append("high_turnover")
        if row["mean_ic"] < 0:
            issues.append("direction_mismatch")
        if row["abs_mean_ic"] < 0.005:
            issues.append("weak_best_horizon_ic")
        if row["positive_ic_rate"] < 0.51:
            issues.append("weak_positive_ic_rate")
        if pd.notna(row.get("persistence")) and row["persistence"] < 0.75:
            issues.append("weak_wfv_persistence")
        if pd.notna(row.get("sign_consistency")) and row["sign_consistency"] < 0.75:
            issues.append("weak_wfv_sign_consistency")
        if row.get("max_abs_baseline_corr", 0) > 0.75:
            issues.append("high_baseline_similarity")
        elif row.get("max_abs_baseline_corr", 0) > 0.65:
            issues.append("moderate_baseline_similarity")

        positive_regimes = int(row.get("positive_regime_count", 0) or 0)
        if not issues:
            status = "CANDIDATE_FOR_FURTHER_VALIDATION"
        elif (
            row["mean_ic"] > 0
            and row["abs_mean_ic"] >= 0.005
            and row["max_abs_baseline_corr"] <= 0.75
            and len([i for i in issues if i not in {"weak_wfv_persistence", "weak_wfv_sign_consistency"}]) <= 1
        ):
            status = "WATCHLIST_RESEARCH"
        elif (
            (_conditional_family(row["signal_name"]) or positive_regimes >= 2)
            and row.get("max_abs_baseline_corr", 1) <= 0.75
            and row.get("best_regime_ic", 0) > 0.004
            and row["missing_pct"] <= 0.25
        ):
            status = "CONDITIONAL_ONLY_RESEARCH"
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
                "positive_regime_count": positive_regimes,
                "best_regime_ic": row.get("best_regime_ic"),
                "status": status,
                "review_issues": "; ".join(issues) if issues else "none",
            }
        )
    return pd.DataFrame(decisions).sort_values(["status", "abs_mean_ic"], ascending=[True, False])


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
    actionable = decisions[decisions["status"].isin(["CANDIDATE_FOR_FURTHER_VALIDATION", "WATCHLIST_RESEARCH", "CONDITIONAL_ONLY_RESEARCH"])]
    rejected = decisions[decisions["status"].eq("REJECT_RESEARCH")]
    stress_best = stress.sort_values("mean_ic", ascending=False).groupby("signal_name").head(2)
    lines = [
        "# Robustness-First Discovery Expansion v4",
        "",
        "## Executive Takeaway",
        "",
        f"Track B ran an isolated mechanism-redesign discovery batch under `{RUN_ID}`.",
        "",
        "This batch used the v3 failure diagnostics to avoid superficial continuation variants, simple inversions, and price-rank reversal proxies. Candidates were redesigned around early formation, non-price liquidity persistence, pre-extension participation, cleaner gap/range structures, rank stability before acceleration, and conditional low-overextension activation.",
        "",
        "This was research-only. It did not register signals, mutate survivor/watchlist lists, alter gates, change schemas, run portfolio construction, use ML, or touch Conditional-Alpha production paths.",
        "",
        f"Candidates tested: {len(registry)}",
        f"Status counts: `{json.dumps(status_counts, sort_keys=True)}`",
        "",
        "## v3 Diagnostics Used",
        "",
        f"- Failure diagnostics source: `{V3_FAILURE_DIR}`",
        "- Key applied lesson: avoid mature price-rank leadership and do not treat sign inversion as a new mechanism.",
        "- Track A `volume_shock_reversal_stable_20` remained an orthogonality baseline only.",
        "",
        "## Candidate Set",
        "",
        registry.to_markdown(index=False),
        "",
        "## Structural Quality And Turnover",
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
        "## Orthogonality / Redundancy",
        "",
        top_orth.sort_values("max_abs_corr", ascending=False).to_markdown(index=False),
        "",
        "## Regime / Stress Behavior",
        "",
        stress_best[["signal_name", "horizon", "state", "n_dates", "mean_ic", "ic_ir", "positive_ic_rate"]].to_markdown(index=False),
        "",
        "## Candidate Decisions",
        "",
        decisions.to_markdown(index=False),
        "",
        "## Actionable Research Candidates",
        "",
        actionable.to_markdown(index=False) if not actionable.empty else "No candidates advanced to watchlist, conditional-only, or further-validation status.",
        "",
        "## Rejected Candidates",
        "",
        rejected.to_markdown(index=False) if not rejected.empty else "No candidates were rejected.",
        "",
        "## Lessons Learned",
        "",
        "- Mechanism redesign reduced some reversal similarity, but orthogonality alone is still not enough.",
        "- Gap and breakout redesigns should be judged first on coverage and turnover before IC.",
        "- Non-price liquidity and participation features should remain separated from direct price-rank multipliers.",
        "- Conditional-only status is research-only and does not create a promotion path.",
        "",
        "## Recommended Next Step",
        "",
        "Carry forward only candidates with `WATCHLIST_RESEARCH`, `CONDITIONAL_ONLY_RESEARCH`, or `CANDIDATE_FOR_FURTHER_VALIDATION` for targeted diagnostics. Do not register or promote any v4 signal without a separate controlled validation step.",
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
    refs = reference_panels(signals, panels, benchmark)
    orth = orthogonality(signals, refs)
    decisions = classify_candidates(structural, scores, wfv_summary, stress, orth)

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
                "v3_failure_diagnostics_used": True,
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
