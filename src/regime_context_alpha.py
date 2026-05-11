from __future__ import annotations

import sqlite3
from pathlib import Path

import numpy as np
import pandas as pd

from src.alpha_construction import compute_alpha_turnover_proxy, zscore_cross_section
from src.run_config import get_sqlite_db_path


APPROVED_QUALITY_STATUS = "APPROVED_FOR_ALPHA_VALIDATION"
APPROVED_WFV_STATUSES = {
    "APPROVED_CONSTRUCTED_ALPHA_WFV",
    "WATCHLIST_CONSTRUCTED_ALPHA_WFV",
}
V3_DYNAMIC_ALPHA_PRIORITY = [
    "alpha_hybrid_adaptive_v3",
    "alpha_rolling_ic_dynamic_v3",
    "alpha_regime_blend_dynamic_v3",
    "alpha_decay_aware_dynamic_v3",
]
OVERLAY_TYPES = [
    "base_passthrough",
    "mild_regime_scaled",
    "defensive_downscale",
    "volatility_stress_scaled",
]


def _quote_identifier(identifier: str) -> str:
    return '"' + identifier.replace('"', '""') + '"'


def _table_exists(conn: sqlite3.Connection, table_name: str) -> bool:
    return (
        conn.execute(
            """
            SELECT 1
            FROM sqlite_master
            WHERE type = 'table'
              AND name = ?
            LIMIT 1
            """,
            (table_name,),
        ).fetchone()
        is not None
    )


def _load_table(table_name: str, db_path: str | Path | None = None) -> pd.DataFrame:
    db_path = Path(db_path) if db_path is not None else get_sqlite_db_path()
    with sqlite3.connect(db_path) as conn:
        if not _table_exists(conn, table_name):
            raise ValueError(f"Required table is missing: {table_name}")
        return pd.read_sql_query(f"SELECT * FROM {_quote_identifier(table_name)}", conn)


def load_regime_context_inputs(db_path: str | Path | None = None) -> dict[str, pd.DataFrame]:
    """Load current inputs for regime-context alpha construction."""
    return {
        "alpha_long": _load_table("alpha_constructed_candidates_current", db_path),
        "alpha_quality": _load_table("alpha_construction_quality_current", db_path),
        "constructed_alpha_wfv_gate": _load_table("constructed_alpha_wfv_gate_current", db_path),
        "constructed_alpha_wfv_winner_summary": _load_table(
            "constructed_alpha_wfv_winner_summary_current", db_path
        ),
        "alpha_metadata": _load_table("alpha_construction_metadata_current", db_path),
        "alpha_diagnostics": _load_table("alpha_construction_diagnostics_current", db_path),
        "regime_features": _load_table("regime_features_ic_current", db_path),
    }


