from __future__ import annotations

import re

import numpy as np
import pandas as pd

from src.db import load_table
from src.forward_returns import make_forward_returns


APPROVED_STRESS = "APPROVED_STRESS"
WATCHLIST_STRESS = "WATCHLIST_STRESS"
REJECTED_STRESS = "REJECTED_STRESS"

ALPHA_STRESS_RESULT_COLUMNS = [
    "alpha_name",
    "horizon",
    "stress_type",
    "stress_case",
    "effective_mean_ic",
    "effective_ic_ir",
    "degradation_from_base",
    "pass_flag",
    "avg_turnover_proxy",
    "turnover_risk_flag",
    "notes",
]

ALPHA_STRESS_SUMMARY_COLUMNS = [
    "alpha_name",
    "horizon",
    "n_stress_cases",
    "n_passed",
    "pass_rate",
    "worst_degradation",
    "catastrophic_degradation",
    "cost_sensitivity_extreme",
    "small_delay_failure",
    "fragile_subset_warning",
    "avg_turnover_proxy",
    "turnover_risk_flag",
    "high_turnover_weak_cost_robustness",
    "failure_notes",
]

ALPHA_STRESS_AUDIT_SUMMARY_COLUMNS = [
    "alpha_name",
    "horizon",
    "n_stress_cases",
    "n_passed",
    "pass_rate",
    "worst_degradation",
    "worst_stress_type",
    "worst_stress_case",
    "catastrophic_degradation",
    "cost_sensitivity_extreme",
    "small_delay_failure",
    "fragile_subset_warning",
    "avg_turnover_proxy",
    "turnover_risk_flag",
    "high_turnover_weak_cost_robustness",
    "survivor_tier",
    "status",
    "stress_gate_notes",
    "promotion_decision",
    "alpha_role",
    "failure_category",
    "interpretation_notes",
]


def load_approved_alpha_winners() -> pd.DataFrame:
    """Load approved alpha WFV winners from Notebook 6 output."""
    return load_table("alpha_wfv_winner_summary_current")


def load_constructed_alpha_stress_inputs() -> dict[str, pd.DataFrame]:
    """Load constructed-alpha stress inputs from Notebook 04A and constructed-alpha WFV."""
    return {
        "alpha_long": load_table("alpha_constructed_candidates_current"),
        "quality": load_table("alpha_construction_quality_current"),
        "diagnostics": load_table("alpha_construction_diagnostics_current"),
        "wfv_gate": load_table("constructed_alpha_wfv_gate_current"),
        "wfv_winner_summary": load_table("constructed_alpha_wfv_winner_summary_current"),
        "regime_overlay_decision": load_table("regime_overlay_diagnostic_decision_current"),
    }


def select_constructed_alpha_stress_candidates(
    alpha_quality: pd.DataFrame,
    alpha_diagnostics: pd.DataFrame,
    constructed_alpha_wfv_gate: pd.DataFrame,
    constructed_alpha_wfv_winner_summary: pd.DataFrame | None = None,
    priority_alphas: list[str] | tuple[str, ...] | None = None,
) -> pd.DataFrame:
    """Select constructed alpha candidates approved by construction and supported by WFV diagnostics."""
    approved_quality = alpha_quality.loc[
        alpha_quality["status"].eq("APPROVED_FOR_ALPHA_VALIDATION")
    ].copy()
    valid_wfv_statuses = {
        "WATCHLIST_CONSTRUCTED_ALPHA_WFV",
        "APPROVED_CONSTRUCTED_ALPHA_WFV",
    }
    valid_wfv = constructed_alpha_wfv_gate.loc[
        constructed_alpha_wfv_gate["status"].isin(valid_wfv_statuses)
    ].copy()
    if valid_wfv.empty:
        return pd.DataFrame(
            columns=[
                "alpha_name",
                "horizon",
                "status",
                "construction_status",
                "wfv_status",
                "avg_turnover_proxy",
                "turnover_risk_flag",
                "selection_priority",
            ]
        )

    wfv_source = valid_wfv
    if constructed_alpha_wfv_winner_summary is not None and not constructed_alpha_wfv_winner_summary.empty:
        winner_names = set(valid_wfv["alpha_name"].dropna().astype(str))
        winner_rows = constructed_alpha_wfv_winner_summary.loc[
            constructed_alpha_wfv_winner_summary["alpha_name"].astype(str).isin(winner_names)
        ].copy()
        if not winner_rows.empty and "status" in winner_rows.columns:
            winner_rows = winner_rows.loc[winner_rows["status"].isin(valid_wfv_statuses)].copy()
        if not winner_rows.empty:
            wfv_source = winner_rows

    wfv_source["effective_mean_test_ic"] = pd.to_numeric(
        wfv_source["effective_mean_test_ic"],
        errors="coerce",
    )
    best_idx = wfv_source.groupby("alpha_name")["effective_mean_test_ic"].idxmax()
    best_wfv = wfv_source.loc[best_idx].copy()
    candidates = approved_quality[["alpha_name", "status"]].rename(
        columns={"status": "construction_status"}
    ).merge(
        best_wfv.rename(columns={"status": "wfv_status"}),
        on="alpha_name",
        how="inner",
    )
    diagnostic_columns = [
        column
        for column in ["alpha_name", "avg_turnover_proxy", "turnover_risk_flag"]
        if column in alpha_diagnostics.columns
    ]
    if diagnostic_columns:
        candidates = candidates.merge(
            alpha_diagnostics[diagnostic_columns].drop_duplicates("alpha_name"),
            on="alpha_name",
            how="left",
        )
    if "turnover_risk_flag" not in candidates.columns:
        candidates["turnover_risk_flag"] = np.where(
            pd.to_numeric(candidates.get("avg_turnover_proxy"), errors="coerce") >= 2.50,
            "HIGH_TURNOVER_RISK",
            np.where(
                pd.to_numeric(candidates.get("avg_turnover_proxy"), errors="coerce") >= 1.75,
                "MODERATE_TURNOVER_RISK",
                "LOW_TURNOVER_RISK",
            ),
        )

    priority = list(priority_alphas or [])
    priority_rank = {alpha_name: rank for rank, alpha_name in enumerate(priority)}
    candidates["selection_priority"] = candidates["alpha_name"].map(priority_rank).fillna(len(priority)).astype(int)
    return candidates.sort_values(
        ["selection_priority", "effective_mean_test_ic", "alpha_name"],
        ascending=[True, False, True],
    ).reset_index(drop=True)


