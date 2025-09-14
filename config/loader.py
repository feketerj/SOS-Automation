#!/usr/bin/env python3
"""
Lightweight configuration loader (optional, read-only).

Goals (low risk):
- Prefer environment variables for secrets/urls
- Optionally load a JSON settings file (config/settings.json),
  falling back to config/settings.example.json if available
- Provide a unified get_config() call without wiring into runtime

NOTE: This module does not change application behavior unless
      explicitly imported and used by a caller.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict

ROOT = Path(__file__).resolve().parents[1]
CONF_DIR = ROOT / "config"

DEFAULTS: Dict[str, Any] = {
    # Logging
    "logging.level": "INFO",
    # Timeouts
    "timeouts.api_request_seconds": 60,
    "timeouts.document_fetch_seconds": 120,
    # Pipeline
    "pipeline.max_documents": 100,
    "pipeline.text_extraction_char_limit": 400_000,
}

def _flatten(prefix: str, obj: Dict[str, Any], out: Dict[str, Any]) -> None:
    for k, v in obj.items():
        key = f"{prefix}.{k}" if prefix else k
        if isinstance(v, dict):
            _flatten(key, v, out)
        else:
            out[key] = v

def _load_settings() -> Dict[str, Any]:
    # Try config/settings.json; fall back to example
    for name in ("settings.json", "settings.example.json"):
        p = CONF_DIR / name
        if p.exists():
            try:
                data = json.loads(p.read_text(encoding="utf-8"))
                flat: Dict[str, Any] = {}
                _flatten("", data, flat)
                return flat
            except Exception:
                # Non-fatal: return empty if malformed
                return {}
    return {}

def _env() -> Dict[str, Any]:
    # Map well-known env vars
    env_map = {
        # HigherGov
        "highergov.api_key": os.environ.get("HIGHERGOV_API_KEY"),
        "highergov.base_url": os.environ.get("HG_API_BASE_URL"),
        # Mistral / Model
        "mistral.api_key": os.environ.get("MISTRAL_API_KEY"),
        "mistral.base_url": os.environ.get("MISTRAL_API_BASE_URL"),
        # Proxy (optional)
        "network.http_proxy": os.environ.get("HTTP_PROXY"),
        "network.https_proxy": os.environ.get("HTTPS_PROXY"),
    }
    # Remove Nones
    return {k: v for k, v in env_map.items() if v is not None}

def get_config() -> Dict[str, Any]:
    """Return merged config (env > settings > defaults)."""
    merged: Dict[str, Any] = {}
    merged.update(DEFAULTS)
    merged.update(_load_settings())
    merged.update(_env())
    return merged

if __name__ == "__main__":
    cfg = get_config()
    # Print a small, redacted view
    print("Resolved configuration (keys only):")
    for k in sorted(cfg.keys()):
        v = cfg[k]
        if any(x in k for x in ("api_key", "token", "secret")):
            print(f"  {k}: **** (redacted)")
        else:
            print(f"  {k}: {v}")

