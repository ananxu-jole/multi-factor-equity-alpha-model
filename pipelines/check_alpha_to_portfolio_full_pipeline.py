"""Smoke checks for the full alpha-to-portfolio dry-run pipeline."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from pipelines.run_alpha_to_portfolio_full import (  # noqa: E402
    run_alpha_to_portfolio_full,
    verify_alpha_to_portfolio_full,
)


def main() -> int:
    results = run_alpha_to_portfolio_full(write=False, verbose=False)
    checks = verify_alpha_to_portfolio_full(results)

    print("combined_check_summary:")
    for check in checks:
        print(f"{check['check_name']}: {'PASS' if check['passed'] else 'FAIL'}")
        print(f"  {check['details']}")

    return 0 if all(check["passed"] for check in checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
