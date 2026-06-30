# deep_detailed.md — Guía de construcción para un agente externo

> **Para quién es esto.** Un agente autónomo de código que solo dispone de: (1) una **API key de OpenRouter** y (2) capacidad de escribir/ejecutar código (pip, bash, archivos). Nada más — **no hay Ollama, ni servidor previo, ni el código de Mentorium**. Esta guía te lleva a **construir desde cero** una "base de conocimiento por agente" (deep research + RAG con citas exactas), con código completo y copiable.
>
> **Lo construí yo** (este sistema corre en producción en otro proyecto). Aquí está el patrón probado, **adaptado a que solo tengas OpenRouter**: sustituyo Ollama por embeddings locales `fastembed` (pip puro, sin servidor) y el motor pesado GPT Researcher por un **loop de research propio** más robusto y fácil de depurar. Todo lo demás (FAISS + DuckDB/BM25 + FlashRank + búsqueda híbrida + citas a nivel chunk) se conserva tal cual, porque es lo que da la calidad.

---

## 0. Qué vas a construir

Un módulo `deepkb/` que hace dos cosas:

1. **`build`** — dado un *tema* y unos *topics*, investiga la web (LLM genera sub-preguntas → busca → scrapea → sintetiza), guarda fuentes en Markdown, y las **indexa** (embeddings + FAISS + BM25).
2. **`query`** — responde preguntas sobre ese tema devolviendo **pasajes con cita exacta** (texto, URL, título, score de relevancia), listos para inyectar a un LLM o mostrar al usuario.

```
TEMA + topics ──► [research: LLM + búsqueda web + scraping] ──► output/<tema>/sources/*.md
                                                                        │
                                                                        ▼
                                              [ingest: chunk + embed + FAISS + BM25] ──► data/<tema>/
                                                                        │
                                          query "..." ──► [BM25 + vector + rerank] ──► pasajes citados
```

**Filosofía no negociable:** dos etapas desacopladas que se comunican **por archivos** (`sources/*.md` + `metadata.json`). El research no sabe del índice; el índice no sabe del research. Esto te deja reconstruir, auditar o reemplazar cada mitad sin tocar la otra.

---

## 1. Restricciones y decisiones de stack (porque solo tienes OpenRouter)

| Necesidad | En el sistema original | **Tu versión (solo OpenRouter + pip)** | Por qué |
|---|---|---|---|
| LLM (research) | OpenRouter | **OpenRouter** (igual) | ya lo tienes |
| Deep research | GPT Researcher (pesado) | **loop propio** (sub-queries → search → scrape → synth) | sin dependencia frágil; controlas cada paso |
| Búsqueda web | Brave/DDG | **DuckDuckGo** (`ddgs`, sin key) | gratis, sin API extra |
| Scraping | Trafilatura | **Trafilatura** (igual) | HTML→Markdown limpio |
| **Embeddings** | **Ollama (servidor local)** | **`fastembed` (pip, ONNX, local, sin servidor)** | no tienes Ollama; fastembed es self-contained |
| Vector store | FAISS | **FAISS** (igual) | |
| BM25 + storage | DuckDB FTS | **DuckDB FTS** (igual) | un archivo, embebido |
| Reranker | FlashRank | **FlashRank** (igual) | cross-encoder ligero (ONNX) |

> **Embeddings sin Ollama:** `fastembed` baja un modelo ONNX multilingüe (`intfloat/multilingual-e5-large`, **1024 dims**, bueno en español) la primera vez y corre 100% local con pip — sin servidor, sin API. Es la pieza que reemplaza a Ollama y hace que "solo OpenRouter" sea suficiente.
>
> *Alternativa si prefieres no embeber un modelo:* OpenRouter también ofrece embeddings (`POST /api/v1/embeddings`, p.ej. `qwen/qwen3-embedding-8b`, 4096 dims). Te dejo esa variante en §6. Por defecto usa **fastembed** (más simple y sin costo por token).

**Solo el LLM de research cuesta dinero (OpenRouter).** Todo lo demás es local y gratis. Costo medido en el sistema real: **~$0.03 USD por base de conocimiento** de ~50 fuentes usando un modelo barato de contexto largo.

