from __future__ import annotations

import sqlite3
from pathlib import Path

import numpy as np
import pandas as pd

from src.forward_returns import make_forward_returns
from src.run_config import get_sqlite_db_path
from src.wfv_scoring import score_signal_wfv


APPROVED_CONSTRUCTED_ALPHA_WFV = "APPROVED_CONSTRUCTED_ALPHA_WFV"
WATCHLIST_CONSTRUCTED_ALPHA_WFV = "WATCHLIST_CONSTRUCTED_ALPHA_WFV"
REJECTED_CONSTRUCTED_ALPHA_WFV = "REJECTED_CONSTRUCTED_ALPHA_WFV"


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


def load_constructed_alpha_candidates(db_path: str | Path | None = None) -> pd.DataFrame:
    """Load constructed alpha candidates approved for alpha validation."""
    db_path = Path(db_path) if db_path is not None else get_sqlite_db_path()
    with sqlite3.connect(db_path) as conn:
        if not _table_exists(conn, "alpha_construction_quality_current"):
            raise ValueError("Required table is missing: alpha_construction_quality_current")
        quality = pd.read_sql_query('SELECT * FROM "alpha_construction_quality_current"', conn)

    candidates = quality.loc[
        quality["status"].eq("APPROVED_FOR_ALPHA_VALIDATION")
    ].copy()
    return candidates.sort_values("alpha_name").reset_index(drop=True)


def pivot_alpha_panel(alpha_long_df: pd.DataFrame, alpha_name: str) -> pd.DataFrame:
    """Convert one constructed alpha from long format to a Date x ticker panel."""
    required_columns = {"Date", "ticker", "alpha_name", "alpha_value"}
    missing_columns = required_columns.difference(alpha_long_df.columns)
    if missing_columns:
        raise ValueError(f"alpha_long_df is missing required columns: {sorted(missing_columns)}")

    selected = alpha_long_df.loc[alpha_long_df["alpha_name"].eq(alpha_name)].copy()
    if selected.empty:
        raise ValueError(f"alpha_name '{alpha_name}' not found in alpha_long_df.")
    selected["Date"] = pd.to_datetime(selected["Date"], errors="coerce")
    selected["alpha_value"] = pd.to_numeric(selected["alpha_value"], errors="coerce")
    panel = selected.pivot(index="Date", columns="ticker", values="alpha_value")
    panel.columns.name = None
    return panel.sort_index().sort_index(axis=1).replace([np.inf, -np.inf], np.nan)


def run_constructed_alpha_wfv(
    approved_alphas: pd.DataFrame,
    alpha_long_df: pd.DataFrame,
    close_prices: pd.DataFrame,
    windows: pd.DataFrame,
    horizons: list[int] | tuple[int, ...] = (1, 5, 10, 20),
    method: str = "spearman",
    alpha_panels: dict[str, pd.DataFrame] | None = None,
    forward_returns: dict[int, pd.DataFrame] | None = None,
) -> pd.DataFrame:
    """Run existing WFV window IC scoring on constructed alpha candidates."""
    if approved_alphas.empty:
        return pd.DataFrame()

    horizon_values = sorted({int(horizon) for horizon in horizons})
    if forward_returns is None:
        forward_returns = make_forward_returns(close_prices, horizon_values)
    panel_cache: dict[str, pd.DataFrame] = {}
    rows: list[pd.DataFrame] = []

    for alpha_name in approved_alphas["alpha_name"].dropna().astype(str).unique():
        if alpha_panels is not None:
            if alpha_name not in alpha_panels:
                raise ValueError(f"alpha panel cache is missing alpha_name: {alpha_name}")
            panel_cache[alpha_name] = alpha_panels[alpha_name]
        elif alpha_name not in panel_cache:
            panel_cache[alpha_name] = pivot_alpha_panel(alpha_long_df, alpha_name)

        for horizon in horizon_values:
            scored = score_signal_wfv(
                signal_panel=panel_cache[alpha_name],
                fwd_return_panel=forward_returns[horizon],
                windows=windows,
                signal_name=alpha_name,
                horizon=horizon,
                method=method,
            ).rename(columns={"signal_name": "alpha_name"})
            scored["expected_direction"] = "POSITIVE"
            rows.append(scored)

    if not rows:
        return pd.DataFrame()
    output = pd.concat(rows, ignore_index=True)
    return output.sort_values(["alpha_name", "horizon", "window_id"]).reset_index(drop=True)


