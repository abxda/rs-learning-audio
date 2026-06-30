"""R0 — harvest the Handbook's own bibliography per chapter and map references to
the 14 learning themes (the seeds that trigger deep research)."""

from __future__ import annotations

import re
from pathlib import Path

from bs4 import BeautifulSoup

from .config import build_dir
from .io_utils import read_json, write_json
from .pages import PAGES
from .stage0_fetch import pages_dir

DOI_RE = re.compile(r"10\.\d{4,9}/[-._;()/:A-Z0-9]+", re.I)


def chapter_refs(html: str) -> list[dict]:
    soup = BeautifulSoup(html, "lxml")
    refs = []
    for i, e in enumerate(soup.select("div#refs .csl-entry") or soup.select(".csl-entry"), 1):
        text = re.sub(r"\s+", " ", e.get_text(" ", strip=True)).strip()
        urls = [a.get("href") for a in e.select("a[href]") if a.get("href")]
        dois = sorted(set(DOI_RE.findall(text) + DOI_RE.findall(" ".join(urls))))
        if text:
            refs.append({"n": i, "text": text, "dois": dois,
                         "url": (urls[0] if urls else (f"https://doi.org/{dois[0]}" if dois else ""))})
    return refs


def run(force: bool = False) -> Path:
    out = build_dir() / "R0_references.json"
    if out.exists() and not force:
        print("R0 cached.")
        return out

    # 1) references per chapter
    by_chapter: dict[str, list[dict]] = {}
    for pg in PAGES:
        html = (pages_dir() / f"{pg.chapter_id}.html").read_text(encoding="utf-8")
        refs = chapter_refs(html)
        if refs:
            by_chapter[pg.chapter_id] = refs
    total = sum(len(v) for v in by_chapter.values())
    print(f"  harvested {total} references across {len(by_chapter)} chapters")

    # 2) map references to themes via concept -> citation chapters -> cluster
    ont = read_json(build_dir().parent / "out" / "ontology.json")
    clu = read_json(build_dir() / "10_clusters.json")
    node_cluster = clu["node_cluster"]
    cl_by_idx = {c["idx"]: c for c in clu["clusters"]}
    cite_chapters: dict[int, set] = {c["idx"]: set() for c in clu["clusters"]}
    for n in ont["nodes"]:
        ci = node_cluster.get(n["id"])
        if ci is None:
            continue
        for c in n.get("citations", []):
            if c.get("chapter_id") in by_chapter:
                cite_chapters[ci].add(c["chapter_id"])

    themes = []
    for c in clu["clusters"]:
        chs = sorted(cite_chapters[c["idx"]])
        # dedup references by DOI/text across the theme's chapters
        seen, refs = set(), []
        for ch in chs:
            for r in by_chapter.get(ch, []):
                key = r["dois"][0] if r["dois"] else r["text"][:80]
                if key not in seen:
                    seen.add(key)
                    refs.append({**r, "chapter": ch})
        themes.append({"idx": c["idx"], "title": c["title"], "desc": c["desc"],
                       "reps": c["reps"], "size": c["size"], "chapters": chs,
                       "n_refs": len(refs), "refs": refs})

    write_json(out, {"by_chapter": by_chapter, "themes": themes,
                     "total_refs": total})
    print(f"R0 done -> {out}")
    for t in themes:
        print(f"  [{t['idx']:2d}] {t['title']['en']:34s} chapters={len(t['chapters'])} refs={t['n_refs']}")
    return out


if __name__ == "__main__":
    run()
