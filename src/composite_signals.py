from __future__ import annotations

from collections.abc import Mapping, Sequence

import numpy as np
import pandas as pd

from src.signal_storage import (
    load_candidate_signals,
    load_candidate_signals_by_names,
    pivot_signal_long_to_panel,
)


POSITIVE_EDGE = "POSITIVE_EDGE"
NEGATIVE_EDGE_REVERSE_SIGNAL = "NEGATIVE_EDGE_REVERSE_SIGNAL"


def load_component_signal_panels(
    component_names: Sequence[str] | None = None,
) -> dict[str, pd.DataFrame]:
    """Load candidate signal panels from SQLite and pivot to Date x ticker format."""
    if component_names is not None:
        selected_names = sorted({str(name) for name in component_names if pd.notna(name)})
        signal_long = load_candidate_signals_by_names(selected_names, current=True, chunksize=500_000)
    else:
        signal_long = load_candidate_signals(current=True)
    if signal_long.empty:
        return {}

    available_names = signal_long["signal_name"].dropna().unique().tolist()
    selected_names = list(component_names) if component_names is not None else sorted(available_names)
    missing_names = sorted(set(selected_names).difference(available_names))
    if missing_names:
        raise ValueError(f"Component signals not found in candidate_signals_current: {missing_names}")

    return {
        signal_name: pivot_signal_long_to_panel(signal_long, signal_name)
        for signal_name in selected_names
    }


def direction_adjust_component(
    signal_panel: pd.DataFrame,
    signal_direction: str,
) -> pd.DataFrame:
    """Orient a component so higher values match the historically favorable edge."""
    if signal_direction == NEGATIVE_EDGE_REVERSE_SIGNAL:
        return signal_panel * -1.0
    if signal_direction == POSITIVE_EDGE:
        return signal_panel.copy()
    raise ValueError(
        "signal_direction must be POSITIVE_EDGE or NEGATIVE_EDGE_REVERSE_SIGNAL; "
        f"received {signal_direction!r}."
    )


def normalize_component_panel(signal_panel: pd.DataFrame) -> pd.DataFrame:
    """Cross-sectionally rank each date and center ranks around zero."""
    if signal_panel.empty:
        return signal_panel.copy()
    ranked = signal_panel.rank(axis=1, pct=True, method="average", na_option="keep")
    return ranked.sub(0.5).replace([np.inf, -np.inf], np.nan)


def _align_component_panels(
    component_panels: Mapping[str, pd.DataFrame],
) -> dict[str, pd.DataFrame]:
    if not component_panels:
        return {}

    common_index: pd.Index | None = None
    common_columns: pd.Index | None = None
    for panel in component_panels.values():
        if common_index is None:
            common_index = panel.index
            common_columns = panel.columns
        else:
            common_index = common_index.intersection(panel.index)
            common_columns = common_columns.intersection(panel.columns)

    if common_index is None or common_columns is None:
        return {}

    return {
        name: panel.reindex(index=common_index, columns=common_columns).sort_index().sort_index(axis=1)
        for name, panel in component_panels.items()
    }


def build_composite_signal(
    component_panels: Mapping[str, pd.DataFrame],
    weights: Mapping[str, float],
) -> pd.DataFrame:
    """Build one weighted composite from aligned, normalized component panels."""
    if not component_panels:
        return pd.DataFrame()

    missing_weights = sorted(set(component_panels).difference(weights))
    if missing_weights:
        raise ValueError(f"Missing weights for components: {missing_weights}")

    aligned_panels = _align_component_panels(component_panels)
    if not aligned_panels:
        return pd.DataFrame()

    template = next(iter(aligned_panels.values()))
    weighted_sum = pd.DataFrame(0.0, index=template.index, columns=template.columns)
    available_weight_sum = pd.DataFrame(0.0, index=template.index, columns=template.columns)

    for component_name, panel in aligned_panels.items():
        weight = float(weights[component_name])
        normalized = normalize_component_panel(panel)
        finite_mask = normalized.notna()
        weighted_sum = weighted_sum.add(normalized.fillna(0.0).mul(weight), fill_value=0.0)
        available_weight_sum = available_weight_sum.add(finite_mask.astype(float).mul(abs(weight)), fill_value=0.0)

    composite = weighted_sum.div(available_weight_sum.replace(0.0, np.nan))
    return composite.replace([np.inf, -np.inf], np.nan).sort_index().sort_index(axis=1)


def build_composite_library(
    component_signal_panels: Mapping[str, pd.DataFrame],
    component_direction_map: Mapping[str, str],
    composite_config: Mapping[str, Mapping[str, float]],
    run_id: str,
    composite_version: str,
) -> tuple[dict[str, pd.DataFrame], pd.DataFrame]:
    """Build a fixed-weight composite signal library and metadata."""
    composite_signals: dict[str, pd.DataFrame] = {}
    metadata_rows: list[dict[str, object]] = []
    created_timestamp = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")

    for composite_name, weights in composite_config.items():
        component_names = list(weights)
        missing_components = sorted(set(component_names).difference(component_signal_panels))
        if missing_components:
            raise ValueError(f"{composite_name} is missing component panels: {missing_components}")

        missing_directions = sorted(set(component_names).difference(component_direction_map))
        if missing_directions:
            raise ValueError(f"{composite_name} is missing component directions: {missing_directions}")

        adjusted_components = {
            component_name: direction_adjust_component(
                component_signal_panels[component_name],
                component_direction_map[component_name],
            )
            for component_name in component_names
        }
        composite_signals[composite_name] = build_composite_signal(adjusted_components, weights)

        metadata_rows.append(
            {
                "composite_name": composite_name,
                "n_components": len(component_names),
                "component_signals": ",".join(component_names),
                "component_weights": ",".join(
                    f"{component_name}={float(weights[component_name]):g}"
                    for component_name in component_names
                ),
                "component_directions": ",".join(
                    f"{component_name}={component_direction_map[component_name]}"
                    for component_name in component_names
                ),
                "normalization": "component_rank_pct_centered_by_date",
                "formula_type": "fixed_weight_average_of_direction_adjusted_components",
                "run_id": run_id,
                "composite_version": composite_version,
                "created_timestamp": created_timestamp,
            }
        )

    metadata = pd.DataFrame(metadata_rows)
    return composite_signals, metadata


__all__ = [
    "NEGATIVE_EDGE_REVERSE_SIGNAL",
    "POSITIVE_EDGE",
    "build_composite_library",
    "build_composite_signal",
    "direction_adjust_component",
    "load_component_signal_panels",
    "normalize_component_panel",
]
