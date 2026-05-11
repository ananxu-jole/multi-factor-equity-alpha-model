from __future__ import annotations

import sqlite3
from pathlib import Path

import numpy as np
import pandas as pd

from src.db import ensure_candidate_signal_indexes
from src.run_config import make_run_id, make_run_timestamp
from src.run_config import get_sqlite_db_path
from src.scoring.diversity_storage import save_signal_diversity_outputs


APPROVED_FOR_ALPHA_RESEARCH = "APPROVED_FOR_ALPHA_RESEARCH"
WATCHLIST_ALPHA_RESEARCH = "WATCHLIST_ALPHA_RESEARCH"
POSITIVE_EDGE = "POSITIVE_EDGE"
NEGATIVE_EDGE_REVERSE_SIGNAL = "NEGATIVE_EDGE_REVERSE_SIGNAL"
CORE_APPROVED = "CORE_APPROVED"
ORTHOGONAL_DIVERSIFIER = "ORTHOGONAL_DIVERSIFIER"
ORTHOGONAL_WATCHLIST_TEST = "ORTHOGONAL_WATCHLIST_TEST"
ORTHOGONAL_GENERATED = "orthogonal_generated"
ORTHOGONAL_DIVERSIFIER_VERSION = "phase2_orthogonal_signals_v2"
DIVERSITY_VERSION = "phase2_signal_diversity_v1"
CORRELATION_THRESHOLD = 0.85
MIN_SELECTED = 3
INCLUDE_WATCHLIST = False
INCLUDE_ORTHOGONAL_DIVERSIFIERS = True
ORTHOGONAL_DIVERSIFIER_MIN_HEALTH_SCORE = 60
ORTHOGONAL_DIVERSIFIER_MIN_PASS_RATE = 0.60
REQUIRED_INPUT_TABLES = (
    "signal_health_score_current",
    "signal_reproducibility_gate_current",
    "candidate_signals_current",
)


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


def readback_sql(
    query: str,
    conn: sqlite3.Connection,
    params: list[object] | tuple[object, ...] | None = None,
    **kwargs: object,
) -> pd.DataFrame:
    """Guard diagnostic readbacks from accidental full candidate signal loads."""
    normalized = " ".join(query.lower().split())
    reads_candidate_signals = (
        "from candidate_signals_current" in normalized
        or 'from "candidate_signals_current"' in normalized
    )
    has_signal_filter = "where" in normalized and "signal_name" in normalized
    is_aggregate_count = "count(" in normalized and "group by" in normalized
    if reads_candidate_signals and not has_signal_filter and not is_aggregate_count:
        raise ValueError(
            "Unsafe 03G readback query blocked: candidate_signals_current reads must "
            "filter by signal_name, or be aggregate COUNT/GROUP BY diagnostics."
        )
    return pd.read_sql_query(query, conn, params=params, **kwargs)


def ensure_signal_diversity_indexes(db_path: str | Path | None = None) -> pd.DataFrame:
    """Create/confirm indexes used by 03G candidate-signal diagnostics."""
    resolved_db_path = Path(db_path) if db_path is not None else get_sqlite_db_path()
    candidate_signal_indexes = ensure_candidate_signal_indexes(resolved_db_path)
    with sqlite3.connect(resolved_db_path) as conn:
        conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_signal_best_horizon_current_signal
            ON signal_best_horizon_current(signal_name)
            """
        )
        conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_candidate_signal_quality_gate_current_signal
            ON candidate_signal_quality_gate_current(signal_name)
            """
        )
        conn.commit()
    return candidate_signal_indexes


def load_candidate_best_horizon_gap(db_path: str | Path | None = None) -> pd.DataFrame:
    """Find candidate signals with no best-horizon row using SQL aggregation only."""
    resolved_db_path = Path(db_path) if db_path is not None else get_sqlite_db_path()
    ensure_signal_diversity_indexes(resolved_db_path)
    with sqlite3.connect(resolved_db_path) as conn:
        return readback_sql(
            """
            WITH candidate_signal_counts AS (
                SELECT
                    signal_name,
                    COUNT(*) AS candidate_rows,
                    COUNT(DISTINCT Date) AS n_dates
                FROM candidate_signals_current
                GROUP BY signal_name
            ),
            best_horizon_signals AS (
                SELECT DISTINCT signal_name
                FROM signal_best_horizon_current
            )
            SELECT
                c.signal_name,
                COALESCE(q.status, 'MISSING_QUALITY_GATE') AS quality_gate_status,
                q.missing_pct,
                q.finite_pct,
                c.candidate_rows,
                c.n_dates,
                CASE WHEN b.signal_name IS NULL THEN 0 ELSE 1 END AS best_horizon_rows
            FROM candidate_signal_counts c
            LEFT JOIN best_horizon_signals b
                ON b.signal_name = c.signal_name
            LEFT JOIN candidate_signal_quality_gate_current q
                ON q.signal_name = c.signal_name
            WHERE b.signal_name IS NULL
            ORDER BY quality_gate_status, c.signal_name
            """,
            conn,
        )


