"""Compare current 03D notebook outputs with a dry-run engine result."""

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
from src.scoring.regime_ic import REGIME_IC_VERSION, run_03d_regime_ic  # noqa: E402


STAMP_COLUMNS = ["run_id", "regime_ic_version"]


def _strip_storage_columns(df: pd.DataFrame) -> pd.DataFrame:
    return df.drop(columns=[column for column in STAMP_COLUMNS if column in df.columns]).copy()


def _normalize_frame(df: pd.DataFrame) -> pd.DataFrame:
    normalized = _strip_storage_columns(df)
    for column in normalized.columns:
        if column == "sign_flip_across_regimes":
            normalized[column] = normalized[column].map(
                lambda value: int(value) if not pd.isna(value) else value
            )
        elif pd.api.types.is_datetime64_any_dtype(normalized[column]) or column.lower() == "date":
            normalized[column] = pd.to_datetime(normalized[column], errors="coerce").dt.strftime("%Y-%m-%d")
        elif pd.api.types.is_float_dtype(normalized[column]):
            normalized[column] = pd.to_numeric(normalized[column], errors="coerce").round(12)
    normalized = normalized.reindex(sorted(normalized.columns), axis=1)
    if normalized.empty:
        return normalized
    sort_columns = normalized.columns.tolist()
    return normalized.sort_values(sort_columns, kind="mergesort", na_position="first").reset_index(drop=True)


def _frame_digest(df: pd.DataFrame) -> str:
    normalized = _normalize_frame(df)
    csv = normalized.to_csv(index=False, na_rep="<NA>")
    return hashlib.sha256(csv.encode("utf-8")).hexdigest()


def _status_counts(df: pd.DataFrame, column: str) -> dict[str, int]:
    if df.empty or column not in df.columns:
        return {}
    return df[column].value_counts(dropna=False).sort_index().astype(int).to_dict()


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
    parser = argparse.ArgumentParser(description="Dry-run parity checks for 03D regime-conditioned IC.")
    parser.add_argument("--db-path", default=None, help="Optional SQLite database path override.")
    parser.add_argument(
        "--regime-ic-version",
        default=REGIME_IC_VERSION,
        help="Regime IC version label for dry-run output.",
    )
    parser.add_argument(
        "--use-panel-cache",
        action="store_true",
        help="Run dry-run parity comparison through cached Parquet signal panels.",
    )
    parser.add_argument("--panel-cache-dir", default=None, help="Optional signal panel cache directory.")
    parser.add_argument(
        "--rebuild-panel-cache",
        action="store_true",
        help="Rebuild selected signal panel cache artifacts before parity comparison.",
    )
    args = parser.parse_args()

    current_features = load_table("regime_features_ic_current", db_path=args.db_path)
    current_daily = load_table("signal_regime_ic_daily_current", db_path=args.db_path)
    current_summary = load_table("signal_regime_ic_summary_current", db_path=args.db_path)
    current_fragility = load_table("signal_regime_fragility_current", db_path=args.db_path)
    current_opportunity = load_table("signal_regime_opportunity_summary_current", db_path=args.db_path)

    dry_run = run_03d_regime_ic(
        db_path=args.db_path,
        regime_ic_version=args.regime_ic_version,
        use_panel_cache=args.use_panel_cache,
        panel_cache_dir=args.panel_cache_dir,
        rebuild_panel_cache=args.rebuild_panel_cache,
        write=False,
        verbose=False,
    )
    dry_features = dry_run["regime_features"]
    dry_daily = dry_run["daily_regime_ic"]
    dry_summary = dry_run["regime_summary"]
    dry_fragility = dry_run["regime_fragility"]
    dry_opportunity = dry_run["regime_opportunity_summary"]

    comparison = pd.DataFrame(
        [
            _comparison_record("regime_feature_rows", len(current_features), len(dry_features)),
            _comparison_record("daily_ic_rows", len(current_daily), len(dry_daily)),
            _comparison_record("summary_rows", len(current_summary), len(dry_summary)),
            _comparison_record("fragility_rows", len(current_fragility), len(dry_fragility)),
            _comparison_record("opportunity_rows", len(current_opportunity), len(dry_opportunity)),
            _comparison_record(
                "fragility_counts",
                _status_counts(current_fragility, "regime_fragility_flag"),
                _status_counts(dry_fragility, "regime_fragility_flag"),
            ),
            _comparison_record(
                "recommended_use_counts",
                _status_counts(current_opportunity, "recommended_use"),
                _status_counts(dry_opportunity, "recommended_use"),
            ),
            _digest_record("regime_features_digest", current_features, dry_features),
            _digest_record("daily_ic_digest", current_daily, dry_daily),
            _digest_record("summary_digest", current_summary, dry_summary),
            _digest_record("fragility_digest", current_fragility, dry_fragility),
            _digest_record("opportunity_digest", current_opportunity, dry_opportunity),
        ]
    )

    print(comparison.to_string(index=False))
    return 0 if comparison["passed"].all() else 1


if __name__ == "__main__":
    raise SystemExit(main())
