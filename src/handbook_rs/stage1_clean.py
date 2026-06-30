"""Stage 1 — clean Quarto HTML into (a) full markdown for LLM grounding and
(b) prose-only text for term mining, plus a section-anchor map for citations.

The handbook is built with Quarto: content lives in ``main.content``; anchor
targets are ``<section id=...>``; code is ``div.cell`` / ``div.sourceCode``;
math is ``span.math``. We keep code (fenced) in the markdown but exclude code,
math, figures, and the bibliography from the prose used for keyphrase mining.
"""

from __future__ import annotations

import re
from pathlib import Path

from bs4 import BeautifulSoup, Tag
from markdownify import markdownify as md

from .config import build_dir, get_config
from .io_utils import write_json
from .pages import PAGES
from .stage0_fetch import pages_dir

# Elements that are navigation / layout chrome, never content.
CHROME_SELECTORS = [
    "nav", "footer", "#quarto-header", "#quarto-sidebar", "#quarto-margin-sidebar",
    ".sidebar", "#TOC", ".toc-actions", ".quarto-title-banner", "#quarto-back-to-top",
    ".nav-footer", "script", "style", "noscript", ".page-navigation",
    ".reproducible-notice", ".reproducible-local-notice", ".quarto-notification",
]
# Within content, drop these from the *mining* text (kept in markdown except math).
NONPROSE_SELECTORS = ["div.cell", "div.sourceCode", "pre", "figure", "span.math",
                      ".header-section-number"]


def md_dir() -> Path:
    p = build_dir() / "02_markdown"
    p.mkdir(parents=True, exist_ok=True)
    return p


def _clean_heading(sec: Tag) -> str:
    h = sec.find(["h1", "h2", "h3", "h4", "h5"], recursive=True)
    if not h:
        return ""
    # Drop the "6.3" section-number span before reading the title.
    for span in h.select(".header-section-number"):
        span.decompose()
    return re.sub(r"\s+", " ", h.get_text(" ", strip=True)).strip()


def _section_own_prose(sec: Tag) -> str:
    """Text of a section excluding nested child sections, code, math, figures."""
    clone = BeautifulSoup(str(sec), "lxml")
    root = clone.find("section")
    for child in root.find_all("section"):  # nested descendants only
        child.decompose()
    for sel in NONPROSE_SELECTORS:
        for el in root.select(sel):
            el.decompose()
    return re.sub(r"\n{3,}", "\n\n", root.get_text("\n", strip=True))


def clean_html(html: str, *, title_fallback: str) -> dict:
    soup = BeautifulSoup(html, "lxml")
    main = soup.select_one("main.content") or soup.select_one("main") or soup.body or soup

    # 1) strip chrome
    for sel in CHROME_SELECTORS:
        for el in main.select(sel):
            el.decompose()

    # 2) page title
    h1 = main.find("h1")
    if h1:
        for span in h1.select(".header-section-number"):
            span.decompose()
        page_title = re.sub(r"\s+", " ", h1.get_text(" ", strip=True)).strip()
    else:
        page_title = title_fallback

    # 3) anchor map + per-section excerpts (drop bibliography/footnotes from mining)
    anchors: dict[str, str] = {}
    sections: list[dict] = []
    skip_ids = {"references", "footnotes", "bibliography"}
    for sec in main.find_all("section", id=True):
        sid = sec.get("id")
        heading = _clean_heading(sec)
        anchors[f"#{sid}"] = heading
        if sid.lower() in skip_ids:
            continue
        prose = _section_own_prose(sec)
        if prose.strip():
            sections.append({"id": sid, "anchor": f"#{sid}", "title": heading, "prose": prose})

    # 4) full markdown for grounding (keep code, drop the bibliography to save tokens)
    md_soup = BeautifulSoup(str(main), "lxml")
    for sid in skip_ids:
        for el in md_soup.select(f"section#{sid}"):
            el.decompose()
    markdown = md(str(md_soup), heading_style="ATX", strip=["a"]).strip()
    markdown = re.sub(r"\n{3,}", "\n\n", markdown)

    # 5) prose-only text for mining (no code, math, figures, bibliography)
    prose_soup = BeautifulSoup(str(main), "lxml")
    for sid in skip_ids:
        for el in prose_soup.select(f"section#{sid}"):
            el.decompose()
    for sel in NONPROSE_SELECTORS:
        for el in prose_soup.select(sel):
            el.decompose()
    prose = re.sub(r"\n{3,}", "\n\n", prose_soup.get_text("\n", strip=True))

    return {
        "title": page_title,
        "anchors": anchors,
        "sections": sections,
        "markdown": markdown,
        "prose": prose,
    }


def run(force: bool = False) -> Path:
    base = get_config()["book"]["base_url"].rstrip("/")
    out = md_dir()
    total_words = 0
    for pg in PAGES:
        dest = out / f"{pg.chapter_id}.json"
        if dest.exists() and not force:
            continue
        html = (pages_dir() / f"{pg.chapter_id}.html").read_text(encoding="utf-8")
        cleaned = clean_html(html, title_fallback=pg.title)
        record = {
            "chapter_id": pg.chapter_id,
            "filename": pg.filename,
            "book_section": pg.section,
            "is_chapter": pg.is_chapter,
            "url": f"{base}/{pg.filename}",
            **cleaned,
        }
        write_json(dest, record)
        w = len(cleaned["prose"].split())
        total_words += w
        print(f"  cleaned {pg.chapter_id:32s} {w:>6d} prose words  {len(cleaned['sections']):>3d} sections")
    print(f"Stage 1 done: ~{total_words:,} prose words total in {out}")
    return out


if __name__ == "__main__":
    run()
