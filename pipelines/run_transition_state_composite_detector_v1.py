from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

from run_dispersion_recovery_stability_after_stress_v1 import VOLATILITY_INVENTORY_PATH
from run_track_b_robustness_discovery_v3 import (
    build_stress_states,
    daily_ic,
    forward_returns,
    load_inputs,
)
from run_track_b_v6_focused_discovery import BREADTH_INVENTORY_PATH, LIQUIDITY_INVENTORY_PATH


RUN_ID = "transition_state_composite_detector_v1"
OUT_DIR = Path("artifacts/research") / RUN_ID
NOTE_PATH = Path("docs/research_notes/transition_state_composite_detector_v1.md")
HORIZONS = (1, 5, 10, 15, 20)
STATE_ORDER = ["ABSORPTION", "PROPAGATION", "NORMALIZATION", "UNRESOLVED_STRESS", "NEUTRAL"]

RESEARCH_ONLY_GUARDRAIL = (
    "This detector is a research-only market/context label. It may identify useful transition-state regimes, "
    "but no output from this run should be promoted, registered, added to survivor/watchlist, or routed into "
    "portfolio/ML/blending/optimization logic from this detector alone. Useful findings should only motivate "
    "future conditional validation, attribution, or detector refinement."
)


def _ensure_dirs() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    NOTE_PATH.parent.mkdir(parents=True, exist_ok=True)


def _safe_div(numerator: pd.Series, denominator: pd.Series) -> pd.Series:
    return numerator / denominator.replace(0.0, np.nan)


def _rolling_rank(series: pd.Series, window: int = 252, min_periods: int = 100) -> pd.Series:
    def pct_rank(values: np.ndarray) -> float:
        valid = values[~np.isnan(values)]
        if valid.size == 0 or np.isnan(values[-1]):
            return np.nan
        return float((valid <= values[-1]).mean())

    return series.rolling(window, min_periods=min_periods).apply(pct_rank, raw=True)


def _clip01(series: pd.Series) -> pd.Series:
    return series.clip(lower=0.0, upper=1.0)


def _mean_score(items: list[pd.Series]) -> pd.Series:
    return pd.concat(items, axis=1).mean(axis=1, skipna=True)


def _forward_return(series: pd.Series, horizon: int) -> pd.Series:
    return series.shift(-horizon) / series - 1.0


