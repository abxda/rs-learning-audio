# deep.md — Arquitectura de cerebros: Deep Research + RAG

> **Qué es esto.** Conocimiento transferible, extraído del sistema de "cerebros de mentor" de Arena Mentor, para que **otro proyecto** lo replique. Cubre las dos mitades: (1) **Investigador** (deep research que construye el corpus) y (2) **Cerebro** (RAG que lo indexa y consulta). Incluye stack, instalación, configuración, comandos, formatos de datos, el servidor de retrieval, y las lecciones que costaron tiempo aprender.
>
> Filosofía de diseño: **dos módulos desacoplados**. El Investigador SOLO produce documentos Markdown. El Cerebro SOLO indexa y consulta. Se comunican por archivos (`sources/*.md` + `metadata.json`), nunca por imports. Cada cerebro es una carpeta autocontenida — sin servidor de BD, sin nube obligatoria.

---

## 0. Visión de 30 segundos

```
  TEMA / PERSONA
       │
       ▼
┌──────────────────┐   produce    ┌──────────────────────┐   indexa    ┌──────────────────┐
│  INVESTIGADOR    │ ───────────► │  output/<id>/        │ ──────────► │  CEREBRO (RAG)   │
│  GPT Researcher  │  archivos    │  sources/*.md        │  archivos   │  FAISS + DuckDB  │
│  + búsqueda web  │              │  metadata.json       │             │  + FlashRank     │
│  + scraping      │              │  snapshots/*.html    │             │  + Ollama embed  │
└──────────────────┘              └──────────────────────┘             └──────────────────┘
   offline, ~$0.03/cerebro                                              consulta < 1s, citas exactas
                                                                              │
                                                                        ┌─────▼──────────┐
                                                                        │ retrieval_server│
                                                                        │ FastAPI :8001   │
                                                                        │ índices en RAM  │
                                                                        └────────────────┘
```

**Dos modos de research, no confundir:**
- **Offline (`deep`/`full`):** construye el corpus permanente de un cerebro. Usa GPT Researcher + LLM. Tarda minutos. Persiste a disco.
- **Live (`fast_research_tool`):** una herramienta que el LLM llama DENTRO de una sesión para traer contexto web fresco. **No llama a ningún LLM**, solo busca/scrapea, con cuota y guardas anti-PII. Cero persistencia. (Documentado en §7; clave para no romper el SLA de latencia en vivo.)

---

## 1. Stack tecnológico

### Investigador (deep research)
| Pieza | Tecnología | Por qué |
|---|---|---|
| Motor de research | **GPT Researcher** (`gpt-researcher>=0.10`, instalado 0.14.8) | Agente autónomo: genera sub-preguntas, busca, agrega, redacta reporte |
| Búsqueda web | **DuckDuckGo** (`ddgs`, sin API key) primaria offline; **Brave Search API** fallback | DDG gratis; Brave de respaldo con cuota |
| Scraping / limpieza | **Trafilatura** (`trafilatura>=1.12`) | HTML → Markdown limpio + metadata |
| LLM | **OpenRouter** (OpenAI-compat) | un endpoint, muchos modelos |
| Embeddings | **Ollama** `qwen3-embedding:0.6b` (local) | no manda batches de tokens a un API remoto |
| Config | PyYAML · audit log en DuckDB | — |

### Cerebro (RAG)
| Pilar | Tecnología | Rol |
|---|---|---|
| Vector store | **FAISS** (`faiss-cpu`, `IndexFlatIP`) | similitud coseno exacta (vectores L2-normalizados) |
| Texto / BM25 / storage | **DuckDB** + extensión **FTS** | un archivo embebido: chunks + BM25 + log de ingesta |
| Reranker | **FlashRank** (`ms-marco-MiniLM-L-12-v2`, ~22MB) | cross-encoder, reordena por relevancia real |
| Embeddings | **Ollama** `qwen3-embedding:0.6b` (1024 dims) | mismo modelo que el investigador |
| Servidor | **FastAPI + uvicorn** (:8001) | mantiene los índices FAISS en RAM |
| Cache (opcional) | **Redis** | cache LRU de embeddings, TTL 7 días |

