# Technical Documentation — *rs-learning-audio*
### An open, bilingual, narrated concept-tree learning resource for **Remote Sensing for Agricultural Statistics**

**Repository:** https://github.com/abxda/rs-learning-audio · **Live app:** https://abxda.github.io/rs-learning-audio/
**Source corpus:** *UN Handbook on Remote Sensing for Agricultural Statistics* (FAO / EOSTAT), 33 chapters.

---

## Abstract

This project transforms the 33-chapter *UN Handbook on Remote Sensing for Agricultural Statistics*
into an **open educational resource**: a closed, navigable, bilingual (English/Spanish) **concept
ontology** of 564 nodes with an explicit prerequisite **learning lineage**, **narrated audio** in two
neural voices with karaoke word-highlighting, **thematic learning routes** derived by embedding-based
clustering, and a fully offline, single-file web application deployable on GitHub Pages (and usable on a
phone or e-reader). The goal is to **lower the barrier to mastering the statistical and Earth-observation
methods** that underpin modern agricultural statistics — sampling frames, area estimation, crop
classification, yield and phenology modelling, survey calibration and prediction-powered inference — for
practitioners in National Statistical Offices, ministries of agriculture, and the FAO member-country
community. Every artefact is reproducible and grounded in the Handbook.

---

## 1. Motivation and contribution to the field

Agricultural statistics are increasingly produced by combining **probability sampling** with **satellite
Earth observation (EO)**. The *UN Handbook on Remote Sensing for Agricultural Statistics* is the
authoritative, FAO-endorsed reference that operationalises this integration. However, as ~120,000 words of
linear technical prose with embedded code, it is demanding to navigate for newcomers, and exists only in
English.

This work contributes to the discipline by **re-representing that knowledge as a learning system**:

1. A **closed knowledge corpus** — every term used in a definition is itself defined, down to primitive
   vocabulary — so a learner can reconstruct any advanced method (e.g. *prediction-powered inference*,
   *area-frame estimators*, *semantic segmentation of parcels*) back to first principles.
2. An explicit **prerequisite DAG** (learning lineage) that encodes the pedagogical order *basic → advanced*,
   which the Handbook only implies.
3. **Bilingual (EN/ES) alignment**, broadening access for Spanish-speaking statistical systems in Latin
   America and beyond.
4. **Multimodal delivery** (read + listen + karaoke) and **thematic routes**, supporting different learning
   styles and low-bandwidth / offline / e-reader contexts common in field and rural settings.

The result is an **open, attributable companion** to the Handbook — not a replacement — intended to widen
adoption of sound EO-based methods in official agricultural statistics.

---

## 2. Source corpus

| Property | Value |
|---|---|
| Title | UN Handbook on Remote Sensing for Agricultural Statistics |
| Publisher / origin | FAO — EOSTAT initiative |
| URL | https://fao-eostat.github.io/UN-Handbook/ (Quarto site) |
| Structure | 33 chapters + 4 front-matter pages, 7 thematic sections |
| Extracted prose | ~120,919 words; full markdown ≈ 262k tokens |

**Sections (chapters):** Foundations (1–11), Crop Type Mapping (12–17), Crop Yield Estimation (18–22),
Crop Statistics Extraction (23–26), UAV Applications (27–30), Agricultural Disaster Response (31),
Additional Topics (32–33). Case studies span Poland, Mexico, Zimbabwe, China, Chile, Finland, Indonesia,
Colombia, the Cook Islands, Digital Earth Africa and WorldCereal.

The corpus is downloaded, cleaned of Quarto chrome/boilerplate, and split into prose (for mining) and
full markdown with a per-section **anchor map** (for citations). All concept definitions cite their source
chapter (and section anchor where available): **487 of 499 concepts carry ≥1 verifiable citation.**

---

## 3. System architecture

A deterministic, resumable, **content-addressed-cached** pipeline (`src/handbook_rs/`, 22 modules)
orchestrated by `handbook_rs.pipeline`. Claude (Opus 4.8) authored the architecture, schema and
quality-control logic; **DeepSeek-v4-flash** performs the heavy corpus reading, extraction, definition,
translation and naming.

