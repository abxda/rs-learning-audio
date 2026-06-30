# Estrategia: 14 Cerebros Documentales para enriquecer el universo de aprendizaje
### *14 thematic "documentary brains" — deep-research enrichment strategy*

> **Principio rector:** el *UN Handbook on Remote Sensing for Agricultural Statistics* es y sigue siendo
> la **columna vertebral**. El deep research es **aditivo y siempre atribuido**; nunca reemplaza al libro,
> lo **desambigua, refuerza sus citas y sube el nivel científico** para comprender todo el libro.

---

## 0. Diagnóstico que motiva esta fase (hallazgos de la 1ª revisión)

- **Ambigüedad real:** `data-image` (y `data-volumes`, `csi-image-driver`, `oci-artifact`, `stateless-data`)
  hablan de **Kubernetes/OCI** porque provienen de la página **`howto`** (infraestructura de reproducibilidad
  del Handbook), **no** del dominio de teledetección. → Hay que **desambiguar**, citar correctamente y
  decidir si se reclasifican o se ocultan del universo de aprendizaje.
- **Citas débiles/insuficientes** en algunos conceptos; el libro **sí trae bibliografía** por capítulo
  (sección `#references`), hoy descartada en la limpieza pero recuperable de `build/01_pages/`.
- **Oportunidad:** usar las **referencias del propio libro como disparadores** de 14 búsquedas profundas
  (una por tema) para llenar huecos y elevar el rigor, en **EN+ES**.

Capacidades verificadas: ✅ Web (WebSearch/WebFetch) · ✅ DeepSeek vía OpenRouter · ✅ skill `deep-research`
· ✅ bibliografía del libro extraíble · ✅ 14 temas ya identificados (clustering).

---

## 1. Qué es un "cerebro documental" (por tema)

Una **base de conocimiento estructurada y citada** por cada uno de los 14 temas, en 3 capas:

1. **Capa columna (el libro):** capítulos/secciones del Handbook relevantes al tema + sus conceptos +
   **la bibliografía propia del libro** para esas secciones.
2. **Capa investigación (deep research):** una búsqueda profunda por tema, **disparada por las referencias
   del libro** + los conceptos del tema → fuentes externas **verificadas** (papers, FAO, guías), con cita y URL.
3. **Capa síntesis:** documento bilingüe que conecta *concepto ↔ libro ↔ ciencia externa*, con
   **desambiguaciones explícitas** y **huecos llenados**.

Salida por tema: `out/brains/<tema>.md` (bilingüe, legible) + `build/brain_<idx>.json` (estructurado, para
enriquecer) + tabla de referencias con enlaces resolubles.

---

## 2. Pipeline propuesto (nuevas etapas, cacheadas y reanudables)

### R0 · Cosecha de referencias del libro
- Re-parsear `build/01_pages/*.html` → extraer la **bibliografía** de cada capítulo (autores, año, título,
  venue, DOI/URL).
- Asociar referencias → temas vía `concepto → capítulo (cita) → cluster/tema`.
- **Salida:** `build/R0_references.json` (referencias semilla por tema).

### R1 · 14 búsquedas profundas (una por tema)
- Brief por tema = título + descripción + conceptos clave + referencias semilla.
- Deep research (skill `deep-research` o fan-out propio con WebSearch/WebFetch + DeepSeek):
  - por cada referencia semilla: localizar el artículo y trabajo relacionado/citante; **fetch** de fuentes
    autoritativas; extraer métodos/definiciones/hallazgos **con cita**.
  - + consultas temáticas (conceptos del tema) para **llenar huecos** y recoger buenas prácticas actuales.
  - **Verificación adversarial**: solo hechos con fuente y **URL que resuelve** (cero referencias alucinadas).
- Síntesis del cerebro (bilingüe): panorama del tema · aclaraciones por concepto clave · referencias
  anotadas · **desambiguaciones** · **huecos del libro que se llenan** · lista de referencias con enlaces.
- **Salida:** `out/brains/<tema>.md` + `build/brain_<idx>.json`.

### R2 · Enriquecimiento y desambiguación de conceptos
Por concepto (agrupado por tema), con su definición actual + el cerebro de su tema → DeepSeek:
- **Desambiguar:** detectar definiciones fuera de dominio/ambiguas (p. ej. `data-image`/Kubernetes) →
  aclarar con contexto + cita correcta, **reclasificar** (p. ej. tema "Plataforma y Reproducibilidad") o
  **degradar/ocultar** si es ajeno; marcar para tu decisión donde haya duda.
- **Enriquecer:** añadir una **capa científica** a la definición (más profunda, con referencias externas),
  **separada** del núcleo del Handbook ("Según el Handbook…" vs "Investigación adicional…").
- **Referenciar:** adjuntar 1–3 referencias científicas externas **verificadas** por concepto.
- **Llenar huecos / ampliar:** proponer **nuevos conceptos** que el libro referencia pero no define →
  integrarlos vía closure/lineage.
- **Salida:** ontología con campos nuevos: `references[]` (externas: título/autores/año/url),
  `disambiguation`, `enrichment.{en,es}`, y conceptos nuevos.

### R3 · Re-integración y regeneración
- Fusionar en `ontology.json`; re-correr lineage/closure para nuevos conceptos; re-emitir vault/glosario/app;
  **regenerar audio solo de lo que cambió** (XTTS+Qwen) → QA STT; re-validar.
- **App:** cada concepto muestra "📚 Profundiza" (referencias externas) + enlace al cerebro de su tema; las
  tarjetas de tema enlazan a su cerebro.

### R4 · QA y verificación
- Toda referencia externa: **URL resuelve (200)** y la cita corresponde (anti-alucinación).
- Las capas de enriquecimiento **no contradicen** al Handbook (chequeo adversarial).
- Completitud bilingüe + validadores del árbol en verde + nuevo validador "referencias resolubles".

---

## 3. Principios de diseño

- **Libro = columna, siempre.** El enriquecimiento va etiquetado como externo; la cita del Handbook es primaria.
- **Cero referencias alucinadas.** Toda cita externa se **fetcha y verifica**; la URL debe resolver.
- **Bilingüe de extremo a extremo.**
- **Desambiguar primero.** El caso `data-image`/howto/Kubernetes es el ejemplo canónico.
- **Cacheado y reanudable** como el resto del pipeline.

---

## 4. Costos/tiempos estimados

- DeepSeek: barato (síntesis + enriquecimiento por lotes) — del orden de **$1–3**.
- Web: 14 deep researches × ~10–30 fetches = el grueso del **tiempo** (no del costo).
- Audio: solo regenerar conceptos modificados.

---

## 5. Decisiones que necesito confirmar (antes de ejecutar)

1. **Profundidad de las 14 búsquedas:** exhaustiva (skill `deep-research`, más fetches/rigor, más tiempo) vs.
   moderada (fan-out acotado por tema).
2. **Conceptos de infraestructura** (`data-image`, `csi-image-driver`, `oci-artifact`, `data-volumes`,
   `stateless-data`): (a) reclasificar a un tema "Plataforma y Reproducibilidad" con nota + cita `howto`;
   (b) ocultarlos del universo de aprendizaje; (c) dejarlos y solo desambiguar.
3. **Alcance:** ¿permitir **agregar conceptos nuevos** desde referencias este ciclo, o solo **enriquecer** los
   existentes primero?
4. **Superficie en la app:** cerebros en `out/brains/<tema>.md` + "Profundiza" por concepto + enlace desde
   tarjetas de tema. ¿OK?

---

*Estrategia diseñada para la fase de enriquecimiento — el Handbook permanece como fuente canónica.*