def build_alpha_panel(alpha_long_df: pd.DataFrame, alpha_name: str) -> pd.DataFrame:
    """Pivot long alpha observations to a Date x ticker panel."""
    required_columns = {"Date", "ticker", "alpha_name", "alpha_value"}
    missing_columns = required_columns.difference(alpha_long_df.columns)
    if missing_columns:
        raise ValueError(f"alpha_long_df is missing required columns: {sorted(missing_columns)}")

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


def _safe_corr(df: pd.DataFrame) -> float:
    if len(df) < 2:
        return np.nan
    if df["alpha"].nunique(dropna=True) < 2 or df["fwd_return"].nunique(dropna=True) < 2:
        return np.nan
    return float(df["alpha"].corr(df["fwd_return"], method="spearman"))


def _score_alpha_panel(
    alpha_panel: pd.DataFrame,
    close_prices: pd.DataFrame,
    horizon: int,
) -> dict[str, object]:
    if alpha_panel.empty or close_prices.empty:
        return {"mean_ic": np.nan, "effective_mean_ic": np.nan, "effective_ic_ir": np.nan, "n_obs": 0}

    forward_returns = make_forward_returns(close_prices, [int(horizon)])[int(horizon)]
    alpha, fwd = _align_panels(alpha_panel, forward_returns)
    paired = pd.concat(
        [
            alpha.stack(future_stack=True).rename("alpha"),
            fwd.stack(future_stack=True).rename("fwd_return"),
        ],
        axis=1,
    ).dropna()

    if paired.empty:
        return {"mean_ic": np.nan, "effective_mean_ic": np.nan, "effective_ic_ir": np.nan, "n_obs": 0}

    ic_by_date = paired.groupby(level=0, sort=True).apply(_safe_corr).dropna()
    if ic_by_date.empty:
        return {
            "mean_ic": np.nan,
            "effective_mean_ic": np.nan,
            "effective_ic_ir": np.nan,
            "n_obs": int(len(paired)),
        }

    mean_ic = float(ic_by_date.mean())
    ic_std = float(ic_by_date.std(ddof=1)) if len(ic_by_date) > 1 else np.nan
    ic_ir = float(mean_ic / ic_std) if ic_std and not pd.isna(ic_std) else np.nan
    return {
        "mean_ic": mean_ic,
        "effective_mean_ic": abs(mean_ic),
        "effective_ic_ir": abs(ic_ir) if not pd.isna(ic_ir) else np.nan,
        "n_obs": int(len(paired)),
    }


def _base_score(alpha_panel: pd.DataFrame, close_prices: pd.DataFrame, horizon: int) -> dict[str, object]:
    return _score_alpha_panel(alpha_panel, close_prices, horizon)


def _degradation(base_effective_ic: float, stressed_effective_ic: float) -> float:
    if pd.isna(base_effective_ic) or float(base_effective_ic) == 0 or pd.isna(stressed_effective_ic):
        return np.nan
    return float((base_effective_ic - stressed_effective_ic) / abs(base_effective_ic))


def _alpha_name(alpha_panel: pd.DataFrame) -> str | None:
    return alpha_panel.attrs.get("alpha_name")


def _result_row(
    alpha_panel: pd.DataFrame,
    horizon: int,
    stress_type: str,
    stress_case: str,
    effective_mean_ic: float,
    effective_ic_ir: float,
    degradation_from_base: float,
    pass_flag: bool,
    notes: str,
    avg_turnover_proxy: float = np.nan,
    turnover_risk_flag: object = np.nan,
) -> dict[str, object]:
    return {
        "alpha_name": _alpha_name(alpha_panel),
        "horizon": int(horizon),
        "stress_type": stress_type,
        "stress_case": stress_case,
        "effective_mean_ic": effective_mean_ic,
        "effective_ic_ir": effective_ic_ir,
        "degradation_from_base": degradation_from_base,
        "pass_flag": bool(pass_flag),
        "avg_turnover_proxy": avg_turnover_proxy,
        "turnover_risk_flag": turnover_risk_flag,
        "notes": notes,
    }


def _turnover_proxy(alpha_panel: pd.DataFrame) -> float:
    attr_turnover = alpha_panel.attrs.get("avg_turnover_proxy")
    if attr_turnover is not None and not pd.isna(attr_turnover):
        return float(attr_turnover)
    ranks = alpha_panel.rank(axis=1, pct=True)
    turnover_by_date = ranks.diff().abs().mean(axis=1, skipna=True)
    turnover = turnover_by_date.dropna()
    return float(turnover.mean()) if not turnover.empty else np.nan


def _turnover_risk_flag(avg_turnover_proxy: float) -> str | float:
    if pd.isna(avg_turnover_proxy):
        return np.nan
    if avg_turnover_proxy < 1.75:
        return "LOW_TURNOVER_RISK"
    if avg_turnover_proxy < 2.50:
        return "MODERATE_TURNOVER_RISK"
    return "HIGH_TURNOVER_RISK"


