"""Stage 2 — statistical term mining (the Zipf-driven backbone selector).

Pipeline:
  1. spaCy noun-chunk + noun candidates over the prose of all 37 pages.
  2. Three salience signals, each normalized to [0,1]:
       - zipf    : in-corpus frequency (the Zipf driver)
       - cvalue  : nested multiword technical-term salience
       - keybert : embedding centrality to the whole-corpus centroid
  3. Blend by config weights -> ranked candidate list (build/03_terms.json).
  4. Take the top `backbone_size` as the broad backbone (build/04_backbone.json).

No LLM here: this stage is deterministic and reproducible.
"""

from __future__ import annotations

import math
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

from .config import build_dir, get_config
from .io_utils import read_json, write_json
from .norms import normalize, slugify
from .pages import PAGES
from .stage1_clean import md_dir

_NLP = None


def nlp():
    global _NLP
    if _NLP is None:
        import spacy
        _NLP = spacy.load("en_core_web_md", disable=["ner"])
        _NLP.max_length = 2_000_000
    return _NLP


def _candidates_from_doc(doc, min_len: int, max_len: int):
    """Yield (normalized_term, surface_form, n_tokens) from noun chunks + nouns."""
    for chunk in doc.noun_chunks:
        toks = [t for t in chunk
                if t.is_alpha and not t.is_stop and len(t) >= 2 and t.pos_ in {"NOUN", "PROPN", "ADJ"}]
        # trim trailing adjectives so "vegetation index normalized" doesn't survive oddly
        while toks and toks[-1].pos_ == "ADJ":
            toks = toks[:-1]
        if not (min_len <= len(toks) <= max_len):
            continue
        lemmas = [t.lemma_.lower() for t in toks]
        term = normalize(" ".join(lemmas))
        surface = " ".join(t.text for t in toks)
        if term and not term.isdigit():
            yield term, surface, len(lemmas)
    # standalone nouns (unigrams) to ensure single-word concepts are candidates
    for t in doc:
        if t.is_alpha and not t.is_stop and len(t) >= 3 and t.pos_ in {"NOUN", "PROPN"}:
            term = normalize(t.lemma_.lower())
            if term:
                yield term, t.text, 1


def _minmax(d: dict[str, float]) -> dict[str, float]:
    if not d:
        return {}
    vals = list(d.values())
    lo, hi = min(vals), max(vals)
    if hi - lo < 1e-12:
        return {k: 0.0 for k in d}
    return {k: (v - lo) / (hi - lo) for k, v in d.items()}


def _cvalue(freq: dict[str, int], nwords: dict[str, int]) -> dict[str, float]:
    """Pragmatic C-value: length-weighted frequency discounted by longer terms
    that nest the candidate. Unigrams get length weight log2(2)=1 so they stay in play."""
    terms = list(freq)
    # map: term -> longer terms that contain it as a whitespace-bounded substring
    longer = defaultdict(list)
    by_len = defaultdict(list)
    for t in terms:
        by_len[nwords[t]].append(t)
    maxlen = max(nwords.values())
    for n in range(1, maxlen):
        shorts = by_len.get(n, [])
        if not shorts:
            continue
        longs = [t for L in range(n + 1, maxlen + 1) for t in by_len.get(L, [])]
        for s in shorts:
            pat = f" {s} "
            for lng in longs:
                if pat in f" {lng} ":
                    longer[s].append(lng)
    cval = {}
    for t in terms:
        lw = math.log2(nwords[t] + 1)
        nested = longer.get(t, [])
        if nested:
            disc = sum(freq[b] for b in nested) / len(nested)
            cval[t] = lw * (freq[t] - disc)
        else:
            cval[t] = lw * freq[t]
        cval[t] = max(cval[t], 0.0)
    return cval