def build_component_scores(panels: dict[str, pd.DataFrame], benchmark: pd.Series) -> tuple[pd.DataFrame, pd.DataFrame]:
    close = panels["close"]
    high = panels["high"]
    low = panels["low"]
    volume = panels["volume"].astype(float).where(panels["volume"].astype(float) > 0)

    ret1 = close.pct_change(1, fill_method=None)
    ret5 = close.pct_change(5, fill_method=None)
    ret10 = close.pct_change(10, fill_method=None)
    ret20 = close.pct_change(20, fill_method=None)
    bench_ret1 = benchmark.pct_change(1, fill_method=None)

    true_range = ((high - low) / close.shift(1)).replace([np.inf, -np.inf], np.nan)
    market_range5 = true_range.rolling(5, min_periods=4).mean().mean(axis=1)
    market_range20 = true_range.rolling(20, min_periods=12).mean().mean(axis=1)
    market_range60 = true_range.rolling(60, min_periods=40).mean().mean(axis=1)
    bench_vol5 = bench_ret1.rolling(5, min_periods=4).std()
    bench_vol20 = bench_ret1.rolling(20, min_periods=12).std()
    bench_vol60 = bench_ret1.rolling(60, min_periods=40).std()

    dollar_volume = close * volume
    market_liquidity = dollar_volume.sum(axis=1, min_count=25)
    liquidity5 = market_liquidity.rolling(5, min_periods=4).mean()
    liquidity20 = market_liquidity.rolling(20, min_periods=12).mean()
    liquidity60 = market_liquidity.rolling(60, min_periods=40).mean()

    breadth5 = (ret5 > 0).mean(axis=1)
    breadth20 = (ret20 > 0).mean(axis=1)
    dispersion10 = ret10.std(axis=1)
    dispersion20 = ret20.std(axis=1)
    dispersion60 = dispersion20.rolling(60, min_periods=40).mean()

    rank10 = ret10.rank(axis=1, pct=True)
    rank_churn10 = rank10.diff().abs().rolling(10, min_periods=6).mean().mean(axis=1)
    residual1 = ret1.sub(bench_ret1, axis=0)
    idio_vol5 = residual1.rolling(5, min_periods=4).std().mean(axis=1)
    idio_vol20 = residual1.rolling(20, min_periods=12).std().mean(axis=1)

    stress = build_stress_states(close, benchmark)
    stress_core = stress[
        ["drawdown_acceleration", "volatility_spike", "panic_liquidity_stress", "weak_breadth"]
    ].fillna(False)
    recent_stress = stress_core.any(axis=1).rolling(10, min_periods=1).max().astype(bool)
    stress_recent_20 = stress_core.any(axis=1).rolling(20, min_periods=1).max().astype(bool)

    volatility_shock_intensity = _mean_score(
        [
            _rolling_rank(_safe_div(bench_vol5, bench_vol60)),
            _rolling_rank(_safe_div(market_range5, market_range60)),
            stress["volatility_spike"].fillna(False).astype(float),
        ]
    )
    volatility_decay_absorption = _mean_score(
        [
            1.0 - _rolling_rank(_safe_div(bench_vol5, bench_vol20)),
            1.0 - _rolling_rank(_safe_div(market_range5, market_range20)),
            recent_stress.astype(float),
        ]
    )
    liquidity_recovery = _mean_score(
        [
            _rolling_rank(_safe_div(liquidity20, liquidity60)),
            _rolling_rank(liquidity20.pct_change(5, fill_method=None)),
            stress_recent_20.astype(float),
        ]
    )
    volume_shock_exhaustion = _mean_score(
        [
            _rolling_rank(_safe_div(liquidity20, liquidity60)),
            1.0 - _rolling_rank(_safe_div(liquidity5, liquidity20)),
            1.0 - _rolling_rank(_safe_div(market_range5, market_range20)),
        ]
    )
    dispersion_normalization = _mean_score(
        [
            _rolling_rank(_safe_div(dispersion20.rolling(20, min_periods=10).max(), dispersion60)),
            1.0 - _rolling_rank(dispersion20.diff(10)),
            1.0 - _rolling_rank(_safe_div(dispersion10, dispersion20)),
        ]
    )
    breadth_stabilization = _mean_score(
        [
            _rolling_rank(breadth5 - breadth20),
            _rolling_rank(breadth20.diff(10)),
            stress_recent_20.astype(float),
        ]
    )
    propagation_pressure = _mean_score(
        [
            _rolling_rank(_safe_div(bench_vol5, bench_vol20)),
            _rolling_rank(_safe_div(market_range5, market_range20)),
            _rolling_rank(dispersion20.diff(5)),
            1.0 - _rolling_rank(breadth20.diff(5)),
            _rolling_rank(rank_churn10),
        ]
    )
    instability_persistence_resolution = _mean_score(
        [
            1.0 - _rolling_rank(_safe_div(idio_vol5, idio_vol20)),
            1.0 - _rolling_rank(rank_churn10),
            volatility_decay_absorption,
            breadth_stabilization,
        ]
    )

    components = pd.DataFrame(
        {
            "volatility_shock_intensity": _clip01(volatility_shock_intensity),
            "volatility_decay_absorption": _clip01(volatility_decay_absorption),
            "liquidity_recovery": _clip01(liquidity_recovery),
            "volume_shock_exhaustion": _clip01(volume_shock_exhaustion),
            "dispersion_normalization": _clip01(dispersion_normalization),
            "breadth_stabilization": _clip01(breadth_stabilization),
            "propagation_pressure": _clip01(propagation_pressure),
            "instability_persistence_resolution": _clip01(instability_persistence_resolution),
        }
    )
    composite = pd.DataFrame(index=components.index)
    composite["absorption_score"] = _mean_score(
        [
            components["volatility_decay_absorption"],
            components["liquidity_recovery"],
            components["volume_shock_exhaustion"],
            components["breadth_stabilization"],
            components["instability_persistence_resolution"],
        ]
    )
    composite["normalization_score"] = _mean_score(
        [
            components["volatility_decay_absorption"],
            components["dispersion_normalization"],
            components["breadth_stabilization"],
            components["instability_persistence_resolution"],
        ]
    )
    composite["propagation_score"] = components["propagation_pressure"]
    composite["stress_score"] = _mean_score(
        [components["volatility_shock_intensity"], stress_core.any(axis=1).astype(float)]
    )
    component_panel = pd.concat([components, composite], axis=1)
    return component_panel, stress


