"""Phase V — embed the corpus chunks with BAAI/bge-m3 and build a local Zvec
hybrid index (dense vector + native FTS + scalar fields)."""

from __future__ import annotations

from pathlib import Path

import httpx
import numpy as np
import zvec
from zvec import (CollectionSchema, DataType, Doc, FieldSchema, FtsIndexParam,
                  HnswIndexParam, MetricType, VectorSchema)

from .config import build_dir
from .io_utils import read_json

DB = "zvec_refs"
EMB = "bge-m3"              # served by Ollama (GPU), 1024-dim dense
DIM = 1024
OLLAMA = "http://localhost:11434/api/embed"


def embed_texts(texts: list[str], batch: int = 8) -> np.ndarray:
    """Embed with bge-m3 via Ollama (GPU). Bulletproof: batch -> per-item with
    decreasing truncation -> zero vector, so one bad chunk never kills the run."""
    out: list = []
    bad = 0
    with httpx.Client(timeout=300) as c:
        def emb_one(t: str):
            nonlocal bad
            for trunc in (2000, 1000, 400, 120):
                try:
                    r = c.post(OLLAMA, json={"model": EMB, "input": t[:trunc] or "."})
                    r.raise_for_status()
                    return r.json()["embeddings"][0]
                except Exception:
                    continue
            bad += 1
            return [0.0] * DIM
        for i in range(0, len(texts), batch):
            chunk = [t[:2000] for t in texts[i:i + batch]]
            try:
                r = c.post(OLLAMA, json={"model": EMB, "input": chunk})
                r.raise_for_status()
                out.extend(r.json()["embeddings"])
            except Exception:
                out.extend(emb_one(t) for t in texts[i:i + batch])
            if (i // batch) % 15 == 0:
                print(f"    embedded {min(i+batch, len(texts))}/{len(texts)} (bad={bad})", flush=True)
    return np.asarray(out, dtype=np.float32)


def db_path() -> str:
    return str(build_dir() / DB)


def run(force: bool = False) -> str:
    import shutil
    chunks = read_json(build_dir() / "E_chunks.json")["chunks"]
    print(f"  embedding {len(chunks)} chunks with {EMB} (Ollama) ...")
    embs = embed_texts([c["text"] for c in chunks])
    embs = embs / (np.linalg.norm(embs, axis=1, keepdims=True) + 1e-9)

    p = db_path()
    if force:
        shutil.rmtree(p, ignore_errors=True)
    schema = CollectionSchema(
        name="references",
        vectors=[VectorSchema("dense", DataType.VECTOR_FP32, dimension=DIM,
                              index_param=HnswIndexParam(metric_type=MetricType.COSINE))],
        fields=[
            FieldSchema("text", DataType.STRING,
                        index_param=FtsIndexParam(tokenizer_name="standard", filters=["lowercase"])),
            FieldSchema("ref_id", DataType.STRING),
            FieldSchema("title", DataType.STRING, nullable=True),
            FieldSchema("year", DataType.INT32, nullable=True),
            FieldSchema("venue", DataType.STRING, nullable=True),
            FieldSchema("doi", DataType.STRING, nullable=True),
            FieldSchema("url", DataType.STRING, nullable=True),
            FieldSchema("source_type", DataType.STRING, nullable=True),
        ])
    col = zvec.create_and_open(path=p, schema=schema)

    docs = []
    for i, c in enumerate(chunks):
        docs.append(Doc(id=f"{c['ref_id']}__{c['chunk']}", vectors={"dense": embs[i].tolist()},
                        fields={"text": c["text"][:8000], "ref_id": c["ref_id"],
                                "title": c.get("title") or "", "year": c.get("year"),
                                "venue": c.get("venue") or "", "doi": c.get("doi") or "",
                                "url": c.get("url") or "", "source_type": c.get("source_type") or ""}))
        if len(docs) >= 500:
            col.insert(docs); docs = []
    if docs:
        col.insert(docs)
    col.flush()
    print(f"Phase V done: Zvec index at {p} ({len(chunks)} chunks indexed)")
    return p


if __name__ == "__main__":
    run(force=True)