---

## 2. Estructura del proyecto (créala así)

```
deepkb/
├── requirements.txt
├── .env                      # OPENROUTER_API_KEY=...
├── config/
│   └── <tema>.yaml           # qué investigar + cómo indexar (un archivo por tema)
├── output/<tema>/            # (generado) sources/*.md + metadata.json + snapshots/
├── data/<tema>/              # (generado) brain.duckdb + brain.faiss
└── src/
    ├── __init__.py
    ├── llm.py                # cliente OpenRouter (OpenAI-compatible)
    ├── search.py             # búsqueda DDG + scraping Trafilatura
    ├── research.py           # loop de deep research (construye el corpus)
    ├── chunker.py            # chunking semántico con offsets de carácter
    ├── embedder.py           # fastembed (o OpenRouter embeddings)
    ├── indexer.py            # DuckDB (chunks+BM25) + FAISS + dedup por hash
    ├── retriever.py          # búsqueda híbrida BM25+vector+rerank
    └── cli.py                # `build` y `query`
```

Añade a `.gitignore`: `.env`, `.venv/`, `data/`, `output/`, `__pycache__/`. Los índices se **regeneran**, no se commitean.

---

## 3. Instalación

`requirements.txt`:
```
openai>=1.40            # cliente OpenRouter (OpenAI-compatible)
fastembed>=0.3          # embeddings locales (ONNX, sin servidor)
faiss-cpu>=1.8          # índice vectorial
duckdb>=1.0             # storage + BM25 (FTS)
flashrank>=0.2          # reranker cross-encoder
ddgs>=9.0               # búsqueda DuckDuckGo (sin API key)
trafilatura>=1.12       # scraping HTML→Markdown
pyyaml>=6.0
python-dotenv>=1.0
numpy>=1.26
```

```bash
mkdir -p deepkb/src deepkb/config && cd deepkb
python3.12 -m venv .venv && source .venv/bin/activate   # fija Python 3.12 (wheels estables)
pip install -r requirements.txt
# Linux/Docker: instala libgomp1 para FAISS  →  apt-get install -y libgomp1
echo "OPENROUTER_API_KEY=sk-or-tu-clave" > .env
```

> **Gotchas de instalación** (cuestan tiempo si no los sabes): fija **una** versión de Python (3.12); en Linux/Docker instala **`libgomp1`** o FAISS no carga; `fastembed` baja el modelo ONNX en el primer uso (necesita red esa vez).

---

## 4. Config del tema — `config/<tema>.yaml`

Un solo archivo define **qué investigar** y **cómo indexar**:
```yaml
tema: financiamiento_pyme
name: "Financiamiento y acceso a capital para PyMEs (México/Bajío)"
topics:                                   # el LLM hará deep research sobre cada uno
  - "financiamiento PyME México 2026 NAFIN FIRA banca de desarrollo requisitos"
  - "fondos y apoyos de gobierno para empresas Bajío Guanajuato 2026"
  - "deuda bancaria vs capital privado para PyME cómo elegir"
search:
  results_per_topic: 8                    # cuántas fuentes web por topic
embedding_model: "intfloat/multilingual-e5-large"   # fastembed; 1024 dims
embedding_dimensions: 1024                # DEBE coincidir con el modelo
chunk_size_words: 400
chunk_overlap_sentences: 1
reranker_model: "ms-marco-MiniLM-L-12-v2"
top_k_default: 5
research_model: "deepseek/deepseek-chat"  # modelo OpenRouter barato y capaz para síntesis
```

---

## 5. Código — `src/llm.py` (cliente OpenRouter)

```python
import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

_client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
)

def chat(model: str, system: str, user: str, temperature: float = 0.3,
         max_tokens: int = 2000, retries: int = 3) -> str:
    """Llamada con reintentos (OpenRouter a veces da 429/5xx)."""
    import time
    for i in range(retries):
        try:
            r = _client.chat.completions.create(
                model=model, temperature=temperature, max_tokens=max_tokens,
                messages=[{"role": "system", "content": system},
                          {"role": "user", "content": user}],
            )
            return r.choices[0].message.content or ""
        except Exception as e:
            if i == retries - 1:
                raise
            time.sleep(2 ** i)   # backoff exponencial: 1s, 2s, 4s
```