def label_states(component_panel: pd.DataFrame) -> pd.DataFrame:
    labels = []
    for _, row in component_panel.iterrows():
        stress = row["stress_score"]
        absorption = row["absorption_score"]
        normalization = row["normalization_score"]
        propagation = row["propagation_score"]
        if pd.isna(stress) or pd.isna(absorption) or pd.isna(normalization) or pd.isna(propagation):
            label = "NEUTRAL"
        elif propagation >= 0.62 and stress >= 0.42:
            label = "PROPAGATION"
        elif absorption >= 0.60 and stress >= 0.35 and propagation < 0.62:
            label = "ABSORPTION"
        elif normalization >= 0.60 and propagation < 0.58 and stress < 0.60:
            label = "NORMALIZATION"
        elif stress >= 0.50:
            label = "UNRESOLVED_STRESS"
        else:
            label = "NEUTRAL"
        labels.append(label)
    out = component_panel.copy()
    out["state_label"] = labels
    out["is_research_only_context_label"] = True
    return out


def state_distribution(labels: pd.DataFrame) -> pd.DataFrame:
    counts = labels["state_label"].value_counts().reindex(STATE_ORDER, fill_value=0)
    return pd.DataFrame(
        {
            "state_label": counts.index,
            "date_count": counts.values,
            "date_ratio": counts.values / len(labels) if len(labels) else np.nan,
        }
    )


