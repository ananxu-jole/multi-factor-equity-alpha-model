from __future__ import annotations

import sqlite3
import json
from pathlib import Path

import numpy as np
import pandas as pd

from src.run_config import get_sqlite_db_path


ALPHA_EQUAL_WEIGHT = "alpha_equal_weight_research_v1"
ALPHA_HEALTH_WEIGHTED = "alpha_health_weighted_research_v1"
ALPHA_REGIME_AWARE = "alpha_regime_aware_research_v1"
ALPHA_DIVERSIFIED_V2 = "alpha_diversified_research_v2"
ALPHA_SMOOTH_REGIME_WEIGHTED_V2 = "alpha_smooth_regime_weighted_v2"
ALPHA_PERSISTENCE_BLEND_V2 = "alpha_persistence_blend_v2"
ALPHA_DECAY_AWARE_DYNAMIC_V3 = "alpha_decay_aware_dynamic_v3"
ALPHA_REGIME_BLEND_DYNAMIC_V3 = "alpha_regime_blend_dynamic_v3"
ALPHA_ROLLING_IC_DYNAMIC_V3 = "alpha_rolling_ic_dynamic_v3"
ALPHA_HYBRID_ADAPTIVE_V3 = "alpha_hybrid_adaptive_v3"
ALPHA_DECAY_AWARE_DYNAMIC_V4_SMOOTH = "alpha_decay_aware_dynamic_v4_smooth"
ALPHA_REGIME_BLEND_DYNAMIC_V4_SMOOTH = "alpha_regime_blend_dynamic_v4_smooth"
ALPHA_ROLLING_IC_DYNAMIC_V4_SMOOTH = "alpha_rolling_ic_dynamic_v4_smooth"
ALPHA_HYBRID_ADAPTIVE_V4_SMOOTH = "alpha_hybrid_adaptive_v4_smooth"
ALPHA_ORTHOGONAL_DIVERSIFIER_V1_SMOOTH = "alpha_orthogonal_diversifier_v1_smooth"
ALPHA_ORTHOGONAL_DIVERSIFIER_V2_SCORE_WEIGHTED_SMOOTH = "alpha_orthogonal_diversifier_v2_score_weighted_smooth"

SLEEVE_CORE_REGIME = "CORE_REGIME"
SLEEVE_DECAY_STABILITY = "DECAY_STABILITY"
SLEEVE_ORTHOGONAL_DIVERSIFIER = "ORTHOGONAL_DIVERSIFIER"

ORTHOGONAL_DIVERSIFIER_V2_COMPONENTS = [
    ("vol_surprise_20_60", 20),
    ("price_impact_proxy_20", 20),
    ("range_expansion_failure_5", 20),
    ("liquidity_adjusted_reversal_5", 5),
]

PREFERRED_DIVERSIFIER_FAMILIES = [
    "short_term_reversal",
    "mean_reversion",
    "momentum",
    "trend_quality",
]

DECAY_RISK_MULTIPLIER = {
    "LOW_DECAY_RISK": 1.0,
    "MODERATE_DECAY_RISK": 0.6,
    "HIGH_DECAY_RISK": 0.25,
}


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


def _load_optional_table(table_name: str, db_path: str | Path | None = None) -> pd.DataFrame:
    db_path = Path(db_path) if db_path is not None else get_sqlite_db_path()
    with sqlite3.connect(db_path) as conn:
        if not _table_exists(conn, table_name):
            return pd.DataFrame()
        return pd.read_sql_query(f"SELECT * FROM {_quote_identifier(table_name)}", conn)


def load_candidate_signals_for_names(
    signal_names: list[str] | tuple[str, ...] | set[str],
    db_path: str | Path | None = None,
) -> pd.DataFrame:
    """Load only the candidate signal rows needed by 04A."""
    names = sorted({str(name) for name in signal_names if pd.notna(name)})
    if not names:
        return pd.DataFrame(columns=["Date", "ticker", "signal_name", "signal_value", "run_id", "signal_version"])

    db_path = Path(db_path) if db_path is not None else get_sqlite_db_path()
    placeholders = ",".join("?" for _ in names)
    query = (
        f"SELECT * FROM {_quote_identifier('candidate_signals_current')} "
        f"WHERE signal_name IN ({placeholders})"
    )
    with sqlite3.connect(db_path) as conn:
        if not _table_exists(conn, "candidate_signals_current"):
            raise ValueError("Required table is missing: candidate_signals_current")
        return pd.read_sql_query(query, conn, params=names)


def _price_panel_from_table(df: pd.DataFrame) -> pd.DataFrame:
    panel = df.copy()
    for column in ["run_id", "run_timestamp", "timestamp"]:
        if column in panel.columns:
            panel = panel.drop(columns=column)
    if "Date" not in panel.columns:
        raise ValueError("Price table is missing Date column.")
    panel["Date"] = pd.to_datetime(panel["Date"], errors="coerce")
    panel = panel.set_index("Date").sort_index()
    return panel.apply(pd.to_numeric, errors="coerce")


def build_dynamic_universe_eligibility_mask(
    membership: pd.DataFrame,
    close_prices: pd.DataFrame,
    warmup_trading_days: int = 60,
) -> tuple[pd.DataFrame, pd.Timestamp]:
    """Build the 04A quality denominator from shifted dynamic universe membership."""
    if membership.empty:
        raise ValueError("Dynamic universe membership table is empty.")
    required_columns = {"Date", "ticker"}
    missing_columns = required_columns.difference(membership.columns)
    if missing_columns:
        raise ValueError(f"membership is missing required columns: {sorted(missing_columns)}")

    selected = membership.copy()
    selected["Date"] = pd.to_datetime(selected["Date"], errors="coerce")
    if "in_universe" in selected.columns:
        selected = selected.loc[pd.to_numeric(selected["in_universe"], errors="coerce").fillna(0).astype(int).eq(1)]
    selected = selected.dropna(subset=["Date", "ticker"])
    selected["_eligible"] = True
    universe_mask = selected.pivot_table(
        index="Date",
        columns="ticker",
        values="_eligible",
        aggfunc="max",
        fill_value=False,
    ).astype(bool)

    close = close_prices.sort_index().sort_index(axis=1).apply(pd.to_numeric, errors="coerce")
    close.index = pd.to_datetime(close.index)
    eligible = universe_mask.reindex(index=close.index, columns=close.columns, fill_value=False).astype(bool)
    eligible = eligible & close.notna()

    warmup_index = min(max(int(warmup_trading_days), 0), max(len(close.index) - 1, 0))
    warmup_cutoff = pd.Timestamp(close.index[warmup_index])
    eligible = eligible & pd.DataFrame(
        np.repeat(np.asarray(close.index >= warmup_cutoff)[:, None], len(close.columns), axis=1),
        index=close.index,
        columns=close.columns,
    )
    return eligible, warmup_cutoff


def load_alpha_construction_inputs(
    db_path: str | Path | None = None,
    include_candidate_signals: bool = True,
) -> dict[str, pd.DataFrame]:
    """Load Phase 4A input tables from SQLite."""
    inputs = {
        "reproducibility_gate": _load_table("signal_reproducibility_gate_current", db_path),
        "signal_health": _load_table("signal_health_score_current", db_path),
        "signal_decay": _load_table("signal_decay_summary_current", db_path),
        "diversity_selection": _load_table("signal_diversity_selection_current", db_path),
        "diversity_similarity": _load_optional_table("signal_diversity_similarity_current", db_path),
        "regime_opportunity": _load_table("signal_regime_opportunity_summary_current", db_path),
        "regime_features": _load_table("regime_features_ic_current", db_path),
        "close_prices": _price_panel_from_table(_load_table("clean_close_prices_current", db_path)),
    }
    inputs["candidate_signals"] = (
        _load_table("candidate_signals_current", db_path)
        if include_candidate_signals
        else pd.DataFrame(columns=["Date", "ticker", "signal_name", "signal_value", "run_id", "signal_version"])
    )
    return inputs


def get_approved_alpha_research_signals(
    reproducibility_gate: pd.DataFrame,
    signal_health: pd.DataFrame,
    regime_opportunity: pd.DataFrame,
) -> pd.DataFrame:
    """Return final research-approved signal/horizon rows enriched with direction and regime info."""
    approved = reproducibility_gate.loc[
        reproducibility_gate["final_research_gate"].eq("APPROVED_FOR_ALPHA_RESEARCH")
    ].copy()
    if approved.empty:
        return approved

    health_columns = [
        "signal_name",
        "horizon",
        "signal_direction",
        "signal_strength",
        "signal_health_score",
    ]
    regime_columns = [
        "signal_name",
        "horizon",
        "best_regime_column",
        "best_regime_value",
    ]
    approved = approved.merge(
        signal_health[[column for column in health_columns if column in signal_health.columns]],
        on=["signal_name", "horizon", "signal_health_score"],
        how="left",
    )
    approved = approved.merge(
        regime_opportunity[[column for column in regime_columns if column in regime_opportunity.columns]],
        on=["signal_name", "horizon"],
        how="left",
    )
    approved["component_id"] = approved["signal_name"].astype(str) + "_h" + approved["horizon"].astype(int).astype(str)
    return approved.sort_values(["signal_health_score", "signal_name", "horizon"], ascending=[False, True, True]).reset_index(drop=True)


def get_watchlist_diversifier_signals(
    signal_health: pd.DataFrame,
    max_signals: int = 3,
) -> pd.DataFrame:
    """Select modest non-volatility watchlist diversifiers for v2 alpha construction."""
    watchlist = signal_health.loc[
        signal_health["signal_health_gate"].eq("WATCHLIST_RESEARCH")
        & signal_health["recommended_use"].ne("AVOID")
        & signal_health["decay_risk_flag"].ne("HIGH_DECAY_RISK")
    ].copy()
    if watchlist.empty:
        return watchlist

    preferred = watchlist.loc[
        ~watchlist["signal_family"].isin(["volatility", "defensive_quality"])
    ].copy()
    if preferred.empty:
        preferred = watchlist.copy()

    family_rank = {family: rank for rank, family in enumerate(PREFERRED_DIVERSIFIER_FAMILIES)}
    preferred["_family_rank"] = preferred["signal_family"].map(family_rank).fillna(
        len(PREFERRED_DIVERSIFIER_FAMILIES)
    )
    selected = (
        preferred.sort_values(
            ["_family_rank", "signal_health_score", "signal_name", "horizon"],
            ascending=[True, False, True, True],
        )
        .head(max_signals)
        .drop(columns=["_family_rank"])
        .copy()
    )
    selected["component_id"] = (
        selected["signal_name"].astype(str) + "_h" + selected["horizon"].astype(int).astype(str)
    )
    selected["source_role"] = "WATCHLIST_DIVERSIFIER"
    return selected.reset_index(drop=True)


def _component_id(df: pd.DataFrame) -> pd.Series:
    return df["signal_name"].astype(str) + "_h" + df["horizon"].astype(int).astype(str)


