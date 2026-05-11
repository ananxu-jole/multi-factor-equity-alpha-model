from __future__ import annotations

import sqlite3
from pathlib import Path

import numpy as np
import pandas as pd

from src.run_config import make_run_id, make_run_timestamp
from src.run_config import get_sqlite_db_path
from src.scoring.health_storage import save_signal_health_outputs


HEALTH_VERSION = "phase2_signal_health_v1"
REQUIRED_INPUT_TABLES = (
    "signal_best_horizon_current",
    "signal_scoring_gate_current",
    "signal_decay_summary_current",
    "signal_regime_opportunity_summary_current",
)
HEALTH_SCORE_COLUMNS = [
    "signal_name",
    "horizon",
    "signal_family",
    "signal_direction",
    "signal_strength",
    "best_mean_ic",
    "best_abs_mean_ic",
    "best_ic_ir",
    "scoring_status",
    "decay_status",
    "decay_risk_flag",
    "mean_rolling_ic",
    "recent_ic",
    "early_ic",
    "ic_change",
    "sign_stability",
    "adjusted_best_abs_ic",
    "recommended_use",
    "regime_fragility_flag",
    "regime_consistency_score",
    "regime_sample_weight",
    "wfv_status",
    "direction_flip_warning",
    "effective_mean_test_ic",
    "effective_test_ic_ir",
    "persistence_ratio",
    "signal_health_score",
    "signal_health_gate",
    "health_notes",
    "run_id",
    "health_version",
]

HEALTH_ATTRIBUTION_COLUMNS = [
    "signal_name",
    "horizon",
    "signal_family",
    "signal_health_score",
    "signal_health_gate",
    "ic_strength_points",
    "ic_ir_points",
    "decay_stability_points",
    "sign_stability_points",
    "regime_opportunity_points",
    "wfv_points",
    "direction_flip_penalty",
    "avoid_penalty",
    "no_signal_penalty",
    "low_regime_consistency_penalty",
    "total_positive_points",
    "total_penalty_points",
    "final_score",
    "biggest_positive_driver",
    "biggest_penalty_driver",
]


def _quote_identifier(identifier: str) -> str:
    return '"' + identifier.replace('"', '""') + '"'


def _load_optional_table(conn: sqlite3.Connection, table_name: str) -> pd.DataFrame | None:
    exists = conn.execute(
        """
        SELECT 1
        FROM sqlite_master
        WHERE type = 'table'
          AND name = ?
        LIMIT 1
        """,
        (table_name,),
    ).fetchone()
    if not exists:
        return None
    return pd.read_sql_query(f"SELECT * FROM {_quote_identifier(table_name)}", conn)


def load_signal_health_inputs(db_path: str | Path | None = None) -> dict[str, pd.DataFrame | None]:
    """Load current scoring, decay, regime, and optional WFV diagnostics from SQLite."""
    db_path = Path(db_path) if db_path is not None else get_sqlite_db_path()
    required_tables = {
        "best_horizon": "signal_best_horizon_current",
        "scoring_gate": "signal_scoring_gate_current",
        "decay_summary": "signal_decay_summary_current",
        "regime_opportunity": "signal_regime_opportunity_summary_current",
    }

    with sqlite3.connect(db_path) as conn:
        inputs: dict[str, pd.DataFrame | None] = {}
        for key, table_name in required_tables.items():
            loaded = _load_optional_table(conn, table_name)
            if loaded is None:
                raise ValueError(f"Required signal health input table is missing: {table_name}")
            inputs[key] = loaded
        inputs["wfv_gate"] = _load_optional_table(conn, "wfv_gate_current")

    return inputs


def _score_ic_strength(best_abs_mean_ic: float) -> int:
    if pd.isna(best_abs_mean_ic):
        return 0
    if best_abs_mean_ic >= 0.04:
        return 25
    if best_abs_mean_ic >= 0.03:
        return 20
    if best_abs_mean_ic >= 0.02:
        return 15
    if best_abs_mean_ic >= 0.012:
        return 10
    return 0


def _score_ic_ir(best_ic_ir: float) -> int:
    if pd.isna(best_ic_ir):
        return 0
    abs_ic_ir = abs(float(best_ic_ir))
    if abs_ic_ir >= 0.15:
        return 15
    if abs_ic_ir >= 0.10:
        return 12
    if abs_ic_ir >= 0.05:
        return 8
    return 0


