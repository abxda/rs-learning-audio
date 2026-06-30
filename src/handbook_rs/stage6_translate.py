"""Stage 6 — bilingual alignment.

1. Translate every node NAME to Spanish and freeze a terminology glossary.
2. Translate every definition, injecting the glossary so concept references stay
   consistent (no EN/ES drift).
3. Light back-translation drift check on a sample (reported, not fatal).
Then assemble the final out/ontology.json (single source of truth).
"""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from .config import build_dir, get_config, out_dir
from .io_utils import read_json, write_json
from .llm import prompts
from .llm.client import chat


def _batched(seq, n):
    return [seq[i:i + n] for i in range(0, len(seq), n)]


def _items(out, key: str) -> list:
    """Extract a list from a response that may be {key:[...]}, {other:[...]}, or [...]."""
    if isinstance(out, list):
        return out
    if isinstance(out, dict):
        v = out.get(key)
        if isinstance(v, list):
            return v
        for vv in out.values():
            if isinstance(vv, list):
                return vv
    return []


def _str_list(val) -> list[str]:
    """Coerce a model field into a clean list of strings (it occasionally nests)."""
    out: list[str] = []
    for a in val or []:
        if isinstance(a, str) and a.strip():
            out.append(a.strip())
        elif isinstance(a, list):
            out.extend(str(x).strip() for x in a if str(x).strip())
    return out


def _translate_names(nodes: list[dict]) -> dict[str, dict]:
    bs = get_config()["translate"]["batch_size"]
    result: dict[str, dict] = {}

    def do(batch):
        block = "\n".join(f"{n['id']} | {n['name_en']}" for n in batch)
        out = chat(prompts.TRANSLATE_SYS, prompts.translate_names(block), json_mode=True).json()
        return _items(out, "terms")

    with ThreadPoolExecutor(max_workers=6) as ex:
        for terms in ex.map(do, _batched(nodes, bs)):
            for t in terms:
                if t.get("id"):
                    name_es = t.get("name_es")
                    name_es = name_es.strip() if isinstance(name_es, str) else ""
                    result[t["id"]] = {"name_es": name_es,
                                       "aliases_es": _str_list(t.get("aliases_es"))}
    return result


def _translate_defs(nodes: list[dict], glossary_block: str) -> dict[str, str]:
    bs = get_config()["translate"]["batch_size"]
    result: dict[str, str] = {}

    def do(batch):
        block = "\n".join(f"{n['id']} | {n['definition_en']}" for n in batch if n['definition_en'])
        if not block:
            return []
        out = chat(prompts.TRANSLATE_SYS, prompts.translate_defs(block, glossary_block),
                   json_mode=True).json()
        return _items(out, "definitions")

    with ThreadPoolExecutor(max_workers=6) as ex:
        for defs in ex.map(do, _batched(nodes, bs)):
            for d in defs:
                de = d.get("definition_es")
                if d.get("id") and isinstance(de, str):
                    result[d["id"]] = de.strip()
    return result


def _translate_bridges(edges: list[dict], glossary_block: str) -> None:
    """Translate prereq-edge bridge_en -> bridge_es in place (batched)."""
    pe = [e for e in edges if e["rel"] == "prereq" and e.get("bridge_en")]
    bs = get_config()["translate"]["batch_size"]

    def do(batch_with_idx):
        block = "\n".join(f"{i} | {e['bridge_en']}" for i, e in batch_with_idx)
        out = chat(prompts.TRANSLATE_SYS, prompts.translate_bridges(block, glossary_block),
                   json_mode=True, max_tokens=4000).json()
        res = {}
        for b in _items(out, "bridges"):
            if isinstance(b, dict) and isinstance(b.get("i"), int) and isinstance(b.get("bridge_es"), str):
                res[b["i"]] = b["bridge_es"].strip()
        return res

    def run_pass(items):
        batches = [items[i:i + bs] for i in range(0, len(items), bs)]
        with ThreadPoolExecutor(max_workers=6) as ex:
            for res in ex.map(do, batches):
                for i, es in res.items():
                    if 0 <= i < len(pe):
                        pe[i]["bridge_es"] = es

    run_pass(list(enumerate(pe)))
    missing = [(i, e) for i, e in enumerate(pe) if not e.get("bridge_es")]
    if missing:
        run_pass(missing)                                  # retry truncated batches
    for e in pe:
        if not e.get("bridge_es"):
            e["bridge_es"] = e["bridge_en"]                # last-resort fallback