def _panel_turnover_context(alpha_panel: pd.DataFrame) -> tuple[float, object]:
    avg_turnover_proxy = _turnover_proxy(alpha_panel)
    attr_flag = alpha_panel.attrs.get("turnover_risk_flag")
    turnover_risk_flag = attr_flag if attr_flag is not None and not pd.isna(attr_flag) else _turnover_risk_flag(avg_turnover_proxy)
    return avg_turnover_proxy, turnover_risk_flag


def stress_alpha_costs(
    alpha_panel: pd.DataFrame,
    close_prices: pd.DataFrame,
    horizon: int,
    cost_bps_list: list[int] | tuple[int, ...] = (0, 5, 10, 25),
) -> pd.DataFrame:
    """Estimate cost sensitivity using turnover-adjusted effective IC proxy."""
    base = _base_score(alpha_panel, close_prices, horizon)
    base_ic = base["effective_mean_ic"]
    turnover, turnover_risk_flag = _panel_turnover_context(alpha_panel)
    rows: list[dict[str, object]] = []

    for cost_bps in cost_bps_list:
        cost_drag = 0.0 if pd.isna(turnover) else float(turnover * (float(cost_bps) / 10000.0))
        stressed_ic = base_ic - cost_drag if not pd.isna(base_ic) else np.nan
        degradation = _degradation(base_ic, stressed_ic)
        pass_flag = (
            not pd.isna(stressed_ic)
            and stressed_ic >= 0.008
            and (pd.isna(degradation) or degradation <= (0.50 if cost_bps <= 10 else 0.80))
        )
        rows.append(
            _result_row(
                alpha_panel=alpha_panel,
                horizon=horizon,
                stress_type="cost",
                stress_case=f"{int(cost_bps)}bps",
                effective_mean_ic=stressed_ic,
                effective_ic_ir=base["effective_ic_ir"],
                degradation_from_base=degradation,
                pass_flag=pass_flag,
                avg_turnover_proxy=turnover,
                turnover_risk_flag=turnover_risk_flag,
                notes=f"turnover_proxy={turnover:.4f}" if not pd.isna(turnover) else "turnover proxy unavailable",
            )
        )

    return pd.DataFrame(rows, columns=ALPHA_STRESS_RESULT_COLUMNS)


def stress_alpha_execution_delay(
    alpha_panel: pd.DataFrame,
    close_prices: pd.DataFrame,
    horizon: int,
    delays: list[int] | tuple[int, ...] = (0, 1, 2, 5),
) -> pd.DataFrame:
    """Rescore alpha after delaying signal availability by whole trading days."""
    base = _base_score(alpha_panel, close_prices, horizon)
    base_ic = base["effective_mean_ic"]
    avg_turnover_proxy, turnover_risk_flag = _panel_turnover_context(alpha_panel)
    rows: list[dict[str, object]] = []

    for delay in delays:
        delayed_alpha = alpha_panel.shift(int(delay))
        delayed_alpha.attrs["alpha_name"] = _alpha_name(alpha_panel)
        score = _score_alpha_panel(delayed_alpha, close_prices, horizon)
        degradation = _degradation(base_ic, score["effective_mean_ic"])
        if int(delay) == 0:
            pass_flag = not pd.isna(score["effective_mean_ic"]) and score["effective_mean_ic"] >= 0.015
        else:
            pass_flag = (
                not pd.isna(score["effective_mean_ic"])
                and score["effective_mean_ic"] >= 0.008
                and (pd.isna(degradation) or degradation <= (0.60 if int(delay) <= 2 else 0.90))
            )
        rows.append(
            _result_row(
                alpha_panel=alpha_panel,
                horizon=horizon,
                stress_type="execution_delay",
                stress_case=f"{int(delay)}d_delay",
                effective_mean_ic=score["effective_mean_ic"],
                effective_ic_ir=score["effective_ic_ir"],
                degradation_from_base=degradation,
                pass_flag=pass_flag,
                avg_turnover_proxy=avg_turnover_proxy,
                turnover_risk_flag=turnover_risk_flag,
                notes=f"n_obs={score['n_obs']}",
            )
        )

    return pd.DataFrame(rows, columns=ALPHA_STRESS_RESULT_COLUMNS)


