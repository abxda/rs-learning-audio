"""Stage 9 — generate out/index.html: a single, self-contained, offline learning
web app (GitHub Pages ready) built from the ontology.

Features: searchable concept universe (basic->advanced); pick any concept and a
graph traces the complete prerequisite route to its origin; Next/Prev along the
route; free lateral exploration with a compass back to the planned route; multiple
routes; per-concept notes; export/import the learning memory as JSON; export notes
+ lineage for a chatbot. No external dependencies (works from file:// and Kindle).
"""

from __future__ import annotations

import json
from pathlib import Path

from .config import build_dir, out_dir
from .io_utils import read_json
from .stage7_emit import _display, _sources


MODEL_LABELS = {
    "xtts": "XTTS v2 · Damien Black",
    "qwen": "Qwen3-TTS · Ryan",
    "kokoro": "Kokoro",
}


def available_models() -> list[dict]:
    """List audio model folders under out/audio/ that already contain clips.
    Ordered by preference (xtts default first)."""
    pref = ["xtts", "qwen", "kokoro"]
    base = out_dir() / "audio"
    models = []
    if base.exists():
        for d in base.iterdir():
            if d.is_dir() and any(d.glob("*.mp3")):
                models.append({"id": d.name, "label": MODEL_LABELS.get(d.name, d.name),
                               "count": len(list(d.glob("*.mp3")))})
    models.sort(key=lambda m: (pref.index(m["id"]) if m["id"] in pref else 99, m["id"]))
    return models


def build_payload(ont: dict) -> dict:
    nodes = ont["nodes"]
    out_nodes = []
    for n in nodes:
        al = " ".join([n["name"]["en"], n["name"]["es"],
                       *n["aliases"].get("en", []), *n["aliases"].get("es", [])]).lower()
        out_nodes.append({
            "id": n["id"],
            "en": _display(n, "en"), "es": _display(n, "es"),
            "den": n["definition"]["en"], "des": n["definition"]["es"],
            "lvl": n["level"], "ord": n.get("topo_order", 0),
            "cat": n["category"], "kind": n["kind"],
            "src": _sources(n), "al": al,
        })
    prereq = [[e["src"], e["dst"], e.get("bridge_en", ""), e.get("bridge_es", "")]
              for e in ont["edges"] if e["rel"] == "prereq"]
    prkey = {(e["src"], e["dst"]) for e in ont["edges"] if e["rel"] == "prereq"}
    rel = []
    seen = set()
    for e in ont["edges"]:
        if e["rel"] in ("see_also", "defines_uses"):
            a, b = e["src"], e["dst"]
            if (a, b) in prkey or (b, a) in prkey:
                continue
            k = tuple(sorted((a, b)))
            if k not in seen and a != b:
                seen.add(k)
                rel.append([a, b])
    cpath = build_dir() / "10_clusters.json"
    clu = read_json(cpath) if cpath.exists() else {"clusters": [], "node_xy": {}, "node_cluster": {}}
    return {"meta": {"title": ont["meta"]["source_book"], "stats": ont["meta"]["stats"],
                     "models": available_models(),
                     "clustering": {"method": clu.get("method"), "k": clu.get("k"),
                                    "silhouette": clu.get("silhouette")}},
            "nodes": out_nodes, "prereq": prereq, "rel": rel,
            "clusters": clu.get("clusters", []), "node_xy": clu.get("node_xy", {}),
            "node_cluster": clu.get("node_cluster", {})}


def run(force: bool = False) -> Path:
    ont = read_json(out_dir() / "ontology.json")
    payload = build_payload(ont)
    data = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    html = _TEMPLATE.replace("__DATA__", data)
    p = out_dir() / "index.html"
    p.write_text(html, encoding="utf-8")
    kb = len(html.encode("utf-8")) // 1024
    print(f"Stage 9 done: {p} ({kb} KB, self-contained, {len(payload['nodes'])} concepts)")
    return p


