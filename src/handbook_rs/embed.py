"""Lazy sentence-embedding index over node names, for semantic merge matching."""

from __future__ import annotations

import numpy as np

from .config import get_config

_MODEL = None


def model():
    global _MODEL
    if _MODEL is None:
        from sentence_transformers import SentenceTransformer
        _MODEL = SentenceTransformer(get_config()["mining"]["embed_model"])
    return _MODEL


class NodeIndex:
    """Embeds one vector per node (its English name) and supports batched argmax."""

    def __init__(self) -> None:
        self.ids: list[str] = []
        self.mat: np.ndarray | None = None

    def build(self, nodes: dict[str, dict]) -> None:
        self.ids = list(nodes)
        texts = [nodes[i]["name_en"] for i in self.ids]
        self.mat = np.asarray(model().encode(texts, normalize_embeddings=True,
                                             batch_size=128, show_progress_bar=False))

    def query_batch(self, terms: list[str]) -> list[tuple[str, float]]:
        if not terms or self.mat is None or not self.ids:
            return [("", 0.0) for _ in terms]
        q = np.asarray(model().encode(terms, normalize_embeddings=True,
                                      batch_size=128, show_progress_bar=False))
        sims = q @ self.mat.T            # (n_terms, n_nodes)
        best = sims.argmax(axis=1)
        return [(self.ids[j], float(sims[r, j])) for r, j in enumerate(best)]