def select_approved_constructed_alphas(
    alpha_quality: pd.DataFrame,
    constructed_alpha_wfv_gate: pd.DataFrame,
    constructed_alpha_wfv_winner_summary: pd.DataFrame,
) -> pd.DataFrame:
    """Select 04A-approved alphas that passed or watchlisted in 04B alpha WFV."""
    approved_quality = alpha_quality.loc[alpha_quality["status"].eq(APPROVED_QUALITY_STATUS)].copy()
    if approved_quality.empty:
        return approved_quality

    eligible_gate = constructed_alpha_wfv_gate.loc[
        constructed_alpha_wfv_gate["status"].isin(APPROVED_WFV_STATUSES)
    ].copy()
    if eligible_gate.empty:
        return pd.DataFrame(columns=list(approved_quality.columns))

    winner = constructed_alpha_wfv_winner_summary.loc[
        constructed_alpha_wfv_winner_summary["alpha_name"].isin(approved_quality["alpha_name"])
        & constructed_alpha_wfv_winner_summary["status"].isin(APPROVED_WFV_STATUSES)
    ].copy()
    if winner.empty:
        winner = (
            eligible_gate.sort_values(
                ["alpha_name", "effective_mean_test_ic", "effective_test_ic_ir", "persistence_ratio"],
                ascending=[True, False, False, False],
            )
            .groupby("alpha_name", as_index=False)
            .head(1)
            .reset_index(drop=True)
        )

    wfv_columns = [
        "alpha_name",
        "horizon",
        "status",
        "effective_mean_test_ic",
        "effective_test_ic_ir",
        "persistence_ratio",
        "sign_consistency",
    ]
    selected = approved_quality.merge(
        winner[[column for column in wfv_columns if column in winner.columns]].rename(
            columns={
                "horizon": "source_alpha_wfv_horizon",
                "status": "source_alpha_wfv_status",
                "effective_mean_test_ic": "source_effective_mean_test_ic",
                "effective_test_ic_ir": "source_effective_test_ic_ir",
                "persistence_ratio": "source_persistence_ratio",
                "sign_consistency": "source_sign_consistency",
            }
        ),
        on="alpha_name",
        how="inner",
    )
    priority = {name: rank for rank, name in enumerate(V3_DYNAMIC_ALPHA_PRIORITY)}
    selected["_priority"] = selected["alpha_name"].map(priority).fillna(len(priority))
    return selected.sort_values(
        ["_priority", "source_alpha_wfv_status", "source_effective_mean_test_ic", "alpha_name"],
        ascending=[True, True, False, True],
    ).drop(columns=["_priority"]).reset_index(drop=True)


def pivot_alpha_panel(alpha_long: pd.DataFrame, alpha_name: str) -> pd.DataFrame:
    """Pivot one constructed alpha from long format to Date x ticker."""
    selected = alpha_long.loc[alpha_long["alpha_name"].eq(alpha_name)].copy()
    if selected.empty:
        raise ValueError(f"alpha_name not found in alpha_long: {alpha_name}")
    selected["Date"] = pd.to_datetime(selected["Date"], errors="coerce")
    selected["alpha_value"] = pd.to_numeric(selected["alpha_value"], errors="coerce")
    panel = selected.pivot(index="Date", columns="ticker", values="alpha_value")
    panel.columns.name = None
    return panel.sort_index().sort_index(axis=1).replace([np.inf, -np.inf], np.nan)


def build_constructed_alpha_panels(
    alpha_long: pd.DataFrame,
    approved_alphas: pd.DataFrame,
) -> dict[str, pd.DataFrame]:
    """Build Date x ticker panels for approved constructed alphas."""
    return {
        alpha_name: pivot_alpha_panel(alpha_long, alpha_name)
        for alpha_name in approved_alphas["alpha_name"].dropna().astype(str)
    }


def _status_rank(status: object) -> int:
    order = {
        "APPROVED_CONSTRUCTED_ALPHA_WFV": 0,
        "WATCHLIST_CONSTRUCTED_ALPHA_WFV": 1,
        "REJECTED_CONSTRUCTED_ALPHA_WFV": 2,
    }
    return order.get(str(status), 9)


def select_strongest_constructed_alpha(
    approved_alphas: pd.DataFrame,
    constructed_alpha_wfv_gate: pd.DataFrame,
) -> str:
    """Pick strongest selected alpha from 04B diagnostics; retained for notebook compatibility."""
    if approved_alphas.empty:
        raise ValueError("approved_alphas is empty.")
    approved_names = set(approved_alphas["alpha_name"].dropna().astype(str))
    eligible = constructed_alpha_wfv_gate.loc[constructed_alpha_wfv_gate["alpha_name"].isin(approved_names)].copy()
    if eligible.empty:
        return sorted(approved_names)[0]
    eligible["_status_rank"] = eligible["status"].map(_status_rank)
    eligible["effective_mean_test_ic"] = pd.to_numeric(eligible["effective_mean_test_ic"], errors="coerce")
    best = eligible.sort_values(
        ["_status_rank", "effective_mean_test_ic", "effective_test_ic_ir"],
        ascending=[True, False, False],
    ).iloc[0]
    return str(best["alpha_name"])


