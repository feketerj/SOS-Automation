#!/usr/bin/env python3
"""Terminal dashboard for the SOS pipeline without Streamlit."""

from __future__ import annotations

import itertools
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Iterable, List, Tuple

try:
    from config.loader import get_config  # type: ignore
except Exception:  # pragma: no cover
    get_config = None  # type: ignore

ROOT = Path(__file__).resolve().parents[1]
PYTHON = sys.executable
LOG_DIR = ROOT / "SOS_UI_Dashboard" / "logs"


def _load_config() -> dict:
    if get_config is None:
        return {}
    try:
        return get_config()
    except Exception:
        return {}


def _endpoints_path(cfg: dict) -> Path:
    location = cfg.get("pipeline.endpoints_file") or "endpoints.txt"
    return (ROOT / location).resolve()


def _read_endpoints(path: Path) -> List[str]:
    if not path.exists():
        return []
    endpoints: List[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        entry = line.strip()
        if entry and not entry.startswith('#'):
            endpoints.append(entry)
    return endpoints


def _write_endpoints(path: Path, endpoints: Iterable[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    unique = sorted(dict.fromkeys(endpoint.strip() for endpoint in endpoints if endpoint.strip()))
    path.write_text("\n".join(unique) + ("\n" if unique else ""), encoding="utf-8")


def _latest_output_dir(root: Path) -> Path | None:
    output_root = root / "SOS_Output"
    if not output_root.exists():
        return None
    candidates = []
    for month_dir in output_root.iterdir():
        if not month_dir.is_dir():
            continue
        for run_dir in month_dir.iterdir():
            if run_dir.is_dir():
                candidates.append(run_dir)
    if not candidates:
        return None
    return max(candidates, key=lambda p: p.stat().st_mtime)


def _stream_pipeline(validate_smoke: bool) -> Tuple[int, str]:
    cmd = [PYTHON, "tools/run_pipeline.py"]
    if validate_smoke:
        cmd.append("--validate-smoke")

    env = os.environ.copy()
    env.setdefault("PYTHONIOENCODING", "utf-8")

    process = subprocess.Popen(
        cmd,
        cwd=str(ROOT),
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        universal_newlines=True,
    )

    assert process.stdout is not None  # for mypy
    lines: List[str] = []
    try:
        for line in process.stdout:
            print(line, end="")
            lines.append(line)
    finally:
        process.stdout.close()
    return_code = process.wait()
    log_text = "".join(lines)
    return return_code, log_text


def _prompt(message: str) -> str:
    try:
        return input(message)
    except EOFError:
        return ""


def _press_enter() -> None:
    _prompt("\nPress Enter to continue...")


def _print_header(endpoints_file: Path, endpoints: List[str], validate_smoke: bool, last_run: Tuple[int, datetime, Path] | None) -> None:
    print("=" * 70)
    print("SOS Assessment Pipeline - Terminal Dashboard")
    print("=" * 70)
    print(f"Endpoint file: {endpoints_file}")
    print(f"Configured endpoints: {len(endpoints)}")
    if endpoints:
        preview = list(itertools.islice(endpoints, 5))
        print("Sample endpoints:")
        for idx, value in enumerate(preview, start=1):
            ellipsis = " ..." if idx == len(preview) and len(endpoints) > len(preview) else ""
            print(f"  {idx:>2}: {value}{ellipsis}")
    else:
        print("No endpoints configured yet.")
    print(f"Preflight smoke tests: {'ON' if validate_smoke else 'OFF'}")
    if last_run:
        code, timestamp, log_path = last_run
        status = "SUCCESS" if code == 0 else f"FAILED (exit {code})"
        print(f"Last pipeline run: {status} at {timestamp:%Y-%m-%d %H:%M:%S} | log: {log_path}")
    print("-" * 70)
    print("Select an option:")
    print("  1. List endpoints")
    print("  2. Add endpoint")
    print("  3. Remove endpoints")
    print("  4. Clear all endpoints")
    print(f"  5. Toggle preflight smoke tests (currently {'ON' if validate_smoke else 'OFF'})")
    print("  6. Run pipeline now")
    print("  7. Show latest results folder")
    print("  8. View last run log")
    print("  9. Quit")


def _list_endpoints(endpoints: List[str]) -> None:
    if not endpoints:
        print("\nNo endpoints configured.")
        return
    print("\nConfigured HigherGov search IDs:")
    for idx, value in enumerate(endpoints, start=1):
        print(f"  {idx:>2}. {value}")


def _add_endpoint(endpoints_file: Path, endpoints: List[str]) -> None:
    raw = _prompt("Enter a HigherGov search ID (comma separated for multiple): ").strip()
    if not raw:
        print("No value entered. Nothing added.")
        return
    additions = [entry.strip() for entry in raw.split(',') if entry.strip()]
    if not additions:
        print("No valid IDs detected.")
        return
    updated = endpoints + additions
    _write_endpoints(endpoints_file, updated)
    print(f"Added {len(additions)} entr{'y' if len(additions) == 1 else 'ies'}.")


def _remove_endpoints(endpoints_file: Path, endpoints: List[str]) -> None:
    if not endpoints:
        print("No endpoints to remove.")
        return
    _list_endpoints(endpoints)
    raw = _prompt("Enter numbers to remove (separated by space or comma): ")
    if not raw.strip():
        print("No selection made. Nothing removed.")
        return
    tokens = [token.strip() for token in raw.replace(',', ' ').split() if token.strip()]
    to_remove = set()
    for token in tokens:
        if not token.isdigit():
            print(f"Ignoring invalid index: {token}")
            continue
        idx = int(token)
        if 1 <= idx <= len(endpoints):
            to_remove.add(idx - 1)
        else:
            print(f"Index out of range: {idx}")
    if not to_remove:
        print("No valid indices provided. Nothing removed.")
        return
    updated = [value for idx, value in enumerate(endpoints) if idx not in to_remove]
    _write_endpoints(endpoints_file, updated)
    print(f"Removed {len(to_remove)} entr{'y' if len(to_remove) == 1 else 'ies'}.")


def _clear_endpoints(endpoints_file: Path, endpoints: List[str]) -> None:
    if not endpoints:
        print("Endpoint list already empty.")
        return
    confirm = _prompt("Are you sure you want to clear ALL endpoints? (y/N): ").strip().lower()
    if confirm == 'y':
        _write_endpoints(endpoints_file, [])
        print("All endpoints removed.")
    else:
        print("Clear action cancelled.")


def _run_pipeline_and_log(validate_smoke: bool) -> Tuple[int, datetime, Path]:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now()
    print("\nStarting pipeline...\n")
    code, output = _stream_pipeline(validate_smoke)
    log_path = LOG_DIR / f"pipeline_run_{timestamp:%Y%m%d_%H%M%S}.log"
    log_path.write_text(output, encoding="utf-8")
    print("\n" + "-" * 70)
    if code == 0:
        print(f"Pipeline completed successfully at {timestamp:%Y-%m-%d %H:%M:%S}.")
    else:
        print(f"Pipeline completed with exit code {code} at {timestamp:%Y-%m-%d %H:%M:%S}.")
    print(f"Output saved to: {log_path}")
    print("-" * 70)
    return code, timestamp, log_path


def _show_latest_results() -> None:
    latest_dir = _latest_output_dir(ROOT)
    if not latest_dir:
        print("\nNo pipeline outputs found yet.")
        return
    print(f"\nMost recent output folder: {latest_dir}")
    report_files = list(latest_dir.glob("*.md")) + list(latest_dir.glob("*.txt")) + list(latest_dir.glob("*.csv"))
    if not report_files:
        print("No summary files (.md/.txt/.csv) in the latest folder yet.")
        return
    print("Summary files:")
    for path in sorted(report_files):
        print(f"  - {path}")


def _view_last_log(last_run: Tuple[int, datetime, Path] | None) -> None:
    if not last_run:
        print("\nNo pipeline run recorded yet.")
        return
    log_path = last_run[2]
    if not log_path.exists():
        print(f"\nLog file missing: {log_path}")
        return
    print(f"\nShowing log: {log_path}\n")
    print(log_path.read_text(encoding="utf-8"))


def main() -> None:
    cfg = _load_config()
    endpoints_file = _endpoints_path(cfg)
    validate_smoke = True
    last_run: Tuple[int, datetime, Path] | None = None

    while True:
        endpoints = _read_endpoints(endpoints_file)
        _print_header(endpoints_file, endpoints, validate_smoke, last_run)
        choice = _prompt("Enter choice [1-9]: ").strip()
        if choice == '1':
            _list_endpoints(endpoints)
            _press_enter()
        elif choice == '2':
            _add_endpoint(endpoints_file, endpoints)
            _press_enter()
        elif choice == '3':
            _remove_endpoints(endpoints_file, endpoints)
            _press_enter()
        elif choice == '4':
            _clear_endpoints(endpoints_file, endpoints)
            _press_enter()
        elif choice == '5':
            validate_smoke = not validate_smoke
            print(f"Preflight smoke tests {'enabled' if validate_smoke else 'disabled'}.")
            _press_enter()
        elif choice == '6':
            if not endpoints:
                print("Cannot run pipeline without at least one endpoint configured.")
                _press_enter()
                continue
            last_run = _run_pipeline_and_log(validate_smoke)
            _press_enter()
        elif choice == '7':
            _show_latest_results()
            _press_enter()
        elif choice == '8':
            _view_last_log(last_run)
            _press_enter()
        elif choice == '9' or choice.lower() in {"q", "quit", "exit"}:
            print("Exiting. Goodbye!")
            break
        else:
            print(f"Unknown option: {choice}. Please choose between 1 and 9.")
            _press_enter()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted. Exiting...")