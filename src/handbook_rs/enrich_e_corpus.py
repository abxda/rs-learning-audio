"""Phase E — build a FULL-TEXT reference corpus (not just abstracts).

Collects the references (book bibliography R0 + deep-research evidence), pulls
metadata/abstract via Semantic Scholar batch, then fetches FULL TEXT through a
fallback ladder: arXiv -> PMC -> open-access PDF (Unpaywall) -> web page. PDFs are
parsed with pypdf, HTML with trafilatura. Text is chunked for the vector index.
Honest coverage (full-text vs abstract-only) is reported.

Output: build/E_refs.json (per-ref) + build/E_chunks.json (chunks) + coverage.
"""

from __future__ import annotations

import json
import re
from concurrent.futures import ThreadPoolExecutor
from io import BytesIO
from pathlib import Path

import httpx

from .config import build_dir
from .io_utils import read_json, write_json
from .norms import slugify

UA = {"User-Agent": "Mozilla/5.0 (research; agricultural-statistics learning)"}
S2_BATCH = "https://api.semanticscholar.org/graph/v1/paper/batch"
S2_FIELDS = "title,abstract,tldr,year,venue,openAccessPdf,externalIds"
MIN_FULL = 1800   # chars threshold to count as "full text"
MAXLEN = 60000


def collect_refs() -> dict:
    """Unique references keyed by a stable id, with doi/arxiv/pmc/url + theme set."""
    refs: dict[str, dict] = {}

    def add(doi="", arxiv="", pmc="", url="", title="", theme=None):
        key = (doi.lower() if doi else "") or (f"arxiv:{arxiv}" if arxiv else "") or url or slugify(title)
        if not key:
            return
        r = refs.setdefault(key, {"id": slugify(key)[:60] or "ref", "doi": doi.lower(), "arxiv": arxiv,
                                  "pmc": pmc, "url": url, "title": title, "themes": set()})
        if theme is not None:
            r["themes"].add(int(theme))
        for k, v in (("doi", doi.lower()), ("arxiv", arxiv), ("pmc", pmc), ("url", url), ("title", title)):
            if v and not r.get(k):
                r[k] = v

    r0 = read_json(build_dir() / "R0_references.json")
    for t in r0["themes"]:
        for r in t["refs"]:
            doi = (r.get("dois") or [""])[0]
            add(doi=doi, url=r.get("url", ""), title=r.get("text", "")[:120], theme=t["idx"])
    ev = {}
    for b in ("R1_evidence_b1.json", "R1_evidence_b2.json", "R1_evidence_b3.json"):
        ev.update(read_json(build_dir() / b))
    for k, e in ev.items():
        for r in e.get("refs", []):
            u = r["u"]
            arx = (re.search(r"arxiv\.org/(?:abs|pdf)/(\d+\.\d+)", u) or [None, ""])[1]
            pmc = (re.search(r"PMC(\d+)", u) or [None, ""])[1]
            doi = (re.search(r"(10\.\d{4,9}/[^\s?]+)", u) or [None, ""])[1].rstrip("/")
            add(doi=doi, arxiv=arx, pmc=pmc, url=u, title=r["t"], theme=int(k))
    for r in refs.values():
        r["themes"] = sorted(r["themes"])
    return refs


def s2_batch(refs: dict) -> dict:
    ids, idmap = [], {}
    for r in refs.values():
        sid = (f"DOI:{r['doi']}" if r["doi"] else f"ARXIV:{r['arxiv']}" if r["arxiv"] else None)
        if sid:
            ids.append(sid); idmap[sid] = r["id"]
    meta = {}
    with httpx.Client(timeout=90) as c:
        for i in range(0, len(ids), 480):
            batch = ids[i:i + 480]
            try:
                resp = c.post(S2_BATCH, params={"fields": S2_FIELDS}, json={"ids": batch})
                for sid, m in zip(batch, resp.json()):
                    if m:
                        meta[idmap[sid]] = m
            except Exception as e:  # noqa: BLE001
                print(f"  S2 batch error: {str(e)[:60]}")
    return meta