> **Lección que costó 120 sesiones aprenderla:** SIEMPRE envuelve las llamadas LLM con retry + backoff. Las APIs externas dan 429/503 bajo carga. Sin esto, un build de research falla a la mitad.

---

## 6. Código — `src/embedder.py` (fastembed; sin servidor)

```python
import numpy as np
from functools import lru_cache
from fastembed import TextEmbedding

@lru_cache(maxsize=4)
def _model(name: str) -> TextEmbedding:
    return TextEmbedding(model_name=name)   # baja el ONNX la 1a vez, luego cachea

def embed_texts(texts: list[str], model: str) -> np.ndarray:
    """Devuelve matriz (N, dims) float32, L2-normalizada (para coseno con IndexFlatIP)."""
    vecs = np.array(list(_model(model).embed(texts)), dtype=np.float32)
    norms = np.linalg.norm(vecs, axis=1, keepdims=True)
    return vecs / np.clip(norms, 1e-9, None)
```

> **Variante OpenRouter** (si NO quieres modelo local): reemplaza `_model().embed()` por `POST https://openrouter.ai/api/v1/embeddings` con `model="qwen/qwen3-embedding-8b"` y pon `embedding_dimensions: 4096` en el YAML. Mismo contrato de salida (matriz normalizada).
>
> ⚠️ **`embedding_dimensions` DEBE coincidir con el modelo.** Y si cambias de modelo de embeddings, **reindexa todo** — el espacio vectorial cambia.

---

## 7. Código — `src/search.py` (búsqueda + scraping)

```python
import hashlib, re
from pathlib import Path
from datetime import datetime, timezone
from ddgs import DDGS
import trafilatura

def search_web(query: str, max_results: int = 8) -> list[dict]:
    """DuckDuckGo, sin API key. Devuelve [{title, url, body}]."""
    try:
        return list(DDGS().text(query, max_results=max_results))
    except Exception:
        return []

def _slug(url: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", url.lower().split("//")[-1])[:80].strip("-")
    return s or hashlib.sha1(url.encode()).hexdigest()[:16]

def scrape(url: str) -> dict | None:
    """Descarga + limpia a Markdown. None si falla / vacío."""
    html = trafilatura.fetch_url(url)
    if not html:
        return None
    md = trafilatura.extract(html, output_format="markdown",
                             include_tables=True, with_metadata=True)
    if not md or len(md) < 200:           # descarta páginas vacías / anti-bot
        return None
    meta = trafilatura.extract_metadata(html)
    return {"url": url, "markdown": md,
            "title": (meta.title if meta else None) or url,
            "sha256": hashlib.sha256(md.encode()).hexdigest()}
```

---

## 8. Código — `src/research.py` (deep research loop)

Reemplaza a GPT Researcher con un loop transparente: el LLM genera sub-preguntas, buscas/scrapeas cada una, el LLM redacta una síntesis. **Persistes tanto las fuentes crudas como la síntesis** — ambas se indexan.

