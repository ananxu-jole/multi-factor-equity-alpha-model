from __future__ import annotations

import json
from pathlib import Path
from typing import List

import pandas as pd

SCHEMA_PATH = Path(__file__).parent / "registry_schema.json"


class RegistryValidationError(Exception):
    pass


def _manual_checks(records: List[dict]) -> List[str]:
    errors: List[str] = []
    seen_ids = set()
    allowed_redundancy = {"low", "medium", "medium-high", "high", "unknown"}

    for i, r in enumerate(records):
        cid = r.get("candidate_id")
        if not cid:
            errors.append(f"row[{i}]: missing candidate_id")
        else:
            if cid in seen_ids:
                errors.append(f"duplicate candidate_id: {cid}")
            seen_ids.add(cid)

        # required string fields
        for fld in (
            "signal_name",
            "family",
            "theme",
            "feature_group",
            "horizon",
            "redundancy_risk",
            "research_status",
            "run_id",
        ):
            if not r.get(fld):
                errors.append(f"{cid or i}: missing {fld}")

        rr = r.get("redundancy_risk")
        if rr and rr not in allowed_redundancy:
            errors.append(f"{cid or i}: redundancy_risk '{rr}' not in allowed {sorted(allowed_redundancy)}")

    return errors


def validate_registry_df(df: pd.DataFrame, schema_path: Path | None = None) -> None:
    """Validate the candidate registry DataFrame.

    The function will attempt to use `jsonschema` if available; otherwise
    it falls back to a set of lightweight manual checks. Raises
    `RegistryValidationError` on validation failure.
    """
    records = df.to_dict(orient="records")

    errors: List[str] = []

    # try jsonschema if available
    try:
        import jsonschema

        schema_file = schema_path or SCHEMA_PATH
        with open(schema_file, "r", encoding="utf-8") as fh:
            schema = json.load(fh)

        validator = jsonschema.Draft7Validator(schema)
        for e in validator.iter_errors(records):
            loc = "->".join(str(x) for x in e.path)
            errors.append(f"{loc}: {e.message}")
    except Exception:
        # ignore jsonschema availability/errors — we'll still run manual checks
        pass

    # always run manual checks for constraints not expressible in simple schema
    errors += _manual_checks(records)

    if errors:
        raise RegistryValidationError("; ".join(errors))


def load_schema_text(schema_path: Path | None = None) -> str:
    p = schema_path or SCHEMA_PATH
    return p.read_text(encoding="utf-8")
