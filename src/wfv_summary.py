from __future__ import annotations

import numpy as np
import pandas as pd


APPROVED_WFV = "APPROVED_WFV"
WATCHLIST_WFV = "WATCHLIST_WFV"
REJECTED_WFV = "REJECTED_WFV"


def _empty_failure_breakdown() -> pd.DataFrame:
    return pd.DataFrame(columns=["failure_reason", "count", "pct_of_candidates"])


def _empty_window_diagnostics() -> pd.DataFrame:
    return pd.DataFrame(
        columns=[
            "window_id",
            "test_start",
            "test_end",
            "n_candidates",
            "avg_abs_test_ic",
            "median_abs_test_ic",
            "n_positive_edges",
            "n_direction_flips",
            "best_signal_name",
            "best_horizon",
            "best_abs_test_ic",
        ]
    )


def _expected_direction(signal_direction: object) -> str:
    if signal_direction == "POSITIVE_EDGE":
        return "POSITIVE"
    if signal_direction == "NEGATIVE_EDGE_REVERSE_SIGNAL":
        return "NEGATIVE"
    return "UNKNOWN"


def _direction_adjusted_value(value: float, signal_direction: object) -> float:
    if pd.isna(value):
        return np.nan
    if signal_direction == "POSITIVE_EDGE":
        return float(value)
    if signal_direction == "NEGATIVE_EDGE_REVERSE_SIGNAL":
        return float(-value)
    return float(abs(value))


def _direction_flip_warning(signal_direction: object, mean_test_ic: float) -> bool:
    if pd.isna(mean_test_ic):
        return False
    return bool(
        (signal_direction == "POSITIVE_EDGE" and float(mean_test_ic) < 0)
        or (signal_direction == "NEGATIVE_EDGE_REVERSE_SIGNAL" and float(mean_test_ic) > 0)
    )


def _test_ic_column(df: pd.DataFrame) -> str:
    if "effective_test_ic" in df.columns:
        return "effective_test_ic"
    if "test_ic" in df.columns:
        return "test_ic"
    if "test_mean_ic" in df.columns:
        return "test_mean_ic"
    raise ValueError("DataFrame must include effective_test_ic, test_ic, or test_mean_ic.")


def _window_results_with_effective_ic(wfv_window_results: pd.DataFrame) -> pd.DataFrame:
    output = wfv_window_results.copy()
    if "effective_test_ic" not in output.columns:
        test_ic_column = _test_ic_column(output)
        if "signal_direction" in output.columns:
            output["effective_test_ic"] = output.apply(
                lambda row: _direction_adjusted_value(row[test_ic_column], row.get("signal_direction")),
                axis=1,
            )
        else:
            output["effective_test_ic"] = output[test_ic_column].abs()
    return output


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


def _target_sign_from_direction(signal_direction: object, fallback_ic: float) -> float:
    if signal_direction == "POSITIVE_EDGE":
        return 1.0
    if signal_direction == "NEGATIVE_EDGE_REVERSE_SIGNAL":
        return -1.0
    return np.sign(fallback_ic) if not pd.isna(fallback_ic) else np.nan


def _degradation_ratio(mean_test_ic: float, mean_train_ic: float) -> float:
    if pd.isna(mean_test_ic) or pd.isna(mean_train_ic) or float(mean_train_ic) == 0:
        return np.nan
    return float(mean_test_ic / mean_train_ic)


