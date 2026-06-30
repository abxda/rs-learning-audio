"""Shared access to the cleaned corpus: a single concatenated context block
(reused as a cached prompt prefix) and a valid-anchor index for citations."""

from __future__ import annotations

from functools import lru_cache

from .io_utils import read_json
from .pages import PAGES
from .stage1_clean import md_dir


@lru_cache(maxsize=1)
def records() -> dict[str, dict]:
    return {pg.chapter_id: read_json(md_dir() / f"{pg.chapter_id}.json") for pg in PAGES}


@lru_cache(maxsize=1)
def corpus_context() -> str:
    """Full handbook markdown, chapter-delimited. ~262k tokens; reused verbatim
    across calls so DeepSeek's server-side prefix cache keeps it cheap."""
    parts = []
    for pg in PAGES:
        rec = records()[pg.chapter_id]
        parts.append(f"\n\n===== CHAPTER [{pg.chapter_id}] — {rec['title']} "
                     f"(section: {pg.section}) =====\n\n{rec['markdown']}")
    return "".join(parts)


@lru_cache(maxsize=1)
def anchor_index() -> dict[str, dict[str, str]]:
    """{chapter_id: {anchor: heading_title}} — the set of valid citation targets."""
    return {cid: rec.get("anchors", {}) for cid, rec in records().items()}


@lru_cache(maxsize=1)
def anchor_index_compact() -> str:
    """Compact text listing of valid citation targets for prompts."""
    lines = []
    for pg in PAGES:
        anchors = anchor_index()[pg.chapter_id]
        if anchors:
            alist = " ".join(sorted(anchors.keys()))
            lines.append(f"[{pg.chapter_id}] {pg.title} :: {alist}")
        else:
            lines.append(f"[{pg.chapter_id}] {pg.title} :: (no sub-anchors; cite the page)")
    return "\n".join(lines)