**Python:** el venv local usa 3.14; el Dockerfile usa 3.12-slim (+ `libgomp1` para FAISS). **Recomendación para un proyecto nuevo: fija UNA versión de Python** (3.12 es la apuesta segura por compatibilidad de wheels).

> ⚠️ **Gotcha de dependencias:** `duckdb` lo importa `searcher.py` del investigador pero **no está en su `requirements.txt`**. Agrégalo.

---

## 2. Instalación (de cero)

### 2.1 Prerequisito común: Ollama (embeddings locales)
```bash
# instalar Ollama (macOS: brew install ollama / o app oficial), luego:
ollama serve                          # demonio en :11434
ollama pull qwen3-embedding:0.6b      # ~490MB, 1024 dims
```

### 2.2 Investigador
```bash
cd modulos/investigador
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pip install duckdb                    # falta en requirements.txt
```
`.env` del investigador (solo NOMBRES de variables; los valores son secretos):
```ini
OPENAI_API_KEY=sk-or-...                       # clave OpenRouter (se espeja a GROQ_API_KEY en runtime)
OPENAI_API_BASE=https://openrouter.ai/api/v1
FAST_LLM=openrouter:google/gemini-3-flash-preview      # sub-queries (muchas, cortas) → barato y rápido
SMART_LLM=openrouter:deepseek/deepseek-v4-flash        # síntesis/reporte (motor pesado) → 1M ctx, ~10x más barato
STRATEGIC_LLM=openrouter:deepseek/deepseek-v4-flash    # planeación
RETRIEVER=duckduckgo
BRAVE_SEARCH_API_KEY=BSA...                    # fallback
BRAVE_SEARCH_RATE_LIMIT=1                       # q/s (tier free)
EMBEDDING=ollama:qwen3-embedding:0.6b
OLLAMA_BASE_URL=http://localhost:11434
OPENROUTER_API_KEY=sk-or-...                   # duplicado de OPENAI_API_KEY
```
> Las variables `FAST_LLM`/`SMART_LLM`/`STRATEGIC_LLM` son los **roles estándar de GPT Researcher** y usan sintaxis `proveedor:modelo`. La decisión de costo: el motor pesado (SMART/STRATEGIC) en DeepSeek V4 Flash; el rápido (FAST) en Gemini Flash para que el build no se eternice. Como es offline, la latencia no importa.

### 2.3 Cerebro
```bash
cd modulos/cerebro
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt        # duckdb, faiss-cpu, flashrank, numpy, fastapi, uvicorn, redis...
```
`.env` del cerebro:
```ini
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_NUM_PARALLEL=4
REDIS_URL=redis://localhost:6379/1     # opcional; sin Redis funciona igual (sin cache)
# EMBEDDING_PROVIDER=ollama            # ollama (default) | bedrock | openrouter
```

---

## 3. Configuración (formatos YAML)

### 3.1 Config del Investigador — `config/<id>.yaml`
Define QUÉ investigar.
```yaml
mentor: financiamiento                 # id; debe coincidir con el nombre de archivo y la carpeta de output
name: "Mentor de Financiamiento y Acceso a Capital"
description: "Banca de desarrollo (NAFIN/FIRA), fondos de gobierno, deuda vs capital — PyME Bajío"
topics:                                # ← lo ÚNICO que el pipeline consume de verdad
  - "financiamiento PyME México 2026 NAFIN FIRA banca de desarrollo crédito requisitos"
  - "fondos y apoyos de gobierno para empresas Bajío Guanajuato Aguascalientes 2026"
  - "deuda bancaria vs capital privado venture capital PyME México cómo elegir"
search:
  max_results_per_topic: 8             # convención/documentación: NO lo aplica el código (ojo)
  max_sources_total: 24
```
> **Gotcha:** el pipeline solo lee `topics`. Los límites `search.max_*` son convención, no se hacen cumplir; `quick` usa el flag `--max-results` (default 10).