def _persistence_ratio(train_ic: pd.Series, test_ic: pd.Series) -> float:
    paired = pd.concat([train_ic.rename("train"), test_ic.rename("test")], axis=1).dropna()
    paired = paired.loc[paired["train"].ne(0) & paired["test"].ne(0)]
    if paired.empty:
        return np.nan
    return float(np.sign(paired["train"]).eq(np.sign(paired["test"])).mean())


def summarize_constructed_alpha_wfv(window_results: pd.DataFrame) -> pd.DataFrame:
    """Summarize constructed alpha WFV results by alpha and horizon."""
    columns = [
        "alpha_name",
        "horizon",
        "n_windows",
        "mean_train_ic",
        "mean_test_ic",
        "median_test_ic",
        "test_ic_std",
        "test_ic_ir",
        "effective_mean_test_ic",
        "effective_test_ic_ir",
        "persistence_ratio",
        "sign_consistency",
        "n_positive_test_windows",
        "n_negative_test_windows",
    ]
    if window_results.empty:
        return pd.DataFrame(columns=columns)

    rows: list[dict[str, object]] = []
    for (alpha_name, horizon), group in window_results.groupby(["alpha_name", "horizon"], dropna=False):
        train_ic = group["train_mean_ic"].astype(float)
        test_ic = group["test_mean_ic"].astype(float)
        valid_test = test_ic.dropna()
        mean_train_ic = float(train_ic.mean()) if not train_ic.dropna().empty else np.nan
        mean_test_ic = float(valid_test.mean()) if not valid_test.empty else np.nan
        test_ic_std = float(valid_test.std(ddof=1)) if len(valid_test) > 1 else np.nan
        test_ic_ir = float(mean_test_ic / test_ic_std) if test_ic_std and not pd.isna(test_ic_std) else np.nan
        rows.append(
            {
                "alpha_name": alpha_name,
                "horizon": int(horizon),
                "n_windows": int(group["window_id"].nunique()),
                "mean_train_ic": mean_train_ic,
                "mean_test_ic": mean_test_ic,
                "median_test_ic": float(valid_test.median()) if not valid_test.empty else np.nan,
                "test_ic_std": test_ic_std,
                "test_ic_ir": test_ic_ir,
                "effective_mean_test_ic": mean_test_ic,
                "effective_test_ic_ir": test_ic_ir,
                "persistence_ratio": _persistence_ratio(train_ic, test_ic),
                "sign_consistency": float(valid_test.gt(0).mean()) if not valid_test.empty else np.nan,
                "n_positive_test_windows": int(valid_test.gt(0).sum()),
                "n_negative_test_windows": int(valid_test.lt(0).sum()),
            }
        )

    return pd.DataFrame(rows)[columns].sort_values(["alpha_name", "horizon"]).reset_index(drop=True)


def _constructed_alpha_status(row: pd.Series) -> str:
    effective_mean_test_ic = row.get("effective_mean_test_ic")
    effective_test_ic_ir = row.get("effective_test_ic_ir")
    persistence_ratio = row.get("persistence_ratio")
    sign_consistency = row.get("sign_consistency")

    if pd.isna(effective_test_ic_ir) or pd.isna(persistence_ratio):
        return REJECTED_CONSTRUCTED_ALPHA_WFV
    if (
        float(effective_mean_test_ic) >= 0.015
        and float(effective_test_ic_ir) >= 0.05
        and float(persistence_ratio) >= 0.67
        and not pd.isna(sign_consistency)
        and float(sign_consistency) >= 0.67
    ):
        return APPROVED_CONSTRUCTED_ALPHA_WFV
    if float(effective_mean_test_ic) >= 0.008 and float(persistence_ratio) >= 0.50:
        return WATCHLIST_CONSTRUCTED_ALPHA_WFV
    return REJECTED_CONSTRUCTED_ALPHA_WFV


