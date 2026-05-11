from __future__ import annotations

import sqlite3
from contextlib import nullcontext, redirect_stdout
from io import StringIO
from pathlib import Path

import numpy as np
import pandas as pd

from src.db import load_price_table
from src.forward_returns import make_forward_returns
from src.run_config import make_run_id, make_run_timestamp
from src.run_config import get_sqlite_db_path
from src.scoring.reproducibility_storage import save_signal_reproducibility_outputs
from src.signal_storage import load_candidate_signals_by_names


PASS_MIN_OBS = 5_000
PASS_MIN_EFFECTIVE_IC = 0.008
PASS_MIN_POSITIVE_RATE = 0.52
BENCHMARK_COLUMNS = {"SPY", "QQQ", "IWM", "DIA"}
REPRODUCIBILITY_VERSION = "phase2_signal_reproducibility_v1"
INCLUDE_WATCHLIST = False
INCLUDE_ORTHOGONAL_WATCHLIST = True
ORTHOGONAL_WATCHLIST_MIN_HEALTH_SCORE = 60
ORTHOGONAL_WATCHLIST_VERSION = "phase2_orthogonal_signals_v2"
IC_METHOD = "spearman"
REQUIRED_INPUT_TABLES = (
    "signal_health_score_current",
    "candidate_signals_current",
    "clean_close_prices_current",
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


def load_reproducibility_candidates(
    db_path: str | Path | None = None,
    include_watchlist: bool = False,
    include_orthogonal_watchlist: bool = False,
    orthogonal_watchlist_min_health_score: float = 60.0,
    orthogonal_watchlist_version: str = "phase2_orthogonal_signals_v2",
) -> pd.DataFrame:
    """Load Notebook 3E health candidates for reproducibility testing."""
    db_path = Path(db_path) if db_path is not None else get_sqlite_db_path()
    with sqlite3.connect(db_path) as conn:
        if not _table_exists(conn, "signal_health_score_current"):
            raise ValueError("Required table is missing: signal_health_score_current")
        health = pd.read_sql_query('SELECT * FROM "signal_health_score_current"', conn)
        metadata = (
            pd.read_sql_query('SELECT * FROM "candidate_signal_metadata_current"', conn)
            if _table_exists(conn, "candidate_signal_metadata_current")
            else pd.DataFrame()
        )
        quality = (
            pd.read_sql_query('SELECT * FROM "candidate_signal_quality_current"', conn)
            if _table_exists(conn, "candidate_signal_quality_current")
            else pd.DataFrame()
        )

    enriched = health.copy()
    if not metadata.empty:
        metadata_columns = [
            "signal_name",
            "signal_source",
            "orthogonal_version",
            "signal_version",
        ]
        enriched = enriched.merge(
            metadata[[column for column in metadata_columns if column in metadata.columns]].drop_duplicates("signal_name"),
            on="signal_name",
            how="left",
        )
    for column in ["signal_source", "orthogonal_version", "signal_version"]:
        if column not in enriched.columns:
            enriched[column] = pd.NA

    if not quality.empty:
        quality_columns = [
            "signal_name",
            "orthogonal_cluster",
            "signal_source",
            "orthogonal_version",
        ]
        enriched = enriched.merge(
            quality[[column for column in quality_columns if column in quality.columns]].drop_duplicates("signal_name"),
            on="signal_name",
            how="left",
            suffixes=("", "_quality"),
        )
        for column in ["signal_source", "orthogonal_version"]:
            quality_column = f"{column}_quality"
            if quality_column in enriched.columns:
                enriched[column] = enriched[column].combine_first(enriched[quality_column])
                enriched = enriched.drop(columns=[quality_column])
    if "orthogonal_cluster" not in enriched.columns:
        enriched["orthogonal_cluster"] = pd.NA

    gates = ["APPROVED_FOR_RESEARCH"]
    if include_watchlist:
        gates.append("WATCHLIST_RESEARCH")
    core_candidates = enriched.loc[enriched["signal_health_gate"].isin(gates)].copy()
    core_candidates["repro_candidate_tier"] = "CORE_APPROVED"

    orthogonal_watchlist = pd.DataFrame(columns=enriched.columns)
    if include_orthogonal_watchlist:
        recommended_use = enriched.get("recommended_use", pd.Series(pd.NA, index=enriched.index))
        orthogonal_watchlist = enriched.loc[
            enriched["signal_health_gate"].eq("WATCHLIST_RESEARCH")
            & enriched["signal_source"].astype(str).eq("orthogonal_generated")
            & enriched["orthogonal_version"].astype(str).eq(orthogonal_watchlist_version)
            & enriched["scoring_status"].isin(["WATCHLIST", "APPROVED_FOR_WFV"])
            & enriched["decay_status"].eq("STABLE")
            & enriched["decay_risk_flag"].eq("LOW_DECAY_RISK")
            & pd.to_numeric(enriched["signal_health_score"], errors="coerce").ge(orthogonal_watchlist_min_health_score)
            & recommended_use.isin(["CONDITIONAL", "WATCHLIST"])
        ].copy()
        orthogonal_watchlist["repro_candidate_tier"] = "ORTHOGONAL_WATCHLIST_TEST"

    candidates = pd.concat([core_candidates, orthogonal_watchlist], ignore_index=True)
    candidates = candidates.drop_duplicates(["signal_name", "horizon"], keep="first")
    return candidates.sort_values(["signal_health_score", "signal_name", "horizon"], ascending=[False, True, True]).reset_index(drop=True)


def _eligible_tickers(close_prices: pd.DataFrame, base_universe: list[str] | None = None) -> list[str]:
    tickers = list(base_universe) if base_universe is not None else list(close_prices.columns)
    return sorted([ticker for ticker in tickers if ticker in close_prices.columns and ticker not in BENCHMARK_COLUMNS])


def build_reproducibility_universes(
    close_prices: pd.DataFrame,
    base_universe: list[str] | None = None,
) -> dict[str, list[str]]:
    """Build deterministic universe slices for reproducibility checks."""
    tickers = _eligible_tickers(close_prices, base_universe=base_universe)
    midpoint = len(tickers) // 2

    rng_42 = np.random.default_rng(42)
    rng_99 = np.random.default_rng(99)
    return {
        "full_universe": tickers,
        "first_half_tickers": tickers[:midpoint],
        "second_half_tickers": tickers[midpoint:],
        "random_half_seed_42": sorted(rng_42.choice(tickers, size=midpoint, replace=False).tolist()) if tickers else [],
        "random_half_seed_99": sorted(rng_99.choice(tickers, size=midpoint, replace=False).tolist()) if tickers else [],
    }


def build_reproducibility_subperiods(close_prices: pd.DataFrame) -> dict[str, tuple[pd.Timestamp, pd.Timestamp]]:
    """Build adaptive date-quantile subperiods for reproducibility checks."""
    dates = pd.Series(pd.to_datetime(close_prices.index, errors="coerce")).dropna().sort_values()
    if dates.empty:
        raise ValueError("close_prices has no valid dates.")

    q0 = dates.iloc[0]
    q1 = dates.iloc[int((len(dates) - 1) * 0.25)]
    q2 = dates.iloc[int((len(dates) - 1) * 0.50)]
    q3 = dates.iloc[int((len(dates) - 1) * 0.75)]
    q4 = dates.iloc[-1]
    return {
        "full_period": (q0, q4),
        "early_period": (q0, q1),
        "middle_period": (q1, q3),
        "recent_period": (q3, q4),
    }


def _daily_cross_sectional_ic(
    signal_panel: pd.DataFrame,
    forward_returns_panel: pd.DataFrame,
    method: str,
) -> pd.DataFrame:
    aligned_signal, aligned_returns = signal_panel.align(forward_returns_panel, join="inner", axis=0)
    aligned_signal, aligned_returns = aligned_signal.align(aligned_returns, join="inner", axis=1)
    rows: list[dict[str, object]] = []

    for date in aligned_signal.index:
        pair = pd.concat(
            [
                pd.to_numeric(aligned_signal.loc[date], errors="coerce").rename("signal"),
                pd.to_numeric(aligned_returns.loc[date], errors="coerce").rename("forward_return"),
            ],
            axis=1,
        ).dropna()
        if len(pair) < 3:
            continue
        daily_ic = pair["signal"].corr(pair["forward_return"], method=method)
        if pd.isna(daily_ic):
            continue
        rows.append({"Date": date, "daily_ic": float(daily_ic), "n_pairs": int(len(pair))})

    return pd.DataFrame(rows)


def score_signal_subset_ic(
    signal_panel: pd.DataFrame,
    forward_returns_panel: pd.DataFrame,
    tickers: list[str] | None = None,
    start_date: str | pd.Timestamp | None = None,
    end_date: str | pd.Timestamp | None = None,
    method: str = "spearman",
    signal_direction: str = "POSITIVE_EDGE",
) -> dict[str, float | int]:
    """Compute raw and direction-adjusted cross-sectional IC for a subset."""
    signal = signal_panel.copy()
    returns = forward_returns_panel.copy()
    signal.index = pd.to_datetime(signal.index, errors="coerce")
    returns.index = pd.to_datetime(returns.index, errors="coerce")

    if tickers is not None:
        selected = [ticker for ticker in tickers if ticker in signal.columns and ticker in returns.columns]
        signal = signal.loc[:, selected]
        returns = returns.loc[:, selected]
    if start_date is not None:
        signal = signal.loc[signal.index >= pd.Timestamp(start_date)]
        returns = returns.loc[returns.index >= pd.Timestamp(start_date)]
    if end_date is not None:
        signal = signal.loc[signal.index <= pd.Timestamp(end_date)]
        returns = returns.loc[returns.index <= pd.Timestamp(end_date)]

    daily_ic = _daily_cross_sectional_ic(signal, returns, method=method)
    if daily_ic.empty:
        return {
            "n_obs": 0,
            "mean_ic_raw": np.nan,
            "mean_ic": np.nan,
            "median_ic": np.nan,
            "ic_std": np.nan,
            "ic_ir": np.nan,
            "positive_ic_rate": np.nan,
            "abs_mean_ic": np.nan,
            "effective_mean_ic": np.nan,
            "effective_ic_ir": np.nan,
            "positive_effective_ic_rate": np.nan,
            "abs_effective_mean_ic": np.nan,
        }

    multiplier = -1.0 if signal_direction == "NEGATIVE_EDGE_REVERSE_SIGNAL" else 1.0
    effective_ic = daily_ic["daily_ic"] * multiplier
    raw_ic = daily_ic["daily_ic"]
    n_obs = int(daily_ic["n_pairs"].sum())
    raw_std = raw_ic.std(ddof=1)
    effective_std = effective_ic.std(ddof=1)
    mean_raw = float(raw_ic.mean())
    mean_effective = float(effective_ic.mean())

    return {
        "n_obs": n_obs,
        "mean_ic_raw": mean_raw,
        "mean_ic": mean_raw,
        "median_ic": float(raw_ic.median()),
        "ic_std": float(raw_std) if not pd.isna(raw_std) else np.nan,
        "ic_ir": float(mean_raw / raw_std) if raw_std and not pd.isna(raw_std) else np.nan,
        "positive_ic_rate": float(raw_ic.gt(0).mean()),
        "abs_mean_ic": abs(mean_raw),
        "effective_mean_ic": mean_effective,
        "effective_ic_ir": float(mean_effective / effective_std) if effective_std and not pd.isna(effective_std) else np.nan,
        "positive_effective_ic_rate": float(effective_ic.gt(0).mean()),
        "abs_effective_mean_ic": abs(mean_effective),
    }


def _pivot_signal_panel(candidate_signals_long: pd.DataFrame, signal_name: str) -> pd.DataFrame:
    selected = candidate_signals_long.loc[candidate_signals_long["signal_name"].eq(signal_name)].copy()
    if selected.empty:
        raise ValueError(f"Signal not found in candidate_signals_long: {signal_name}")
    selected["Date"] = pd.to_datetime(selected["Date"], errors="coerce")
    selected["signal_value"] = pd.to_numeric(selected["signal_value"], errors="coerce")
    panel = selected.pivot(index="Date", columns="ticker", values="signal_value")
    return panel.sort_index().sort_index(axis=1)


def _pass_failure(summary: dict[str, float | int]) -> tuple[int, str]:
    reasons: list[str] = []
    if int(summary["n_obs"]) < PASS_MIN_OBS:
        reasons.append("insufficient observations")
    if pd.isna(summary["effective_mean_ic"]) or float(summary["effective_mean_ic"]) < PASS_MIN_EFFECTIVE_IC:
        reasons.append("weak effective IC")
    if (
        pd.isna(summary["positive_effective_ic_rate"])
        or float(summary["positive_effective_ic_rate"]) < PASS_MIN_POSITIVE_RATE
    ):
        reasons.append("weak sign consistency")
    return (0 if reasons else 1, "; ".join(reasons) if reasons else "passed")


def run_signal_reproducibility_tests(
    candidate_table: pd.DataFrame,
    candidate_signals_long: pd.DataFrame,
    close_prices: pd.DataFrame,
    run_id: str | None = None,
    reproducibility_version: str | None = None,
    method: str = "spearman",
) -> pd.DataFrame:
    """Run universe, subperiod, and recent-universe reproducibility tests."""
    if candidate_table.empty:
        return pd.DataFrame()

    close = close_prices.copy()
    close.index = pd.to_datetime(close.index, errors="coerce")
    close = close.sort_index().apply(pd.to_numeric, errors="coerce")
    universes = build_reproducibility_universes(close)
    subperiods = build_reproducibility_subperiods(close)
    horizons = sorted(candidate_table["horizon"].astype(int).unique().tolist())
    forward_returns = make_forward_returns(close, horizons)

    rows: list[dict[str, object]] = []
    for candidate in candidate_table.itertuples(index=False):
        signal_name = str(candidate.signal_name)
        horizon = int(candidate.horizon)
        signal_direction = getattr(candidate, "signal_direction", "POSITIVE_EDGE")
        signal_panel = _pivot_signal_panel(candidate_signals_long, signal_name)
        forward_panel = forward_returns[horizon]

        tests: list[tuple[str, str, list[str] | None, pd.Timestamp | None, pd.Timestamp | None]] = []
        for universe_name, tickers in universes.items():
            tests.append(("universe", universe_name, tickers, None, None))
        for subperiod_name, (start_date, end_date) in subperiods.items():
            tests.append(("subperiod", subperiod_name, None, start_date, end_date))
        recent_start, recent_end = subperiods["recent_period"]
        for universe_name, tickers in universes.items():
            tests.append(("universe_recent_period", f"{universe_name}__recent_period", tickers, recent_start, recent_end))

        for test_type, test_name, tickers, start_date, end_date in tests:
            result = score_signal_subset_ic(
                signal_panel,
                forward_panel,
                tickers=tickers,
                start_date=start_date,
                end_date=end_date,
                method=method,
                signal_direction=signal_direction,
            )
            pass_flag, failure_reason = _pass_failure(result)
            rows.append(
                {
                    "signal_name": signal_name,
                    "horizon": horizon,
                    "test_type": test_type,
                    "test_name": test_name,
                    "n_obs": result["n_obs"],
                    "mean_ic_raw": result["mean_ic_raw"],
                    "effective_mean_ic": result["effective_mean_ic"],
                    "effective_ic_ir": result["effective_ic_ir"],
                    "positive_effective_ic_rate": result["positive_effective_ic_rate"],
                    "abs_effective_mean_ic": result["abs_effective_mean_ic"],
                    "pass_flag": pass_flag,
                    "failure_reason": failure_reason,
                    "run_id": run_id,
                    "reproducibility_version": reproducibility_version,
                }
            )

    return pd.DataFrame(rows)


def _reproducibility_status(pass_rate: float, worst_effective_mean_ic: float) -> str:
    if pass_rate >= 0.80 and worst_effective_mean_ic >= 0.005:
        return "GLOBAL_PASS"
    if pass_rate >= 0.60:
        return "CONDITIONAL_PASS"
    if pass_rate >= 0.40:
        return "WEAK_OUT_OF_SAMPLE"
    return "REJECT_REPRODUCIBILITY"


def summarize_signal_reproducibility(results: pd.DataFrame) -> pd.DataFrame:
    """Summarize reproducibility detail rows one row per signal/horizon."""
    if results.empty:
        return pd.DataFrame()

    rows: list[dict[str, object]] = []
    for (signal_name, horizon), group in results.groupby(["signal_name", "horizon"], dropna=False):
        n_tests = int(len(group))
        n_passed = int(group["pass_flag"].sum())
        pass_rate = float(n_passed / n_tests) if n_tests else np.nan
        failed_tests = ", ".join(group.loc[group["pass_flag"].eq(0), "test_name"].astype(str).tolist())
        worst_effective_mean_ic = float(group["effective_mean_ic"].min())
        rows.append(
            {
                "signal_name": signal_name,
                "horizon": int(horizon),
                "n_tests": n_tests,
                "n_passed": n_passed,
                "pass_rate": pass_rate,
                "worst_effective_mean_ic": worst_effective_mean_ic,
                "avg_effective_mean_ic": float(group["effective_mean_ic"].mean()),
                "min_positive_effective_ic_rate": float(group["positive_effective_ic_rate"].min()),
                "failed_tests": failed_tests,
                "reproducibility_status": _reproducibility_status(pass_rate, worst_effective_mean_ic),
            }
        )
    return pd.DataFrame(rows).sort_values(["pass_rate", "avg_effective_mean_ic"], ascending=[False, False]).reset_index(drop=True)


def build_reproducibility_final_gate(summary: pd.DataFrame, health_table: pd.DataFrame) -> pd.DataFrame:
    """Join health evidence and reproducibility status into a final research gate."""
    if summary.empty:
        return pd.DataFrame()
    health_columns = [
        "signal_name",
        "horizon",
        "signal_family",
        "signal_health_score",
        "signal_health_gate",
        "repro_candidate_tier",
        "signal_source",
        "orthogonal_version",
        "orthogonal_cluster",
        "signal_version",
    ]
    gate = summary.merge(
        health_table[[column for column in health_columns if column in health_table.columns]],
        on=["signal_name", "horizon"],
        how="left",
    )

    def final_gate(row: pd.Series) -> str:
        if (
            row["signal_health_gate"] == "APPROVED_FOR_RESEARCH"
            and row["reproducibility_status"] in {"GLOBAL_PASS", "CONDITIONAL_PASS"}
        ):
            return "APPROVED_FOR_ALPHA_RESEARCH"
        if (
            row["signal_health_gate"] in {"APPROVED_FOR_RESEARCH", "WATCHLIST_RESEARCH"}
            and row["reproducibility_status"] in {"WEAK_OUT_OF_SAMPLE", "CONDITIONAL_PASS"}
        ):
            return "WATCHLIST_ALPHA_RESEARCH"
        return "REJECTED_ALPHA_RESEARCH"

    gate["final_research_gate"] = gate.apply(final_gate, axis=1)
    columns = [
        "signal_name",
        "horizon",
        "signal_family",
        "repro_candidate_tier",
        "signal_source",
        "orthogonal_version",
        "orthogonal_cluster",
        "signal_version",
        "signal_health_score",
        "signal_health_gate",
        "n_tests",
        "n_passed",
        "pass_rate",
        "avg_effective_mean_ic",
        "worst_effective_mean_ic",
        "reproducibility_status",
        "final_research_gate",
    ]
    return gate[[column for column in columns if column in gate.columns]].sort_values(
        ["final_research_gate", "signal_health_score", "pass_rate"],
        ascending=[True, False, False],
    ).reset_index(drop=True)


def build_signal_reproducibility_summary(
    run_id: str,
    run_timestamp: str,
    reproducibility_version: str,
    candidates: pd.DataFrame,
    candidate_signals_long: pd.DataFrame,
    results: pd.DataFrame,
    summary: pd.DataFrame,
    gate: pd.DataFrame,
) -> pd.DataFrame:
    """Build compact pipeline summary artifacts without changing output schemas."""
    final_gate_counts = (
        gate["final_research_gate"].value_counts(dropna=False).sort_index().astype(int).to_dict()
        if not gate.empty and "final_research_gate" in gate.columns
        else {}
    )
    status_counts = (
        summary["reproducibility_status"].value_counts(dropna=False).sort_index().astype(int).to_dict()
        if not summary.empty and "reproducibility_status" in summary.columns
        else {}
    )
    return pd.DataFrame(
        [
            {"metric": "run_id", "value": run_id},
            {"metric": "run_timestamp", "value": run_timestamp},
            {"metric": "reproducibility_version", "value": reproducibility_version},
            {"metric": "candidate_count", "value": len(candidates)},
            {"metric": "unique_candidate_signals", "value": int(candidates["signal_name"].nunique()) if "signal_name" in candidates else 0},
            {"metric": "candidate_signal_rows_loaded", "value": len(candidate_signals_long)},
            {"metric": "result_rows", "value": len(results)},
            {"metric": "summary_rows", "value": len(summary)},
            {"metric": "gate_rows", "value": len(gate)},
            {"metric": "approved_alpha_research_count", "value": int(final_gate_counts.get("APPROVED_FOR_ALPHA_RESEARCH", 0))},
            {"metric": "watchlist_alpha_research_count", "value": int(final_gate_counts.get("WATCHLIST_ALPHA_RESEARCH", 0))},
            {"metric": "rejected_alpha_research_count", "value": int(final_gate_counts.get("REJECTED_ALPHA_RESEARCH", 0))},
            {"metric": "reproducibility_status_counts", "value": status_counts},
            {"metric": "final_research_gate_counts", "value": final_gate_counts},
        ]
    )


def run_03f_signal_reproducibility(
    db_path: str | Path | None = None,
    reproducibility_version: str = REPRODUCIBILITY_VERSION,
    run_id: str | None = None,
    include_watchlist: bool = INCLUDE_WATCHLIST,
    include_orthogonal_watchlist: bool = INCLUDE_ORTHOGONAL_WATCHLIST,
    orthogonal_watchlist_min_health_score: float = ORTHOGONAL_WATCHLIST_MIN_HEALTH_SCORE,
    orthogonal_watchlist_version: str = ORTHOGONAL_WATCHLIST_VERSION,
    method: str = IC_METHOD,
    write: bool = False,
    verbose: bool = True,
) -> dict[str, object]:
    """Run the 03F signal reproducibility workflow with notebook-equivalent logic."""
    resolved_run_id = run_id or make_run_id("phase2_nb03f_signal_reproducibility")
    run_timestamp = make_run_timestamp()

    if verbose:
        print("03F signal reproducibility: loading candidates")
    reproducibility_candidates = load_reproducibility_candidates(
        db_path=db_path,
        include_watchlist=include_watchlist,
        include_orthogonal_watchlist=include_orthogonal_watchlist,
        orthogonal_watchlist_min_health_score=orthogonal_watchlist_min_health_score,
        orthogonal_watchlist_version=orthogonal_watchlist_version,
    )
    health_table = reproducibility_candidates.copy()
    needed_signals = reproducibility_candidates["signal_name"].dropna().unique().tolist()

    if verbose:
        print(f"03F signal reproducibility: loading {len(needed_signals):,} candidate signal panels")
    close_prices = load_price_table("clean_close_prices_current", db_path=db_path)
    load_context = nullcontext() if verbose else redirect_stdout(StringIO())
    with load_context:
        candidate_signals_long = load_candidate_signals_by_names(
            needed_signals,
            current=True,
            db_path=db_path,
            chunksize=None,
        )

    if verbose:
        print("03F signal reproducibility: running subset IC tests")
    reproducibility_results = run_signal_reproducibility_tests(
        candidate_table=reproducibility_candidates,
        candidate_signals_long=candidate_signals_long,
        close_prices=close_prices,
        run_id=resolved_run_id,
        reproducibility_version=reproducibility_version,
        method=method,
    )
    reproducibility_summary = summarize_signal_reproducibility(reproducibility_results)
    reproducibility_gate = build_reproducibility_final_gate(
        summary=reproducibility_summary,
        health_table=health_table,
    )
    pipeline_summary = build_signal_reproducibility_summary(
        run_id=resolved_run_id,
        run_timestamp=run_timestamp,
        reproducibility_version=reproducibility_version,
        candidates=reproducibility_candidates,
        candidate_signals_long=candidate_signals_long,
        results=reproducibility_results,
        summary=reproducibility_summary,
        gate=reproducibility_gate,
    )

    saved_paths: dict[str, Path] = {}
    if write:
        if verbose:
            print("03F signal reproducibility: writing SQLite outputs")
        saved_paths = save_signal_reproducibility_outputs(
            reproducibility_results=reproducibility_results,
            reproducibility_summary=reproducibility_summary,
            reproducibility_gate=reproducibility_gate,
            db_path=db_path,
            run_id=resolved_run_id,
            reproducibility_version=reproducibility_version,
        )

    return {
        "run_id": resolved_run_id,
        "run_timestamp": run_timestamp,
        "reproducibility_version": reproducibility_version,
        "reproducibility_candidates": reproducibility_candidates,
        "health_table": health_table,
        "close_prices": close_prices,
        "candidate_signals_long": candidate_signals_long,
        "candidate_signal_rows_loaded": len(candidate_signals_long),
        "reproducibility_results": reproducibility_results,
        "reproducibility_summary": reproducibility_summary,
        "reproducibility_gate": reproducibility_gate,
        "summary": pipeline_summary,
        "saved_paths": saved_paths,
    }


__all__ = [
    "build_reproducibility_final_gate",
    "build_reproducibility_subperiods",
    "build_reproducibility_universes",
    "build_signal_reproducibility_summary",
    "IC_METHOD",
    "INCLUDE_ORTHOGONAL_WATCHLIST",
    "INCLUDE_WATCHLIST",
    "load_reproducibility_candidates",
    "ORTHOGONAL_WATCHLIST_MIN_HEALTH_SCORE",
    "ORTHOGONAL_WATCHLIST_VERSION",
    "PASS_MIN_EFFECTIVE_IC",
    "PASS_MIN_OBS",
    "PASS_MIN_POSITIVE_RATE",
    "REPRODUCIBILITY_VERSION",
    "REQUIRED_INPUT_TABLES",
    "run_03f_signal_reproducibility",
    "run_signal_reproducibility_tests",
    "score_signal_subset_ic",
    "summarize_signal_reproducibility",
]
