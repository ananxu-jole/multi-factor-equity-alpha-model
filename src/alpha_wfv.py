from __future__ import annotations

import numpy as np
import pandas as pd

from src.alpha_scoring import (
    APPROVED_FOR_ALPHA_WFV,
    NEGATIVE_EDGE_REVERSE_ALPHA,
    POSITIVE_EDGE,
    WATCHLIST_ALPHA_WFV,
)
from src.db import load_table
from src.forward_returns import make_forward_returns


APPROVED_ALPHA_WFV = "APPROVED_ALPHA_WFV"
WATCHLIST_ALPHA_WFV_STATUS = "WATCHLIST_ALPHA_WFV"
REJECTED_ALPHA_WFV = "REJECTED_ALPHA_WFV"

ALPHA_WFV_STATUS_LABELS = [
    APPROVED_ALPHA_WFV,
    WATCHLIST_ALPHA_WFV_STATUS,
    REJECTED_ALPHA_WFV,
]

ALPHA_WFV_WINDOW_RESULT_COLUMNS = [
    "window_id",
    "alpha_name",
    "horizon",
    "candidate_tier",
    "alpha_direction",
    "alpha_strength",
    "source_status",
    "method",
    "train_start",
    "train_end",
    "test_start",
    "test_end",
    "train_mean_ic",
    "test_mean_ic",
    "effective_train_ic",
    "effective_test_ic",
    "train_positive_ic_rate",
    "test_positive_ic_rate",
    "train_n_obs",
    "test_n_obs",
    "direction_flip_warning",
]

ALPHA_WFV_SUMMARY_COLUMNS = [
    "alpha_name",
    "horizon",
    "candidate_tier",
    "alpha_direction",
    "alpha_strength",
    "n_windows",
    "mean_train_ic",
    "mean_test_ic",
    "effective_mean_train_ic",
    "effective_mean_test_ic",
    "median_test_ic",
    "effective_median_test_ic",
    "test_ic_std",
    "effective_test_ic_std",
    "test_ic_ir",
    "effective_test_ic_ir",
    "test_positive_ic_rate",
    "persistence_ratio",
    "sign_consistency",
    "direction_flip_warning",
    "degradation_ratio",
    "n_positive_test_windows",
    "n_negative_test_windows",
]


def _validate_method(method: str) -> None:
    if method not in {"spearman", "pearson", "kendall"}:
        raise ValueError("method must be one of: spearman, pearson, kendall.")


def _pivot_alpha_long_to_panel(alpha_long_df: pd.DataFrame, alpha_name: str) -> pd.DataFrame:
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


def _safe_corr(df: pd.DataFrame, method: str) -> float:
    if len(df) < 2:
        return np.nan
    if df["alpha"].nunique(dropna=True) < 2 or df["fwd_return"].nunique(dropna=True) < 2:
        return np.nan
    return float(df["alpha"].corr(df["fwd_return"], method=method))


def _direction_adjusted_value(value: float, alpha_direction: object) -> float:
    if pd.isna(value):
        return np.nan
    if alpha_direction == POSITIVE_EDGE:
        return float(value)
    if alpha_direction == NEGATIVE_EDGE_REVERSE_ALPHA:
        return float(-value)
    return float(value)


def _direction_flip_warning(alpha_direction: object, mean_test_ic: float) -> bool:
    if pd.isna(mean_test_ic):
        return False
    return bool(
        (alpha_direction == POSITIVE_EDGE and float(mean_test_ic) < 0)
        or (alpha_direction == NEGATIVE_EDGE_REVERSE_ALPHA and float(mean_test_ic) > 0)
    )


def _score_period(
    alpha_panel: pd.DataFrame,
    fwd_return_panel: pd.DataFrame,
    start_date,
    end_date,
    method: str,
) -> dict[str, object]:
    alpha_slice = alpha_panel.loc[start_date:end_date]
    fwd_slice = fwd_return_panel.loc[start_date:end_date]

    paired = pd.concat(
        [
            alpha_slice.stack(future_stack=True).rename("alpha"),
            fwd_slice.stack(future_stack=True).rename("fwd_return"),
        ],
        axis=1,
    ).dropna()

    if paired.empty:
        return {"mean_ic": np.nan, "positive_ic_rate": np.nan, "n_obs": 0}

    ic_by_date = paired.groupby(level=0, sort=True).apply(_safe_corr, method=method).dropna()
    return {
        "mean_ic": float(ic_by_date.mean()) if not ic_by_date.empty else np.nan,
        "positive_ic_rate": float((ic_by_date > 0).mean()) if not ic_by_date.empty else np.nan,
        "n_obs": int(len(paired)),
    }