def _regime_series(regime_features: pd.DataFrame, regime_column: str, index: pd.Index) -> pd.Series:
    features = regime_features.copy()
    features["Date"] = pd.to_datetime(features["Date"], errors="coerce")
    features = features.dropna(subset=["Date"]).set_index("Date").sort_index()
    if regime_column not in features.columns:
        raise ValueError(f"regime_features missing column: {regime_column}")
    return features[regime_column].reindex(pd.DatetimeIndex(index))


def _regime_frame(regime_features: pd.DataFrame, index: pd.Index) -> pd.DataFrame:
    frame = pd.DataFrame(index=pd.DatetimeIndex(index))
    for column in [
        "benchmark_vol_regime",
        "benchmark_trend_regime",
        "drawdown_regime",
        "correlation_regime",
    ]:
        if column in regime_features.columns:
            frame[column] = _regime_series(regime_features, column, index)
        else:
            frame[column] = np.nan
    return frame


def _scale_series(overlay_type: str, regime_features: pd.DataFrame, index: pd.Index) -> pd.Series:
    regimes = _regime_frame(regime_features, index)
    if overlay_type == "base_passthrough":
        return pd.Series(1.0, index=pd.DatetimeIndex(index), name="scale_factor")
    if overlay_type == "mild_regime_scaled":
        favorable = (
            regimes["benchmark_trend_regime"].ne("DOWNTREND")
            & regimes["drawdown_regime"].ne("HIGH_DRAWDOWN")
            & regimes["benchmark_vol_regime"].ne("HIGH_VOL")
        )
        return favorable.map({True: 1.10, False: 0.90}).astype(float).rename("scale_factor")
    if overlay_type == "defensive_downscale":
        defensive = regimes["drawdown_regime"].eq("HIGH_DRAWDOWN") | regimes["benchmark_trend_regime"].eq("DOWNTREND")
        return defensive.map({True: 0.75, False: 1.00}).astype(float).rename("scale_factor")
    if overlay_type == "volatility_stress_scaled":
        stress = regimes["benchmark_vol_regime"].eq("HIGH_VOL")
        return stress.map({True: 0.75, False: 1.00}).astype(float).rename("scale_factor")
    raise ValueError(f"Unknown overlay_type: {overlay_type}")


def _scaling_rule(overlay_type: str) -> str:
    rules = {
        "base_passthrough": "scale=1.00 for all dates; no overlay.",
        "mild_regime_scaled": "scale=1.10 when not DOWNTREND/HIGH_DRAWDOWN/HIGH_VOL, else 0.90.",
        "defensive_downscale": "scale=0.75 during HIGH_DRAWDOWN or DOWNTREND, else 1.00.",
        "volatility_stress_scaled": "scale=0.75 during HIGH_VOL, else 1.00.",
    }
    return rules[overlay_type]


def _overlay_alpha(base_panel: pd.DataFrame, scale: pd.Series) -> pd.DataFrame:
    """Apply same-day regime scale and keep dense normalized alpha surface."""
    scaled = base_panel.mul(scale.reindex(base_panel.index).astype(float), axis=0)
    output = zscore_cross_section(scaled, clip_value=3.0)
    output.attrs["scale_factor"] = scale.reindex(base_panel.index).astype(float)
    return output


