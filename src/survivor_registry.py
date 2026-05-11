from __future__ import annotations

import pandas as pd

from src.alpha_stress import APPROVED_STRESS
from src.db import load_table


APPROVED_SURVIVOR = "APPROVED_SURVIVOR"
PRIMARY_PROMOTION_DECISIONS = ["PROMOTE_CORE", "PROMOTE_BALANCED", "REVIEW_SATELLITE"]
CORE_ELIGIBLE_PROMOTION_DECISIONS = ["PROMOTE_CORE", "PROMOTE_BALANCED"]

CONSTRUCTED_SURVIVOR_FINAL_STATUS = {
    "CORE_STRESS_SURVIVOR": "CORE_ALPHA_SURVIVOR",
    "BALANCED_STRESS_SURVIVOR": "BALANCED_ALPHA_SURVIVOR",
    "AGGRESSIVE_STRESS_SURVIVOR": "AGGRESSIVE_ALPHA_SURVIVOR",
    "WATCH_STRESS_SURVIVOR": "WATCH_ALPHA_SURVIVOR",
}

CONSTRUCTED_SURVIVOR_REGISTRY_COLUMNS = [
    "survivor_id",
    "alpha_name",
    "horizon",
    "final_status",
    "survivor_tier",
    "promotion_decision",
    "alpha_role",
    "failure_category",
    "interpretation_notes",
    "stress_status",
    "source_wfv_status",
    "pass_rate",
    "worst_degradation",
    "turnover_risk_flag",
    "avg_turnover_proxy",
    "source_construction_version",
    "alpha_construction_version",
    "stress_version",
    "component_signals",
    "component_horizons",
    "weighting_method",
    "direction_adjusted",
    "regime_aware",
    "construction_quality_status",
    "date_frozen",
    "survivor_version",
    "run_id",
    "timestamp_frozen",
]

CORRELATION_AWARE_SURVIVOR_REGISTRY_COLUMNS = [
    "survivor_id",
    "alpha_name",
    "horizon",
    "alpha_sleeve",
    "original_promotion_decision",
    "promotion_decision_final",
    "final_status",
    "alpha_role",
    "survivor_tier",
    "survivor_selection_score",
    "alpha_behavior_cluster",
    "cluster_rank",
    "cluster_selection_role",
    "cluster_selection_reason",
    "max_corr_to_selected_core",
    "correlated_with_core_alpha",
    "pass_rate",
    "worst_degradation",
    "avg_turnover_proxy",
    "turnover_risk_flag",
    "stress_status",
    "source_wfv_status",
    "failure_category",
    "interpretation_notes",
    "stress_version",
    "alpha_construction_version",
    "date_frozen",
    "survivor_version",
    "run_id",
    "timestamp_frozen",
]

SURVIVOR_CLUSTER_SUMMARY_COLUMNS = [
    "alpha_behavior_cluster",
    "alpha_sleeve",
    "n_candidates",
    "n_promote_core_original",
    "n_review_satellite",
    "n_final_core",
    "best_alpha_name",
    "best_score",
    "best_final_status",
    "avg_abs_corr_with_selected_core",
    "cluster_decision",
    "survivor_version",
    "run_id",
]

SURVIVOR_ALPHA_CORRELATION_COLUMNS = [
    "alpha_name_1",
    "alpha_name_2",
    "correlation",
    "abs_correlation",
    "alpha_1_promotion_decision",
    "alpha_2_promotion_decision",
    "alpha_1_pass_rate",
    "alpha_2_pass_rate",
    "alpha_1_worst_degradation",
    "alpha_2_worst_degradation",
    "survivor_version",
    "run_id",
]

SURVIVOR_REGISTRY_COLUMNS = [
    "survivor_id",
    "alpha_name",
    "source_signal",
    "horizon",
    "regime_column",
    "allowed_regimes",
    "signal_direction",
    "alpha_direction",
    "direction_multiplier",
    "active_pct",
    "n_active_dates",
    "avg_active_tickers_per_active_day",
    "effective_mean_test_ic",
    "effective_test_ic_ir",
    "persistence_ratio",
    "sign_consistency",
    "n_stress_cases",
    "n_passed",
    "pass_rate",
    "worst_degradation",
    "worst_stress_type",
    "worst_stress_case",
    "final_status",
    "survivor_version",
    "run_id",
    "timestamp_frozen",
]

PRE_ML_ALPHA_INPUT_COLUMNS = [
    "Date",
    "ticker",
    "alpha_name",
    "alpha_value",
    "horizon",
    "survivor_id",
    "survivor_version",
    "run_id",
]

SURVIVOR_FREEZE_REPORT_COLUMNS = [
    "survivor_version",
    "n_survivors",
    "survivor_names",
    "date_frozen",
    "notes",
]

SURVIVOR_VALIDATION_REPORT_COLUMNS = [
    "check_name",
    "passed",
    "details",
]

SURVIVOR_LINEAGE_REPORT_COLUMNS = [
    "survivor_id",
    "alpha_name",
    "source_signal",
    "regime_column",
    "allowed_regimes",
    "survivor_version",
    "alpha_version",
    "alpha_wfv_version",
    "stress_version",
    "run_id",
    "timestamp_frozen",
]


def load_stress_approved_alphas() -> pd.DataFrame:
    """Load Notebook 7 stress gate winners from the current SQLite artifact."""
    stress_gate = load_table("alpha_stress_gate_current")
    if stress_gate.empty:
        return pd.DataFrame(columns=stress_gate.columns)
    if "promotion_decision" in stress_gate.columns:
        return stress_gate.loc[
            stress_gate["promotion_decision"].isin(CORE_ELIGIBLE_PROMOTION_DECISIONS)
        ].reset_index(drop=True)
    if "status" in stress_gate.columns:
        return stress_gate.loc[stress_gate["status"].eq(APPROVED_STRESS)].reset_index(drop=True)
    return pd.DataFrame(columns=stress_gate.columns)


def load_constructed_stress_approved_alphas() -> pd.DataFrame:
    """Load constructed-alpha stress survivors from Notebook 7."""
    return load_stress_approved_alphas()


def _normalize_horizon(df: pd.DataFrame) -> pd.DataFrame:
    output = df.copy()
    if "horizon" in output.columns:
        output["horizon"] = pd.to_numeric(output["horizon"], errors="coerce").astype("Int64")
    return output


