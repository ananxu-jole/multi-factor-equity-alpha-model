from __future__ import annotations

import numpy as np
import pandas as pd

from src.db import load_table


def load_survivor_alpha_registry() -> pd.DataFrame:
    """Load the frozen survivor alpha registry from Notebook 8."""
    output = load_table("survivor_alpha_registry_current")
    if "date_frozen" in output.columns:
        output["date_frozen"] = pd.to_datetime(output["date_frozen"], errors="coerce")
    return output


def load_pre_ml_alpha_inputs() -> pd.DataFrame:
    """Load the frozen pre-ML survivor alpha inputs from Notebook 8."""
    output = load_table("pre_ml_alpha_inputs_current")
    if "Date" in output.columns:
        output["Date"] = pd.to_datetime(output["Date"])
    return output


def select_promote_core_survivors(survivor_registry):
    if survivor_registry.empty:
        return survivor_registry.copy()

    decision_col = (
        "promotion_decision_final"
        if "promotion_decision_final" in survivor_registry.columns
        else "promotion_decision")
    if decision_col not in survivor_registry.columns:
        raise ValueError(
            "survivor registry is missing required decision column: "
            "promotion_decision_final or promotion_decision")
    if "alpha_name" not in survivor_registry.columns:
        raise ValueError("survivor registry is missing required column: alpha_name")
    return survivor_registry[
        survivor_registry[decision_col].eq("PROMOTE_CORE")].copy()


def filter_pre_ml_alpha_inputs_to_survivors(
    pre_ml_alpha_inputs: pd.DataFrame,
    survivor_registry: pd.DataFrame,
) -> pd.DataFrame:
    """Keep only pre-ML alpha rows matching PROMOTE_CORE survivor registry rows."""
    required_input_columns = {"Date", "ticker", "alpha_name", "alpha_value"}
    missing_input_columns = required_input_columns.difference(pre_ml_alpha_inputs.columns)
    if missing_input_columns:
        raise ValueError(
            f"pre_ml_alpha_inputs is missing required columns: {sorted(missing_input_columns)}"
        )
    if survivor_registry.empty:
        return pre_ml_alpha_inputs.iloc[0:0].copy()
    if "alpha_name" not in survivor_registry.columns:
        raise ValueError("survivor registry is missing required column: alpha_name")

    if "survivor_id" in pre_ml_alpha_inputs.columns and "survivor_id" in survivor_registry.columns:
        survivor_ids = set(survivor_registry["survivor_id"].dropna())
        filtered = pre_ml_alpha_inputs.loc[
            pre_ml_alpha_inputs["survivor_id"].isin(survivor_ids)
        ].copy()
    elif "horizon" in pre_ml_alpha_inputs.columns and "horizon" in survivor_registry.columns:
        survivor_keys = survivor_registry[["alpha_name", "horizon"]].dropna().drop_duplicates()
        filtered = pre_ml_alpha_inputs.merge(
            survivor_keys,
            on=["alpha_name", "horizon"],
            how="inner",
        )
    else:
        survivor_names = set(survivor_registry["alpha_name"].dropna())
        filtered = pre_ml_alpha_inputs.loc[
            pre_ml_alpha_inputs["alpha_name"].isin(survivor_names)
        ].copy()
    if "Date" in filtered.columns:
        filtered["Date"] = pd.to_datetime(filtered["Date"])
    return filtered.reset_index(drop=True)


def pivot_alpha_input(pre_ml_alpha_inputs: pd.DataFrame, alpha_name: str) -> pd.DataFrame:
    """Pivot one survivor alpha from long format into a Date x ticker panel."""
    required_columns = {"Date", "ticker", "alpha_name", "alpha_value"}
    missing_columns = required_columns.difference(pre_ml_alpha_inputs.columns)
    if missing_columns:
        raise ValueError(f"pre_ml_alpha_inputs is missing required columns: {sorted(missing_columns)}")

    alpha_input = pre_ml_alpha_inputs.loc[
        pre_ml_alpha_inputs["alpha_name"].eq(alpha_name),
        ["Date", "ticker", "alpha_value"],
    ].copy()
    if alpha_input.empty:
        return pd.DataFrame()

    alpha_input["Date"] = pd.to_datetime(alpha_input["Date"])
    panel = alpha_input.pivot_table(
        index="Date",
        columns="ticker",
        values="alpha_value",
        aggfunc="first",
    )
    return panel.sort_index().sort_index(axis=1)


