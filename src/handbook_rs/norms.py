"""Surface-form normalization shared by mining, closure, and alias matching.

A normalized key is the lookup identity of a term: lowercase, punctuation-folded,
whitespace-collapsed. Two surface forms with the same normalized key are treated
as the same lexical item (before any semantic merge).
"""

from __future__ import annotations

import re

_WS = re.compile(r"\s+")
_KEEP = re.compile(r"[^a-z0-9\s\-/]")


def normalize(s: str) -> str:
    s = s.lower().strip().replace("’", "'").replace("–", "-").replace("—", "-")
    s = _KEEP.sub(" ", s)
    s = s.replace(" - ", " ").replace("/", " ")
    s = _WS.sub(" ", s).strip()
    return s


def slugify(s: str) -> str:
    s = normalize(s)
    return _WS.sub("-", s)[:80].strip("-")