def _join_on_alpha_horizon(left: pd.DataFrame, right: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    if right.empty:
        return left

    available_columns = [column for column in columns if column in right.columns]
    if not {"alpha_name", "horizon"}.issubset(available_columns):
        return left

    right_subset = (
        _normalize_horizon(right[available_columns])
        .drop_duplicates(["alpha_name", "horizon"])
    )
    return left.merge(right_subset, on=["alpha_name", "horizon"], how="left")


def _join_on_alpha_name(left: pd.DataFrame, right: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    if right.empty:
        return left
    available_columns = [column for column in columns if column in right.columns]
    if "alpha_name" not in available_columns:
        return left
    right_subset = right[available_columns].drop_duplicates("alpha_name")
    return left.merge(right_subset, on="alpha_name", how="left")


def _constructed_final_status(survivor_tier: object) -> str:
    return CONSTRUCTED_SURVIVOR_FINAL_STATUS.get(str(survivor_tier), "REJECTED_SURVIVOR")


def build_constructed_survivor_alpha_registry(
    stress_gate: pd.DataFrame,
    stress_audit: pd.DataFrame,
    construction_metadata: pd.DataFrame,
    construction_quality: pd.DataFrame,
    construction_diagnostics: pd.DataFrame,
    survivor_version: str,
    run_id: str,
    timestamp_frozen: str,
    constructed_alpha_wfv_gate: pd.DataFrame | None = None,
) -> pd.DataFrame:
    """Build one immutable registry row per stress-approved constructed alpha survivor."""
    if stress_gate.empty:
        return pd.DataFrame(columns=CONSTRUCTED_SURVIVOR_REGISTRY_COLUMNS)

    survivors = _normalize_horizon(stress_gate.copy())
    if "promotion_decision" in survivors.columns:
        survivors = survivors.loc[
            survivors["promotion_decision"].isin(CORE_ELIGIBLE_PROMOTION_DECISIONS)
        ].copy()
    elif "status" in survivors.columns:
        survivors = survivors.loc[survivors["status"].eq(APPROVED_STRESS)].copy()
    if survivors.empty:
        return pd.DataFrame(columns=CONSTRUCTED_SURVIVOR_REGISTRY_COLUMNS)

    base_columns = [
        "alpha_name",
        "horizon",
        "survivor_tier",
        "promotion_decision",
        "alpha_role",
        "failure_category",
        "interpretation_notes",
        "status",
        "pass_rate",
        "worst_degradation",
        "turnover_risk_flag",
        "avg_turnover_proxy",
        "stress_version",
    ]
    survivors = survivors[[column for column in base_columns if column in survivors.columns]].drop_duplicates(
        ["alpha_name", "horizon"]
    )
    survivors = survivors.rename(columns={"status": "stress_status"})

    survivors = _join_on_alpha_horizon(
        survivors,
        stress_audit,
        [
            "alpha_name",
            "horizon",
            "worst_degradation",
            "turnover_risk_flag",
            "avg_turnover_proxy",
            "stress_version",
            "promotion_decision",
            "alpha_role",
            "failure_category",
            "interpretation_notes",
        ],
    )
    for column in [
        "worst_degradation",
        "turnover_risk_flag",
        "avg_turnover_proxy",
        "stress_version",
        "promotion_decision",
        "alpha_role",
        "failure_category",
        "interpretation_notes",
    ]:
        audit_column = f"{column}_y"
        base_column = f"{column}_x"
        if audit_column in survivors.columns:
            survivors[column] = survivors.get(base_column).combine_first(survivors[audit_column])
            survivors = survivors.drop(columns=[c for c in [base_column, audit_column] if c in survivors.columns])

    survivors = _join_on_alpha_name(
        survivors,
        construction_metadata,
        [
            "alpha_name",
            "component_signals",
            "component_horizons",
            "weighting_method",
            "direction_adjusted",
            "regime_aware",
            "alpha_construction_version",
        ],
    )
    survivors = survivors.rename(columns={"alpha_construction_version": "source_construction_version"})
    survivors = _join_on_alpha_name(
        survivors,
        construction_quality.rename(columns={"status": "construction_quality_status"}),
        [
            "alpha_name",
            "construction_quality_status",
            "alpha_construction_version",
        ],
    )
    if "source_construction_version" not in survivors.columns and "alpha_construction_version" in survivors.columns:
        survivors = survivors.rename(columns={"alpha_construction_version": "source_construction_version"})
    elif "alpha_construction_version" in survivors.columns:
        survivors["source_construction_version"] = survivors["source_construction_version"].combine_first(
            survivors["alpha_construction_version"]
        )
        survivors = survivors.drop(columns=["alpha_construction_version"])
    survivors["alpha_construction_version"] = survivors.get("source_construction_version")

    if constructed_alpha_wfv_gate is not None and not constructed_alpha_wfv_gate.empty:
        wfv_status = _join_on_alpha_horizon(
            survivors[["alpha_name", "horizon"]].drop_duplicates(),
            constructed_alpha_wfv_gate.rename(columns={"status": "source_wfv_status"}),
            ["alpha_name", "horizon", "source_wfv_status"],
        )
        survivors = _normalize_horizon(survivors).merge(
            wfv_status,
            on=["alpha_name", "horizon"],
            how="left",
        )

    survivors = _join_on_alpha_name(
        survivors,
        construction_diagnostics,
        [
            "alpha_name",
            "avg_turnover_proxy",
            "turnover_risk_flag",
        ],
    )
    for column in ["avg_turnover_proxy", "turnover_risk_flag"]:
        diagnostic_column = f"{column}_y"
        base_column = f"{column}_x"
        if diagnostic_column in survivors.columns:
            survivors[column] = survivors.get(base_column).combine_first(survivors[diagnostic_column])
            survivors = survivors.drop(columns=[c for c in [base_column, diagnostic_column] if c in survivors.columns])

    survivors["horizon"] = survivors["horizon"].astype(int)
    survivors["final_status"] = survivors["survivor_tier"].map(_constructed_final_status)
    survivors["survivor_version"] = survivor_version
    survivors["run_id"] = run_id
    survivors["timestamp_frozen"] = timestamp_frozen
    survivors["date_frozen"] = pd.to_datetime(timestamp_frozen, errors="coerce").date().isoformat()
    survivors["survivor_id"] = survivors.apply(
        lambda row: f"{survivor_version}::{row['alpha_name']}::{int(row['horizon'])}d",
        axis=1,
    )

    return (
        survivors.reindex(columns=CONSTRUCTED_SURVIVOR_REGISTRY_COLUMNS)
        .sort_values(["final_status", "alpha_name", "horizon"])
        .reset_index(drop=True)
    )


def build_survivor_alpha_registry(
    stress_gate: pd.DataFrame,
    alpha_metadata: pd.DataFrame,
    alpha_quality: pd.DataFrame,
    alpha_wfv_gate: pd.DataFrame,
    alpha_stress_audit: pd.DataFrame,
    survivor_version: str,
    run_id: str,
    timestamp_frozen: str,
) -> pd.DataFrame:
    """Build one immutable registry row per stress-approved survivor alpha."""
    if stress_gate.empty:
        return pd.DataFrame(columns=SURVIVOR_REGISTRY_COLUMNS)

    survivors = _normalize_horizon(stress_gate.copy())
    if "status" in survivors.columns:
        survivors = survivors.loc[survivors["status"].eq(APPROVED_STRESS)].copy()

    survivors = survivors[["alpha_name", "horizon"]].drop_duplicates()
    if survivors.empty:
        return pd.DataFrame(columns=SURVIVOR_REGISTRY_COLUMNS)

    survivors = _join_on_alpha_horizon(
        survivors,
        alpha_metadata,
        [
            "alpha_name",
            "horizon",
            "source_signal",
            "regime_column",
            "allowed_regimes",
            "signal_direction",
            "direction_multiplier",
        ],
    )
    survivors = _join_on_alpha_horizon(
        survivors,
        alpha_quality,
        [
            "alpha_name",
            "horizon",
            "active_pct",
            "n_active_dates",
            "avg_active_tickers_per_active_day",
        ],
    )
    survivors = _join_on_alpha_horizon(
        survivors,
        alpha_wfv_gate,
        [
            "alpha_name",
            "horizon",
            "alpha_direction",
            "effective_mean_test_ic",
            "effective_test_ic_ir",
            "persistence_ratio",
            "sign_consistency",
        ],
    )
    survivors = _join_on_alpha_horizon(
        survivors,
        alpha_stress_audit,
        [
            "alpha_name",
            "horizon",
            "n_stress_cases",
            "n_passed",
            "pass_rate",
            "worst_degradation",
            "worst_stress_type",
            "worst_stress_case",
        ],
    )

    survivors["horizon"] = survivors["horizon"].astype(int)
    survivors["survivor_id"] = survivors.apply(
        lambda row: f"{survivor_version}::{row['alpha_name']}::{int(row['horizon'])}d",
        axis=1,
    )
    survivors["final_status"] = APPROVED_SURVIVOR
    survivors["survivor_version"] = survivor_version
    survivors["run_id"] = run_id
    survivors["timestamp_frozen"] = timestamp_frozen

    return (
        survivors.reindex(columns=SURVIVOR_REGISTRY_COLUMNS)
        .sort_values(["alpha_name", "horizon"])
        .reset_index(drop=True)
    )


def build_pre_ml_alpha_inputs(
    alpha_candidates_long: pd.DataFrame,
    survivor_registry: pd.DataFrame,
) -> pd.DataFrame:
    """Keep only frozen survivor alpha observations for downstream pre-ML use."""
    if alpha_candidates_long.empty or survivor_registry.empty:
        return pd.DataFrame(columns=PRE_ML_ALPHA_INPUT_COLUMNS)

    required_alpha_columns = {"Date", "ticker", "alpha_name", "alpha_value"}
    missing_alpha_columns = required_alpha_columns.difference(alpha_candidates_long.columns)
    if missing_alpha_columns:
        raise ValueError(
            f"alpha_candidates_long is missing required columns: {sorted(missing_alpha_columns)}"
        )

    required_registry_columns = {"alpha_name", "horizon", "survivor_id", "survivor_version", "run_id"}
    missing_registry_columns = required_registry_columns.difference(survivor_registry.columns)
    if missing_registry_columns:
        raise ValueError(
            f"survivor_registry is missing required columns: {sorted(missing_registry_columns)}"
        )

    survivor_lookup = survivor_registry[
        ["alpha_name", "horizon", "survivor_id", "survivor_version", "run_id"]
    ].drop_duplicates("alpha_name")
    candidate_columns = ["Date", "ticker", "alpha_name", "alpha_value"]
    pre_ml = alpha_candidates_long[candidate_columns].merge(survivor_lookup, on="alpha_name", how="inner")
    return pre_ml.reindex(columns=PRE_ML_ALPHA_INPUT_COLUMNS).sort_values(
        ["alpha_name", "Date", "ticker"]
    ).reset_index(drop=True)


def build_constructed_pre_ml_alpha_inputs(
    alpha_candidates_long: pd.DataFrame,
    survivor_registry: pd.DataFrame,
) -> pd.DataFrame:
    """Keep only frozen constructed survivor alpha observations for downstream pre-ML use."""
    return build_pre_ml_alpha_inputs(alpha_candidates_long, survivor_registry)


def build_survivor_candidate_pool(
    stress_gate: pd.DataFrame,
    stress_audit: pd.DataFrame | None = None,
    construction_metadata: pd.DataFrame | None = None,
    construction_diagnostics: pd.DataFrame | None = None,
    construction_quality: pd.DataFrame | None = None,
    constructed_alpha_wfv_winner_summary: pd.DataFrame | None = None,
) -> pd.DataFrame:
    """Build a stress-labeled candidate pool for correlation-aware survivor selection."""
    if stress_gate.empty:
        return pd.DataFrame(
            columns=[
                "alpha_name",
                "horizon",
                "promotion_decision",
                "survivor_tier",
                "alpha_role",
                "failure_category",
                "interpretation_notes",
                "stress_status",
                "pass_rate",
                "worst_degradation",
                "avg_turnover_proxy",
                "turnover_risk_flag",
                "stress_version",
                "source_wfv_status",
            ]
        )

    candidates = _normalize_horizon(stress_gate.copy())
    if "promotion_decision" not in candidates.columns:
        raise ValueError("stress_gate is missing required column: promotion_decision")

    base_columns = [
        "alpha_name",
        "horizon",
        "promotion_decision",
        "survivor_tier",
        "alpha_role",
        "failure_category",
        "interpretation_notes",
        "status",
        "pass_rate",
        "worst_degradation",
        "avg_turnover_proxy",
        "turnover_risk_flag",
        "stress_version",
    ]
    candidates = candidates[[column for column in base_columns if column in candidates.columns]].rename(
        columns={"status": "stress_status"}
    )
    candidates = candidates.drop_duplicates(["alpha_name", "horizon"])

    if stress_audit is not None and not stress_audit.empty:
        candidates = _join_on_alpha_horizon(
            candidates,
            stress_audit,
            [
                "alpha_name",
                "horizon",
                "pass_rate",
                "worst_degradation",
                "avg_turnover_proxy",
                "turnover_risk_flag",
                "stress_version",
                "failure_category",
                "interpretation_notes",
            ],
        )
        for column in [
            "pass_rate",
            "worst_degradation",
            "avg_turnover_proxy",
            "turnover_risk_flag",
            "stress_version",
            "failure_category",
            "interpretation_notes",
        ]:
            base_column = f"{column}_x"
            audit_column = f"{column}_y"
            if audit_column in candidates.columns:
                candidates[column] = candidates.get(base_column).combine_first(candidates[audit_column])
                candidates = candidates.drop(columns=[c for c in [base_column, audit_column] if c in candidates.columns])

    if constructed_alpha_wfv_winner_summary is not None and not constructed_alpha_wfv_winner_summary.empty:
        candidates = _join_on_alpha_horizon(
            candidates,
            constructed_alpha_wfv_winner_summary.rename(columns={"status": "source_wfv_status"}),
            ["alpha_name", "horizon", "source_wfv_status"],
        )

    if construction_metadata is not None and not construction_metadata.empty:
        candidates = _join_on_alpha_name(
            candidates,
            construction_metadata,
            [
                "alpha_name",
                "component_signals",
                "component_horizons",
                "alpha_sleeve",
                "source_signal_names",
                "source_signal_horizons",
                "source_diversity_groups",
                "source_orthogonal_version",
                "weighting_method",
                "regime_aware",
                "alpha_construction_version",
            ],
        )

    if construction_diagnostics is not None and not construction_diagnostics.empty:
        candidates = _join_on_alpha_name(
            candidates,
            construction_diagnostics,
            ["alpha_name", "avg_turnover_proxy", "turnover_risk_flag"],
        )
        for column in ["avg_turnover_proxy", "turnover_risk_flag"]:
            base_column = f"{column}_x"
            diagnostic_column = f"{column}_y"
            if diagnostic_column in candidates.columns:
                candidates[column] = candidates.get(base_column).combine_first(candidates[diagnostic_column])
                candidates = candidates.drop(columns=[c for c in [base_column, diagnostic_column] if c in candidates.columns])

    if construction_quality is not None and not construction_quality.empty:
        candidates = _join_on_alpha_name(
            candidates,
            construction_quality,
            ["alpha_name", "alpha_construction_version"],
        )
        if "alpha_construction_version_x" in candidates.columns and "alpha_construction_version_y" in candidates.columns:
            candidates["alpha_construction_version"] = candidates["alpha_construction_version_x"].combine_first(
                candidates["alpha_construction_version_y"]
            )
            candidates = candidates.drop(columns=["alpha_construction_version_x", "alpha_construction_version_y"])

    return candidates.reset_index(drop=True)


def _text_contains(value: object, patterns: list[str]) -> bool:
    text = "" if pd.isna(value) else str(value).lower()
    return any(pattern in text for pattern in patterns)


def classify_alpha_behavior_cluster(row: pd.Series | dict) -> str:
    """Classify constructed alphas into behavior clusters for survivor diversity."""
    get = row.get if isinstance(row, dict) else row.get
    turnover_risk = str(get("turnover_risk_flag", "")).upper()
    if turnover_risk == "HIGH_TURNOVER_RISK":
        return "HIGH_TURNOVER_EXPERIMENT"

    alpha_name = get("alpha_name", "")
    alpha_sleeve = str(get("alpha_sleeve", "")).upper()
    if alpha_sleeve == "ORTHOGONAL_DIVERSIFIER":
        return "ORTHOGONAL_DIVERSIFIER"
    if alpha_sleeve == "DECAY_STABILITY":
        return "DECAY_STABILITY"
    if alpha_sleeve == "CORE_REGIME":
        return "CORE_REGIME"

    weighting_method = get("weighting_method", "")
    component_signals = get("component_signals", "")
    component_horizons = get("component_horizons", "")
    combined = " ".join(str(value).lower() for value in [alpha_name, weighting_method, component_signals, component_horizons])
    regime_aware = pd.to_numeric(pd.Series([get("regime_aware", 0)]), errors="coerce").fillna(0).iloc[0]

    if regime_aware == 1 or "regime" in combined:
        return "REGIME_ADAPTIVE"
    if "rolling_ic" in combined:
        return "ROLLING_IC_DYNAMIC"
    if "diversified" in combined or "hybrid" in combined:
        return "DIVERSIFIED_BLEND"
    if "equal_weight" in combined or "health_weighted" in combined:
        return "EQUAL_HEALTH_BASELINE"
    if any(pattern in combined for pattern in ["decay", "stability", "health", "persistence"]):
        return "DECAY_STABILITY"
    return "OTHER"


def add_alpha_behavior_clusters(candidates: pd.DataFrame) -> pd.DataFrame:
    """Attach behavior cluster labels and score ranks within each cluster."""
    if candidates.empty:
        output = candidates.copy()
        output["alpha_behavior_cluster"] = pd.Series(dtype="object")
        output["cluster_rank"] = pd.Series(dtype="Int64")
        return output

    output = candidates.copy()
    if "survivor_selection_score" not in output.columns:
        output = add_survivor_selection_scores(output)
    output["alpha_behavior_cluster"] = output.apply(classify_alpha_behavior_cluster, axis=1)
    output = output.sort_values(
        ["alpha_behavior_cluster", "survivor_selection_score", "pass_rate", "alpha_name"],
        ascending=[True, False, False, True],
    ).reset_index(drop=True)
    output["cluster_rank"] = output.groupby("alpha_behavior_cluster").cumcount() + 1
    return output


def add_survivor_selection_scores(candidates: pd.DataFrame) -> pd.DataFrame:
    """Score survivor candidates using stress strength, degradation, turnover, and labels."""
    if candidates.empty:
        output = candidates.copy()
        output["survivor_selection_score"] = pd.Series(dtype="float64")
        return output

    output = candidates.copy()
    pass_rate = pd.to_numeric(
        output.get("pass_rate", pd.Series(pd.NA, index=output.index)),
        errors="coerce",
    ).fillna(0.0)
    worst_degradation = pd.to_numeric(
        output.get("worst_degradation", pd.Series(pd.NA, index=output.index)),
        errors="coerce",
    ).fillna(1.0)
    avg_turnover_proxy = pd.to_numeric(
        output.get("avg_turnover_proxy", pd.Series(pd.NA, index=output.index)),
        errors="coerce",
    ).fillna(0.0)
    promotion = output.get("promotion_decision", pd.Series("", index=output.index)).astype(str)
    turnover_risk = output.get("turnover_risk_flag", pd.Series("", index=output.index)).astype(str)

    score = (
        100.0 * pass_rate
        - 25.0 * worst_degradation
        - 5.0 * avg_turnover_proxy
        + promotion.eq("PROMOTE_CORE").astype(float) * 20.0
        - promotion.eq("REVIEW_SATELLITE").astype(float) * 20.0
        - turnover_risk.eq("HIGH_TURNOVER_RISK").astype(float) * 50.0
    )
    output["survivor_selection_score"] = score
    return output


def compute_survivor_alpha_correlations(
    alpha_candidates_long: pd.DataFrame,
    candidates: pd.DataFrame,
    survivor_version: str,
    run_id: str,
) -> pd.DataFrame:
    """Compute pairwise alpha correlations over aligned date/ticker observations."""
    if alpha_candidates_long.empty or candidates.empty:
        return pd.DataFrame(columns=SURVIVOR_ALPHA_CORRELATION_COLUMNS)

    required_columns = {"Date", "ticker", "alpha_name", "alpha_value"}
    missing_columns = required_columns.difference(alpha_candidates_long.columns)
    if missing_columns:
        raise ValueError(f"alpha_candidates_long is missing required columns: {sorted(missing_columns)}")

    candidate_names = sorted(candidates["alpha_name"].dropna().unique())
    alpha_values = alpha_candidates_long.loc[
        alpha_candidates_long["alpha_name"].isin(candidate_names),
        ["Date", "ticker", "alpha_name", "alpha_value"],
    ].copy()
    alpha_values["alpha_value"] = pd.to_numeric(alpha_values["alpha_value"], errors="coerce")
    if alpha_values.empty:
        return pd.DataFrame(columns=SURVIVOR_ALPHA_CORRELATION_COLUMNS)

    wide = alpha_values.pivot_table(
        index=["Date", "ticker"],
        columns="alpha_name",
        values="alpha_value",
        aggfunc="first",
    )
    corr = wide.corr(min_periods=20)
    lookup = candidates.drop_duplicates("alpha_name").set_index("alpha_name")

    records = []
    for i, alpha_name_1 in enumerate(candidate_names):
        for alpha_name_2 in candidate_names[i + 1:]:
            correlation = corr.loc[alpha_name_1, alpha_name_2] if alpha_name_1 in corr.index and alpha_name_2 in corr.columns else pd.NA
            records.append(
                {
                    "alpha_name_1": alpha_name_1,
                    "alpha_name_2": alpha_name_2,
                    "correlation": correlation,
                    "abs_correlation": abs(correlation) if pd.notna(correlation) else pd.NA,
                    "alpha_1_promotion_decision": lookup.at[alpha_name_1, "promotion_decision"]
                    if alpha_name_1 in lookup.index and "promotion_decision" in lookup.columns
                    else pd.NA,
                    "alpha_2_promotion_decision": lookup.at[alpha_name_2, "promotion_decision"]
                    if alpha_name_2 in lookup.index and "promotion_decision" in lookup.columns
                    else pd.NA,
                    "alpha_1_pass_rate": lookup.at[alpha_name_1, "pass_rate"]
                    if alpha_name_1 in lookup.index and "pass_rate" in lookup.columns
                    else pd.NA,
                    "alpha_2_pass_rate": lookup.at[alpha_name_2, "pass_rate"]
                    if alpha_name_2 in lookup.index and "pass_rate" in lookup.columns
                    else pd.NA,
                    "alpha_1_worst_degradation": lookup.at[alpha_name_1, "worst_degradation"]
                    if alpha_name_1 in lookup.index and "worst_degradation" in lookup.columns
                    else pd.NA,
                    "alpha_2_worst_degradation": lookup.at[alpha_name_2, "worst_degradation"]
                    if alpha_name_2 in lookup.index and "worst_degradation" in lookup.columns
                    else pd.NA,
                    "survivor_version": survivor_version,
                    "run_id": run_id,
                }
            )
    return pd.DataFrame(records, columns=SURVIVOR_ALPHA_CORRELATION_COLUMNS)


def build_correlation_aware_survivor_registry(
    candidates: pd.DataFrame,
    alpha_correlations: pd.DataFrame,
    survivor_version: str,
    run_id: str,
    timestamp_frozen: str,
    core_max_abs_correlation: float = 0.90,
    cluster_max_abs_correlation: float = 0.95,
    target_max_core_survivors: int = 4,
    min_cluster_score: float = 40.0,
) -> pd.DataFrame:
    """Select final core survivors while retaining cluster-aware alternates for audit."""
    if candidates.empty:
        return pd.DataFrame(columns=CORRELATION_AWARE_SURVIVOR_REGISTRY_COLUMNS)

    scored = add_alpha_behavior_clusters(add_survivor_selection_scores(candidates))
    scored = scored.sort_values(
        ["survivor_selection_score", "pass_rate", "alpha_name"],
        ascending=[False, False, True],
    ).reset_index(drop=True)

    corr_lookup: dict[tuple[str, str], float] = {}
    if not alpha_correlations.empty:
        for row in alpha_correlations.itertuples(index=False):
            corr_lookup[(row.alpha_name_1, row.alpha_name_2)] = row.abs_correlation
            corr_lookup[(row.alpha_name_2, row.alpha_name_1)] = row.abs_correlation

    selected_core: list[str] = []
    selected_clusters: set[str] = set()
    decisions: dict[str, dict[str, object]] = {}

    def selected_corr(alpha_name: str) -> tuple[object, object]:
        max_corr = pd.NA
        correlated_core = pd.NA
        if selected_core:
            correlations = [
                (core_alpha, corr_lookup.get((alpha_name, core_alpha), pd.NA))
                for core_alpha in selected_core
            ]
            valid_correlations = [(name, corr) for name, corr in correlations if pd.notna(corr)]
            if valid_correlations:
                correlated_core, max_corr = max(valid_correlations, key=lambda item: item[1])
        return max_corr, correlated_core

    eligible_mask = (
        scored["promotion_decision"].isin(PRIMARY_PROMOTION_DECISIONS)
        & pd.to_numeric(scored["survivor_selection_score"], errors="coerce").ge(min_cluster_score)
        & scored["turnover_risk_flag"].astype(str).ne("HIGH_TURNOVER_RISK")
    )
    eligible = scored.loc[eligible_mask].copy()

    original_core = eligible.loc[eligible["promotion_decision"].eq("PROMOTE_CORE")].copy()
    if not original_core.empty:
        first = original_core.iloc[0].to_dict()
        selected_core.append(first["alpha_name"])
        selected_clusters.add(first["alpha_behavior_cluster"])
        decisions[first["alpha_name"]] = {
            "promotion_decision_final": "PROMOTE_CORE",
            "final_status": "CORE_ALPHA_SURVIVOR",
            "alpha_role": "CORE_ALPHA",
            "cluster_selection_role": "INITIAL_BEST_CORE",
            "cluster_selection_reason": "Best original PROMOTE_CORE alpha selected first.",
            "max_corr_to_selected_core": pd.NA,
            "correlated_with_core_alpha": pd.NA,
        }

    for cluster_name, cluster_candidates in eligible.groupby("alpha_behavior_cluster", sort=False):
        if len(selected_core) >= target_max_core_survivors:
            break
        if cluster_name in selected_clusters:
            continue

        cluster_candidates = cluster_candidates.sort_values(
            ["survivor_selection_score", "pass_rate", "alpha_name"],
            ascending=[False, False, True],
        )
        best_rejected = None
        for row in cluster_candidates.to_dict("records"):
            alpha_name = row["alpha_name"]
            if alpha_name in decisions:
                continue
            max_corr, correlated_core = selected_corr(alpha_name)
            too_correlated = pd.notna(max_corr) and float(max_corr) > core_max_abs_correlation
            if too_correlated:
                best_rejected = best_rejected or (row, max_corr, correlated_core)
                continue
            selected_core.append(alpha_name)
            selected_clusters.add(cluster_name)
            decisions[alpha_name] = {
                "promotion_decision_final": "PROMOTE_CORE",
                "final_status": "CORE_ALPHA_SURVIVOR",
                "alpha_role": "CORE_ALPHA",
                "cluster_selection_role": "CLUSTER_CORE_SURVIVOR",
                "cluster_selection_reason": "Best eligible alpha from a distinct behavior cluster passed score, turnover, and correlation gates.",
                "max_corr_to_selected_core": max_corr,
                "correlated_with_core_alpha": correlated_core,
            }
            break

        if cluster_name not in selected_clusters and best_rejected is not None:
            row, max_corr, correlated_core = best_rejected
            alpha_name = row["alpha_name"]
            decisions[alpha_name] = {
                "promotion_decision_final": "REVIEW_CORRELATED_ALTERNATE",
                "final_status": "CORRELATED_CORE_ALTERNATE",
                "alpha_role": "CORE_ALTERNATE",
                "cluster_selection_role": "CORRELATED_CORE_ALTERNATE",
                "cluster_selection_reason": (
                    f"Strongest eligible alpha in cluster exceeded core correlation threshold "
                    f"{core_max_abs_correlation:.2f}."
                ),
                "max_corr_to_selected_core": max_corr,
                "correlated_with_core_alpha": correlated_core,
            }

    records = []
    for row in scored.to_dict("records"):
        alpha_name = row["alpha_name"]
        promotion_decision = row.get("promotion_decision")
        max_corr, correlated_core = selected_corr(alpha_name)
        decision = decisions.get(alpha_name)

        if decision is not None:
            promotion_decision_final = decision["promotion_decision_final"]
            final_status = decision["final_status"]
            alpha_role = decision["alpha_role"]
            cluster_selection_role = decision["cluster_selection_role"]
            cluster_selection_reason = decision["cluster_selection_reason"]
            max_corr = decision["max_corr_to_selected_core"]
            correlated_core = decision["correlated_with_core_alpha"]
        elif promotion_decision in CORE_ELIGIBLE_PROMOTION_DECISIONS:
            score = pd.to_numeric(pd.Series([row.get("survivor_selection_score")]), errors="coerce").iloc[0]
            same_cluster_selected = [
                core_alpha
                for core_alpha in selected_core
                if scored.loc[
                    scored["alpha_name"].eq(core_alpha),
                    "alpha_behavior_cluster",
                ].astype(str).eq(str(row.get("alpha_behavior_cluster"))).any()
            ]
            same_cluster_corrs = [
                (core_alpha, corr_lookup.get((alpha_name, core_alpha), pd.NA))
                for core_alpha in same_cluster_selected
            ]
            valid_same_cluster_corrs = [(name, corr) for name, corr in same_cluster_corrs if pd.notna(corr)]
            same_cluster_core, same_cluster_max_corr = (
                max(valid_same_cluster_corrs, key=lambda item: item[1])
                if valid_same_cluster_corrs
                else (pd.NA, pd.NA)
            )
            if str(row.get("turnover_risk_flag")) == "HIGH_TURNOVER_RISK":
                final_status = "REJECTED_HIGH_TURNOVER"
                alpha_role = "HIGH_TURNOVER_REJECT"
                promotion_decision_final = "REJECT_HIGH_TURNOVER"
                cluster_selection_role = "HIGH_TURNOVER_TRACKING_ONLY"
                cluster_selection_reason = "High-turnover risk rows stay in the registry for tracking only."
            elif pd.notna(score) and score < min_cluster_score:
                final_status = "BALANCED_ALTERNATE" if promotion_decision == "PROMOTE_BALANCED" else "SATELLITE_WATCHLIST"
                alpha_role = "BALANCED_ALPHA_ALTERNATE" if promotion_decision == "PROMOTE_BALANCED" else "SATELLITE_CANDIDATE"
                promotion_decision_final = (
                    "REVIEW_BALANCED_ALTERNATE" if promotion_decision == "PROMOTE_BALANCED" else "REVIEW_SATELLITE"
                )
                cluster_selection_role = "WEAK_SCORE_WATCHLIST"
                cluster_selection_reason = f"Score below MIN_CLUSTER_SCORE {min_cluster_score:.0f}."
            elif row.get("alpha_behavior_cluster") in selected_clusters:
                too_correlated_with_cluster_core = (
                    pd.notna(same_cluster_max_corr)
                    and float(same_cluster_max_corr) > cluster_max_abs_correlation
                )
                final_status = (
                    "CORRELATED_CORE_ALTERNATE"
                    if too_correlated_with_cluster_core
                    else ("BALANCED_ALTERNATE" if promotion_decision == "PROMOTE_BALANCED" else "SATELLITE_WATCHLIST")
                )
                alpha_role = (
                    "CORE_ALTERNATE"
                    if too_correlated_with_cluster_core
                    else ("BALANCED_ALPHA_ALTERNATE" if promotion_decision == "PROMOTE_BALANCED" else "SATELLITE_CANDIDATE")
                )
                promotion_decision_final = (
                    "REVIEW_CORRELATED_ALTERNATE"
                    if too_correlated_with_cluster_core
                    else ("REVIEW_BALANCED_ALTERNATE" if promotion_decision == "PROMOTE_BALANCED" else "REVIEW_SATELLITE")
                )
                cluster_selection_role = (
                    "WITHIN_CLUSTER_CORRELATED_ALTERNATE"
                    if too_correlated_with_cluster_core
                    else ("BALANCED_ALTERNATE" if promotion_decision == "PROMOTE_BALANCED" else "SAME_CLUSTER_ALTERNATE")
                )
                cluster_selection_reason = (
                    f"Same-cluster alternate exceeded within-cluster correlation threshold {cluster_max_abs_correlation:.2f}."
                    if too_correlated_with_cluster_core
                    else (
                        "PROMOTE_BALANCED alpha retained as a balanced alternate because its behavior cluster "
                        "is dominated by a stronger selected core alpha."
                        if promotion_decision == "PROMOTE_BALANCED"
                        else "Same behavior cluster is dominated by a stronger selected core alpha."
                    )
                )
                if too_correlated_with_cluster_core:
                    max_corr = same_cluster_max_corr
                    correlated_core = same_cluster_core
            else:
                too_correlated = pd.notna(max_corr) and float(max_corr) > core_max_abs_correlation
                final_status = (
                    "CORRELATED_CORE_ALTERNATE"
                    if too_correlated
                    else ("BALANCED_ALTERNATE" if promotion_decision == "PROMOTE_BALANCED" else "SATELLITE_WATCHLIST")
                )
                alpha_role = (
                    "CORE_ALTERNATE"
                    if too_correlated
                    else ("BALANCED_ALPHA_ALTERNATE" if promotion_decision == "PROMOTE_BALANCED" else "SATELLITE_CANDIDATE")
                )
                promotion_decision_final = (
                    "REVIEW_CORRELATED_ALTERNATE"
                    if too_correlated
                    else ("REVIEW_BALANCED_ALTERNATE" if promotion_decision == "PROMOTE_BALANCED" else "REVIEW_SATELLITE")
                )
                cluster_selection_role = (
                    "CORRELATED_CORE_ALTERNATE"
                    if too_correlated
                    else ("BALANCED_ALTERNATE" if promotion_decision == "PROMOTE_BALANCED" else "SATELLITE_WATCHLIST")
                )
                cluster_selection_reason = (
                    "Too correlated with selected core alpha."
                    if too_correlated
                    else (
                        "PROMOTE_BALANCED alpha retained as a balanced alternate after cluster and target survivor gates."
                        if promotion_decision == "PROMOTE_BALANCED"
                        else "Not selected after cluster and target survivor gates."
                    )
                )
        elif promotion_decision == "REVIEW_SATELLITE":
            final_status = "SATELLITE_WATCHLIST"
            alpha_role = "SATELLITE_CANDIDATE"
            promotion_decision_final = "REVIEW_SATELLITE"
            if str(row.get("turnover_risk_flag")) == "HIGH_TURNOVER_RISK":
                cluster_selection_role = "HIGH_TURNOVER_TRACKING_ONLY"
                cluster_selection_reason = "High-turnover risk rows stay in the registry for tracking only."
            elif pd.to_numeric(pd.Series([row.get("survivor_selection_score")]), errors="coerce").fillna(-float("inf")).iloc[0] < min_cluster_score:
                cluster_selection_role = "WEAK_SCORE_WATCHLIST"
                cluster_selection_reason = f"Score below MIN_CLUSTER_SCORE {min_cluster_score:.0f}."
            else:
                cluster_selection_role = "SATELLITE_WATCHLIST"
                cluster_selection_reason = "Satellite candidate retained for monitoring but not promoted by cluster-aware gates."
        elif promotion_decision == "REJECT_HIGH_TURNOVER":
            final_status = "REJECTED_HIGH_TURNOVER"
            alpha_role = "HIGH_TURNOVER_REJECT"
            promotion_decision_final = "REJECT_HIGH_TURNOVER"
            cluster_selection_role = "HIGH_TURNOVER_TRACKING_ONLY"
            cluster_selection_reason = "Rejected high-turnover row retained in registry for tracking only."
        else:
            final_status = "REJECTED_ALPHA"
            alpha_role = "REJECTED_ALPHA"
            promotion_decision_final = "REJECT"
            cluster_selection_role = "REJECTED_TRACKING_ONLY"
            cluster_selection_reason = "Rejected by upstream stress promotion decision."

        horizon = int(row["horizon"]) if pd.notna(row.get("horizon")) else pd.NA
        records.append(
            {
                "survivor_id": f"{survivor_version}::{alpha_name}::{horizon}d",
                "alpha_name": alpha_name,
                "horizon": horizon,
                "alpha_sleeve": row.get("alpha_sleeve"),
                "original_promotion_decision": promotion_decision,
                "promotion_decision_final": promotion_decision_final,
                "final_status": final_status,
                "alpha_role": alpha_role,
                "survivor_tier": row.get("survivor_tier"),
                "survivor_selection_score": row.get("survivor_selection_score"),
                "alpha_behavior_cluster": row.get("alpha_behavior_cluster"),
                "cluster_rank": row.get("cluster_rank"),
                "cluster_selection_role": cluster_selection_role,
                "cluster_selection_reason": cluster_selection_reason,
                "max_corr_to_selected_core": max_corr,
                "correlated_with_core_alpha": correlated_core,
                "pass_rate": row.get("pass_rate"),
                "worst_degradation": row.get("worst_degradation"),
                "avg_turnover_proxy": row.get("avg_turnover_proxy"),
                "turnover_risk_flag": row.get("turnover_risk_flag"),
                "stress_status": row.get("stress_status"),
                "source_wfv_status": row.get("source_wfv_status"),
                "failure_category": row.get("failure_category"),
                "interpretation_notes": row.get("interpretation_notes"),
                "stress_version": row.get("stress_version"),
                "alpha_construction_version": row.get("alpha_construction_version"),
                "date_frozen": pd.to_datetime(timestamp_frozen, errors="coerce").date().isoformat(),
                "survivor_version": survivor_version,
                "run_id": run_id,
                "timestamp_frozen": timestamp_frozen,
            }
        )

    return pd.DataFrame(records, columns=CORRELATION_AWARE_SURVIVOR_REGISTRY_COLUMNS).sort_values(
        ["promotion_decision_final", "survivor_selection_score", "alpha_name"],
        ascending=[True, False, True],
    ).reset_index(drop=True)


def build_survivor_cluster_summary(
    survivor_registry: pd.DataFrame,
    alpha_correlations: pd.DataFrame,
    survivor_version: str,
    run_id: str,
) -> pd.DataFrame:
    """Summarize cluster representation and why each cluster did or did not promote."""
    if survivor_registry.empty:
        return pd.DataFrame(columns=SURVIVOR_CLUSTER_SUMMARY_COLUMNS)

    corr_lookup: dict[tuple[str, str], float] = {}
    if not alpha_correlations.empty:
        for row in alpha_correlations.itertuples(index=False):
            corr_lookup[(row.alpha_name_1, row.alpha_name_2)] = row.abs_correlation
            corr_lookup[(row.alpha_name_2, row.alpha_name_1)] = row.abs_correlation

    selected_core = survivor_registry.loc[
        survivor_registry["promotion_decision_final"].eq("PROMOTE_CORE"),
        "alpha_name",
    ].dropna().tolist()

    records = []
    for cluster_name, group in survivor_registry.groupby("alpha_behavior_cluster", dropna=False):
        sorted_group = group.sort_values(
            ["survivor_selection_score", "pass_rate", "alpha_name"],
            ascending=[False, False, True],
        )
        best = sorted_group.iloc[0]
        final_core = group.loc[group["promotion_decision_final"].eq("PROMOTE_CORE")]
        corr_values = []
        for alpha_name in group["alpha_name"].dropna():
            for core_alpha in selected_core:
                if alpha_name == core_alpha:
                    continue
                corr = corr_lookup.get((alpha_name, core_alpha), pd.NA)
                if pd.notna(corr):
                    corr_values.append(float(corr))
        if not final_core.empty:
            cluster_decision = "FINAL_CORE_SELECTED"
        elif group["final_status"].eq("CORRELATED_CORE_ALTERNATE").any():
            cluster_decision = "TOO_CORRELATED_WITH_SELECTED_CORE"
        elif group["cluster_selection_role"].astype(str).str.contains("WEAK_SCORE", na=False).any():
            cluster_decision = "WEAK_SCORE_WATCHLIST"
        elif group["cluster_selection_role"].astype(str).str.contains("HIGH_TURNOVER", na=False).any():
            cluster_decision = "HIGH_TURNOVER_TRACKING_ONLY"
        elif group["cluster_selection_role"].astype(str).str.contains("SAME_CLUSTER", na=False).any():
            cluster_decision = "SAME_CLUSTER_DOMINATED"
        else:
            cluster_decision = "SATELLITE_WATCHLIST"

        records.append(
            {
                "alpha_behavior_cluster": cluster_name,
                "alpha_sleeve": ",".join(sorted(group.get("alpha_sleeve", pd.Series(dtype=str)).dropna().astype(str).unique())),
                "n_candidates": len(group),
                "n_promote_core_original": int(group["original_promotion_decision"].eq("PROMOTE_CORE").sum()),
                "n_review_satellite": int(group["original_promotion_decision"].eq("REVIEW_SATELLITE").sum()),
                "n_final_core": len(final_core),
                "best_alpha_name": best.get("alpha_name"),
                "best_score": best.get("survivor_selection_score"),
                "best_final_status": best.get("final_status"),
                "avg_abs_corr_with_selected_core": sum(corr_values) / len(corr_values) if corr_values else pd.NA,
                "cluster_decision": cluster_decision,
                "survivor_version": survivor_version,
                "run_id": run_id,
            }
        )

    return pd.DataFrame(records, columns=SURVIVOR_CLUSTER_SUMMARY_COLUMNS).sort_values(
        ["n_final_core", "best_score", "alpha_behavior_cluster"],
        ascending=[False, False, True],
    ).reset_index(drop=True)


def validate_correlation_aware_survivor_registry(survivor_registry: pd.DataFrame) -> pd.DataFrame:
    """Validate correlation-aware survivor registry handoff constraints."""
    results = []

    def add_result(check_name: str, passed: bool, details: str) -> None:
        results.append({"check_name": check_name, "passed": bool(passed), "details": details})

    missing_columns = [
        column for column in CORRELATION_AWARE_SURVIVOR_REGISTRY_COLUMNS
        if column not in survivor_registry.columns
    ]
    add_result(
        "required_columns_exist",
        not missing_columns,
        "All required correlation-aware survivor registry columns exist."
        if not missing_columns
        else f"Missing columns: {missing_columns}",
    )
    if missing_columns:
        return pd.DataFrame(results, columns=SURVIVOR_VALIDATION_REPORT_COLUMNS)

    duplicate_survivor_ids = int(survivor_registry["survivor_id"].duplicated().sum())
    add_result("survivor_id_unique", duplicate_survivor_ids == 0, f"Duplicate survivor_id rows: {duplicate_survivor_ids}")

    final_core_count = int(survivor_registry["promotion_decision_final"].eq("PROMOTE_CORE").sum())
    add_result("at_least_one_final_core", final_core_count > 0, f"Final PROMOTE_CORE rows: {final_core_count}")

    invalid_core_sources = int(
        survivor_registry.loc[
            survivor_registry["promotion_decision_final"].eq("PROMOTE_CORE"),
            "original_promotion_decision",
        ].isin(PRIMARY_PROMOTION_DECISIONS).pipe(lambda series: (~series).sum())
    )
    add_result(
        "final_core_originates_from_eligible_stress_decisions",
        invalid_core_sources == 0,
        f"Final core rows not originally in {PRIMARY_PROMOTION_DECISIONS}: {invalid_core_sources}",
    )

    high_turnover_core_count = int(
        survivor_registry.loc[
            survivor_registry["promotion_decision_final"].eq("PROMOTE_CORE"),
            "turnover_risk_flag",
        ].astype(str).eq("HIGH_TURNOVER_RISK").sum()
    )
    add_result(
        "no_high_turnover_final_core",
        high_turnover_core_count == 0,
        f"Final core rows with HIGH_TURNOVER_RISK: {high_turnover_core_count}",
    )

    regime_context_count = int(
        survivor_registry["alpha_name"].astype(str).str.contains("context|__", case=False, na=False).sum()
    )
    add_result(
        "no_regime_overlay_alpha_names",
        regime_context_count == 0,
        f"Rows with regime-overlay-like alpha names: {regime_context_count}",
    )

    return pd.DataFrame(results, columns=SURVIVOR_VALIDATION_REPORT_COLUMNS)


def _has_missing_values(series: pd.Series) -> bool:
    as_string = series.astype("string")
    return bool(series.isna().any() or as_string.str.strip().eq("").any())


def validate_survivor_registry(survivor_registry: pd.DataFrame) -> pd.DataFrame:
    """Validate the frozen survivor registry and return an audit report."""
    results = []

    def add_result(check_name: str, passed: bool, details: str) -> None:
        results.append(
            {
                "check_name": check_name,
                "passed": bool(passed),
                "details": details,
            }
        )

    missing_columns = [
        column for column in SURVIVOR_REGISTRY_COLUMNS if column not in survivor_registry.columns
    ]
    add_result(
        "required_columns_exist",
        not missing_columns,
        "All required survivor registry columns exist."
        if not missing_columns
        else f"Missing columns: {missing_columns}",
    )

    if missing_columns:
        return pd.DataFrame(results, columns=SURVIVOR_VALIDATION_REPORT_COLUMNS)

    duplicate_survivor_ids = int(survivor_registry["survivor_id"].duplicated().sum())
    add_result(
        "survivor_id_unique",
        duplicate_survivor_ids == 0,
        f"Duplicate survivor_id rows: {duplicate_survivor_ids}",
    )

    duplicate_alpha_names = int(survivor_registry["alpha_name"].duplicated().sum())
    add_result(
        "alpha_name_unique",
        duplicate_alpha_names == 0,
        f"Duplicate alpha_name rows: {duplicate_alpha_names}",
    )

    invalid_status_count = int(
        survivor_registry["final_status"].ne(APPROVED_SURVIVOR).fillna(True).sum()
    )
    add_result(
        "final_status_all_approved_survivor",
        invalid_status_count == 0,
        f"Rows with final_status != {APPROVED_SURVIVOR}: {invalid_status_count}",
    )

    unique_survivor_versions = survivor_registry["survivor_version"].dropna().unique()
    add_result(
        "survivor_version_one_unique_value",
        len(unique_survivor_versions) == 1,
        f"Unique non-null survivor_version values: {list(unique_survivor_versions)}",
    )

    required_non_missing = ["alpha_name", "horizon", "allowed_regimes", "regime_column"]
    missing_value_columns = [
        column for column in required_non_missing if _has_missing_values(survivor_registry[column])
    ]
    add_result(
        "required_fields_not_missing",
        not missing_value_columns,
        "No missing alpha_name, horizon, allowed_regimes, or regime_column values."
        if not missing_value_columns
        else f"Columns with missing values: {missing_value_columns}",
    )

    pass_rate = pd.to_numeric(survivor_registry["pass_rate"], errors="coerce")
    invalid_pass_rate_count = int(pass_rate.lt(1.0).fillna(True).sum())
    add_result(
        "pass_rate_at_least_one",
        invalid_pass_rate_count == 0,
        f"Rows with pass_rate < 1.0 or missing/non-numeric: {invalid_pass_rate_count}",
    )

    n_passed = pd.to_numeric(survivor_registry["n_passed"], errors="coerce")
    n_stress_cases = pd.to_numeric(survivor_registry["n_stress_cases"], errors="coerce")
    invalid_stress_count = int(n_passed.ne(n_stress_cases).fillna(True).sum())
    add_result(
        "n_passed_equals_n_stress_cases",
        invalid_stress_count == 0,
        f"Rows where n_passed != n_stress_cases or missing/non-numeric: {invalid_stress_count}",
    )

    return pd.DataFrame(results, columns=SURVIVOR_VALIDATION_REPORT_COLUMNS)


def validate_constructed_survivor_registry(survivor_registry: pd.DataFrame) -> pd.DataFrame:
    """Validate the constructed-alpha survivor registry."""
    results = []

    def add_result(check_name: str, passed: bool, details: str) -> None:
        results.append(
            {
                "check_name": check_name,
                "passed": bool(passed),
                "details": details,
            }
        )

    missing_columns = [
        column for column in CONSTRUCTED_SURVIVOR_REGISTRY_COLUMNS if column not in survivor_registry.columns
    ]
    add_result(
        "required_columns_exist",
        not missing_columns,
        "All required constructed survivor registry columns exist."
        if not missing_columns
        else f"Missing columns: {missing_columns}",
    )
    if missing_columns:
        return pd.DataFrame(results, columns=SURVIVOR_VALIDATION_REPORT_COLUMNS)

    duplicate_survivor_ids = int(survivor_registry["survivor_id"].duplicated().sum())
    add_result(
        "survivor_id_unique",
        duplicate_survivor_ids == 0,
        f"Duplicate survivor_id rows: {duplicate_survivor_ids}",
    )

    allowed_statuses = set(CONSTRUCTED_SURVIVOR_FINAL_STATUS.values())
    invalid_status_count = int(survivor_registry["final_status"].isin(allowed_statuses).eq(False).sum())
    add_result(
        "final_status_uses_constructed_tiers",
        invalid_status_count == 0,
        f"Rows with final_status outside constructed survivor statuses: {invalid_status_count}",
    )

    stress_status_count = int(survivor_registry["stress_status"].ne(APPROVED_STRESS).fillna(True).sum())
    add_result(
        "stress_status_all_approved",
        stress_status_count == 0,
        f"Rows with stress_status != {APPROVED_STRESS}: {stress_status_count}",
    )

    regime_context_count = int(
        survivor_registry["alpha_name"].astype(str).str.contains("context", case=False, na=False).sum()
    )
    add_result(
        "no_regime_context_alpha_names",
        regime_context_count == 0,
        f"Rows with regime-context-like alpha names: {regime_context_count}",
    )

    required_non_missing = [
        "alpha_name",
        "horizon",
        "survivor_tier",
        "pass_rate",
        "source_construction_version",
        "stress_version",
        "final_status",
    ]
    missing_value_columns = [
        column for column in required_non_missing if _has_missing_values(survivor_registry[column])
    ]
    add_result(
        "required_fields_not_missing",
        not missing_value_columns,
        "No missing constructed survivor freeze fields."
        if not missing_value_columns
        else f"Columns with missing values: {missing_value_columns}",
    )

    return pd.DataFrame(results, columns=SURVIVOR_VALIDATION_REPORT_COLUMNS)


def _optional_version_lookup(
    df: pd.DataFrame | None,
    version_column: str,
) -> pd.DataFrame:
    if df is None or df.empty or version_column not in df.columns:
        return pd.DataFrame(columns=["alpha_name", "horizon", version_column])
    if not {"alpha_name", "horizon"}.issubset(df.columns):
        return pd.DataFrame(columns=["alpha_name", "horizon", version_column])
    return (
        _normalize_horizon(df[["alpha_name", "horizon", version_column]])
        .drop_duplicates(["alpha_name", "horizon"])
    )


def build_survivor_lineage_report(
    survivor_registry: pd.DataFrame,
    alpha_metadata: pd.DataFrame | None = None,
    alpha_wfv_gate: pd.DataFrame | None = None,
    alpha_stress_audit: pd.DataFrame | None = None,
) -> pd.DataFrame:
    """Build one lineage row per frozen survivor alpha."""
    if survivor_registry.empty:
        return pd.DataFrame(columns=SURVIVOR_LINEAGE_REPORT_COLUMNS)

    required_columns = [
        "survivor_id",
        "alpha_name",
        "horizon",
        "source_signal",
        "regime_column",
        "allowed_regimes",
        "survivor_version",
        "run_id",
        "timestamp_frozen",
    ]
    missing_columns = [column for column in required_columns if column not in survivor_registry.columns]
    if missing_columns:
        raise ValueError(f"survivor_registry is missing required columns: {missing_columns}")

    lineage = _normalize_horizon(survivor_registry[required_columns].copy())
    for source, version_column in [
        (alpha_metadata, "alpha_version"),
        (alpha_wfv_gate, "alpha_wfv_version"),
        (alpha_stress_audit, "stress_version"),
    ]:
        lineage = lineage.merge(
            _optional_version_lookup(source, version_column),
            on=["alpha_name", "horizon"],
            how="left",
        )

    return (
        lineage.reindex(columns=SURVIVOR_LINEAGE_REPORT_COLUMNS)
        .sort_values(["alpha_name", "survivor_id"])
        .reset_index(drop=True)
    )


def build_constructed_survivor_lineage_report(
    survivor_registry: pd.DataFrame,
    construction_metadata: pd.DataFrame | None = None,
    stress_audit: pd.DataFrame | None = None,
) -> pd.DataFrame:
    """Build lineage rows for constructed-alpha survivors."""
    if survivor_registry.empty:
        return pd.DataFrame()

    columns = [
        "survivor_id",
        "alpha_name",
        "horizon",
        "survivor_tier",
        "final_status",
        "component_signals",
        "component_horizons",
        "weighting_method",
        "source_construction_version",
        "stress_version",
        "survivor_version",
        "run_id",
        "timestamp_frozen",
    ]
    lineage = survivor_registry[[column for column in columns if column in survivor_registry.columns]].copy()

    if construction_metadata is not None and not construction_metadata.empty:
        metadata_versions = _join_on_alpha_name(
            lineage[["alpha_name"]].drop_duplicates(),
            construction_metadata,
            ["alpha_name", "alpha_construction_version", "notes"],
        )
        lineage = lineage.merge(metadata_versions, on="alpha_name", how="left")
        if "source_construction_version" not in lineage and "alpha_construction_version" in lineage:
            lineage = lineage.rename(columns={"alpha_construction_version": "source_construction_version"})
        elif "alpha_construction_version" in lineage:
            lineage["source_construction_version"] = lineage["source_construction_version"].combine_first(
                lineage["alpha_construction_version"]
            )
            lineage = lineage.drop(columns=["alpha_construction_version"])

    if stress_audit is not None and not stress_audit.empty and "stress_version" in stress_audit.columns:
        stress_versions = _normalize_horizon(
            stress_audit[["alpha_name", "horizon", "stress_version"]].drop_duplicates(["alpha_name", "horizon"])
        )
        lineage = _normalize_horizon(lineage).merge(
            stress_versions,
            on=["alpha_name", "horizon"],
            how="left",
            suffixes=("", "_audit"),
        )
        if "stress_version_audit" in lineage.columns:
            lineage["stress_version"] = lineage["stress_version"].combine_first(lineage["stress_version_audit"])
            lineage = lineage.drop(columns=["stress_version_audit"])

    ordered = [
        "survivor_id",
        "alpha_name",
        "horizon",
        "survivor_tier",
        "final_status",
        "component_signals",
        "component_horizons",
        "weighting_method",
        "source_construction_version",
        "stress_version",
        "notes",
        "survivor_version",
        "run_id",
        "timestamp_frozen",
    ]
    return lineage.reindex(columns=ordered).sort_values(["alpha_name", "horizon"]).reset_index(drop=True)


def build_survivor_freeze_report(survivor_registry: pd.DataFrame) -> pd.DataFrame:
    """Build a concise one-row freeze report for audit and handoff."""
    if survivor_registry.empty:
        return pd.DataFrame(
            [
                {
                    "survivor_version": pd.NA,
                    "n_survivors": 0,
                    "survivor_names": "",
                    "date_frozen": pd.NA,
                    "notes": "No stress-approved survivor alphas were frozen.",
                }
            ],
            columns=SURVIVOR_FREEZE_REPORT_COLUMNS,
        )

    survivor_version = survivor_registry["survivor_version"].dropna().iloc[0]
    timestamp_frozen = pd.to_datetime(
        survivor_registry["timestamp_frozen"].dropna().iloc[0],
        errors="coerce",
    )
    date_frozen = timestamp_frozen.date().isoformat() if not pd.isna(timestamp_frozen) else pd.NA
    survivor_names = ", ".join(sorted(survivor_registry["alpha_name"].dropna().unique()))

    return pd.DataFrame(
        [
            {
                "survivor_version": survivor_version,
                "n_survivors": int(survivor_registry["survivor_id"].nunique()),
                "survivor_names": survivor_names,
                "date_frozen": date_frozen,
                "notes": "Frozen from stress-approved Notebook 7 alphas; no formula, regime, WFV, or stress threshold changes.",
            }
        ],
        columns=SURVIVOR_FREEZE_REPORT_COLUMNS,
    )


__all__ = [
    "APPROVED_SURVIVOR",
    "CORRELATION_AWARE_SURVIVOR_REGISTRY_COLUMNS",
    "CONSTRUCTED_SURVIVOR_REGISTRY_COLUMNS",
    "PRE_ML_ALPHA_INPUT_COLUMNS",
    "SURVIVOR_ALPHA_CORRELATION_COLUMNS",
    "SURVIVOR_CLUSTER_SUMMARY_COLUMNS",
    "SURVIVOR_FREEZE_REPORT_COLUMNS",
    "SURVIVOR_LINEAGE_REPORT_COLUMNS",
    "SURVIVOR_REGISTRY_COLUMNS",
    "SURVIVOR_VALIDATION_REPORT_COLUMNS",
    "add_alpha_behavior_clusters",
    "add_survivor_selection_scores",
    "build_correlation_aware_survivor_registry",
    "build_constructed_pre_ml_alpha_inputs",
    "build_constructed_survivor_alpha_registry",
    "build_constructed_survivor_lineage_report",
    "build_pre_ml_alpha_inputs",
    "build_survivor_candidate_pool",
    "build_survivor_cluster_summary",
    "build_survivor_alpha_registry",
    "build_survivor_freeze_report",
    "build_survivor_lineage_report",
    "compute_survivor_alpha_correlations",
    "load_constructed_stress_approved_alphas",
    "load_stress_approved_alphas",
    "validate_correlation_aware_survivor_registry",
    "validate_constructed_survivor_registry",
    "validate_survivor_registry",
]
