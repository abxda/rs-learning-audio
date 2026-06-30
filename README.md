# UN Handbook → Integrated Bilingual Concept Tree
### Árbol de conceptos integrado y bilingüe del Manual de la ONU

A closed, navigable knowledge tree built from the 33 chapters of the
[UN Handbook on Remote Sensing for Agricultural Statistics](https://fao-eostat.github.io/UN-Handbook/),
ordered from the most basic ideas to the most advanced, in **English and Spanish, aligned**.
Every term used inside a definition is itself a defined node — the corpus is *closed* from
primitives up to the most advanced methods.

> **Engine:** OpenRouter → `deepseek/deepseek-v4-flash` (1M-token context).
> **Roles:** Claude orchestrates, designs the schema and does quality control; DeepSeek reads
> the corpus, extracts, defines and translates.

---

## The analytical strategy / La estrategia analítica

The key idea is to **separate two graphs** that are usually conflated:

| relation | meaning | drives |
|---|---|---|
| `defines_uses` | term *T* appears in concept *C*'s definition | **closure** (recursion) |
| `prereq` | *B* must be understood before *A* | **basic → advanced leveling** |

A `prereq` edge is admitted only when it is **grounded** (the prerequisite's name occurs in
the dependent's definition) and **asymmetric** (the prerequisite is strictly more basic by
corpus frequency). This keeps the prerequisite graph acyclic and the levels meaningful.

**Zipf's law** supplies the backbone: terms are mined and ranked by in-corpus frequency
(blended with C-value multiword salience and embedding centrality). The high-frequency head
becomes the ~300-concept spine; **closure** then recurses down every definition until it
bottoms out at everyday-vocabulary *primitives*, guaranteed to terminate by depth/word/node
caps. Nothing is dropped silently — capped terms are degraded to primitive leaves and logged.

**Pedagogical lineage (the mind map).** A dedicated DeepSeek pass builds an explicit
**learning DAG**: for every concept it picks the more-basic prerequisites a learner must
master first, and writes a *knowledge-building bridge sentence* that constructs the concept
from each prerequisite (e.g. *"A random forest extends the decision tree by training many of
them on random subsets and averaging their votes, which reduces overfitting."*). Both the
bridges and definitions are bilingual. From any concept you can read its **lineage to the
fundamentals** — the full chain back to root primitives — making this a genuine, traversable
knowledge corpus rather than a flat glossary. Current build: 883 prerequisite links, **9
levels** deep, 457 concepts with a multi-step lineage.

### Pipeline

```
0 fetch      download 37 pages
1 clean      Quarto HTML → prose + markdown + section-anchor map
2 mine       spaCy + C-value/YAKE/embedding + Zipf → ranked terms → backbone
3 canonical  DeepSeek merges term variants → canonical concepts (batched + merge)
4 define     grounded EN definitions + terminating closure loop
5 graph      defines_uses → grounded prereq → longest-path levels (basic→advanced)
5b lineage   DeepSeek learning-DAG: prerequisites + knowledge-building bridges → deep levels
6 translate  freeze ES name glossary → translate definitions + bridges (no EN/ES drift)
7 emit       ontology.json → vault/ + graph.html + glossary.md (mind map: bridges + lineage)
8 validate   7 hard validators + build report
```

Run it all:

```bash
python -m handbook_rs.pipeline           # skips cached stages
python -m handbook_rs.pipeline --force   # rebuild everything
python -m handbook_rs.pipeline --from 4  # force stage 4 onward
```

Every DeepSeek call is content-addressed and cached to `build/cache/`, so reruns are free and
the build is fully resumable.

---

> 📄 **Formal technical documentation** (sources, models, clustering experiments, architecture,
> reproducibility, attribution): see [`DOCUMENTATION.md`](DOCUMENTATION.md).

## Deliverables / Entregables (`out/`)

- **`index.html`** — a **self-contained offline learning app** (≈600 KB, no external
  dependencies, works from `file://`, a phone, or a Kindle). Search the concept universe
  (basic→advanced); pick any concept and graph analysis traces the **complete prerequisite
  route to its origin**; walk it with **Siguiente / Anterior**; wander laterally and use the
  **🧭 compass** to return to your planned route; run several routes at once; take **per-topic
  notes**; **export/import your learning memory as JSON** (continue on another device, send by
  WhatsApp); export **notes + lineage** as Markdown to feed a chatbot. Reading-first, three
  themes (paper / light / dark). **Deploy to GitHub Pages:** push `out/` (or copy `index.html`)
  to a Pages branch — it is the site root, fully static.
- **`ontology.json`** — the single source of truth (nodes, edges, bilingual fields, citations).
- **`vault/`** — Obsidian-style notes, one per concept, with `[[wikilinks]]`. Open the folder
  in Obsidian and navigate from any advanced concept down to primitives; every link resolves.
- **`graph.html`** — a self-contained interactive graph (open in a browser). Nodes colored by
  level; click a node for its aligned EN/ES definition; search box.
- **`glossary.md`** — a bilingual glossary ordered basic → advanced by level.

`build/build_report.md` summarizes the 7 validators (closure, acyclicity, level monotonicity,
bilingual completeness, citation validity, Zipf coverage, drop accounting).

---

## Resumen en español

Este proyecto convierte las 33 capítulos del Manual de la ONU sobre teledetección para
estadísticas agrícolas en un **árbol de conceptos cerrado y navegable**, de lo básico a lo
avanzado, con definiciones **alineadas en inglés y español**. Cada término usado en una
definición es a su vez un nodo definido: el corpus es *cerrado* desde los conceptos primitivos
(vocabulario cotidiano) hasta los métodos más avanzados.

La estrategia combina la **ley de Zipf** (para identificar la columna vertebral de conceptos
por frecuencia) con DeepSeek (lectura del corpus, definiciones y traducción) y una **clausura
recursiva** que garantiza que ninguna definición use términos sin definir. Se distinguen dos
grafos: el de *dependencia definicional* (impulsa la clausura) y el de *prerrequisitos*
(impulsa la jerarquía básico→avanzado), lo que evita ciclos y mantiene niveles con sentido.

Entregables en `out/`: `ontology.json` (fuente única), `vault/` (notas estilo Obsidian con
`[[enlaces]]`), `graph.html` (grafo interactivo) y `glossary.md` (glosario bilingüe).
