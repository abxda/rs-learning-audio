"""Stage 3 — merge the Zipf backbone terms into canonical concepts.

Canonicalization runs in batches (bounded reasoning per call), then a cross-batch
merge unifies concepts that name the same idea (exact normalized name or high fuzzy
match). Output: build/05_concepts.json — the seed concept set for definitions.
"""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from rapidfuzz import fuzz

from .config import build_dir, get_config
from .io_utils import read_json, write_json
from .llm import prompts
from .llm.client import chat
from .norms import normalize, slugify


def _terms_block(backbone: list[dict], idxs: list[int]) -> str:
    return "\n".join(f"{i} | {backbone[i]['surface']} | {backbone[i]['freq']} | "
                     f"{backbone[i]['doc_freq']}" for i in idxs)


def _canon_batch(backbone: list[dict], idxs: list[int]) -> list[dict]:
    user = prompts.canonicalize(_terms_block(backbone, idxs))
    res = chat(prompts.CANON_SYS, user, json_mode=True, max_tokens=8000)
    return res.json().get("concepts", [])


def _merge_concepts(raw: list[dict], backbone: list[dict]) -> list[dict]:
    """Union concepts sharing a normalized name or fuzzy>=95; assign global ids."""
    merged: list[dict] = []
    norm_to_idx: dict[str, int] = {}
    used_ids: set[str] = set()
    absorbed: set[int] = set()

    def attach(target: dict, c: dict, idxs: list[int]) -> None:
        target["aliases"].update(a.strip() for a in c.get("aliases", []) if a.strip())
        for i in idxs:
            target["aliases"].add(backbone[i]["surface"])
            target["_idxs"].add(i)

    for c in raw:
        name = (c.get("name") or "").strip()
        if not name:
            continue
        idxs = [i for i in c.get("absorbs", []) if isinstance(i, int) and 0 <= i < len(backbone)
                and i not in absorbed]
        absorbed.update(idxs)
        nn = normalize(name)
        hit = norm_to_idx.get(nn)
        if hit is None:
            # fuzzy against existing names
            for ex_nn, j in norm_to_idx.items():
                if fuzz.token_sort_ratio(nn, ex_nn) >= 95:
                    hit = j
                    break
        if hit is not None:
            attach(merged[hit], c, idxs)
        else:
            cid = slugify(c.get("id") or name) or "concept"
            base, n = cid, 2
            while cid in used_ids:
                cid, n = f"{base}-{n}", n + 1
            used_ids.add(cid)
            entry = {"id": cid, "name": name, "category": c.get("category", "other"),
                     "aliases": set(), "_idxs": set()}
            attach(entry, c, idxs)
            norm_to_idx[nn] = len(merged)
            merged.append(entry)

    # singletons for any backbone term no concept absorbed (no silent loss)
    for i in range(len(backbone)):
        if i not in absorbed:
            t = backbone[i]
            cid = (t.get("slug") or slugify(t["surface"])) or "term"
            base, n = cid, 2
            while cid in used_ids:
                cid, n = f"{base}-{n}", n + 1
            used_ids.add(cid)
            merged.append({"id": cid, "name": t["surface"], "category": "other",
                           "aliases": {t["surface"]}, "_idxs": {i}})
    return merged


def run(force: bool = False) -> Path:
    out = build_dir() / "05_concepts.json"
    if out.exists() and not force:
        print("Stage 3 cached.")
        return out

    cfg = get_config()["mining"]
    bb = read_json(build_dir() / "04_backbone.json")["terms"]
    bs = cfg["canon_batch"]
    batches = [list(range(i, min(i + bs, len(bb)))) for i in range(0, len(bb), bs)]
    print(f"  canonicalizing {len(bb)} terms in {len(batches)} batches ...")
    with ThreadPoolExecutor(max_workers=4) as ex:
        chunk_results = list(ex.map(lambda idxs: _canon_batch(bb, idxs), batches))
    raw = [c for chunk in chunk_results for c in chunk]
    print(f"  {len(raw)} raw concepts across batches -> merging ...")

    merged = _merge_concepts(raw, bb)
    concepts = []
    for m in merged:
        idxs = sorted(m["_idxs"])
        members = [bb[i] for i in idxs]
        concepts.append({
            "id": m["id"],
            "name_en": m["name"],
            "category": m["category"],
            "aliases_en": sorted(m["aliases"]),
            "absorbs": [bb[i]["surface"] for i in idxs],
            "zipf": {
                "corpus_rank": min((bb[i]["rank"] for i in idxs), default=None),
                "corpus_freq": sum(bb[i]["freq"] for i in idxs),
                "doc_freq": max((bb[i]["doc_freq"] for i in idxs), default=0),
                "in_backbone": True,
            },
            "provenance": {"created_in": "backbone"},
        })

    write_json(out, {"count": len(concepts), "concepts": concepts})
    cats: dict[str, int] = {}
    for c in concepts:
        cats[c["category"]] = cats.get(c["category"], 0) + 1
    print(f"Stage 3 done: {len(concepts)} canonical concepts -> {out}")
    print("  categories:", dict(sorted(cats.items(), key=lambda x: -x[1])))
    return out


if __name__ == "__main__":
    run()
