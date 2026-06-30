"""In-memory node store for the define+closure stage.

Holds concept and primitive nodes plus the alias index that maps any normalized
surface form to a node id. Primitives ARE nodes (kind="primitive") so that every
term referenced in a definition resolves to a real node => the corpus is closed and
every [[link]] in the vault has a target.
"""

from __future__ import annotations

from .norms import normalize


class NodeStore:
    def __init__(self) -> None:
        self.nodes: dict[str, dict] = {}
        self.alias_norm: dict[str, str] = {}     # normalized surface -> node id
        self.ledger: set[str] = set()            # normalized forms that are primitives
        self.classified: set[str] = set()        # every term ever triaged (monotonic frontier)
        self.dropped: list[dict] = []

    # ---- registration ----
    def _register(self, node_id: str, surfaces: list[str]) -> None:
        for s in surfaces:
            n = normalize(s)
            if n and n not in self.alias_norm:
                self.alias_norm[n] = node_id

    def add_concept(self, rec: dict, depth: int) -> str:
        cid = rec["id"]
        node = {
            "id": cid,
            "kind": "concept",
            "name_en": rec["name_en"],
            "category": rec.get("category", "other"),
            "aliases_en": sorted(set(rec.get("aliases_en", []))),
            "definition_en": "",
            "citations": [],
            "definition_terms": [],     # normalized key terms used in the definition
            "def_uses": [],             # resolved node ids (defines_uses targets)
            "closure_depth": depth,
            "zipf": rec.get("zipf", {"in_backbone": False, "corpus_freq": 0,
                                     "corpus_rank": None, "doc_freq": 0}),
            "provenance": rec.get("provenance", {"created_in": "backbone"}),
        }
        self.nodes[cid] = node
        self._register(cid, [rec["name_en"], *node["aliases_en"], *rec.get("absorbs", [])])
        return cid

    def add_alias(self, node_id: str, surface: str) -> None:
        """Record `surface` as a way to refer to node_id (keeps closure verifiable
        and lets the vault link the exact definition wording to its node)."""
        n = normalize(surface)
        if not n or node_id not in self.nodes:
            return
        self.alias_norm.setdefault(n, node_id)
        node = self.nodes[node_id]
        if surface not in node["aliases_en"] and surface.strip():
            node["aliases_en"].append(surface.strip())

    def add_primitive(self, name_en: str, gloss_en: str, depth: int,
                      discovered_under: str = "", reason: str = "") -> str:
        from .norms import slugify
        base = slugify(name_en) or "term"
        cid = base
        n = 2
        while cid in self.nodes:
            cid, n = f"{base}-{n}", n + 1
        node = {
            "id": cid, "kind": "primitive", "name_en": name_en, "category": "primitive",
            "aliases_en": [], "definition_en": gloss_en, "citations": [],
            "definition_terms": [], "def_uses": [], "closure_depth": depth,
            "zipf": {"in_backbone": False, "corpus_freq": 0, "corpus_rank": None, "doc_freq": 0},
            "provenance": {"created_in": "closure"},
        }
        self.nodes[cid] = node
        self.ledger.add(normalize(name_en))
        self._register(cid, [name_en])
        if reason:
            self.dropped.append({"term": name_en, "reason": reason,
                                 "discovered_under": discovered_under, "zipf_rank": None})
        return cid

    # ---- lookup ----
    def resolve(self, term: str) -> str | None:
        return self.alias_norm.get(normalize(term))

    def undefined_concept_ids(self) -> list[str]:
        return [i for i, n in self.nodes.items()
                if n["kind"] == "concept" and not n["definition_en"]]

    def n_concepts(self) -> int:
        return sum(1 for n in self.nodes.values() if n["kind"] == "concept")