def _score_decay(decay_risk_flag: str) -> int:
    return {
        "LOW_DECAY_RISK": 20,
        "MODERATE_DECAY_RISK": 12,
        "HIGH_DECAY_RISK": 0,
    }.get(str(decay_risk_flag), 0)


def _score_sign_stability(sign_stability: float) -> int:
    if pd.isna(sign_stability):
        return 0
    if sign_stability >= 0.65:
        return 10
    if sign_stability >= 0.60:
        return 8
    if sign_stability >= 0.55:
        return 5
    return 0


def _score_regime_opportunity(adjusted_best_abs_ic: float) -> int:
    if pd.isna(adjusted_best_abs_ic):
        return 0
    if adjusted_best_abs_ic >= 0.08:
        return 15
    if adjusted_best_abs_ic >= 0.05:
        return 12
    if adjusted_best_abs_ic >= 0.03:
        return 8
    if adjusted_best_abs_ic >= 0.015:
        return 5
    return 0


def _score_wfv(wfv_status: str) -> int:
    return {
        "APPROVED_WFV": 15,
        "WATCHLIST_WFV": 8,
        "REJECTED_WFV": 0,
    }.get(str(wfv_status), 0)


def _as_warning(value: object) -> int:
    if pd.isna(value):
        return 0
    return int(float(value) == 1.0)


def _build_health_notes(row: pd.Series) -> str:
    notes: list[str] = []
    if row["signal_health_gate"] == "APPROVED_FOR_RESEARCH":
        notes.append("Strong multi-diagnostic research candidate")
    elif row["signal_health_gate"] == "WATCHLIST_RESEARCH":
        notes.append("Mixed evidence; monitor before promotion")
    else:
        notes.append("Insufficient combined evidence")

    if row.get("wfv_status") == "REJECTED_WFV":
        notes.append("WFV rejected")
    if row.get("direction_flip_warning", 0) == 1:
        notes.append("direction flip warning")
    if row.get("recommended_use") == "AVOID":
        notes.append("regime opportunity avoid")
    if row.get("decay_risk_flag") == "HIGH_DECAY_RISK":
        notes.append("high decay risk")
    if row.get("signal_strength") == "NO_SIGNAL":
        notes.append("low scoring signal strength")
    if not pd.isna(row.get("regime_consistency_score")) and row.get("regime_consistency_score") < 0.50:
        notes.append("low regime consistency")
    return "; ".join(notes)


def _compute_health_score(row: pd.Series) -> float:
    score = (
        _score_ic_strength(row.get("best_abs_mean_ic"))
        + _score_ic_ir(row.get("best_ic_ir"))
        + _score_decay(row.get("decay_risk_flag"))
        + _score_sign_stability(row.get("sign_stability"))
        + _score_regime_opportunity(row.get("adjusted_best_abs_ic"))
        + _score_wfv(row.get("wfv_status"))
    )

    if row.get("direction_flip_warning", 0) == 1:
        score -= 20
    if row.get("recommended_use") == "AVOID":
        score -= 20
    if row.get("signal_strength") == "NO_SIGNAL":
        score -= 10
    if not pd.isna(row.get("regime_consistency_score")) and row.get("regime_consistency_score") < 0.50:
        score -= 10

    return float(np.clip(score, 0, 100))


def _health_gate(row: pd.Series) -> str:
    if (
        row["signal_health_score"] >= 70
        and row.get("recommended_use") != "AVOID"
        and row.get("decay_risk_flag") != "HIGH_DECAY_RISK"
        and row.get("direction_flip_warning", 0) != 1
    ):
        return "APPROVED_FOR_RESEARCH"
    if row["signal_health_score"] >= 45 and row.get("recommended_use") != "AVOID":
        return "WATCHLIST_RESEARCH"
    return "REJECTED_RESEARCH"


