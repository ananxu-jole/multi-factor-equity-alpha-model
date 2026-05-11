from __future__ import annotations

import pandas as pd


SIGNAL_METADATA_COLUMNS = [
    "signal_name",
    "signal_family",
    "formula_type",
    "parameters",
    "data_dependencies",
    "lookback",
    "direction_convention",
    "input_fields",
    "normalization_notes",
    "normalization",
    "signal_source",
    "discovery_family",
    "discovery_version",
    "signal_template_name",
    "parameter_config_json",
    "signal_version",
    "run_id",
    "timestamp",
    "created_timestamp",
    "notes",
]


def build_signal_metadata_row(
    signal_name: str,
    signal_family: str,
    formula_type: str,
    lookback: int | None,
    direction_convention: str,
    input_fields: list[str] | tuple[str, ...],
    normalization: str,
    signal_version: str,
    run_id: str,
    created_timestamp: str,
    notes: str = "",
    parameters: str | dict[str, object] | None = None,
    data_dependencies: list[str] | tuple[str, ...] | None = None,
    normalization_notes: str | None = None,
    signal_source: str = "manual_core",
    discovery_family: str | None = None,
    discovery_version: str | None = None,
    signal_template_name: str | None = None,
    parameter_config_json: str | None = None,
) -> dict[str, object]:
    """Build one standardized signal metadata row."""
    if isinstance(parameters, dict):
        parameter_text = ",".join(f"{key}={value}" for key, value in sorted(parameters.items()))
    elif parameters is None:
        parameter_text = f"lookback={lookback}" if lookback is not None else ""
    else:
        parameter_text = str(parameters)

    dependencies = data_dependencies if data_dependencies is not None else input_fields
    normalization_text = normalization_notes if normalization_notes is not None else normalization

    return {
        "signal_name": signal_name,
        "signal_family": signal_family,
        "formula_type": formula_type,
        "parameters": parameter_text,
        "data_dependencies": ",".join(dependencies),
        "lookback": int(lookback) if lookback is not None else pd.NA,
        "direction_convention": direction_convention,
        "input_fields": ",".join(input_fields),
        "normalization_notes": normalization_text,
        "normalization": normalization,
        "signal_source": signal_source,
        "discovery_family": discovery_family or "",
        "discovery_version": discovery_version or "",
        "signal_template_name": signal_template_name or "",
        "parameter_config_json": parameter_config_json or "",
        "signal_version": signal_version,
        "run_id": run_id,
        "timestamp": created_timestamp,
        "created_timestamp": created_timestamp,
        "notes": notes,
    }


def build_signal_metadata(rows: list[dict[str, object]]) -> pd.DataFrame:
    """Return metadata with the canonical Phase 2 signal metadata column order."""
    return pd.DataFrame(rows, columns=SIGNAL_METADATA_COLUMNS)


__all__ = [
    "SIGNAL_METADATA_COLUMNS",
    "build_signal_metadata",
    "build_signal_metadata_row",
]
