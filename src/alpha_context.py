from __future__ import annotations

from collections.abc import Iterable

import pandas as pd


POSITIVE_EDGE = "POSITIVE_EDGE"
NEGATIVE_EDGE_REVERSE_SIGNAL = "NEGATIVE_EDGE_REVERSE_SIGNAL"


def _as_list(value: object) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [item.strip() for item in value.split(",") if item.strip()]
    if isinstance(value, Iterable):
        return [str(item) for item in value]
    return [str(value)]


def _direction_multiplier(signal_direction: str | None) -> float:
    if signal_direction in (None, "", POSITIVE_EDGE):
        return 1.0
    if signal_direction == NEGATIVE_EDGE_REVERSE_SIGNAL:
        return -1.0
    raise ValueError(
        "signal_direction must be POSITIVE_EDGE or NEGATIVE_EDGE_REVERSE_SIGNAL; "
        f"got {signal_direction!r}."
    )


def _normalize_candidate_config(candidate_config: list[dict[str, object]] | pd.DataFrame) -> list[dict[str, object]]:
    if isinstance(candidate_config, pd.DataFrame):
        return candidate_config.to_dict("records")
    return [dict(row) for row in candidate_config]


def _regime_by_date(regime_table: pd.DataFrame, regime_column: str) -> pd.Series:
    if "Date" not in regime_table.columns:
        raise ValueError("regime_table must include a Date column.")
    if regime_column not in regime_table.columns:
        raise ValueError(f"regime_table does not include regime_column '{regime_column}'.")

    regime = regime_table[["Date", regime_column]].copy()
    regime["Date"] = pd.to_datetime(regime["Date"], errors="coerce")
    return regime.dropna(subset=["Date"]).set_index("Date")[regime_column].sort_index()


def apply_regime_filter(
    signal_panel: pd.DataFrame,
    regime_table: pd.DataFrame,
    allowed_regimes: list[str] | tuple[str, ...] | set[str] | str,
    regime_column: str,
) -> pd.DataFrame:
    """Keep signal values only on dates where the selected regime is allowed."""
    panel = signal_panel.copy()
    panel.index = pd.to_datetime(panel.index)
    panel = panel.sort_index()

    allowed = set(_as_list(allowed_regimes))
    regime = _regime_by_date(regime_table, regime_column=regime_column)
    aligned_regime = regime.reindex(panel.index)
    active_dates = aligned_regime.isin(allowed)
    filtered = panel.copy()
    filtered.loc[~active_dates] = pd.NA
    return filtered


def build_conditional_alpha_candidates(
    signal_panels: dict[str, pd.DataFrame],
    regime_table: pd.DataFrame,
    candidate_config: list[dict[str, object]] | pd.DataFrame,
) -> tuple[dict[str, pd.DataFrame], pd.DataFrame]:
    """Build regime-conditioned alpha panels and metadata from raw signal panels."""
    alpha_candidates: dict[str, pd.DataFrame] = {}
    metadata_rows: list[dict[str, object]] = []

    for config in _normalize_candidate_config(candidate_config):
        signal_name = str(config["signal_name"])
        if signal_name not in signal_panels:
            raise KeyError(f"signal_name '{signal_name}' not found in signal_panels.")

        horizon = int(config["horizon"])
        regime_column = str(config["regime_column"])
        allowed_regimes = _as_list(config["allowed_regimes"])
        alpha_name = str(
            config.get("alpha_name")
            or f"{signal_name}_{horizon}d_{regime_column}_{'_'.join(allowed_regimes)}"
        )
        signal_direction = str(config.get("signal_direction", POSITIVE_EDGE))
        multiplier = _direction_multiplier(signal_direction)

        adjusted_signal = signal_panels[signal_name] * multiplier
        alpha_panel = apply_regime_filter(
            signal_panel=adjusted_signal,
            regime_table=regime_table,
            allowed_regimes=allowed_regimes,
            regime_column=regime_column,
        )
        alpha_candidates[alpha_name] = alpha_panel

        regime_filter_description = f"{regime_column} in {','.join(allowed_regimes)}"
        metadata_rows.append(
            {
                "alpha_name": alpha_name,
                "source_signal": signal_name,
                "horizon": horizon,
                "regime_column": regime_column,
                "allowed_regimes": ",".join(allowed_regimes),
                "signal_direction": signal_direction,
                "direction_multiplier": multiplier,
                "regime_filter_description": regime_filter_description,
                "notes": config.get("notes", ""),
            }
        )

    alpha_metadata = pd.DataFrame(metadata_rows)
    return alpha_candidates, alpha_metadata


__all__ = [
    "NEGATIVE_EDGE_REVERSE_SIGNAL",
    "POSITIVE_EDGE",
    "apply_regime_filter",
    "build_conditional_alpha_candidates",
]