def _score_alpha_wfv(
    alpha_panel: pd.DataFrame,
    fwd_return_panel: pd.DataFrame,
    windows: pd.DataFrame,
    candidate: pd.Series,
    method: str,
) -> pd.DataFrame:
    alpha, fwd = _align_panels(alpha_panel, fwd_return_panel)
    alpha_name = str(candidate["alpha_name"])
    horizon = int(candidate["horizon"])
    alpha_direction = candidate.get("alpha_direction")
    rows: list[dict[str, object]] = []

    for _, window in windows.iterrows():
        train = _score_period(alpha, fwd, window["train_start"], window["train_end"], method=method)
        test = _score_period(alpha, fwd, window["test_start"], window["test_end"], method=method)
        effective_train_ic = _direction_adjusted_value(train["mean_ic"], alpha_direction)
        effective_test_ic = _direction_adjusted_value(test["mean_ic"], alpha_direction)
        rows.append(
            {
                "window_id": int(window["window_id"]),
                "alpha_name": alpha_name,
                "horizon": horizon,
                "candidate_tier": candidate.get("candidate_tier"),
                "alpha_direction": alpha_direction,
                "alpha_strength": candidate.get("alpha_strength"),
                "source_status": candidate.get("source_status"),
                "method": method,
                "train_start": window["train_start"],
                "train_end": window["train_end"],
                "test_start": window["test_start"],
                "test_end": window["test_end"],
                "train_mean_ic": train["mean_ic"],
                "test_mean_ic": test["mean_ic"],
                "effective_train_ic": effective_train_ic,
                "effective_test_ic": effective_test_ic,
                "train_positive_ic_rate": train["positive_ic_rate"],
                "test_positive_ic_rate": test["positive_ic_rate"],
                "train_n_obs": train["n_obs"],
                "test_n_obs": test["n_obs"],
                "direction_flip_warning": _direction_flip_warning(alpha_direction, test["mean_ic"]),
            }
        )

    return pd.DataFrame(rows)


def run_wfv_for_alpha_candidates(
    alpha_candidates: pd.DataFrame,
    close_prices: pd.DataFrame,
    windows: pd.DataFrame,
    method: str = "spearman",
    alpha_long_df: pd.DataFrame | None = None,
) -> pd.DataFrame:
    """Run walk-forward IC validation for alpha scoring-gate candidates."""
    _validate_method(method)
    required_columns = {"alpha_name", "horizon"}
    missing_columns = required_columns.difference(alpha_candidates.columns)
    if missing_columns:
        raise ValueError(f"alpha_candidates is missing required columns: {sorted(missing_columns)}")

    candidates_to_run = alpha_candidates.copy()
    candidates_to_run["horizon"] = pd.to_numeric(candidates_to_run["horizon"], errors="coerce").astype("Int64")
    if "status" in candidates_to_run.columns:
        candidates_to_run = candidates_to_run[
            candidates_to_run["status"].isin([APPROVED_FOR_ALPHA_WFV, WATCHLIST_ALPHA_WFV])
        ].copy()

    if candidates_to_run.empty:
        return pd.DataFrame(columns=ALPHA_WFV_WINDOW_RESULT_COLUMNS)

    if alpha_long_df is None:
        alpha_long_df = load_table("alpha_candidates_current")

    horizon_values = sorted(candidates_to_run["horizon"].dropna().astype(int).unique().tolist())
    forward_returns = make_forward_returns(close_prices, horizon_values)
    panel_cache: dict[str, pd.DataFrame] = {}
    rows: list[pd.DataFrame] = []

    for _, candidate in candidates_to_run.iterrows():
        alpha_name = str(candidate["alpha_name"])
        horizon = int(candidate["horizon"])
        if alpha_name not in panel_cache:
            panel_cache[alpha_name] = _pivot_alpha_long_to_panel(alpha_long_df, alpha_name)

        rows.append(
            _score_alpha_wfv(
                alpha_panel=panel_cache[alpha_name],
                fwd_return_panel=forward_returns[horizon],
                windows=windows,
                candidate=candidate,
                method=method,
            )
        )

    if not rows:
        return pd.DataFrame(columns=ALPHA_WFV_WINDOW_RESULT_COLUMNS)

    output = pd.concat(rows, ignore_index=True)
    ordered = [column for column in ALPHA_WFV_WINDOW_RESULT_COLUMNS if column in output.columns]
    remaining = [column for column in output.columns if column not in ordered]
    return output[ordered + remaining].sort_values(["alpha_name", "horizon", "window_id"]).reset_index(drop=True)


