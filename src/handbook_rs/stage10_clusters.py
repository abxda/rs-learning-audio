"""Stage 10 — group concepts into learning THEMES for the homepage.

Embeds every concept with Ollama `embeddinggemma`, selects the best clustering
(KMeans vs Agglomerative, k chosen by silhouette), names each theme with DeepSeek
(bilingual title + description), and computes 2D PCA coordinates for the minimap.

Output: build/10_clusters.json  (read by stage9 to build the cover/menu + minimap).
"""

from __future__ import annotations

import json
from pathlib import Path

import httpx
import numpy as np
from sklearn.cluster import AgglomerativeClustering, KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score

from .config import build_dir, out_dir
from .io_utils import read_json, write_json
from .llm import prompts
from .llm.client import chat

OLLAMA = "http://localhost:11434/api/embed"
EMB_MODEL = "embeddinggemma:latest"
PALETTE = ["#2e7d32", "#1565c0", "#c62828", "#6a1b9a", "#ef6c00", "#00838f",
           "#ad1457", "#558b2f", "#4527a0", "#d84315", "#00695c", "#5d4037",
           "#9e9d24", "#283593", "#37474f"]


def embed(texts: list[str]) -> np.ndarray:
    vecs: list = []
    with httpx.Client(timeout=180) as c:
        for i in range(0, len(texts), 32):
            r = c.post(OLLAMA, json={"model": EMB_MODEL, "input": texts[i:i + 32]})
            r.raise_for_status()
            vecs.extend(r.json()["embeddings"])
            print(f"  embedded {min(i+32, len(texts))}/{len(texts)}", flush=True)
    return np.asarray(vecs, dtype=np.float32)


def best_clustering(Xn: np.ndarray) -> tuple:
    best = None
    for k in range(7, 15):
        for name, model in (("kmeans", KMeans(k, n_init=10, random_state=0)),
                            ("agglomerative", AgglomerativeClustering(k))):
            labels = model.fit_predict(Xn)
            s = silhouette_score(Xn, labels, metric="cosine")
            print(f"  {name} k={k}: silhouette={s:.3f}", flush=True)
            if best is None or s > best[0]:
                best = (s, name, k, labels)
    return best


def name_clusters(blocks: str) -> dict:
    res = chat(prompts.CLUSTER_SYS, prompts.name_clusters(blocks), json_mode=True, max_tokens=4000)
    return {c["idx"]: c for c in res.json().get("clusters", []) if "idx" in c}


def run(force: bool = False) -> Path:
    out = build_dir() / "10_clusters.json"
    if out.exists() and not force:
        print("Stage 10 cached.")
        return out

    ont = read_json(out_dir() / "ontology.json")
    nodes = ont["nodes"]
    by_id = {n["id"]: n for n in nodes}
    texts = [f"{n['name']['en']}. {n['definition']['en']}" for n in nodes]
    print(f"  embedding {len(texts)} concepts with {EMB_MODEL} ...")
    X = embed(texts)
    Xn = X / (np.linalg.norm(X, axis=1, keepdims=True) + 1e-9)

    sil, method, k, labels = best_clustering(Xn)
    print(f"  best: {method} k={k} silhouette={sil:.3f}")

    xy = PCA(2, random_state=0).fit_transform(Xn)
    xy = (xy - xy.min(0)) / (xy.max(0) - xy.min(0) + 1e-9)

    groups: dict[int, list[int]] = {}
    for i in range(len(nodes)):
        groups.setdefault(int(labels[i]), []).append(i)

    # representatives (closest to centroid) + a natural entry (most basic member)
    clusters = []
    name_blocks = []
    for ci, idxs in sorted(groups.items()):
        centroid = Xn[idxs].mean(0)
        order = sorted(idxs, key=lambda i: -float(Xn[i] @ centroid))
        reps = [nodes[i]["id"] for i in order[:6]]
        members = [nodes[i]["id"] for i in idxs]
        entry = min(members, key=lambda mid: (by_id[mid]["level"], by_id[mid].get("topo_order", 0)))
        clusters.append({
            "idx": ci, "members": members, "reps": reps, "size": len(idxs),
            "entry": entry, "color": PALETTE[ci % len(PALETTE)],
            "cx": round(float(xy[idxs, 0].mean()), 4), "cy": round(float(xy[idxs, 1].mean()), 4),
        })
        rep_txt = "; ".join(f"{by_id[r]['name']['en']}" for r in reps)
        name_blocks.append(f"{ci} | {rep_txt}")

    print("  naming themes with DeepSeek ...")
    names = name_clusters("\n".join(name_blocks))
    for c in clusters:
        nm = names.get(c["idx"], {})
        c["title"] = {"en": nm.get("title_en", f"Theme {c['idx']+1}"),
                      "es": nm.get("title_es", f"Tema {c['idx']+1}")}
        c["desc"] = {"en": nm.get("desc_en", ""), "es": nm.get("desc_es", "")}

    node_xy = {nodes[i]["id"]: [round(float(xy[i, 0]), 4), round(float(xy[i, 1]), 4)]
               for i in range(len(nodes))}
    node_cluster = {nodes[i]["id"]: int(labels[i]) for i in range(len(nodes))}

    write_json(out, {"method": method, "k": k, "silhouette": round(float(sil), 3),
                     "clusters": clusters, "node_xy": node_xy, "node_cluster": node_cluster})
    print(f"Stage 10 done: {k} themes ({method}, silhouette {sil:.3f}) -> {out}")
    for c in clusters:
        print(f"  [{c['idx']}] {c['title']['en']} ({c['size']}) — {c['desc']['en'][:60]}")
    return out


if __name__ == "__main__":
    run()