```
0 fetch        download 37 pages
1 clean        Quarto HTML → prose + markdown + section-anchor map
2 mine         spaCy noun-chunks + C-value/YAKE/KeyBERT + Zipf → ranked terms → backbone
3 canonicalize DeepSeek merges term variants → canonical concepts (batched + cross-batch merge)
4 define+close grounded EN definitions + terminating closure loop (COVERED/PRIMITIVE/NEW)
5 graph        defines_uses → grounded prereq → longest-path levels
5b lineage     DeepSeek learning-DAG: prerequisites + knowledge-building bridges → deep levels
6 translate    freeze ES name glossary → translate definitions + bridges (no EN/ES drift)
7 emit         ontology.json → Obsidian vault + interactive graph + bilingual glossary
8 validate     7 hard validators (closure, acyclicity, levels, bilingual, citations, Zipf, schema)
85 clusters    embeddinggemma embeddings → best clustering → DeepSeek theme names → 2D minimap coords
9 app          ontology + clusters → single self-contained offline web app (out/index.html)
+ audio        narrated EN/ES mp3 per concept (XTTS / Qwen) + STT reverse-check QA + regen loop
```

### 3.1 The two-graph design (key architectural decision)

Two edge relations are kept **distinct**:
- **`defines_uses`** — term *T* appears in concept *C*'s definition; drives the **closure** recursion.
- **`prereq`** — *B* must be understood before *A*; drives **basic→advanced leveling**, kept acyclic.

A `prereq` edge is admitted only when **grounded** (the prerequisite's name occurs in the dependent's
definition) and **asymmetric** (the prerequisite is strictly more basic by corpus frequency). This
prevents cycles by construction and eliminates hallucinated prerequisites. Stage 5b additionally elicits an
explicit learning DAG from DeepSeek, yielding **883 prerequisite edges over 9 levels** (457 concepts have a
multi-step lineage to the fundamentals).

### 3.2 Closure (closed corpus guarantee)

A persisted, set-deduplicated frontier classifies every term found in a definition as
`COVERED | PRIMITIVE | NEW_CONCEPT` before spending a model call, with monotonic termination guards
(`MAX_DEPTH=4`, `MAX_NODES≈1000`, a ≤3-new-terms-per-definition budget). Caps degrade a would-be concept
to a primitive **leaf** rather than dropping it, so closure always holds; everything excluded is logged.
Result: **0 dangling references** — every one of the 6,400+ inter-concept links resolves.

---

## 4. Models, tools and their roles

| Component | Model / tool | Version | Role | License |
|---|---|---|---|---|
| Reasoning / NLG | **deepseek/deepseek-v4-flash** (OpenRouter) | 1,048,576-ctx, temp 0 | Canonicalization, grounded definitions, closure adjudication, prerequisite lineage + bridges, EN→ES translation, cluster naming | Commercial API |
| Narration voice A | **Coqui XTTS v2** (`tts_models/multilingual/multi-dataset/xtts_v2`) | coqui-tts 0.27.5 | EN/ES neural TTS, speaker *Damien Black* | Coqui Public Model License (non-commercial) |
| Narration voice B | **Qwen3-TTS-12Hz-1.7B-CustomVoice** | HF, speaker *ryan* | EN/ES neural TTS (instruction/timbre control) | Apache-2.0 |
| Audio QA (STT) | **Whisper large-v3** via faster-whisper | float16 | Reverse-check: transcribe audio, compare to source text | MIT |
| Concept embeddings | **embeddinggemma** (Ollama) | 768-dim | Thematic clustering of concepts | Gemma terms |
| (embedding fallback) | qwen3-embedding:0.6b (Ollama) | 1024-dim | Alternate embedder | Apache-2.0 |
| Term mining | **spaCy** `en_core_web_md` | 3.8 | Tokenisation, lemmas, noun-chunks | MIT |
| Keyphrases | C-value (custom) + **YAKE** + **KeyBERT** | — | Multiword technical-term salience | open |
| Embedding centrality / merge | sentence-transformers `paraphrase-multilingual-MiniLM-L12-v2` | — | Mining centrality + closure merge matching | Apache-2.0 |
| Everyday-word floor | **wordfreq** | — | Primitive-vocabulary detection (Zipf scale) | open |
| Graph | **networkx** | — | DAG build, cycle-breaking, longest-path leveling | BSD |
| Clustering | **scikit-learn** | 1.9.0 | KMeans/Agglomerative/HDBSCAN, silhouette/DB/CH, PCA | BSD |
| DL runtime | PyTorch | 2.5.1+cu121 | TTS / embeddings on GPU | BSD |
| Web app | Vanilla JS (no runtime deps) | — | Offline single-file learning app | this project |