def build_signal_health_table(
    best_horizon: pd.DataFrame,
    scoring_gate: pd.DataFrame,
    decay_summary: pd.DataFrame,
    regime_opportunity: pd.DataFrame,
    wfv_gate: pd.DataFrame | None = None,
    run_id: str | None = None,
    health_version: str | None = None,
) -> pd.DataFrame:
    """Combine scoring, decay, regime, and WFV diagnostics into a research health gate."""
    required_base = {"signal_name", "horizon", "status"}
    missing_base = required_base.difference(scoring_gate.columns)
    if missing_base:
        raise ValueError(f"scoring_gate is missing required columns: {sorted(missing_base)}")

    base_columns = [
        "signal_name",
        "horizon",
        "signal_family",
        "signal_direction",
        "signal_strength",
        "status",
    ]
    health = scoring_gate[[column for column in base_columns if column in scoring_gate.columns]].copy()
    health = health.rename(columns={"status": "scoring_status"})

    best_columns = [
        "signal_name",
        "best_horizon",
        "best_mean_ic",
        "best_abs_mean_ic",
        "best_ic_ir",
    ]
    best = best_horizon[[column for column in best_columns if column in best_horizon.columns]].copy()
    health = health.merge(best, on="signal_name", how="left")

    decay_columns = [
        "signal_name",
        "horizon",
        "decay_status",
        "decay_risk_flag",
        "mean_rolling_ic",
        "recent_ic",
        "early_ic",
        "ic_change",
        "sign_stability",
    ]
    decay = decay_summary[[column for column in decay_columns if column in decay_summary.columns]].copy()
    health = health.merge(decay, on=["signal_name", "horizon"], how="left")

    regime_columns = [
        "signal_name",
        "horizon",
        "adjusted_best_abs_ic",
        "recommended_use",
        "regime_fragility_flag",
        "regime_consistency_score",
        "regime_sample_weight",
    ]
    regime = regime_opportunity[
        [column for column in regime_columns if column in regime_opportunity.columns]
    ].copy()
    health = health.merge(regime, on=["signal_name", "horizon"], how="left")

    if wfv_gate is not None and not wfv_gate.empty:
        wfv_columns = [
            "signal_name",
            "horizon",
            "status",
            "direction_flip_warning",
            "effective_mean_test_ic",
            "effective_test_ic_ir",
            "persistence_ratio",
        ]
        wfv = wfv_gate[[column for column in wfv_columns if column in wfv_gate.columns]].copy()
        wfv = wfv.rename(columns={"status": "wfv_status"})
        health = health.merge(wfv, on=["signal_name", "horizon"], how="left")
    else:
        health["wfv_status"] = np.nan
        health["direction_flip_warning"] = np.nan
        health["effective_mean_test_ic"] = np.nan
        health["effective_test_ic_ir"] = np.nan
        health["persistence_ratio"] = np.nan

    health["wfv_status"] = health["wfv_status"].fillna("MISSING_WFV")
    health["direction_flip_warning"] = health["direction_flip_warning"].map(_as_warning)
    health["signal_health_score"] = health.apply(_compute_health_score, axis=1)
    health["signal_health_gate"] = health.apply(_health_gate, axis=1)
    health["health_notes"] = health.apply(_build_health_notes, axis=1)
    health["run_id"] = run_id
    health["health_version"] = health_version

    return (
        health[[column for column in HEALTH_SCORE_COLUMNS if column in health.columns]]
        .sort_values(["signal_health_score", "signal_name", "horizon"], ascending=[False, True, True])
        .reset_index(drop=True)
    )


def build_signal_health_summary(signal_health_table: pd.DataFrame) -> pd.DataFrame:
    """Build a one-row summary of signal health gate outcomes."""
    if signal_health_table.empty:
        return pd.DataFrame(
            [
                {
                    "n_signals": 0,
                    "n_approved": 0,
                    "n_watchlist": 0,
                    "n_rejected": 0,
                    "avg_health_score": np.nan,
                    "max_health_score": np.nan,
                    "best_signal_name": np.nan,
                    "best_signal_horizon": np.nan,
                    "health_version": np.nan,
                    "run_id": np.nan,
                }
            ]
        )

    gates = signal_health_table["signal_health_gate"]
    best = signal_health_table.sort_values(
        ["signal_health_score", "signal_name", "horizon"],
        ascending=[False, True, True],
    ).iloc[0]
    return pd.DataFrame(
        [
            {
                "n_signals": int(len(signal_health_table)),
                "n_approved": int(gates.eq("APPROVED_FOR_RESEARCH").sum()),
                "n_watchlist": int(gates.eq("WATCHLIST_RESEARCH").sum()),
                "n_rejected": int(gates.eq("REJECTED_RESEARCH").sum()),
                "avg_health_score": float(signal_health_table["signal_health_score"].mean()),
                "max_health_score": float(signal_health_table["signal_health_score"].max()),
                "best_signal_name": best["signal_name"],
                "best_signal_horizon": int(best["horizon"]),
                "health_version": best.get("health_version"),
                "run_id": best.get("run_id"),
            }
        ]
    )


