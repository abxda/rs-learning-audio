"""Stage 4 — grounded definitions + the terminating closure loop.

1. Define the seed concepts (corpus-grounded, threaded, cached).
2. Collect the key terms used in those definitions; classify each as COVERED /
   PRIMITIVE / NEW_CONCEPT. New concepts get defined; their key terms feed the next
   round. Repeat breadth-first until the frontier is dry or caps (max_depth /
   max_nodes) are hit. Caps degrade a would-be concept to a primitive LEAF (with a
   gloss) rather than dropping it, so closure always holds. Everything capped is logged.

Output: build/06_nodes.json (concepts + primitives, with def_uses links), plus a
build report fragment.
"""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from rapidfuzz import fuzz, process

from .config import build_dir, get_config
from .corpus import anchor_index, anchor_index_compact, corpus_context
from .embed import NodeIndex
from .io_utils import read_json, write_json
from .llm import prompts
from .llm.client import chat
from .norms import normalize
from .store import NodeStore

CFG = None


def cfg():
    global CFG
    if CFG is None:
        CFG = get_config()
    return CFG


# --------------------------------------------------------------------------- #
# definitions
# --------------------------------------------------------------------------- #
def _valid_citations(raw: list) -> list[dict]:
    ai = anchor_index()
    out = []
    for c in raw or []:
        cid = (c.get("chapter_id") or "").strip()
        if cid not in ai:
            continue
        anchor = (c.get("anchor") or "").strip()
        if anchor and anchor not in ai[cid]:
            anchor = ""
        out.append({"chapter_id": cid, "anchor": anchor})
    return out[:3]


def _grounded_key_terms(definition: str, key_terms: list, own_name: str) -> list[str]:
    """Keep only key terms that actually appear in the definition (grounded), and
    are not the concept's own name."""
    dn = normalize(definition)
    own = normalize(own_name)
    seen, out = set(), []
    for t in key_terms or []:
        nt = normalize(t)
        if not nt or nt == own or nt in seen:
            continue
        if nt in dn:
            seen.add(nt)
            out.append(t.strip())
    return out


def _define_batch(store: NodeStore, ids: list[str], *, is_new: bool) -> None:
    if not ids:
        return
    nodes = store.nodes
    block = "\n".join(f"{i} | {nodes[i]['name_en']} | {nodes[i]['category']}" for i in ids)
    anchors = anchor_index_compact()
    c = cfg()["definitions"]
    if is_new:
        instr = prompts.define_new(block, anchors, cfg()["definitions"]["max_def_words"],
                                   cfg()["closure"]["new_terms_per_def"])
    else:
        instr = prompts.define_batch(block, anchors, cfg()["definitions"]["max_def_words"],
                                     cfg()["closure"]["new_terms_per_def"])
    # corpus first (stable cached prefix), then the batch instruction
    user = corpus_context() + "\n\n----- TASK -----\n" + instr
    res = chat(prompts.DEFINE_SYS, user, json_mode=True, max_tokens=8000)
    for d in res.json().get("definitions", []):
        cid = d.get("id")
        if cid not in nodes:
            continue
        definition = (d.get("definition_en") or "").strip()
        nodes[cid]["definition_en"] = definition
        nodes[cid]["citations"] = _valid_citations(d.get("citations"))
        nodes[cid]["definition_terms"] = _grounded_key_terms(
            definition, d.get("key_terms", []), nodes[cid]["name_en"])
        nodes[cid]["provenance"]["definition_call_id"] = res.call_id


def _define_round(store: NodeStore, ids: list[str], *, is_new: bool) -> None:
    bs = cfg()["definitions"]["batch_size"]
    batches = [ids[i:i + bs] for i in range(0, len(ids), bs)]
    print(f"    defining {len(ids)} concepts in {len(batches)} batch(es) ...")
    with ThreadPoolExecutor(max_workers=6) as ex:
        list(ex.map(lambda b: _define_batch(store, b, is_new=is_new), batches))