def build_alpha_signal_stack(pre_ml_alpha_inputs: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """Build one wide Date x ticker alpha panel per frozen survivor alpha."""
    if pre_ml_alpha_inputs.empty:
        return {}
    if "alpha_name" not in pre_ml_alpha_inputs.columns:
        raise ValueError("pre_ml_alpha_inputs is missing required column: alpha_name")

    alpha_names = sorted(pre_ml_alpha_inputs["alpha_name"].dropna().unique())
    return {
        alpha_name: pivot_alpha_input(pre_ml_alpha_inputs, alpha_name)
        for alpha_name in alpha_names
    }


def combine_survivor_alphas(
    alpha_panels: dict[str, pd.DataFrame],
    method: str = "equal_weight",
    weights: dict[str, float] | pd.Series | None = None,
) -> pd.DataFrame:
    """Combine survivor alpha panels into one raw alpha score panel."""
    if method not in {"equal_weight", "custom_weight"}:
        raise ValueError("method must be 'equal_weight' or 'custom_weight'.")
    if not alpha_panels:
        return pd.DataFrame()

    valid_panels = {
        alpha_name: panel.astype(float)
        for alpha_name, panel in alpha_panels.items()
        if not panel.empty
    }
    if not valid_panels:
        return pd.DataFrame()

    if method == "equal_weight" and weights is None:
        component_weights = pd.Series(1.0, index=sorted(valid_panels))
    else:
        if weights is None:
            raise ValueError("weights are required when method='custom_weight'.")
        component_weights = pd.Series(weights, dtype=float).reindex(sorted(valid_panels)).fillna(0.0)

    component_weights = component_weights.clip(lower=0.0)
    if component_weights.sum() <= 0:
        component_weights = pd.Series(1.0, index=sorted(valid_panels))
    component_weights = component_weights / component_weights.sum()

    weighted_panels = [
        valid_panels[alpha_name].mul(float(component_weights.loc[alpha_name]))
        for alpha_name in component_weights.index
    ]
    combined = weighted_panels[0].copy()
    for panel in weighted_panels[1:]:
        combined = combined.add(panel, fill_value=0.0)
    return combined.sort_index().sort_index(axis=1)


def _normalize_positive_weights(raw_weights: pd.Series) -> pd.Series:
    weights = pd.to_numeric(raw_weights, errors="coerce").replace([np.inf, -np.inf], np.nan)
    weights = weights.clip(lower=0.0)
    if weights.notna().sum() == 0 or weights.fillna(0.0).sum() <= 0:
        weights = pd.Series(1.0, index=raw_weights.index, dtype=float)
    else:
        positive_median = weights.loc[weights.gt(0)].median()
        fallback = float(positive_median) if pd.notna(positive_median) and positive_median > 0 else 1.0
        weights = weights.fillna(fallback)
    return weights / weights.sum()


def build_survivor_weight_table(survivor_registry: pd.DataFrame) -> pd.DataFrame:
    """Build dynamic survivor alpha weights for all portfolio pooling methods."""
    if survivor_registry.empty:
        return pd.DataFrame(
            columns=[
                "portfolio_method",
                "alpha_name",
                "horizon",
                "component_weight",
                "raw_weight_score",
            ]
        )

    required_columns = {"alpha_name", "horizon"}
    missing_columns = required_columns.difference(survivor_registry.columns)
    if missing_columns:
        raise ValueError(f"survivor registry is missing required columns: {sorted(missing_columns)}")

    registry = survivor_registry.copy()
    registry["pass_rate"] = pd.to_numeric(registry.get("pass_rate", np.nan), errors="coerce")
    registry["worst_degradation"] = pd.to_numeric(
        registry.get("worst_degradation", np.nan),
        errors="coerce",
    )
    registry["avg_turnover_proxy"] = pd.to_numeric(
        registry.get("avg_turnover_proxy", np.nan),
        errors="coerce",
    )
    registry = registry.drop_duplicates(subset=["alpha_name", "horizon"]).reset_index(drop=True)
    index = registry.index

    equal_raw = pd.Series(1.0, index=index)
    degradation_penalty = 1.0 / (1.0 + registry["worst_degradation"].abs().fillna(0.0))
    stress_raw = registry["pass_rate"].fillna(registry["pass_rate"].median()).fillna(1.0) * degradation_penalty
    turnover = registry["avg_turnover_proxy"].where(registry["avg_turnover_proxy"].gt(0))
    turnover_raw = 1.0 / turnover.fillna(turnover.median()).fillna(1.0)

    equal_weights = _normalize_positive_weights(equal_raw)
    stress_weights = _normalize_positive_weights(stress_raw)
    turnover_weights = _normalize_positive_weights(turnover_raw)
    hybrid_weights = _normalize_positive_weights(stress_weights.add(turnover_weights, fill_value=0.0))

    method_weights = {
        "equal_weight_survivors": (equal_raw, equal_weights),
        "stress_score_weighted_survivors": (stress_raw, stress_weights),
        "inverse_turnover_weighted_survivors": (turnover_raw, turnover_weights),
        "hybrid_survivor_weighted_portfolio": (
            stress_raw.rank(pct=True).add(turnover_raw.rank(pct=True), fill_value=0.0),
            hybrid_weights,
        ),
    }

    records = []
    carry_columns = [
        "survivor_id",
        "alpha_name",
        "horizon",
        "promotion_decision",
        "survivor_tier",
        "alpha_role",
        "pass_rate",
        "worst_degradation",
        "avg_turnover_proxy",
        "turnover_risk_flag",
        "stress_version",
        "survivor_version",
    ]
    carry_columns = [column for column in carry_columns if column in registry.columns]
    for method, (raw_scores, weights) in method_weights.items():
        for idx, row in registry.iterrows():
            record = {column: row[column] for column in carry_columns}
            record.update(
                {
                    "portfolio_method": method,
                    "component_weight": float(weights.loc[idx]),
                    "raw_weight_score": float(raw_scores.loc[idx]) if pd.notna(raw_scores.loc[idx]) else np.nan,
                    "weighting_rule": method,
                }
            )
            records.append(record)
    return pd.DataFrame(records)


def normalize_cross_sectional_scores(alpha_score_panel: pd.DataFrame) -> pd.DataFrame:
    """Rank-normalize each date's alpha scores and center them around zero."""
    if alpha_score_panel.empty:
        return alpha_score_panel.copy()

    valid_counts = alpha_score_panel.notna().sum(axis=1)
    ranks = alpha_score_panel.rank(axis=1, pct=True, method="average", na_option="keep")
    normalized = ranks.sub(ranks.mean(axis=1), axis=0)
    normalized = normalized.where(valid_counts.ge(2), np.nan)
    return normalized.sort_index().sort_index(axis=1)


def build_target_positions(
    score_panel: pd.DataFrame,
    top_quantile: float = 0.20,
    bottom_quantile: float = 0.20,
    gross_exposure: float = 1.0,
) -> pd.DataFrame:
    """Build equal-weight long/short target weights from cross-sectional scores."""
    if score_panel.empty:
        return score_panel.copy()
    if not 0 < top_quantile < 1:
        raise ValueError("top_quantile must be between 0 and 1.")
    if not 0 < bottom_quantile < 1:
        raise ValueError("bottom_quantile must be between 0 and 1.")
    if gross_exposure <= 0:
        raise ValueError("gross_exposure must be positive.")

    positions = pd.DataFrame(0.0, index=score_panel.index, columns=score_panel.columns)
    side_gross = gross_exposure / 2.0

    for date, scores in score_panel.iterrows():
        valid_scores = scores.dropna()
        if valid_scores.empty:
            continue

        long_cutoff = valid_scores.quantile(1.0 - top_quantile)
        short_cutoff = valid_scores.quantile(bottom_quantile)
        long_names = valid_scores.index[valid_scores.ge(long_cutoff)]
        short_names = valid_scores.index[valid_scores.le(short_cutoff)]

        overlapping_names = long_names.intersection(short_names)
        if not overlapping_names.empty:
            long_names = long_names.difference(overlapping_names)
            short_names = short_names.difference(overlapping_names)

        if len(long_names) == 0 or len(short_names) == 0:
            continue

        positions.loc[date, long_names] = side_gross / len(long_names)
        positions.loc[date, short_names] = -side_gross / len(short_names)

    return positions.sort_index().sort_index(axis=1)


def build_long_only_top_bucket_positions(
    score_panel: pd.DataFrame,
    top_quantile: float = 0.20,
    gross_exposure: float = 1.0,
) -> pd.DataFrame:
    """Build equal-weight long-only target weights from top cross-sectional scores."""
    if score_panel.empty:
        return score_panel.copy()
    if not 0 < top_quantile < 1:
        raise ValueError("top_quantile must be between 0 and 1.")
    if gross_exposure <= 0:
        raise ValueError("gross_exposure must be positive.")

    positions = pd.DataFrame(0.0, index=score_panel.index, columns=score_panel.columns)
    for date, scores in score_panel.iterrows():
        valid_scores = scores.dropna()
        if valid_scores.empty:
            continue
        long_cutoff = valid_scores.quantile(1.0 - top_quantile)
        long_names = valid_scores.index[valid_scores.ge(long_cutoff)]
        if len(long_names) == 0:
            continue
        positions.loc[date, long_names] = gross_exposure / len(long_names)
    return positions.sort_index().sort_index(axis=1)


def apply_position_smoothing(
    target_positions: pd.DataFrame,
    smoothing_window: int = 3,
) -> pd.DataFrame:
    """Smooth target positions with a trailing rolling average."""
    if smoothing_window < 1:
        raise ValueError("smoothing_window must be at least 1.")
    if target_positions.empty:
        return target_positions.copy()
    return target_positions.rolling(window=smoothing_window, min_periods=1).mean()


def apply_rebalance_schedule(
    target_positions: pd.DataFrame,
    rebalance_frequency: int = 5,
) -> pd.DataFrame:
    """Update target positions every N trading days and forward-fill between dates."""
    if rebalance_frequency < 1:
        raise ValueError("rebalance_frequency must be at least 1.")
    if target_positions.empty:
        return target_positions.copy()

    rebalance_mask = pd.Series(
        np.arange(len(target_positions)) % rebalance_frequency == 0,
        index=target_positions.index,
    )
    scheduled = target_positions.where(rebalance_mask, np.nan)
    return scheduled.ffill().fillna(0.0)


def cap_position_weights(
    positions: pd.DataFrame,
    max_abs_weight: float = 0.05,
) -> pd.DataFrame:
    """Cap individual ticker weights at a maximum absolute position size."""
    if max_abs_weight <= 0:
        raise ValueError("max_abs_weight must be positive.")
    if positions.empty:
        return positions.copy()
    return positions.astype(float).clip(lower=-max_abs_weight, upper=max_abs_weight)


def renormalize_long_short(
    positions: pd.DataFrame,
    gross_exposure: float = 1.0,
) -> pd.DataFrame:
    """Rebalance each active day to equal long and short gross exposure."""
    if gross_exposure <= 0:
        raise ValueError("gross_exposure must be positive.")
    if positions.empty:
        return positions.copy()

    output = positions.astype(float).fillna(0.0).copy()
    side_gross = gross_exposure / 2.0

    for date, row in output.iterrows():
        long_mask = row.gt(0)
        short_mask = row.lt(0)
        long_gross = row[long_mask].sum()
        short_gross = row[short_mask].abs().sum()

        if long_gross <= 0 or short_gross <= 0:
            output.loc[date] = 0.0
            continue

        output.loc[date, long_mask] = row[long_mask] * (side_gross / long_gross)
        output.loc[date, short_mask] = row[short_mask] * (side_gross / short_gross)

    return output.sort_index().sort_index(axis=1)


def compute_turnover(positions: pd.DataFrame) -> pd.Series:
    """Compute daily portfolio turnover as half the absolute position change."""
    if positions.empty:
        return pd.Series(dtype=float, name="turnover")
    turnover = positions.diff().abs().sum(axis=1).div(2.0).fillna(0.0)
    turnover.name = "turnover"
    return turnover


def compute_exposure_stats(positions: pd.DataFrame) -> pd.DataFrame:
    """Compute daily gross, net, breadth, and max position exposure diagnostics."""
    if positions.empty:
        return pd.DataFrame(
            columns=[
                "Date",
                "gross_exposure",
                "net_exposure",
                "n_long",
                "n_short",
                "n_active_positions",
                "max_abs_weight",
            ]
        )

    weights = positions.astype(float).fillna(0.0)
    output = pd.DataFrame(
        {
            "Date": weights.index,
            "gross_exposure": weights.abs().sum(axis=1).to_numpy(),
            "net_exposure": weights.sum(axis=1).to_numpy(),
            "n_long": weights.gt(0).sum(axis=1).to_numpy(),
            "n_short": weights.lt(0).sum(axis=1).to_numpy(),
            "n_active_positions": weights.ne(0).sum(axis=1).to_numpy(),
            "max_abs_weight": weights.abs().max(axis=1).to_numpy(),
        }
    )
    return output


def compute_position_concentration(positions: pd.DataFrame) -> pd.DataFrame:
    """Compute daily concentration diagnostics from absolute portfolio weights."""
    if positions.empty:
        return pd.DataFrame(
            columns=[
                "Date",
                "top_5_abs_weight_sum",
                "top_10_abs_weight_sum",
                "herfindahl_index",
            ]
        )

    weights = positions.astype(float).fillna(0.0).abs()
    records = []
    for date, row in weights.iterrows():
        sorted_abs_weights = row.sort_values(ascending=False)
        gross = sorted_abs_weights.sum()
        exposure_shares = sorted_abs_weights.div(gross) if gross > 0 else sorted_abs_weights
        records.append(
            {
                "Date": date,
                "top_5_abs_weight_sum": sorted_abs_weights.head(5).sum(),
                "top_10_abs_weight_sum": sorted_abs_weights.head(10).sum(),
                "herfindahl_index": exposure_shares.pow(2).sum() if gross > 0 else 0.0,
            }
        )
    return pd.DataFrame(records)


def compute_activity_stats(
    positions: pd.DataFrame,
    returns: pd.Series | pd.DataFrame,
) -> pd.DataFrame:
    """Compute daily activity flags plus full-period activity percentages."""
    if positions.empty:
        return pd.DataFrame(
            columns=[
                "Date",
                "active_day_flag",
                "active_day_pct",
                "invested_day_pct",
                "zero_position_day_pct",
            ]
        )

    weights = positions.astype(float).fillna(0.0)
    gross_exposure = weights.abs().sum(axis=1)
    invested_day_flag = gross_exposure.gt(0)

    if isinstance(returns, pd.DataFrame):
        if "net_return" in returns.columns:
            return_series = returns["net_return"]
        elif returns.shape[1] == 1:
            return_series = returns.iloc[:, 0]
        else:
            raise ValueError("returns DataFrame must include net_return or one column.")
    else:
        return_series = pd.Series(returns)

    return_series = return_series.reindex(weights.index).fillna(0.0)
    active_day_flag = invested_day_flag & return_series.ne(0)
    active_day_pct = float(active_day_flag.mean()) if len(active_day_flag) else np.nan
    invested_day_pct = float(invested_day_flag.mean()) if len(invested_day_flag) else np.nan
    zero_position_day_pct = float((~invested_day_flag).mean()) if len(invested_day_flag) else np.nan

    return pd.DataFrame(
        {
            "Date": weights.index,
            "active_day_flag": active_day_flag.astype(int).to_numpy(),
            "active_day_pct": active_day_pct,
            "invested_day_pct": invested_day_pct,
            "zero_position_day_pct": zero_position_day_pct,
        }
    )


__all__ = [
    "apply_position_smoothing",
    "apply_rebalance_schedule",
    "build_alpha_signal_stack",
    "build_long_only_top_bucket_positions",
    "build_survivor_weight_table",
    "build_target_positions",
    "cap_position_weights",
    "combine_survivor_alphas",
    "compute_activity_stats",
    "compute_exposure_stats",
    "compute_position_concentration",
    "compute_turnover",
    "filter_pre_ml_alpha_inputs_to_survivors",
    "load_pre_ml_alpha_inputs",
    "load_survivor_alpha_registry",
    "normalize_cross_sectional_scores",
    "pivot_alpha_input",
    "renormalize_long_short",
    "select_promote_core_survivors",
]