### 3.2 Config del Cerebro — `config/<id>.yaml`
Define CÓMO indexar. (Es un archivo distinto, en el módulo cerebro.)
```yaml
mentor: financiamiento
name: "Cerebro del Mentor de Financiamiento y Acceso a Capital"
sources_dir: "/ruta/abs/a/investigador/output/financiamiento/sources"   # o relativa: ../investigador/output/<id>/sources
metadata_path: "/ruta/abs/a/investigador/output/financiamiento/metadata.json"
embedding_model: "qwen3-embedding:0.6b"
embedding_dimensions: 1024             # DEBE coincidir con el modelo de embeddings
chunk_size_words: 400                  # objetivo de palabras por chunk
chunk_overlap_sentences: 1             # frases del chunk previo que se solapan
reranker_model: "ms-marco-MiniLM-L-12-v2"
top_k_default: 5
```
Rutas relativas se resuelven contra el dir del módulo cerebro. Los datos siempre van a `data/<id>/brain.duckdb` + `data/<id>/brain.faiss`.

---

## 4. El pipeline del Investigador

Entry point: `python -m src.pipeline`. Tres subcomandos:

```bash
source .venv/bin/activate

# QUICK — sin LLM: busca + scrapea (barato, ~2-3 min). Útil para sembrar rápido.
python -m src.pipeline quick "aranceles China México 2026" --mentor tmec --max-results 10

# DEEP — GPT Researcher (con LLM): investiga a fondo UN tema, redacta reporte + archiva fuentes (~15-20 min/tema)
python -m src.pipeline deep "T-MEC revisión 2026" --mentor tmec

# FULL — itera sobre TODOS los topics del config; --mode elige quick|deep
python -m src.pipeline full --mentor financiamiento --mode deep
```

**Qué hace `deep` por dentro:**
1. Instancia `GPTResearcher(query=topic, report_type="research_report")`.
2. GPT Researcher genera sub-preguntas, busca cada una, agrega (todo interno, con su LLM).
3. `conduct_research()` → `write_report()` → escribe `sources/research_<id>_<timestamp>.md`.
4. Recorre `get_source_urls()` y scrapea cada fuente → `.md` limpio + snapshot HTML + entrada en `metadata.json`.

**Costo real medido:** un cerebro de ~50 fuentes con DeepSeek ≈ **$0.03 USD**.

---

## 5. Estructura de salida (el contrato entre módulos)

```
output/<id>/
├── sources/
│   ├── <slug>.md                          # página scrapeada, Markdown limpio (header: título/URL/fecha/autor)
│   └── research_<id>_<YYYYMMDD_HHMMSS>.md  # reporte de GPT Researcher (modo deep)
├── snapshots/
│   └── <slug>_<YYYYMMDD_HHMMSS>.html       # HTML crudo archivado (auditoría/reproducibilidad)
└── metadata.json                          # array JSON, una entrada por fuente
```

**Entrada de `metadata.json`** (el cerebro la usa para mapear archivo → url/título/hash):
```json
{
  "url": "https://...",
  "title": "60 Sites That Pay You To Write Content",
  "author": "Amjad Izhar",
  "date_published": "2025-08-16",
  "date_scraped": "2026-04-07T20:15:47Z",
  "sha256_hash": "2af9ccb1...",          // ← clave de idempotencia (re-runs saltan lo igual)
  "filename": ".../sources/<slug>.md",
  "snapshot_filename": ".../snapshots/<slug>_<ts>.html",
  "text_length": 89250                    // 0 = bloqueado por anti-bot (no se reintenta caro)
}
```

---

## 6. El módulo Cerebro: ingesta y consulta

### 6.1 Ingesta
```bash
# Incremental (default): solo procesa archivos nuevos o cambiados (por hash). Idempotente.
python -m src.brain ingest --mentor financiamiento

# Rebuild destructivo: borra chunks + ingestion_log + brain.faiss y reconstruye TODO.
# Úsalo cuando BORRASTE fuentes del corpus (p.ej. curación de basura).
python -m src.brain ingest --mentor financiamiento --rebuild
```

