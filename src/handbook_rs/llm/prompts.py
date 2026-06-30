"""Versioned prompt templates. Each returns (system, user). All require strict
JSON output. The corpus is injected by callers as a cached prefix where needed.

PROMPT_VERSION bumps invalidate the LLM cache for prompts (it is part of payload
only indirectly via text, so changing wording already changes cache keys)."""

from __future__ import annotations

PROMPT_VERSION = "v1"

# --------------------------------------------------------------------------- #
# Stage 3 — canonicalize backbone terms into concepts
# --------------------------------------------------------------------------- #
CANON_SYS = (
    "You are an ontology engineer building a closed, navigable concept tree for the "
    "UN Handbook on Remote Sensing for Agricultural Statistics. You merge surface "
    "term variants (plurals, acronyms, synonyms, spelling) into single canonical "
    "concepts grounded ONLY in the handbook. You never invent concepts absent from "
    "the supplied term list. You output strict JSON and nothing else."
)


def canonicalize(terms_block: str) -> str:
    return f"""From the indexed candidate terms below (mined from the handbook by frequency),
produce the canonical CONCEPTS. Rules:
- Merge variants/synonyms/acronyms of the SAME idea into ONE concept (e.g. "rf",
  "random forests", "random forest" -> one). Keep genuinely distinct ideas separate
  (e.g. "training set" vs "validation set" are DIFFERENT).
- NAME each concept with its CONVENTIONAL, specific term, not a bare stem. Prefer
  "machine learning" over "learning", "remote sensing" over "sensing", "time series"
  over "series", "random forest" over "forest". Only use a single word when that word
  truly is the standard concept name (e.g. "pixel", "accuracy", "yield").
- Do NOT merge an object with a PROPERTY or METRIC of it: "model" and "model accuracy"
  are different; "map" and "map accuracy" are different; a method and its output differ.
- Every input term index MUST be absorbed by exactly one concept (use "absorbs").
  Absorb a generic stem (e.g. "classification") into its specific concept only if they
  denote the same idea; otherwise give the generic term its own concept.
- If a term is everyday/general vocabulary not specific to the domain (e.g. "data",
  "result", "approach", "chapter", "number"), still absorb it but set
  "category":"primitive".
- Give each concept a stable lowercase-hyphen "id" (English, derived from the chosen
  name), a clean English "name", and a "category" from: method, metric, data, sensor,
  platform, phenomenon, statistic, software, organization, index, product, primitive,
  other.

Return JSON: {{"concepts":[{{"id","name","category","aliases":[..],
"absorbs":[term_index,..]}}]}}

CANDIDATE TERMS (index | surface | freq | doc_freq):
{terms_block}
"""


# --------------------------------------------------------------------------- #
# Stage 4 — grounded definitions (corpus injected as prefix)
# --------------------------------------------------------------------------- #
DEFINE_SYS = (
    "You are a technical lexicographer. Using ONLY the handbook corpus provided, "
    "write precise, self-contained English definitions for the requested concepts. "
    "Ground every definition in the corpus and cite the chapter (and a section "
    "anchor when one fits). A definition must read clearly to a learner and should "
    "introduce as few NEW technical terms as possible. Output strict JSON only."
)


def define_batch(concepts_block: str, anchors_block: str, max_words: int, max_new: int) -> str:
    return f"""Write a definition for each concept id below. Constraints per definition:
- <= {max_words} words, plain and precise, true to the corpus.
- Introduce at most {max_new} NEW technical terms beyond common vocabulary; if a
  concept needs more, it is too broad — define it at the right altitude.
- "citations": 1-3 entries from the VALID CITATION TARGETS only. Use the exact
  chapter_id; use an anchor from that chapter when one matches, else "".
- "key_terms": list the technical terms you USED in the definition that themselves
  deserve their own concept entry (these drive closure). Lowercase noun phrases.

Return JSON: {{"definitions":[{{"id","definition_en","citations":[{{"chapter_id","anchor"}}],"key_terms":[..]}}]}}

VALID CITATION TARGETS (chapter_id :: anchors):
{anchors_block}

CONCEPTS TO DEFINE (id | name | category):
{concepts_block}
"""


