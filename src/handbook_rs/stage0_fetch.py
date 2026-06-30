"""Stage 0 — download the 37 handbook pages (33 chapters + 4 front matter)."""

from __future__ import annotations

import time
from pathlib import Path

import httpx

from .config import build_dir, get_config
from .pages import PAGES


def pages_dir() -> Path:
    p = build_dir() / "01_pages"
    p.mkdir(parents=True, exist_ok=True)
    return p


def run(force: bool = False) -> Path:
    base = get_config()["book"]["base_url"].rstrip("/")
    out = pages_dir()
    with httpx.Client(timeout=60, follow_redirects=True, headers={"User-Agent": "handbook-rs/0.1"}) as client:
        for pg in PAGES:
            dest = out / f"{pg.chapter_id}.html"
            if dest.exists() and not force:
                continue
            url = f"{base}/{pg.filename}"
            r = client.get(url)
            r.raise_for_status()
            dest.write_text(r.text, encoding="utf-8")
            print(f"  fetched {pg.chapter_id:32s} {len(r.text):>8d} bytes")
            time.sleep(0.3)  # be polite to GitHub Pages
    print(f"Stage 0 done: {len(list(out.glob('*.html')))} pages in {out}")
    return out


if __name__ == "__main__":
    run()