def _embedding_centrality(terms: list[str], chunks: list[str], model_name: str) -> dict[str, float]:
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer(model_name)
    chunk_emb = model.encode(chunks, normalize_embeddings=True, batch_size=64,
                             show_progress_bar=False)
    centroid = np.asarray(chunk_emb).mean(axis=0)
    centroid /= (np.linalg.norm(centroid) + 1e-12)
    term_emb = model.encode(terms, normalize_embeddings=True, batch_size=128,
                            show_progress_bar=False)
    sims = np.asarray(term_emb) @ centroid          # cosine, terms already normalized
    return {t: float(max(s, 0.0)) for t, s in zip(terms, sims)}


def run(force: bool = False) -> Path:
    cfg = get_config()["mining"]
    out = build_dir() / "03_terms.json"
    bb_out = build_dir() / "04_backbone.json"
    if out.exists() and bb_out.exists() and not force:
        print("Stage 2 cached.")
        return out

    # --- load prose; build per-chapter docs for document frequency + chunks for embedding
    docs_text: dict[str, str] = {}
    chunks: list[str] = []
    for pg in PAGES:
        rec = read_json(md_dir() / f"{pg.chapter_id}.json")
        docs_text[pg.chapter_id] = rec["prose"]
        if rec.get("sections"):
            chunks.extend(s["prose"] for s in rec["sections"] if len(s["prose"]) > 80)
        else:
            words = rec["prose"].split()
            chunks.extend(" ".join(words[i:i + 200]) for i in range(0, len(words), 200))

    print(f"  spaCy parsing {len(docs_text)} docs ...")
    freq: Counter = Counter()
    nwords: dict[str, int] = {}
    docfreq: defaultdict = defaultdict(set)
    surface_counts: defaultdict = defaultdict(Counter)
    examples: dict[str, str] = {}
    pipe = nlp().pipe(docs_text.values(), batch_size=4)
    for cid, doc in zip(docs_text.keys(), pipe):
        for term, surface, n in _candidates_from_doc(doc, cfg["min_term_len"], cfg["max_term_len"]):
            freq[term] += 1
            nwords[term] = n
            docfreq[term].add(cid)
            surface_counts[term][surface] += 1
            examples.setdefault(term, surface)

    # --- filter by min frequency
    minf = cfg["min_freq"]
    terms = [t for t, c in freq.items() if c >= minf and len(t) >= 3]
    print(f"  {len(freq):,} raw candidates -> {len(terms):,} after freq>={minf}")

    # --- three signals
    zipf_score = {t: float(freq[t]) for t in terms}
    cvalue_score = {t: v for t, v in _cvalue({t: freq[t] for t in terms},
                                             {t: nwords[t] for t in terms}).items()}
    print("  embedding centrality ...")
    keybert_score = _embedding_centrality(terms, chunks, cfg["embed_model"])

    z = _minmax(zipf_score)
    c = _minmax(cvalue_score)
    k = _minmax({t: keybert_score.get(t, 0.0) for t in terms})
    w = cfg["weights"]
    blended = {t: w["zipf"] * z[t] + w["cvalue"] * c[t] + w["keybert"] * k[t] for t in terms}

    ranked = sorted(terms, key=lambda t: blended[t], reverse=True)
    records = []
    for rank, t in enumerate(ranked, 1):
        best_surface = surface_counts[t].most_common(1)[0][0]
        records.append({
            "term": t,
            "surface": best_surface,
            "rank": rank,
            "freq": freq[t],
            "doc_freq": len(docfreq[t]),
            "n_words": nwords[t],
            "score": round(blended[t], 5),
            "zipf": round(z[t], 4),
            "cvalue": round(c[t], 4),
            "keybert": round(k[t], 4),
        })
    write_json(out, {"count": len(records), "terms": records})

    # --- backbone = top N, with a slug each
    backbone = []
    for r in records[: cfg["backbone_size"]]:
        backbone.append({**r, "slug": slugify(r["surface"])})
    write_json(bb_out, {"backbone_size": len(backbone), "terms": backbone})
    print(f"Stage 2 done: {len(records):,} ranked terms; backbone={len(backbone)}")
    print("  top 25:", ", ".join(r["surface"] for r in records[:25]))
    return out


if __name__ == "__main__":
    run()
