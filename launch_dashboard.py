#!/usr/bin/env python3
"""Robust launcher for the SOS pipeline terminal dashboard."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parent
VENV_DIR = ROOT / ".venv"
SCRIPTS_DIR = VENV_DIR / ("Scripts" if os.name == "nt" else "bin")
PYTHON_EXE = SCRIPTS_DIR / ("python.exe" if os.name == "nt" else "python")
PIP_EXE = SCRIPTS_DIR / ("pip.exe" if os.name == "nt" else "pip")
REQ_FILE = ROOT / "ui_service" / "requirements.txt"
CLI_SCRIPT = ROOT / "ui_service" / "dashboard_cli.py"
SENTINEL = VENV_DIR / "dashboard_cli_ready.txt"


def _assert_python_version() -> None:
    if sys.version_info < (3, 11):
        raise RuntimeError("Python 3.11 or newer is required to run the dashboard launcher.")


def _run(command: Iterable[str]) -> None:
    result = subprocess.run(list(command), check=False)
    if result.returncode != 0:
        joined = " ".join(str(part) for part in command)
        raise RuntimeError(f"Command failed with exit code {result.returncode}: {joined}")


def _ensure_venv() -> bool:
    created = False
    if not PYTHON_EXE.exists():
        print("[SETUP] Creating virtual environment (.venv)...")
        _run((sys.executable, "-m", "venv", str(VENV_DIR), "--upgrade-deps"))
        created = True
    elif not PIP_EXE.exists():
        print("[SETUP] Restoring pip inside the virtual environment...")
        _run((sys.executable, "-m", "venv", str(VENV_DIR), "--upgrade-deps"))
        created = True
    return created


def _requirements_present() -> bool:
    if not REQ_FILE.exists():
        return False
    for line in REQ_FILE.read_text(encoding="utf-8", errors="ignore").splitlines():
        stripped = line.strip()
        if stripped and not stripped.startswith("#"):
            return True
    return False


def _install_requirements() -> None:
    if not _requirements_present():
        return
    print("[SETUP] Installing dashboard dependencies...")
    _run((str(PYTHON_EXE), "-m", "pip", "install", "--upgrade", "pip"))
    _run((str(PYTHON_EXE), "-m", "pip", "install", "--disable-pip-version-check", "-r", str(REQ_FILE)))


def _ensure_cli_exists() -> None:
    if not CLI_SCRIPT.exists():
        raise FileNotFoundError(f"Dashboard CLI not found: {CLI_SCRIPT}")


def _launch_cli() -> int:
    env = os.environ.copy()
    env.setdefault("PYTHONIOENCODING", "utf-8")
    env["VIRTUAL_ENV"] = str(VENV_DIR)
    env["PATH"] = str(SCRIPTS_DIR) + os.pathsep + env.get("PATH", "")
    command = [str(PYTHON_EXE), str(CLI_SCRIPT)]
    result = subprocess.run(command, cwd=str(ROOT), env=env)
    return result.returncode


def main() -> int:
    try:
        _assert_python_version()
        created = _ensure_venv()
        _ensure_cli_exists()
        if created or not SENTINEL.exists():
            _install_requirements()
            SENTINEL.write_text("dashboard cli dependencies installed\n", encoding="utf-8")
        code = _launch_cli()
        if code != 0:
            print(f"[WARN] Dashboard exited with error code {code}.")
        return code
    except Exception as exc:  # noqa: BLE001
        print(f"[ERROR] {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())