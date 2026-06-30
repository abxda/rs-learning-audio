"""Stage 7 — render the three deliverables from out/ontology.json as a true
pedagogical mind map: prerequisites with knowledge-building bridge sentences,
"this unlocks", and a full lineage-to-fundamentals chain for every concept.

  - out/glossary.md     bilingual glossary, basic -> advanced, with a learning path
  - out/vault/          Obsidian notes: prerequisites + bridges + lineage + [[links]]
  - out/graph.html      interactive learning DAG; click a node for its lineage/bridges
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import networkx as nx

from .config import out_dir
from .io_utils import read_json
from .norms import normalize


# --------------------------------------------------------------------------- #
# display helpers
# --------------------------------------------------------------------------- #
def _display(node: dict, lang: str) -> str:
    name = node["name"][lang]
    nn = normalize(name)
    best = name
    for a in node["aliases"].get(lang, []):
        if normalize(a) == nn and sum(c.isupper() for c in a) > sum(c.isupper() for c in best):
            best = a
    if best and best == best.lower():
        best = best[:1].upper() + best[1:]
    return best


def _sources(node: dict) -> str:
    cites = node.get("citations", [])
    return " · ".join(f"{c['chapter_id']}{c.get('anchor','')}" for c in cites) if cites else ""


def _surface_list(nodes: list[dict], lang: str) -> list[tuple[str, str]]:
    surfaces: list[tuple[str, str]] = []
    for n in nodes:
        for s in [n["name"][lang], *n["aliases"].get(lang, [])]:
            if s and len(s) >= 4:
                surfaces.append((s, n["id"]))
    surfaces.sort(key=lambda x: -len(x[0]))
    return surfaces


def _compile_linker(surfaces: list[tuple[str, str]]):
    lookup: dict[str, str] = {}
    for s, tid in surfaces:
        lookup.setdefault(s.lower(), tid)
    if not lookup:
        return None, {}
    alt = "|".join(re.escape(s) for s, _ in surfaces)
    return re.compile(rf"(?<!\w)(?:{alt})(?!\w)", re.IGNORECASE), lookup


def _linkify(text: str, linker, self_id: str) -> str:
    pat, lookup = linker
    if not text or pat is None:
        return text
    used = {self_id}

    def repl(m: re.Match) -> str:
        s = m.group(0)
        tid = lookup.get(s.lower())
        if not tid or tid in used:
            return s
        used.add(tid)
        return f"[[{tid}|{s}]]"

    return pat.sub(repl, text)


# --------------------------------------------------------------------------- #
# lineage structures
# --------------------------------------------------------------------------- #
def _build_lineage(nodes: list[dict], edges: list[dict]):
    """Return (parents, children, chain) where parents[id]=[(pid,bridge_en,bridge_es)],
    children[id]=[(cid,bridge_en,bridge_es)], chain[id]=[ancestor ids ... self] (the
    longest path from a fundamental root down to the node)."""
    parents: dict[str, list] = {n["id"]: [] for n in nodes}
    children: dict[str, list] = {n["id"]: [] for n in nodes}
    g = nx.DiGraph()
    g.add_nodes_from(n["id"] for n in nodes)
    for e in edges:
        if e["rel"] != "prereq":
            continue
        p, c = e["src"], e["dst"]          # parent (basic) -> child (advanced)
        be, bs = e.get("bridge_en", ""), e.get("bridge_es", "")
        if c in parents:
            parents[c].append((p, be, bs))
        if p in children:
            children[p].append((c, be, bs))
        g.add_edge(p, c)
    # longest path to each node
    chain: dict[str, list[str]] = {}
    best_parent: dict[str, str] = {}
    dist: dict[str, int] = {}
    for nid in nx.topological_sort(g):
        preds = list(g.predecessors(nid))
        if not preds:
            dist[nid] = 0
        else:
            bp = max(preds, key=lambda p: dist.get(p, 0))
            dist[nid] = dist[bp] + 1
            best_parent[nid] = bp
    for nid in g.nodes():
        path, cur = [], nid
        seen = set()
        while cur is not None and cur not in seen:
            seen.add(cur)
            path.append(cur)
            cur = best_parent.get(cur)
        chain[nid] = list(reversed(path))
    return parents, children, chain


# --------------------------------------------------------------------------- #
# glossary
# --------------------------------------------------------------------------- #
def emit_glossary(ont: dict, parents, chain) -> Path:
    nodes = ont["nodes"]
    by_id = {n["id"]: n for n in nodes}
    levels: dict[int, list[dict]] = {}
    for n in nodes:
        levels.setdefault(n["level"], []).append(n)
    s = ont["meta"]["stats"]
    out = ["# UN Handbook — Bilingual Concept Mind Map / Mapa mental bilingüe",
           f"*{ont['meta']['source_book']}*", "",
           "A closed, navigable knowledge corpus: concepts ordered from **fundamentals "
           "(level 0)** to **advanced**, each built from its prerequisites by a "
           "knowledge-construction sentence. / Corpus de conocimiento cerrado: de los "
           "**fundamentos (nivel 0)** a lo **avanzado**, cada concepto construido desde "
           "sus prerrequisitos.", "",
           f"> {s['nodes']} nodes · {s['concepts']} concepts · {s['primitives']} primitives "
           f"· {s['prereq_edges']} prerequisite links · {s['max_level']} levels", ""]
    for lvl in sorted(levels):
        out.append(f"\n## Level {lvl}\n")
        for n in sorted(levels[lvl], key=lambda x: x["name"]["en"].lower()):
            out.append(f"<a id='{n['id']}'></a>")
            out.append(f"### {_display(n, 'en')} — {_display(n, 'es')}")
            meta = f"*{n['category']}*"
            if _sources(n):
                meta += f" · sources: {_sources(n)}"
            out.append(meta)
            out.append(f"- **EN.** {n['definition']['en']}")
            out.append(f"- **ES.** {n['definition']['es']}")
            ps = parents.get(n["id"], [])
            if ps:
                out.append("- **Prerequisites / Prerrequisitos:**")
                for pid, be, _bs in ps[:6]:
                    if pid in by_id:
                        out.append(f"    - [{_display(by_id[pid], 'en')}](#{pid})"
                                   + (f" — {be}" if be else ""))
            ch = chain.get(n["id"], [])
            if len(ch) > 1:
                path = " → ".join(_display(by_id[c], "en") for c in ch if c in by_id)
                out.append(f"- **Lineage / Linaje:** {path}")
            out.append("")
    p = out_dir() / "glossary.md"
    p.write_text("\n".join(out), encoding="utf-8")
    return p


# --------------------------------------------------------------------------- #
# Obsidian vault
# --------------------------------------------------------------------------- #
def emit_vault(ont: dict, parents, children, chain) -> Path:
    nodes = ont["nodes"]
    by_id = {n["id"]: n for n in nodes}
    vault = out_dir() / "vault"
    vault.mkdir(parents=True, exist_ok=True)
    en_linker = _compile_linker(_surface_list(nodes, "en"))
    es_linker = _compile_linker(_surface_list(nodes, "es"))

    for n in nodes:
        nid = n["id"]
        def_en = _linkify(n["definition"]["en"], en_linker, nid)
        def_es = _linkify(n["definition"]["es"], es_linker, nid)
        fm = ["---", f"id: {nid}", f"kind: {n['kind']}", f"category: {n['category']}",
              f"level: {n['level']}",
              f"aliases: [{', '.join(json.dumps(a) for a in n['aliases']['en'][:8])}]",
              "---", ""]
        body = [f"# {_display(n, 'en')} / {_display(n, 'es')}", "",
                f"> **level {n['level']}** · *{n['category']}*"
                + (f" · sources: {_sources(n)}" if _sources(n) else ""), "",
                "**What it is / Qué es.**", "",
                "- **EN.** " + def_en, "- **ES.** " + def_es, ""]

        ps = [(pid, be, bs) for pid, be, bs in parents.get(nid, []) if pid in by_id]
        if ps:
            body.append("## Understand these first / Entiende esto primero")
            for pid, be, bs in ps:
                body.append(f"- [[{pid}|{_display(by_id[pid], 'en')}]]"
                            f" — *{by_id[pid]['category']}*")
                if be:
                    body.append(f"    - **EN.** {be}")
                if bs:
                    body.append(f"    - **ES.** {bs}")
            body.append("")

        ch = chain.get(nid, [])
        if len(ch) > 1:
            link_chain = " → ".join(f"[[{c}|{_display(by_id[c], 'en')}]]"
                                    for c in ch if c in by_id)
            body.append("## Lineage to fundamentals / Linaje hasta los fundamentos")
            body.append(link_chain)
            body.append("")

        cs = [(cid, be, bs) for cid, be, bs in children.get(nid, []) if cid in by_id]
        if cs:
            body.append("## This unlocks / Esto habilita")
            for cid, be, _bs in cs[:20]:
                body.append(f"- [[{cid}|{_display(by_id[cid], 'en')}]]"
                            + (f" — {be}" if be else ""))
            body.append("")

        (vault / f"{nid}.md").write_text("\n".join(fm + body), encoding="utf-8")

    # index: the fundamentals to start from
    roots = sorted([n for n in nodes if n["level"] == 0], key=lambda x: x["name"]["en"].lower())
    idx = ["# Concept Mind Map — Index / Índice", "",
           "Start from the fundamentals and follow **This unlocks** forward, or open any "
           "concept and walk its **Lineage** backward. / Empieza por los fundamentos y "
           "sigue **Esto habilita**, o abre cualquier concepto y recorre su **Linaje**.", "",
           "## Fundamentals / Fundamentos (level 0)"]
    idx += [f"- [[{n['id']}|{_display(n, 'en')}]] — {_display(n, 'es')}" for n in roots]
    (vault / "_index.md").write_text("\n".join(idx), encoding="utf-8")
    return vault


# --------------------------------------------------------------------------- #
# interactive graph
# --------------------------------------------------------------------------- #
_HTML = """<!doctype html><html lang="en"><head><meta charset="utf-8">
<title>UN Handbook — Concept Mind Map</title>
<script src="https://unpkg.com/vis-network@9.1.6/dist/vis-network.min.js"></script>
<style>
 body{margin:0;font-family:system-ui,sans-serif;display:flex;height:100vh}
 #graph{flex:1;background:#0e1116}
 #side{width:400px;padding:16px 18px;overflow:auto;background:#161b22;color:#d7dde6;box-sizing:border-box}
 #side h2{margin:.2em 0;font-size:1.15rem;color:#fff}
 .es{color:#9fb4d6}.muted{color:#8b97a8;font-size:.82rem}
 #search{width:100%;padding:8px;margin-bottom:10px;border-radius:6px;border:1px solid #30363d;background:#0e1116;color:#fff}
 .pill{display:inline-block;padding:1px 8px;border-radius:10px;background:#243049;color:#9fb4d6;font-size:.72rem;margin-right:4px}
 .bridge{font-size:.86rem;margin:.15em 0 .5em 0;border-left:2px solid #30425e;padding-left:8px}
 a{color:#6cb6ff;cursor:pointer}
 h3{margin:.8em 0 .2em;font-size:.9rem;color:#cbd5e1;text-transform:uppercase;letter-spacing:.04em}
</style></head><body>
<div id="graph"></div>
<div id="side">
 <input id="search" placeholder="Search concept / buscar concepto…">
 <div id="info"><p class="muted">Click a node — Haz clic en un nodo.<br>Arrows point from basic → advanced.<br>Color = level.</p></div>
</div>
<script>
const DATA = __DATA__;
const palette=["#2e7d32","#388e3c","#558b2f","#9e9d24","#f9a825","#ef6c00","#d84315","#c62828","#ad1457","#6a1b9a","#4527a0","#283593"];
const colorFor=l=>palette[Math.min(l,palette.length-1)];
const byId=Object.fromEntries(DATA.nodes.map(n=>[n.id,n]));
const nodes=new vis.DataSet(DATA.nodes.map(n=>({id:n.id,label:n.name_en,level:n.level,
  color:colorFor(n.level),shape:n.kind==='primitive'?'dot':'box',
  font:{color:'#e6edf3',size:14},value:Math.max(1,n.freq)})));
const edges=new vis.DataSet(DATA.edges.map(e=>({from:e.src,to:e.dst,arrows:'to',
  color:{color:'#30425e'},title:e.bridge||''})));
const net=new vis.Network(document.getElementById('graph'),{nodes,edges},{
  layout:{hierarchical:{enabled:true,direction:'UD',sortMethod:'directed',levelSeparation:150,nodeSpacing:115}},
  physics:false,interaction:{hover:true,tooltipDelay:120}});
function chainHtml(id){const c=byId[id].chain||[];return c.map(x=>`<a onclick="show('${x}')">${byId[x].name_en}</a>`).join(' → ');}
function show(id){const n=byId[id];if(!n)return;
  const pre=(n.parents||[]).map(p=>`<div><a onclick="show('${p.id}')">${byId[p.id].name_en}</a><div class='bridge'>${p.be||''}<br><span class='es'>${p.bs||''}</span></div></div>`).join('');
  const unl=(n.children||[]).map(c=>`<a onclick="show('${c}')">${byId[c].name_en}</a>`).join(', ');
  document.getElementById('info').innerHTML=
   `<h2>${n.name_en}</h2><h2 class='es'>${n.name_es}</h2>
    <p><span class='pill'>level ${n.level}</span><span class='pill'>${n.category}</span></p>
    <p><b>EN.</b> ${n.def_en}</p><p class='es'><b>ES.</b> ${n.def_es}</p>
    <p class='muted'>${n.sources?('sources: '+n.sources):''}</p>
    <h3>Understand first / Entiende primero</h3>${pre||'<p class="muted">— fundamental —</p>'}
    <h3>Lineage / Linaje</h3><p>${chainHtml(id)}</p>
    <h3>This unlocks / Esto habilita</h3><p>${unl||'—'}</p>`;
  net.selectNodes([id]);net.focus(id,{scale:1.0,animation:true});}
net.on('click',p=>{if(p.nodes.length)show(p.nodes[0]);});
document.getElementById('search').addEventListener('keydown',e=>{if(e.key!=='Enter')return;
  const q=e.target.value.toLowerCase();
  const hit=DATA.nodes.find(n=>n.name_en.toLowerCase().includes(q)||n.name_es.toLowerCase().includes(q));
  if(hit)show(hit.id);});
</script></body></html>"""


def emit_graph_html(ont: dict, parents, children, chain) -> Path:
    nodes = ont["nodes"]
    by_id = {n["id"]: n for n in nodes}
    jnodes = [{
        "id": n["id"], "name_en": _display(n, "en"), "name_es": _display(n, "es"),
        "def_en": n["definition"]["en"], "def_es": n["definition"]["es"],
        "level": n["level"], "category": n["category"], "kind": n["kind"],
        "freq": (n.get("zipf", {}).get("corpus_freq") or 1), "sources": _sources(n),
        "parents": [{"id": p, "be": be, "bs": bs} for p, be, bs in parents.get(n["id"], [])
                    if p in by_id][:6],
        "children": [c for c, _, _ in children.get(n["id"], []) if c in by_id][:12],
        "chain": [c for c in chain.get(n["id"], []) if c in by_id],
    } for n in nodes]
    jedges = [{"src": e["src"], "dst": e["dst"], "bridge": e.get("bridge_en", "")}
              for e in ont["edges"] if e["rel"] == "prereq"]
    data = json.dumps({"nodes": jnodes, "edges": jedges}, ensure_ascii=False)
    p = out_dir() / "graph.html"
    p.write_text(_HTML.replace("__DATA__", data), encoding="utf-8")
    return p


def run(force: bool = False) -> Path:
    ont = read_json(out_dir() / "ontology.json")
    parents, children, chain = _build_lineage(ont["nodes"], ont["edges"])
    g = emit_glossary(ont, parents, chain)
    v = emit_vault(ont, parents, children, chain)
    h = emit_graph_html(ont, parents, children, chain)
    deep = sum(1 for c in chain.values() if len(c) > 1)
    print(f"Stage 7 done: {g.name}, {v.name}/ ({len(ont['nodes'])} notes), {h.name}; "
          f"{deep} concepts with a multi-step lineage")
    return out_dir()


if __name__ == "__main__":
    run()
