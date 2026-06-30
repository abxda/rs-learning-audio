"""OpenRouter chat client for deepseek/deepseek-v4-flash.

Deterministic (temperature=0), retried, and cached. Every call returns a
``CallResult`` whose ``call_id`` is the cache key — that id is stored in node
provenance so any concept traces back to the exact prompt that produced it.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from typing import Any, Optional

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from ..config import get_config, openrouter_key
from . import cache


@dataclass
class CallResult:
    text: str
    call_id: str
    cached: bool
    usage: dict[str, Any] = field(default_factory=dict)

    def json(self) -> Any:
        """Parse the response as JSON, tolerating ```json fences and stray prose.
        Falls back to salvaging complete objects from a truncated array."""
        try:
            return _extract_json(self.text)
        except LLMError:
            salvaged = _salvage_array(self.text)
            if salvaged is not None:
                return salvaged
            raise


class LLMError(RuntimeError):
    pass


def _extract_json(text: str) -> Any:
    s = text.strip()
    # Strip ```json ... ``` or ``` ... ``` fences.
    fence = re.match(r"^```(?:json)?\s*(.*?)\s*```$", s, re.DOTALL)
    if fence:
        s = fence.group(1).strip()
    try:
        return json.loads(s)
    except json.JSONDecodeError:
        # Fall back to the first balanced {...} or [...] block.
        for opener, closer in (("{", "}"), ("[", "]")):
            i, j = s.find(opener), s.rfind(closer)
            if 0 <= i < j:
                try:
                    return json.loads(s[i : j + 1])
                except json.JSONDecodeError:
                    continue
        raise LLMError(f"Could not parse JSON from response:\n{text[:500]}")


def _salvage_array(text: str) -> Any:
    """Recover complete objects from a truncated `{"key":[ {...}, {...}, ...`
    response. Returns {key: [parsed objects]} keeping every fully-formed element."""
    m = re.search(r'"(\w+)"\s*:\s*\[', text)
    if not m:
        return None
    key = m.group(1)
    objs, depth, start, instr, esc = [], 0, None, False, False
    for i in range(m.end(), len(text)):
        ch = text[i]
        if instr:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == '"':
                instr = False
            continue
        if ch == '"':
            instr = True
        elif ch == "{":
            if depth == 0:
                start = i
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0 and start is not None:
                try:
                    objs.append(json.loads(text[start:i + 1]))
                except json.JSONDecodeError:
                    pass
                start = None
        elif ch == "]" and depth == 0:
            break
    return {key: objs} if objs else None


@retry(
    retry=retry_if_exception_type((httpx.HTTPError, LLMError)),
    wait=wait_exponential(multiplier=2, min=2, max=30),
    stop=stop_after_attempt(3),
    reraise=True,
)
def _post(payload: dict[str, Any]) -> dict[str, Any]:
    cfg = get_config()["llm"]
    headers = {
        "Authorization": f"Bearer {openrouter_key()}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/handbook-rs",
        "X-Title": "UN Handbook Concept Tree",
    }
    with httpx.Client(timeout=cfg["request_timeout"]) as client:
        r = client.post(f"{cfg['base_url']}/chat/completions", headers=headers, json=payload)
        if r.status_code >= 400:
            # 429 / 5xx are retryable; surface body for 4xx config errors.
            raise LLMError(f"HTTP {r.status_code}: {r.text[:400]}")
        data = r.json()
    if "choices" not in data or not data["choices"]:
        raise LLMError(f"No choices in response: {json.dumps(data)[:400]}")
    msg = data["choices"][0].get("message", {})
    if not msg.get("content"):
        fr = data["choices"][0].get("finish_reason")
        raise LLMError(f"Empty content (finish_reason={fr}); likely truncated by max_tokens.")
    return data


def chat(
    system: str,
    user: str,
    *,
    json_mode: bool = False,
    max_tokens: Optional[int] = None,
) -> CallResult:
    """One cached chat completion. Identical inputs => cached file => no API call."""
    cfg = get_config()["llm"]
    payload: dict[str, Any] = {
        "model": cfg["model"],
        "temperature": cfg["temperature"],
        "top_p": cfg["top_p"],
        "max_tokens": max_tokens or cfg["max_tokens"],
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    }
    if json_mode:
        payload["response_format"] = {"type": "json_object"}

    key = cache.call_key(payload)
    hit = cache.get(key)
    if hit is not None:
        resp = hit["response"]
        return CallResult(
            text=resp["choices"][0]["message"]["content"],
            call_id=key,
            cached=True,
            usage=resp.get("usage", {}),
        )

    data = _post(payload)
    cache.put(key, payload, data)
    return CallResult(
        text=data["choices"][0]["message"]["content"],
        call_id=key,
        cached=False,
        usage=data.get("usage", {}),
    )