def _pdf_text(data: bytes) -> str:
    try:
        from pypdf import PdfReader
        rd = PdfReader(BytesIO(data))
        return "\n".join((p.extract_text() or "") for p in rd.pages)[:MAXLEN]
    except Exception:
        return ""


def fetch_text(url: str) -> str:
    if not url:
        return ""
    try:
        with httpx.Client(timeout=35, follow_redirects=True, headers=UA) as c:
            r = c.get(url)
        if r.status_code >= 400:
            return ""
        data = r.content
        if data[:5] == b"%PDF-" or "application/pdf" in r.headers.get("content-type", ""):
            return _pdf_text(data)
        import trafilatura
        return (trafilatura.extract(r.text) or "")[:MAXLEN]
    except Exception:
        return ""


def full_text(r: dict, m: dict) -> tuple[str, str]:
    ext = m.get("externalIds") or {}
    arx = r.get("arxiv") or ext.get("ArXiv", "")
    pmc = r.get("pmc") or ext.get("PubMedCentral", "")
    oa = (m.get("openAccessPdf") or {}).get("url", "")
    for src, url in (("arxiv", f"https://arxiv.org/pdf/{arx}" if arx else ""),
                     ("pmc", f"https://pmc.ncbi.nlm.nih.gov/articles/PMC{pmc}/" if pmc else ""),
                     ("oa", oa), ("web", r.get("url", ""))):
        if not url:
            continue
        txt = fetch_text(url)
        if len(txt) >= MIN_FULL:
            return txt, src
    # fallback: abstract + tldr
    ab = m.get("abstract") or ""
    tldr = (m.get("tldr") or {}).get("text", "") if m.get("tldr") else ""
    return (ab + (" " + tldr if tldr else "")).strip(), "abstract"


def chunks(text: str, size: int = 2800, overlap: int = 300) -> list[str]:
    out, i = [], 0
    while i < len(text):
        c = text[i:i + size].strip()
        if len(c) > 120:
            out.append(c)
        i += size - overlap
    return out


def run(force: bool = False) -> Path:
    out = build_dir() / "E_refs.json"
    if out.exists() and not force:
        print("Phase E cached.")
        return out

    refs = collect_refs()
    print(f"  {len(refs)} unique references; querying Semantic Scholar ...")
    meta = s2_batch(refs)
    print(f"  metadata for {len(meta)} refs")

    rlist = list(refs.values())

    def do(r):
        m = meta.get(r["id"], {})
        txt, src = full_text(r, m)
        r2 = {**r, "title": (m.get("title") or r.get("title") or "")[:200],
              "year": m.get("year"), "venue": m.get("venue"),
              "source_type": src, "has_full_text": src != "abstract" and len(txt) >= MIN_FULL,
              "n_chars": len(txt), "text": txt}
        return r2

    print("  fetching full text (arxiv -> pmc -> oa pdf -> web) ...")
    with ThreadPoolExecutor(max_workers=8) as ex:
        done = list(ex.map(do, rlist))

    chunk_rows = []
    for r in done:
        for j, ch in enumerate(chunks(r["text"])):
            chunk_rows.append({"ref_id": r["id"], "chunk": j, "text": ch,
                               "title": r["title"], "year": r.get("year"),
                               "venue": r.get("venue"), "doi": r.get("doi"),
                               "url": r.get("url"), "themes": r["themes"],
                               "source_type": r["source_type"]})
    for r in done:
        r.pop("text", None)  # keep refs file light; chunks hold the text
    write_json(out, {"n": len(done), "refs": done})
    write_json(build_dir() / "E_chunks.json", {"n": len(chunk_rows), "chunks": chunk_rows})

    full = sum(1 for r in done if r["has_full_text"])
    by_src: dict = {}
    for r in done:
        by_src[r["source_type"]] = by_src.get(r["source_type"], 0) + 1
    print(f"Phase E done: {len(done)} refs, {full} with FULL TEXT ({100*full//max(1,len(done))}%), "
          f"{len(chunk_rows)} chunks")
    print("  by source:", dict(sorted(by_src.items(), key=lambda x: -x[1])))
    return out


if __name__ == "__main__":
    run()