def _base_pool_rows(
    reproducibility_gate: pd.DataFrame,
    signal_health: pd.DataFrame,
    signal_decay: pd.DataFrame,
    regime_opportunity: pd.DataFrame,
    diversity_selection: pd.DataFrame,
) -> pd.DataFrame:
    health = signal_health.copy()
    health["component_id"] = _component_id(health)

    repro_columns = [
        "signal_name",
        "horizon",
        "final_research_gate",
        "reproducibility_status",
        "pass_rate",
        "avg_effective_mean_ic",
    ]
    decay_columns = [
        "signal_name",
        "horizon",
        "decay_status",
        "decay_risk_flag",
        "sign_stability",
    ]
    regime_columns = [
        "signal_name",
        "horizon",
        "best_regime_column",
        "best_regime_value",
        "adjusted_best_abs_ic",
    ]
    diversity_columns = [
        "signal_name",
        "horizon",
        "selected_flag",
        "diversity_group",
        "diversity_candidate_tier",
        "signal_source",
        "orthogonal_version",
    ]

    pool = health.merge(
        reproducibility_gate[[column for column in repro_columns if column in reproducibility_gate.columns]],
        on=["signal_name", "horizon"],
        how="left",
        suffixes=("", "_repro"),
    )
    pool = pool.merge(
        signal_decay[[column for column in decay_columns if column in signal_decay.columns]],
        on=["signal_name", "horizon"],
        how="left",
        suffixes=("", "_decay"),
    )
    pool = pool.merge(
        regime_opportunity[[column for column in regime_columns if column in regime_opportunity.columns]],
        on=["signal_name", "horizon"],
        how="left",
        suffixes=("", "_regime"),
    )
    if not diversity_selection.empty:
        pool = pool.merge(
            diversity_selection[[column for column in diversity_columns if column in diversity_selection.columns]],
            on=["signal_name", "horizon"],
            how="left",
        )
    else:
        pool["selected_flag"] = 0
        pool["diversity_group"] = np.nan

    for column in ["final_research_gate", "reproducibility_status", "decay_status", "decay_risk_flag"]:
        if column not in pool.columns:
            pool[column] = np.nan
    pool["selected_flag"] = pd.to_numeric(pool.get("selected_flag", 0), errors="coerce").fillna(0).astype(int)
    return pool


def _low_redundancy_watchlist(
    candidates: pd.DataFrame,
    selected_components: set[str],
    diversity_similarity: pd.DataFrame,
    max_abs_corr: float = 0.85,
) -> pd.DataFrame:
    if candidates.empty or diversity_similarity.empty:
        return candidates
    sim = diversity_similarity.copy()
    if "signal_key_1" not in sim.columns or "signal_key_2" not in sim.columns:
        return candidates

    keep_rows = []
    for row in candidates.itertuples(index=False):
        component_id = str(row.component_id)
        related = sim.loc[
            (
                sim["signal_key_1"].eq(component_id)
                & sim["signal_key_2"].isin(selected_components)
            )
            | (
                sim["signal_key_2"].eq(component_id)
                & sim["signal_key_1"].isin(selected_components)
            )
        ]
        max_corr = pd.to_numeric(related.get("correlation", pd.Series(dtype=float)), errors="coerce").abs().max()
        if pd.isna(max_corr) or float(max_corr) < max_abs_corr:
            keep_rows.append(row._asdict())
    return pd.DataFrame(keep_rows)


def build_alpha_signal_pool(
    reproducibility_gate: pd.DataFrame,
    signal_health: pd.DataFrame,
    signal_decay: pd.DataFrame,
    regime_opportunity: pd.DataFrame,
    diversity_selection: pd.DataFrame,
    diversity_similarity: pd.DataFrame | None = None,
    max_watchlist_diversifiers: int = 3,
) -> pd.DataFrame:
    """Build explicit v3 signal pool from approved, diversity-selected, and watchlist diversifier rows."""
    if diversity_similarity is None:
        diversity_similarity = pd.DataFrame()
    pool = _base_pool_rows(
        reproducibility_gate=reproducibility_gate,
        signal_health=signal_health,
        signal_decay=signal_decay,
        regime_opportunity=regime_opportunity,
        diversity_selection=diversity_selection,
    )

    approved_mask = pool["final_research_gate"].eq("APPROVED_FOR_ALPHA_RESEARCH")
    selected_mask = pool["selected_flag"].eq(1)
    core = pool.loc[approved_mask | selected_mask].copy()
    core["source_role"] = np.where(core["selected_flag"].eq(1), "DIVERSITY_SELECTED", "CORE_APPROVED")

    selected_components = set(core["component_id"].astype(str))
    watchlist = pool.loc[
        pool["signal_health_gate"].eq("WATCHLIST_RESEARCH")
        & pool["decay_status"].eq("STABLE")
        & ~pool.get("scoring_status", pd.Series(index=pool.index, dtype=object)).astype(str).str.contains("REJECTED", na=False)
        & ~pool["component_id"].isin(selected_components)
    ].copy()
    watchlist = _low_redundancy_watchlist(watchlist, selected_components, diversity_similarity)
    if not watchlist.empty:
        watchlist = watchlist.sort_values(
            ["signal_health_score", "adjusted_best_abs_ic", "signal_name", "horizon"],
            ascending=[False, False, True, True],
        ).head(max_watchlist_diversifiers)
        watchlist["source_role"] = "WATCHLIST_DIVERSIFIER"

    output = pd.concat([core, watchlist], ignore_index=True)
    if output.empty:
        return output
    output = output.drop_duplicates("component_id").copy()

    output["sign_stability"] = pd.to_numeric(output.get("sign_stability", 0.5), errors="coerce").fillna(0.5)
    output["signal_health_score"] = pd.to_numeric(output["signal_health_score"], errors="coerce").fillna(0.0)
    output["decay_multiplier"] = output["decay_risk_flag"].map(DECAY_RISK_MULTIPLIER).fillna(0.5)
    output["pool_weight_raw"] = (
        output["signal_health_score"].clip(lower=0.0)
        * output["sign_stability"].clip(lower=0.0)
        * output["decay_multiplier"]
    )
    raw_total = output["pool_weight_raw"].sum()
    output["pool_weight_base"] = output["pool_weight_raw"] / raw_total if raw_total > 0 else 1.0 / len(output)
    output["pool_eligible_flag"] = 1
    output["pool_reason"] = output["source_role"].map(
        {
            "CORE_APPROVED": "Approved for alpha research.",
            "DIVERSITY_SELECTED": "Selected by 03G diversity engine.",
            "WATCHLIST_DIVERSIFIER": "Watchlist diversifier with stable decay and acceptable redundancy.",
        }
    )

    columns = [
        "component_id",
        "signal_name",
        "horizon",
        "signal_family",
        "signal_direction",
        "signal_strength",
        "source_role",
        "signal_health_score",
        "final_research_gate",
        "reproducibility_status",
        "pass_rate",
        "avg_effective_mean_ic",
        "decay_status",
        "decay_risk_flag",
        "sign_stability",
        "recommended_use",
        "best_regime_column",
        "best_regime_value",
        "adjusted_best_abs_ic",
        "selected_flag",
        "diversity_group",
        "diversity_candidate_tier",
        "signal_source",
        "orthogonal_version",
        "pool_weight_base",
        "pool_eligible_flag",
        "pool_reason",
    ]
    for column in columns:
        if column not in output.columns:
            output[column] = np.nan
    return output[columns].sort_values(["source_role", "pool_weight_base"], ascending=[True, False]).reset_index(drop=True)


def _pivot_signal_panel(candidate_signals: pd.DataFrame, signal_name: str) -> pd.DataFrame:
    selected = candidate_signals.loc[candidate_signals["signal_name"].eq(signal_name)].copy()
    if selected.empty:
        raise ValueError(f"Signal not found in candidate_signals: {signal_name}")
    selected["Date"] = pd.to_datetime(selected["Date"], errors="coerce")
    selected["signal_value"] = pd.to_numeric(selected["signal_value"], errors="coerce")
    panel = selected.pivot(index="Date", columns="ticker", values="signal_value")
    panel.columns.name = None
    return panel.sort_index().sort_index(axis=1).replace([np.inf, -np.inf], np.nan)


def normalize_signal_panel(signal_panel: pd.DataFrame, signal_direction: str) -> pd.DataFrame:
    """Direction-adjust and cross-sectionally rank a Date x ticker signal panel around zero."""
    panel = signal_panel.copy().apply(pd.to_numeric, errors="coerce")
    if signal_direction == "NEGATIVE_EDGE_REVERSE_SIGNAL":
        panel = -panel
    normalized = panel.rank(axis=1, pct=True) - 0.5
    return normalized.replace([np.inf, -np.inf], np.nan)


def zscore_cross_section(panel: pd.DataFrame, clip_value: float = 3.0) -> pd.DataFrame:
    """Cross-sectionally z-score each date, safely handling zero dispersion."""
    values = panel.copy().apply(pd.to_numeric, errors="coerce")
    row_mean = values.mean(axis=1, skipna=True)
    row_std = values.std(axis=1, skipna=True).replace(0.0, np.nan)
    zscored = values.sub(row_mean, axis=0).div(row_std, axis=0)
    return zscored.replace([np.inf, -np.inf], np.nan).clip(-clip_value, clip_value)


def build_normalized_signal_panels(
    approved_signals: pd.DataFrame,
    candidate_signals: pd.DataFrame,
) -> dict[str, pd.DataFrame]:
    """Build direction-adjusted normalized component panels keyed by signal/horizon component id."""
    raw_cache: dict[str, pd.DataFrame] = {}
    panels: dict[str, pd.DataFrame] = {}
    for row in approved_signals.itertuples(index=False):
        signal_name = str(row.signal_name)
        if signal_name not in raw_cache:
            raw_cache[signal_name] = _pivot_signal_panel(candidate_signals, signal_name)
        panels[str(row.component_id)] = normalize_signal_panel(
            raw_cache[signal_name],
            getattr(row, "signal_direction", "POSITIVE_EDGE"),
        )
    return panels


def build_component_signal_panels(
    component_signals: pd.DataFrame,
    candidate_signals: pd.DataFrame,
) -> dict[str, pd.DataFrame]:
    """Build direction-adjusted normalized panels for arbitrary signal/horizon components."""
    if component_signals.empty:
        return {}
    components = component_signals.copy()
    if "component_id" not in components.columns:
        components["component_id"] = (
            components["signal_name"].astype(str) + "_h" + components["horizon"].astype(int).astype(str)
        )

    raw_cache: dict[str, pd.DataFrame] = {}
    panels: dict[str, pd.DataFrame] = {}
    for row in components.itertuples(index=False):
        signal_name = str(row.signal_name)
        if signal_name not in raw_cache:
            raw_cache[signal_name] = _pivot_signal_panel(candidate_signals, signal_name)
        panels[str(row.component_id)] = normalize_signal_panel(
            raw_cache[signal_name],
            getattr(row, "signal_direction", "POSITIVE_EDGE"),
        )
    return panels


def build_zscored_component_signal_panels(
    component_signals: pd.DataFrame,
    candidate_signals: pd.DataFrame,
) -> dict[str, pd.DataFrame]:
    """Build direction-adjusted cross-sectional z-scored panels for v3 dynamic alphas."""
    if component_signals.empty:
        return {}
    components = component_signals.copy()
    raw_cache: dict[str, pd.DataFrame] = {}
    panels: dict[str, pd.DataFrame] = {}
    for row in components.itertuples(index=False):
        signal_name = str(row.signal_name)
        if signal_name not in raw_cache:
            raw_cache[signal_name] = _pivot_signal_panel(candidate_signals, signal_name)
        panel = raw_cache[signal_name].copy()
        if getattr(row, "signal_direction", "POSITIVE_EDGE") == "NEGATIVE_EDGE_REVERSE_SIGNAL":
            panel = -panel
        panels[str(row.component_id)] = zscore_cross_section(panel, clip_value=3.0)
    return panels