```python
import json
from pathlib import Path
from datetime import datetime, timezone
from . import llm, search

def _subqueries(topic: str, model: str) -> list[str]:
    raw = llm.chat(model,
        "Eres un investigador. Devuelve SOLO un array JSON de 3-5 sub-preguntas de búsqueda.",
        f"Tema: {topic}\nGenera sub-preguntas específicas y complementarias.",
        max_tokens=400)
    try:
        return json.loads(raw[raw.index("["): raw.rindex("]") + 1])[:5]
    except Exception:
        return [topic]

def research_topic(topic: str, out_dir: Path, model: str, per_q: int = 6) -> list[dict]:
    """Investiga un topic. Escribe sources/*.md + síntesis. Devuelve metadata nueva."""
    sources_dir = out_dir / "sources"; sources_dir.mkdir(parents=True, exist_ok=True)
    meta_path = out_dir / "metadata.json"
    meta = json.loads(meta_path.read_text()) if meta_path.exists() else []
    seen = {m["sha256"] for m in meta}
    collected = []

    for q in _subqueries(topic, model):
        for r in search.search_web(q, per_q):
            doc = search.scrape(r["url"])
            if not doc or doc["sha256"] in seen:
                continue
            seen.add(doc["sha256"])
            slug = search._slug(doc["url"])
            f = sources_dir / f"{slug}.md"
            f.write_text(f"# {doc['title']}\n\nURL: {doc['url']}\n\n---\n\n{doc['markdown']}")
            entry = {"url": doc["url"], "title": doc["title"], "sha256": doc["sha256"],
                     "filename": str(f), "date_scraped": datetime.now(timezone.utc).isoformat()}
            meta.append(entry); collected.append(entry)

    # Síntesis del LLM sobre lo recolectado (también se indexa)
    if collected:
        ctx = "\n\n".join(f"[{c['title']}]\n{Path(c['filename']).read_text()[:1500]}"
                          for c in collected[:8])
        synth = llm.chat(model,
            "Sintetiza los hallazgos en un informe estructurado en español, con secciones y datos concretos.",
            f"Tema: {topic}\n\nFuentes:\n{ctx}", max_tokens=2500)
        ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        sf = sources_dir / f"research_{ts}.md"
        sf.write_text(f"# Investigación: {topic}\n\n---\n\n{synth}")
        meta.append({"url": f"synthesis://{topic}", "title": f"Síntesis: {topic}",
                     "sha256": __import__('hashlib').sha256(synth.encode()).hexdigest(),
                     "filename": str(sf), "date_scraped": datetime.now(timezone.utc).isoformat()})

    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2))
    return collected
```

> **Idempotencia desde el día 1:** deduplica por `sha256` del contenido. Re-correr el build no re-scrapea ni re-sintetiza lo idéntico.

---

## 9. Código — `src/chunker.py` (chunks con offsets de carácter)

Las **citas exactas** dependen de guardar `char_start`/`char_end` por chunk.

```python
import re

def chunk_document(text: str, source_file: str, source_url: str, title: str,
                   target_words: int = 400, overlap_sentences: int = 1) -> list[dict]:
    # párrafos con offsets reales
    paras, pos = [], 0
    for block in re.split(r"\n\s*\n", text):
        start = text.find(block, pos); pos = start + len(block)
        if len(block.split()) >= 5:
            paras.append((block.strip(), start, start + len(block)))

    chunks, buf, wc, c_start = [], [], 0, None
    def flush(c_end):
        nonlocal buf, wc, c_start
        if not buf: return
        body = " ".join(p for p, _, _ in buf)
        # solapamiento: últimas N frases del chunk previo
        prefix = ""
        if chunks and overlap_sentences:
            sents = re.split(r"(?<=[.!?])\s+", chunks[-1]["text"])
            prefix = " ".join(sents[-overlap_sentences:]) + " "
        chunks.append({"source_file": source_file, "source_url": source_url, "title": title,
                       "chunk_index": len(chunks), "char_start": buf[0][1], "char_end": c_end,
                       "text": prefix + body})
        buf, wc, c_start = [], 0, None

    for p, s, e in paras:
        buf.append((p, s, e)); wc += len(p.split())
        if wc >= target_words:
            flush(e)
    if buf: flush(paras[-1][2])
    return chunks
```

---

## 10. Código — `src/indexer.py` (DuckDB + FAISS + dedup)

