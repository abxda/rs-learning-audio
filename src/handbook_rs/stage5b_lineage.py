"""Stage 5b — prerequisite lineage + knowledge-building bridges.

DeepSeek picks, for every concept, the direct prerequisites a learner must master
first (from the existing concept catalog) and writes a bridge sentence that
*constructs* the concept from each prerequisite. These explicit prerequisites
replace the sparse definition-derived ones, giving a deep basic->advanced lineage.
Cycles are broken by basicness; levels are recomputed by longest path.

Overwrites build/07_graph.json with: prereq edges carrying `bridge_en`, plus the
preserved defines_uses/see_also edges, and refreshed node level/topo_order.
"""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import networkx as nx

from .config import build_dir, get_config
from .io_utils import read_json, write_json
from .llm import prompts
from .llm.client import chat
from .stage5_graph import _basicness


def _catalog(nodes: list[dict]) -> str:
    rows = []
    for n in nodes:
        d = (n.get("definition_en") or "").replace("\n", " ")[:110]
        rows.append(f"{n['id']} | {n['name_en']} | {d}")
    return "\n".join(rows)


def _lineage_calls(nodes: list[dict]) -> dict[str, list[dict]]:
    catalog = _catalog(nodes)
    bs = get_config()["definitions"]["batch_size"]
    concepts = [n for n in nodes if n["kind"] == "concept"]
    batches = [concepts[i:i + bs] for i in range(0, len(concepts), bs)]
    result: dict[str, list[dict]] = {}

    def do(batch):
        block = "\n".join(f"{n['id']} | {n['name_en']}" for n in batch)
        user = prompts.lineage(catalog, block)
        try:
            out = chat(prompts.LINEAGE_SYS, user, json_mode=True, max_tokens=7000).json()
            return out.get("items", [])
        except Exception as e:  # noqa: BLE001 — a slow/failed batch must not block the stage
            print(f"    ! lineage batch failed ({str(e)[:60]}); concepts left as roots")
            return []

    print(f"  lineage over {len(concepts)} concepts in {len(batches)} batches ...")
    with ThreadPoolExecutor(max_workers=6) as ex:
        for items in ex.map(do, batches):
            for it in items:
                if it.get("id"):
                    result[it["id"]] = it.get("prereqs", [])
    # one retry pass for concepts that got nothing (covers a transiently-slow batch)
    missing = [n for n in concepts if n["id"] not in result]
    if missing:
        print(f"  retrying lineage for {len(missing)} concepts ...")
        retry_batches = [missing[i:i + 10] for i in range(0, len(missing), 10)]
        with ThreadPoolExecutor(max_workers=6) as ex:
            for items in ex.map(do, retry_batches):
                for it in items:
                    if it.get("id"):
                        result[it["id"]] = it.get("prereqs", [])
    return result


def run(force: bool = False) -> Path:
    marker = build_dir() / "07b_lineage.json"
    out = build_dir() / "07_graph.json"
    if marker.exists() and not force:
        print("Stage 5b cached.")
        return out

    g = read_json(out)
    nodes = {n["id"]: n for n in g["nodes"]}
    basic = {i: _basicness(n) for i, n in nodes.items()}
    prereqs = _lineage_calls(g["nodes"])

    # build prereq edges (prereq -> concept) with bridges, validated + oriented basic->adv
    pg = nx.DiGraph()
    pg.add_nodes_from(nodes)
    bridges: dict[tuple[str, str], str] = {}
    raw = 0
    for cid, plist in prereqs.items():
        if cid not in nodes:
            continue
        for p in plist[:5]:
            pid = p.get("id")
            if pid not in nodes or pid == cid:
                continue
            # orient so the edge always points more-basic -> less-basic
            a, b = (pid, cid) if basic[pid] >= basic[cid] else (cid, pid)
            bridge = (p.get("bridge") or "").strip()
            pg.add_edge(a, b)
            bridges[(a, b)] = bridge if (a, b) == (pid, cid) else bridge
            raw += 1

    # break residual cycles by weakest basicness margin
    cut = 0
    while not nx.is_directed_acyclic_graph(pg):
        cyc = nx.find_cycle(pg)
        u, v = min(cyc, key=lambda e: basic[e[0]] - basic[e[1]])[:2]
        pg.remove_edge(u, v)
        bridges.pop((u, v), None)
        cut += 1
    if cut:
        print(f"  broke {cut} cycles")

    # recompute longest-path levels + topo order
    topo = list(nx.topological_sort(pg))
    level: dict[str, int] = {}
    for nid in topo:
        preds = list(pg.predecessors(nid))
        level[nid] = 0 if not preds else 1 + max(level[p] for p in preds)
    order = {nid: i for i, nid in enumerate(topo)}
    for nid, n in nodes.items():
        n["level"] = level.get(nid, 0)
        n["topo_order"] = order.get(nid, 0)

    # rebuild edge list: keep defines_uses/see_also, replace prereq with lineage edges
    kept = [e for e in g["edges"] if e["rel"] != "prereq"]
    new_prereq = [{"src": u, "dst": v, "rel": "prereq", "bridge_en": bridges.get((u, v), "")}
                  for u, v in pg.edges()]
    g["edges"] = kept + new_prereq
    g["nodes"] = list(nodes.values())

    write_json(out, g)
    write_json(marker, {"prereq_edges": len(new_prereq), "cycles_cut": cut})
    maxlvl = max(level.values()) if level else 0
    roots = sum(1 for nid in nodes if level.get(nid, 0) == 0)
    print(f"Stage 5b done: {len(new_prereq)} prereq edges, max level {maxlvl}, "
          f"{roots} roots (level 0)")
    return out


if __name__ == "__main__":
    run()
