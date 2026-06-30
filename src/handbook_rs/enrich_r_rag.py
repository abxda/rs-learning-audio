"""Phase R — for a concept, do a HYBRID retrieval over the Zvec corpus (dense
bge-m3 + native FTS), fuse with Reciprocal Rank Fusion, then let DeepSeek rerank
the passages and write a grounded bilingual 'Profundiza' enrichment + per-card
references + a literature-alignment verdict. Pilot over a few concepts."""

from __future__ import annotations

import json
import re
from pathlib import Path

import zvec
from zvec import Fts, Query

from .config import build_dir, out_dir
from .io_utils import read_json, write_json
import numpy as np

from .enrich_v_index import db_path, embed_texts

STOP = set("the of and to a in for with from that this is are by an on as it its their which "
           "los las una uno del que para con por una como sus este esta son the de la el en y a".split())


def keywords(text: str, k: int = 10) -> str:
    toks = re.findall(r"[A-Za-z][A-Za-z0-9\-]{2,}", text)
    seen, out = set(), []
    for t in toks:
        tl = t.lower()
        if tl in STOP or tl in seen:
            continue
        seen.add(tl); out.append(t)
        if len(out) >= k:
            break
    return " ".join(out)


def rrf(lists: list[list], k: int = 60, topn: int = 8) -> list:
    """Reciprocal Rank Fusion over result lists; dedupe to best chunk per ref_id."""
    score: dict[str, float] = {}
    doc: dict[str, object] = {}
    for lst in lists:
        for rank, d in enumerate(lst):
            score[d.id] = score.get(d.id, 0.0) + 1.0 / (k + rank)
            doc[d.id] = d
    order = sorted(score, key=lambda i: -score[i])
    seen_ref, fused = set(), []
    for i in order:
        ref = doc[i].fields.get("ref_id")
        if ref in seen_ref:
            continue
        seen_ref.add(ref); fused.append(doc[i])
        if len(fused) >= topn:
            break
    return fused


def retrieve(col, qtext: str, topk: int = 15) -> list:
    qv = embed_texts([qtext])[0]
    qe = (qv / (np.linalg.norm(qv) + 1e-9)).tolist()
    fields = ["ref_id", "title", "year", "venue", "url", "source_type", "text"]
    rv = list(col.query(queries=Query("dense", vector=qe), topk=topk, output_fields=fields))
    try:
        rf = list(col.query(queries=Query("text", fts=Fts(query_string=keywords(qtext))),
                            topk=topk, output_fields=fields))
    except Exception:
        rf = []
    return rrf([rv, rf])


ENRICH_SYS = (
    "You enrich ONE concept of a Remote Sensing for Agricultural Statistics course using retrieved "
    "literature passages. You ground every claim in the passages, cite the passages you use by their "
    "number [n], select the 2-4 most relevant, write a concise bilingual 'deepen' layer that EXTENDS "
    "the Handbook definition (does not repeat it), and give a literature-alignment verdict. Output strict JSON only."
)


def enrich(concept: dict, passages: list) -> dict:
    blocks = []
    for i, d in enumerate(passages, 1):
        f = d.fields
        blocks.append(f"[{i}] {f.get('title','')[:140]} ({f.get('year') or 's.f.'}, {f.get('venue') or ''}) "
                      f"[{f.get('source_type')}] {f.get('url','')}\n    EXCERPT: {f.get('text','')[:700]}")
    from .llm.client import chat
    user = (f"CONCEPT: {concept['name']} ({concept['id']}).\nHANDBOOK DEFINITION (do not repeat, EXTEND it):\n"
            f"{concept['definition']}\n\nRETRIEVED PASSAGES:\n" + "\n\n".join(blocks) +
            "\n\nReturn JSON {\"deepen_en\":\"<=70 words extending the definition with literature, cite [n]\","
            "\"deepen_es\":\"<same Spanish>\","
            "\"references\":[{\"n\":<int>,\"why\":\"<6-word relevance>\"}],"  # the 2-4 chosen
            "\"alignment\":\"supported|partially_supported|underspecified|contradicts\","
            "\"alignment_note\":\"<1 short sentence>\"}")
    d = chat(ENRICH_SYS, user, json_mode=True, max_tokens=1500).json()
    chosen = []
    for r in d.get("references", []):
        n = r.get("n")
        if isinstance(n, int) and 1 <= n <= len(passages):
            f = passages[n - 1].fields
            chosen.append({"title": f.get("title"), "year": f.get("year"), "venue": f.get("venue"),
                           "url": f.get("url"), "doi": f.get("doi"), "source_type": f.get("source_type"),
                           "why": r.get("why", "")})
    return {"id": concept["id"], "deepen": {"en": d.get("deepen_en", ""), "es": d.get("deepen_es", "")},
            "references": chosen, "alignment": d.get("alignment", ""),
            "alignment_note": d.get("alignment_note", ""),
            "retrieved": [{"ref_id": p.fields.get("ref_id"), "title": p.fields.get("title"),
                           "source_type": p.fields.get("source_type")} for p in passages]}


