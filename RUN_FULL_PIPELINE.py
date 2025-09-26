#!/usr/bin/env python3
"""Convenience wrapper for running the SOS pipeline end-to-end.

This script now delegates to the maintained runners instead of relying on
archived batch artifacts. Use it as a quick way to trigger either the single
search-id production flow or the combined batch/agent pipeline.
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent


def _run(cmd: list[str]) -> int:
    """Run a subprocess relative to the project root and return its exit code."""
    print("=" * 70)
    print("Forwarding pipeline request:")
    print("  $", " ".join(cmd))
    print("=" * 70)
    env = os.environ.copy()
    env.setdefault("PYTHONPATH", str(PROJECT_ROOT))
    result = subprocess.run(cmd, cwd=str(PROJECT_ROOT), env=env)
    return result.returncode


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run the SOS pipeline using the supported runners."
    )
    parser.add_argument(
        "search_id",
        nargs="?",
        help="Optional HigherGov search ID for a single production assessment.",
    )
    parser.add_argument(
        "--mode",
        choices=("batch", "agent", "batch-agent"),
        default="batch-agent",
        help="Pipeline mode when running without a specific search ID.",
    )
    parser.add_argument(
        "--verify",
        action="store_true",
        help="Forward --verify to RUN_MODES (enables agent verification in batch mode).",
    )
    parser.add_argument(
        "--skip-regex",
        action="store_true",
        help="Forward --skip-regex to RUN_MODES (not recommended).",
    )

    args = parser.parse_args()

    if args.search_id:
        cmd = [sys.executable, "LOCKED_PRODUCTION_RUNNER.py", args.search_id]
    else:
        cmd = [sys.executable, "RUN_MODES.py", "--mode", args.mode]
        if args.verify:
            cmd.append("--verify")
        if args.skip_regex:
            cmd.append("--skip-regex")

    return _run(cmd)


if __name__ == "__main__":
    sys.exit(main())