def _same_sign_rate(values: pd.Series, target_sign: float) -> float:
    valid = values.dropna()
    if valid.empty or target_sign == 0 or pd.isna(target_sign):
        return np.nan
    return float((np.sign(valid) == target_sign).mean())


def _window_persistence_ratio(train_ic: pd.Series, test_ic: pd.Series) -> float:
    paired = pd.concat(
        [train_ic.rename("train_mean_ic"), test_ic.rename("test_mean_ic")],
        axis=1,
    ).dropna()
    paired = paired[(paired["train_mean_ic"] != 0) & (paired["test_mean_ic"] != 0)]
    if paired.empty:
        return np.nan
    return float((np.sign(paired["train_mean_ic"]) == np.sign(paired["test_mean_ic"])).mean())


def _target_sign_from_direction(alpha_direction: object, fallback_ic: float) -> float:
    if alpha_direction == POSITIVE_EDGE:
        return 1.0
    if alpha_direction == NEGATIVE_EDGE_REVERSE_ALPHA:
        return -1.0
    return np.sign(fallback_ic) if not pd.isna(fallback_ic) else np.nan


def _degradation_ratio(effective_mean_test_ic: float, effective_mean_train_ic: float) -> float:
    if (
        pd.isna(effective_mean_test_ic)
        or pd.isna(effective_mean_train_ic)
        or float(effective_mean_train_ic) == 0
    ):
        return np.nan
    return float(effective_mean_test_ic / effective_mean_train_ic)


def summarize_alpha_wfv_results(alpha_wfv_window_results: pd.DataFrame) -> pd.DataFrame:
    """Summarize alpha WFV window results by alpha and horizon."""
    if alpha_wfv_window_results.empty:
        return pd.DataFrame(columns=ALPHA_WFV_SUMMARY_COLUMNS)

    rows: list[dict[str, object]] = []
    for (alpha_name, horizon), group in alpha_wfv_window_results.groupby(["alpha_name", "horizon"], dropna=False):
        train_ic = pd.to_numeric(group["train_mean_ic"], errors="coerce")
        test_ic = pd.to_numeric(group["test_mean_ic"], errors="coerce")
        effective_train_ic = pd.to_numeric(group["effective_train_ic"], errors="coerce")
        effective_test_ic = pd.to_numeric(group["effective_test_ic"], errors="coerce")
        valid_test = test_ic.dropna()
        valid_effective_test = effective_test_ic.dropna()
        alpha_direction = group["alpha_direction"].iloc[0] if "alpha_direction" in group else None
        target_sign = _target_sign_from_direction(alpha_direction, float(valid_test.mean()) if not valid_test.empty else np.nan)

        mean_train_ic = float(train_ic.mean()) if not train_ic.dropna().empty else np.nan
        mean_test_ic = float(valid_test.mean()) if not valid_test.empty else np.nan
        effective_mean_train_ic = (
            float(effective_train_ic.mean()) if not effective_train_ic.dropna().empty else np.nan
        )
        effective_mean_test_ic = (
            float(valid_effective_test.mean()) if not valid_effective_test.empty else np.nan
        )
        test_ic_std = float(valid_test.std(ddof=1)) if len(valid_test) > 1 else np.nan
        effective_test_ic_std = (
            float(valid_effective_test.std(ddof=1)) if len(valid_effective_test) > 1 else np.nan
        )

        rows.append(
            {
                "alpha_name": alpha_name,
                "horizon": int(horizon),
                "candidate_tier": group["candidate_tier"].iloc[0] if "candidate_tier" in group else None,
                "alpha_direction": alpha_direction,
                "alpha_strength": group["alpha_strength"].iloc[0] if "alpha_strength" in group else None,
                "n_windows": int(group["window_id"].nunique()),
                "mean_train_ic": mean_train_ic,
                "mean_test_ic": mean_test_ic,
                "effective_mean_train_ic": effective_mean_train_ic,
                "effective_mean_test_ic": effective_mean_test_ic,
                "median_test_ic": float(valid_test.median()) if not valid_test.empty else np.nan,
                "effective_median_test_ic": (
                    float(valid_effective_test.median()) if not valid_effective_test.empty else np.nan
                ),
                "test_ic_std": test_ic_std,
                "effective_test_ic_std": effective_test_ic_std,
                "test_ic_ir": (
                    float(mean_test_ic / test_ic_std)
                    if test_ic_std and not pd.isna(test_ic_std)
                    else np.nan
                ),
                "effective_test_ic_ir": (
                    float(effective_mean_test_ic / effective_test_ic_std)
                    if effective_test_ic_std and not pd.isna(effective_test_ic_std)
                    else np.nan
                ),
                "test_positive_ic_rate": float((valid_test > 0).mean()) if not valid_test.empty else np.nan,
                "persistence_ratio": _window_persistence_ratio(train_ic, test_ic),
                "sign_consistency": _same_sign_rate(valid_test, target_sign),
                "direction_flip_warning": bool(group["direction_flip_warning"].any()),
                "degradation_ratio": _degradation_ratio(effective_mean_test_ic, effective_mean_train_ic),
                "n_positive_test_windows": int((valid_test > 0).sum()),
                "n_negative_test_windows": int((valid_test < 0).sum()),
            }
        )

    summary = pd.DataFrame(rows)
    ordered = [column for column in ALPHA_WFV_SUMMARY_COLUMNS if column in summary.columns]
    remaining = [column for column in summary.columns if column not in ordered]
    return summary[ordered + remaining].sort_values(["alpha_name", "horizon"]).reset_index(drop=True)


