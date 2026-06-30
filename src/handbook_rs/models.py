"""Pydantic models = the ontology contract shared by every stage."""

from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, Field


class Bi(BaseModel):
    """A bilingual string pair (English / Spanish)."""
    en: str = ""
    es: str = ""


class BiList(BaseModel):
    en: list[str] = Field(default_factory=list)
    es: list[str] = Field(default_factory=list)


class Citation(BaseModel):
    chapter_id: str
    chapter_title: str = ""
    anchor: str = ""           # e.g. "#sec-vegetation-indices" ("" if whole page)
    url: str = ""


class Zipf(BaseModel):
    corpus_rank: Optional[int] = None
    corpus_freq: float = 0.0
    in_backbone: bool = False


class Provenance(BaseModel):
    created_in: Literal["backbone", "closure", "closure-inferred"] = "backbone"
    merged_from: list[str] = Field(default_factory=list)
    definition_call_id: str = ""
    translation_call_id: str = ""


# Coarse category used to forbid nonsensical merges (a metric is never a sensor).
# Kept as a free string (the model occasionally coins reasonable extras like
# "index"/"product"); known values are enumerated for documentation/merge rules.
Category = str
KNOWN_CATEGORIES = {
    "method", "metric", "data", "sensor", "platform", "phenomenon", "statistic",
    "software", "organization", "index", "product", "primitive", "other",
}


class Node(BaseModel):
    id: str                         # language-neutral slug, e.g. "ndvi"
    kind: Literal["concept", "primitive"] = "concept"
    name: Bi = Field(default_factory=Bi)
    aliases: BiList = Field(default_factory=BiList)
    definition: Bi = Field(default_factory=Bi)
    category: Category = "other"
    level: int = 0                  # longest-path prereq depth (basic -> advanced)
    topo_order: int = 0
    closure_depth: int = 0          # distance from a backbone seed
    zipf: Zipf = Field(default_factory=Zipf)
    citations: list[Citation] = Field(default_factory=list)
    definition_terms: list[str] = Field(default_factory=list)  # normalized terms in def
    provenance: Provenance = Field(default_factory=Provenance)


EdgeRel = Literal["prereq", "defines_uses", "see_also"]


class Edge(BaseModel):
    src: str
    dst: str
    rel: EdgeRel
    weight: float = 1.0


class Meta(BaseModel):
    schema_version: str = "1.0"
    source_book: str = ""
    generated_at: str = ""
    model: str = ""
    stats: dict = Field(default_factory=dict)


class Dropped(BaseModel):
    term: str
    reason: str                     # node_cap | max_depth | primitive | ...
    discovered_under: str = ""
    zipf_rank: Optional[int] = None


class Ontology(BaseModel):
    meta: Meta = Field(default_factory=Meta)
    nodes: list[Node] = Field(default_factory=list)
    edges: list[Edge] = Field(default_factory=list)
    primitive_ledger: list[str] = Field(default_factory=list)
    dropped: list[Dropped] = Field(default_factory=list)

    # ---- convenience ----
    def by_id(self) -> dict[str, Node]:
        return {n.id: n for n in self.nodes}
