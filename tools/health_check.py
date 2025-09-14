#!/usr/bin/env python3
"""
Health check (optional, warn-only by default).

Usage:
  python tools/health_check.py [--live]

Checks:
  - Env vars present: HIGHERGOV_API_KEY, MISTRAL_API_KEY (warn if missing)
  - URL config present if set (HG_API_BASE_URL, MISTRAL_API_BASE_URL)
  - If --live: perform minimal connectivity checks with short timeouts

Notes:
  - No changes to application state. Safe to run preflight.
  - Live checks are best-effort and will only print warnings on error.
"""

import os
import sys
from typing import Optional


def warn(msg: str):
    print(f"WARN: {msg}")


def ok(msg: str):
    print(f"OK  : {msg}")


def check_env():
    print("[1] Checking environment variables")
    hg = os.environ.get("HIGHERGOV_API_KEY")
    mi = os.environ.get("MISTRAL_API_KEY")
    print(f"  HIGHERGOV_API_KEY: {'set' if hg else 'missing'}")
    print(f"  MISTRAL_API_KEY  : {'set' if mi else 'missing'}")
    if not hg:
        warn("HIGHERGOV_API_KEY not set (HigherGov fetch may fail)")
    if not mi:
        warn("MISTRAL_API_KEY not set (batch/agent may fail)")

    hg_url = os.environ.get("HG_API_BASE_URL")
    mi_url = os.environ.get("MISTRAL_API_BASE_URL")
    if hg_url:
        ok(f"HG_API_BASE_URL: {hg_url}")
    if mi_url:
        ok(f"MISTRAL_API_BASE_URL: {mi_url}")


def live_highergov() -> None:
    try:
        import requests  # type: ignore
    except Exception:
        warn("requests not installed; skipping HigherGov live check")
        return
    api_key = os.environ.get("HIGHERGOV_API_KEY")
    if not api_key:
        warn("HIGHERGOV_API_KEY missing; skipping HigherGov live check")
        return
    base = os.environ.get("HG_API_BASE_URL", "https://www.highergov.com/api-external/opportunity/")
    params = {"api_key": api_key, "search_id": "dummy", "page_size": 1, "page_number": 1}
    try:
        r = requests.get(base, params=params, timeout=5)
        print(f"  HigherGov status: {r.status_code}")
        if r.status_code in (401, 403):
            warn("HigherGov auth failed (401/403)")
        elif r.status_code >= 500:
            warn("HigherGov server error (>=500)")
        else:
            ok("HigherGov reachable")
    except Exception as e:
        warn(f"HigherGov connectivity error: {e}")


def live_mistral() -> None:
    api_key = os.environ.get("MISTRAL_API_KEY")
    if not api_key:
        warn("MISTRAL_API_KEY missing; skipping Mistral live check")
        return
    try:
        from mistralai import Mistral  # type: ignore
        client = Mistral(api_key=api_key)
        # Lightweight API call: list files (does not modify state)
        try:
            _ = client.files.list()
            ok("Mistral reachable")
        except Exception as e:
            warn(f"Mistral API error: {e}")
    except Exception as e:
        warn(f"mistralai not installed or import failed: {e}")


def main():
    live = "--live" in sys.argv[1:]
    print("=" * 60)
    print("SOS HEALTH CHECK (optional)")
    print("=" * 60)
    check_env()
    if live:
        print("\n[2] Live connectivity checks (best-effort)")
        live_highergov()
        live_mistral()
    print("\nDone.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

