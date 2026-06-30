"""Stage 8 — the hard validators + build report. Closure, acyclicity, level
monotonicity, bilingual completeness, citation validity, Zipf coverage, and drop
accounting. Critical failures are reported loudly."""

from __future__ import annotations

from pathlib import Path

import networkx as nx

from .config import build_dir, get_config, out_dir
from .corpus import anchor_index
from .io_utils import read_json, write_json
from .norms import normalize


def _alias_index(nodes: list[dict]) -> dict[str, str]:
    idx: dict[str, str] = {}
    for n in nodes:
        for s in [n["name"]["en"], *n["aliases"]["en"]]:
            k = normalize(s)
            if k:
                idx.setdefault(k, n["id"])
    return idx


def validate(ontology: dict) -> dict:
    nodes = ontology["nodes"]
    edges = ontology["edges"]
    ids = {n["id"] for n in nodes}
    alias = _alias_index(nodes)
    ledger = set(ontology.get("primitive_ledger", []))
    results: dict[str, dict] = {}

    # 1) closure — no dangling edge endpoints + definition terms resolve
    dangling_edges = [e for e in edges if e["src"] not in ids or e["dst"] not in ids]
    unresolved = []
    for n in nodes:
        if n["kind"] != "concept":
            continue
        for t in n.get("definition_terms", []):
            k = normalize(t)
            if k and k not in alias and k not in ledger:
                unresolved.append((n["id"], t))
    results["closure"] = {
        "pass": not dangling_edges and not unresolved,
        "dangling_edges": len(dangling_edges),
        "unresolved_terms": len(unresolved),
        "examples": unresolved[:8],
        "critical": True,
    }

    # 2) acyclicity of prereq graph
    g = nx.DiGraph()
    g.add_nodes_from(ids)
    g.add_edges_from((e["src"], e["dst"]) for e in edges if e["rel"] == "prereq")
    is_dag = nx.is_directed_acyclic_graph(g)
    results["acyclicity"] = {"pass": is_dag,
                             "cycle": [] if is_dag else nx.find_cycle(g)[:6],
                             "critical": True}

    # 3) level monotonicity (prereq src must be a lower level than dst)
    level = {n["id"]: n["level"] for n in nodes}
    inv = [(e["src"], e["dst"]) for e in edges
           if e["rel"] == "prereq" and level.get(e["src"], 0) >= level.get(e["dst"], 0)]
    results["level_monotonicity"] = {"pass": not inv, "violations": len(inv),
                                     "examples": inv[:8], "critical": False}

    # 4) bilingual completeness
    miss = [n["id"] for n in nodes
            if not (n["name"]["en"] and n["name"]["es"] and n["definition"]["en"]
                    and n["definition"]["es"])]
    results["bilingual"] = {"pass": not miss, "missing": len(miss),
                            "examples": miss[:8], "critical": True}

    # 5) citation validity
    ai = anchor_index()
    bad = []
    for n in nodes:
        for c in n.get("citations", []):
            cid, anc = c.get("chapter_id"), c.get("anchor", "")
            if cid not in ai or (anc and anc not in ai[cid]):
                bad.append((n["id"], cid, anc))
    results["citations"] = {"pass": not bad, "invalid": len(bad),
                            "examples": bad[:8], "critical": False}

    # 6) Zipf coverage — top backbone mined terms that map to a node
    bb = read_json(build_dir() / "04_backbone.json")["terms"]
    top = bb[: min(len(bb), 250)]
    covered = sum(1 for t in top if normalize(t["surface"]) in alias)
    frac = covered / len(top) if top else 1.0
    thr = get_config()["validate"]["zipf_coverage_min"]
    results["zipf_coverage"] = {"pass": frac >= thr, "coverage": round(frac, 3),
                                "threshold": thr, "covered": covered, "of": len(top),
                                "critical": False}

    # 7) JSON-schema conformance
    try:
        import jsonschema
        from .config import ROOT
        schema = read_json(ROOT / "schema" / "ontology.schema.json")
        jsonschema.validate(ontology, schema)
        results["schema"] = {"pass": True, "critical": False}
    except Exception as e:  # noqa: BLE001
        results["schema"] = {"pass": False, "error": str(e)[:160], "critical": False}

    # 8) drop accounting
    stats = ontology["meta"]["stats"]
    results["drop_accounting"] = {
        "pass": True, "concepts": stats["concepts"], "primitives": stats["primitives"],
        "dropped": stats["dropped"], "critical": False,
        "note": "capped terms are degraded to primitive leaves (still closed) and logged",
    }
    return results


def _report(ontology: dict, results: dict) -> str:
    s = ontology["meta"]["stats"]
    lines = ["# Build Report — UN Handbook Concept Tree", "",
             f"- Source: {ontology['meta']['source_book']}",
             f"- Model: {ontology['meta']['model']}",
             f"- Nodes: **{s['nodes']}** ({s['concepts']} concepts, {s['primitives']} primitives)",
             f"- Edges: {s['edges']} ({s['prereq_edges']} prereq)",
             f"- Max level: {s['max_level']}", f"- Capped/logged: {s['dropped']}", "",
             "## Validators", ""]
    for name, r in results.items():
        mark = "✅" if r["pass"] else ("❌" if r.get("critical") else "⚠️")
        detail = ", ".join(f"{k}={v}" for k, v in r.items()
                           if k not in ("pass", "critical", "examples", "note"))
        lines.append(f"- {mark} **{name}** — {detail}")
        if r.get("examples"):
            lines.append(f"    - e.g. {r['examples'][:4]}")
    return "\n".join(lines) + "\n"


def run(force: bool = False) -> dict:
    ontology = read_json(out_dir() / "ontology.json")
    results = validate(ontology)
    report = _report(ontology, results)
    (build_dir() / "build_report.md").write_text(report)
    write_json(build_dir() / "validation.json", results)
    print(report)
    crit_fail = [k for k, r in results.items() if r.get("critical") and not r["pass"]]
    if crit_fail:
        print(f"\n❌ CRITICAL VALIDATORS FAILED: {crit_fail}")
    else:
        print("\n✅ All critical validators passed.")
    return results


if __name__ == "__main__":
    run()
