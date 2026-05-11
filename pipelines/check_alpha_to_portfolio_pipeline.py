"""Smoke checks for the combined alpha-to-portfolio dry-run pipeline."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from pipelines.run_alpha_to_portfolio import run_alpha_to_portfolio  # noqa: E402


BASELINE_ALPHA = "alpha_regime_blend_dynamic_v4_smooth"


def _check(name: str, passed: bool, details: str) -> dict[str, object]:
    return {"check_name": name, "passed": bool(passed), "details": details}


def main() -> int:
    results = run_alpha_to_portfolio(write=False, verbose=False)
    stage_08 = results["08_survivor_freeze"]
    stage_09 = results["09_portfolio_construction"]
    stage_09b = results["09b_dashboard"]

    final_core = stage_08["final_core_registry"]
    portfolio_alpha_pool = stage_09["portfolio_alpha_pool"]
    dashboard_validation = stage_09b["validation_report"]

    final_core_names = set(final_core["alpha_name"].dropna())
    portfolio_alpha_names = set(portfolio_alpha_pool["alpha_name"].dropna())

    checks = [
        _check(
            "08_final_core_survivor_exists",
            len(final_core_names) > 0,
            f"final_core_names={sorted(final_core_names)}",
        ),
        _check(
            "09_uses_only_final_core_survivors",
            portfolio_alpha_names == final_core_names,
            f"portfolio_alpha_names={sorted(portfolio_alpha_names)}; final_core_names={sorted(final_core_names)}",
        ),
        _check(
            "09b_validation_passed",
            bool(dashboard_validation["passed"].all()),
            dashboard_validation.to_dict("records").__repr__(),
        ),
        _check(
            "baseline_final_alpha_matches",
            final_core_names == {BASELINE_ALPHA},
            f"expected={[BASELINE_ALPHA]}; actual={sorted(final_core_names)}",
        ),
    ]

    for check in checks:
        print(f"{check['check_name']}: {'PASS' if check['passed'] else 'FAIL'}")
        print(f"  {check['details']}")

    return 0 if all(check["passed"] for check in checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