def _assign_alpha_wfv_status(row: pd.Series) -> str:
    effective_mean_test_ic = row.get("effective_mean_test_ic")
    effective_test_ic_ir = row.get("effective_test_ic_ir")
    persistence_ratio = row.get("persistence_ratio")
    sign_consistency = row.get("sign_consistency")
    direction_flip_warning = bool(row.get("direction_flip_warning", False))

    if pd.isna(effective_test_ic_ir) or pd.isna(persistence_ratio):
        return REJECTED_ALPHA_WFV

    if pd.isna(effective_mean_test_ic) or direction_flip_warning:
        return REJECTED_ALPHA_WFV

    if (
        float(effective_mean_test_ic) >= 0.015
        and float(effective_test_ic_ir) >= 0.05
        and float(persistence_ratio) >= 0.67
        and not pd.isna(sign_consistency)
        and float(sign_consistency) >= 0.67
    ):
        return APPROVED_ALPHA_WFV

    if float(effective_mean_test_ic) >= 0.008 and float(persistence_ratio) >= 0.50:
        return WATCHLIST_ALPHA_WFV_STATUS

    return REJECTED_ALPHA_WFV


def _alpha_wfv_gate_notes(row: pd.Series) -> str:
    status = row.get("status")
    if status == APPROVED_ALPHA_WFV:
        return "Meets strict direction-adjusted alpha WFV thresholds."
    if status == WATCHLIST_ALPHA_WFV_STATUS:
        return "Meets secondary direction-adjusted alpha IC and persistence thresholds."

    notes: list[str] = []
    effective_mean_test_ic = row.get("effective_mean_test_ic")
    effective_test_ic_ir = row.get("effective_test_ic_ir")
    persistence_ratio = row.get("persistence_ratio")
    sign_consistency = row.get("sign_consistency")

    if pd.isna(effective_test_ic_ir) or pd.isna(persistence_ratio):
        notes.append("insufficient valid WFV windows")
    if bool(row.get("direction_flip_warning", False)):
        notes.append("direction flip")
    if pd.isna(effective_mean_test_ic) or float(effective_mean_test_ic) < 0.008:
        notes.append("weak effective alpha IC")
    if pd.isna(effective_test_ic_ir) or float(effective_test_ic_ir) < 0.05:
        notes.append("weak effective alpha IC IR")
    if pd.isna(persistence_ratio) or float(persistence_ratio) < 0.50:
        notes.append("low alpha persistence")
    if pd.isna(sign_consistency) or float(sign_consistency) < 0.67:
        notes.append("low alpha sign consistency")

    return "; ".join(notes) if notes else "fails strict alpha WFV approval thresholds"