def _largest_driver(row: pd.Series, columns: list[str], no_driver_label: str) -> str:
    values = row[columns]
    if values.empty:
        return no_driver_label
    best_column = values.idxmax()
    return str(best_column) if values[best_column] > 0 else no_driver_label


def _largest_penalty(row: pd.Series, columns: list[str], no_driver_label: str) -> str:
    values = row[columns]
    if values.empty:
        return no_driver_label
    worst_column = values.idxmin()
    return str(worst_column) if values[worst_column] < 0 else no_driver_label


def build_signal_health_attribution(health_table: pd.DataFrame) -> pd.DataFrame:
    """Break the existing health score into auditable point and penalty components."""
    if health_table.empty:
        return pd.DataFrame(columns=HEALTH_ATTRIBUTION_COLUMNS)

    attribution = health_table[
        [
            "signal_name",
            "horizon",
            "signal_family",
            "signal_health_score",
            "signal_health_gate",
            "best_abs_mean_ic",
            "best_ic_ir",
            "decay_risk_flag",
            "sign_stability",
            "adjusted_best_abs_ic",
            "wfv_status",
            "direction_flip_warning",
            "recommended_use",
            "signal_strength",
            "regime_consistency_score",
        ]
    ].copy()

    attribution["ic_strength_points"] = attribution["best_abs_mean_ic"].map(_score_ic_strength)
    attribution["ic_ir_points"] = attribution["best_ic_ir"].map(_score_ic_ir)
    attribution["decay_stability_points"] = attribution["decay_risk_flag"].map(_score_decay)
    attribution["sign_stability_points"] = attribution["sign_stability"].map(_score_sign_stability)
    attribution["regime_opportunity_points"] = attribution["adjusted_best_abs_ic"].map(
        _score_regime_opportunity
    )
    attribution["wfv_points"] = attribution["wfv_status"].map(_score_wfv)

    attribution["direction_flip_penalty"] = np.where(
        attribution["direction_flip_warning"].eq(1),
        -20,
        0,
    )
    attribution["avoid_penalty"] = np.where(attribution["recommended_use"].eq("AVOID"), -20, 0)
    attribution["no_signal_penalty"] = np.where(
        attribution["signal_strength"].eq("NO_SIGNAL"),
        -10,
        0,
    )
    attribution["low_regime_consistency_penalty"] = np.where(
        attribution["regime_consistency_score"].lt(0.50),
        -10,
        0,
    )

    positive_columns = [
        "ic_strength_points",
        "ic_ir_points",
        "decay_stability_points",
        "sign_stability_points",
        "regime_opportunity_points",
        "wfv_points",
    ]
    penalty_columns = [
        "direction_flip_penalty",
        "avoid_penalty",
        "no_signal_penalty",
        "low_regime_consistency_penalty",
    ]
    attribution["total_positive_points"] = attribution[positive_columns].sum(axis=1)
    attribution["total_penalty_points"] = attribution[penalty_columns].sum(axis=1)
    attribution["final_score"] = attribution["signal_health_score"]
    attribution["biggest_positive_driver"] = attribution.apply(
        _largest_driver,
        axis=1,
        columns=positive_columns,
        no_driver_label="NO_POSITIVE_DRIVER",
    )
    attribution["biggest_penalty_driver"] = attribution.apply(
        _largest_penalty,
        axis=1,
        columns=penalty_columns,
        no_driver_label="NO_PENALTY",
    )

    computed_score = (
        attribution["total_positive_points"] + attribution["total_penalty_points"]
    ).clip(lower=0, upper=100)
    if not np.allclose(computed_score, attribution["signal_health_score"], equal_nan=True):
        raise ValueError("Signal health attribution does not match signal_health_score.")

    return (
        attribution[HEALTH_ATTRIBUTION_COLUMNS]
        .sort_values(["signal_health_score", "signal_name", "horizon"], ascending=[False, True, True])
        .reset_index(drop=True)
    )