def _constructed_alpha_notes(row: pd.Series) -> str:
    status = row.get("status")
    if status == APPROVED_CONSTRUCTED_ALPHA_WFV:
        return "Meets strict constructed alpha WFV thresholds."
    if status == WATCHLIST_CONSTRUCTED_ALPHA_WFV:
        return "Meets secondary constructed alpha WFV thresholds."

    notes: list[str] = []
    effective_mean_test_ic = row.get("effective_mean_test_ic")
    effective_test_ic_ir = row.get("effective_test_ic_ir")
    persistence_ratio = row.get("persistence_ratio")
    sign_consistency = row.get("sign_consistency")
    if pd.isna(effective_test_ic_ir) or pd.isna(persistence_ratio):
        notes.append("insufficient valid WFV windows")
    if pd.isna(effective_mean_test_ic) or float(effective_mean_test_ic) < 0.008:
        notes.append("weak effective IC")
    if pd.isna(effective_test_ic_ir) or float(effective_test_ic_ir) < 0.05:
        notes.append("weak effective IC IR")
    if pd.isna(persistence_ratio) or float(persistence_ratio) < 0.50:
        notes.append("low persistence")
    if pd.isna(sign_consistency) or float(sign_consistency) < 0.67:
        notes.append("low sign consistency")
    return "; ".join(dict.fromkeys(notes)) if notes else "fails constructed alpha WFV thresholds"


def apply_constructed_alpha_wfv_gate(summary: pd.DataFrame) -> pd.DataFrame:
    """Apply constructed alpha WFV gates."""
    gated = summary.copy()
    gated["status"] = gated.apply(_constructed_alpha_status, axis=1)
    gated["constructed_alpha_wfv_notes"] = gated.apply(_constructed_alpha_notes, axis=1)
    return gated


def build_constructed_alpha_wfv_failure_breakdown(gate: pd.DataFrame) -> pd.DataFrame:
    """Count rejected constructed alpha WFV failure reasons."""
    if gate.empty or "constructed_alpha_wfv_notes" not in gate.columns:
        return pd.DataFrame(columns=["failure_reason", "count", "pct_of_rejected"])
    rejected = gate.loc[gate["status"].eq(REJECTED_CONSTRUCTED_ALPHA_WFV)].copy()
    if rejected.empty:
        return pd.DataFrame(columns=["failure_reason", "count", "pct_of_rejected"])
    exploded = (
        rejected["constructed_alpha_wfv_notes"]
        .str.split("; ")
        .explode()
        .dropna()
        .loc[lambda s: s.ne("")]
    )
    counts = exploded.value_counts().rename_axis("failure_reason").reset_index(name="count")
    counts["pct_of_rejected"] = counts["count"] / len(rejected)
    return counts


def build_constructed_alpha_wfv_winner_summary(gate: pd.DataFrame) -> pd.DataFrame:
    """Summarize strongest constructed alpha WFV candidates by alpha and overall."""
    if gate.empty:
        return pd.DataFrame()
    status_rank = {
        APPROVED_CONSTRUCTED_ALPHA_WFV: 0,
        WATCHLIST_CONSTRUCTED_ALPHA_WFV: 1,
        REJECTED_CONSTRUCTED_ALPHA_WFV: 2,
    }
    ranked = gate.copy()
    ranked["_status_rank"] = ranked["status"].map(status_rank).fillna(9)
    winners = (
        ranked.sort_values(
            ["_status_rank", "effective_mean_test_ic", "effective_test_ic_ir", "persistence_ratio"],
            ascending=[True, False, False, False],
        )
        .groupby("alpha_name", as_index=False)
        .head(1)
        .reset_index(drop=True)
    )
    return winners[
        [
            "alpha_name",
            "horizon",
            "status",
            "effective_mean_test_ic",
            "effective_test_ic_ir",
            "persistence_ratio",
            "sign_consistency",
            "constructed_alpha_wfv_notes",
        ]
    ].sort_values(["status", "effective_mean_test_ic"], ascending=[True, False]).reset_index(drop=True)


__all__ = [
    "APPROVED_CONSTRUCTED_ALPHA_WFV",
    "REJECTED_CONSTRUCTED_ALPHA_WFV",
    "WATCHLIST_CONSTRUCTED_ALPHA_WFV",
    "apply_constructed_alpha_wfv_gate",
    "build_constructed_alpha_wfv_failure_breakdown",
    "build_constructed_alpha_wfv_winner_summary",
    "load_constructed_alpha_candidates",
    "pivot_alpha_panel",
    "run_constructed_alpha_wfv",
    "summarize_constructed_alpha_wfv",
]