**`ingest_all()` paso a paso:**
1. Lee `metadata.json` → mapas `url/title/hash` por archivo.
2. `glob("*.md")` en `sources_dir`.
3. Por archivo → `ingest_document()`:
   - SHA-256 del archivo (o el de metadata).
   - **Dedup** contra `ingestion_log`: `new` / `skip` (hash igual) / `updated` (hash distinto → borra chunks viejos).
   - **Chunking** (`chunk_document`, ~400 palabras, solapamiento de 1 frase, con `char_start`/`char_end` exactos).
   - **Embedding** en lotes de 16 vía Ollama.
   - Inserta chunks+vectores en DuckDB; UPSERT al `ingestion_log`.
4. Al final, si hubo cambios: reconstruye **FTS (BM25)** y **FAISS**, persiste `brain.faiss`.
5. Invalida cache de Redis.

Devuelve `{new, updated, skipped, total_chunks}`. Resultado típico: ~50 fuentes → ~190 chunks.

**Esquema DuckDB** (un archivo `brain.duckdb` por cerebro):
```sql
CREATE TABLE chunks (
  id INTEGER PRIMARY KEY, source_file VARCHAR, source_url VARCHAR, title VARCHAR,
  chunk_index INTEGER, char_start INTEGER, char_end INTEGER,
  text VARCHAR, embedding FLOAT[], embedding_id INTEGER,
  date_indexed TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE ingestion_log (
  source_file VARCHAR PRIMARY KEY, sha256_hash VARCHAR,
  date_ingested TIMESTAMP, chunk_count INTEGER, status VARCHAR DEFAULT 'active');
```
> Los embeddings se guardan **dos veces**: en DuckDB (`FLOAT[]`, fuente de verdad para rebuild) y en FAISS (para buscar). `rebuild_faiss()` re-deriva los `embedding_id` secuenciales desde DuckDB, así un borrado nunca corrompe el mapeo FAISS↔DuckDB.

### 6.2 Consulta (búsqueda híbrida)
```bash
python -m src.brain query "reglas de origen T-MEC" --mentor tmec
python -m src.brain query "nearshoring Bajío" --mentor tmec --top-k 10 --json
python -m src.brain query "aranceles" --mentor tmec --exclude analysis-china.md
```
**Pipeline de búsqueda** (`Retriever.search`):
1. **BM25** vía DuckDB FTS (`match_bm25`), top 20. `stemmer='none', lower=1` para preservar morfología del español.
2. **Vector** vía FAISS (embebe la query con el mismo modelo, sobre-pide 3× para absorber exclusiones), top 20.
3. **Fusión** por `id` de chunk; si aparece en ambos, **suma** los scores.
4. **Rerank** con FlashRank (cross-encoder) → `relevance_score`. Si FlashRank falla, fallback ordenando por score combinado.

**Resultado** (cada item): `text, source_file, source_url, title, chunk_index, char_start, char_end, relevance_score`. Eso permite **citas exactas a nivel párrafo** (título + URL + offset de caracteres).

---

## 7. Diferencia crítica: research OFFLINE vs LIVE

| | Offline (`deep`/`full`) | Live (`fast_research_tool.py`) |
|---|---|---|
| Para qué | construir el corpus de un cerebro | inyectar contexto web fresco en una sesión en curso |
| ¿Llama a un LLM? | **Sí** (GPT Researcher) | **No** — solo busca + scrapea |
| Persistencia | sí, a disco (permanente) | **ninguna** (en memoria, efímero) |
| Latencia | minutos (no importa) | segundos (crítico, dentro del SLA) |
| Guardas | — | cuota (5 llamadas), anti-PII, sanitización anti-inyección |
| Búsqueda | Brave-primaria | DDG-primaria (cuota Brave es escasa) |

> **Lección clave:** si vas a darle "buscar en la web" a un agente en vivo, NO uses el pipeline de deep research (rompe latencia y ensucia el corpus). Usa una herramienta ligera, acotada por cuota y con guardas de PII/inyección, que solo busque y scrapee. El LLM decide *cuándo* usarla mediante el schema de la tool inyectado en su system prompt — la tool en sí no razona.