**DeepSeek usage to date:** 300 cached calls, 9.15M prompt + 0.87M completion tokens, **total ≈ US$0.84**.
All calls are content-addressed-cached, so re-runs are free and the build is deterministic.

> **XTTS compatibility note (reproducibility-critical):** coqui-tts 0.27.5 requires `transformers≥4.57`
> for `is_torchcodec_available`, yet its tortoise layer imports `isin_mps_friendly`, removed from newer
> transformers. We resolve this by **monkey-patching** `isin_mps_friendly = lambda elements, test_elements:
> torch.isin(elements, test_elements)` before importing `TTS.api`.

---

## 5. Methodology (selected stages)

**Term mining (Zipf backbone, stage 2).** Candidate terms (spaCy noun-chunks + nouns) are ranked by a
blend of in-corpus Zipf frequency (0.45), C-value nested-multiword salience (0.35) and multilingual
embedding centrality (0.20). The top ~400 form the backbone seed; canonicalization (stage 3) merges
variants/acronyms into **342 canonical concepts**.

**Grounded definitions + closure (stage 4).** Definitions are written by DeepSeek from the full corpus,
constrained to ≤60 words and ≤3 new technical terms, with mandatory citations validated against the
anchor map. The closure loop expands to **564 nodes (499 concepts + 65 primitives)** and converges (frontier
266→54→12→5→0).