# --------------------------------------------------------------------------- #
# closure classification
# --------------------------------------------------------------------------- #
def _link(store: NodeStore, parent: str, target: str, term: str = "") -> None:
    if term:
        store.add_alias(target, term)        # keep closure verifiable + linkable
    if target and parent and target != parent:
        du = store.nodes[parent]["def_uses"]
        if target not in du:
            du.append(target)


def _collect_frontier(store: NodeStore) -> list[tuple[str, str]]:
    seen, frontier = set(), []
    for n in store.nodes.values():
        if n["kind"] != "concept" or not n["definition_en"]:
            continue
        for t in n["definition_terms"]:
            nt = normalize(t)
            if nt and nt not in store.classified and nt not in seen:
                seen.add(nt)
                frontier.append((t, n["id"]))
    return frontier


def _classify_round(store: NodeStore, frontier: list[tuple[str, str]], depth: int,
                    index: NodeIndex) -> list[str]:
    """Triage frontier terms; return ids of NEW concepts that need defining."""
    cc = cfg()["closure"]
    alias_keys = list(store.alias_norm.keys())
    band: list[tuple[str, str, str]] = []     # (term, parent, candidate_id) -> LLM adjudicate
    to_llm: list[tuple[str, str]] = []        # (term, parent) -> LLM classify

    # direct + lexical resolution
    pending: list[tuple[str, str]] = []
    for term, parent in frontier:
        nt = normalize(term)
        store.classified.add(nt)
        rid = store.resolve(term)
        if rid:
            _link(store, parent, rid, term)
            continue
        m = process.extractOne(nt, alias_keys, scorer=fuzz.token_sort_ratio)
        if m and m[1] >= cc["tau_merge_lexical"]:
            _link(store, parent, store.alias_norm[m[0]], term)
            continue
        pending.append((term, parent))

    # embedding band
    if pending:
        hits = index.query_batch([t for t, _ in pending])
        for (term, parent), (cand_id, cos) in zip(pending, hits):
            if cos >= cc["tau_merge_high"] and cand_id:
                _link(store, parent, cand_id, term)
            elif cc["tau_merge_low"] <= cos < cc["tau_merge_high"] and cand_id:
                band.append((term, parent, cand_id))
            else:
                to_llm.append((term, parent))

    # LLM adjudication of the ambiguous band (batched to avoid truncation)
    CH = 30
    if band:
        for start in range(0, len(band), CH):
            chunk = band[start:start + CH]
            pb = "\n".join(
                f"{i} | {term} | {store.nodes[cid]['name_en']} | {store.nodes[cid]['definition_en'][:140]}"
                for i, (term, _, cid) in enumerate(chunk))
            verdicts = chat(prompts.ADJ_SYS, prompts.adjudicate(pb), json_mode=True,
                            max_tokens=4000).json()
            same = {v["i"]: v.get("same") for v in verdicts.get("verdicts", []) if "i" in v}
            for i, (term, parent, cid) in enumerate(chunk):
                if same.get(i):
                    _link(store, parent, cid, term)
                else:
                    to_llm.append((term, parent))

    # LLM classify: concept vs primitive (always returns gloss), batched
    new_ids: list[str] = []
    if to_llm:
        # de-dup by normalized term, remember every parent that used it
        uniq: dict[str, list[str]] = {}
        disp: dict[str, str] = {}
        for term, parent in to_llm:
            nt = normalize(term)
            uniq.setdefault(nt, []).append(parent)
            disp.setdefault(nt, term)
        terms_list = list(uniq)
        by_term: dict[str, dict] = {}
        for start in range(0, len(terms_list), CH):
            chunk = terms_list[start:start + CH]
            tb = "\n".join(disp[nt] for nt in chunk)
            items = chat(prompts.CLASSIFY_SYS, prompts.classify_terms(tb), json_mode=True,
                         max_tokens=6000).json()
            for it in items.get("items", []):
                by_term[normalize(it.get("term", ""))] = it
        at_cap_or_depth = depth >= cc["max_depth"]
        for nt, parents in uniq.items():
            it = by_term.get(nt, {})
            decision = it.get("decision", "primitive")
            name = (it.get("name") or disp[nt]).strip()
            gloss = (it.get("gloss") or name).strip()
            full = store.n_concepts() >= cc["max_nodes"]
            if decision == "concept" and not at_cap_or_depth and not full:
                cid = _mk_concept(store, name, it.get("category", "other"), depth + 1)
                new_ids.append(cid)
            else:
                reason = ""
                if decision == "concept" and (at_cap_or_depth or full):
                    reason = "node_cap" if full else "max_depth"
                cid = store.add_primitive(name, gloss, depth + 1,
                                          discovered_under=parents[0], reason=reason)
            store.add_alias(cid, disp[nt])          # original surface -> the new node
            for p in parents:
                _link(store, p, cid, disp[nt])
    return new_ids