```python
import duckdb, faiss, hashlib, json
import numpy as np
from pathlib import Path
from .embedder import embed_texts
from .chunker import chunk_document

class Indexer:
    def __init__(self, tema: str, dims: int, emb_model: str, data_root="data"):
        self.dir = Path(data_root) / tema; self.dir.mkdir(parents=True, exist_ok=True)
        self.dims, self.emb_model = dims, emb_model
        self.db = duckdb.connect(str(self.dir / "brain.duckdb"))
        self.faiss_path = self.dir / "brain.faiss"
        self.db.execute("INSTALL fts"); self.db.execute("LOAD fts")
        self.db.execute("""CREATE TABLE IF NOT EXISTS chunks(
            id INTEGER PRIMARY KEY, source_file VARCHAR, source_url VARCHAR, title VARCHAR,
            chunk_index INTEGER, char_start INTEGER, char_end INTEGER,
            text VARCHAR, embedding FLOAT[], embedding_id INTEGER)""")
        self.db.execute("""CREATE TABLE IF NOT EXISTS ingestion_log(
            source_file VARCHAR PRIMARY KEY, sha256 VARCHAR, chunk_count INTEGER)""")
        self.faiss = faiss.read_index(str(self.faiss_path)) if self.faiss_path.exists() \
                     else faiss.IndexFlatIP(dims)

    def ingest(self, sources_dir, metadata_path, rebuild=False):
        if rebuild:
            self.db.execute("DELETE FROM chunks"); self.db.execute("DELETE FROM ingestion_log")
            self.faiss_path.unlink(missing_ok=True); self.faiss = faiss.IndexFlatIP(self.dims)
        meta = {Path(m["filename"]).name: m for m in json.loads(Path(metadata_path).read_text())}
        new = upd = skip = 0
        for f in sorted(Path(sources_dir).glob("*.md")):
            raw = f.read_text()
            h = meta.get(f.name, {}).get("sha256") or hashlib.sha256(raw.encode()).hexdigest()
            row = self.db.execute("SELECT sha256 FROM ingestion_log WHERE source_file=?", [f.name]).fetchone()
            if row and row[0] == h: skip += 1; continue
            if row: self.db.execute("DELETE FROM chunks WHERE source_file=?", [f.name]); upd += 1
            else: new += 1
            m = meta.get(f.name, {})
            chs = chunk_document(raw, f.name, m.get("url", ""), m.get("title", f.stem),
                                 self.cfg_words, self.cfg_overlap) if hasattr(self, "cfg_words") \
                  else chunk_document(raw, f.name, m.get("url",""), m.get("title", f.stem))
            if not chs: continue
            embs = embed_texts([c["text"] for c in chs], self.emb_model)
            base = (self.db.execute("SELECT COALESCE(MAX(id),0) FROM chunks").fetchone()[0])
            for i, (c, v) in enumerate(zip(chs, embs)):
                self.db.execute("""INSERT INTO chunks VALUES(?,?,?,?,?,?,?,?,?,?)""",
                    [base+i+1, c["source_file"], c["source_url"], c["title"], c["chunk_index"],
                     c["char_start"], c["char_end"], c["text"], v.tolist(), 0])
            self.db.execute("INSERT OR REPLACE INTO ingestion_log VALUES(?,?,?)", [f.name, h, len(chs)])
        if new or upd or rebuild:
            self._rebuild_indexes()
        return {"new": new, "updated": upd, "skipped": skip}

    def _rebuild_indexes(self):
        # FTS (BM25) — stemmer='none' para preservar español
        self.db.execute("PRAGMA create_fts_index('chunks','id','text','title',stemmer='none',lower=1,overwrite=1)")
        # FAISS — re-deriva embedding_id secuenciales desde DuckDB (fuente de verdad)
        rows = self.db.execute("SELECT id, embedding FROM chunks ORDER BY id").fetchall()
        self.faiss = faiss.IndexFlatIP(self.dims)
        mat = np.array([r[1] for r in rows], dtype=np.float32)
        if len(mat):
            self.faiss.add(mat)
            for eid, (cid, _) in enumerate(rows):
                self.db.execute("UPDATE chunks SET embedding_id=? WHERE id=?", [eid, cid])
        faiss.write_index(self.faiss, str(self.faiss_path))

    def close(self): self.db.close()
```

> **Por qué guardar el embedding en DuckDB Y en FAISS:** DuckDB es la fuente de verdad; FAISS se reconstruye desde ahí. Así un borrado de fuentes nunca corrompe el mapeo FAISS↔DuckDB (`_rebuild_indexes` re-deriva los `embedding_id`).

---

## 11. Código — `src/retriever.py` (híbrido + rerank)