def load_signal_diversity_inputs(db_path: str | Path | None = None) -> dict[str, pd.DataFrame]:
    """Load current health and reproducibility inputs for signal diversity analysis."""
    return {
        "health": _load_table("signal_health_score_current", db_path),
        "reproducibility_gate": _load_table("signal_reproducibility_gate_current", db_path),
    }


def build_diversity_candidate_table(
    health: pd.DataFrame,
    reproducibility_gate: pd.DataFrame,
    include_watchlist: bool = False,
    include_orthogonal_diversifiers: bool = False,
    orthogonal_diversifier_version: str = ORTHOGONAL_DIVERSIFIER_VERSION,
    orthogonal_diversifier_min_health_score: float = 60.0,
    orthogonal_diversifier_min_pass_rate: float = 0.60,
) -> pd.DataFrame:
    """Join health and reproducibility evidence and mark eligible diversity candidates."""
    key_columns = ["signal_name", "horizon"]
    candidates = reproducibility_gate.copy()
    candidates["horizon"] = pd.to_numeric(candidates["horizon"], errors="coerce").astype("Int64")
    health_join = health.copy()
    health_join["horizon"] = pd.to_numeric(health_join["horizon"], errors="coerce").astype("Int64")
    keep_health_columns = [
        column
        for column in [
            "signal_name",
            "horizon",
            "signal_direction",
            "signal_strength",
            "recommended_use",
            "regime_fragility_flag",
            "decay_risk_flag",
            "scoring_status",
            "decay_status",
        ]
        if column in health_join.columns
    ]
    joined = candidates.merge(
        health_join[keep_health_columns].drop_duplicates(key_columns),
        on=key_columns,
        how="left",
    )
    for column in ["signal_health_score", "pass_rate"]:
        if column not in joined.columns:
            joined[column] = np.nan
        joined[column] = pd.to_numeric(joined[column], errors="coerce")

    core_mask = joined["final_research_gate"].eq(APPROVED_FOR_ALPHA_RESEARCH)
    broad_watchlist_mask = (
        joined["final_research_gate"].eq(WATCHLIST_ALPHA_RESEARCH)
        if include_watchlist
        else pd.Series(False, index=joined.index)
    )
    orthogonal_mask = (
        joined["final_research_gate"].eq(WATCHLIST_ALPHA_RESEARCH)
        & joined.get("repro_candidate_tier", pd.Series("", index=joined.index)).eq(ORTHOGONAL_WATCHLIST_TEST)
        & joined.get("signal_source", pd.Series("", index=joined.index)).eq(ORTHOGONAL_GENERATED)
        & joined.get("orthogonal_version", pd.Series("", index=joined.index)).eq(orthogonal_diversifier_version)
        & joined.get("reproducibility_status", pd.Series("", index=joined.index)).isin(["GLOBAL_PASS", "CONDITIONAL_PASS"])
        & joined["pass_rate"].ge(orthogonal_diversifier_min_pass_rate)
        & joined["signal_health_score"].ge(orthogonal_diversifier_min_health_score)
    )
    if not include_orthogonal_diversifiers:
        orthogonal_mask = pd.Series(False, index=joined.index)

    joined["diversity_candidate_tier"] = np.select(
        [core_mask, orthogonal_mask],
        [CORE_APPROVED, ORTHOGONAL_DIVERSIFIER],
        default="NOT_ELIGIBLE",
    )
    joined["eligible_for_diversity"] = core_mask | broad_watchlist_mask | orthogonal_mask
    return joined.sort_values(
        ["eligible_for_diversity", "diversity_candidate_tier", "signal_health_score", "pass_rate", "avg_effective_mean_ic"],
        ascending=[False, True, False, False, False],
    ).reset_index(drop=True)


