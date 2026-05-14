"""Compare current 03 notebook outputs with a dry-run engine result."""

from __future__ import annotations

import argparse
import hashlib
import math
import sys
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.db import load_table  # noqa: E402
from src.scoring.signal_scoring import SCORING_VERSION, run_03_signal_scoring  # noqa: E402
from src.scoring.signal_scoring_storage import SCORING_TABLES  # noqa: E402


STAMP_COLUMNS = ["run_id", "scoring_version"]


def _strip_storage_columns(df: pd.DataFrame) -> pd.DataFrame:
    return df.drop(columns=[column for column in STAMP_COLUMNS if column in df.columns]).copy()


def _normalize_frame(df: pd.DataFrame) -> pd.DataFrame:
    normalized = _strip_storage_columns(df)
    for column in normalized.columns:
        if pd.api.types.is_datetime64_any_dtype(normalized[column]) or column.lower().endswith("date"):
            normalized[column] = pd.to_datetime(normalized[column], errors="coerce").dt.strftime("%Y-%m-%d")
        elif pd.api.types.is_float_dtype(normalized[column]):
            normalized[column] = pd.to_numeric(normalized[column], errors="coerce").round(12)
    normalized = normalized.reindex(sorted(normalized.columns), axis=1)
    if normalized.empty:
        return normalized
    return normalized.sort_values(normalized.columns.tolist(), kind="mergesort", na_position="first").reset_index(drop=True)


def _frame_digest(df: pd.DataFrame) -> str:
    csv = _normalize_frame(df).to_csv(index=False, na_rep="<NA>")
    return hashlib.sha256(csv.encode("utf-8")).hexdigest()


def _status_counts(df: pd.DataFrame) -> dict[str, int]:
    if df.empty or "status" not in df.columns:
        return {}
    return df["status"].value_counts(dropna=False).sort_index().astype(int).to_dict()


def _best_horizon_counts(df: pd.DataFrame) -> dict[int, int]:
    if df.empty or "best_horizon" not in df.columns:
        return {}
    counts = df["best_horizon"].value_counts(dropna=False).sort_index()
    return {int(key): int(value) for key, value in counts.items() if not pd.isna(key)}


def _close_enough(current: object, dry_run: object) -> bool:
    if isinstance(current, float) or isinstance(dry_run, float):
        if pd.isna(current) and pd.isna(dry_run):
            return True
        return math.isclose(float(current), float(dry_run), rel_tol=1e-10, abs_tol=1e-12)
    return current == dry_run


def _comparison_record(check_name: str, current: object, dry_run: object) -> dict[str, object]:
    return {
        "check_name": check_name,
        "passed": _close_enough(current, dry_run),
        "current": current,
        "dry_run": dry_run,
    }


def _digest_record(check_name: str, current: pd.DataFrame, dry_run: pd.DataFrame) -> dict[str, object]:
    current_digest = _frame_digest(current)
    dry_digest = _frame_digest(dry_run)
    return {
        "check_name": check_name,
        "passed": current_digest == dry_digest,
        "current": current_digest,
        "dry_run": dry_digest,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Dry-run parity checks for 03 signal scoring.")
    parser.add_argument("--db-path", default=None, help="Optional SQLite database path override.")
    parser.add_argument(
        "--scoring-version",
        default=SCORING_VERSION,
        help="Signal scoring version label for dry-run output.",
    )
    parser.add_argument("--use-panel-cache", action="store_true", help="Use cached signal panels for dry-run parity.")
    parser.add_argument("--panel-cache-dir", default=None, help="Optional signal panel cache directory.")
    parser.add_argument(
        "--rebuild-panel-cache",
        action="store_true",
        help="Rebuild selected signal panel cache artifacts before running parity.",
    )
    args = parser.parse_args()

    current = {
        artifact: load_table(current_table, db_path=args.db_path)
        for artifact, (current_table, _) in SCORING_TABLES.items()
    }
    dry_run = run_03_signal_scoring(
        db_path=args.db_path,
        scoring_version=args.scoring_version,
        use_panel_cache=args.use_panel_cache,
        panel_cache_dir=args.panel_cache_dir,
        rebuild_panel_cache=args.rebuild_panel_cache,
        write=False,
        verbose=False,
    )
    dry = {
        "scores": dry_run["scores"],
        "summary": dry_run["score_summary"],
        "gate": dry_run["scoring_gate"],
        "best_horizon": dry_run["best_horizon_summary"],
        "family_summary": dry_run["family_summary"],
    }

    records: list[dict[str, object]] = []
    for artifact in SCORING_TABLES:
        records.append(_comparison_record(f"{artifact}_rows", len(current[artifact]), len(dry[artifact])))
        records.append(_digest_record(f"{artifact}_digest", current[artifact], dry[artifact]))

    records.extend(
        [
            _comparison_record(
                "scores_signal_count",
                current["scores"]["signal_name"].nunique() if "signal_name" in current["scores"].columns else 0,
                dry["scores"]["signal_name"].nunique() if "signal_name" in dry["scores"].columns else 0,
            ),
            _comparison_record(
                "scores_horizon_count",
                current["scores"]["horizon"].nunique() if "horizon" in current["scores"].columns else 0,
                dry["scores"]["horizon"].nunique() if "horizon" in dry["scores"].columns else 0,
            ),
            _comparison_record("gate_status_counts", _status_counts(current["gate"]), _status_counts(dry["gate"])),
            _comparison_record(
                "best_horizon_counts",
                _best_horizon_counts(current["best_horizon"]),
                _best_horizon_counts(dry["best_horizon"]),
            ),
        ]
    )

    comparison = pd.DataFrame(records)
    print(comparison.to_string(index=False))
    return 0 if comparison["passed"].all() else 1


if __name__ == "__main__":
    raise SystemExit(main())