```python
import duckdb, faiss
import numpy as np
from pathlib import Path
from .embedder import embed_texts

class Retriever:
    def __init__(self, tema, dims, emb_model, reranker="ms-marco-MiniLM-L-12-v2", data_root="data"):
        d = Path(data_root) / tema
        self.db = duckdb.connect(str(d / "brain.duckdb"), read_only=True)
        self.db.execute("INSTALL fts"); self.db.execute("LOAD fts")
        self.faiss = faiss.read_index(str(d / "brain.faiss"))
        self.dims, self.emb_model, self.reranker_name = dims, emb_model, reranker
        self._ranker = None

    def _bm25(self, q, n=20):
        try:
            return self.db.execute("""SELECT id, source_file, source_url, title, text,
                char_start, char_end, fts_main_chunks.match_bm25(id, ?) AS s
                FROM chunks WHERE s IS NOT NULL ORDER BY s DESC LIMIT ?""", [q, n]).fetchall()
        except Exception:
            return []

    def _vector(self, q, n=20):
        v = embed_texts([q], self.emb_model)[0].reshape(1, -1).astype(np.float32)
        scores, idx = self.faiss.search(v, min(n*3, self.faiss.ntotal))
        eids = [int(i) for i in idx[0] if i >= 0]
        if not eids: return []
        rows = self.db.execute(f"""SELECT id, source_file, source_url, title, text,
            char_start, char_end, embedding_id FROM chunks
            WHERE embedding_id IN ({','.join('?'*len(eids))})""", eids).fetchall()
        smap = {int(e): float(s) for e, s in zip(idx[0], scores[0])}
        return [(r[0], r[1], r[2], r[3], r[4], r[5], r[6], smap.get(r[7], 0)) for r in rows]

    def search(self, question, top_k=5):
        merged = {}
        for r in self._bm25(question):
            merged[r[0]] = {"id": r[0], "source_file": r[1], "source_url": r[2], "title": r[3],
                            "text": r[4], "char_start": r[5], "char_end": r[6], "score": r[7]}
        for r in self._vector(question):
            if r[0] in merged: merged[r[0]]["score"] += r[7]
            else: merged[r[0]] = {"id": r[0], "source_file": r[1], "source_url": r[2], "title": r[3],
                                  "text": r[4], "char_start": r[5], "char_end": r[6], "score": r[7]}
        cands = list(merged.values())
        # rerank cross-encoder
        try:
            from flashrank import Ranker, RerankRequest
            if self._ranker is None: self._ranker = Ranker(model_name=self.reranker_name)
            ranked = self._ranker.rerank(RerankRequest(query=question,
                passages=[{"id": c["id"], "text": c["text"], "meta": c} for c in cands]))
            out = []
            for p in ranked[:top_k]:
                c = p["meta"]; c["relevance_score"] = float(p["score"]); out.append(c)
            return out
        except Exception:
            cands.sort(key=lambda c: c["score"], reverse=True)
            for c in cands: c["relevance_score"] = c["score"]
            return cands[:top_k]
```

---

## 12. Código — `src/cli.py` (build + query)

```python
import sys, json, yaml, asyncio
from pathlib import Path
from . import research
from .indexer import Indexer
from .retriever import Retriever

def load_cfg(tema): return yaml.safe_load(Path(f"config/{tema}.yaml").read_text())

def build(tema):
    cfg = load_cfg(tema)
    out = Path("output") / tema
    for t in cfg["topics"]:
        print(f"→ research: {t}")
        research.research_topic(t, out, cfg["research_model"], cfg["search"]["results_per_topic"])
    idx = Indexer(tema, cfg["embedding_dimensions"], cfg["embedding_model"])
    idx.cfg_words = cfg["chunk_size_words"]; idx.cfg_overlap = cfg["chunk_overlap_sentences"]
    print("→ ingest:", idx.ingest(out / "sources", out / "metadata.json"))
    idx.close()

def query(tema, question, k=None):
    cfg = load_cfg(tema)
    r = Retriever(tema, cfg["embedding_dimensions"], cfg["embedding_model"], cfg["reranker_model"])
    for h in r.search(question, k or cfg["top_k_default"]):
        print(f"[{h['relevance_score']:.3f}] {h['title']}\n  {h['source_url']}\n  {h['text'][:200]}...\n")

if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "build": build(sys.argv[2])
    elif cmd == "query": query(sys.argv[2], sys.argv[3])
```