def _weighted_average_panels(
    panels: dict[str, pd.DataFrame],
    weights: dict[str, float],
    masks: dict[str, pd.Series] | None = None,
) -> pd.DataFrame:
    if not panels:
        return pd.DataFrame()
    all_index = sorted(set().union(*(panel.index for panel in panels.values())))
    all_columns = sorted(set().union(*(panel.columns for panel in panels.values())))
    numerator = pd.DataFrame(0.0, index=all_index, columns=all_columns)
    denominator = pd.DataFrame(0.0, index=all_index, columns=all_columns)

    for name, panel in panels.items():
        weight = float(weights.get(name, 0.0))
        aligned = panel.reindex(index=all_index, columns=all_columns)
        valid = aligned.notna()
        if masks is not None and name in masks:
            mask = masks[name].reindex(all_index).fillna(False).astype(bool)
            valid = valid & pd.DataFrame(
                np.repeat(mask.to_numpy()[:, None], len(all_columns), axis=1),
                index=all_index,
                columns=all_columns,
            )
            aligned = aligned.where(valid)
        numerator = numerator.add(aligned.fillna(0.0) * weight, fill_value=0.0)
        denominator = denominator.add(valid.astype(float) * abs(weight), fill_value=0.0)

    output = numerator / denominator.replace(0.0, np.nan)
    output.index = pd.to_datetime(output.index)
    return output.sort_index().sort_index(axis=1).replace([np.inf, -np.inf], np.nan)


def build_equal_weight_alpha(normalized_panels: dict[str, pd.DataFrame]) -> pd.DataFrame:
    weights = {name: 1.0 for name in normalized_panels}
    return _weighted_average_panels(normalized_panels, weights)


def build_health_weighted_alpha(
    normalized_panels: dict[str, pd.DataFrame],
    approved_signals: pd.DataFrame,
) -> pd.DataFrame:
    scores = approved_signals.set_index("component_id")["signal_health_score"].astype(float)
    total = scores.sum()
    weights = (scores / total).to_dict() if total > 0 else {name: 1.0 for name in normalized_panels}
    return _weighted_average_panels(normalized_panels, weights)


def build_regime_aware_alpha(
    normalized_panels: dict[str, pd.DataFrame],
    approved_signals: pd.DataFrame,
    regime_features: pd.DataFrame,
) -> pd.DataFrame:
    features = regime_features.copy()
    features["Date"] = pd.to_datetime(features["Date"], errors="coerce")
    features = features.set_index("Date").sort_index()
    masks: dict[str, pd.Series] = {}
    for row in approved_signals.itertuples(index=False):
        column = getattr(row, "best_regime_column", None)
        value = getattr(row, "best_regime_value", None)
        component_id = str(row.component_id)
        if column in features.columns and pd.notna(value):
            masks[component_id] = features[column].eq(value)
        else:
            masks[component_id] = pd.Series(False, index=features.index)
    scores = approved_signals.set_index("component_id")["signal_health_score"].astype(float)
    total = scores.sum()
    weights = (scores / total).to_dict() if total > 0 else {name: 1.0 for name in normalized_panels}
    return _weighted_average_panels(normalized_panels, weights, masks=masks)


def build_diversified_alpha_v2(
    normalized_panels: dict[str, pd.DataFrame],
    approved_signals: pd.DataFrame,
    watchlist_diversifiers: pd.DataFrame,
) -> pd.DataFrame:
    components = pd.concat([approved_signals, watchlist_diversifiers], ignore_index=True)
    if watchlist_diversifiers.empty:
        scores = approved_signals.set_index("component_id")["signal_health_score"].astype(float)
        weights = (scores / scores.sum()).to_dict() if scores.sum() > 0 else {name: 1.0 for name in normalized_panels}
        return _weighted_average_panels(normalized_panels, weights)

    weights: dict[str, float] = {}
    approved_scores = approved_signals.set_index("component_id")["signal_health_score"].astype(float)
    diversifier_scores = watchlist_diversifiers.set_index("component_id")["signal_health_score"].astype(float)
    approved_total = approved_scores.sum()
    diversifier_total = diversifier_scores.sum()

    for component_id, score in approved_scores.items():
        weights[component_id] = 0.70 * float(score / approved_total) if approved_total > 0 else 0.0
    for component_id, score in diversifier_scores.items():
        weights[component_id] = weights.get(component_id, 0.0) + (
            0.30 * float(score / diversifier_total) if diversifier_total > 0 else 0.0
        )
    return _weighted_average_panels(
        {name: normalized_panels[name] for name in components["component_id"] if name in normalized_panels},
        weights,
    )


def _date_weighted_average_panels(
    panels: dict[str, pd.DataFrame],
    date_weights: dict[str, pd.Series],
) -> pd.DataFrame:
    if not panels:
        return pd.DataFrame()
    all_index = pd.DatetimeIndex(sorted(set().union(*(panel.index for panel in panels.values()))))
    all_columns = sorted(set().union(*(panel.columns for panel in panels.values())))
    raw_weights = pd.DataFrame(index=all_index)
    for name in panels:
        raw_weights[name] = date_weights[name].reindex(all_index).astype(float)
    normalized_weights = raw_weights.div(raw_weights.abs().sum(axis=1).replace(0.0, np.nan), axis=0)

    numerator = pd.DataFrame(0.0, index=all_index, columns=all_columns)
    denominator = pd.DataFrame(0.0, index=all_index, columns=all_columns)
    for name, panel in panels.items():
        aligned = panel.reindex(index=all_index, columns=all_columns)
        weights = normalized_weights[name]
        weighted = aligned.mul(weights, axis=0)
        valid = aligned.notna() & weights.notna().to_numpy()[:, None]
        numerator = numerator.add(weighted.fillna(0.0), fill_value=0.0)
        denominator = denominator.add(
            pd.DataFrame(
                valid,
                index=all_index,
                columns=all_columns,
            ).mul(weights.abs(), axis=0),
            fill_value=0.0,
        )
    return (numerator / denominator.replace(0.0, np.nan)).replace([np.inf, -np.inf], np.nan)


def _normalize_date_weights(raw_weights: pd.DataFrame, max_weight: float | None = None) -> pd.DataFrame:
    weights = raw_weights.clip(lower=0.0).replace([np.inf, -np.inf], np.nan).fillna(0.0)
    denominator = weights.sum(axis=1).replace(0.0, np.nan)
    weights = weights.div(denominator, axis=0)
    if max_weight is not None:
        weights = weights.clip(upper=max_weight)
    return weights.replace([np.inf, -np.inf], np.nan)


def _alpha_from_normalized_weights(
    panels: dict[str, pd.DataFrame],
    normalized_weights: pd.DataFrame,
) -> pd.DataFrame:
    if not panels:
        return pd.DataFrame()
    all_index = pd.DatetimeIndex(normalized_weights.index)
    all_columns = sorted(set().union(*(panel.columns for panel in panels.values())))
    numerator = pd.DataFrame(0.0, index=all_index, columns=all_columns)
    denominator = pd.DataFrame(0.0, index=all_index, columns=all_columns)
    for component_id, panel in panels.items():
        if component_id not in normalized_weights.columns:
            continue
        aligned = panel.reindex(index=all_index, columns=all_columns)
        weights = normalized_weights[component_id].reindex(all_index).astype(float)
        valid = aligned.notna() & weights.notna().to_numpy()[:, None]
        numerator = numerator.add(aligned.mul(weights, axis=0).fillna(0.0), fill_value=0.0)
        denominator = denominator.add(
            pd.DataFrame(valid, index=all_index, columns=all_columns).mul(weights.abs(), axis=0),
            fill_value=0.0,
        )
    return (numerator / denominator.replace(0.0, np.nan)).replace([np.inf, -np.inf], np.nan)


def _base_weight_series(signal_pool: pd.DataFrame, component_ids: list[str]) -> pd.Series:
    weights = signal_pool.set_index("component_id")["pool_weight_base"].astype(float).reindex(component_ids).fillna(0.0)
    total = weights.sum()
    if total <= 0:
        return pd.Series(1.0 / len(component_ids), index=component_ids) if component_ids else pd.Series(dtype=float)
    return weights / total


def _base_weight_frame(index: pd.Index, base_weights: pd.Series) -> pd.DataFrame:
    return pd.DataFrame(
        np.repeat(base_weights.to_numpy(dtype=float)[None, :], len(index), axis=0),
        index=pd.DatetimeIndex(index),
        columns=base_weights.index,
    )