def load_candidate_signal_rows(
    signal_names: list[str] | tuple[str, ...],
    db_path: str | Path | None = None,
) -> pd.DataFrame:
    """Load candidate_signals_current rows for the requested signal names only."""
    names = sorted({str(name) for name in signal_names if pd.notna(name)})
    if not names:
        return pd.DataFrame(columns=["Date", "ticker", "signal_name", "signal_value"])

    db_path = Path(db_path) if db_path is not None else get_sqlite_db_path()
    placeholders = ",".join(["?"] * len(names))
    query = (
        'SELECT Date, ticker, signal_name, signal_value '
        'FROM "candidate_signals_current" '
        f"WHERE signal_name IN ({placeholders})"
    )
    with sqlite3.connect(db_path) as conn:
        if not _table_exists(conn, "candidate_signals_current"):
            raise ValueError("Required table is missing: candidate_signals_current")
        return pd.read_sql_query(query, conn, params=names)


def signal_key(signal_name: str, horizon: int) -> str:
    return f"{signal_name}__h{int(horizon)}"


def _pivot_signal_panel(candidate_signals_long: pd.DataFrame, signal_name: str) -> pd.DataFrame:
    selected = candidate_signals_long.loc[candidate_signals_long["signal_name"].eq(signal_name)].copy()
    if selected.empty:
        raise ValueError(f"Signal not found in candidate signals: {signal_name}")
    selected["Date"] = pd.to_datetime(selected["Date"], errors="coerce")
    selected["signal_value"] = pd.to_numeric(selected["signal_value"], errors="coerce")
    panel = selected.pivot(index="Date", columns="ticker", values="signal_value")
    return panel.sort_index().sort_index(axis=1).replace([np.inf, -np.inf], np.nan)


def direction_adjust_panel(signal_panel: pd.DataFrame, signal_direction: str | None) -> pd.DataFrame:
    """Adjust signal panel so higher values represent the expected positive edge."""
    if signal_direction == NEGATIVE_EDGE_REVERSE_SIGNAL:
        return signal_panel * -1.0
    return signal_panel.copy()


def normalize_signal_panel(signal_panel: pd.DataFrame) -> pd.DataFrame:
    """Cross-sectionally rank-normalize a signal panel to rank percentile centered at zero."""
    normalized = signal_panel.rank(axis=1, pct=True) - 0.5
    return normalized.replace([np.inf, -np.inf], np.nan)


def build_signal_panels(
    candidate_table: pd.DataFrame,
    candidate_signals_long: pd.DataFrame,
) -> dict[str, pd.DataFrame]:
    """Build direction-adjusted, normalized Date x ticker panels for candidate signal-horizon rows."""
    raw_panel_cache: dict[str, pd.DataFrame] = {}
    panels: dict[str, pd.DataFrame] = {}
    eligible = candidate_table.loc[candidate_table["eligible_for_diversity"].eq(True)].copy()
    for _, row in eligible.iterrows():
        name = str(row["signal_name"])
        horizon = int(row["horizon"])
        key = signal_key(name, horizon)
        if name not in raw_panel_cache:
            raw_panel_cache[name] = _pivot_signal_panel(candidate_signals_long, name)
        adjusted = direction_adjust_panel(raw_panel_cache[name], row.get("signal_direction"))
        panels[key] = normalize_signal_panel(adjusted)
    return panels


def _flatten_panel(panel: pd.DataFrame) -> pd.Series:
    flattened = panel.copy()
    flattened.index.name = "Date"
    flattened.columns.name = "ticker"
    return flattened.stack(future_stack=True).rename("value")


def build_signal_similarity_matrix(
    candidate_table: pd.DataFrame,
    signal_panels: dict[str, pd.DataFrame],
) -> pd.DataFrame:
    """Compute pairwise flattened Pearson correlations between signal-horizon panels."""
    key_metadata = candidate_table.assign(
        signal_key=lambda df: df.apply(lambda row: signal_key(row["signal_name"], int(row["horizon"])), axis=1)
    )
    key_metadata = key_metadata.loc[key_metadata["signal_key"].isin(signal_panels)].copy()
    metadata_by_key = key_metadata.drop_duplicates("signal_key").set_index("signal_key")
    flat_cache = {key: _flatten_panel(panel) for key, panel in signal_panels.items()}
    keys = sorted(signal_panels)
    rows: list[dict[str, object]] = []

    for key_1 in keys:
        for key_2 in keys:
            pair = pd.concat(
                [flat_cache[key_1].rename("x"), flat_cache[key_2].rename("y")],
                axis=1,
            ).dropna()
            correlation = np.nan
            if len(pair) >= 2 and pair["x"].nunique(dropna=True) > 1 and pair["y"].nunique(dropna=True) > 1:
                correlation = float(pair["x"].corr(pair["y"], method="pearson"))
            meta_1 = metadata_by_key.loc[key_1]
            meta_2 = metadata_by_key.loc[key_2]
            rows.append(
                {
                    "signal_key_1": key_1,
                    "signal_key_2": key_2,
                    "signal_name_1": meta_1["signal_name"],
                    "horizon_1": int(meta_1["horizon"]),
                    "signal_name_2": meta_2["signal_name"],
                    "horizon_2": int(meta_2["horizon"]),
                    "correlation": correlation,
                }
            )

    return pd.DataFrame(rows)


