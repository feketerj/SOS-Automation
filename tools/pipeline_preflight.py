#!/usr/bin/env python3
"""
Pipeline Preflight Runner
Runs smoke collection and single-batch checks with optional validation.
"""

import argparse
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def run_step(name: str, command: list[str], cwd: Path) -> bool:
    print(f"\n{'=' * 70}")
    print(f"RUNNING {name.upper()}")
    print(f"Command: {' '.join(command)}")
    print(f"Working directory: {cwd}")
    print(f"{'=' * 70}")
    try:
        subprocess.run(command, cwd=str(cwd), check=True)
        print(f"\n[OK] {name} completed successfully.")
        return True
    except subprocess.CalledProcessError as exc:
        print(f"\n[ERROR] {name} failed with exit code {exc.returncode}.")
        return False


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run recommended preflight checks before full pipeline execution."
    )
    parser.add_argument(
        "--skip-smoke",
        action="store_true",
        help="Skip the smoke collection step."
    )
    parser.add_argument(
        "--skip-single",
        action="store_true",
        help="Skip the single search-id batch check."
    )
    parser.add_argument(
        "--validate-smoke",
        action="store_true",
        help="Run validators during the smoke collection step."
    )
    args = parser.parse_args()

    python = sys.executable
    success = True

    if not args.skip_smoke:
        smoke_cmd = [python, "tools/smoke_run.py"]
        if args.validate_smoke:
            smoke_cmd.append("--validate")
        success = run_step("Smoke Run", smoke_cmd, REPO_ROOT)

    if success and not args.skip_single:
        single_cmd = [python, "run_batch_single.py"]
        success = run_step("Single Batch Check", single_cmd, REPO_ROOT)

    if success:
        print("\nAll requested preflight steps completed without errors.")
        return 0

    print("\nOne or more preflight steps failed. Review the logs above before continuing.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