def _regime_weight_frame(
    index: pd.Index,
    signal_pool: pd.DataFrame,
    base_weights: pd.Series,
    regime_features: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    features = regime_features.copy()
    features["Date"] = pd.to_datetime(features["Date"], errors="coerce")
    features = features.set_index("Date").sort_index()
    raw = _base_weight_frame(index, base_weights)
    match_flags = pd.DataFrame(False, index=pd.DatetimeIndex(index), columns=base_weights.index)
    pool_by_component = signal_pool.set_index("component_id")
    for component_id in base_weights.index:
        column = pool_by_component.at[component_id, "best_regime_column"] if component_id in pool_by_component.index else None
        value = pool_by_component.at[component_id, "best_regime_value"] if component_id in pool_by_component.index else None
        if column in features.columns and pd.notna(value):
            matches = features[column].reindex(index).eq(value).fillna(False)
            match_flags[component_id] = matches.astype(bool)
            raw[component_id] = raw[component_id] * matches.map({True: 1.25, False: 0.75}).astype(float)
        else:
            raw[component_id] = raw[component_id] * 0.75
    return _normalize_date_weights(raw), match_flags


def _cross_sectional_ic_by_date(signal_panel: pd.DataFrame, forward_returns: pd.DataFrame) -> pd.Series:
    signal, forward = signal_panel.align(forward_returns, join="inner", axis=0)
    signal, forward = signal.align(forward, join="inner", axis=1)
    values: list[float] = []
    for date in signal.index:
        paired = pd.concat(
            [signal.loc[date].rename("signal"), forward.loc[date].rename("forward_return")],
            axis=1,
        ).dropna()
        if len(paired) < 3 or paired["signal"].nunique() < 2 or paired["forward_return"].nunique() < 2:
            values.append(np.nan)
        else:
            values.append(float(paired["signal"].corr(paired["forward_return"], method="spearman")))
    return pd.Series(values, index=signal.index)


def _forward_returns(close_prices: pd.DataFrame, horizon: int) -> pd.DataFrame:
    prices = close_prices.copy().apply(pd.to_numeric, errors="coerce")
    return (prices.shift(-int(horizon)) / prices - 1.0).replace([np.inf, -np.inf], np.nan)


def _turnover_control_alpha_panel(
    alpha_panel: pd.DataFrame,
    smoothing_window: int = 10,
    rebalance_frequency: int = 5,
    update_rate: float = 0.10,
) -> pd.DataFrame:
    """Apply trailing-only smoothing and rebalance-date holds to an alpha panel."""
    if alpha_panel.empty:
        return alpha_panel.copy()

    smoothing_window = max(int(smoothing_window), 1)
    rebalance_frequency = max(int(rebalance_frequency), 1)
    update_rate = min(max(float(update_rate), 0.0), 1.0)
    panel = alpha_panel.sort_index().sort_index(axis=1).apply(pd.to_numeric, errors="coerce")
    smoothed = panel.rolling(window=smoothing_window, min_periods=1).mean()
    rebalance_mask = pd.Series(False, index=smoothed.index)
    rebalance_mask.iloc[::rebalance_frequency] = True
    held = pd.DataFrame(np.nan, index=smoothed.index, columns=smoothed.columns)
    previous = pd.Series(np.nan, index=smoothed.columns, dtype=float)
    for date in smoothed.index:
        if bool(rebalance_mask.loc[date]):
            target = smoothed.loc[date]
            if previous.notna().any():
                updated = previous.copy()
                existing = previous.notna() & target.notna()
                updated.loc[existing] = previous.loc[existing] + update_rate * (
                    target.loc[existing] - previous.loc[existing]
                )
                newly_valid = previous.isna() & target.notna()
                updated.loc[newly_valid] = target.loc[newly_valid]
                previous = updated
            else:
                previous = target
        held.loc[date] = previous
    return held.replace([np.inf, -np.inf], np.nan)


def _add_turnover_controlled_v4_alphas(
    alphas: dict[str, pd.DataFrame],
    smoothing_window: int,
    rebalance_frequency: int,
    update_rate: float = 0.10,
    enabled: bool = True,
) -> dict[str, pd.DataFrame]:
    if not enabled:
        return {}

    mapping = {
        ALPHA_DECAY_AWARE_DYNAMIC_V3: ALPHA_DECAY_AWARE_DYNAMIC_V4_SMOOTH,
        ALPHA_REGIME_BLEND_DYNAMIC_V3: ALPHA_REGIME_BLEND_DYNAMIC_V4_SMOOTH,
        ALPHA_ROLLING_IC_DYNAMIC_V3: ALPHA_ROLLING_IC_DYNAMIC_V4_SMOOTH,
        ALPHA_HYBRID_ADAPTIVE_V3: ALPHA_HYBRID_ADAPTIVE_V4_SMOOTH,
    }
    controlled: dict[str, pd.DataFrame] = {}
    for source_alpha, target_alpha in mapping.items():
        if source_alpha in alphas:
            controlled[target_alpha] = zscore_cross_section(
                _turnover_control_alpha_panel(
                    alphas[source_alpha],
                    smoothing_window=smoothing_window,
                    rebalance_frequency=rebalance_frequency,
                    update_rate=update_rate,
                )
            )
    return controlled


def _rolling_ic_weight_frame(
    panels: dict[str, pd.DataFrame],
    signal_pool: pd.DataFrame,
    close_prices: pd.DataFrame,
    base_weights: pd.Series,
    window: int = 252,
    min_periods: int = 126,
    max_weight: float = 0.35,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    index = next(iter(panels.values())).index if panels else pd.Index([])
    raw = pd.DataFrame(index=pd.DatetimeIndex(index), columns=base_weights.index, dtype=float)
    rolling_ic_used = pd.DataFrame(False, index=pd.DatetimeIndex(index), columns=base_weights.index)
    pool_by_component = signal_pool.set_index("component_id")
    fwd_cache: dict[int, pd.DataFrame] = {}
    for component_id in base_weights.index:
        horizon = int(pool_by_component.at[component_id, "horizon"]) if component_id in pool_by_component.index else 20
        if horizon not in fwd_cache:
            fwd_cache[horizon] = _forward_returns(close_prices, horizon)
        ic = _cross_sectional_ic_by_date(panels[component_id], fwd_cache[horizon])
        rolling_ic = ic.rolling(window=window, min_periods=min_periods).mean().shift(1)
        positive_ic = rolling_ic.clip(lower=0.0)
        raw[component_id] = positive_ic.reindex(index)
        rolling_ic_used[component_id] = positive_ic.reindex(index).notna() & positive_ic.reindex(index).gt(0.0)
    normalized = _normalize_date_weights(raw, max_weight=max_weight)
    base_frame = _base_weight_frame(index, base_weights)
    fallback_dates = normalized.sum(axis=1).fillna(0.0).le(0.0)
    normalized.loc[fallback_dates] = base_frame.loc[fallback_dates]
    return normalized, rolling_ic_used


def _weights_to_audit(
    alpha_name: str,
    weights: pd.DataFrame,
    signal_pool: pd.DataFrame,
    weight_method: str,
    regime_match_flags: pd.DataFrame | None = None,
    rolling_ic_used: pd.DataFrame | None = None,
) -> pd.DataFrame:
    if weights.empty:
        return pd.DataFrame()
    pool_lookup = signal_pool.set_index("component_id")
    long = weights.stack(future_stack=True).rename("weight").reset_index()
    long.columns = ["Date", "component_id", "weight"]
    long["alpha_name"] = alpha_name
    long["weight_method"] = weight_method
    long["signal_name"] = long["component_id"].map(pool_lookup["signal_name"])
    long["horizon"] = long["component_id"].map(pool_lookup["horizon"])
    if regime_match_flags is not None and not regime_match_flags.empty:
        regime_long = regime_match_flags.reindex(index=weights.index, columns=weights.columns).stack(future_stack=True)
        long["regime_match_flag"] = regime_long.reset_index(drop=True).astype(float)
    else:
        long["regime_match_flag"] = np.nan
    if rolling_ic_used is not None and not rolling_ic_used.empty:
        rolling_long = rolling_ic_used.reindex(index=weights.index, columns=weights.columns).stack(future_stack=True)
        long["rolling_ic_used"] = rolling_long.reset_index(drop=True).astype(float)
    else:
        long["rolling_ic_used"] = np.nan
    return long[
        [
            "alpha_name",
            "Date",
            "signal_name",
            "horizon",
            "component_id",
            "weight",
            "weight_method",
            "regime_match_flag",
            "rolling_ic_used",
        ]
    ]


def _orthogonal_diversifier_pool(signal_pool: pd.DataFrame) -> pd.DataFrame:
    """Return selected orthogonal diversifier signal rows without core/regime spillover."""
    if signal_pool.empty:
        return signal_pool.copy()
    diversity_group = signal_pool.get("diversity_group", pd.Series("", index=signal_pool.index)).astype(str)
    diversity_tier = signal_pool.get("diversity_candidate_tier", pd.Series("", index=signal_pool.index)).astype(str)
    selected = signal_pool.loc[
        diversity_group.eq("ORTHOGONAL_DIVERSIFIER_SELECTED")
        | diversity_tier.eq("ORTHOGONAL_DIVERSIFIER")
    ].copy()
    if "pool_eligible_flag" in selected.columns:
        selected = selected.loc[selected["pool_eligible_flag"].eq(1)].copy()
    return selected


def _build_orthogonal_diversifier_alpha_v1(
    signal_pool: pd.DataFrame,
    candidate_signals: pd.DataFrame,
    smoothing_window: int,
    rebalance_frequency: int,
    update_rate: float,
    turnover_control_enabled: bool,
) -> tuple[dict[str, pd.DataFrame], pd.DataFrame, dict[str, dict[str, float]]]:
    """Build a standalone orthogonal diversifier sleeve from 03G-selected components only."""
    orthogonal_pool = _orthogonal_diversifier_pool(signal_pool)
    if orthogonal_pool.empty:
        return {}, pd.DataFrame(), {}

    panels = build_zscored_component_signal_panels(orthogonal_pool, candidate_signals)
    component_ids = [component_id for component_id in orthogonal_pool["component_id"].astype(str) if component_id in panels]
    panels = {component_id: panels[component_id] for component_id in component_ids}
    if not panels:
        return {}, pd.DataFrame(), {}

    index = next(iter(panels.values())).index
    weights = _base_weight_frame(index, _base_weight_series(orthogonal_pool, component_ids))
    raw_alpha = zscore_cross_section(_alpha_from_normalized_weights(panels, weights))
    if turnover_control_enabled:
        alpha = _turnover_control_alpha_panel(
            raw_alpha,
            smoothing_window=smoothing_window,
            rebalance_frequency=rebalance_frequency,
            update_rate=update_rate,
        )
    else:
        alpha = raw_alpha

    audit = _weights_to_audit(
        ALPHA_ORTHOGONAL_DIVERSIFIER_V1_SMOOTH,
        weights,
        orthogonal_pool,
        "orthogonal_diversifier_base",
    )
    component_stats = {
        ALPHA_ORTHOGONAL_DIVERSIFIER_V1_SMOOTH: {
            "avg_effective_n_components": float((1.0 / weights.pow(2).sum(axis=1).replace(0.0, np.nan)).mean()),
            "max_component_weight": float(weights.max(axis=1).max()),
        }
    }
    return {ALPHA_ORTHOGONAL_DIVERSIFIER_V1_SMOOTH: alpha}, audit, component_stats


def _component_metric(
    metrics: pd.DataFrame,
    signal_name: str,
    horizon: int,
    column: str,
    default: float,
) -> float:
    if metrics is None or metrics.empty or column not in metrics.columns:
        return default
    matched = metrics.loc[
        metrics.get("signal_name", pd.Series(dtype=str)).astype(str).eq(signal_name)
        & pd.to_numeric(metrics.get("horizon", pd.Series(dtype=float)), errors="coerce").eq(horizon)
    ]
    if matched.empty:
        return default
    value = pd.to_numeric(pd.Series([matched.iloc[0].get(column)]), errors="coerce").iloc[0]
    return float(value) if pd.notna(value) else default


def _component_text_metric(
    metrics: pd.DataFrame,
    signal_name: str,
    horizon: int,
    column: str,
    default: str,
) -> str:
    if metrics is None or metrics.empty or column not in metrics.columns:
        return default
    matched = metrics.loc[
        metrics.get("signal_name", pd.Series(dtype=str)).astype(str).eq(signal_name)
        & pd.to_numeric(metrics.get("horizon", pd.Series(dtype=float)), errors="coerce").eq(horizon)
    ]
    if matched.empty or pd.isna(matched.iloc[0].get(column)):
        return default
    return str(matched.iloc[0].get(column))


def _cap_and_renormalize_weights(raw_weights: dict[str, float], max_weight: float = 0.50) -> dict[str, float]:
    if not raw_weights:
        return {}
    weights = {key: max(float(value), 0.0) for key, value in raw_weights.items()}
    total = sum(weights.values())
    if total <= 0:
        return {}
    weights = {key: value / total for key, value in weights.items()}
    capped: dict[str, float] = {}
    remaining = dict(weights)
    while remaining:
        overweight = {key: value for key, value in remaining.items() if value > max_weight}
        if not overweight:
            capped.update(remaining)
            break
        for key in overweight:
            capped[key] = max_weight
            remaining.pop(key, None)
        remaining_budget = 1.0 - sum(capped.values())
        remaining_total = sum(remaining.values())
        if remaining_total <= 0 or remaining_budget <= 0:
            capped.update({key: 0.0 for key in remaining})
            break
        remaining = {key: value / remaining_total * remaining_budget for key, value in remaining.items()}
    final_total = sum(capped.values())
    return {key: value / final_total for key, value in capped.items() if final_total > 0 and value > 0}


def _build_orthogonal_diversifier_alpha_v2(
    candidate_signals: pd.DataFrame,
    core_alpha_panel: pd.DataFrame,
    eligible_mask: pd.DataFrame | None = None,
    component_metrics: pd.DataFrame | None = None,
    smoothing_window: int = 10,
    rebalance_frequency: int = 5,
    update_rate: float = 0.10,
    turnover_control_enabled: bool = True,
    small_epsilon: float = 1e-6,
) -> tuple[dict[str, pd.DataFrame], pd.DataFrame, dict[str, dict[str, float]], pd.DataFrame]:
    """Build a rule-weighted multi-signal orthogonal sleeve using diagnostics available at 04A time."""
    rows: list[dict[str, object]] = []
    panels: dict[str, pd.DataFrame] = {}
    available_names = set(candidate_signals.get("signal_name", pd.Series(dtype=str)).dropna().astype(str).unique())
    for signal_name, horizon in ORTHOGONAL_DIVERSIFIER_V2_COMPONENTS:
        component_id = f"{signal_name}_h{horizon}"
        if signal_name not in available_names:
            rows.append(
                {
                    "component_id": component_id,
                    "signal_name": signal_name,
                    "horizon": horizon,
                    "included_flag": 0,
                    "exclusion_reason": "missing_candidate_signal_panel",
                }
            )
            continue
        signal_direction = _component_text_metric(component_metrics, signal_name, horizon, "signal_direction", "POSITIVE_EDGE")
        panel = normalize_signal_panel(_pivot_signal_panel(candidate_signals, signal_name), signal_direction)
        smooth_component = _turnover_control_alpha_panel(
            zscore_cross_section(panel),
            smoothing_window=smoothing_window,
            rebalance_frequency=rebalance_frequency,
            update_rate=update_rate,
        )
        aligned_component, aligned_core = smooth_component.align(core_alpha_panel, join="inner", axis=0)
        aligned_component, aligned_core = aligned_component.align(aligned_core, join="inner", axis=1)
        pair = pd.DataFrame(
            {
                "component": aligned_component.to_numpy(dtype=float).ravel(),
                "core": aligned_core.to_numpy(dtype=float).ravel(),
            }
        ).dropna()
        corr_to_core = pair["component"].corr(pair["core"]) if len(pair) >= 2 else np.nan
        if eligible_mask is not None:
            aligned_mask = eligible_mask.reindex(
                index=smooth_component.index,
                columns=smooth_component.columns,
                fill_value=False,
            ).astype(bool)
        else:
            aligned_mask = None
        turnover = compute_alpha_turnover_proxy(smooth_component, eligible_mask=aligned_mask)["turnover_proxy"].dropna()
        turnover_proxy = float(turnover.mean()) if not turnover.empty else np.nan
        mean_ic = _component_metric(component_metrics, signal_name, horizon, "mean_ic", 0.0)
        persistence_ratio = _component_metric(component_metrics, signal_name, horizon, "persistence_ratio", 0.50)
        sign_consistency = _component_metric(component_metrics, signal_name, horizon, "sign_consistency", 0.50)
        if pd.isna(turnover_proxy) or turnover_proxy <= 0:
            denominator_turnover = small_epsilon
        else:
            denominator_turnover = max(turnover_proxy, small_epsilon)
        abs_corr_to_core = abs(float(corr_to_core)) if pd.notna(corr_to_core) else 1.0
        score = (
            max(mean_ic, 0.0)
            * max(persistence_ratio, 0.0)
            * max(sign_consistency, 0.0)
            * max(1.0 - abs_corr_to_core, 0.0)
            / denominator_turnover
        )
        panels[component_id] = panel
        rows.append(
            {
                "component_id": component_id,
                "signal_name": signal_name,
                "horizon": horizon,
                "signal_direction": signal_direction,
                "mean_ic": mean_ic,
                "persistence_ratio": persistence_ratio,
                "sign_consistency": sign_consistency,
                "corr_to_core": corr_to_core,
                "abs_corr_to_core": abs_corr_to_core,
                "turnover_proxy": turnover_proxy,
                "component_score": score,
                "included_flag": int(score > 0),
                "exclusion_reason": "" if score > 0 else "non_positive_rule_score",
            }
        )
    score_table = pd.DataFrame(rows)
    included = score_table.loc[score_table["included_flag"].eq(1)].copy()
    if len(included) < 2:
        score_table["final_component_weight"] = 0.0
        return {}, pd.DataFrame(), {}, score_table

    raw_scores = included.set_index("component_id")["component_score"].astype(float)
    raw_weights = (raw_scores / raw_scores.sum()).to_dict() if raw_scores.sum() > 0 else {}
    weights = _cap_and_renormalize_weights(raw_weights, max_weight=0.50)
    score_table["final_component_weight"] = score_table["component_id"].map(weights).fillna(0.0)

    weighted_panel = _weighted_average_panels(
        {component_id: panels[component_id] for component_id in weights if component_id in panels},
        weights,
    )
    alpha = zscore_cross_section(weighted_panel)
    if turnover_control_enabled:
        alpha = _turnover_control_alpha_panel(
            alpha,
            smoothing_window=smoothing_window,
            rebalance_frequency=rebalance_frequency,
            update_rate=update_rate,
        )

    weight_index = alpha.index
    weight_frame = pd.DataFrame(
        {
            component_id: pd.Series(weight, index=weight_index)
            for component_id, weight in weights.items()
        },
        index=weight_index,
    )
    pool = score_table.loc[score_table["final_component_weight"].gt(0)].copy()
    pool["pool_eligible_flag"] = 1
    audit = _weights_to_audit(
        ALPHA_ORTHOGONAL_DIVERSIFIER_V2_SCORE_WEIGHTED_SMOOTH,
        weight_frame,
        pool,
        "orthogonal_v2_rule_score_weighted",
    )
    component_stats = {
        ALPHA_ORTHOGONAL_DIVERSIFIER_V2_SCORE_WEIGHTED_SMOOTH: {
            "avg_effective_n_components": float((1.0 / weight_frame.pow(2).sum(axis=1).replace(0.0, np.nan)).mean()),
            "max_component_weight": float(weight_frame.max(axis=1).max()),
        }
    }
    return {ALPHA_ORTHOGONAL_DIVERSIFIER_V2_SCORE_WEIGHTED_SMOOTH: alpha}, audit, component_stats, score_table


def build_dynamic_alpha_candidates_v3(
    signal_pool: pd.DataFrame,
    candidate_signals: pd.DataFrame,
    regime_features: pd.DataFrame,
    close_prices: pd.DataFrame,
    eligible_mask: pd.DataFrame | None = None,
    orthogonal_v2_component_metrics: pd.DataFrame | None = None,
    smoothing_window: int = 10,
    rebalance_frequency: int = 5,
    update_rate: float = 0.10,
    turnover_control_enabled: bool = True,
) -> tuple[dict[str, pd.DataFrame], pd.DataFrame, dict[str, float]]:
    """Build raw v3 and turnover-controlled v4 dynamic/adaptive alphas."""
    if signal_pool.empty:
        return {}, pd.DataFrame(), {}
    eligible_pool = signal_pool.loc[signal_pool["pool_eligible_flag"].eq(1)].copy()
    panels = build_zscored_component_signal_panels(eligible_pool, candidate_signals)
    component_ids = [component_id for component_id in eligible_pool["component_id"].astype(str) if component_id in panels]
    panels = {component_id: panels[component_id] for component_id in component_ids}
    if not panels:
        return {}, pd.DataFrame(), {}

    index = next(iter(panels.values())).index
    base_weights = _base_weight_series(eligible_pool, component_ids)
    base_frame = _base_weight_frame(index, base_weights)
    regime_weights, regime_matches = _regime_weight_frame(index, eligible_pool, base_weights, regime_features)
    rolling_weights, rolling_ic_used = _rolling_ic_weight_frame(
        panels,
        eligible_pool,
        close_prices,
        base_weights,
    )

    raw_decay = _alpha_from_normalized_weights(panels, base_frame)
    raw_regime = _alpha_from_normalized_weights(panels, regime_weights)
    raw_rolling = _alpha_from_normalized_weights(panels, rolling_weights)
    raw_hybrid = 0.60 * zscore_cross_section(raw_decay) + 0.25 * zscore_cross_section(raw_rolling) + 0.15 * zscore_cross_section(raw_regime)

    alphas = {
        ALPHA_DECAY_AWARE_DYNAMIC_V3: zscore_cross_section(raw_decay),
        ALPHA_REGIME_BLEND_DYNAMIC_V3: zscore_cross_section(raw_regime),
        ALPHA_ROLLING_IC_DYNAMIC_V3: zscore_cross_section(raw_rolling),
        ALPHA_HYBRID_ADAPTIVE_V3: zscore_cross_section(raw_hybrid),
    }
    alphas.update(
        _add_turnover_controlled_v4_alphas(
            alphas,
            smoothing_window=smoothing_window,
            rebalance_frequency=rebalance_frequency,
            update_rate=update_rate,
            enabled=turnover_control_enabled,
        )
    )
    orthogonal_alphas, orthogonal_audit, orthogonal_component_stats = _build_orthogonal_diversifier_alpha_v1(
        signal_pool=signal_pool,
        candidate_signals=candidate_signals,
        smoothing_window=smoothing_window,
        rebalance_frequency=rebalance_frequency,
        update_rate=update_rate,
        turnover_control_enabled=turnover_control_enabled,
    )
    alphas.update(orthogonal_alphas)
    orthogonal_v2_alphas, orthogonal_v2_audit, orthogonal_v2_component_stats, orthogonal_v2_score_table = (
        _build_orthogonal_diversifier_alpha_v2(
            candidate_signals=candidate_signals,
            core_alpha_panel=alphas[ALPHA_REGIME_BLEND_DYNAMIC_V4_SMOOTH],
            eligible_mask=eligible_mask,
            component_metrics=orthogonal_v2_component_metrics,
            smoothing_window=smoothing_window,
            rebalance_frequency=rebalance_frequency,
            update_rate=update_rate,
            turnover_control_enabled=turnover_control_enabled,
        )
    )
    alphas.update(orthogonal_v2_alphas)

    audit_frames = [
            _weights_to_audit(ALPHA_DECAY_AWARE_DYNAMIC_V3, base_frame, eligible_pool, "decay_aware_base"),
            _weights_to_audit(ALPHA_REGIME_BLEND_DYNAMIC_V3, regime_weights, eligible_pool, "regime_blend", regime_matches),
            _weights_to_audit(ALPHA_ROLLING_IC_DYNAMIC_V3, rolling_weights, eligible_pool, "rolling_ic", rolling_ic_used=rolling_ic_used),
            _weights_to_audit(ALPHA_HYBRID_ADAPTIVE_V3, base_frame, eligible_pool, "hybrid_reference_base"),
    ]
    if not orthogonal_audit.empty:
        audit_frames.append(orthogonal_audit)
    if not orthogonal_v2_audit.empty:
        audit_frames.append(orthogonal_v2_audit)
    audit = pd.concat(audit_frames, ignore_index=True)
    component_stats = {
        alpha_name: {
            "avg_effective_n_components": float((1.0 / weights.pow(2).sum(axis=1).replace(0.0, np.nan)).mean()),
            "max_component_weight": float(weights.max(axis=1).max()),
        }
        for alpha_name, weights in {
            ALPHA_DECAY_AWARE_DYNAMIC_V3: base_frame,
            ALPHA_REGIME_BLEND_DYNAMIC_V3: regime_weights,
            ALPHA_ROLLING_IC_DYNAMIC_V3: rolling_weights,
            ALPHA_HYBRID_ADAPTIVE_V3: base_frame,
            ALPHA_DECAY_AWARE_DYNAMIC_V4_SMOOTH: base_frame,
            ALPHA_REGIME_BLEND_DYNAMIC_V4_SMOOTH: regime_weights,
            ALPHA_ROLLING_IC_DYNAMIC_V4_SMOOTH: rolling_weights,
            ALPHA_HYBRID_ADAPTIVE_V4_SMOOTH: base_frame,
        }.items()
        if alpha_name in alphas
    }
    component_stats.update(orthogonal_component_stats)
    component_stats.update(orthogonal_v2_component_stats)
    if not orthogonal_v2_score_table.empty:
        component_stats[f"{ALPHA_ORTHOGONAL_DIVERSIFIER_V2_SCORE_WEIGHTED_SMOOTH}__component_scores"] = {
            "score_table": orthogonal_v2_score_table.to_json(orient="records")
        }
    return alphas, audit, component_stats


def build_smooth_regime_weighted_alpha_v2(
    normalized_panels: dict[str, pd.DataFrame],
    approved_signals: pd.DataFrame,
    regime_features: pd.DataFrame,
) -> pd.DataFrame:
    features = regime_features.copy()
    features["Date"] = pd.to_datetime(features["Date"], errors="coerce")
    features = features.set_index("Date").sort_index()
    scores = approved_signals.set_index("component_id")["signal_health_score"].astype(float)
    score_total = scores.sum()
    base_weights = (scores / score_total).to_dict() if score_total > 0 else {name: 1.0 for name in normalized_panels}
    date_weights: dict[str, pd.Series] = {}

    for row in approved_signals.itertuples(index=False):
        component_id = str(row.component_id)
        column = getattr(row, "best_regime_column", None)
        value = getattr(row, "best_regime_value", None)
        if column in features.columns and pd.notna(value):
            multiplier = features[column].eq(value).map({True: 1.5, False: 0.75}).astype(float)
        else:
            multiplier = pd.Series(0.75, index=features.index)
        date_weights[component_id] = multiplier * float(base_weights.get(component_id, 0.0))
    return _date_weighted_average_panels(
        {name: normalized_panels[name] for name in approved_signals["component_id"] if name in normalized_panels},
        date_weights,
    )


def _select_persistence_components(watchlist_diversifiers: pd.DataFrame) -> pd.DataFrame:
    if watchlist_diversifiers.empty:
        return watchlist_diversifiers
    preferred = watchlist_diversifiers.loc[
        watchlist_diversifiers["signal_family"].isin(["short_term_reversal", "mean_reversion"])
    ].sort_values(["signal_health_score", "signal_name", "horizon"], ascending=[False, True, True])
    fallback_pool = watchlist_diversifiers.sort_values(
        ["signal_health_score", "signal_name", "horizon"],
        ascending=[False, True, True],
    )

    selected_rows = []
    if not preferred.empty:
        selected_rows.append(preferred.iloc[0])
    else:
        selected_rows.append(fallback_pool.iloc[0])

    non_vol = fallback_pool.loc[~fallback_pool["component_id"].isin([selected_rows[0]["component_id"]])]
    if not non_vol.empty:
        selected_rows.append(non_vol.iloc[0])
    return pd.DataFrame(selected_rows).drop_duplicates("component_id").reset_index(drop=True)


def build_persistence_blend_alpha_v2(
    health_weighted_alpha_v1: pd.DataFrame,
    normalized_panels: dict[str, pd.DataFrame],
    watchlist_diversifiers: pd.DataFrame,
) -> pd.DataFrame:
    selected = _select_persistence_components(watchlist_diversifiers)
    panels = {"__core_health_weighted_v1": health_weighted_alpha_v1}
    weights = {"__core_health_weighted_v1": 0.60 if not selected.empty else 1.0}
    if not selected.empty:
        for row in selected.itertuples(index=False):
            component_id = str(row.component_id)
            if component_id in normalized_panels:
                panels[component_id] = normalized_panels[component_id]
                weights[component_id] = 0.20
    weight_sum = sum(weights.values())
    weights = {name: weight / weight_sum for name, weight in weights.items()}
    return _weighted_average_panels(panels, weights)


def build_alpha_candidates(
    approved_signals: pd.DataFrame,
    candidate_signals: pd.DataFrame,
    regime_features: pd.DataFrame,
    watchlist_diversifiers: pd.DataFrame | None = None,
    signal_pool: pd.DataFrame | None = None,
    close_prices: pd.DataFrame | None = None,
    eligible_mask: pd.DataFrame | None = None,
    orthogonal_v2_component_metrics: pd.DataFrame | None = None,
    smoothing_window: int = 10,
    rebalance_frequency: int = 5,
    update_rate: float = 0.10,
    turnover_control_enabled: bool = True,
) -> tuple[dict[str, pd.DataFrame], dict[str, pd.DataFrame], pd.DataFrame, dict[str, dict[str, float]]]:
    """Build normalized component panels and Phase 4A alpha candidates."""
    if watchlist_diversifiers is None:
        watchlist_diversifiers = pd.DataFrame()
    component_signals = pd.concat([approved_signals, watchlist_diversifiers], ignore_index=True)
    normalized_panels = build_component_signal_panels(component_signals, candidate_signals)
    raw_alphas: dict[str, pd.DataFrame] = {}
    if "component_id" in approved_signals.columns and not approved_signals.empty:
        approved_panels = {
            component_id: normalized_panels[component_id]
            for component_id in approved_signals["component_id"]
            if component_id in normalized_panels
        }
        if approved_panels:
            raw_alphas = {
                ALPHA_EQUAL_WEIGHT: build_equal_weight_alpha(approved_panels),
                ALPHA_HEALTH_WEIGHTED: build_health_weighted_alpha(approved_panels, approved_signals),
                ALPHA_REGIME_AWARE: build_regime_aware_alpha(approved_panels, approved_signals, regime_features),
            }
            raw_alphas[ALPHA_DIVERSIFIED_V2] = build_diversified_alpha_v2(
                normalized_panels,
                approved_signals,
                watchlist_diversifiers,
            )
            raw_alphas[ALPHA_SMOOTH_REGIME_WEIGHTED_V2] = build_smooth_regime_weighted_alpha_v2(
                normalized_panels,
                approved_signals,
                regime_features,
            )
            raw_alphas[ALPHA_PERSISTENCE_BLEND_V2] = build_persistence_blend_alpha_v2(
                zscore_cross_section(raw_alphas[ALPHA_HEALTH_WEIGHTED]),
                normalized_panels,
                watchlist_diversifiers,
            )
    alphas = {alpha_name: zscore_cross_section(panel) for alpha_name, panel in raw_alphas.items()}
    dynamic_weight_audit = pd.DataFrame()
    dynamic_component_stats: dict[str, dict[str, float]] = {}
    if signal_pool is not None and close_prices is not None and not signal_pool.empty:
        dynamic_alphas, dynamic_weight_audit, dynamic_component_stats = build_dynamic_alpha_candidates_v3(
            signal_pool=signal_pool,
            candidate_signals=candidate_signals,
            regime_features=regime_features,
            close_prices=close_prices,
            eligible_mask=eligible_mask,
            orthogonal_v2_component_metrics=orthogonal_v2_component_metrics,
            smoothing_window=smoothing_window,
            rebalance_frequency=rebalance_frequency,
            update_rate=update_rate,
            turnover_control_enabled=turnover_control_enabled,
        )
        alphas.update(dynamic_alphas)
    return alphas, normalized_panels, dynamic_weight_audit, dynamic_component_stats


def build_alpha_construction_metadata(
    alpha_candidates: dict[str, pd.DataFrame],
    approved_signals: pd.DataFrame,
    run_id: str,
    alpha_construction_version: str,
    watchlist_diversifiers: pd.DataFrame | None = None,
    signal_pool: pd.DataFrame | None = None,
    smoothing_window: int | None = None,
    rebalance_frequency: int | None = None,
    update_rate: float | None = None,
    turnover_control_enabled: bool = False,
    dynamic_component_stats: dict[str, dict[str, object]] | None = None,
) -> pd.DataFrame:
    if watchlist_diversifiers is None:
        watchlist_diversifiers = pd.DataFrame()
    if dynamic_component_stats is None:
        dynamic_component_stats = {}
    component_signals = ",".join(approved_signals["signal_name"].astype(str).tolist())
    component_horizons = ",".join(approved_signals["horizon"].astype(int).astype(str).tolist())
    diversifier_signals = ",".join(watchlist_diversifiers.get("signal_name", pd.Series(dtype=str)).astype(str).tolist())
    diversifier_horizons = ",".join(watchlist_diversifiers.get("horizon", pd.Series(dtype=int)).astype(str).tolist())
    diversified_component_signals = ",".join([item for item in [component_signals, diversifier_signals] if item])
    diversified_component_horizons = ",".join([item for item in [component_horizons, diversifier_horizons] if item])
    dynamic_pool = pd.DataFrame()
    if signal_pool is not None and not signal_pool.empty and "pool_eligible_flag" in signal_pool.columns:
        dynamic_pool = signal_pool.loc[signal_pool["pool_eligible_flag"].eq(1)].copy()
    orthogonal_pool = _orthogonal_diversifier_pool(signal_pool if signal_pool is not None else pd.DataFrame())

    def _join_values(frame: pd.DataFrame, column: str, as_int: bool = False) -> str:
        if frame.empty or column not in frame.columns:
            return ""
        values = frame[column].dropna()
        if as_int:
            values = pd.to_numeric(values, errors="coerce").dropna().astype(int)
        return ",".join(values.astype(str).tolist())

    dynamic_component_signals = (
        ",".join(dynamic_pool.get("signal_name", pd.Series(dtype=str)).astype(str).tolist())
        if not dynamic_pool.empty
        else diversified_component_signals
    )
    dynamic_component_horizons = (
        ",".join(dynamic_pool.get("horizon", pd.Series(dtype=int)).astype(int).astype(str).tolist())
        if not dynamic_pool.empty
        else diversified_component_horizons
    )
    dynamic_diversity_groups = _join_values(dynamic_pool, "diversity_group")
    orthogonal_component_signals = _join_values(orthogonal_pool, "signal_name")
    orthogonal_component_horizons = _join_values(orthogonal_pool, "horizon", as_int=True)
    orthogonal_diversity_groups = _join_values(orthogonal_pool, "diversity_group")
    orthogonal_versions = _join_values(orthogonal_pool, "orthogonal_version")
    v2_score_table = pd.DataFrame()
    v2_score_json = dynamic_component_stats.get(
        f"{ALPHA_ORTHOGONAL_DIVERSIFIER_V2_SCORE_WEIGHTED_SMOOTH}__component_scores",
        {},
    ).get("score_table")
    if v2_score_json:
        try:
            v2_score_table = pd.read_json(v2_score_json)
        except ValueError:
            v2_score_table = pd.DataFrame()
    v2_included = v2_score_table.loc[
        pd.to_numeric(v2_score_table.get("final_component_weight", pd.Series(dtype=float)), errors="coerce").gt(0)
    ].copy() if not v2_score_table.empty else pd.DataFrame()
    v2_component_signals = _join_values(v2_included, "signal_name")
    v2_component_horizons = _join_values(v2_included, "horizon", as_int=True)
    v2_scores_json = (
        json.dumps(dict(zip(v2_score_table["component_id"], v2_score_table["component_score"])), sort_keys=True)
        if not v2_score_table.empty and {"component_id", "component_score"}.issubset(v2_score_table.columns)
        else "{}"
    )
    v2_weights_json = (
        json.dumps(dict(zip(v2_score_table["component_id"], v2_score_table["final_component_weight"])), sort_keys=True)
        if not v2_score_table.empty and {"component_id", "final_component_weight"}.issubset(v2_score_table.columns)
        else "{}"
    )
    v2_corr_json = (
        json.dumps(dict(zip(v2_score_table["component_id"], v2_score_table["abs_corr_to_core"])), sort_keys=True)
        if not v2_score_table.empty and {"component_id", "abs_corr_to_core"}.issubset(v2_score_table.columns)
        else "{}"
    )
    rows = [
        {
            "alpha_name": ALPHA_EQUAL_WEIGHT,
            "component_signals": component_signals,
            "component_horizons": component_horizons,
            "weighting_method": "equal_weight",
            "direction_adjusted": 1,
            "regime_aware": 0,
            "notes": "Equal weight across approved signal-horizon research components.",
        },
        {
            "alpha_name": ALPHA_HEALTH_WEIGHTED,
            "component_signals": component_signals,
            "component_horizons": component_horizons,
            "weighting_method": "signal_health_score_normalized",
            "direction_adjusted": 1,
            "regime_aware": 0,
            "notes": "Weights proportional to Notebook 3E signal health score.",
        },
        {
            "alpha_name": ALPHA_REGIME_AWARE,
            "component_signals": component_signals,
            "component_horizons": component_horizons,
            "weighting_method": "signal_health_score_normalized_when_best_regime_active",
            "direction_adjusted": 1,
            "regime_aware": 1,
            "notes": "Component active only when Notebook 3D best regime label is active.",
        },
        {
            "alpha_name": ALPHA_DIVERSIFIED_V2,
            "component_signals": diversified_component_signals,
            "component_horizons": diversified_component_horizons,
            "weighting_method": "70pct_approved_health_weighted_30pct_watchlist_diversifiers",
            "direction_adjusted": 1,
            "regime_aware": 0,
            "notes": "Adds up to three non-volatility watchlist diversifiers with fixed 30% allocation.",
        },
        {
            "alpha_name": ALPHA_SMOOTH_REGIME_WEIGHTED_V2,
            "component_signals": component_signals,
            "component_horizons": component_horizons,
            "weighting_method": "health_weighted_with_1p5_best_regime_0p75_other_regime",
            "direction_adjusted": 1,
            "regime_aware": 1,
            "notes": "Smooth regime weights without binary deactivation outside best regime.",
        },
        {
            "alpha_name": ALPHA_PERSISTENCE_BLEND_V2,
            "component_signals": diversified_component_signals,
            "component_horizons": diversified_component_horizons,
            "weighting_method": "60pct_health_weighted_core_20pct_reversal_mean_reversion_20pct_non_vol_watchlist",
            "direction_adjusted": 1,
            "regime_aware": 0,
            "notes": "Blends strong core alpha with stabilizing watchlist diversifiers.",
        },
        {
            "alpha_name": ALPHA_DECAY_AWARE_DYNAMIC_V3,
            "component_signals": dynamic_component_signals,
            "component_horizons": dynamic_component_horizons,
            "weighting_method": "health_x_sign_stability_x_decay_multiplier",
            "direction_adjusted": 1,
            "regime_aware": 0,
            "notes": "Dynamic v3 base alpha using explicit signal pool and decay-aware static weights.",
            "alpha_sleeve": SLEEVE_DECAY_STABILITY,
        },
        {
            "alpha_name": ALPHA_REGIME_BLEND_DYNAMIC_V3,
            "component_signals": dynamic_component_signals,
            "component_horizons": dynamic_component_horizons,
            "weighting_method": "decay_aware_base_tilted_1p25_best_regime_0p75_other_regime",
            "direction_adjusted": 1,
            "regime_aware": 1,
            "notes": "Dynamic v3 regime blend tilts but does not deactivate components.",
            "alpha_sleeve": SLEEVE_CORE_REGIME,
        },
        {
            "alpha_name": ALPHA_ROLLING_IC_DYNAMIC_V3,
            "component_signals": dynamic_component_signals,
            "component_horizons": dynamic_component_horizons,
            "weighting_method": "trailing_252d_ic_shifted_1d_positive_only_capped_35pct",
            "direction_adjusted": 1,
            "regime_aware": 0,
            "notes": "Dynamic v3 adaptive weights from trailing realized cross-sectional IC history only.",
            "alpha_sleeve": SLEEVE_CORE_REGIME,
        },
        {
            "alpha_name": ALPHA_HYBRID_ADAPTIVE_V3,
            "component_signals": dynamic_component_signals,
            "component_horizons": dynamic_component_horizons,
            "weighting_method": "60pct_decay_aware_25pct_rolling_ic_15pct_regime_blend",
            "direction_adjusted": 1,
            "regime_aware": 1,
            "notes": "Hybrid adaptive v3 blend of stable base, rolling IC adaptation, and regime tilt.",
            "alpha_sleeve": SLEEVE_CORE_REGIME,
        },
        {
            "alpha_name": ALPHA_DECAY_AWARE_DYNAMIC_V4_SMOOTH,
            "component_signals": dynamic_component_signals,
            "component_horizons": dynamic_component_horizons,
            "weighting_method": "v3_decay_aware_alpha_trailing_smooth_rebalance_hold",
            "direction_adjusted": 1,
            "regime_aware": 0,
            "notes": "Turnover-controlled v4 variant of raw decay-aware dynamic v3 alpha.",
            "alpha_sleeve": SLEEVE_DECAY_STABILITY,
        },
        {
            "alpha_name": ALPHA_REGIME_BLEND_DYNAMIC_V4_SMOOTH,
            "component_signals": dynamic_component_signals,
            "component_horizons": dynamic_component_horizons,
            "weighting_method": "v3_regime_blend_alpha_trailing_smooth_rebalance_hold",
            "direction_adjusted": 1,
            "regime_aware": 1,
            "notes": "Turnover-controlled v4 variant of raw regime-blend dynamic v3 alpha.",
            "alpha_sleeve": SLEEVE_CORE_REGIME,
        },
        {
            "alpha_name": ALPHA_ROLLING_IC_DYNAMIC_V4_SMOOTH,
            "component_signals": dynamic_component_signals,
            "component_horizons": dynamic_component_horizons,
            "weighting_method": "v3_rolling_ic_alpha_trailing_smooth_rebalance_hold",
            "direction_adjusted": 1,
            "regime_aware": 0,
            "notes": "Turnover-controlled v4 variant of raw rolling-IC dynamic v3 alpha.",
            "alpha_sleeve": SLEEVE_CORE_REGIME,
        },
        {
            "alpha_name": ALPHA_HYBRID_ADAPTIVE_V4_SMOOTH,
            "component_signals": dynamic_component_signals,
            "component_horizons": dynamic_component_horizons,
            "weighting_method": "v3_hybrid_alpha_trailing_smooth_rebalance_hold",
            "direction_adjusted": 1,
            "regime_aware": 1,
            "notes": "Turnover-controlled v4 variant of raw hybrid adaptive dynamic v3 alpha.",
            "alpha_sleeve": SLEEVE_CORE_REGIME,
        },
        {
            "alpha_name": ALPHA_ORTHOGONAL_DIVERSIFIER_V1_SMOOTH,
            "component_signals": orthogonal_component_signals,
            "component_horizons": orthogonal_component_horizons,
            "weighting_method": "orthogonal_diversifier_selected_trailing_smooth_rebalance_hold",
            "direction_adjusted": 1,
            "regime_aware": 0,
            "notes": "Standalone turnover-controlled sleeve from 03G orthogonal diversifier-selected signals only.",
            "alpha_sleeve": SLEEVE_ORTHOGONAL_DIVERSIFIER,
        },
        {
            "alpha_name": ALPHA_ORTHOGONAL_DIVERSIFIER_V2_SCORE_WEIGHTED_SMOOTH,
            "component_signals": v2_component_signals,
            "component_horizons": v2_component_horizons,
            "weighting_method": "orthogonal_v2_rule_based_score_weighted_trailing_smooth_rebalance_hold",
            "direction_adjusted": 1,
            "regime_aware": 0,
            "notes": "Standalone v2 orthogonal diversifier sleeve using rule-based diagnostic scores and capped weights.",
            "alpha_sleeve": SLEEVE_ORTHOGONAL_DIVERSIFIER,
            "sleeve_version": "v2_score_weighted",
            "component_weight_method": "rule_based_score",
            "component_scores_json": v2_scores_json,
            "component_weights_json": v2_weights_json,
            "abs_corr_to_core_json": v2_corr_json,
        },
    ]
    metadata = pd.DataFrame(rows)
    metadata = metadata.loc[metadata["alpha_name"].isin(alpha_candidates.keys())].copy()
    fallback_sleeve = pd.Series(
        np.where(
            metadata["alpha_name"].astype(str).str.contains("decay|persistence|stability", case=False, regex=True),
            SLEEVE_DECAY_STABILITY,
            SLEEVE_CORE_REGIME,
        ),
        index=metadata.index,
    )
    metadata["alpha_sleeve"] = metadata.get("alpha_sleeve", pd.Series(pd.NA, index=metadata.index)).fillna(fallback_sleeve)
    metadata["source_signal_names"] = metadata["component_signals"]
    metadata["source_signal_horizons"] = metadata["component_horizons"]
    for column in ["sleeve_version", "component_weight_method", "component_scores_json", "component_weights_json", "abs_corr_to_core_json"]:
        if column not in metadata.columns:
            metadata[column] = pd.NA
    metadata["source_diversity_groups"] = np.where(
        metadata["alpha_name"].eq(ALPHA_ORTHOGONAL_DIVERSIFIER_V1_SMOOTH),
        orthogonal_diversity_groups,
        np.where(
            metadata["alpha_name"].eq(ALPHA_ORTHOGONAL_DIVERSIFIER_V2_SCORE_WEIGHTED_SMOOTH),
            "RULE_BASED_ORTHOGONAL_CANDIDATE",
            dynamic_diversity_groups,
        ),
    )
    metadata["source_orthogonal_version"] = np.where(
        metadata["alpha_name"].eq(ALPHA_ORTHOGONAL_DIVERSIFIER_V1_SMOOTH),
        orthogonal_versions,
        np.where(
            metadata["alpha_name"].eq(ALPHA_ORTHOGONAL_DIVERSIFIER_V2_SCORE_WEIGHTED_SMOOTH),
            "v2_rule_based_candidate_screen",
            pd.NA,
        ),
    )
    metadata["smoothing_window"] = np.where(
        metadata["alpha_name"].astype(str).str.contains(
            "_v4_smooth|orthogonal_diversifier_v1_smooth|orthogonal_diversifier_v2_score_weighted_smooth",
            regex=True,
        ),
        smoothing_window,
        pd.NA,
    )
    metadata["rebalance_frequency"] = np.where(
        metadata["alpha_name"].astype(str).str.contains(
            "_v4_smooth|orthogonal_diversifier_v1_smooth|orthogonal_diversifier_v2_score_weighted_smooth",
            regex=True,
        ),
        rebalance_frequency,
        pd.NA,
    )
    smooth_mask = metadata["alpha_name"].astype(str).str.contains(
        "_v4_smooth|orthogonal_diversifier_v1_smooth|orthogonal_diversifier_v2_score_weighted_smooth",
        regex=True,
    )
    metadata["turnover_control_enabled"] = smooth_mask & bool(turnover_control_enabled)
    metadata["turnover_control_update_rate"] = np.where(
        smooth_mask,
        update_rate,
        pd.NA,
    )
    metadata["source_alpha_version"] = np.where(
        metadata["alpha_name"].eq(ALPHA_ORTHOGONAL_DIVERSIFIER_V2_SCORE_WEIGHTED_SMOOTH),
        "v2/orthogonal_score_weighted_smooth",
        np.where(
        metadata["alpha_name"].eq(ALPHA_ORTHOGONAL_DIVERSIFIER_V1_SMOOTH),
        "v1/orthogonal_smooth",
        np.where(
        metadata["alpha_name"].astype(str).str.contains("_v4_smooth"),
        "v4/smooth",
        np.where(metadata["alpha_name"].astype(str).str.contains("_v3"), "v3/raw", "legacy"),
        ),
        ),
    )
    metadata["run_id"] = run_id
    metadata["alpha_construction_version"] = alpha_construction_version
    return metadata


def _quality_status(
    finite_pct: float,
    max_abs_alpha: float | None = None,
    avg_turnover_proxy: float | None = None,
    dynamic_alpha_flag: int = 0,
) -> str:
    if dynamic_alpha_flag:
        if finite_pct >= 0.90 and (pd.isna(max_abs_alpha) or max_abs_alpha <= 3.0) and (
            pd.isna(avg_turnover_proxy) or avg_turnover_proxy < 2.50
        ):
            return "APPROVED_FOR_ALPHA_VALIDATION"
        return "REJECTED_ALPHA_CONSTRUCTION"
    if finite_pct >= 0.85:
        return "APPROVED_FOR_ALPHA_VALIDATION"
    if finite_pct >= 0.70:
        return "WATCHLIST_ALPHA_CONSTRUCTION"
    return "REJECTED_ALPHA_CONSTRUCTION"


def build_alpha_construction_quality(
    alpha_candidates: dict[str, pd.DataFrame],
    run_id: str,
    alpha_construction_version: str,
    eligible_mask: pd.DataFrame | None = None,
) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for alpha_name, panel in alpha_candidates.items():
        values = panel.to_numpy(dtype=float)
        finite = np.isfinite(values)
        if eligible_mask is not None:
            aligned_mask = eligible_mask.reindex(index=panel.index, columns=panel.columns, fill_value=False).astype(bool)
            eligible_values = aligned_mask.to_numpy(dtype=bool)
        else:
            aligned_mask = None
            eligible_values = np.ones_like(finite, dtype=bool)
        denominator = int(eligible_values.sum())
        finite_eligible = finite & eligible_values
        finite_pct = float(finite_eligible.sum() / denominator) if denominator else 0.0
        finite_values = values[finite_eligible]
        max_abs_alpha = float(np.nanmax(np.abs(finite_values))) if finite_values.size else np.nan
        turnover = compute_alpha_turnover_proxy(panel, eligible_mask=aligned_mask)["turnover_proxy"].dropna()
        avg_turnover_proxy = float(turnover.mean()) if not turnover.empty else np.nan
        dynamic_alpha_flag = int(
            str(alpha_name)
            in {
                ALPHA_DECAY_AWARE_DYNAMIC_V3,
                ALPHA_REGIME_BLEND_DYNAMIC_V3,
                ALPHA_ROLLING_IC_DYNAMIC_V3,
                ALPHA_HYBRID_ADAPTIVE_V3,
                ALPHA_DECAY_AWARE_DYNAMIC_V4_SMOOTH,
                ALPHA_REGIME_BLEND_DYNAMIC_V4_SMOOTH,
                ALPHA_ROLLING_IC_DYNAMIC_V4_SMOOTH,
                ALPHA_HYBRID_ADAPTIVE_V4_SMOOTH,
                ALPHA_ORTHOGONAL_DIVERSIFIER_V1_SMOOTH,
                ALPHA_ORTHOGONAL_DIVERSIFIER_V2_SCORE_WEIGHTED_SMOOTH,
            }
        )
        valid_dates = panel.index[pd.Series(finite_eligible.any(axis=1), index=panel.index)]
        status = _quality_status(
            finite_pct,
            max_abs_alpha=max_abs_alpha,
            avg_turnover_proxy=avg_turnover_proxy,
            dynamic_alpha_flag=dynamic_alpha_flag,
        )
        notes = (
            "Passes construction coverage, scale, and turnover checks."
            if status == "APPROVED_FOR_ALPHA_VALIDATION"
            else "Fails construction coverage, scale, or turnover checks."
        )
        rows.append(
            {
                "alpha_name": alpha_name,
                "finite_pct": finite_pct,
                "missing_pct": 1.0 - finite_pct,
                "max_abs_alpha": max_abs_alpha,
                "avg_turnover_proxy": avg_turnover_proxy,
                "n_dates": int(panel.shape[0]),
                "n_tickers": int(panel.shape[1]),
                "first_valid_date": valid_dates.min() if len(valid_dates) else pd.NaT,
                "last_valid_date": valid_dates.max() if len(valid_dates) else pd.NaT,
                "status": status,
                "quality_notes": notes,
                "run_id": run_id,
                "alpha_construction_version": alpha_construction_version,
            }
        )
    return pd.DataFrame(rows)


def compute_alpha_turnover_proxy(
    alpha_panel: pd.DataFrame,
    eligible_mask: pd.DataFrame | None = None,
) -> pd.DataFrame:
    """Compute a simple daily rank-based turnover proxy for an alpha panel."""
    panel = alpha_panel.copy()
    if eligible_mask is not None:
        panel = panel.where(eligible_mask.reindex(index=panel.index, columns=panel.columns, fill_value=False).astype(bool))
    centered_ranks = panel.rank(axis=1, pct=True) - 0.5
    turnover = centered_ranks.diff().abs().sum(axis=1, min_count=1) / 2.0
    return pd.DataFrame({"turnover_proxy": turnover})


def build_alpha_construction_diagnostics(
    alpha_panels: dict[str, pd.DataFrame],
    run_id: str | None = None,
    alpha_construction_version: str | None = None,
    dynamic_component_stats: dict[str, dict[str, float]] | None = None,
    eligible_mask: pd.DataFrame | None = None,
) -> pd.DataFrame:
    """Build alpha scale and turnover diagnostics for constructed alpha panels."""
    if dynamic_component_stats is None:
        dynamic_component_stats = {}
    rows: list[dict[str, object]] = []
    for alpha_name, panel in alpha_panels.items():
        values = panel.to_numpy(dtype=float)
        finite = np.isfinite(values)
        if eligible_mask is not None:
            aligned_mask = eligible_mask.reindex(index=panel.index, columns=panel.columns, fill_value=False).astype(bool)
            eligible_values = aligned_mask.to_numpy(dtype=bool)
        else:
            aligned_mask = None
            eligible_values = np.ones_like(finite, dtype=bool)
        denominator = int(eligible_values.sum())
        finite_eligible = finite & eligible_values
        finite_values = values[finite_eligible]
        turnover = compute_alpha_turnover_proxy(panel, eligible_mask=aligned_mask)["turnover_proxy"].dropna()
        avg_turnover_proxy = float(turnover.mean()) if not turnover.empty else np.nan
        if pd.isna(avg_turnover_proxy):
            turnover_risk_flag = np.nan
        elif avg_turnover_proxy < 1.75:
            turnover_risk_flag = "LOW_TURNOVER_RISK"
        elif avg_turnover_proxy < 2.50:
            turnover_risk_flag = "MODERATE_TURNOVER_RISK"
        else:
            turnover_risk_flag = "HIGH_TURNOVER_RISK"
        rows.append(
            {
                "alpha_name": alpha_name,
                "mean_abs_alpha": float(np.nanmean(np.abs(finite_values))) if finite_values.size else np.nan,
                "alpha_std": float(np.nanstd(finite_values, ddof=1)) if finite_values.size > 1 else np.nan,
                "max_abs_alpha": float(np.nanmax(np.abs(finite_values))) if finite_values.size else np.nan,
                "avg_turnover_proxy": avg_turnover_proxy,
                "median_turnover_proxy": float(turnover.median()) if not turnover.empty else np.nan,
                "max_turnover_proxy": float(turnover.max()) if not turnover.empty else np.nan,
                "turnover_risk_flag": turnover_risk_flag,
                "finite_pct": float(finite_eligible.sum() / denominator) if denominator else 0.0,
                "n_dates": int(panel.shape[0]),
                "n_tickers": int(panel.shape[1]),
                "dynamic_alpha_flag": int(
                    str(alpha_name)
                    in {
                        ALPHA_DECAY_AWARE_DYNAMIC_V3,
                        ALPHA_REGIME_BLEND_DYNAMIC_V3,
                        ALPHA_ROLLING_IC_DYNAMIC_V3,
                        ALPHA_HYBRID_ADAPTIVE_V3,
                        ALPHA_DECAY_AWARE_DYNAMIC_V4_SMOOTH,
                        ALPHA_REGIME_BLEND_DYNAMIC_V4_SMOOTH,
                        ALPHA_ROLLING_IC_DYNAMIC_V4_SMOOTH,
                        ALPHA_HYBRID_ADAPTIVE_V4_SMOOTH,
                    }
                ),
                "avg_effective_n_components": dynamic_component_stats.get(alpha_name, {}).get(
                    "avg_effective_n_components", np.nan
                ),
                "max_component_weight": dynamic_component_stats.get(alpha_name, {}).get(
                    "max_component_weight", np.nan
                ),
                "run_id": run_id,
                "alpha_construction_version": alpha_construction_version,
            }
        )
    return pd.DataFrame(rows)


def build_alpha_correlation_matrix(
    alpha_panels: dict[str, pd.DataFrame],
    run_id: str | None = None,
    alpha_construction_version: str | None = None,
) -> pd.DataFrame:
    """Build long-form pairwise alpha correlations using overlapping flattened values."""
    rows: list[dict[str, object]] = []
    names = list(alpha_panels.keys())
    for name_1 in names:
        panel_1 = alpha_panels[name_1]
        for name_2 in names:
            panel_2 = alpha_panels[name_2]
            aligned_1, aligned_2 = panel_1.align(panel_2, join="inner", axis=0)
            aligned_1, aligned_2 = aligned_1.align(aligned_2, join="inner", axis=1)
            pair = pd.DataFrame(
                {
                    "alpha_1": aligned_1.to_numpy(dtype=float).ravel(),
                    "alpha_2": aligned_2.to_numpy(dtype=float).ravel(),
                }
            ).dropna()
            correlation = pair["alpha_1"].corr(pair["alpha_2"]) if len(pair) >= 2 else np.nan
            rows.append(
                {
                    "alpha_name_1": name_1,
                    "alpha_name_2": name_2,
                    "correlation": float(correlation) if not pd.isna(correlation) else np.nan,
                    "run_id": run_id,
                    "alpha_construction_version": alpha_construction_version,
                }
            )
    return pd.DataFrame(rows)


__all__ = [
    "ALPHA_EQUAL_WEIGHT",
    "ALPHA_HEALTH_WEIGHTED",
    "ALPHA_REGIME_AWARE",
    "ALPHA_DIVERSIFIED_V2",
    "ALPHA_SMOOTH_REGIME_WEIGHTED_V2",
    "ALPHA_PERSISTENCE_BLEND_V2",
    "ALPHA_DECAY_AWARE_DYNAMIC_V3",
    "ALPHA_REGIME_BLEND_DYNAMIC_V3",
    "ALPHA_ROLLING_IC_DYNAMIC_V3",
    "ALPHA_HYBRID_ADAPTIVE_V3",
    "ALPHA_DECAY_AWARE_DYNAMIC_V4_SMOOTH",
    "ALPHA_REGIME_BLEND_DYNAMIC_V4_SMOOTH",
    "ALPHA_ROLLING_IC_DYNAMIC_V4_SMOOTH",
    "ALPHA_HYBRID_ADAPTIVE_V4_SMOOTH",
    "ALPHA_ORTHOGONAL_DIVERSIFIER_V1_SMOOTH",
    "ALPHA_ORTHOGONAL_DIVERSIFIER_V2_SCORE_WEIGHTED_SMOOTH",
    "build_alpha_candidates",
    "build_alpha_construction_diagnostics",
    "build_alpha_construction_metadata",
    "build_alpha_construction_quality",
    "build_alpha_correlation_matrix",
    "build_component_signal_panels",
    "build_alpha_signal_pool",
    "build_dynamic_alpha_candidates_v3",
    "build_dynamic_universe_eligibility_mask",
    "build_normalized_signal_panels",
    "build_zscored_component_signal_panels",
    "compute_alpha_turnover_proxy",
    "get_approved_alpha_research_signals",
    "get_watchlist_diversifier_signals",
    "load_candidate_signals_for_names",
    "load_alpha_construction_inputs",
    "zscore_cross_section",
]