def stress_alpha_universe_subsamples(
    alpha_panel: pd.DataFrame,
    close_prices: pd.DataFrame,
    horizon: int,
) -> pd.DataFrame:
    """Test alpha robustness across deterministic ticker subsets."""
    tickers = list(alpha_panel.columns)
    midpoint = max(1, len(tickers) // 2)
    rng_42 = np.random.default_rng(42)
    rng_99 = np.random.default_rng(99)
    half_size = max(1, len(tickers) // 2)
    subsets = {
        "first_half_tickers": tickers[:midpoint],
        "second_half_tickers": tickers[midpoint:] or tickers[:midpoint],
        "random_half_seed_42": sorted(rng_42.choice(tickers, size=half_size, replace=False).tolist()),
        "random_half_seed_99": sorted(rng_99.choice(tickers, size=half_size, replace=False).tolist()),
    }

    base = _base_score(alpha_panel, close_prices, horizon)
    base_ic = base["effective_mean_ic"]
    avg_turnover_proxy, turnover_risk_flag = _panel_turnover_context(alpha_panel)
    rows: list[dict[str, object]] = []

    for stress_case, subset in subsets.items():
        subset_alpha = alpha_panel.reindex(columns=subset)
        subset_alpha.attrs["alpha_name"] = _alpha_name(alpha_panel)
        subset_close = close_prices.reindex(columns=subset)
        score = _score_alpha_panel(subset_alpha, subset_close, horizon)
        degradation = _degradation(base_ic, score["effective_mean_ic"])
        pass_flag = (
            not pd.isna(score["effective_mean_ic"])
            and score["effective_mean_ic"] >= 0.008
            and (pd.isna(degradation) or degradation <= 0.75)
        )
        rows.append(
            _result_row(
                alpha_panel=alpha_panel,
                horizon=horizon,
                stress_type="universe_subsample",
                stress_case=stress_case,
                effective_mean_ic=score["effective_mean_ic"],
                effective_ic_ir=score["effective_ic_ir"],
                degradation_from_base=degradation,
                pass_flag=pass_flag,
                avg_turnover_proxy=avg_turnover_proxy,
                turnover_risk_flag=turnover_risk_flag,
                notes=f"n_tickers={len(subset)}; n_obs={score['n_obs']}",
            )
        )

    return pd.DataFrame(rows, columns=ALPHA_STRESS_RESULT_COLUMNS)


def _infer_regime_filter(alpha_name: str | None) -> tuple[str | None, set[str]]:
    if alpha_name is None:
        return None, set()
    suffix_map = {
        "high_vol": ("benchmark_vol_regime", {"HIGH_VOL"}),
        "low_vol": ("benchmark_vol_regime", {"LOW_VOL"}),
        "uptrend": ("benchmark_trend_regime", {"UPTREND"}),
        "downtrend": ("benchmark_trend_regime", {"DOWNTREND"}),
        "high_drawdown": ("drawdown_regime", {"HIGH_DRAWDOWN"}),
    }
    for suffix, regime_filter in suffix_map.items():
        if re.search(fr"_{suffix}$", alpha_name):
            return regime_filter
    return None, set()


def _regime_features_indexed(regime_features: pd.DataFrame) -> pd.DataFrame:
    features = regime_features.copy()
    if "Date" in features.columns:
        features["Date"] = pd.to_datetime(features["Date"], errors="coerce")
        features = features.set_index("Date")
    else:
        features.index = pd.to_datetime(features.index, errors="coerce")
    return features.sort_index()


def stress_alpha_regime_holdout(
    alpha_panel: pd.DataFrame,
    close_prices: pd.DataFrame,
    regime_features: pd.DataFrame,
    horizon: int,
) -> pd.DataFrame:
    """Check intended-regime behavior and document outside-regime exposure."""
    alpha_name = _alpha_name(alpha_panel)
    regime_column, allowed_regimes = _infer_regime_filter(alpha_name)
    if regime_column is None:
        score = _score_alpha_panel(alpha_panel, close_prices, horizon)
        return pd.DataFrame(
            [
                _result_row(
                    alpha_panel=alpha_panel,
                    horizon=horizon,
                    stress_type="regime_holdout",
                    stress_case="no_inferred_regime",
                    effective_mean_ic=score["effective_mean_ic"],
                    effective_ic_ir=score["effective_ic_ir"],
                    degradation_from_base=0.0,
                    pass_flag=not pd.isna(score["effective_mean_ic"]) and score["effective_mean_ic"] >= 0.008,
                    notes="could not infer intended regime from alpha name",
                )
            ],
            columns=ALPHA_STRESS_RESULT_COLUMNS,
        )

    features = _regime_features_indexed(regime_features)
    if regime_column not in features.columns:
        return pd.DataFrame(
            [
                _result_row(
                    alpha_panel=alpha_panel,
                    horizon=horizon,
                    stress_type="regime_holdout",
                    stress_case="missing_regime_feature",
                    effective_mean_ic=np.nan,
                    effective_ic_ir=np.nan,
                    degradation_from_base=np.nan,
                    pass_flag=False,
                    notes=f"missing regime feature: {regime_column}",
                )
            ],
            columns=ALPHA_STRESS_RESULT_COLUMNS,
        )

    aligned_regime = features.reindex(alpha_panel.index)
    intended_dates = aligned_regime[regime_column].isin(allowed_regimes)
    outside_dates = intended_dates.eq(False)
    base = _base_score(alpha_panel, close_prices, horizon)
    base_ic = base["effective_mean_ic"]

    intended_alpha = alpha_panel.loc[intended_dates.fillna(False)]
    intended_alpha.attrs["alpha_name"] = alpha_name
    intended_close = close_prices.reindex(index=intended_alpha.index)
    intended_score = _score_alpha_panel(intended_alpha, intended_close, horizon)
    intended_degradation = _degradation(base_ic, intended_score["effective_mean_ic"])

    outside_alpha = alpha_panel.loc[outside_dates.fillna(False)]
    outside_alpha.attrs["alpha_name"] = alpha_name
    outside_close = close_prices.reindex(index=outside_alpha.index)
    outside_score = _score_alpha_panel(outside_alpha, outside_close, horizon)
    outside_has_exposure = int(outside_alpha.notna().sum().sum()) > 0

    rows = [
        _result_row(
            alpha_panel=alpha_panel,
            horizon=horizon,
            stress_type="regime_holdout",
            stress_case="intended_regime_only",
            effective_mean_ic=intended_score["effective_mean_ic"],
            effective_ic_ir=intended_score["effective_ic_ir"],
            degradation_from_base=intended_degradation,
            pass_flag=not pd.isna(intended_score["effective_mean_ic"]) and intended_score["effective_mean_ic"] >= 0.008,
            notes=f"{regime_column} in {sorted(allowed_regimes)}; n_obs={intended_score['n_obs']}",
        )
    ]

    if outside_has_exposure:
        outside_degradation = _degradation(base_ic, outside_score["effective_mean_ic"])
        outside_pass = not pd.isna(outside_score["effective_mean_ic"]) and outside_score["effective_mean_ic"] >= 0.0
        outside_notes = f"outside intended regime exposure found; n_obs={outside_score['n_obs']}"
    else:
        outside_degradation = np.nan
        outside_pass = True
        outside_notes = "regime-specific alpha has no outside-regime exposure; outside holdout not scoreable"

    rows.append(
        _result_row(
            alpha_panel=alpha_panel,
            horizon=horizon,
            stress_type="regime_holdout",
            stress_case="outside_intended_regime",
            effective_mean_ic=outside_score["effective_mean_ic"],
            effective_ic_ir=outside_score["effective_ic_ir"],
            degradation_from_base=outside_degradation,
            pass_flag=outside_pass,
            notes=outside_notes,
        )
    )

    return pd.DataFrame(rows, columns=ALPHA_STRESS_RESULT_COLUMNS)


def stress_alpha_turnover(
    alpha_panel: pd.DataFrame,
    close_prices: pd.DataFrame,
    horizon: int,
) -> pd.DataFrame:
    """Flag turnover risk using the alpha construction diagnostics turnover proxy."""
    score = _base_score(alpha_panel, close_prices, horizon)
    avg_turnover_proxy, turnover_risk_flag = _panel_turnover_context(alpha_panel)
    pass_flag = turnover_risk_flag != "HIGH_TURNOVER_RISK"
    return pd.DataFrame(
        [
            _result_row(
                alpha_panel=alpha_panel,
                horizon=horizon,
                stress_type="turnover",
                stress_case=str(turnover_risk_flag) if not pd.isna(turnover_risk_flag) else "UNKNOWN_TURNOVER_RISK",
                effective_mean_ic=score["effective_mean_ic"],
                effective_ic_ir=score["effective_ic_ir"],
                degradation_from_base=0.0,
                pass_flag=pass_flag,
                avg_turnover_proxy=avg_turnover_proxy,
                turnover_risk_flag=turnover_risk_flag,
                notes=f"avg_turnover_proxy={avg_turnover_proxy:.4f}"
                if not pd.isna(avg_turnover_proxy)
                else "turnover proxy unavailable",
            )
        ],
        columns=ALPHA_STRESS_RESULT_COLUMNS,
    )


def _subperiods_from_dates(dates: pd.Index) -> dict[str, tuple[pd.Timestamp, pd.Timestamp]]:
    date_index = pd.DatetimeIndex(pd.to_datetime(dates, errors="coerce")).dropna().drop_duplicates().sort_values()
    if date_index.empty:
        return {}
    split_1 = int(len(date_index) / 3)
    split_2 = int(2 * len(date_index) / 3)
    periods = {
        "early": date_index[: max(split_1, 1)],
        "middle": date_index[max(split_1, 1) : max(split_2, max(split_1, 1) + 1)],
        "recent": date_index[max(split_2, max(split_1, 1) + 1) :],
    }
    return {
        name: (period.min(), period.max())
        for name, period in periods.items()
        if len(period) > 0
    }


def stress_alpha_subperiods(
    alpha_panel: pd.DataFrame,
    close_prices: pd.DataFrame,
    horizon: int,
) -> pd.DataFrame:
    """Test alpha robustness across early, middle, and recent date subperiods."""
    base = _base_score(alpha_panel, close_prices, horizon)
    base_ic = base["effective_mean_ic"]
    avg_turnover_proxy, turnover_risk_flag = _panel_turnover_context(alpha_panel)
    rows: list[dict[str, object]] = []

    for stress_case, (start_date, end_date) in _subperiods_from_dates(alpha_panel.index).items():
        sub_alpha = alpha_panel.loc[start_date:end_date]
        sub_alpha.attrs.update(alpha_panel.attrs)
        sub_close = close_prices.loc[start_date:end_date]
        score = _score_alpha_panel(sub_alpha, sub_close, horizon)
        degradation = _degradation(base_ic, score["effective_mean_ic"])
        pass_flag = (
            not pd.isna(score["effective_mean_ic"])
            and score["effective_mean_ic"] >= 0.008
            and (pd.isna(degradation) or degradation <= 0.75)
        )
        rows.append(
            _result_row(
                alpha_panel=alpha_panel,
                horizon=horizon,
                stress_type="subperiod",
                stress_case=stress_case,
                effective_mean_ic=score["effective_mean_ic"],
                effective_ic_ir=score["effective_ic_ir"],
                degradation_from_base=degradation,
                pass_flag=pass_flag,
                avg_turnover_proxy=avg_turnover_proxy,
                turnover_risk_flag=turnover_risk_flag,
                notes=f"{start_date.date()} to {end_date.date()}; n_obs={score['n_obs']}",
            )
        )

    return pd.DataFrame(rows, columns=ALPHA_STRESS_RESULT_COLUMNS)


def stress_alpha_degradation(
    alpha_panel: pd.DataFrame,
    close_prices: pd.DataFrame,
    horizon: int,
    multipliers: list[float] | tuple[float, ...] = (0.75, 0.50),
) -> pd.DataFrame:
    """Rescore alpha after multiplying alpha values by fixed degradation factors."""
    base = _base_score(alpha_panel, close_prices, horizon)
    base_ic = base["effective_mean_ic"]
    avg_turnover_proxy, turnover_risk_flag = _panel_turnover_context(alpha_panel)
    rows: list[dict[str, object]] = []

    for multiplier in multipliers:
        degraded_alpha = alpha_panel * float(multiplier)
        degraded_alpha.attrs.update(alpha_panel.attrs)
        score = _score_alpha_panel(degraded_alpha, close_prices, horizon)
        degradation = _degradation(base_ic, score["effective_mean_ic"])
        pass_flag = (
            not pd.isna(score["effective_mean_ic"])
            and score["effective_mean_ic"] >= 0.008
            and (pd.isna(degradation) or degradation <= 0.75)
        )
        rows.append(
            _result_row(
                alpha_panel=alpha_panel,
                horizon=horizon,
                stress_type="alpha_degradation",
                stress_case=f"alpha_x_{float(multiplier):.2f}",
                effective_mean_ic=score["effective_mean_ic"],
                effective_ic_ir=score["effective_ic_ir"],
                degradation_from_base=degradation,
                pass_flag=pass_flag,
                avg_turnover_proxy=avg_turnover_proxy,
                turnover_risk_flag=turnover_risk_flag,
                notes=f"alpha_multiplier={float(multiplier):.2f}; n_obs={score['n_obs']}",
            )
        )

    return pd.DataFrame(rows, columns=ALPHA_STRESS_RESULT_COLUMNS)


def summarize_alpha_stress_results(all_stress_results: pd.DataFrame) -> pd.DataFrame:
    """Build one stress robustness summary row per alpha."""
    if all_stress_results.empty:
        return pd.DataFrame(columns=ALPHA_STRESS_SUMMARY_COLUMNS)

    rows: list[dict[str, object]] = []
    for (alpha_name, horizon), group in all_stress_results.groupby(["alpha_name", "horizon"], dropna=False):
        pass_flags = group["pass_flag"].astype(bool)
        failures = group.loc[~pass_flags]
        degradations = pd.to_numeric(group["degradation_from_base"], errors="coerce")
        worst_degradation = float(degradations.max()) if not degradations.dropna().empty else np.nan
        catastrophic_degradation = bool((degradations > 0.80).any())

        cost_group = group[group["stress_type"].eq("cost")]
        cost_sensitivity_extreme = bool(
            (
                pd.to_numeric(cost_group["degradation_from_base"], errors="coerce") > 0.50
            ).any()
            or cost_group.loc[cost_group["stress_case"].isin(["5bps", "10bps"]), "pass_flag"].eq(False).any()
        )

        delay_group = group[group["stress_type"].eq("execution_delay")]
        small_delay_failure = bool(
            delay_group.loc[delay_group["stress_case"].isin(["1d_delay", "2d_delay"]), "pass_flag"]
            .eq(False)
            .any()
        )

        subset_group = group[group["stress_type"].eq("universe_subsample")]
        fragile_subset_warning = bool(
            not subset_group.empty and subset_group["pass_flag"].astype(bool).mean() < 0.50
        )
        avg_turnover_values = pd.to_numeric(group.get("avg_turnover_proxy"), errors="coerce")
        avg_turnover_proxy = (
            float(avg_turnover_values.dropna().iloc[0])
            if not avg_turnover_values.dropna().empty
            else np.nan
        )
        turnover_flags = group.get("turnover_risk_flag", pd.Series(dtype=object)).dropna().astype(str)
        turnover_risk_flag = turnover_flags.iloc[0] if not turnover_flags.empty else _turnover_risk_flag(avg_turnover_proxy)
        high_turnover = turnover_risk_flag == "HIGH_TURNOVER_RISK"
        weak_cost_robustness = bool(
            cost_group.loc[cost_group["stress_case"].isin(["5bps", "10bps"]), "pass_flag"]
            .eq(False)
            .any()
        )
        high_turnover_weak_cost_robustness = bool(high_turnover and weak_cost_robustness)

        failure_notes = "; ".join(
            failures.assign(reason=lambda df: df["stress_type"] + "/" + df["stress_case"] + ": " + df["notes"].astype(str))[
                "reason"
            ].tolist()
        )

        rows.append(
            {
                "alpha_name": alpha_name,
                "horizon": int(horizon),
                "n_stress_cases": int(len(group)),
                "n_passed": int(pass_flags.sum()),
                "pass_rate": float(pass_flags.mean()) if len(pass_flags) else np.nan,
                "worst_degradation": worst_degradation,
                "catastrophic_degradation": catastrophic_degradation,
                "cost_sensitivity_extreme": cost_sensitivity_extreme,
                "small_delay_failure": small_delay_failure,
                "fragile_subset_warning": fragile_subset_warning,
                "avg_turnover_proxy": avg_turnover_proxy,
                "turnover_risk_flag": turnover_risk_flag,
                "high_turnover_weak_cost_robustness": high_turnover_weak_cost_robustness,
                "failure_notes": failure_notes,
            }
        )

    return pd.DataFrame(rows, columns=ALPHA_STRESS_SUMMARY_COLUMNS).sort_values(
        ["pass_rate", "worst_degradation"],
        ascending=[False, True],
    ).reset_index(drop=True)


def _stress_matrix_column_name(stress_type: object, stress_case: object) -> str:
    return f"{stress_type}__{stress_case}"


def _build_alpha_stress_matrix(stress_results: pd.DataFrame, value_column: str) -> pd.DataFrame:
    if stress_results.empty:
        return pd.DataFrame(columns=["alpha_name", "horizon"])

    required_columns = {"alpha_name", "horizon", "stress_type", "stress_case", value_column}
    missing_columns = required_columns.difference(stress_results.columns)
    if missing_columns:
        raise ValueError(f"stress_results is missing required columns: {sorted(missing_columns)}")

    matrix_input = stress_results.copy()
    matrix_input["stress_column"] = matrix_input.apply(
        lambda row: _stress_matrix_column_name(row["stress_type"], row["stress_case"]),
        axis=1,
    )
    stress_columns = sorted(matrix_input["stress_column"].dropna().unique())
    matrix = matrix_input.pivot_table(
        index=["alpha_name", "horizon"],
        columns="stress_column",
        values=value_column,
        aggfunc="last",
        sort=True,
    )
    matrix = matrix.reindex(columns=stress_columns)
    return matrix.reset_index().rename_axis(columns=None)


def build_alpha_stress_case_matrix(stress_results: pd.DataFrame) -> pd.DataFrame:
    """Build an alpha x stress-case matrix of pass/fail flags."""
    return _build_alpha_stress_matrix(stress_results, "pass_flag")


def build_alpha_stress_degradation_matrix(stress_results: pd.DataFrame) -> pd.DataFrame:
    """Build an alpha x stress-case matrix of degradation from base IC."""
    return _build_alpha_stress_matrix(stress_results, "degradation_from_base")


def build_alpha_stress_audit_summary(
    stress_results: pd.DataFrame,
    stress_gate: pd.DataFrame,
) -> pd.DataFrame:
    """Build the pre-freeze audit summary with worst-case stress context."""
    if stress_results.empty:
        return pd.DataFrame(columns=ALPHA_STRESS_AUDIT_SUMMARY_COLUMNS)

    summary = summarize_alpha_stress_results(stress_results)
    worst_rows: list[dict[str, object]] = []
    for (alpha_name, horizon), group in stress_results.groupby(["alpha_name", "horizon"], dropna=False):
        degradations = pd.to_numeric(group["degradation_from_base"], errors="coerce")
        if degradations.dropna().empty:
            worst_rows.append(
                {
                    "alpha_name": alpha_name,
                    "horizon": int(horizon),
                    "worst_stress_type": np.nan,
                    "worst_stress_case": np.nan,
                }
            )
            continue

        worst_idx = degradations.idxmax()
        worst_row = group.loc[worst_idx]
        worst_rows.append(
            {
                "alpha_name": alpha_name,
                "horizon": int(horizon),
                "worst_stress_type": worst_row["stress_type"],
                "worst_stress_case": worst_row["stress_case"],
            }
        )

    worst_context = pd.DataFrame(worst_rows)
    audit = summary.merge(worst_context, on=["alpha_name", "horizon"], how="left")

    gate_columns = [
        "alpha_name",
        "horizon",
        "status",
        "stress_gate_notes",
        "survivor_tier",
        "promotion_decision",
        "alpha_role",
        "failure_category",
        "interpretation_notes",
    ]
    available_gate_columns = [column for column in gate_columns if column in stress_gate.columns]
    if {"alpha_name", "horizon"}.issubset(available_gate_columns):
        audit = audit.merge(
            stress_gate[available_gate_columns].drop_duplicates(["alpha_name", "horizon"]),
            on=["alpha_name", "horizon"],
            how="left",
        )
    else:
        audit["status"] = np.nan
        audit["stress_gate_notes"] = np.nan

    return audit.reindex(columns=ALPHA_STRESS_AUDIT_SUMMARY_COLUMNS).sort_values(
        ["status", "pass_rate", "worst_degradation"],
        ascending=[True, False, True],
        na_position="last",
    ).reset_index(drop=True)


def apply_alpha_stress_gate(alpha_stress_summary: pd.DataFrame) -> pd.DataFrame:
    """Apply the pre-freeze alpha stress gate."""
    gated = alpha_stress_summary.copy()
    if gated.empty:
        return gated.assign(
            status=pd.Series(dtype=object),
            stress_gate_notes=pd.Series(dtype=object),
            survivor_tier=pd.Series(dtype=object),
            promotion_decision=pd.Series(dtype=object),
            alpha_role=pd.Series(dtype=object),
            failure_category=pd.Series(dtype=object),
            interpretation_notes=pd.Series(dtype=object),
        )

    def assign_status(row: pd.Series) -> str:
        pass_rate = row.get("pass_rate")
        fatal_failure = bool(row.get("catastrophic_degradation", False))
        cost_extreme = bool(row.get("cost_sensitivity_extreme", False))
        high_turnover_weak_cost_robustness = bool(row.get("high_turnover_weak_cost_robustness", False))

        if (
            pd.isna(pass_rate)
            or float(pass_rate) < 0.50
            or fatal_failure
        ):
            return REJECTED_STRESS

        if float(pass_rate) >= 0.75 and not high_turnover_weak_cost_robustness:
            return APPROVED_STRESS

        if float(pass_rate) >= 0.50 and not fatal_failure:
            return WATCHLIST_STRESS

        return REJECTED_STRESS

    def gate_notes(row: pd.Series) -> str:
        status = row.get("status")
        if status == APPROVED_STRESS:
            return "Passes majority of stress cases with no fatal fragility flags."
        if status == WATCHLIST_STRESS:
            return "Mixed stress results but no fatal failure flags."

        notes: list[str] = []
        if pd.isna(row.get("pass_rate")) or float(row.get("pass_rate", 0.0)) < 0.50:
            notes.append("fails most stress tests")
        if bool(row.get("catastrophic_degradation", False)):
            notes.append("catastrophic degradation")
        if bool(row.get("high_turnover_weak_cost_robustness", False)):
            notes.append("high turnover with weak cost robustness")
        if bool(row.get("fragile_subset_warning", False)):
            notes.append("works only due to one fragile subset")
        if bool(row.get("small_delay_failure", False)):
            notes.append("breaks under small delays")
        if bool(row.get("cost_sensitivity_extreme", False)):
            notes.append("breaks under modest cost assumptions")
        return "; ".join(notes) if notes else "fails stress robustness gate"

    gated["status"] = gated.apply(assign_status, axis=1)
    gated["stress_gate_notes"] = gated.apply(gate_notes, axis=1)

    def assign_survivor_tier(row: pd.Series) -> str:
        status = row.get("status")
        pass_rate = row.get("pass_rate")
        turnover_risk_flag = row.get("turnover_risk_flag")
        if status != APPROVED_STRESS:
            return "NON_SURVIVOR"
        if pd.isna(pass_rate) or float(pass_rate) < 0.90:
            return "WATCH_STRESS_SURVIVOR"
        if turnover_risk_flag == "LOW_TURNOVER_RISK":
            return "CORE_STRESS_SURVIVOR"
        if turnover_risk_flag == "MODERATE_TURNOVER_RISK":
            return "BALANCED_STRESS_SURVIVOR"
        if turnover_risk_flag == "HIGH_TURNOVER_RISK":
            return "AGGRESSIVE_STRESS_SURVIVOR"
        return "WATCH_STRESS_SURVIVOR"

    gated["survivor_tier"] = gated.apply(assign_survivor_tier, axis=1)

    def promotion_decision(row: pd.Series) -> str:
        status = row.get("status")
        survivor_tier = row.get("survivor_tier")
        turnover_risk_flag = row.get("turnover_risk_flag")
        pass_rate = row.get("pass_rate")
        catastrophic_degradation = bool(row.get("catastrophic_degradation", False))

        if turnover_risk_flag == "HIGH_TURNOVER_RISK" and status == REJECTED_STRESS:
            return "REJECT_HIGH_TURNOVER"
        if status == APPROVED_STRESS and survivor_tier == "CORE_STRESS_SURVIVOR":
            return "PROMOTE_CORE"
        if status == APPROVED_STRESS and survivor_tier == "BALANCED_STRESS_SURVIVOR":
            return "PROMOTE_BALANCED"
        if status == REJECTED_STRESS and not pd.isna(pass_rate) and float(pass_rate) >= 0.90 and catastrophic_degradation:
            return "REVIEW_SATELLITE"
        if status == REJECTED_STRESS and (pd.isna(pass_rate) or float(pass_rate) < 0.90):
            return "REJECT"
        return "REJECT" if status == REJECTED_STRESS else "REVIEW_SATELLITE"

    def alpha_role(row: pd.Series) -> str:
        decision = row.get("promotion_decision")
        if decision == "PROMOTE_CORE":
            return "CORE_ALPHA"
        if decision == "PROMOTE_BALANCED":
            return "BALANCED_ALPHA"
        if decision == "REVIEW_SATELLITE":
            return "SATELLITE_CANDIDATE"
        if decision == "REJECT_HIGH_TURNOVER":
            return "HIGH_TURNOVER_REJECT"
        return "REJECTED_ALPHA"

    def failure_category(row: pd.Series) -> str:
        if row.get("status") == APPROVED_STRESS:
            return "NONE"

        categories: list[str] = []
        failure_notes = str(row.get("failure_notes", ""))
        if "subperiod/early" in failure_notes:
            categories.append("EARLY_SUBPERIOD_FRAGILITY")
        if row.get("turnover_risk_flag") == "HIGH_TURNOVER_RISK":
            categories.append("HIGH_TURNOVER")
        if bool(row.get("catastrophic_degradation", False)):
            categories.append("CATASTROPHIC_DEGRADATION")
        pass_rate = row.get("pass_rate")
        if pd.isna(pass_rate) or float(pass_rate) < 0.90:
            categories.append("LOW_PASS_RATE")

        unique_categories = list(dict.fromkeys(categories))
        if not unique_categories:
            return "MIXED_FAILURES"
        if len(unique_categories) == 1:
            return unique_categories[0]
        return "MIXED_FAILURES"

    def interpretation_notes(row: pd.Series) -> str:
        decision = row.get("promotion_decision")
        category = row.get("failure_category")
        if decision == "PROMOTE_CORE":
            return "Stable under stress; eligible for survivor freeze."
        if decision == "PROMOTE_BALANCED":
            return "Stress-resilient with balanced risk; eligible for survivor freeze review."
        if decision == "REVIEW_SATELLITE":
            return "High average performance but failed catastrophic degradation check; keep as satellite/watchlist only."
        if decision == "REJECT_HIGH_TURNOVER":
            return "Rejected due to high turnover risk."
        if category == "LOW_PASS_RATE":
            return "Rejected due to weak stress pass rate."
        if category == "EARLY_SUBPERIOD_FRAGILITY":
            return "Rejected due to early subperiod fragility."
        if category == "CATASTROPHIC_DEGRADATION":
            return "Rejected due to catastrophic degradation under stress."
        return "Rejected due to mixed stress failures."

    gated["promotion_decision"] = gated.apply(promotion_decision, axis=1)
    gated["alpha_role"] = gated.apply(alpha_role, axis=1)
    gated["failure_category"] = gated.apply(failure_category, axis=1)
    gated["interpretation_notes"] = gated.apply(interpretation_notes, axis=1)
    return gated


__all__ = [
    "ALPHA_STRESS_AUDIT_SUMMARY_COLUMNS",
    "ALPHA_STRESS_RESULT_COLUMNS",
    "ALPHA_STRESS_SUMMARY_COLUMNS",
    "APPROVED_STRESS",
    "REJECTED_STRESS",
    "WATCHLIST_STRESS",
    "apply_alpha_stress_gate",
    "build_alpha_stress_audit_summary",
    "build_alpha_stress_case_matrix",
    "build_alpha_stress_degradation_matrix",
    "build_alpha_panel",
    "load_approved_alpha_winners",
    "load_constructed_alpha_stress_inputs",
    "select_constructed_alpha_stress_candidates",
    "stress_alpha_costs",
    "stress_alpha_degradation",
    "stress_alpha_execution_delay",
    "stress_alpha_regime_holdout",
    "stress_alpha_subperiods",
    "stress_alpha_turnover",
    "stress_alpha_universe_subsamples",
    "summarize_alpha_stress_results",
]