def apply_alpha_wfv_gate(alpha_wfv_summary: pd.DataFrame) -> pd.DataFrame:
    """Apply strict alpha WFV stability thresholds."""
    gated = alpha_wfv_summary.copy()
    if gated.empty:
        return gated.assign(
            abs_mean_test_ic=pd.Series(dtype=float),
            abs_test_ic_ir=pd.Series(dtype=float),
            status=pd.Series(dtype=object),
            wfv_gate_notes=pd.Series(dtype=object),
        )

    gated["abs_mean_test_ic"] = pd.to_numeric(gated["mean_test_ic"], errors="coerce").abs()
    gated["abs_test_ic_ir"] = pd.to_numeric(gated["test_ic_ir"], errors="coerce").abs()
    gated["status"] = gated.apply(_assign_alpha_wfv_status, axis=1)
    gated["wfv_gate_notes"] = gated.apply(_alpha_wfv_gate_notes, axis=1)
    return gated


def build_alpha_wfv_failure_breakdown(alpha_wfv_gate: pd.DataFrame) -> pd.DataFrame:
    """Count rejected alpha WFV failure reasons from semicolon-delimited gate notes."""
    columns = ["failure_reason", "count", "pct_of_candidates"]
    if alpha_wfv_gate.empty or "wfv_gate_notes" not in alpha_wfv_gate.columns:
        return pd.DataFrame(columns=columns)

    rejected = alpha_wfv_gate
    if "status" in rejected.columns:
        rejected = rejected[rejected["status"].eq(REJECTED_ALPHA_WFV)]

    reasons = (
        rejected["wfv_gate_notes"]
        .dropna()
        .astype(str)
        .str.split(";")
        .explode()
        .str.strip()
    )
    reasons = reasons[reasons.ne("")]
    if reasons.empty:
        return pd.DataFrame(columns=columns)

    total_candidates = len(alpha_wfv_gate)
    breakdown = reasons.value_counts().rename_axis("failure_reason").reset_index(name="count")
    breakdown["pct_of_candidates"] = (
        breakdown["count"] / total_candidates if total_candidates else np.nan
    )
    return breakdown[columns].sort_values(["count", "failure_reason"], ascending=[False, True]).reset_index(drop=True)


def build_alpha_wfv_winner_summary(alpha_wfv_gate: pd.DataFrame) -> pd.DataFrame:
    """Return approved alpha WFV rows sorted by direction-adjusted test IC."""
    columns = [
        "alpha_name",
        "horizon",
        "effective_mean_test_ic",
        "effective_test_ic_ir",
        "persistence_ratio",
        "sign_consistency",
        "candidate_tier",
        "alpha_direction",
        "alpha_strength",
        "status",
    ]
    if alpha_wfv_gate.empty or "status" not in alpha_wfv_gate.columns:
        return pd.DataFrame(columns=columns)

    winners = alpha_wfv_gate.loc[alpha_wfv_gate["status"].eq(APPROVED_ALPHA_WFV)].copy()
    if winners.empty:
        return pd.DataFrame(columns=columns)

    for column in columns:
        if column not in winners.columns:
            winners[column] = np.nan
    return winners[columns].sort_values("effective_mean_test_ic", ascending=False).reset_index(drop=True)


__all__ = [
    "ALPHA_WFV_STATUS_LABELS",
    "ALPHA_WFV_SUMMARY_COLUMNS",
    "ALPHA_WFV_WINDOW_RESULT_COLUMNS",
    "APPROVED_ALPHA_WFV",
    "REJECTED_ALPHA_WFV",
    "WATCHLIST_ALPHA_WFV_STATUS",
    "apply_alpha_wfv_gate",
    "build_alpha_wfv_failure_breakdown",
    "build_alpha_wfv_winner_summary",
    "run_wfv_for_alpha_candidates",
    "summarize_alpha_wfv_results",
]