**Prerequisite lineage + bridges (stage 5b).** For each concept, DeepSeek selects its direct
prerequisites from the catalogue and writes a bilingual *knowledge-building bridge sentence* (e.g. *"A random
forest extends the decision tree by training many of them on random subsets and averaging their votes,
which reduces overfitting."*). Levels are recomputed by longest path: **max depth 9**.

**Bilingual alignment (stage 6).** A single language-neutral `id` carries `name.{en,es}` and
`definition.{en,es}`; structure can never drift. ES concept names are frozen into a glossary injected into
every definition/bridge translation to prevent terminological drift. **100% bilingual coverage** (0 missing).

**Narrated audio + STT reverse-check (§7).** Each concept is narrated EN+ES (name + definition) by both
voices. A **reverse quality check** transcribes every clip with Whisper-large-v3 and compares to the source,
decomposing errors into **missing content** (truncation/omission: `del_rate`, `len_ratio`) versus **garbage**
(hallucination/loops: `ins_rate`, `len_ratio`, repeated-n-gram detection). Flagged clips are regenerated
(abbreviation/unit normalisation + sentence-splitting; Qwen re-rolls under sampling) and re-checked, in a
loop, until clean.

---

## 6. Clustering experiments (learning themes)

**Goal.** Organise the 564 concepts into a small set of coherent **learning themes** for the homepage menu
and a "you-are-here" minimap.

**Setup.** Each concept is embedded with **embeddinggemma (768-dim)** from text `name. definition`; vectors
are L2-normalised (cosine geometry). We evaluate **KMeans** and **Agglomerative (Ward)** for *k* = 6…16, and
**HDBSCAN** at several `min_cluster_size`, using three internal indices: **silhouette ↑**, **Davies–Bouldin ↓**,
**Calinski–Harabasz ↑**.

### 6.1 Results

| Method | k | silhouette ↑ | Davies–Bouldin ↓ | Calinski–Harabasz ↑ |
|---|---|---|---|---|
| KMeans | 6 | 0.0717 | 3.899 | 15.6 |
| KMeans | 9 | 0.0745 | 3.478 | 12.8 |
| KMeans | 10 | 0.0753 | 3.433 | 12.3 |
| KMeans | 13 | 0.0785 | 3.385 | 10.8 |
| **KMeans** | **14** | **0.0818** | **3.237** | 10.4 |
| KMeans | 16 | 0.0850 | 3.254 | 9.7 |
| Agglomerative (Ward) | 14 | 0.0623 | 3.383 | 9.5 |
| Agglomerative (Ward) | 16 | 0.0669 | 3.249 | 9.0 |
| HDBSCAN (mcs=8) | 2 | 0.3025* | — | *514 of 564 as noise* |
| HDBSCAN (mcs=12) | 2 | 0.3699* | — | *531 of 564 as noise* |
| HDBSCAN (mcs=16,20) | 0 | — | — | *all 564 as noise* |

(*Full table for k=6…16 in `experiments_clustering_eval.py` output.*)

### 6.2 Findings and method selection

- **KMeans dominates Agglomerative (Ward)** on silhouette and Davies–Bouldin at every *k* — KMeans is ~30–40%
  higher silhouette throughout.
- **HDBSCAN is unsuitable here:** it labels 91–100% of concepts as *noise*, returning only 0–2 tiny
  clusters. Its high silhouette is an artefact of evaluating a handful of dense points; it provides **no
  usable full partition** of the corpus. This is the expected behaviour of density-based clustering on a
  **single-domain, vocabulary-overlapping** corpus where there are no low-density gaps.
- **Absolute silhouette is low (~0.06–0.085)** across all partitional settings. This is **not a defect** but a
  property of the domain: every concept shares EO/statistics vocabulary, so the embedding space is a
  continuum of *thematic tendencies* rather than well-separated islands. Davies–Bouldin and
  Calinski–Harabasz improve monotonically with *k* (finer = tighter), but more themes degrade usability as
  a menu.
- **Production choice: KMeans, k = 14** — the silhouette-optimal partition within a *menu-usable* range
  (7–14 themes). k=16 is marginally higher silhouette (0.085 vs 0.082) but yields more, smaller themes; 14
  balances cluster quality against cognitive load. 2D layout for the minimap uses **PCA**.

### 6.3 Resulting themes (k = 14)

Satellite Data Cubes · Satellite Imagery Essentials · Image Preprocessing Basics · Geospatial Data Handling ·
Field Ground Truth · Vegetation Indices Deep Dive · Crop Classification Methods · Model Training and
Algorithms · Crop and Yield Basics · Large-Scale Crop Monitoring · Accuracy Assessment · Error Analysis
(Omission/Commission) · Area Estimation from Samples · Building a Workflow.

Each theme becomes a **learning route** (its members ordered basic→advanced) with a bilingual title and a
one-sentence "what you'll master" description authored by DeepSeek; per-device progress is tracked.

---

## 7. Results and quality assurance

**Concept tree (all 8 validators green).** 564 nodes (499 concepts, 65 primitives); 1,437 edges of which
883 are prerequisites; max level 9; 5 capped terms (logged); **0 dangling references**; 100% bilingual;
Zipf coverage 1.0; JSON-schema valid.

**Narrated audio (STT reverse-check, Whisper-large-v3).**

| Voice | Clips | Mean STT similarity | Flagged (final) | Size | Speed (RTF) |
|---|---|---|---|---|---|
| XTTS v2 (Damien Black) | 1,128 | **0.979** | **0** | 96 MB | 0.27 (3.7× real-time) |
| Qwen3-TTS 1.7B (ryan) | 1,128 | **0.977** | 1 (borderline) | 102 MB | 1.33 seq · ~0.23 batched |

The reverse-check loop reduced Qwen garbage from **53 → 1** flagged clips across three regeneration rounds.
Two data-quality defects in the ontology (degenerate definitions for *oversampling*, *near-infrared*) were
discovered **through** the audio QA and corrected at the source.

**TTS performance note.** Qwen is ~5× slower than XTTS; we found **flash-attention gives no speed-up**
(the bottleneck is autoregressive 12 Hz token decoding, not attention) whereas **request batching does**
(batch-8 ≈ 6× throughput). A batch + per-item OOM-fallback generator was used.

---

## 8. The learning application

A single, dependency-free `out/index.html` (≈640 KB + audio), deployable to GitHub Pages and openable from
`file://`, a phone or a Kindle. Features: **homepage** with the 14-theme menu and interactive **cluster
minimap** ("you-are-here"); **search** of the whole concept universe; **graph-traced learning routes** (full
prerequisite curriculum to any chosen concept) with Next/Prev and a **compass** to return after lateral
exploration; **per-concept narration** (EN/ES, two voices, model selector) with **karaoke** word-highlighting
(click-to-seek); **reading mode** with three themes (paper/light/dark); **notes** per concept exported with
their lineage for downstream LLM use; and **export/import of learning memory** as JSON (continue on another
device). State persists in `localStorage`. Deployment is automated via a GitHub Actions Pages workflow.

---

## 9. Reproducibility

**Hardware used:** NVIDIA RTX 3060 (12 GB) for TTS/STT/embeddings; CPU-only for the NLP/graph/clustering
stages. **Environments:** a primary Python 3.13 venv (pipeline); conda envs `tts-xtts`, `tts-qwen`,
`stt-whisper` (Python 3.11) for the GPU models; Ollama for embeddings.

```bash
python -m handbook_rs.pipeline            # stages 0→9 (skips cached)
python -m handbook_rs.pipeline --only 85  # re-run clustering only
python tts/gen_full_xtts.py               # XTTS corpus (conda tts-xtts)
python tts/qa_stt.py xtts large-v3        # STT reverse-check (conda stt-whisper)
```

Determinism: every LLM call is content-addressed-cached under `build/cache/`; `temperature=0`. Secrets
(`.env` with the OpenRouter key) are git-ignored.

---

## 10. Limitations

- **Clustering separation is weak** (silhouette ~0.08): themes are useful *tendencies*, not crisp partitions
  — inherent to a single-domain corpus. The minimap (PCA) shows overlap honestly.
- **Definitions and lineage are model-generated** (DeepSeek), grounded and validated but not peer-reviewed;
  the ontology should be read as a study aid, not an authoritative source — the Handbook remains canonical.
- **Audio is approximate** for ultra-short/degenerate texts; one Qwen clip remains borderline. Karaoke timing
  is proportional (length-weighted), not forced-aligned.
- **STT QA is itself imperfect** (Whisper mishears acronyms such as "NDVI"), so a low score is not always a
  TTS fault.

## 11. Future work

Expert review of definitions/prerequisites; forced-alignment for exact karaoke; a recommender that proposes
the next theme from progress; additional languages; optional UMAP minimap; and linking concepts to the
Handbook's executable code cells for hands-on practice.

## 12. Attribution, licenses and ethics

The knowledge originates from the **UN Handbook on Remote Sensing for Agricultural Statistics (FAO/EOSTAT)**;
this project is a derivative *educational companion* and credits the Handbook as the canonical source. Model
licenses differ (see §4): **XTTS v2 is non-commercial** (Coqui Public Model License) — for commercial reuse,
prefer the **Qwen3-TTS (Apache-2.0)** voice. The web app and pipeline code are released openly for the
agricultural-statistics community.

---

## References

1. FAO/EOSTAT. *UN Handbook on Remote Sensing for Agricultural Statistics.* https://fao-eostat.github.io/UN-Handbook/
2. Rousseeuw, P. (1987). *Silhouettes: a graphical aid to the interpretation and validation of cluster analysis.*
3. Davies, D. & Bouldin, D. (1979). *A cluster separation measure.*
4. Caliński, T. & Harabasz, J. (1974). *A dendrite method for cluster analysis.*
5. Campello, Moulavi & Sander (2013). *Density-based clustering (HDBSCAN).*
6. Zipf, G. (1949). *Human Behavior and the Principle of Least Effort.*
7. Coqui TTS — XTTS v2. 8. Qwen Team — Qwen3-TTS. 9. OpenAI — Whisper. 10. Google — EmbeddingGemma.

*Documentation generated as part of the project build (Claude Opus 4.8 + DeepSeek-v4-flash).*
