"""Stage 5 — build the graph and the basic->advanced leveling.

Two edge relations (kept distinct, per the design):
  - defines_uses : C uses term T in its definition (raw definitional dependency).
  - prereq       : B is a prerequisite of A. Derived from defines_uses with a strict
                   "more basic" asymmetry so the prereq graph is acyclic by
                   construction; residual cycles are cut to see_also.
Levels come from the longest prereq chain (so depth reads as basic->advanced).
A defines_uses pair that did not yield a prereq edge is emitted as see_also.
"""

from __future__ import annotations

from pathlib import Path

import networkx as nx

from .config import build_dir
from .io_utils import read_json, write_json


def _basicness(node: dict) -> float:
    """Higher = more basic. Primitives are most basic; then more frequent / earlier."""
    is_prim = 1 if node["kind"] == "primitive" else 0
    freq = node.get("zipf", {}).get("corpus_freq", 0) or 0
    depth = node.get("closure_depth", 0)
    return is_prim * 1e12 + freq * 1e3 - depth


def run(force: bool = False) -> Path:
    out = build_dir() / "07_graph.json"
    if out.exists() and not force:
        print("Stage 5 cached.")
        return out

    data = read_json(build_dir() / "06_nodes.json")
    nodes = {n["id"]: n for n in data["nodes"]}
    basic = {i: _basicness(n) for i, n in nodes.items()}

    edges: list[dict] = []
    prereq = nx.DiGraph()
    prereq.add_nodes_from(nodes)

    for cid, n in nodes.items():
        for tid in n.get("def_uses", []):
            if tid not in nodes or tid == cid:
                continue
            edges.append({"src": cid, "dst": tid, "rel": "defines_uses"})
            if basic[tid] > basic[cid]:           # T strictly more basic -> prereq of C
                prereq.add_edge(tid, cid)
            else:
                edges.append({"src": cid, "dst": tid, "rel": "see_also"})

    # guarantee acyclicity: cut the least-basic-justified edge in each cycle
    cut = 0
    while not nx.is_directed_acyclic_graph(prereq):
        cycle = nx.find_cycle(prereq)
        # remove the edge with the smallest basicness margin (weakest prereq)
        u, v = min(cycle, key=lambda e: basic[e[0]] - basic[e[1]])[:2]
        prereq.remove_edge(u, v)
        edges.append({"src": v, "dst": u, "rel": "see_also"})
        cut += 1
    if cut:
        print(f"  cut {cut} prereq edges to break cycles")

    # longest-path levels + topological order
    topo = list(nx.topological_sort(prereq))
    level: dict[str, int] = {}
    for node_id in topo:
        preds = list(prereq.predecessors(node_id))
        level[node_id] = 0 if not preds else 1 + max(level[p] for p in preds)
    topo_order = {nid: i for i, nid in enumerate(topo)}

    for cid, n in nodes.items():
        n["level"] = level.get(cid, 0)
        n["topo_order"] = topo_order.get(cid, 0)
    for u, v in prereq.edges():
        edges.append({"src": u, "dst": v, "rel": "prereq"})

    # de-dup edges
    seen, uniq = set(), []
    for e in edges:
        k = (e["src"], e["dst"], e["rel"])
        if k not in seen:
            seen.add(k)
            uniq.append(e)

    write_json(out, {"nodes": list(nodes.values()), "edges": uniq,
                     "ledger": data.get("ledger", []), "dropped": data.get("dropped", [])})
    maxlvl = max(level.values()) if level else 0
    print(f"Stage 5 done: {len(nodes)} nodes, {len(uniq)} edges, "
          f"{sum(1 for e in uniq if e['rel']=='prereq')} prereq, max level {maxlvl}")
    return out


if __name__ == "__main__":
    run()
