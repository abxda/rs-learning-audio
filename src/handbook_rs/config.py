"""Load config.yaml + .env once and expose typed access to settings/paths."""

from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

# Project root = two levels up from this file (src/handbook_rs/config.py -> repo root).
ROOT = Path(__file__).resolve().parents[2]


def _load_env() -> None:
    """Minimal .env loader (avoids a hard dependency on python-dotenv at import time)."""
    env_path = ROOT / ".env"
    if not env_path.exists():
        return
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, val = line.partition("=")
        key, val = key.strip(), val.strip().strip('"').strip("'")
        os.environ.setdefault(key, val)


@lru_cache(maxsize=1)
def get_config() -> dict[str, Any]:
    _load_env()
    cfg = yaml.safe_load((ROOT / "config.yaml").read_text())
    return cfg


def openrouter_key() -> str:
    _load_env()
    # The user's .env uses the lowercase `openrouter` key name.
    key = os.environ.get("openrouter") or os.environ.get("OPENROUTER_API_KEY")
    if not key:
        raise RuntimeError("OpenRouter API key not found (.env key 'openrouter').")
    return key


def build_dir() -> Path:
    p = ROOT / get_config()["paths"]["build"]
    p.mkdir(parents=True, exist_ok=True)
    return p


def out_dir() -> Path:
    p = ROOT / get_config()["paths"]["out"]
    p.mkdir(parents=True, exist_ok=True)
    return p


def cache_dir() -> Path:
    p = ROOT / get_config()["paths"]["cache"]
    p.mkdir(parents=True, exist_ok=True)
    return p
