"""Smoke checks for the combined stress-to-portfolio dry-run pipeline."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from pipelines.run_stress_to_portfolio import (  # noqa: E402
    run_stress_to_portfolio,
    verify_stress_to_portfolio,
)


def main() -> int:
    results = run_stress_to_portfolio(write=False, verbose=False)
    checks = verify_stress_to_portfolio(results)

    print("combined_check_summary:")
    for check in checks:
        print(f"{check['check_name']}: {'PASS' if check['passed'] else 'FAIL'}")
        print(f"  {check['details']}")

    return 0 if all(check["passed"] for check in checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
