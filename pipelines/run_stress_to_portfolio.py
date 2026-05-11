"""Run extracted 07 -> 08 -> 09 -> 09B engines in order."""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.alpha.stress import run_07_alpha_stress  # noqa: E402
from src.alpha.survivor_registry import run_08_survivor_freeze  # noqa: E402
from src.pipeline.registry import get_stage  # noqa: E402
from src.portfolio.construction import run_09_portfolio_construction  # noqa: E402
from src.portfolio.dashboard import run_09b_dashboard  # noqa: E402


STAGES = [
    ("07_alpha_stress", run_07_alpha_stress),
    ("08_survivor_freeze", run_08_survivor_freeze),
    ("09_portfolio_construction", run_09_portfolio_construction),
    ("09b_dashboard", run_09b_dashboard),
]


def _metric_value(summary, metric: str):
    if summary is None or summary.empty or not {"metric", "value"}.issubset(summary.columns):
        return None
    rows = summary.loc[summary["metric"].eq(metric), "value"]
    return rows.iloc[0] if not rows.empty else None


def _alpha_names(result: dict[str, object]) -> str:
    summary = result.get("summary")
    for metric in [
        "stress_candidate_names",
        "pre_ml_alpha_names",
        "alpha_names_used",
        "final_survivor_alpha_names",
    ]:
        value = _metric_value(summary, metric)
        if value:
            return str(value)
    return ""


def _stress_gate_count(result: dict[str, object]) -> object:
    stress_gate = result.get("stress_gate")
    if stress_gate is not None:
        return len(stress_gate)
    summary = result.get("summary")
    value = _metric_value(summary, "stress_gate_rows")
    return "" if value is None else value


def _core_survivor_count(result: dict[str, object]) -> object:
    summary = result.get("summary")
    for metric in [
        "n_final_core_survivors",
        "n_promote_core_survivors",
        "n_final_survivors",
    ]:
        value = _metric_value(summary, metric)
        if value is not None:
            return value
    survivor_registry = result.get("survivor_registry")
    if survivor_registry is not None and "promotion_decision_final" in survivor_registry.columns:
        return int(survivor_registry["promotion_decision_final"].eq("PROMOTE_CORE").sum())
    return ""


def _portfolio_method_count(result: dict[str, object]) -> object:
    summary = result.get("summary")
    method_value = _metric_value(summary, "portfolio_methods")
    if method_value:
        return len([name for name in str(method_value).split(", ") if name])
    alpha_pool = result.get("portfolio_alpha_pool")
    if alpha_pool is not None and "portfolio_method" in alpha_pool.columns:
        return int(alpha_pool["portfolio_method"].nunique())
    method_comparison = result.get("method_comparison")
    if method_comparison is not None and "portfolio_method" in method_comparison.columns:
        return int(method_comparison["portfolio_method"].nunique())
    return ""


def _validation_status(result: dict[str, object]) -> object:
    validation_report = result.get("validation_report")
    if validation_report is None:
        validation_report = result.get("portfolio_validation_report")
    if validation_report is not None and "passed" in validation_report.columns:
        return bool(validation_report["passed"].all())
    summary = result.get("summary")
    value = _metric_value(summary, "validation_checks_pass")
    return "" if value is None else value


def _print_stage_summary(stage_id: str, elapsed_seconds: float, result: dict[str, object]) -> None:
    print(f"stage_id: {stage_id}")
    print(f"  elapsed_seconds: {elapsed_seconds:.2f}")
    print(f"  stress_gate_rows: {_stress_gate_count(result)}")
    print(f"  core_survivor_count: {_core_survivor_count(result)}")
    print(f"  alpha_names_used: {_alpha_names(result)}")
    print(f"  portfolio_method_count: {_portfolio_method_count(result)}")
    print(f"  validation_status: {_validation_status(result)}")


def _print_description() -> None:
    print("combined_pipeline: stress_to_portfolio")
    print("stages:")
    for stage_id, _ in STAGES:
        stage = get_stage(stage_id)
        print(f"  - stage_id: {stage.stage_id}")
        print(f"    notebook_path: {stage.notebook_path}")
        print(f"    current_module: {stage.current_module}")
        print(f"    current_function: {stage.current_function}")
        print(f"    input_tables: {', '.join(stage.expected_input_tables)}")
        print(f"    output_tables: {', '.join(stage.expected_output_tables)}")


def verify_stress_to_portfolio(results: dict[str, dict[str, object]]) -> list[dict[str, object]]:
    stage_07 = results["07_alpha_stress"]
    stage_08 = results["08_survivor_freeze"]
    stage_09 = results["09_portfolio_construction"]
    stage_09b = results["09b_dashboard"]

    stress_gate = stage_07["stress_gate"]
    final_core = stage_08["final_core_registry"]
    portfolio_alpha_pool = stage_09["portfolio_alpha_pool"]
    dashboard_validation = stage_09b["validation_report"]

    final_core_names = set(final_core["alpha_name"].dropna())
    portfolio_alpha_names = set(portfolio_alpha_pool["alpha_name"].dropna())

    return [
        {
            "check_name": "07_stress_gate_non_empty",
            "passed": not stress_gate.empty,
            "details": f"stress_gate_rows={len(stress_gate)}",
        },
        {
            "check_name": "08_final_core_survivor_exists",
            "passed": len(final_core_names) > 0,
            "details": f"final_core_names={sorted(final_core_names)}",
        },
        {
            "check_name": "09_uses_only_final_core_survivors",
            "passed": portfolio_alpha_names == final_core_names,
            "details": (
                f"portfolio_alpha_names={sorted(portfolio_alpha_names)}; "
                f"final_core_names={sorted(final_core_names)}"
            ),
        },
        {
            "check_name": "09b_validation_passed",
            "passed": bool(dashboard_validation["passed"].all()),
            "details": dashboard_validation.to_dict("records").__repr__(),
        },
    ]


def run_stress_to_portfolio(
    *,
    db_path=None,
    write: bool,
    verbose: bool,
) -> dict[str, dict[str, object]]:
    results: dict[str, dict[str, object]] = {}
    for stage_id, runner in STAGES:
        started = time.perf_counter()
        try:
            result = runner(db_path=db_path, write=write, verbose=verbose)
        except Exception as exc:
            elapsed = time.perf_counter() - started
            print(f"stage_failed: {stage_id}")
            print(f"  elapsed_seconds: {elapsed:.2f}")
            print(f"  error: {exc}")
            raise
        elapsed = time.perf_counter() - started
        results[stage_id] = result
        _print_stage_summary(stage_id, elapsed, result)

    checks = verify_stress_to_portfolio(results)
    for check in checks:
        print(f"{check['check_name']}: {'PASS' if check['passed'] else 'FAIL'}")
        print(f"  {check['details']}")
    if not all(check["passed"] for check in checks):
        raise ValueError("stress_to_portfolio verification failed")
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description="Run extracted 07 -> 08 -> 09 -> 09B engines.")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--describe", action="store_true", help="Print combined pipeline metadata.")
    mode.add_argument("--dry-run", action="store_true", help="Run all stages without SQLite writes.")
    mode.add_argument("--run", action="store_true", help="Run all stages and allow SQLite writes.")
    parser.add_argument("--db-path", default=None, help="Optional SQLite database path override.")
    parser.add_argument("--quiet", action="store_true", help="Suppress per-engine progress logging.")
    args = parser.parse_args()

    if args.describe:
        _print_description()
        return 0

    try:
        run_stress_to_portfolio(
            db_path=args.db_path,
            write=args.run,
            verbose=not args.quiet,
        )
    except Exception:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
