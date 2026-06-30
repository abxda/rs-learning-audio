"""Content-addressed disk cache for LLM calls.

Key = sha256 over the full request payload (model, params, messages). Because we
call with temperature=0, the same inputs deterministically map to one cache file,
so reruns are free and the whole build is idempotent/resumable.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Optional

from ..config import cache_dir


def call_key(payload: dict[str, Any]) -> str:
    blob = json.dumps(payload, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def _path(key: str) -> Path:
    return cache_dir() / f"{key}.json"


def get(key: str) -> Optional[dict[str, Any]]:
    p = _path(key)
    if p.exists():
        return json.loads(p.read_text())
    return None


def put(key: str, request: dict[str, Any], response: dict[str, Any]) -> None:
    _path(key).write_text(
        json.dumps({"request": request, "response": response}, ensure_ascii=False, indent=2)
    )