---

## 8. El servidor de retrieval (consulta en producción)

Mantiene **todos** los índices FAISS en RAM para no leer disco por query.
```bash
cd modulos/cerebro && source .venv/bin/activate
uvicorn retrieval_server:app --port 8001
```
Al arrancar hace `glob("config/*.yaml")`, salta los que no tengan `brain.duckdb`, y carga cada uno (`Indexer.open()` + `Retriever`) en un dict global.

**Endpoints:**
| Método/Ruta | Para qué |
|---|---|
| `POST /query` | búsqueda híbrida. Body: `{mentor_id, question, top_k}`. ⚠️ el campo es **`question`**, no `query`. |
| `POST /reload/{id}` | recarga un cerebro desde disco (tras reindexar) |
| `POST /unload/{id}` | descarga de RAM y **libera el lock de DuckDB** |
| `POST /reload-all` | recarga todo |
| `GET /status` | conteo de vectores por cerebro, queries servidas |
| `GET /health` | `{status, mentors}` |

```bash
curl -X POST localhost:8001/query -H 'Content-Type: application/json' \
  -d '{"mentor_id":"financiamiento","question":"opciones NAFIN para PyME","top_k":3}'
```

> ⚠️ **El lock de DuckDB es el gotcha operativo #1.** DuckDB no permite escrituras concurrentes. Mientras el servidor tiene un cerebro abierto, su `brain.duckdb` está bloqueado. Para reindexar (proceso escritor aparte): **`/unload/{id}` → ingest → `/reload/{id}`**. Para solo leer, `/status` basta.

### Flujo completo: crear un cerebro nuevo y ponerlo en vivo
```bash
# 1. Config de investigador + topics → research (DeepSeek)
python -m src.pipeline full --mentor nuevo --mode deep      # en modulos/investigador
# 2. Config de cerebro → ingesta
python -m src.brain ingest --mentor nuevo                   # en modulos/cerebro
# 3. Recargar en el servidor de retrieval
curl -X POST localhost:8001/reload/nuevo
# 4. (En el proyecto consumidor) registrar la personalidad/uso del mentor
```

---

## 9. Embeddings: proveedor intercambiable (para escalar a la nube)

`src/embedding_provider.py` abstrae el proveedor vía `EMBEDDING_PROVIDER`:
- `ollama` (default) — local, gratis, 1024 dims. Para dev / single-box.
- `bedrock` — AWS Cohere `embed-multilingual-v3`, 1024 dims (requiere `boto3`). Para producción gestionada.
- `openrouter` — `qwen/qwen3-embedding-8b`, **4096 dims** (ajusta `embedding_dimensions`).

> ⚠️ Cambiar de proveedor **cambia el espacio vectorial** → hay que **reindexar todos los cerebros**. El `embedding_dimensions` del config DEBE coincidir con el modelo.

---

## 10. Decisiones de diseño que valen oro (lecciones)

1. **Dos módulos desacoplados por archivos.** El investigador no sabe del cerebro; el cerebro no sabe del investigador. Se hablan por `sources/*.md` + `metadata.json`. Esto permite reconstruir, auditar y reemplazar cada mitad sin tocar la otra.
2. **Idempotencia por SHA-256.** Re-correr ingesta es seguro y barato: solo procesa lo nuevo/cambiado. El hash viene del `metadata.json`, con fallback a hashear el archivo.
3. **Embeddings guardados dos veces** (DuckDB + FAISS). DuckDB es la fuente de verdad; FAISS se reconstruye desde ahí. Borrar fuentes nunca corrompe el índice.
4. **`IndexFlatIP` + L2-norm = coseno exacto.** Sin ANN aproximado. A esta escala (índices de ~1MB) es instantáneo y exacto; no compliques con HNSW hasta tener millones de chunks.
5. **Búsqueda híbrida + rerank.** BM25 (léxico) + vector (semántico) + cross-encoder (relevancia real). Cada uno tapa los huecos del otro. El rerank es lo que sube la calidad percibida.
6. **BM25 con `stemmer='none'` para español.** El stemmer inglés por defecto destroza la morfología; desactívalo.
7. **Citas a nivel chunk con offsets de caracteres.** `char_start`/`char_end` permiten resaltar la frase exacta de la fuente — la diferencia entre "parece IA" y "esto es verificable".
8. **Offline ≠ Live.** Separar deep-research (LLM, persistente, lento) de la tool de búsqueda en vivo (sin LLM, efímera, con guardas) es lo que mantiene las sesiones rápidas y el corpus limpio.
9. **Curación de fuentes.** El scraping trae basura ocasional (dominios sin sentido). Tener un `--rebuild` + borrar el `.md` ofensor + reindexar es el flujo de limpieza. No sobre-cures: distinguir basura real de fuentes legítimas de bajo "glamour".
10. **Modelos por costo, validado con experimentos.** Motor de research pesado en un modelo barato de contexto largo (DeepSeek V4 Flash, ~10× más barato); el rápido en Gemini Flash. Como es offline, la latencia da igual y solo importa el costo.