def summarize_wfv_results(wfv_window_results: pd.DataFrame) -> pd.DataFrame:
    """Summarize WFV window results by signal and horizon."""
    columns = [
        "signal_name",
        "horizon",
        "candidate_tier",
        "bridge_source",
        "bridge_reason",
        "signal_direction",
        "signal_family",
        "n_windows",
        "mean_train_ic",
        "mean_test_ic",
        "expected_direction",
        "effective_mean_test_ic",
        "median_test_ic",
        "test_ic_std",
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
    if wfv_window_results.empty:
        return pd.DataFrame(columns=columns)

    rows: list[dict[str, object]] = []
    group_columns = ["signal_name", "horizon"]
    for (signal_name, horizon), group in wfv_window_results.groupby(group_columns, dropna=False):
        train_ic = group["train_mean_ic"].astype(float)
        test_ic = group["test_mean_ic"].astype(float)
        valid_test = test_ic.dropna()

        mean_train_ic = float(train_ic.mean()) if not train_ic.dropna().empty else np.nan
        mean_test_ic = float(valid_test.mean()) if not valid_test.empty else np.nan
        signal_direction = group["signal_direction"].iloc[0] if "signal_direction" in group else None
        expected_direction = _expected_direction(signal_direction)
        target_sign = _target_sign_from_direction(signal_direction, mean_test_ic)
        test_ic_std = float(valid_test.std(ddof=1)) if len(valid_test) > 1 else np.nan
        test_ic_ir = float(mean_test_ic / test_ic_std) if test_ic_std and not pd.isna(test_ic_std) else np.nan
        persistence_ratio = _window_persistence_ratio(train_ic, test_ic)
        sign_consistency = _same_sign_rate(valid_test, target_sign)

        row = {
            "signal_name": signal_name,
            "horizon": int(horizon),
            "candidate_tier": group["candidate_tier"].iloc[0] if "candidate_tier" in group else None,
            "bridge_source": group["bridge_source"].iloc[0] if "bridge_source" in group else None,
            "bridge_reason": group["bridge_reason"].iloc[0] if "bridge_reason" in group else None,
            "signal_direction": signal_direction,
            "signal_family": group["signal_family"].iloc[0] if "signal_family" in group else None,
            "n_windows": int(group["window_id"].nunique()),
            "mean_train_ic": mean_train_ic,
            "mean_test_ic": mean_test_ic,
            "expected_direction": expected_direction,
            "effective_mean_test_ic": _direction_adjusted_value(mean_test_ic, signal_direction),
            "median_test_ic": float(valid_test.median()) if not valid_test.empty else np.nan,
            "test_ic_std": test_ic_std,
            "test_ic_ir": test_ic_ir,
            "effective_test_ic_ir": _direction_adjusted_value(test_ic_ir, signal_direction),
            "test_positive_ic_rate": float((valid_test > 0).mean()) if not valid_test.empty else np.nan,
            "persistence_ratio": persistence_ratio,
            "sign_consistency": sign_consistency,
            "direction_flip_warning": _direction_flip_warning(signal_direction, mean_test_ic),
            "degradation_ratio": _degradation_ratio(mean_test_ic, mean_train_ic),
            "n_positive_test_windows": int((valid_test > 0).sum()),
            "n_negative_test_windows": int((valid_test < 0).sum()),
        }
        rows.append(row)

    summary = pd.DataFrame(rows)
    ordered = [column for column in columns if column in summary.columns]
    remaining = [column for column in summary.columns if column not in ordered]
    return summary[ordered + remaining].sort_values(["signal_name", "horizon"]).reset_index(drop=True)


def _assign_wfv_status(row: pd.Series) -> str:
    effective_mean_test_ic = row.get("effective_mean_test_ic")
    effective_test_ic_ir = row.get("effective_test_ic_ir")
    persistence_ratio = row.get("persistence_ratio")
    sign_consistency = row.get("sign_consistency")
    direction_flip_warning = bool(row.get("direction_flip_warning", False))

    if (
        pd.isna(effective_mean_test_ic)
        or pd.isna(persistence_ratio)
        or direction_flip_warning
    ):
        return REJECTED_WFV

    if (
        float(effective_mean_test_ic) >= 0.015
        and not pd.isna(effective_test_ic_ir)
        and float(effective_test_ic_ir) >= 0.05
        and float(persistence_ratio) >= 0.67
        and not pd.isna(sign_consistency)
        and float(sign_consistency) >= 0.67
    ):
        return APPROVED_WFV

    if float(effective_mean_test_ic) >= 0.008 and float(persistence_ratio) >= 0.50:
        return WATCHLIST_WFV

    return REJECTED_WFV


def _wfv_gate_notes(row: pd.Series) -> str:
    status = row.get("status")
    if status == APPROVED_WFV:
        return "Meets strict direction-adjusted WFV thresholds."
    if status == WATCHLIST_WFV:
        return "Meets secondary direction-adjusted IC and persistence thresholds."

    notes: list[str] = []
    effective_mean_test_ic = row.get("effective_mean_test_ic")
    effective_test_ic_ir = row.get("effective_test_ic_ir")
    persistence_ratio = row.get("persistence_ratio")
    sign_consistency = row.get("sign_consistency")

    if bool(row.get("direction_flip_warning", False)):
        notes.append("direction flip")
    if pd.isna(effective_mean_test_ic) or float(effective_mean_test_ic) < 0.008:
        notes.append("weak effective IC")
    if pd.isna(effective_test_ic_ir) or float(effective_test_ic_ir) < 0.05:
        notes.append("weak effective IC IR")
    if pd.isna(persistence_ratio) or float(persistence_ratio) < 0.50:
        notes.append("low persistence")
    if pd.isna(sign_consistency) or float(sign_consistency) < 0.67:
        notes.append("low sign consistency")

    if not notes:
        notes.append("fails strict WFV approval thresholds")
    return "; ".join(notes)


def apply_wfv_gate(wfv_summary: pd.DataFrame) -> pd.DataFrame:
    """Apply the Phase 2 WFV stability gate."""
    gated = wfv_summary.copy()
    gated["abs_mean_test_ic"] = gated["mean_test_ic"].abs()
    gated["abs_test_ic_ir"] = gated["test_ic_ir"].abs()
    gated["status"] = gated.apply(_assign_wfv_status, axis=1)
    gated["wfv_gate_notes"] = gated.apply(_wfv_gate_notes, axis=1)
    return gated


def build_wfv_failure_breakdown(wfv_gate: pd.DataFrame) -> pd.DataFrame:
    """Count rejected WFV failure reasons from semicolon-delimited gate notes."""
    if wfv_gate.empty or "wfv_gate_notes" not in wfv_gate.columns:
        return _empty_failure_breakdown()

    rejected = wfv_gate
    if "status" in rejected.columns:
        rejected = rejected[rejected["status"] == REJECTED_WFV]

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
        return _empty_failure_breakdown()

    total_candidates = len(wfv_gate)
    breakdown = reasons.value_counts().rename_axis("failure_reason").reset_index(name="count")
    breakdown["pct_of_candidates"] = breakdown["count"] / total_candidates if total_candidates else np.nan
    return breakdown.sort_values(["count", "failure_reason"], ascending=[False, True]).reset_index(drop=True)


def build_wfv_window_diagnostics(wfv_window_results: pd.DataFrame) -> pd.DataFrame:
    """Summarize window-level WFV behavior across candidates."""
    if wfv_window_results.empty:
        return _empty_window_diagnostics()

    results = _window_results_with_effective_ic(wfv_window_results)
    test_ic_column = _test_ic_column(wfv_window_results)
    results["_raw_test_ic"] = pd.to_numeric(results[test_ic_column], errors="coerce")
    results["_abs_test_ic"] = results["_raw_test_ic"].abs()
    results["_direction_flip"] = results.apply(
        lambda row: _direction_flip_warning(row.get("signal_direction"), row["_raw_test_ic"]),
        axis=1,
    )

    rows: list[dict[str, object]] = []
    for window_id, group in results.groupby("window_id", sort=True, dropna=False):
        valid_abs = group["_abs_test_ic"].dropna()
        best_row = None
        if not valid_abs.empty:
            best_row = group.loc[group["_abs_test_ic"].idxmax()]

        rows.append(
            {
                "window_id": int(window_id),
                "test_start": group["test_start"].iloc[0] if "test_start" in group else pd.NaT,
                "test_end": group["test_end"].iloc[0] if "test_end" in group else pd.NaT,
                "n_candidates": int(group[["signal_name", "horizon"]].drop_duplicates().shape[0]),
                "avg_abs_test_ic": float(valid_abs.mean()) if not valid_abs.empty else np.nan,
                "median_abs_test_ic": float(valid_abs.median()) if not valid_abs.empty else np.nan,
                "n_positive_edges": int((pd.to_numeric(group["effective_test_ic"], errors="coerce") > 0).sum()),
                "n_direction_flips": int(group["_direction_flip"].sum()),
                "best_signal_name": best_row["signal_name"] if best_row is not None else None,
                "best_horizon": int(best_row["horizon"]) if best_row is not None and not pd.isna(best_row["horizon"]) else np.nan,
                "best_abs_test_ic": float(best_row["_abs_test_ic"]) if best_row is not None else np.nan,
            }
        )

    return pd.DataFrame(rows, columns=_empty_window_diagnostics().columns)


def build_signal_window_matrix(wfv_window_results: pd.DataFrame) -> pd.DataFrame:
    """Build a signal/horizon by window matrix of IC values."""
    if wfv_window_results.empty:
        return pd.DataFrame(columns=["signal_name", "horizon"])

    results = _window_results_with_effective_ic(wfv_window_results)
    value_column = "effective_test_ic" if "effective_test_ic" in results.columns else _test_ic_column(results)
    matrix = results.pivot_table(
        index=["signal_name", "horizon"],
        columns="window_id",
        values=value_column,
        aggfunc="mean",
    )
    matrix = matrix.rename(columns=lambda window_id: f"window_{int(window_id)}")
    return matrix.reset_index().sort_values(["signal_name", "horizon"]).reset_index(drop=True)


__all__ = [
    "APPROVED_WFV",
    "REJECTED_WFV",
    "WATCHLIST_WFV",
    "apply_wfv_gate",
    "build_signal_window_matrix",
    "build_wfv_failure_breakdown",
    "build_wfv_window_diagnostics",
    "summarize_wfv_results",
]
