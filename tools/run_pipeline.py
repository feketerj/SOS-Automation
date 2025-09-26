#!/usr/bin/env python3
"""
High-level pipeline runner.
Runs preflight checks (optional) and executes the batch+agent pipeline.
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path
from typing import List

try:
    from config.loader import get_config  # type: ignore
except Exception:  # pragma: no cover
    get_config = None  # type: ignore

ROOT = Path(__file__).resolve().parents[1]
PYTHON = sys.executable


class PipelineError(Exception):
    """Raised when a prerequisite or subprocess fails."""


def _print_header(title: str) -> None:
    bar = "=" * 70
    print(f"\n{bar}\n{title}\n{bar}")


def _run_step(name: str, command: List[str], cwd: Path | None = None) -> None:
    cwd = cwd or ROOT
    env = os.environ.copy()
    env.setdefault("PYTHONIOENCODING", "utf-8")

    _print_header(f"RUNNING {name.upper()}")
    print(f"Command: {' '.join(command)}")
    print(f"Working directory: {cwd}")

    result = subprocess.run(command, cwd=str(cwd), env=env)
    if result.returncode != 0:
        raise PipelineError(f"{name} failed with exit code {result.returncode}")
    print(f"\n[OK] {name} completed successfully.")


def _check_prerequisites() -> None:
    _print_header("CHECKING PREREQUISITES")

    # API keys must live in API_KEYS; config/env overrides are optional
    try:
        import sys
        sys.path.insert(0, str(ROOT))
        from API_KEYS import HIGHERGOV_API_KEY as _LEGACY_HG_KEY, MISTRAL_API_KEY as _LEGACY_M_KEY  # type: ignore
    except Exception as exc:
        raise PipelineError("API_KEYS module not found. Create API_KEYS.py with HIGHERGOV_API_KEY and MISTRAL_API_KEY defined.") from exc

    if not _LEGACY_HG_KEY:
        raise PipelineError("HIGHERGOV_API_KEY missing in API_KEYS.py. Add the baked-in key once and rerun.")
    if not _LEGACY_M_KEY:
        raise PipelineError("MISTRAL_API_KEY missing in API_KEYS.py. Add the baked-in key once and rerun.")

    cfg = get_config() if get_config is not None else {}
    endpoints_path = ROOT / cfg.get('pipeline.endpoints_file', 'endpoints.txt')
    if not endpoints_path.exists():
        raise PipelineError(f"Endpoints file not found at {endpoints_path}. Use tools/endpoints_manager.py to set it up.")

    print("Configuration and endpoints file look good.")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run SOS pipeline with optional preflight checks.")
    parser.add_argument("--skip-preflight", action="store_true", help="Skip the smoke + single-batch preflight.")
    parser.add_argument("--preflight-only", action="store_true", help="Only run preflight checks and exit.")
    parser.add_argument("--validate-smoke", action="store_true", help="Request validation during the smoke run.")
    parser.add_argument("--skip-agent", action="store_true", help="Run batch processor without the agent verification stage.")
    args = parser.parse_args()

    try:
        _check_prerequisites()

        if not args.skip_preflight:
            cmd = [PYTHON, "tools/pipeline_preflight.py"]
            if args.validate_smoke:
                cmd.append("--validate-smoke")
            _run_step("Preflight", cmd)

        if args.preflight_only:
            print("Preflight completed. Skipping full pipeline as requested.")
            return 0

        batch_cmd = [PYTHON, "Mistral_Batch_Processor/FULL_BATCH_PROCESSOR.py"]
        if args.skip_agent:
            os.environ["SKIP_AGENT_VERIFICATION"] = "1"
        else:
            os.environ.pop("SKIP_AGENT_VERIFICATION", None)

        _run_step("Batch + Agent Pipeline", batch_cmd)

        print("\nPipeline finished successfully.")
        return 0

    except PipelineError as exc:
        print(f"\n[ERROR] {exc}")
        return 1
    except KeyboardInterrupt:
        print("\n[ABORTED] Pipeline interrupted by user.")
        return 130


if __name__ == "__main__":
    sys.exit(main())