def build_regime_context_alpha_candidates(
    alpha_panels: dict[str, pd.DataFrame],
    approved_alphas: pd.DataFrame,
    constructed_alpha_wfv_gate: pd.DataFrame,
    regime_features: pd.DataFrame,
) -> tuple[dict[str, pd.DataFrame], pd.DataFrame]:
    """Build optional regime overlay candidates from selected 04B-approved/watchlist base alphas."""
    candidates: dict[str, pd.DataFrame] = {}
    metadata_rows: list[dict[str, object]] = []
    for row in approved_alphas.to_dict("records"):
        base_alpha_name = str(row["alpha_name"])
        if base_alpha_name not in alpha_panels:
            continue
        base_panel = alpha_panels[base_alpha_name]
        for overlay_type in OVERLAY_TYPES:
            alpha_name = f"{base_alpha_name}__{overlay_type}"
            scale = _scale_series(overlay_type, regime_features, base_panel.index)
            candidates[alpha_name] = _overlay_alpha(base_panel, scale)
            metadata_rows.append(
                {
                    "alpha_name": alpha_name,
                    "overlay_type": overlay_type,
                    "base_alpha_name": base_alpha_name,
                    "source_alpha_wfv_status": row.get("source_alpha_wfv_status"),
                    "source_alpha_wfv_horizon": row.get("source_alpha_wfv_horizon"),
                    "source_effective_mean_test_ic": row.get("source_effective_mean_test_ic"),
                    "source_persistence_ratio": row.get("source_persistence_ratio"),
                    "scaling_rule": _scaling_rule(overlay_type),
                    "regime_column": "benchmark_trend_regime,drawdown_regime,benchmark_vol_regime",
                    "notes": "Optional same-day regime overlay diagnostic; base alpha direction and formula are unchanged.",
                }
            )
    return candidates, pd.DataFrame(metadata_rows)


def _quality_status(finite_pct: float, max_abs_alpha: float, turnover_risk_flag: str | float) -> str:
    if finite_pct >= 0.90 and max_abs_alpha <= 3.0 and turnover_risk_flag != "HIGH_TURNOVER_RISK":
        return "APPROVED_FOR_REGIME_CONTEXT_WFV"
    return "REJECTED_REGIME_CONTEXT"


def _quality_notes(status: str) -> str:
    if status == "APPROVED_FOR_REGIME_CONTEXT_WFV":
        return "Passes overlay coverage, scale, and turnover checks."
    return "Fails overlay coverage, scale, all-NaN, or turnover checks."


def build_regime_context_quality(alpha_candidates: dict[str, pd.DataFrame]) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for alpha_name, panel in alpha_candidates.items():
        values = panel.to_numpy(dtype=float)
        finite = np.isfinite(values)
        finite_pct = float(finite.mean()) if values.size else 0.0
        finite_values = values[finite]
        max_abs_alpha = float(np.nanmax(np.abs(finite_values))) if finite_values.size else np.nan
        turnover = compute_alpha_turnover_proxy(panel)["turnover_proxy"].dropna()
        avg_turnover_proxy = float(turnover.mean()) if not turnover.empty else np.nan
        turnover_risk_flag = _turnover_risk_flag(avg_turnover_proxy)
        status = _quality_status(finite_pct, max_abs_alpha, turnover_risk_flag)
        valid_dates = panel.index[pd.Series(finite.any(axis=1), index=panel.index)]
        rows.append(
            {
                "alpha_name": alpha_name,
                "finite_pct": finite_pct,
                "missing_pct": 1.0 - finite_pct,
                "max_abs_alpha": max_abs_alpha,
                "avg_turnover_proxy": avg_turnover_proxy,
                "turnover_risk_flag": turnover_risk_flag,
                "n_dates": int(panel.shape[0]),
                "n_tickers": int(panel.shape[1]),
                "first_valid_date": valid_dates.min() if len(valid_dates) else pd.NaT,
                "last_valid_date": valid_dates.max() if len(valid_dates) else pd.NaT,
                "status": status,
                "quality_notes": _quality_notes(status),
            }
        )
    return pd.DataFrame(rows)


def _turnover_risk_flag(avg_turnover_proxy: float) -> str | float:
    if pd.isna(avg_turnover_proxy):
        return np.nan
    if avg_turnover_proxy < 1.75:
        return "LOW_TURNOVER_RISK"
    if avg_turnover_proxy < 2.50:
        return "MODERATE_TURNOVER_RISK"
    return "HIGH_TURNOVER_RISK"