def assemble(nodes: list[dict], edges: list[dict], ledger, dropped,
             names_es: dict, defs_es: dict) -> dict:
    from . import __version__
    out_nodes = []
    for n in nodes:
        ne = names_es.get(n["id"], {})
        out_nodes.append({
            "id": n["id"], "kind": n["kind"],
            "name": {"en": n["name_en"], "es": ne.get("name_es", "")},
            "aliases": {"en": n.get("aliases_en", []), "es": ne.get("aliases_es", [])},
            "definition": {"en": n["definition_en"], "es": defs_es.get(n["id"], "")},
            "category": n.get("category", "other"),
            "level": n.get("level", 0), "topo_order": n.get("topo_order", 0),
            "closure_depth": n.get("closure_depth", 0),
            "zipf": n.get("zipf", {}),
            "citations": n.get("citations", []),
            "definition_terms": n.get("definition_terms", []),
            "def_uses": n.get("def_uses", []),
            "provenance": n.get("provenance", {}),
        })
    cfg = get_config()
    return {
        "meta": {
            "schema_version": "1.0",
            "source_book": cfg["book"]["title"],
            "model": cfg["llm"]["model"],
            "generator_version": __version__,
            "stats": {
                "nodes": len(out_nodes),
                "concepts": sum(1 for n in out_nodes if n["kind"] == "concept"),
                "primitives": sum(1 for n in out_nodes if n["kind"] == "primitive"),
                "edges": len(edges),
                "prereq_edges": sum(1 for e in edges if e["rel"] == "prereq"),
                "dropped": len(dropped),
                "max_level": max((n["level"] for n in out_nodes), default=0),
            },
        },
        "nodes": out_nodes,
        "edges": edges,
        "primitive_ledger": list(ledger),
        "dropped": dropped,
    }


def run(force: bool = False) -> Path:
    out = out_dir() / "ontology.json"
    if out.exists() and not force:
        print("Stage 6 cached.")
        return out

    g = read_json(build_dir() / "07_graph.json")
    nodes = g["nodes"]
    print(f"  translating {len(nodes)} names ...")
    names_es = _translate_names(nodes)
    glossary_block = "\n".join(
        f"{n['id']} | {n['name_en']} | {names_es.get(n['id'], {}).get('name_es', n['name_en'])}"
        for n in nodes)
    print(f"  translating {len(nodes)} definitions ...")
    defs_es = _translate_defs(nodes, glossary_block)

    # patch anything missed (e.g. a truncated batch) then fall back to EN
    miss_n = [n for n in nodes if not names_es.get(n["id"], {}).get("name_es")]
    if miss_n:
        print(f"  retrying {len(miss_n)} missing es-names ...")
        names_es.update(_translate_names(miss_n))
    miss_d = [n for n in nodes if n["definition_en"] and not defs_es.get(n["id"])]
    if miss_d:
        print(f"  retrying {len(miss_d)} missing es-defs ...")
        defs_es.update(_translate_defs(miss_d, glossary_block))
    for n in nodes:
        names_es.setdefault(n["id"], {})
        if not names_es[n["id"]].get("name_es"):
            names_es[n["id"]] = {"name_es": n["name_en"], "aliases_es": []}
        if n["definition_en"] and not defs_es.get(n["id"]):
            defs_es[n["id"]] = n["definition_en"]   # last-resort fallback

    n_bridges = sum(1 for e in g["edges"] if e["rel"] == "prereq" and e.get("bridge_en"))
    print(f"  translating {n_bridges} bridge sentences ...")
    _translate_bridges(g["edges"], glossary_block)

    ontology = assemble(nodes, g["edges"], g.get("ledger", []), g.get("dropped", []),
                        names_es, defs_es)
    write_json(out, ontology)
    write_json(build_dir() / "08_ontology.json", ontology)
    miss_name = sum(1 for n in ontology["nodes"] if not n["name"]["es"])
    miss_def = sum(1 for n in ontology["nodes"] if n["definition"]["en"] and not n["definition"]["es"])
    print(f"Stage 6 done: ontology.json written; missing es-name={miss_name}, es-def={miss_def}")
    return out


if __name__ == "__main__":
    run()