---

## 13. Uso end-to-end

```bash
source .venv/bin/activate

# 1) crea config/financiamiento_pyme.yaml (ver §4)

# 2) construye la base de conocimiento (research + ingest)
python -m src.cli build financiamiento_pyme
# → research por cada topic, scrapea, sintetiza, indexa. ~minutos. ~$0.03 en OpenRouter.

# 3) consulta con citas exactas
python -m src.cli query financiamiento_pyme "¿qué requisitos pide NAFIN para una PyME?"
# → pasajes rankeados: score, título, URL, extracto.
```

**Para servir consultas a otro proceso** (opcional): envuelve `Retriever.search` en FastAPI (un endpoint `POST /query {tema, question, top_k}`), carga los `Retriever` en memoria al arrancar, y exponlo en un puerto. Recuerda el lock de DuckDB (§14).

---

## 14. Lineamientos básicos (lo que importa de verdad)

1. **Desacopla research e índice por archivos.** Nunca los acoples por imports. `sources/*.md` + `metadata.json` es el contrato.
2. **Idempotencia por SHA-256.** Dedup de fuentes y de chunks por hash → re-correr es barato y seguro.
3. **Guarda embeddings dos veces** (DuckDB = verdad, FAISS = búsqueda). Reconstruye FAISS desde DuckDB; borrar fuentes nunca corrompe el índice.
4. **`IndexFlatIP` + vectores L2-normalizados = coseno exacto.** No uses ANN aproximado hasta tener millones de chunks.
5. **Búsqueda híbrida + rerank, siempre.** BM25 (léxico) + vector (semántico) tapan huecos mutuos; el cross-encoder (FlashRank) es lo que sube la calidad percibida. No te saltes el rerank.
6. **BM25 con `stemmer='none'`** si trabajas en español — el stemmer inglés destroza la morfología.
7. **Citas a nivel chunk con `char_start`/`char_end`.** Es la diferencia entre "parece IA" y "esto es verificable". Propaga URL + título + offsets hasta la UI.
8. **Retry + backoff en TODA llamada LLM.** 429/503 son normales bajo carga.
9. **Research offline ≠ búsqueda en vivo.** Si luego das "buscar web" a un agente en tiempo real, NO uses este pipeline pesado: usa una tool ligera con cuota y guardas anti-PII/inyección, **sin LLM**, que solo busque y scrapee, y deja que el LLM decida cuándo llamarla. (Mezclarlos rompe latencia y ensucia el corpus.)
10. **`embedding_dimensions` debe casar con el modelo; cambiar de modelo ⇒ reindexar todo.**
11. **Lock de DuckDB:** no permite escrituras concurrentes. Si un servidor tiene el `.duckdb` abierto y quieres reindexar, **cierra/descarga primero**, reindexa, recarga. Para solo leer no hay problema.
12. **Costo:** lo único que paga tokens es el LLM de research. Pon el motor pesado en un modelo barato de contexto largo (p.ej. `deepseek/deepseek-chat` en OpenRouter); como es offline, la latencia no importa, solo el costo.

---

## 15. Checklist de validación (cuándo está "listo")

- [ ] `build` corre sin errores y deja `output/<tema>/sources/*.md` + `metadata.json` + `data/<tema>/brain.{duckdb,faiss}`.
- [ ] Re-correr `build` reporta `skipped > 0` (idempotencia funciona).
- [ ] `query` devuelve pasajes con `source_url` real y `relevance_score` descendente.
- [ ] Un `query` claramente fuera de tema devuelve scores bajos / pocos resultados (no alucina relevancia).
- [ ] Borrar un `.md` de `sources/` + `ingest(rebuild=True)` → ese contenido desaparece de los resultados.
- [ ] El conteo de chunks es razonable (~3-5 chunks por fuente de tamaño medio).

---

*Guía de construcción derivada de un sistema en producción (GPT Researcher + FAISS/DuckDB/FlashRank/Ollama). Adaptada para un agente con solo OpenRouter: research loop propio + `fastembed` local reemplazan las piezas que requerían servidores externos, conservando la arquitectura probada de RAG híbrido con citas exactas.*
