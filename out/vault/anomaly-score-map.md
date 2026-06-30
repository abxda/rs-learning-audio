---
id: anomaly-score-map
kind: concept
category: product
level: 4
aliases: ["anomaly score map"]
---

# Anomaly score map / Mapa de puntuación de anomalías

> **level 4** · *product* · sources: dis_china_floods

**What it is / Qué es.**

- **EN.** A [[raster|raster]] layer where each [[pixels|pixel]] represents a normalized score indicating [[deviation|deviation]] from expected [[patterns|patterns]], used to detect unusual events like floods.
- **ES.** Una capa [[raster|ráster]] donde cada píxel representa una puntuación normalizada que indica una [[deviation|desviación]] de los [[patterns|patrones]] esperados, utilizada para detectar eventos inusuales como inundaciones.

## Understand these first / Entiende esto primero
- [[map|Map]] — *product*
    - **EN.** An anomaly score map is a thematic map where each pixel shows deviation from expected patterns.
    - **ES.** Un mapa de puntuación de anomalías es un mapa temático donde cada píxel muestra la desviación de los patrones esperados.
- [[deviation|Deviation]] — *primitive*
    - **EN.** An anomaly score map quantifies deviation, assigning high scores to unusual observations.
    - **ES.** Un mapa de puntuación de anomalías cuantifica la desviación, asignando puntuaciones altas a observaciones inusuales.

## Lineage to fundamentals / Linaje hasta los fundamentos
[[data|Data]] → [[samples|Samples]] → [[classification|Classification]] → [[map|Map]] → [[anomaly-score-map|Anomaly score map]]