---

## 11. Checklist de replicación (gotchas que cuestan tiempo)

- [ ] **Fija UNA versión de Python** (recomendado 3.12 por wheels; el venv original mezclaba 3.14 y el Docker 3.12).
- [ ] **Agrega `duckdb` al `requirements.txt`** del investigador (lo importa `searcher.py`, falta en el archivo).
- [ ] **Instala `libgomp1`** (Linux/Docker) — FAISS lo necesita (`apt-get install libgomp1`).
- [ ] **Ollama corriendo + modelo bajado** antes de ingestar o consultar (`ollama pull qwen3-embedding:0.6b`).
- [ ] **`embedding_dimensions` DEBE coincidir** con el modelo (1024 para qwen3-0.6b).
- [ ] **Libera el lock de DuckDB** (`/unload`) antes de reindexar un cerebro que está en el servidor de retrieval.
- [ ] **Sintaxis `proveedor:modelo`** para los `*_LLM` de GPT Researcher (`openrouter:deepseek/deepseek-v4-flash`).
- [ ] `OPENAI_API_KEY` del investigador se **espeja a `GROQ_API_KEY`** en runtime (herencia histórica; hoy contiene una clave OpenRouter).
- [ ] **Cambiar de proveedor de embeddings ⇒ reindexar todo.**
- [ ] **`data/`, `.venv/`, `.env`, `output/` van en `.gitignore`** — los índices se regeneran, no se commitean.

---

## 12. Referencia rápida de comandos

```bash
# ── INVESTIGADOR (construir corpus) ──
cd modulos/investigador && source .venv/bin/activate
python -m src.pipeline quick "<query>" --mentor <id> --max-results 10   # sin LLM
python -m src.pipeline deep  "<topic>" --mentor <id>                    # GPT Researcher
python -m src.pipeline full  --mentor <id> --mode deep                  # todos los topics

# ── CEREBRO (indexar + consultar) ──
cd modulos/cerebro && source .venv/bin/activate
python -m src.brain ingest --mentor <id>            # incremental
python -m src.brain ingest --mentor <id> --rebuild  # destructivo
python -m src.brain query "<pregunta>" --mentor <id> --top-k 5 [--json] [--exclude f.md]

# ── SERVIDOR DE RETRIEVAL (:8001) ──
uvicorn retrieval_server:app --port 8001
curl -X POST localhost:8001/query   -H 'Content-Type: application/json' -d '{"mentor_id":"<id>","question":"...","top_k":3}'
curl -X POST localhost:8001/unload/<id>    # antes de reindexar
curl -X POST localhost:8001/reload/<id>    # después de reindexar
curl localhost:8001/status
```

---

*Documento de transferencia de conocimiento. Sistema original: Arena Mentor (Mentorium). Stack a junio 2026: GPT Researcher + DeepSeek/Gemini vía OpenRouter (research), FAISS + DuckDB/FTS + FlashRank + Ollama qwen3-embedding (RAG). Costo medido: ~$0.03/cerebro en research, índices de ~1MB, consulta sub-segundo.*
