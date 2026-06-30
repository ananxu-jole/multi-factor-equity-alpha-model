"""Research-only economic context enrichment utilities.

This package provides metadata loaders, validators, diagnostics, and persistence
helpers for economic context research. It does not implement alpha candidates,
change validation logic, or authorize production use.
"""

from src.economic_context.schema import (
    DIAGNOSTIC_ONLY_LABEL,
    POINT_IN_TIME_VALIDATED,
    SNAPSHOT_WARNING,
    STATIC_SNAPSHOT_ONLY,
)

__all__ = [
    "DIAGNOSTIC_ONLY_LABEL",
    "POINT_IN_TIME_VALIDATED",
    "SNAPSHOT_WARNING",
    "STATIC_SNAPSHOT_ONLY",
]