_TEMPLATE = r"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Ruta de Aprendizaje — Teledetección para Estadísticas Agrícolas</title>
<style>
:root{
  --bg:#f5efe2; --panel:#efe7d6; --ink:#2b2620; --soft:#6f6657; --line:#ddd1ba;
  --accent:#9a5b2e; --accent2:#3f6f55; --chip:#e7dcc4; --link:#8a4b1f; --shadow:rgba(60,45,20,.12);
  --read: 'Iowan Old Style','Palatino Linotype','Georgia',serif;
  --ui: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;
}
[data-theme="light"]{--bg:#ffffff;--panel:#f4f4f6;--ink:#1a1a1d;--soft:#666;--line:#e3e3e8;--chip:#ececf2;--accent:#9a5b2e;--accent2:#2f6f55;--link:#8a4b1f;--shadow:rgba(0,0,0,.08);}
[data-theme="dark"]{--bg:#14161a;--panel:#1c2026;--ink:#e7e2d6;--soft:#9aa0aa;--line:#2a2f37;--accent:#e0a86b;--accent2:#7bc4a0;--chip:#262b33;--link:#e0a86b;--shadow:rgba(0,0,0,.4);}
*{box-sizing:border-box}
html,body{margin:0;padding:0}
body{background:var(--bg);color:var(--ink);font-family:var(--ui);line-height:1.6;-webkit-text-size-adjust:100%;}
a{color:var(--link);cursor:pointer;text-decoration:none}
a:hover{text-decoration:underline}
button{font-family:var(--ui);cursor:pointer;border:1px solid var(--line);background:var(--panel);color:var(--ink);border-radius:8px;padding:7px 12px;font-size:14px}
button:hover{border-color:var(--accent)}
button.primary{background:var(--accent);color:#fff;border-color:var(--accent)}
button.ghost{background:transparent}
.pill{display:inline-block;padding:1px 9px;border-radius:11px;background:var(--chip);color:var(--soft);font-size:.72rem;margin-right:5px;white-space:nowrap}
.pill.lvl{background:var(--accent2);color:#fff}

/* layout */
header{position:sticky;top:0;z-index:30;background:var(--bg);border-bottom:1px solid var(--line);
  display:flex;gap:8px;align-items:center;padding:8px 12px;flex-wrap:wrap}
header .title{font-weight:600;font-size:15px;margin-right:auto;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
#search{flex:1;min-width:140px;padding:8px 10px;border-radius:9px;border:1px solid var(--line);background:var(--panel);color:var(--ink);font-size:14px}
.iconbtn{padding:7px 10px}

.wrap{display:flex;max-width:1180px;margin:0 auto}
#drawer{width:330px;flex-shrink:0;border-right:1px solid var(--line);height:calc(100vh - 53px);position:sticky;top:53px;overflow:auto;padding:14px;background:var(--bg)}
#main{flex:1;min-width:0;padding:26px 22px 120px;}
.reader{max-width:72ch;margin:0 auto}
.reader h1{font-family:var(--read);font-size:2rem;line-height:1.2;margin:.1em 0 .1em}
.reader h1 .es{display:block;color:var(--soft);font-size:1.25rem;font-weight:400;font-style:italic}
.def{font-family:var(--read);font-size:1.16rem;line-height:1.72;margin:1em 0}
.def.es{color:var(--soft);font-size:1.04rem;border-top:1px dashed var(--line);padding-top:.8em}
.sec{margin:1.6em 0}
.sec h3{font-size:.78rem;text-transform:uppercase;letter-spacing:.07em;color:var(--soft);margin:.2em 0 .6em;font-family:var(--ui)}
.item{padding:9px 12px;border:1px solid var(--line);border-radius:10px;margin:7px 0;background:var(--panel)}
.item .nm{font-weight:600}
.bridge{font-family:var(--read);font-size:.97rem;margin-top:4px}
.bridge .es{color:var(--soft);display:block;font-size:.9rem}
.lineage{font-size:.92rem;line-height:2.1}
.lineage .step{display:inline-block;background:var(--chip);border-radius:8px;padding:2px 8px;margin:2px 3px}
.lineage .step.cur{background:var(--accent);color:#fff}
.note{width:100%;min-height:120px;border:1px solid var(--line);border-radius:10px;padding:11px;background:var(--panel);
  color:var(--ink);font-family:var(--read);font-size:1.02rem;line-height:1.55;resize:vertical}
.savednote{font-size:.8rem;color:var(--accent2);margin-top:4px}
.audiobar{margin:.6em 0}
.audiobar button{padding:6px 12px;margin-right:6px}
#autoBtn.on{background:var(--accent);color:#fff;border-color:var(--accent)}
#karaoke{display:none;margin:0 auto 18px;max-width:72ch;padding:14px 16px;background:var(--panel);
  border:1px solid var(--line);border-radius:12px;font-family:var(--read);font-size:1.3rem;line-height:2}
#karaoke.on{display:block}
#karaoke .kw{cursor:pointer;border-radius:6px;padding:0 2px;transition:none}
#karaoke .kw.cur{background:var(--accent);color:#fff}
#karaoke .kw.done{color:var(--soft)}
#karaoke .lead{font-size:.72rem;text-transform:uppercase;letter-spacing:.06em;color:var(--soft);
  font-family:var(--ui);display:block;margin-bottom:6px}
/* ---- home / cover ---- */
#home{max-width:1000px;margin:0 auto}
#home h1{font-family:var(--read);font-size:2rem;margin:.1em 0}
#home .sub{color:var(--soft);font-size:1.05rem;margin:.2em 0 1.2em;max-width:70ch}
.minimap{width:100%;max-width:760px;margin:0 auto 18px;display:block;background:var(--panel);
  border:1px solid var(--line);border-radius:14px}
.mm-dot{cursor:pointer}
.mm-label{font-family:var(--ui);font-weight:600;paint-order:stroke;stroke:var(--bg);stroke-width:3.5px;cursor:pointer}
.mm-here{fill:none;stroke:var(--ink);stroke-width:1.6}
.mm-here-txt{fill:var(--ink);font-family:var(--ui);font-weight:700}
.themes{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:12px}
.tcard{border:1px solid var(--line);border-radius:12px;padding:13px 14px;background:var(--panel);
  cursor:pointer;display:flex;flex-direction:column;gap:6px;transition:none}
.tcard:hover{border-color:var(--accent)}
.tcard .tt{font-weight:700;font-size:1.05rem;display:flex;align-items:center;gap:7px}
.tcard .sw{width:12px;height:12px;border-radius:3px;flex-shrink:0}
.tcard .tes{color:var(--soft);font-size:.85rem;font-style:italic}
.tcard .td{font-size:.9rem;line-height:1.45}
.tcard .pg{height:6px;background:var(--chip);border-radius:4px;overflow:hidden;margin-top:auto}
.tcard .pg i{display:block;height:100%;background:var(--accent2)}
.tcard .meta{font-size:.74rem;color:var(--soft);display:flex;justify-content:space-between}
.tcard.done{border-color:var(--accent2)}

/* drawer sections */
.dh{font-size:.74rem;text-transform:uppercase;letter-spacing:.06em;color:var(--soft);margin:14px 0 6px}
.res{padding:8px 10px;border-radius:9px;cursor:pointer;border:1px solid transparent}
.res:hover{background:var(--panel);border-color:var(--line)}
.res .meta{font-size:.74rem;color:var(--soft)}
.route{padding:9px 10px;border:1px solid var(--line);border-radius:10px;margin:6px 0;background:var(--panel)}
.route.active{border-color:var(--accent)}
.route .bar{height:6px;background:var(--chip);border-radius:4px;overflow:hidden;margin-top:6px}
.route .bar i{display:block;height:100%;background:var(--accent2)}
.lvlgroup{margin:2px 0 6px}
.lvlgroup summary{cursor:pointer;font-size:.84rem;color:var(--ink);padding:4px 0}

/* compass / bottom bar */
#compass{position:fixed;left:0;right:0;bottom:0;z-index:40;background:var(--panel);border-top:1px solid var(--line);
  box-shadow:0 -4px 14px var(--shadow);padding:8px 12px;display:none}
#compass .row{max-width:900px;margin:0 auto;display:flex;align-items:center;gap:10px}
#compass .lbl{flex:1;min-width:0;font-size:.86rem}
#compass .lbl b{display:block;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
#compass .bar{height:6px;background:var(--chip);border-radius:4px;overflow:hidden;margin-top:4px}
#compass .bar i{display:block;height:100%;background:var(--accent)}
.offbanner{background:var(--accent);color:#fff;border-radius:9px;padding:8px 12px;margin:0 0 14px;display:flex;
  gap:10px;align-items:center;flex-wrap:wrap}
.offbanner button{background:#fff;color:var(--accent);border:none}

.hidden{display:none!important}
.scrim{position:fixed;inset:0;background:rgba(0,0,0,.35);z-index:25;display:none}
@media(max-width:820px){
  #drawer{position:fixed;left:0;top:53px;z-index:28;box-shadow:4px 0 18px var(--shadow);transform:translateX(-105%);transition:transform .18s}
  #drawer.open{transform:none}
  .scrim.open{display:block}
  #main{padding:18px 15px 130px}
  .reader h1{font-size:1.65rem}
}
@media(min-width:821px){ #drawer.collapsed{display:none} }
@media print{header,#drawer,#compass,.note{display:none}}
</style>
</head>
<body>
<header>
  <button class="iconbtn ghost" id="menuBtn" title="Menú" aria-label="Menú">☰</button>
  <button class="iconbtn ghost" id="homeBtn" title="Inicio · mapa de temas">🏠</button>
  <span class="title">📡 Ruta de Aprendizaje · Teledetección Agrícola</span>
  <input id="search" placeholder="Buscar concepto / search…" autocomplete="off">
  <button class="iconbtn ghost" id="themeBtn" title="Tema">◐</button>
  <button class="iconbtn ghost" id="langBtn" title="Idioma de lectura">EN/ES</button>
  <button class="iconbtn ghost" id="autoBtn" title="Modo automático: lee en voz de lo básico a lo avanzado">▶🔊</button>
  <select id="modelSel" title="Modelo de voz (TTS)" style="padding:6px 8px;border-radius:8px;border:1px solid var(--line);background:var(--panel);color:var(--ink);font-size:13px"></select>
  <button class="iconbtn ghost" id="exportBtn" title="Guardar / exportar memoria">⬇</button>
  <button class="iconbtn ghost" id="importBtn" title="Cargar memoria">⬆</button>
  <input type="file" id="importFile" accept="application/json" class="hidden">
</header>

<div class="scrim" id="scrim"></div>
<div class="wrap">
  <aside id="drawer">
    <div id="searchResults"></div>
    <div id="routesPanel"></div>
    <div id="browse"></div>
  </aside>
  <main id="main"><div id="home" class="hidden"></div><div id="karaoke"></div><div class="reader" id="reader"></div></main>
</div>

<div id="compass"><div class="row">
  <button id="prevBtn" title="Anterior">◀ Ant.</button>
  <div class="lbl"><b id="compassLbl">—</b><div class="bar"><i id="compassBar"></i></div></div>
  <button id="returnBtn" class="ghost" title="Volver a mi ruta">🧭 Mi ruta</button>
  <button id="nextBtn" class="primary" title="Siguiente">Sig. ▶</button>
</div></div>
<audio id="player" preload="none"></audio>

<script>
const DATA = __DATA__;
/* ---------- graph model ---------- */
const byId = {}; DATA.nodes.forEach(n=>byId[n.id]=n);
const parents={}, children={}, related={};
DATA.nodes.forEach(n=>{parents[n.id]=[];children[n.id]=[];related[n.id]=[];});
DATA.prereq.forEach(([p,c,be,bs])=>{ if(byId[p]&&byId[c]){children[p].push({id:c,be,bs}); parents[c].push({id:p,be,bs});}});
DATA.rel.forEach(([a,b])=>{ if(byId[a]&&byId[b]){related[a].push(b); related[b].push(a);}});

/* full ancestor curriculum, ordered basic->advanced (the complete route to origin) */
function routeTo(target){
  const anc=new Set(); const stack=[target];
  while(stack.length){const x=stack.pop();
    for(const p of parents[x]||[]){ if(!anc.has(p.id)){anc.add(p.id);stack.push(p.id);} }}
  anc.add(target);
  return [...anc].sort((a,b)=> (byId[a].lvl-byId[b].lvl) || (byId[a].ord-byId[b].ord) || byId[a].en.localeCompare(byId[b].en));
}
/* direct lineage spine (longest single chain) for the breadcrumb */
function lineage(target){
  const path=[]; let cur=target, guard=0;
  while(cur && guard++<200){ path.push(cur);
    const ps=parents[cur]||[]; if(!ps.length) break;
    cur=ps.reduce((best,p)=> (byId[p.id].lvl>byId[best.id].lvl?p:best), ps[0]).id; }
  return path.reverse();
}

/* ---------- persistent state ---------- */
const KEY='handbook-learn-v1';
let S = load();
function load(){ try{return JSON.parse(localStorage.getItem(KEY))||{};}catch(e){return {};} }
function save(){ try{localStorage.setItem(KEY,JSON.stringify(S));}catch(e){} }
S.routes = S.routes || {};            // id -> {target, order:[ids], pos}
S.activeRoute = S.activeRoute || null;
S.notes = S.notes || {};              // id -> text
S.visited = S.visited || {};          // id -> true
S.theme = S.theme || 'paper';
S.lang = S.lang || 'both';            // both | en | es
S.model = S.model || (((DATA.meta.models||[])[0]||{}).id || 'xtts');   // TTS voice model
S.viewing = S.viewing || (DATA.nodes.find(n=>n.lvl===0)||DATA.nodes[0]).id;
document.documentElement.dataset.theme = S.theme==='paper'?'':S.theme;

/* ---------- helpers ---------- */
function esc(s){return (s||'').replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));}
function active(){ return S.activeRoute?S.routes[S.activeRoute]:null; }
function onRoute(){ const r=active(); return r && r.order[r.pos]===S.viewing; }

/* ---------- render reader ---------- */
function openConcept(id, fromRoute){
  if(!byId[id])return;
  S.viewing=id; save();
  const _k=document.getElementById('karaoke'); if(_k) _k.classList.remove('on');  /* reset karaoke */
  showReader();
  const n=byId[id];
  const r=active();
  const off = r && r.order[r.pos]!==id;
  let h='';
  if(off){
    h+=`<div class="offbanner">🧭 Estás explorando fuera de tu ruta.
        <button onclick="returnToRoute()">Volver al paso ${r.pos+1}</button>`;
    if(r.order.includes(id)) h+=`<button onclick="jumpRoutePos('${id}')">Continuar desde aquí</button>`;
    h+=`</div>`;
  }
  h+=`<h1>${esc(n.en)}<span class="es">${esc(n.es)}</span></h1>
      <div><span class="pill lvl">nivel ${n.lvl}</span><span class="pill">${esc(n.cat)}</span>
      ${n.kind==='primitive'?'<span class="pill">fundamento</span>':''}
      ${S.visited[id]?'<span class="pill">✓ leído</span>':''}</div>`;
  h+=`<div class="audiobar">🔊 <button onclick="playLang('en')">▶ Leer EN</button>
      <button onclick="playLang('es')">▶ Leer ES</button>
      <button onclick="toggleAuto()" class="ghost">▶ Modo automático</button></div>`;
  if(S.lang!=='es') h+=`<div class="def"><b>EN.</b> ${linkify(n.den,id)}</div>`;
  if(S.lang!=='en') h+=`<div class="def es"><b>ES.</b> ${linkify(n.des,id)}</div>`;
  if(n.src) h+=`<div class="pill">fuentes: ${esc(n.src)}</div>`;

  // lineage breadcrumb
  const lin=lineage(id);
  if(lin.length>1){
    h+=`<div class="sec"><h3>Linaje hasta el origen / Lineage</h3><div class="lineage">`+
       lin.map(x=>`<span class="step ${x===id?'cur':''}"><a onclick="openConcept('${x}')">${esc(byId[x].en)}</a></span>`)
          .join('<span style="color:var(--soft)"> → </span>')+`</div></div>`;
  }
  // prerequisites with bridges
  const ps=parents[id];
  if(ps.length){
    h+=`<div class="sec"><h3>Entiende esto primero / Prerequisites</h3>`;
    for(const p of ps){const m=byId[p.id];
      h+=`<div class="item"><div class="nm"><a onclick="openConcept('${p.id}')">${esc(m.en)}</a> · <span class="pill">${esc(m.cat)}</span></div>`;
      if(S.lang!=='es'&&p.be) h+=`<div class="bridge">${esc(p.be)}</div>`;
      if(S.lang!=='en'&&p.bs) h+=`<div class="bridge"><span class="es">${esc(p.bs)}</span></div>`;
      h+=`</div>`;}
    h+=`</div>`;
  }
  // unlocks
  const cs=children[id];
  if(cs.length){
    h+=`<div class="sec"><h3>Esto habilita / This unlocks</h3>`+
       cs.slice(0,30).map(c=>`<span class="pill" style="cursor:pointer" onclick="openConcept('${c.id}')">${esc(byId[c.id].en)}</span>`).join(' ')+`</div>`;
  }
  // related lateral
  const rl=related[id];
  if(rl.length){
    h+=`<div class="sec"><h3>Relacionados / Related</h3>`+
       rl.slice(0,20).map(x=>`<span class="pill" style="cursor:pointer" onclick="openConcept('${x}')">${esc(byId[x].en)}</span>`).join(' ')+`</div>`;
  }
  // actions
  h+=`<div class="sec">
      <button class="primary" onclick="setTarget('${id}')">🎯 Trazar mi ruta hasta aquí</button>
      <button onclick="toggleRead('${id}')">${S.visited[id]?'Marcar no leído':'✓ Marcar leído'}</button>
      </div>`;
  // notes
  h+=`<div class="sec"><h3>Mis notas / My notes</h3>
      <textarea class="note" id="noteBox" placeholder="Escribe notas sobre este tema… se guardan en tu dispositivo.">${esc(S.notes[id]||'')}</textarea>
      <div class="savednote" id="noteSaved"></div></div>`;
  document.getElementById('reader').innerHTML=h;
  document.getElementById('main').scrollTop=0; window.scrollTo(0,0);
  const nb=document.getElementById('noteBox');
  nb.addEventListener('input',()=>{S.notes[id]=nb.value;save();
    document.getElementById('noteSaved').textContent='guardado ✓';});
  renderCompass(); renderRoutes();
  closeDrawer();
}

/* link concept names inside a definition (first mention each) */
let LINKER=null;
function buildLinker(){
  const surfaces=[];
  DATA.nodes.forEach(n=>{ if(n.en.length>=4) surfaces.push([n.en,n.id]); if(n.es.length>=4) surfaces.push([n.es,n.id]); });
  surfaces.sort((a,b)=>b[0].length-a[0].length);
  const map={}; surfaces.forEach(([s,id])=>{const k=s.toLowerCase(); if(!(k in map))map[k]=id;});
  const alt=surfaces.map(([s])=>s.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')).join('|');
  LINKER={re:new RegExp('(?<![\\w])(?:'+alt+')(?![\\w])','gi'),map};
}
function linkify(text,selfId){
  try{
    if(!LINKER)buildLinker();
    const used=new Set([selfId]);
    return esc(text).replace(LINKER.re,m=>{const id=LINKER.map[m.toLowerCase()];
      if(!id||used.has(id))return m; used.add(id); return `<a onclick="openConcept('${id}')">${m}</a>`;});
  }catch(e){ return esc(text); }   /* old browsers (e.g. Kindle) may lack lookbehind */
}

/* ---------- routes ---------- */
function setTarget(id){
  const order=routeTo(id);
  S.routes[id]={target:id, order, pos:0};
  S.activeRoute=id; save();
  openConcept(order[0]); renderRoutes(); renderCompass();
}
function returnToRoute(){ const r=active(); if(r) openConcept(r.order[r.pos]); }
function jumpRoutePos(id){ const r=active(); if(!r)return; const i=r.order.indexOf(id); if(i>=0){r.pos=i;save();openConcept(id);} }
function step(d){ const r=active(); if(!r)return;
  if(d>0) S.visited[r.order[r.pos]]=true;
  r.pos=Math.max(0,Math.min(r.order.length-1,r.pos+d)); save(); openConcept(r.order[r.pos]); }
function toggleRead(id){ S.visited[id]=!S.visited[id]; save(); openConcept(id); }
function deleteRoute(id){ delete S.routes[id]; if(S.activeRoute===id)S.activeRoute=Object.keys(S.routes)[0]||null; save(); renderRoutes(); renderCompass(); }
function selectRoute(id){ S.activeRoute=id; save(); openConcept(S.routes[id].order[S.routes[id].pos]); }

function renderCompass(){
  const r=active(); const c=document.getElementById('compass');
  if(!r){c.style.display='none';return;}
  c.style.display='block';
  const cur=byId[r.order[r.pos]];
  const done=r.order.filter(x=>S.visited[x]).length;
  document.getElementById('compassLbl').textContent=`Paso ${r.pos+1}/${r.order.length} · ${cur.en}  (${done} leídos)`;
  document.getElementById('compassBar').style.width=(100*(r.pos+1)/r.order.length)+'%';
  document.getElementById('returnBtn').style.display=onRoute()?'none':'';
}

/* ---------- drawer: search / routes / browse ---------- */
function renderRoutes(){
  const el=document.getElementById('routesPanel'); const ids=Object.keys(S.routes);
  let h=`<div class="dh">Mis rutas (${ids.length})</div>`;
  if(!ids.length) h+=`<div class="res meta">Elige un concepto y pulsa “Trazar mi ruta”.</div>`;
  ids.forEach(id=>{const r=S.routes[id];const done=r.order.filter(x=>S.visited[x]).length;
    const label = id==='__all__' ? 'Recorrido completo (todo el árbol)'
      : id.indexOf('theme:')===0 ? esc((cluById[+id.slice(6)]||{title:{en:'Tema'}}).title.en)
      : esc(byId[id] ? byId[id].en : id);
    h+=`<div class="route ${S.activeRoute===id?'active':''}">
      <div><a onclick="selectRoute('${id}')"><b>${label}</b></a></div>
      <div class="meta" style="font-size:.74rem;color:var(--soft)">${done}/${r.order.length} · paso ${r.pos+1}
        <a onclick="deleteRoute('${id}')" style="float:right">borrar</a></div>
      <div class="bar"><i style="width:${100*done/r.order.length}%"></i></div></div>`;});
  el.innerHTML=h;
}
function renderBrowse(){
  const byLvl={}; DATA.nodes.forEach(n=>{(byLvl[n.lvl]=byLvl[n.lvl]||[]).push(n);});
  let h=`<div class="dh">Explorar de lo básico a lo avanzado</div>`;
  Object.keys(byLvl).map(Number).sort((a,b)=>a-b).forEach(l=>{
    const arr=byLvl[l].slice().sort((a,b)=>a.en.localeCompare(b.en));
    h+=`<details class="lvlgroup" ${l<=1?'open':''}><summary>Nivel ${l} · ${arr.length} conceptos</summary>`;
    arr.forEach(n=>{h+=`<div class="res" onclick="openConcept('${n.id}')">${esc(n.en)} <span class="meta">${esc(n.cat)}</span></div>`;});
    h+=`</details>`;});
  document.getElementById('browse').innerHTML=h;
}
function doSearch(q){
  const el=document.getElementById('searchResults');
  q=q.trim().toLowerCase();
  if(!q){el.innerHTML='';document.getElementById('browse').style.display='';return;}
  document.getElementById('browse').style.display='none';
  const hits=DATA.nodes.filter(n=>n.al.includes(q)).slice(0,40)
    .sort((a,b)=>a.lvl-b.lvl);
  el.innerHTML=`<div class="dh">${hits.length} resultados</div>`+
    hits.map(n=>`<div class="res" onclick="openConcept('${n.id}')"><b>${esc(n.en)}</b> — ${esc(n.es)}
      <div class="meta">nivel ${n.lvl} · ${esc(n.cat)}</div></div>`).join('');
}

/* ---------- export / import ---------- */
function download(name,text,type){
  const b=new Blob([text],{type:type||'application/json'});
  const u=URL.createObjectURL(b);const a=document.createElement('a');
  a.href=u;a.download=name;a.click();URL.revokeObjectURL(u);
}
function exportMemory(){
  const mem={app:'handbook-learn',version:1,exported:new Date().toISOString(),
    theme:S.theme,lang:S.lang,activeRoute:S.activeRoute,
    routes:S.routes,visited:S.visited,notes:S.notes};
  download('mi-aprendizaje.json',JSON.stringify(mem,null,2));
  exportNotesForChatbot();
}
function exportNotesForChatbot(){
  const ids=Object.keys(S.notes).filter(id=>S.notes[id]&&S.notes[id].trim()&&byId[id]);
  if(!ids.length)return;
  let md=`# Mis notas de aprendizaje — Teledetección para Estadísticas Agrícolas\n`+
         `_Cada nota incluye el linaje del concepto para dar contexto a un asistente._\n\n`;
  ids.forEach(id=>{const n=byId[id];const lin=lineage(id).map(x=>byId[x].en).join(' → ');
    md+=`## ${n.en} / ${n.es}\n`+
        `- **Linaje:** ${lin}\n`+
        `- **Nivel:** ${n.lvl} · **Categoría:** ${n.cat}\n`+
        `- **Definición (EN):** ${n.den}\n`+
        `- **Definición (ES):** ${n.des}\n`+
        (n.src?`- **Fuentes:** ${n.src}\n`:``)+
        `- **Prerrequisitos:** ${(parents[id]||[]).map(p=>byId[p.id].en).join(', ')||'—'}\n\n`+
        `**Mi nota:**\n${S.notes[id]}\n\n---\n\n`;});
  download('mis-notas-con-linaje.md',md,'text/markdown');
}
function importMemory(file){
  const fr=new FileReader();
  fr.onload=()=>{try{const m=JSON.parse(fr.result);
    S.routes=m.routes||S.routes; S.notes=Object.assign(S.notes,m.notes||{});
    S.visited=Object.assign(S.visited,m.visited||{}); S.activeRoute=m.activeRoute||S.activeRoute;
    if(m.theme)S.theme=m.theme; if(m.lang)S.lang=m.lang;
    document.documentElement.dataset.theme=S.theme==='paper'?'':S.theme; save();
    renderRoutes();renderCompass();openConcept(S.viewing);
    alert('Memoria de aprendizaje cargada ✓');
  }catch(e){alert('Archivo no válido');}};
  fr.readAsText(file);
}

/* ---------- chrome ---------- */
function openDrawer(){document.getElementById('drawer').classList.add('open');document.getElementById('scrim').classList.add('open');}
function closeDrawer(){document.getElementById('drawer').classList.remove('open');document.getElementById('scrim').classList.remove('open');}
const THEMES=['paper','light','dark'];
document.getElementById('themeBtn').onclick=()=>{S.theme=THEMES[(THEMES.indexOf(S.theme)+1)%THEMES.length];
  document.documentElement.dataset.theme=S.theme==='paper'?'':S.theme;save();};
document.getElementById('langBtn').onclick=()=>{const m=['both','en','es'];S.lang=m[(m.indexOf(S.lang)+1)%3];save();openConcept(S.viewing);
  document.getElementById('langBtn').textContent={both:'EN/ES',en:'EN',es:'ES'}[S.lang];};
document.getElementById('menuBtn').onclick=()=>{const d=document.getElementById('drawer');
  if(window.innerWidth>820){ d.classList.toggle('collapsed'); }   /* desktop: collapse sidebar */
  else { d.classList.contains('open')?closeDrawer():openDrawer(); } /* mobile: slide-in overlay */
};
document.getElementById('scrim').onclick=closeDrawer;
document.getElementById('search').addEventListener('input',e=>doSearch(e.target.value));
document.getElementById('prevBtn').onclick=()=>step(-1);
document.getElementById('nextBtn').onclick=()=>step(1);
document.getElementById('returnBtn').onclick=returnToRoute;
document.getElementById('exportBtn').onclick=exportMemory;
document.getElementById('importBtn').onclick=()=>document.getElementById('importFile').click();
document.getElementById('importFile').onchange=e=>{if(e.target.files[0])importMemory(e.target.files[0]);};
document.addEventListener('keydown',e=>{ if(e.target.tagName==='TEXTAREA'||e.target.tagName==='INPUT')return;
  if(e.key==='ArrowRight')step(1); if(e.key==='ArrowLeft')step(-1); });

/* ---------- audio + auto mode ---------- */
let autoOn=false;
const player=document.getElementById('player');
function audioLang(){ return S.lang==='es'?'es':'en'; }   /* default language for auto */

/* karaoke: split total audio time across words (weighted by length) and highlight */
let kWords=[], kWeights=[], kTotal=0, kStarts=[], kEnds=[];
const kBox=document.getElementById('karaoke');
function setupKaraoke(text, lang){
  kWords=text.trim().split(/\s+/);
  kWeights=kWords.map(w=>Math.max(1, (w.match(/[\p{L}\p{N}]/gu)||[]).length) + 1);
  kTotal=kWeights.reduce((a,b)=>a+b,0); kStarts=[]; kEnds=[];
  kBox.innerHTML=`<span class="lead">🔊 ${lang==='es'?'Lectura en español':'Reading in English'} — `+
    `karaoke (clic en una palabra para saltar)</span>`+
    kWords.map((w,i)=>`<span class="kw" data-i="${i}" onclick="seekWord(${i})">${esc(w)}</span>`).join(' ');
  kBox.classList.add('on');
}
function computeKaraokeTimings(){
  const dur=player.duration; if(!dur||!isFinite(dur))return;
  let acc=0; kStarts=[]; kEnds=[];
  for(let i=0;i<kWords.length;i++){ kStarts.push(acc/kTotal*dur); acc+=kWeights[i]; kEnds.push(acc/kTotal*dur); }
}
function highlightKaraoke(){
  if(!kStarts.length)return; const t=player.currentTime; let idx=kWords.length-1;
  for(let i=0;i<kStarts.length;i++){ if(t<kEnds[i]){ idx=i; break; } }
  const kids=kBox.getElementsByClassName('kw');
  for(let i=0;i<kids.length;i++) kids[i].className='kw'+(i===idx?' cur':(i<idx?' done':''));
}
function seekWord(i){ if(kStarts[i]!=null){ player.currentTime=kStarts[i]+0.01; player.play().catch(()=>{}); } }

function playLang(lang){
  const n=byId[S.viewing];
  setupKaraoke(lang==='es' ? (n.es+'. '+n.des) : (n.en+'. '+n.den), lang);
  player.src='audio/'+S.model+'/'+S.viewing+'_'+lang+'.mp3'; player.currentTime=0;
  player.play().catch(()=>{});
}
function setAutoBtn(){ const b=document.getElementById('autoBtn');
  b.textContent=autoOn?'⏸🔊':'▶🔊'; b.classList.toggle('on',autoOn); }
function buildGlobalOrder(){ return DATA.nodes.map(n=>n.id)
  .sort((a,b)=>(byId[a].lvl-byId[b].lvl)||(byId[a].ord-byId[b].ord)); }
function toggleAuto(){
  autoOn=!autoOn;
  if(autoOn){
    let r=active();
    if(!r){ const order=buildGlobalOrder();              /* no route -> traverse whole tree */
      S.routes['__all__']={target:order[order.length-1],order,pos:0,global:true};
      S.activeRoute='__all__'; r=S.routes['__all__']; }
    r.pos=0; save();                                     /* start at the most basic concept */
    openConcept(r.order[0]); renderCompass(); playLang(audioLang());
  } else { player.pause(); }
  setAutoBtn();
}
function autoAdvance(){
  if(!autoOn)return; const r=active(); if(!r){autoOn=false;setAutoBtn();return;}
  if(r.pos<r.order.length-1){ S.visited[r.order[r.pos]]=true; r.pos++; save();
    openConcept(r.order[r.pos]); renderCompass(); playLang(audioLang()); }
  else { autoOn=false; setAutoBtn(); }
}
player.onended=autoAdvance;
player.onerror=()=>{ if(autoOn) setTimeout(autoAdvance,150); };  /* skip a missing clip */
player.onloadedmetadata=computeKaraokeTimings;
player.ontimeupdate=highlightKaraoke;
document.getElementById('autoBtn').onclick=toggleAuto;
(function initModels(){
  const sel=document.getElementById('modelSel'); const M=DATA.meta.models||[];
  if(!M.length){ sel.style.display='none'; return; }
  if(!S.modelSet){ S.model=M[0].id; S.modelSet=true; save(); }   /* default to XTTS once */
  else if(!M.find(m=>m.id===S.model)) S.model=M[0].id;
  sel.innerHTML=M.map(m=>`<option value="${m.id}">🔊 ${m.label}</option>`).join('');
  sel.value=S.model; sel.onchange=()=>{ S.model=sel.value; save(); player.pause(); };
})();

/* ---------- home / themes / minimap ---------- */
const CLUSTERS = DATA.clusters || [];
const NODE_XY = DATA.node_xy || {};
const NODE_CLUSTER = DATA.node_cluster || {};
const cluById = {}; CLUSTERS.forEach(c => cluById[c.idx] = c);

function themeProgress(c){
  const v = c.members.filter(id => S.visited[id]).length;
  return {v, total: c.members.length, pct: c.members.length ? Math.round(100*v/c.members.length) : 0};
}
function startTheme(idx){
  const c = cluById[idx]; if(!c) return;
  const order = c.members.filter(id => byId[id])
    .sort((a,b) => (byId[a].lvl-byId[b].lvl) || (byId[a].ord-byId[b].ord));
  S.routes['theme:'+idx] = {target: c.entry, order, pos: 0, theme: idx}; S.activeRoute = 'theme:'+idx;
  save(); openConcept(order[0]); renderCompass();
}
function minimapSVG(curId){
  const W=760,H=460,P=26, sx=x=>P+x*(W-2*P), sy=y=>P+(1-y)*(H-2*P);
  let dots='';
  for(const id in NODE_XY){ const p=NODE_XY[id]; const c=cluById[NODE_CLUSTER[id]];
    dots+=`<circle class="mm-dot" cx="${sx(p[0]).toFixed(1)}" cy="${sy(p[1]).toFixed(1)}" r="3"
      fill="${c?c.color:'#888'}" opacity="${S.visited[id]?0.95:0.45}"
      onclick="openConcept('${id}')"><title>${esc(byId[id].en)}</title></circle>`; }
  let labels='';
  CLUSTERS.forEach(c=>{ labels+=`<text class="mm-label" x="${sx(c.cx).toFixed(1)}" y="${sy(c.cy).toFixed(1)}"
    fill="${c.color}" font-size="12.5" text-anchor="middle" onclick="startTheme(${c.idx})">${esc(c.title.en)}</text>`; });
  let here='';
  if(curId && NODE_XY[curId]){ const p=NODE_XY[curId];
    here=`<circle class="mm-here" cx="${sx(p[0]).toFixed(1)}" cy="${sy(p[1]).toFixed(1)}" r="9"/>
      <text class="mm-here-txt" x="${sx(p[0]).toFixed(1)}" y="${(sy(p[1])-12).toFixed(1)}" text-anchor="middle" font-size="10">● estás aquí</text>`; }
  return `<svg class="minimap" viewBox="0 0 ${W} ${H}">${dots}${labels}${here}</svg>`;
}
function renderHome(){
  const cur = S.viewing;
  let h=`<h1>🛰️ Universo de aprendizaje</h1>
    <p class="sub">Teledetección para estadísticas agrícolas — <b>${DATA.nodes.length}</b> conceptos
    en <b>${CLUSTERS.length}</b> temas. Elige una ruta para empezar o explora el mapa (haz clic en un punto
    o en el nombre de un tema). El glosario lateral sigue disponible. El círculo marca <b>dónde te quedaste</b>.</p>`;
  h += minimapSVG(cur);
  h += `<div class="themes">`;
  CLUSTERS.forEach(c=>{ const p=themeProgress(c);
    h+=`<div class="tcard ${p.pct===100?'done':''}" onclick="startTheme(${c.idx})">
      <div class="tt"><span class="sw" style="background:${c.color}"></span>${esc(c.title.en)} ${p.pct===100?'✓':''}</div>
      <div class="tes">${esc(c.title.es)}</div>
      <div class="td">${esc(c.desc.es||c.desc.en)}</div>
      <div class="pg"><i style="width:${p.pct}%"></i></div>
      <div class="meta"><span>${p.v}/${p.total} vistos</span><span>Comenzar →</span></div></div>`; });
  h += `</div>`;
  document.getElementById('home').innerHTML = h;
}
function showHome(){ renderHome();
  document.getElementById('home').classList.remove('hidden');
  document.getElementById('reader').classList.add('hidden');
  document.getElementById('karaoke').classList.remove('on');
  window.scrollTo(0,0); closeDrawer(); }
function showReader(){
  document.getElementById('home').classList.add('hidden');
  document.getElementById('reader').classList.remove('hidden'); }
document.getElementById('homeBtn').onclick = showHome;

/* ---------- boot ---------- */
document.getElementById('langBtn').textContent={both:'EN/ES',en:'EN',es:'ES'}[S.lang];
renderBrowse(); renderRoutes(); setAutoBtn(); openConcept(S.viewing); showHome();
</script>
</body>
</html>
"""

if __name__ == "__main__":
    run()