def run_all(force: bool = False) -> Path:
    """Enrich ALL concepts: retrieve (sequential, fast) then DeepSeek rerank (threaded)."""
    from concurrent.futures import ThreadPoolExecutor
    out = build_dir() / "R_enrichment.json"
    ont = read_json(out_dir() / "ontology.json"); by_id = {n["id"]: n for n in ont["nodes"]}
    done = {}
    if out.exists() and not force:
        done = {r["id"]: r for r in read_json(out)["results"]}
    col = zvec.open(db_path())
    todo = [n for n in ont["nodes"] if n["id"] not in done]
    print(f"  {len(done)} done, retrieving passages for {len(todo)} concepts ...")
    jobs = []
    for k, n in enumerate(todo):
        q = f"{n['name']['en']}. {n['definition']['en']}"
        jobs.append((n, retrieve(col, q)))
        if (k + 1) % 50 == 0:
            print(f"    retrieved {k+1}/{len(todo)}", flush=True)

    def do(job):
        n, passages = job
        try:
            return enrich({"id": n["id"], "name": n["name"]["en"], "definition": n["definition"]["en"]}, passages)
        except Exception as e:  # noqa: BLE001
            print(f"    ! enrich {n['id']} failed: {str(e)[:50]}", flush=True)
            return None

    print(f"  enriching {len(jobs)} concepts (DeepSeek rerank, threaded) ...")
    with ThreadPoolExecutor(max_workers=6) as ex:
        new = [r for r in ex.map(do, jobs) if r]
    results = list(done.values()) + new
    write_json(out, {"results": results})
    aligned = {}
    for r in results:
        aligned[r["alignment"]] = aligned.get(r["alignment"], 0) + 1
    withref = sum(1 for r in results if r["references"])
    print(f"R full done: {len(results)} concepts, {withref} with references; alignment={aligned}")
    return out


def run(pilot=None) -> Path:
    ont = read_json(out_dir() / "ontology.json"); by_id = {n["id"]: n for n in ont["nodes"]}
    col = zvec.open(db_path())
    pilot = pilot or ["phenology", "area-estimation", "data-image", "ndvi", "random-forest",
                      "accuracy", "overall-accuracy"]
    results = []
    for cid in pilot:
        if cid not in by_id:
            continue
        n = by_id[cid]
        q = f"{n['name']['en']}. {n['definition']['en']}"
        passages = retrieve(col, q)
        r = enrich({"id": cid, "name": n["name"]["en"], "definition": n["definition"]["en"]}, passages)
        results.append(r)
        print(f"\n### {cid} — alignment={r['alignment']} ({len(r['references'])} refs)")
        print("  deepen EN:", r["deepen"]["en"][:160])
        for ref in r["references"]:
            print(f"   • [{ref.get('source_type')}] {ref.get('title','')[:70]} ({ref.get('year')}) {ref.get('url','')}")
    out = build_dir() / "R_pilot_enrichment.json"
    write_json(out, {"results": results})
    print(f"\nPhase R pilot done -> {out}")
    return out


if __name__ == "__main__":
    import sys
    run_all(force="--force" in sys.argv)