# --------------------------------------------------------------------------- #
# Stage 4 closure — adjudicate ambiguous merges
# --------------------------------------------------------------------------- #
ADJ_SYS = (
    "You decide whether two technical terms denote the SAME concept in the context "
    "of remote sensing for agricultural statistics. Be conservative: if they play "
    "different roles, keep them separate. Output strict JSON only."
)


def adjudicate(pairs_block: str) -> str:
    return f"""For each pair, decide if term A and the existing concept B are the same concept.
Return JSON: {{"verdicts":[{{"i",[index],"same":true/false,"distinction":"... if different"}}]}}
Pairs (i | term A | concept B name | B definition):
{pairs_block}
"""


# --------------------------------------------------------------------------- #
# Stage 4 closure — classify a frontier term: new concept vs primitive
# --------------------------------------------------------------------------- #
CLASSIFY_SYS = (
    "You triage terms found inside definitions. A term is a CONCEPT if it carries "
    "domain meaning worth its own entry; it is a PRIMITIVE if it is everyday or "
    "very general vocabulary needing only a one-line gloss. Output strict JSON only."
)


def classify_terms(terms_block: str) -> str:
    return f"""Classify each term as "concept" or "primitive" for a closed knowledge tree about
remote sensing for agricultural statistics. A CONCEPT carries specific domain meaning
worth its own entry; a PRIMITIVE is everyday/general vocabulary needing only a gloss.
For every item give a clean English "name", a "category" (method, metric, data,
sensor, platform, phenomenon, statistic, software, organization, index, product,
primitive, other), and ALWAYS a <=20-word plain English "gloss".

Return JSON: {{"items":[{{"term","decision":"concept|primitive","name","category","gloss"}}]}}

TERMS:
{terms_block}
"""


# --------------------------------------------------------------------------- #
# Stage 4 closure — define newly discovered concepts (corpus injected as prefix)
# --------------------------------------------------------------------------- #
def define_new(concepts_block: str, anchors_block: str, max_words: int, max_new: int) -> str:
    return f"""These concepts were discovered while closing definitions. Define each one.
If the corpus covers it, ground and cite it. If the corpus does NOT really cover it
(it is general scientific vocabulary), write a correct general definition and set
citations to [] — do not invent a chapter. Same JSON shape and constraints as before
(<= {max_words} words, <= {max_new} new terms, include "key_terms").

Return JSON: {{"definitions":[{{"id","definition_en","grounded":true/false,"citations":[{{"chapter_id","anchor"}}],"key_terms":[..]}}]}}

VALID CITATION TARGETS:
{anchors_block}

CONCEPTS TO DEFINE (id | name | category):
{concepts_block}
"""


# --------------------------------------------------------------------------- #
# Stage 5b — prerequisite lineage + knowledge-building bridges
# --------------------------------------------------------------------------- #
LINEAGE_SYS = (
    "You are a curriculum designer building a LEARNING DAG (prerequisite graph) for a "
    "closed knowledge corpus on remote sensing for agricultural statistics. For each "
    "concept you choose the more-basic concepts a learner must understand immediately "
    "before it, and you write a knowledge-building sentence that constructs the concept "
    "from each prerequisite. Output strict JSON only."
)


def lineage(catalog_block: str, concepts_block: str) -> str:
    return f"""For each TARGET concept choose its DIRECT prerequisites: the 1-4 more basic
concepts from the CATALOG that a learner must understand IMMEDIATELY before it (its parents
in a learning DAG — not the whole ancestry, not advanced concepts). Rules:
- Use ONLY ids that appear in the CATALOG. Never invent ids.
- A prerequisite must be MORE BASIC than the target (you would teach it earlier).
- For each prerequisite write ONE "bridge" sentence (<=28 words) that builds the target FROM
  the prerequisite — a real knowledge-construction phrase, e.g. "A random forest extends the
  decision tree by training many of them on random subsets and averaging their votes, which
  reduces overfitting." Do not just say "is related to".
- If a concept is genuinely foundational (no prerequisite inside this corpus), return [].

Return JSON: {{"items":[{{"id","prereqs":[{{"id","bridge"}}]}}]}}

CATALOG (id | name | short definition):
{catalog_block}

TARGET CONCEPTS (id | name):
{concepts_block}
"""