def build_signal_health_pipeline_summary(
    run_id: str,
    run_timestamp: str,
    health_version: str,
    signal_health_table: pd.DataFrame,
    signal_health_summary: pd.DataFrame,
    signal_health_attribution: pd.DataFrame,
) -> pd.DataFrame:
    """Build compact pipeline summary artifacts without changing output schemas."""
    gate_counts = (
        signal_health_table["signal_health_gate"].value_counts(dropna=False).sort_index().astype(int).to_dict()
        if not signal_health_table.empty and "signal_health_gate" in signal_health_table.columns
        else {}
    )
    return pd.DataFrame(
        [
            {"metric": "run_id", "value": run_id},
            {"metric": "run_timestamp", "value": run_timestamp},
            {"metric": "health_version", "value": health_version},
            {"metric": "score_rows", "value": len(signal_health_table)},
            {"metric": "summary_rows", "value": len(signal_health_summary)},
            {"metric": "attribution_rows", "value": len(signal_health_attribution)},
            {"metric": "approved_count", "value": int(gate_counts.get("APPROVED_FOR_RESEARCH", 0))},
            {"metric": "watchlist_count", "value": int(gate_counts.get("WATCHLIST_RESEARCH", 0))},
            {"metric": "rejected_count", "value": int(gate_counts.get("REJECTED_RESEARCH", 0))},
            {"metric": "health_gate_counts", "value": gate_counts},
        ]
    )


def run_03e_signal_health(
    db_path: str | Path | None = None,
    health_version: str = HEALTH_VERSION,
    run_id: str | None = None,
    write: bool = False,
    verbose: bool = True,
) -> dict[str, object]:
    """Run the 03E signal health workflow with notebook-equivalent logic."""
    resolved_run_id = run_id or make_run_id("phase2_nb03e_signal_health")
    run_timestamp = make_run_timestamp()

    if verbose:
        print("03E signal health: loading inputs")
    health_inputs = load_signal_health_inputs(db_path=db_path)

    if verbose:
        print("03E signal health: building score and attribution tables")
    signal_health_table = build_signal_health_table(
        best_horizon=health_inputs["best_horizon"],
        scoring_gate=health_inputs["scoring_gate"],
        decay_summary=health_inputs["decay_summary"],
        regime_opportunity=health_inputs["regime_opportunity"],
        wfv_gate=health_inputs.get("wfv_gate"),
        run_id=resolved_run_id,
        health_version=health_version,
    )
    signal_health_attribution = build_signal_health_attribution(signal_health_table)
    signal_health_summary = build_signal_health_summary(signal_health_table)
    pipeline_summary = build_signal_health_pipeline_summary(
        run_id=resolved_run_id,
        run_timestamp=run_timestamp,
        health_version=health_version,
        signal_health_table=signal_health_table,
        signal_health_summary=signal_health_summary,
        signal_health_attribution=signal_health_attribution,
    )

    saved_paths: dict[str, Path] = {}
    if write:
        if verbose:
            print("03E signal health: writing SQLite outputs")
        saved_paths = save_signal_health_outputs(
            signal_health_score=signal_health_table,
            signal_health_summary=signal_health_summary,
            signal_health_attribution=signal_health_attribution,
            db_path=db_path,
            run_id=resolved_run_id,
            health_version=health_version,
        )

    return {
        "run_id": resolved_run_id,
        "run_timestamp": run_timestamp,
        "health_version": health_version,
        "health_inputs": health_inputs,
        "signal_health_score": signal_health_table,
        "signal_health_summary": signal_health_summary,
        "signal_health_attribution": signal_health_attribution,
        "summary": pipeline_summary,
        "saved_paths": saved_paths,
    }


__all__ = [
    "HEALTH_ATTRIBUTION_COLUMNS",
    "HEALTH_SCORE_COLUMNS",
    "HEALTH_VERSION",
    "build_signal_health_attribution",
    "build_signal_health_pipeline_summary",
    "build_signal_health_summary",
    "build_signal_health_table",
    "load_signal_health_inputs",
    "REQUIRED_INPUT_TABLES",
    "run_03e_signal_health",
]