def _correlation_matrix_from_similarity(similarity: pd.DataFrame) -> pd.DataFrame:
    if similarity.empty:
        return pd.DataFrame()
    matrix = similarity.pivot(index="signal_key_1", columns="signal_key_2", values="correlation")
    keys = sorted(set(matrix.index).union(matrix.columns))
    matrix = matrix.reindex(index=keys, columns=keys)
    for key in keys:
        matrix.loc[key, key] = 1.0
    return matrix


def compute_diversity_diagnostics(
    similarity: pd.DataFrame,
    candidate_table: pd.DataFrame,
) -> pd.DataFrame:
    """Compute aggregate diversity diagnostics for the eligible candidate set."""
    eligible_count = int(candidate_table["eligible_for_diversity"].sum()) if "eligible_for_diversity" in candidate_table else 0
    if similarity.empty:
        return pd.DataFrame(
            [
                {
                    "n_candidates": eligible_count,
                    "avg_abs_correlation": np.nan,
                    "max_abs_correlation": np.nan,
                    "median_abs_correlation": np.nan,
                    "effective_signal_count": np.nan,
                }
            ]
        )

    off_diag = similarity.loc[similarity["signal_key_1"].ne(similarity["signal_key_2"]), "correlation"]
    abs_corr = pd.to_numeric(off_diag, errors="coerce").abs().dropna()
    corr_matrix = _correlation_matrix_from_similarity(similarity)
    filled = corr_matrix.fillna(0.0)
    filled = (filled + filled.T) / 2.0
    eigenvalues = np.linalg.eigvalsh(filled.to_numpy(dtype=float)) if not filled.empty else np.array([])
    eigenvalues = np.clip(eigenvalues, 0.0, None)
    effective_signal_count = (
        float((eigenvalues.sum() ** 2) / np.square(eigenvalues).sum())
        if eigenvalues.size and np.square(eigenvalues).sum() > 0
        else np.nan
    )
    return pd.DataFrame(
        [
            {
                "n_candidates": eligible_count,
                "avg_abs_correlation": float(abs_corr.mean()) if not abs_corr.empty else np.nan,
                "max_abs_correlation": float(abs_corr.max()) if not abs_corr.empty else np.nan,
                "median_abs_correlation": float(abs_corr.median()) if not abs_corr.empty else np.nan,
                "effective_signal_count": effective_signal_count,
            }
        ]
    )


def _max_abs_corr_to_selected(
    signal_key_value: str,
    selected_keys: list[str],
    corr_lookup: dict[tuple[str, str], float],
) -> float:
    if not selected_keys:
        return 0.0
    values = [
        abs(corr_lookup.get((signal_key_value, selected_key), np.nan))
        for selected_key in selected_keys
    ]
    values = [value for value in values if not pd.isna(value)]
    return float(max(values)) if values else np.nan