def _mk_concept(store: NodeStore, name: str, category: str, depth: int) -> str:
    from .norms import slugify
    base = slugify(name) or "concept"
    cid, n = base, 2
    while cid in store.nodes:
        cid, n = f"{base}-{n}", n + 1
    store.add_concept({"id": cid, "name_en": name, "category": category,
                       "aliases_en": [name], "absorbs": [],
                       "zipf": {"in_backbone": False, "corpus_freq": 0,
                                "corpus_rank": None, "doc_freq": 0},
                       "provenance": {"created_in": "closure"}}, depth)
    return cid


# --------------------------------------------------------------------------- #
# driver
# --------------------------------------------------------------------------- #
def run(force: bool = False) -> Path:
    out = build_dir() / "06_nodes.json"
    if out.exists() and not force:
        print("Stage 4 cached.")
        return out

    seeds = read_json(build_dir() / "05_concepts.json")["concepts"]
    store = NodeStore()
    for c in seeds:
        store.add_concept(c, depth=0)

    print(f"  Stage 4: {store.n_concepts()} seed concepts")
    _define_round(store, store.undefined_concept_ids(), is_new=False)

    index = NodeIndex()
    cc = cfg()["closure"]
    depth = 0
    while depth < cc["max_depth"]:
        frontier = _collect_frontier(store)
        if not frontier:
            print(f"  closure converged at depth {depth} (frontier dry)")
            break
        index.build(store.nodes)
        print(f"  depth {depth}: {len(frontier)} frontier terms, {store.n_concepts()} concepts")
        new_ids = _classify_round(store, frontier, depth, index)
        if new_ids:
            _define_round(store, new_ids, is_new=True)
        depth += 1
    else:
        # hit max_depth: resolve any remaining frontier terms to primitive leaves
        frontier = _collect_frontier(store)
        if frontier:
            print(f"  max_depth reached: degrading {len(frontier)} leftover terms to primitives")
            index.build(store.nodes)
            _classify_round(store, frontier, cc["max_depth"], index)

    # patch any concept that came back without a definition (missed in a batch)
    undefined = store.undefined_concept_ids()
    if undefined:
        print(f"  patching {len(undefined)} undefined concepts ...")
        _define_round(store, undefined, is_new=True)
        for cid in store.undefined_concept_ids():
            n = store.nodes[cid]
            n["definition_en"] = f"{n['name_en']}: a concept used in the handbook."

    # final closure sweep: no definition term may be left dangling (terms found in
    # late/patched definitions are resolved or degraded to primitive leaves)
    leftover = _collect_frontier(store)
    if leftover:
        print(f"  final closure sweep: resolving {len(leftover)} leftover terms")
        index.build(store.nodes)
        _classify_round(store, leftover, cc["max_depth"], index)

    # finalize
    nodes = list(store.nodes.values())
    n_concept = sum(1 for n in nodes if n["kind"] == "concept")
    n_prim = sum(1 for n in nodes if n["kind"] == "primitive")
    write_json(out, {"n_nodes": len(nodes), "n_concepts": n_concept, "n_primitives": n_prim,
                     "nodes": nodes, "ledger": sorted(store.ledger),
                     "dropped": store.dropped})
    undefined = [n["id"] for n in nodes if n["kind"] == "concept" and not n["definition_en"]]
    print(f"Stage 4 done: {len(nodes)} nodes ({n_concept} concepts, {n_prim} primitives); "
          f"{len(store.dropped)} capped; {len(undefined)} undefined")
    return out


if __name__ == "__main__":
    run()