def translate_bridges(items_block: str, glossary_block: str) -> str:
    return f"""Translate each knowledge-building bridge sentence into natural Spanish, using the
GLOSSARY's Spanish concept names for any concept mentioned. Keep it equally concise.
Return JSON: {{"bridges":[{{"i": <index>, "bridge_es": "..."}}]}}

GLOSSARY (id | english | spanish):
{glossary_block}

BRIDGES (index | english bridge):
{items_block}
"""


# --------------------------------------------------------------------------- #
# Stage 10 — name the concept clusters (learning themes)
# --------------------------------------------------------------------------- #
CLUSTER_SYS = (
    "You name learning THEMES for a course on remote sensing for agricultural "
    "statistics. Each theme is a cluster of related concepts. You give a short, "
    "inviting bilingual title and a one-sentence description of what the learner "
    "will master. Output strict JSON only."
)


def name_clusters(blocks: str) -> str:
    return f"""For each cluster (its most representative concepts are listed), produce a concise
learning-theme name and description. Rules:
- "title_en"/"title_es": <=5 words, clear and inviting (e.g. "Crop Classification",
  "Yield & Phenology", "Sampling & Statistics").
- "desc_en"/"desc_es": ONE sentence (<=22 words) describing what the learner will master.
- Titles must be distinct across clusters.

Return JSON: {{"clusters":[{{"idx":<int>,"title_en","title_es","desc_en","desc_es"}}]}}

CLUSTERS (idx | representative concepts):
{blocks}
"""


# --------------------------------------------------------------------------- #
# Stage 6 — translation
# --------------------------------------------------------------------------- #
TRANSLATE_SYS = (
    "You are a bilingual (English/Spanish) terminologist specialized in remote "
    "sensing, geospatial science and agricultural statistics. You produce natural, "
    "standard Spanish terminology. Output strict JSON only."
)


def translate_names(names_block: str) -> str:
    return f"""Translate each English concept NAME into standard Spanish terminology used in
remote sensing / agricultural statistics. Keep widely-used acronyms (NDVI, SAR)
untranslated but you may add the Spanish expansion as an alias. Return JSON:
{{"terms":[{{"id","name_es","aliases_es":[..]}}]}}
NAMES (id | english name):
{names_block}
"""


def translate_defs(items_block: str, glossary_block: str) -> str:
    return f"""Translate each English definition into Spanish. You MUST use exactly the Spanish
concept names from the GLOSSARY for any concept mentioned, for consistency. Keep it
faithful and equally concise. Return JSON: {{"definitions":[{{"id","definition_es"}}]}}

GLOSSARY (id | english | spanish — use these Spanish terms):
{glossary_block}

DEFINITIONS TO TRANSLATE (id | english definition):
{items_block}
"""


# --------------------------------------------------------------------------- #
# Stage 8 — critic pass
# --------------------------------------------------------------------------- #
CRITIC_SYS = (
    "You are a meticulous reviewer of a concept ontology. You flag problems but do "
    "not rewrite. Output strict JSON only."
)


def critic(items_block: str) -> str:
    return f"""Review each concept entry and flag issues. Possible flags: "circular" (defines
itself), "vague", "wrong_category", "ungrounded" (claims a citation not supported),
"too_broad". Return JSON: {{"flags":[{{"id","flags":[..],"note":"..."}}]}} — include
only entries that have at least one flag.
ENTRIES (id | category | definition):
{items_block}
"""