def greedy_diversity_selection(
    candidate_table: pd.DataFrame,
    similarity: pd.DataFrame,
    correlation_threshold: float = 0.85,
    min_selected: int = 3,
) -> pd.DataFrame:
    """Select a diversified subset using greedy health-first ranking with correlation caps."""
    selection = candidate_table.copy()
    selection["signal_key"] = selection.apply(lambda row: signal_key(row["signal_name"], int(row["horizon"])), axis=1)
    sort_columns = ["signal_health_score", "pass_rate", "avg_effective_mean_ic"]
    for column in sort_columns:
        if column not in selection.columns:
            selection[column] = np.nan
        selection[column] = pd.to_numeric(selection[column], errors="coerce")
    selection = selection.sort_values(sort_columns + ["signal_name", "horizon"], ascending=[False, False, False, True, True])

    corr_lookup = {
        (row.signal_key_1, row.signal_key_2): row.correlation
        for row in similarity.itertuples(index=False)
    }
    selected_keys: list[str] = []
    rows: list[dict[str, object]] = []

    for _, row in selection.iterrows():
        row_dict = row.to_dict()
        if not bool(row_dict.get("eligible_for_diversity", False)):
            row_dict.update(
                {
                    "selected_flag": 0,
                    "selection_rank": np.nan,
                    "max_corr_to_selected": np.nan,
                    "selection_reason": "Not eligible under final research gate filter.",
                    "diversity_group": "NOT_ELIGIBLE",
                }
            )
            rows.append(row_dict)
            continue
        is_orthogonal_diversifier = row_dict.get("diversity_candidate_tier") == ORTHOGONAL_DIVERSIFIER
        avg_effective_mean_ic = pd.to_numeric(pd.Series([row_dict.get("avg_effective_mean_ic")]), errors="coerce").iloc[0]
        pass_rate = pd.to_numeric(pd.Series([row_dict.get("pass_rate")]), errors="coerce").iloc[0]
        if is_orthogonal_diversifier and (pd.isna(pass_rate) or pass_rate < 0.60):
            row_dict.update(
                {
                    "selected_flag": 0,
                    "selection_rank": np.nan,
                    "max_corr_to_selected": np.nan,
                    "selection_reason": "Orthogonal diversifier watchlist; pass rate below 0.60.",
                    "diversity_group": "ORTHOGONAL_DIVERSIFIER_WATCHLIST",
                }
            )
            rows.append(row_dict)
            continue
        if is_orthogonal_diversifier and (pd.isna(avg_effective_mean_ic) or avg_effective_mean_ic <= 0):
            row_dict.update(
                {
                    "selected_flag": 0,
                    "selection_rank": np.nan,
                    "max_corr_to_selected": np.nan,
                    "selection_reason": "Orthogonal diversifier watchlist; average effective IC is not positive.",
                    "diversity_group": "ORTHOGONAL_DIVERSIFIER_WATCHLIST",
                }
            )
            rows.append(row_dict)
            continue
        max_corr = _max_abs_corr_to_selected(row_dict["signal_key"], selected_keys, corr_lookup)
        if not selected_keys or pd.isna(max_corr) or max_corr <= correlation_threshold:
            selected_keys.append(row_dict["signal_key"])
            row_dict.update(
                {
                    "selected_flag": 1,
                    "selection_rank": len(selected_keys),
                    "max_corr_to_selected": max_corr,
                    "selection_reason": f"Selected within correlation threshold {correlation_threshold:.2f}.",
                    "diversity_group": (
                        "ORTHOGONAL_DIVERSIFIER_SELECTED"
                        if is_orthogonal_diversifier
                        else "CORE_SELECTED"
                    ),
                }
            )
        else:
            row_dict.update(
                {
                    "selected_flag": 0,
                    "selection_rank": np.nan,
                    "max_corr_to_selected": max_corr,
                    "selection_reason": f"Rejected as redundant; max abs correlation {max_corr:.3f} exceeds {correlation_threshold:.2f}.",
                    "diversity_group": "REDUNDANT_REJECTED",
                }
            )
        rows.append(row_dict)

    output = pd.DataFrame(rows)

    if int(output["selected_flag"].sum()) < min_selected:
        relaxed_threshold = 0.90
        selected_keys = output.loc[output["selected_flag"].eq(1), "signal_key"].tolist()
        for idx, row in output.loc[
            output["eligible_for_diversity"].eq(True)
            & output["selected_flag"].eq(0)
            & output["diversity_candidate_tier"].eq(CORE_APPROVED)
        ].iterrows():
            if int(output["selected_flag"].sum()) >= min_selected:
                break
            max_corr = _max_abs_corr_to_selected(row["signal_key"], selected_keys, corr_lookup)
            if pd.isna(max_corr) or max_corr <= relaxed_threshold:
                selected_keys.append(row["signal_key"])
                output.loc[idx, "selected_flag"] = 1
                output.loc[idx, "selection_rank"] = len(selected_keys)
                output.loc[idx, "max_corr_to_selected"] = max_corr
                output.loc[idx, "selection_reason"] = f"Selected after relaxing threshold to {relaxed_threshold:.2f}."
                output.loc[idx, "diversity_group"] = "CORE_SELECTED"

    if int(output["selected_flag"].sum()) < min_selected:
        selected_keys = output.loc[output["selected_flag"].eq(1), "signal_key"].tolist()
        for idx, row in output.loc[
            output["eligible_for_diversity"].eq(True)
            & output["selected_flag"].eq(0)
            & output["diversity_candidate_tier"].eq(CORE_APPROVED)
        ].iterrows():
            if int(output["selected_flag"].sum()) >= min_selected:
                break
            max_corr = _max_abs_corr_to_selected(row["signal_key"], selected_keys, corr_lookup)
            selected_keys.append(row["signal_key"])
            output.loc[idx, "selected_flag"] = 1
            output.loc[idx, "selection_rank"] = len(selected_keys)
            output.loc[idx, "max_corr_to_selected"] = max_corr
            output.loc[idx, "selection_reason"] = "Forced to meet MIN_SELECTED after threshold relaxation."
            output.loc[idx, "diversity_group"] = "FORCED_MIN_SELECTED"

    columns = [
        "signal_key",
        "signal_name",
        "horizon",
        "signal_family",
        "diversity_candidate_tier",
        "signal_source",
        "orthogonal_version",
        "orthogonal_cluster",
        "repro_candidate_tier",
        "signal_health_score",
        "final_research_gate",
        "reproducibility_status",
        "pass_rate",
        "avg_effective_mean_ic",
        "selected_flag",
        "selection_rank",
        "max_corr_to_selected",
        "selection_reason",
        "diversity_group",
    ]
    for column in columns:
        if column not in output.columns:
            output[column] = np.nan
    return output[columns].sort_values(["selected_flag", "selection_rank", "signal_health_score"], ascending=[False, True, False]).reset_index(drop=True)