def build_regime_context_diagnostics(alpha_candidates: dict[str, pd.DataFrame]) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for alpha_name, panel in alpha_candidates.items():
        values = panel.to_numpy(dtype=float)
        finite = np.isfinite(values)
        finite_values = values[finite]
        turnover = compute_alpha_turnover_proxy(panel)["turnover_proxy"].dropna()
        avg_turnover_proxy = float(turnover.mean()) if not turnover.empty else np.nan
        scale = panel.attrs.get("scale_factor")
        if isinstance(scale, pd.Series):
            overlay_active_pct = float(scale.ne(1.0).mean())
            avg_scale_factor = float(scale.mean())
            min_scale_factor = float(scale.min())
            max_scale_factor = float(scale.max())
        else:
            overlay_active_pct = np.nan
            avg_scale_factor = np.nan
            min_scale_factor = np.nan
            max_scale_factor = np.nan
        rows.append(
            {
                "alpha_name": alpha_name,
                "finite_pct": float(finite.mean()) if values.size else 0.0,
                "missing_pct": 1.0 - (float(finite.mean()) if values.size else 0.0),
                "n_dates": int(panel.shape[0]),
                "n_tickers": int(panel.shape[1]),
                "mean_abs_alpha": float(np.nanmean(np.abs(finite_values))) if finite_values.size else np.nan,
                "alpha_std": float(np.nanstd(finite_values, ddof=1)) if finite_values.size > 1 else np.nan,
                "max_abs_alpha": float(np.nanmax(np.abs(finite_values))) if finite_values.size else np.nan,
                "avg_turnover_proxy": avg_turnover_proxy,
                "median_turnover_proxy": float(turnover.median()) if not turnover.empty else np.nan,
                "max_turnover_proxy": float(turnover.max()) if not turnover.empty else np.nan,
                "turnover_risk_flag": _turnover_risk_flag(avg_turnover_proxy),
                "overlay_active_pct": overlay_active_pct,
                "avg_scale_factor": avg_scale_factor,
                "min_scale_factor": min_scale_factor,
                "max_scale_factor": max_scale_factor,
            }
        )
    return pd.DataFrame(rows)


def build_regime_context_activation_diagnostics(
    metadata: pd.DataFrame,
    regime_features: pd.DataFrame,
    alpha_candidates: dict[str, pd.DataFrame] | None = None,
) -> pd.DataFrame:
    """Summarize overlay scale behavior for each regime-context alpha."""
    rows: list[dict[str, object]] = []
    for row in metadata.to_dict("records"):
        alpha_name = str(row.get("alpha_name"))
        panel = alpha_candidates.get(alpha_name) if alpha_candidates is not None else None
        if panel is None:
            continue
        scale = panel.attrs.get("scale_factor")
        if not isinstance(scale, pd.Series):
            scale = pd.Series(1.0, index=panel.index)
        rows.append(
            {
                "alpha_name": alpha_name,
                "overlay_type": row.get("overlay_type"),
                "base_alpha_name": row.get("base_alpha_name"),
                "scaling_rule": row.get("scaling_rule"),
                "overlay_active_pct": float(scale.ne(1.0).mean()),
                "avg_scale_factor": float(scale.mean()),
                "min_scale_factor": float(scale.min()),
                "max_scale_factor": float(scale.max()),
                "n_scaled_dates": int(scale.ne(1.0).sum()),
                "n_total_dates": int(len(scale)),
            }
        )

    return pd.DataFrame(rows)


__all__ = [
    "APPROVED_WFV_STATUSES",
    "OVERLAY_TYPES",
    "V3_DYNAMIC_ALPHA_PRIORITY",
    "build_constructed_alpha_panels",
    "build_regime_context_activation_diagnostics",
    "build_regime_context_alpha_candidates",
    "build_regime_context_diagnostics",
    "build_regime_context_quality",
    "load_regime_context_inputs",
    "pivot_alpha_panel",
    "select_approved_constructed_alphas",
    "select_strongest_constructed_alpha",
]