def transition_matrix(labels: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    previous = labels["state_label"].shift(1)
    current = labels["state_label"]
    counts = pd.crosstab(previous, current).reindex(index=STATE_ORDER, columns=STATE_ORDER, fill_value=0)
    row_sums = counts.sum(axis=1).replace(0, np.nan)
    rates = counts.div(row_sums, axis=0)
    return counts, rates


def forward_returns_by_state(labels: pd.DataFrame, close: pd.DataFrame, benchmark: pd.Series) -> pd.DataFrame:
    rows = []
    state = labels["state_label"]
    market_proxy = close.mean(axis=1)
    for horizon in HORIZONS:
        series = {
            "benchmark": _forward_return(benchmark, horizon),
            "equal_weight_universe": _forward_return(market_proxy, horizon),
        }
        for asset_scope, fwd in series.items():
            for state_label, values in fwd.groupby(state):
                valid = values.dropna()
                rows.append(
                    {
                        "asset_scope": asset_scope,
                        "state_label": state_label,
                        "horizon": horizon,
                        "mean_forward_return": float(valid.mean()) if not valid.empty else np.nan,
                        "median_forward_return": float(valid.median()) if not valid.empty else np.nan,
                        "positive_forward_return_rate": float((valid > 0).mean()) if not valid.empty else np.nan,
                        "n_dates": int(valid.shape[0]),
                    }
                )
    return pd.DataFrame(rows)


def stress_regime_attribution(labels: pd.DataFrame, stress: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for state_label in STATE_ORDER:
        state_mask = labels["state_label"].eq(state_label)
        state_dates = int(state_mask.sum())
        for stress_name, stress_mask in stress.fillna(False).astype(bool).items():
            overlap = state_mask & stress_mask
            stress_dates = int(stress_mask.sum())
            rows.append(
                {
                    "state_label": state_label,
                    "stress_regime": stress_name,
                    "state_dates": state_dates,
                    "stress_dates": stress_dates,
                    "overlap_dates": int(overlap.sum()),
                    "overlap_ratio_with_state": float(overlap.sum() / state_dates) if state_dates else np.nan,
                    "overlap_ratio_with_stress": float(overlap.sum() / stress_dates) if stress_dates else np.nan,
                }
            )
    return pd.DataFrame(rows)


def time_window_stability(labels: pd.DataFrame, component_panel: pd.DataFrame, n_windows: int = 4) -> pd.DataFrame:
    windows = pd.qcut(pd.Series(np.arange(len(labels)), index=labels.index), q=n_windows, labels=False, duplicates="drop")
    rows = []
    for window_id in sorted(windows.dropna().unique()):
        mask = windows.eq(window_id)
        window_labels = labels.loc[mask, "state_label"]
        row = {
            "window_id": int(window_id) + 1,
            "start_date": str(window_labels.index.min().date()),
            "end_date": str(window_labels.index.max().date()),
            "n_dates": int(mask.sum()),
        }
        for state_label in STATE_ORDER:
            row[f"{state_label.lower()}_ratio"] = float(window_labels.eq(state_label).mean())
        for score in ["absorption_score", "normalization_score", "propagation_score", "stress_score"]:
            row[f"mean_{score}"] = float(component_panel.loc[mask, score].mean())
        rows.append(row)
    return pd.DataFrame(rows)


def state_component_profile(labels: pd.DataFrame) -> pd.DataFrame:
    score_cols = [col for col in labels.columns if col.endswith("_score") or col in {
        "volatility_shock_intensity",
        "volatility_decay_absorption",
        "liquidity_recovery",
        "volume_shock_exhaustion",
        "dispersion_normalization",
        "breadth_stabilization",
        "propagation_pressure",
        "instability_persistence_resolution",
    }]
    return labels.groupby("state_label")[score_cols].mean().reindex(STATE_ORDER).reset_index()


def sample_size_sanity(labels: pd.DataFrame, close: pd.DataFrame) -> pd.DataFrame:
    rows = []
    available_assets = close.notna().sum(axis=1)
    for state_label in STATE_ORDER:
        mask = labels["state_label"].eq(state_label)
        rows.append(
            {
                "state_label": state_label,
                "date_count": int(mask.sum()),
                "date_ratio": float(mask.mean()),
                "mean_available_assets": float(available_assets.loc[mask].mean()) if mask.any() else np.nan,
                "min_available_assets": int(available_assets.loc[mask].min()) if mask.any() else 0,
            }
        )
    return pd.DataFrame(rows)


def inventory_panels(index: pd.Index, columns: pd.Index) -> dict[str, pd.DataFrame]:
    paths = {
        "inventory_participation_liquidity_state_shift_20_60": LIQUIDITY_INVENTORY_PATH,
        "inventory_participation_breadth_repair_under_hostile_trend": BREADTH_INVENTORY_PATH,
        "inventory_volatility_compression_after_stress_stabilization": VOLATILITY_INVENTORY_PATH,
        "research_short_horizon_volatility_shock_absorption_10_refinement": Path(
            "artifacts/research/short_horizon_volatility_shock_absorption_10_refinement/"
            "rebalance_5_zero_signal_panel.parquet"
        ),
    }
    refs = {}
    for name, path in paths.items():
        if path.exists():
            refs[name] = pd.read_parquet(path).reindex(index=index, columns=columns)
    return refs


def alpha_context_attribution(labels: pd.DataFrame, close: pd.DataFrame) -> pd.DataFrame:
    refs = inventory_panels(close.index, close.columns)
    rows = []
    for signal_name, panel in refs.items():
        active = panel.notna().sum(axis=1) >= 25
        for horizon in HORIZONS:
            ic = daily_ic(panel, forward_returns(close, horizon))
            for state_label in STATE_ORDER:
                mask = labels["state_label"].eq(state_label)
                valid = ic.loc[mask].dropna()
                rows.append(
                    {
                        "signal_name": signal_name,
                        "state_label": state_label,
                        "horizon": horizon,
                        "mean_ic": float(valid.mean()) if not valid.empty else np.nan,
                        "positive_ic_rate": float((valid > 0).mean()) if not valid.empty else np.nan,
                        "n_ic_dates": int(valid.shape[0]),
                        "active_overlap_dates": int((mask & active).sum()),
                    }
                )
    return pd.DataFrame(rows)


def write_note(
    labels: pd.DataFrame,
    distribution: pd.DataFrame,
    forward_summary: pd.DataFrame,
    context_attr: pd.DataFrame,
    stability: pd.DataFrame,
) -> None:
    state_counts = distribution.to_markdown(index=False, floatfmt=".4f")
    fwd = forward_summary[
        (forward_summary["asset_scope"].eq("benchmark")) & (forward_summary["horizon"].isin([5, 10, 20]))
    ].copy()
    fwd_table = fwd.to_markdown(index=False, floatfmt=".6f") if not fwd.empty else "No forward return summary available."
    context = context_attr[context_attr["horizon"].isin([5, 10, 20])].copy()
    if not context.empty:
        context = context.sort_values(["signal_name", "horizon", "state_label"])
        context_table = context.head(40).to_markdown(index=False, floatfmt=".6f")
    else:
        context_table = "No reusable inventory/context alpha panels were available."
    stability_table = stability.to_markdown(index=False, floatfmt=".4f") if not stability.empty else "No stability table available."

    note = f"""# Transition-State Composite Detector v1

Date: 2026-05-21

Run id: `{RUN_ID}`

Status: RESEARCH_ONLY_CONTEXT_DETECTOR

## Research-Only Guardrail

{RESEARCH_ONLY_GUARDRAIL}

This run does not claim alpha discovery. It creates a date-level context layer for future conditional diagnostics.

## Objective

The standalone Transition-State Alpha Discovery Batch rejected all 10 simple transition-state alpha structures. This detector pivots the same ingredients away from tradable signal construction and toward market-state inference:

- volatility shock intensity
- volatility decay / absorption
- liquidity recovery
- volume shock exhaustion
- dispersion normalization
- breadth stabilization
- propagation pressure
- instability persistence / resolution

## Label Semantics

- `ABSORPTION`: recent stress or volatility shock with improving absorption, liquidity, breadth, and instability-resolution scores.
- `PROPAGATION`: stress with elevated propagation pressure, range/volatility pressure, dispersion pressure, or rank churn.
- `NORMALIZATION`: post-stress normalization where dispersion, breadth, and volatility decay improve without high propagation pressure.
- `UNRESOLVED_STRESS`: stress remains elevated without enough absorption or normalization evidence.
- `NEUTRAL`: no strong transition-state condition.

## State Distribution

{state_counts}

## Benchmark Forward Returns By State

{fwd_table}

## Existing Alpha Context Attribution

This attribution is diagnostic only. It asks whether existing inventory/research panels behave differently inside detector labels; it does not promote or route the detector.

{context_table}

## Time-Window Stability

{stability_table}

## Interpretation

The detector should be read as a context map, not an alpha. A useful result would be stable, interpretable state labels with differentiated forward-return and alpha-attribution profiles. A weak result would be unstable labels, tiny state samples, or context slices that do not distinguish absorption from propagation.

## Recommendation

Keep `transition_state_composite_detector_v1` as a research artifact only. The appropriate next step is a future conditional attribution pass that tests whether existing inventory candidates and future repair/stabilization candidates behave differently under these labels. Do not promote, register, blend, optimize, or validate this detector as a signal from this run alone.

## Artifacts

- `component_scores.csv`
- `composite_state_labels.csv`
- `state_distribution.csv`
- `state_transition_counts.csv`
- `state_transition_matrix.csv`
- `state_component_profile.csv`
- `forward_returns_by_state.csv`
- `alpha_context_attribution.csv`
- `stress_regime_attribution.csv`
- `sample_size_sanity.csv`
- `time_window_stability.csv`
- `manifest.json`
"""
    NOTE_PATH.write_text(note)


def write_manifest(artifacts: list[str], labels: pd.DataFrame, context_attr: pd.DataFrame) -> None:
    manifest = {
        "run_id": RUN_ID,
        "status": "RESEARCH_ONLY_CONTEXT_DETECTOR",
        "research_only_guardrail": RESEARCH_ONLY_GUARDRAIL,
        "state_labels": STATE_ORDER,
        "date_count": int(labels.shape[0]),
        "start_date": str(labels.index.min().date()),
        "end_date": str(labels.index.max().date()),
        "inventory_context_panels_available": sorted(context_attr["signal_name"].unique().tolist())
        if not context_attr.empty
        else [],
        "artifacts": artifacts,
        "intentional_non_changes": {
            "production_registration_changed": False,
            "survivor_watchlist_changed": False,
            "portfolio_or_ml_route_changed": False,
            "blending_or_optimization_changed": False,
            "gates_schemas_thresholds_validation_changed": False,
            "governance_rules_changed": False,
            "alpha_discovery_claimed": False,
        },
    }
    (OUT_DIR / "manifest.json").write_text(json.dumps(manifest, indent=2))


def main() -> None:
    _ensure_dirs()
    panels, benchmark = load_inputs()
    close = panels["close"]

    component_panel, stress = build_component_scores(panels, benchmark)
    labels = label_states(component_panel)
    distribution = state_distribution(labels)
    transition_counts, transition_rates = transition_matrix(labels)
    fwd = forward_returns_by_state(labels, close, benchmark)
    stress_attr = stress_regime_attribution(labels, stress)
    samples = sample_size_sanity(labels, close)
    stability = time_window_stability(labels, component_panel)
    profile = state_component_profile(labels)
    context_attr = alpha_context_attribution(labels, close)

    artifacts = [
        "component_scores.csv",
        "composite_state_labels.csv",
        "state_distribution.csv",
        "state_transition_counts.csv",
        "state_transition_matrix.csv",
        "state_component_profile.csv",
        "forward_returns_by_state.csv",
        "alpha_context_attribution.csv",
        "stress_regime_attribution.csv",
        "sample_size_sanity.csv",
        "time_window_stability.csv",
        "manifest.json",
    ]

    component_panel.to_csv(OUT_DIR / "component_scores.csv", index_label="Date")
    labels.to_csv(OUT_DIR / "composite_state_labels.csv", index_label="Date")
    distribution.to_csv(OUT_DIR / "state_distribution.csv", index=False)
    transition_counts.to_csv(OUT_DIR / "state_transition_counts.csv")
    transition_rates.to_csv(OUT_DIR / "state_transition_matrix.csv")
    profile.to_csv(OUT_DIR / "state_component_profile.csv", index=False)
    fwd.to_csv(OUT_DIR / "forward_returns_by_state.csv", index=False)
    context_attr.to_csv(OUT_DIR / "alpha_context_attribution.csv", index=False)
    stress_attr.to_csv(OUT_DIR / "stress_regime_attribution.csv", index=False)
    samples.to_csv(OUT_DIR / "sample_size_sanity.csv", index=False)
    stability.to_csv(OUT_DIR / "time_window_stability.csv", index=False)
    write_manifest(artifacts, labels, context_attr)
    write_note(labels, distribution, fwd, context_attr, stability)

    print(f"Wrote {RUN_ID} artifacts to {OUT_DIR}")
    print(f"Wrote research note to {NOTE_PATH}")
    print(RESEARCH_ONLY_GUARDRAIL)


if __name__ == "__main__":
    main()