def build_family_diversity_report(
    candidate_table: pd.DataFrame,
    selection: pd.DataFrame,
    similarity: pd.DataFrame,
) -> pd.DataFrame:
    """Summarize diversity and selection coverage by signal family."""
    eligible = candidate_table.loc[candidate_table["eligible_for_diversity"].eq(True)].copy()
    if eligible.empty:
        return pd.DataFrame(
            columns=[
                "signal_family",
                "n_candidates",
                "n_selected",
                "avg_health_score",
                "max_health_score",
                "avg_abs_corr_within_family",
            ]
        )
    eligible["signal_key"] = eligible.apply(lambda row: signal_key(row["signal_name"], int(row["horizon"])), axis=1)
    family_by_key = eligible.drop_duplicates("signal_key").set_index("signal_key")["signal_family"].to_dict()
    selected_keys = set(selection.loc[selection["selected_flag"].eq(1), "signal_key"])
    rows: list[dict[str, object]] = []

    for family, group in eligible.groupby("signal_family", dropna=False):
        keys = set(group["signal_key"])
        within = similarity.loc[
            similarity["signal_key_1"].isin(keys)
            & similarity["signal_key_2"].isin(keys)
            & similarity["signal_key_1"].ne(similarity["signal_key_2"])
        ]
        abs_corr = pd.to_numeric(within["correlation"], errors="coerce").abs().dropna()
        rows.append(
            {
                "signal_family": family,
                "n_candidates": int(group["signal_key"].nunique()),
                "n_selected": int(len(keys.intersection(selected_keys))),
                "avg_health_score": float(pd.to_numeric(group["signal_health_score"], errors="coerce").mean()),
                "max_health_score": float(pd.to_numeric(group["signal_health_score"], errors="coerce").max()),
                "avg_abs_corr_within_family": float(abs_corr.mean()) if not abs_corr.empty else np.nan,
            }
        )

    return pd.DataFrame(rows).sort_values(["n_selected", "max_health_score"], ascending=[False, False]).reset_index(drop=True)


def build_cluster_diversity_report(
    candidate_table: pd.DataFrame,
    selection: pd.DataFrame,
    similarity: pd.DataFrame,
) -> pd.DataFrame:
    """Summarize diversity and selection coverage by orthogonal cluster when available."""
    eligible = candidate_table.loc[candidate_table["eligible_for_diversity"].eq(True)].copy()
    if eligible.empty or "orthogonal_cluster" not in eligible.columns:
        return pd.DataFrame(
            columns=[
                "orthogonal_cluster",
                "n_candidates",
                "n_selected",
                "n_orthogonal_diversifiers",
                "avg_health_score",
                "max_health_score",
                "avg_abs_corr_within_cluster",
            ]
        )
    eligible["orthogonal_cluster"] = eligible["orthogonal_cluster"].fillna("CORE_OR_UNSPECIFIED")
    eligible["signal_key"] = eligible.apply(lambda row: signal_key(row["signal_name"], int(row["horizon"])), axis=1)
    selected_keys = set(selection.loc[selection["selected_flag"].eq(1), "signal_key"])
    rows: list[dict[str, object]] = []

    for cluster, group in eligible.groupby("orthogonal_cluster", dropna=False):
        keys = set(group["signal_key"])
        within = similarity.loc[
            similarity["signal_key_1"].isin(keys)
            & similarity["signal_key_2"].isin(keys)
            & similarity["signal_key_1"].ne(similarity["signal_key_2"])
        ]
        abs_corr = pd.to_numeric(within["correlation"], errors="coerce").abs().dropna()
        rows.append(
            {
                "orthogonal_cluster": cluster,
                "n_candidates": int(group["signal_key"].nunique()),
                "n_selected": int(len(keys.intersection(selected_keys))),
                "n_orthogonal_diversifiers": int(group["diversity_candidate_tier"].eq(ORTHOGONAL_DIVERSIFIER).sum()),
                "avg_health_score": float(pd.to_numeric(group["signal_health_score"], errors="coerce").mean()),
                "max_health_score": float(pd.to_numeric(group["signal_health_score"], errors="coerce").max()),
                "avg_abs_corr_within_cluster": float(abs_corr.mean()) if not abs_corr.empty else np.nan,
            }
        )

    return pd.DataFrame(rows).sort_values(["n_selected", "max_health_score"], ascending=[False, False]).reset_index(drop=True)


def run_signal_diversity_analysis(
    db_path: str | Path | None = None,
    include_watchlist: bool = False,
    include_orthogonal_diversifiers: bool = False,
    correlation_threshold: float = 0.85,
    min_selected: int = 3,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Run the full signal diversity workflow."""
    inputs = load_signal_diversity_inputs(db_path=db_path)
    candidates = build_diversity_candidate_table(
        health=inputs["health"],
        reproducibility_gate=inputs["reproducibility_gate"],
        include_watchlist=include_watchlist,
        include_orthogonal_diversifiers=include_orthogonal_diversifiers,
    )
    eligible_signal_names = candidates.loc[candidates["eligible_for_diversity"].eq(True), "signal_name"].tolist()
    candidate_signals = load_candidate_signal_rows(eligible_signal_names, db_path=db_path)
    panels = build_signal_panels(candidates, candidate_signals)
    similarity = build_signal_similarity_matrix(candidates, panels)
    diagnostics = compute_diversity_diagnostics(similarity, candidates)
    selection = greedy_diversity_selection(
        candidates,
        similarity,
        correlation_threshold=correlation_threshold,
        min_selected=min_selected,
    )
    family_report = build_family_diversity_report(candidates, selection, similarity)
    cluster_report = build_cluster_diversity_report(candidates, selection, similarity)
    return similarity, diagnostics, selection, family_report, cluster_report


def build_signal_diversity_summary(
    run_id: str,
    run_timestamp: str,
    diversity_version: str,
    candidates: pd.DataFrame,
    eligible_candidates: pd.DataFrame,
    similarity: pd.DataFrame,
    selection: pd.DataFrame,
    family_report: pd.DataFrame,
    cluster_report: pd.DataFrame,
    candidate_signal_rows_loaded: int,
) -> pd.DataFrame:
    """Build a compact downstream summary without changing output table schemas."""
    selected = selection.loc[selection["selected_flag"].eq(1)] if "selected_flag" in selection else pd.DataFrame()
    redundant = (
        selection.loc[selection["diversity_group"].eq("REDUNDANT_REJECTED")]
        if "diversity_group" in selection
        else pd.DataFrame()
    )
    return pd.DataFrame(
        [
            {"metric": "run_id", "value": run_id},
            {"metric": "run_timestamp", "value": run_timestamp},
            {"metric": "diversity_version", "value": diversity_version},
            {"metric": "candidate_rows", "value": len(candidates)},
            {"metric": "candidate_count", "value": len(eligible_candidates)},
            {"metric": "unique_eligible_signals", "value": int(eligible_candidates["signal_name"].nunique()) if "signal_name" in eligible_candidates else 0},
            {"metric": "candidate_signal_rows_loaded", "value": candidate_signal_rows_loaded},
            {"metric": "pairwise_comparisons", "value": len(similarity)},
            {"metric": "selected_count", "value": int(selection["selected_flag"].sum()) if "selected_flag" in selection else 0},
            {"metric": "redundant_rejected_count", "value": len(redundant)},
            {"metric": "family_report_rows", "value": len(family_report)},
            {"metric": "cluster_report_rows", "value": len(cluster_report)},
        ]
    )


def run_03g_signal_diversity(
    db_path: str | Path | None = None,
    diversity_version: str = DIVERSITY_VERSION,
    run_id: str | None = None,
    include_watchlist: bool = INCLUDE_WATCHLIST,
    include_orthogonal_diversifiers: bool = INCLUDE_ORTHOGONAL_DIVERSIFIERS,
    orthogonal_diversifier_version: str = ORTHOGONAL_DIVERSIFIER_VERSION,
    orthogonal_diversifier_min_health_score: float = ORTHOGONAL_DIVERSIFIER_MIN_HEALTH_SCORE,
    orthogonal_diversifier_min_pass_rate: float = ORTHOGONAL_DIVERSIFIER_MIN_PASS_RATE,
    correlation_threshold: float = CORRELATION_THRESHOLD,
    min_selected: int = MIN_SELECTED,
    write: bool = False,
    verbose: bool = True,
) -> dict[str, object]:
    """Run the 03G signal diversity workflow with notebook-equivalent logic."""
    resolved_run_id = run_id or make_run_id(prefix="phase2_signal_diversity")
    run_timestamp = make_run_timestamp()
    ensure_signal_diversity_indexes(db_path)

    if verbose:
        print("03G signal diversity: loading inputs")
    inputs = load_signal_diversity_inputs(db_path=db_path)
    candidates = build_diversity_candidate_table(
        health=inputs["health"],
        reproducibility_gate=inputs["reproducibility_gate"],
        include_watchlist=include_watchlist,
        include_orthogonal_diversifiers=include_orthogonal_diversifiers,
        orthogonal_diversifier_version=orthogonal_diversifier_version,
        orthogonal_diversifier_min_health_score=orthogonal_diversifier_min_health_score,
        orthogonal_diversifier_min_pass_rate=orthogonal_diversifier_min_pass_rate,
    )
    eligible_candidates = candidates.loc[candidates["eligible_for_diversity"].eq(True)].copy()
    eligible_signal_names = eligible_candidates["signal_name"].dropna().astype(str).unique().tolist()

    if verbose:
        print(f"03G signal diversity: loading {len(eligible_signal_names):,} eligible signal panels")
    candidate_signals = load_candidate_signal_rows(eligible_signal_names, db_path=db_path)
    panels = build_signal_panels(candidates, candidate_signals)
    similarity = build_signal_similarity_matrix(candidates, panels)
    diagnostics = compute_diversity_diagnostics(similarity, candidates)
    selection = greedy_diversity_selection(
        candidates,
        similarity,
        correlation_threshold=correlation_threshold,
        min_selected=min_selected,
    )
    family_report = build_family_diversity_report(candidates, selection, similarity)
    cluster_report = build_cluster_diversity_report(candidates, selection, similarity)
    summary = build_signal_diversity_summary(
        run_id=resolved_run_id,
        run_timestamp=run_timestamp,
        diversity_version=diversity_version,
        candidates=candidates,
        eligible_candidates=eligible_candidates,
        similarity=similarity,
        selection=selection,
        family_report=family_report,
        cluster_report=cluster_report,
        candidate_signal_rows_loaded=len(candidate_signals),
    )

    saved_paths: dict[str, Path] = {}
    if write:
        if verbose:
            print("03G signal diversity: writing SQLite outputs")
        saved_paths = save_signal_diversity_outputs(
            similarity=similarity,
            diagnostics=diagnostics,
            selection=selection,
            family_report=family_report,
            cluster_report=cluster_report,
            db_path=db_path,
            run_id=resolved_run_id,
            diversity_version=diversity_version,
        )

    return {
        "run_id": resolved_run_id,
        "run_timestamp": run_timestamp,
        "diversity_version": diversity_version,
        "inputs": inputs,
        "diversity_candidates": candidates,
        "eligible_candidates": eligible_candidates,
        "candidate_signal_rows_loaded": len(candidate_signals),
        "signal_diversity_similarity": similarity,
        "signal_diversity_diagnostics": diagnostics,
        "signal_diversity_selection": selection,
        "signal_diversity_family_report": family_report,
        "signal_diversity_cluster_report": cluster_report,
        "summary": summary,
        "saved_paths": saved_paths,
    }


__all__ = [
    "APPROVED_FOR_ALPHA_RESEARCH",
    "WATCHLIST_ALPHA_RESEARCH",
    "build_cluster_diversity_report",
    "build_diversity_candidate_table",
    "build_family_diversity_report",
    "build_signal_diversity_summary",
    "build_signal_panels",
    "build_signal_similarity_matrix",
    "compute_diversity_diagnostics",
    "CORRELATION_THRESHOLD",
    "DIVERSITY_VERSION",
    "ensure_signal_diversity_indexes",
    "greedy_diversity_selection",
    "INCLUDE_ORTHOGONAL_DIVERSIFIERS",
    "INCLUDE_WATCHLIST",
    "load_candidate_signal_rows",
    "load_candidate_best_horizon_gap",
    "load_signal_diversity_inputs",
    "MIN_SELECTED",
    "normalize_signal_panel",
    "ORTHOGONAL_DIVERSIFIER_MIN_HEALTH_SCORE",
    "ORTHOGONAL_DIVERSIFIER_MIN_PASS_RATE",
    "readback_sql",
    "REQUIRED_INPUT_TABLES",
    "run_03g_signal_diversity",
    "run_signal_diversity_analysis",
    "signal_key",
]
